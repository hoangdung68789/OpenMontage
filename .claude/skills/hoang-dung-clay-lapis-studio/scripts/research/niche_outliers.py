"""RADAR XU HƯỚNG: tìm video MỚI, ĐANG LÊN trong 5 trụ cột của ICYFOX bằng YouTube Data API (không đoán từ trí nhớ).

  python niche_outliers.py [--days 7] [--pillars P1,P2,P3,P4,P5] [--per-query 25] [--min-minutes 8] [--out <thư mục>]

Cách làm:
 1. search.list (order=viewCount, publishedAfter = hôm nay - days, regionCode=US, relevanceLanguage=en) cho 2 truy vấn mỗi trụ cột.
 2. videos.list lấy lượt xem, thời lượng, ngày đăng → tính lượt xem/giờ kể từ khi đăng (đà tăng).
 3. Với mỗi kênh đăng: lấy 10 video gần nhất → trung bình (avg10). Tỉ lệ = lượt xem / avg10.
    Nhãn: VIRAL nếu >= 5 lần avg10 (định nghĩa của anh), VƯỢT TRỘI nếu >= 3 lần.
 4. Lưu outliers.json + RADAR.md (bảng theo trụ cột, link, số liệu, giờ tra).
Hạn mức: mỗi truy vấn search 100 đơn vị; 5 trụ cột x 2 truy vấn = khoảng 1.000 đơn vị + khoảng 2 đơn vị mỗi kênh (hạn mức mặc định 10.000/ngày).
Chạy lại sau 24–48 giờ trên cùng video để có số liệu 2 thời điểm (bằng chứng (b) "đang lên").
"""
import argparse
import json
import re
import statistics as st
import sys
from collections import Counter
from datetime import datetime, timedelta, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from icyfox_common import CS, api, iso_dur, now_vn, rel, utf8, yt_headers  # noqa: E402

API = "https://www.googleapis.com/youtube/v3"
QUERIES = {
    "P1": ["unsolved mystery documentary", "ocean mystery story documentary"],
    "P2": ["survival story documentary", "lost expedition true story"],
    "P3": ["ww2 untold story documentary", "war story documentary true"],
    "P4": ["disaster documentary what happened", "engineering disaster story"],
    "P5": ["ancient history documentary", "mythology story documentary"],
}
# Cảnh báo ngoài phạm vi (content-pillars.md: loại true crime, lịch sử giả, hư cấu). Video bị gắn cờ không được dùng làm ý tưởng.
FLAGS = {
    "hư cấu": r"\b(full movie|film explained|movie|zombie|thriller|horror story|fiction|animated story|creepypasta)\b",
    "lịch sử giả": r"\b(ancient aliens?|aliens?|annunaki|anunnaki|giants|atlantis is real|nephilim)\b",
    "án mạng / true crime": r"\b(murders?|killer|serial|homicide|death of|true crime|crime)\b",
    "động vật / tự nhiên": r"\b(wildlife|animal kingdom|predators?|cougar|lion|shark attack)\b",
    "trực tiếp / tổng hợp": r"(🔴|\blive\b|\bmarathon\b|\bcompilation\b)",
}
STOP = set("the a an of and in to for on at is was what how why who with from this that his her their full story documentary".split())


def latin(title):
    letters = [c for c in title if c.isalpha()]
    return not letters or sum(c.isascii() for c in letters) / len(letters) >= 0.8


def flags(title):
    return [k for k, rx in FLAGS.items() if re.search(rx, title, re.I)]


def chunks(xs, n=50):
    for i in range(0, len(xs), n):
        yield xs[i:i + n]


def main():
    utf8()
    ap = argparse.ArgumentParser()
    ap.add_argument("--days", type=int, default=7)
    ap.add_argument("--pillars", default="P1,P2,P3,P4,P5")
    ap.add_argument("--per-query", type=int, default=25)
    ap.add_argument("--min-minutes", type=float, default=8)
    ap.add_argument("--out")
    ap.add_argument("--min-views", type=int, default=20000, help="ngưỡng lượt xem tối thiểu cho ứng viên ý tưởng")
    ap.add_argument("--rerender", help="đọc lại outliers.json có sẵn, không gọi API")
    a = ap.parse_args()
    pillars = [p.strip().upper() for p in a.pillars.split(",") if p.strip().upper() in QUERIES]
    if a.rerender:
        j = json.loads(Path(a.rerender).read_text(encoding="utf-8"))
        rows = [v for v in j.pop("videos") if latin(v["title"])]
        j.setdefault("min_minutes", a.min_minutes)
        render(rows, j, Path(a.rerender).parent, pillars, a.min_views)
        return
    h, _ = yt_headers()
    now = datetime.now(timezone.utc)
    after = (now - timedelta(days=a.days)).strftime("%Y-%m-%dT%H:%M:%SZ")
    found, units = {}, 0
    for p in pillars:
        for q in QUERIES[p]:
            ok, j = api(h, f"{API}/search", {"part": "snippet", "type": "video", "q": q, "order": "viewCount",
                                             "publishedAfter": after, "maxResults": a.per_query,
                                             "regionCode": "US", "relevanceLanguage": "en"}, fatal=False)
            units += 100
            if not ok:
                print(f"  lỗi search '{q}': {j}")
                continue
            for it in j.get("items", []):
                vid = it["id"].get("videoId")
                if vid:
                    found.setdefault(vid, {"pillars": set(), "queries": set()})
                    found[vid]["pillars"].add(p)
                    found[vid]["queries"].add(q)
    ids = list(found)
    vids = {}
    for c in chunks(ids):
        ok, j = api(h, f"{API}/videos", {"part": "snippet,statistics,contentDetails", "id": ",".join(c)}, fatal=False)
        units += 1
        for v in (j.get("items", []) if ok else []):
            dur = iso_dur(v["contentDetails"].get("duration"))
            lang = (v["snippet"].get("defaultAudioLanguage") or v["snippet"].get("defaultLanguage") or "en").lower()
            if dur < a.min_minutes * 60 or not lang.startswith("en") or not latin(v["snippet"]["title"]):
                continue
            pub = datetime.fromisoformat(v["snippet"]["publishedAt"].replace("Z", "+00:00"))
            hours = max((now - pub).total_seconds() / 3600, 1)
            views = int(v["statistics"].get("viewCount", 0))
            vids[v["id"]] = {"id": v["id"], "title": v["snippet"]["title"], "channel": v["snippet"]["channelTitle"],
                             "channel_id": v["snippet"]["channelId"], "published": v["snippet"]["publishedAt"],
                             "minutes": round(dur / 60, 1), "views": views, "views_per_hour": round(views / hours, 1),
                             "likes": int(v["statistics"].get("likeCount", 0)),
                             "comments": int(v["statistics"].get("commentCount", 0)),
                             "pillars": sorted(found[v["id"]]["pillars"]), "url": f"https://www.youtube.com/watch?v={v['id']}"}
    # Kênh: số sub + trung bình 10 video gần nhất
    chans = {}
    cids = sorted({v["channel_id"] for v in vids.values()})
    for c in chunks(cids):
        ok, j = api(h, f"{API}/channels", {"part": "statistics,contentDetails", "id": ",".join(c)}, fatal=False)
        units += 1
        for ch in (j.get("items", []) if ok else []):
            chans[ch["id"]] = {"subs": int(ch["statistics"].get("subscriberCount", 0) or 0),
                               "uploads": ch["contentDetails"]["relatedPlaylists"]["uploads"]}
    for cid, ch in chans.items():
        ok, j = api(h, f"{API}/playlistItems", {"part": "contentDetails", "playlistId": ch["uploads"], "maxResults": 12}, fatal=False)
        units += 1
        recent = [it["contentDetails"]["videoId"] for it in (j.get("items", []) if ok else [])]
        ok, j = api(h, f"{API}/videos", {"part": "statistics", "id": ",".join(recent)}, fatal=False) if recent else (False, {})
        units += 1
        views = {it["id"]: int(it["statistics"].get("viewCount", 0)) for it in (j.get("items", []) if ok else [])}
        ch["recent"] = [views[v] for v in recent if v in views]
    for v in vids.values():
        ch = chans.get(v["channel_id"], {})
        others = [x for x in ch.get("recent", []) if x != v["views"]][:10]
        avg10 = st.mean(others) if len(others) >= 5 else None
        v["channel_subs"] = ch.get("subs")
        v["avg10"] = round(avg10) if avg10 else None
        v["ratio"] = round(v["views"] / avg10, 2) if avg10 else None
        v["label"] = "VIRAL" if v["ratio"] and v["ratio"] >= 5 else "VƯỢT TRỘI" if v["ratio"] and v["ratio"] >= 3 else ""
    stamp = now_vn()
    out = Path(a.out) if a.out else CS / "research" / f"{stamp:%Y-%m-%d}-radar"
    rows = sorted(vids.values(), key=lambda v: -v["views_per_hour"])
    meta = {"checked_at_vn": stamp.strftime("%Y-%m-%d %H:%M"), "days": a.days, "published_after_utc": after,
            "min_minutes": a.min_minutes, "quota_units_est": units}
    render(rows, meta, out, pillars, a.min_views)


def render(rows, meta, out, pillars, min_views):
    for v in rows:
        v["flags"] = flags(v["title"])
    out.mkdir(parents=True, exist_ok=True)
    (out / "outliers.json").write_text(json.dumps({**meta, "videos": rows}, ensure_ascii=False, indent=1), encoding="utf-8")
    L = [f"# Radar xu hướng ICYFOX — tra lúc {meta['checked_at_vn']} (giờ Việt Nam)", "",
         f"Nguồn: YouTube Data API v3 (search.list order=viewCount, regionCode=US, tiếng Anh, video đăng sau {meta['published_after_utc']}, "
         f"dài >= {meta['min_minutes']} phút). Ước tính hạn mức đã dùng: {meta['quota_units_est']} đơn vị.",
         "Nhãn theo định nghĩa của anh: VIRAL = lượt xem >= 5 lần trung bình 10 video gần nhất của chính kênh đó; VƯỢT TRỘI >= 3 lần.",
         "Cột Cảnh báo: chủ đề ngoài phạm vi ICYFOX (hư cấu, lịch sử giả, true crime...) → không dùng làm ý tưởng.",
         "Một lần tra = 1 thời điểm. Muốn gắn nhãn 'ĐANG LÊN – ĐÃ KIỂM CHỨNG' phải chạy lại sau 24–48 giờ và so lượt xem.", ""]
    good = [v for v in rows if v["label"] and not v["flags"] and v["views"] >= min_views]
    L += [f"## ỨNG VIÊN Ý TƯỞNG (có nhãn, không bị cờ, >= {min_views:,} lượt xem)", "",
          "| Video | Kênh | Trụ cột | Đăng | Lượt xem | Xem/giờ | x TB10 | Nhãn |", "|---|---|---|---|---|---|---|---|"]
    L += [f"| [{v['title'][:80]}]({v['url']}) | {v['channel']} | {','.join(v['pillars'])} | {v['published'][:10]} | {v['views']:,} | "
          f"{v['views_per_hour']:,} | {v['ratio']} | {v['label']} |" for v in good] or ["| (không có) | | | | | | | |"]
    L.append("")
    for p in pillars:
        pv = [v for v in rows if p in v["pillars"]][:12]
        L += [f"## {p}", "", "| # | Video | Kênh (sub) | Đăng | Phút | Lượt xem | Xem/giờ | x TB10 | Nhãn | Cảnh báo |",
              "|---|---|---|---|---|---|---|---|---|---|"]
        for i, v in enumerate(pv, 1):
            L.append(f"| {i} | [{v['title'][:70]}]({v['url']}) | {v['channel']} ({v['channel_subs'] or '?'}) | {v['published'][:10]} | "
                     f"{v['minutes']} | {v['views']:,} | {v['views_per_hour']:,} | {v['ratio'] or '-'} | {v['label']} | {', '.join(v['flags'])} |")
        L.append("")
        hot = [v for v in pv if not v["flags"]]
        words = Counter(w for v in hot for w in re.findall(r"[a-z']+", v["title"].lower()) if w not in STOP and len(w) > 3)
        L += ["Từ hay gặp trong tiêu đề (bỏ video bị cờ): " + ", ".join(f"{w} ({c})" for w, c in words.most_common(10)), ""]
    L += ["## Việc tiếp theo (autopilot)", "",
          f"- {len(good)} ứng viên ở bảng đầu. Đưa vào `channel-studio/ideas/IDEA_BANK.md` kèm link, số liệu, giờ tra; chấm điểm theo references/analytics-loop.md.",
          "- Chạy lại radar sau 24–48 giờ: video nào tiếp tục tăng thì đủ 2 bằng chứng (nhãn 'ĐANG LÊN – ĐÃ KIỂM CHỨNG').", ""]
    (out / "RADAR.md").write_text("\n".join(L), encoding="utf-8")
    print(f"Đã lưu {rel(out / 'RADAR.md')} ({len(rows)} video, {len(good)} ứng viên ý tưởng)")
    for v in good[:10]:
        print(f"  {v['label']:9} x{v['ratio']:<6} {v['views']:>9,} view  {v['pillars']}  {v['title'][:70]}")


if __name__ == "__main__":
    main()
