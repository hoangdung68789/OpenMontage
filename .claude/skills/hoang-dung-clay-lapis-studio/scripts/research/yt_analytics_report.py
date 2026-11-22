"""BÁO CÁO SỐ LIỆU KÊNH ICYFOX từ YouTube Analytics API + Data API. Tự tìm video thắng và rút quy luật.

  python yt_analytics_report.py [--days 28] [--studio-csv "Table data.csv"] [--replay data.json] [--out <thư mục>]

Lấy (đã thử thật trên kênh ICYFOX ngày 22/11/2026):
 - Tổng theo ngày: views, estimatedMinutesWatched, averageViewDuration, subscribersGained, subscribersLost
 - Từng video (dimension video): views, estimatedMinutesWatched, averageViewDuration, averageViewPercentage,
   subscribersGained, likes, shares, comments; thêm số liệu 7 ngày đầu của từng video để so công bằng
 - Nguồn lưu lượng (insightTrafficSourceType), quốc gia (country), loại nội dung (creatorContentType)
 - Giữ chân người xem (elapsedVideoTimeRatio + audienceWatchRatio, bắt buộc lọc video==ID) cho 3 video dài tốt nhất
KHÔNG có qua API (đã thử 22/11/2026): số lần hiển thị thumbnail và CTR → lấy từ YouTube Studio (Analytics > Advanced mode > Export,
  file "Table data.csv") rồi đưa vào --studio-csv. Doanh thu (estimatedRevenue) cần quyền yt-analytics-monetary.readonly (hiện chưa có).
Ghi: channel-studio/analytics/reports/<ngày>/report.md + data.json, cập nhật analytics/WINNERS.md.
"""
import argparse
import csv
import json
import statistics as st
import sys
from datetime import date, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from icyfox_common import CS, api, iso_dur, load_json, now_vn, rel, utf8, yt_headers  # noqa: E402

DATA = "https://www.googleapis.com/youtube/v3"
ANA = "https://youtubeanalytics.googleapis.com/v2/reports"
SHORT_MAX_S = 180
WIN, LOSE = 2.0, 0.5   # video thắng: >= 2 lần trung vị cùng loại; video yếu: <= 0,5 lần (NHẬN ĐỊNH, xem analytics-loop.md)
VIDEO_METRICS = "views,estimatedMinutesWatched,averageViewDuration,averageViewPercentage,subscribersGained,likes,shares,comments"


def table(j):
    cols = [c["name"] for c in j.get("columnHeaders", [])]
    return [dict(zip(cols, r)) for r in j.get("rows") or []]


def report_q(h, start, end, **p):
    ok, j = api(h, ANA, {"ids": "channel==MINE", "startDate": str(start), "endDate": str(end), **p}, fatal=False)
    return table(j) if ok else {"error": j}


def fetch(days):
    h, scopes = yt_headers()
    end = now_vn().date() - timedelta(days=1)
    start = end - timedelta(days=days - 1)
    raw = {"fetched_at_vn": now_vn().strftime("%Y-%m-%d %H:%M"), "start": str(start), "end": str(end), "scopes": scopes}
    ok, j = api(h, f"{DATA}/channels", {"part": "snippet,statistics,contentDetails", "mine": "true"})
    ch = j["items"][0]
    raw["channel"] = {"id": ch["id"], "title": ch["snippet"]["title"], "stats": ch["statistics"]}
    uploads, token = [], None
    while True:
        ok, j = api(h, f"{DATA}/playlistItems", {"part": "contentDetails", "maxResults": 50, "pageToken": token or "",
                                                  "playlistId": ch["contentDetails"]["relatedPlaylists"]["uploads"]}, fatal=False)
        if not ok:
            break
        uploads += [it["contentDetails"]["videoId"] for it in j.get("items", [])]
        token = j.get("nextPageToken")
        if not token or len(uploads) >= 500:
            break
    videos = {}
    for i in range(0, len(uploads), 50):
        ok, j = api(h, f"{DATA}/videos", {"part": "snippet,contentDetails,statistics,status", "id": ",".join(uploads[i:i + 50])})
        for v in j.get("items", []):
            videos[v["id"]] = {"id": v["id"], "title": v["snippet"]["title"], "published": v["snippet"]["publishedAt"][:10],
                               "seconds": iso_dur(v["contentDetails"]["duration"]), "privacy": v["status"]["privacyStatus"],
                               "lifetime_views": int(v["statistics"].get("viewCount", 0))}
    raw["videos"] = videos
    raw["daily"] = report_q(h, start, end, metrics="views,estimatedMinutesWatched,averageViewDuration,subscribersGained,subscribersLost",
                            dimensions="day", sort="day")
    raw["per_video"] = report_q(h, start, end, metrics=VIDEO_METRICS, dimensions="video", sort="-estimatedMinutesWatched", maxResults=200)
    raw["per_video_lifetime"] = report_q(h, "2020-01-01", end, metrics=VIDEO_METRICS, dimensions="video",
                                         sort="-estimatedMinutesWatched", maxResults=200)
    raw["traffic"] = report_q(h, start, end, metrics="views,estimatedMinutesWatched", dimensions="insightTrafficSourceType",
                              sort="-estimatedMinutesWatched")
    raw["country"] = report_q(h, start, end, metrics="views,estimatedMinutesWatched", dimensions="country",
                              sort="-estimatedMinutesWatched", maxResults=10)
    raw["content_type"] = report_q(h, start, end, metrics="views,estimatedMinutesWatched", dimensions="creatorContentType")
    raw["revenue"] = report_q(h, start, end, metrics="estimatedRevenue,estimatedAdRevenue,playbackBasedCpm")
    # 7 ngày đầu của từng video công khai (tối đa 60 video mới nhất)
    first7 = {}
    for v in sorted(videos.values(), key=lambda v: v["published"], reverse=True)[:60]:
        pub = date.fromisoformat(v["published"])
        if v["privacy"] != "public" or pub + timedelta(days=7) > end:
            continue
        rows = report_q(h, pub, pub + timedelta(days=6), metrics="views,estimatedMinutesWatched,subscribersGained",
                        filters=f"video=={v['id']}")
        if isinstance(rows, list) and rows:
            first7[v["id"]] = rows[0]
    raw["first7"] = first7
    # Giữ chân: 3 video dài nhiều giờ xem nhất (trọn đời)
    life = raw["per_video_lifetime"] if isinstance(raw["per_video_lifetime"], list) else []
    longs = [r["video"] for r in life if videos.get(r["video"], {}).get("seconds", 0) > SHORT_MAX_S][:3]
    raw["retention"] = {vid: report_q(h, "2020-01-01", end, metrics="audienceWatchRatio,relativeRetentionPerformance",
                                      dimensions="elapsedVideoTimeRatio", filters=f"video=={vid}") for vid in longs}
    return raw


def studio_csv(path):
    """Đọc file 'Table data.csv' xuất từ YouTube Studio (Advanced mode). Khớp cột theo tên, không phụ thuộc thứ tự."""
    out = {}
    with open(path, encoding="utf-8-sig") as f:
        for r in csv.DictReader(f):
            vid = r.get("Content") or r.get("Video") or ""
            if len(vid) != 11:
                continue
            imp = next((r[k] for k in r if k and k.strip().lower() == "impressions"), "")
            ctr = next((r[k] for k in r if k and "click-through" in k.lower()), "")
            out[vid] = {"impressions": imp, "ctr_percent": ctr}
    return out


def med(xs):
    xs = [x for x in xs if x is not None]
    return st.median(xs) if xs else None


def analyze(raw, studio=None):
    vids = raw.get("videos", {})
    vmap = load_json(CS / "analytics" / "video_map.json", {})
    per = {r["video"]: r for r in raw.get("per_video", []) if isinstance(raw.get("per_video"), list)}
    life = {r["video"]: r for r in raw.get("per_video_lifetime", []) if isinstance(raw.get("per_video_lifetime"), list)}
    f7 = raw.get("first7", {})
    rows = []
    for vid, v in vids.items():
        m = vmap.get(vid, {})
        L, P, F = life.get(vid, {}), per.get(vid, {}), f7.get(vid, {})
        kind = "short" if v["seconds"] <= SHORT_MAX_S else "long"
        rows.append({"id": vid, "title": v["title"], "published": v["published"], "kind": kind, "minutes": round(v["seconds"] / 60, 1),
                     "privacy": v["privacy"], "pillar": m.get("pillar", ""), "series": m.get("series", ""), "episode": m.get("episode", ""),
                     "hook": m.get("hook", ""), "dir": m.get("video_dir", ""),
                     "views_period": P.get("views", 0), "hours_period": round(P.get("estimatedMinutesWatched", 0) / 60, 1),
                     "views_life": L.get("views", v.get("lifetime_views", 0)), "hours_life": round(L.get("estimatedMinutesWatched", 0) / 60, 1),
                     "avd_s": L.get("averageViewDuration"), "avp": L.get("averageViewPercentage"),
                     "subs_life": L.get("subscribersGained", 0),
                     "views_7d": F.get("views"), "hours_7d": round(F["estimatedMinutesWatched"] / 60, 1) if F else None,
                     "subs_7d": F.get("subscribersGained"), **((studio or {}).get(vid, {}))})
    for kind, key in (("long", "hours_7d"), ("short", "views_7d")):
        grp = [r for r in rows if r["kind"] == kind]
        m = med([r[key] for r in grp])
        for r in grp:
            r["score"] = round(r[key] / m, 2) if (m and r[key] is not None) else None
            r["verdict"] = "THẮNG" if r["score"] and r["score"] >= WIN and len(grp) >= 3 else \
                           "YẾU" if r["score"] is not None and r["score"] <= LOSE and len(grp) >= 3 else ""
    groups = {}
    for dim in ("pillar", "series", "hook"):
        g = {}
        for r in rows:
            if r["kind"] == "long" and r[dim]:
                g.setdefault(r[dim], []).append(r)
        groups[dim] = {k: {"videos": len(v), "median_hours_7d": med([x["hours_7d"] for x in v]), "median_avp": med([x["avp"] for x in v])}
                       for k, v in g.items()}
    return rows, groups


def write(raw, rows, groups, out):
    out.mkdir(parents=True, exist_ok=True)
    (out / "data.json").write_text(json.dumps({"raw": raw, "rows": rows, "groups": groups}, ensure_ascii=False, indent=1), encoding="utf-8")
    daily = raw.get("daily") if isinstance(raw.get("daily"), list) else []
    tot_h = round(sum(r.get("estimatedMinutesWatched", 0) for r in daily) / 60, 1)
    tot_v = sum(r.get("views", 0) for r in daily)
    subs = sum(r.get("subscribersGained", 0) - r.get("subscribersLost", 0) for r in daily)
    ch = raw.get("channel", {})
    L = [f"# Báo cáo kênh {ch.get('title', 'ICYFOX')} — {raw.get('start')} → {raw.get('end')}", "",
         f"Nguồn: YouTube Analytics API v2 + Data API v3, lấy lúc {raw.get('fetched_at_vn')} (giờ Việt Nam). Số liệu YouTube thường trễ 1–3 ngày.", "",
         "## Tổng quan kỳ này", "",
         f"- Lượt xem: {tot_v:,} · Giờ xem: {tot_h:,} · Sub ròng: {subs:+,} · Tổng sub hiện tại: {ch.get('stats', {}).get('subscriberCount', '?')}",
         f"- Video trên kênh: {len(rows)} ({sum(r['kind'] == 'long' for r in rows)} video dài, {sum(r['kind'] == 'short' for r in rows)} Shorts)"]
    rev = raw.get("revenue")
    L.append("- Doanh thu: " + (f"{rev}" if isinstance(rev, list) and rev else
                                "chưa lấy được (cần quyền yt-analytics-monetary.readonly sau khi vào YPP; xem analytics-loop.md)"))
    if not rows:
        L += ["", "**Kênh chưa có video.** Ra quyết định chủ đề bằng radar xu hướng (`niche_outliers.py`) và số liệu đối thủ (`yt_api_channel.py`)."]
    for kind, title, key in (("long", "Video dài (so bằng giờ xem 7 ngày đầu)", "hours_7d"), ("short", "Shorts (so bằng lượt xem 7 ngày đầu)", "views_7d")):
        grp = sorted([r for r in rows if r["kind"] == kind], key=lambda r: -(r[key] or 0))
        if not grp:
            continue
        L += ["", f"## {title}", "", "| Video | Đăng | Trụ cột / series | 7 ngày | x trung vị | Giữ chân TB | Thời gian xem TB | Sub (trọn đời) | CTR (Studio) | Kết luận |",
              "|---|---|---|---|---|---|---|---|---|---|"]
        for r in grp:
            L.append(f"| [{r['title'][:60]}](https://youtu.be/{r['id']}) | {r['published']} | {r['pillar']} {r['series']} {r['episode']} | "
                     f"{r[key] if r[key] is not None else '-'} | {r.get('score') or '-'} | {r['avp'] if r['avp'] is not None else '-'}% | "
                     f"{r['avd_s'] or '-'} s | {r['subs_life']} | {r.get('ctr_percent', '-')} | {r.get('verdict', '')} |")
    for name, key in (("Nguồn lưu lượng", "traffic"), ("Quốc gia (top 10)", "country"), ("Loại nội dung", "content_type")):
        data = raw.get(key)
        if isinstance(data, list) and data:
            cols = list(data[0])
            L += ["", f"## {name}", "", "| " + " | ".join(cols) + " |", "|" + "---|" * len(cols)] + \
                 ["| " + " | ".join(str(r[c]) for c in cols) + " |" for r in data]
    ret = raw.get("retention", {})
    if ret:
        L += ["", "## Giữ chân người xem (3 video dài nhiều giờ xem nhất)", ""]
        for vid, pts in ret.items():
            if not isinstance(pts, list) or not pts:
                continue
            at = {round(p["elapsedVideoTimeRatio"], 2): p["audienceWatchRatio"] for p in pts}
            pick = lambda x: next((v for k, v in sorted(at.items()) if k >= x), None)  # noqa: E731
            drops = sorted(((pts[i]["audienceWatchRatio"] - pts[i + 1]["audienceWatchRatio"], pts[i + 1]["elapsedVideoTimeRatio"])
                            for i in range(len(pts) - 1)), reverse=True)[:2]
            L.append(f"- {vids_title(raw, vid)}: còn {pct(pick(0.1))} ở 10%, {pct(pick(0.25))} ở 25%, {pct(pick(0.5))} ở 50%, "
                     f"{pct(pick(0.9))} ở 90%. Rơi mạnh nhất quanh mốc " + ", ".join(f"{d[1] * 100:.0f}%" for d in drops))
    for dim, label in (("pillar", "trụ cột"), ("series", "series"), ("hook", "kiểu hook")):
        g = groups.get(dim, {})
        if g:
            L += ["", f"## Theo {label} (video dài)", "", "| Nhóm | Số video | Trung vị giờ xem 7 ngày | Trung vị giữ chân % |", "|---|---|---|---|"]
            L += [f"| {k} | {v['videos']} | {v['median_hours_7d']} | {v['median_avp']} |" for k, v in sorted(g.items(), key=lambda kv: -(kv[1]['median_hours_7d'] or 0))]
    winners = [r for r in rows if r.get("verdict") == "THẮNG"]
    L += ["", "## Việc tiếp theo (bắt buộc, theo analytics-loop.md)", "",
          f"- Video thắng: {len(winners)}. Mỗi video thắng → ghi quy luật vào WINNERS.md và tạo 2–3 ý tưởng 'cùng gen' (khác chủ đề) trong IDEA_BANK.",
          "- Video yếu → ghi giả thuyết nguyên nhân (tiêu đề/thumbnail/hook/chủ đề) và 1 thử nghiệm cho video kế tiếp.",
          "- Đối chiếu ngưỡng quyết định trong PLAN.md / KE_HOACH_90_NGAY.md mục 5."]
    (out / "report.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    W = CS / "analytics" / "WINNERS.md"
    W.parent.mkdir(parents=True, exist_ok=True)
    old = W.read_text(encoding="utf-8") if W.exists() else "# Video thắng của ICYFOX và quy luật rút ra\n\nAutopilot thêm mục mới ở cuối sau mỗi báo cáo. Cột 'Quy luật' do AI viết sau khi xem video.\n"
    if winners:
        old += f"\n## Báo cáo {raw.get('end')}\n\n| Video | Loại | x trung vị | Giữ chân % | Trụ cột / series | Quy luật (AI điền) |\n|---|---|---|---|---|---|\n"
        old += "".join(f"| [{r['title'][:60]}](https://youtu.be/{r['id']}) | {r['kind']} | {r['score']} | {r['avp']} | {r['pillar']} {r['series']} | |\n" for r in winners)
    W.write_text(old, encoding="utf-8")
    print(f"Đã lưu {rel(out / 'report.md')} ({len(rows)} video, {len(winners)} video thắng)")


def vids_title(raw, vid):
    return raw.get("videos", {}).get(vid, {}).get("title", vid)[:60]


def pct(x):
    return f"{x * 100:.0f}%" if x is not None else "?"


def main():
    utf8()
    ap = argparse.ArgumentParser()
    ap.add_argument("--days", type=int, default=28)
    ap.add_argument("--studio-csv")
    ap.add_argument("--replay", help="phân tích lại data.json đã lưu (không gọi API)")
    ap.add_argument("--out")
    a = ap.parse_args()
    raw = json.loads(Path(a.replay).read_text(encoding="utf-8"))["raw"] if a.replay else fetch(a.days)
    studio = studio_csv(a.studio_csv) if a.studio_csv else None
    rows, groups = analyze(raw, studio)
    out = Path(a.out) if a.out else CS / "analytics" / "reports" / now_vn().strftime("%Y-%m-%d")
    write(raw, rows, groups, out)


if __name__ == "__main__":
    main()
