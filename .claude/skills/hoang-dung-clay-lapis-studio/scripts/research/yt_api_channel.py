"""Phân tích kênh đối thủ bằng YouTube Data API v3 (MẶC ĐỊNH cho mọi phân tích đối thủ).

    python yt_api_channel.py <@handle | URL kênh | channel_id> [thư_mục_kết_quả] [số_video=100]

Dùng OAuth của kênh ICYFOX (YT_CLIENT_ID, YT_CLIENT_SECRET, YT_REFRESH_TOKEN). Đọc từ biến môi trường,
hoặc từ OpenMontage/.env trên máy local. Không in khóa.
Hạn mức: channels.list, playlistItems.list, videos.list mỗi lần gọi 1 đơn vị. 100 video tốn khoảng 5 đơn vị.
Đầu ra: <dir>/<handle>_api.json (từng video) + <dir>/<handle>_api.md (bảng tóm tắt).
"""
import json
import os
import re
import statistics as st
import sys
from datetime import datetime, timezone
from pathlib import Path

import requests

API = "https://www.googleapis.com/youtube/v3"


def load_env():
    for p in [Path.cwd()] + list(Path(__file__).resolve().parents):
        f = p / ".env"
        if f.is_file() and (p / "AGENT_GUIDE.md").exists() or (f.is_file() and p == Path.cwd()):
            for line in f.read_text(encoding="utf-8", errors="ignore").splitlines():
                if "=" in line and not line.strip().startswith("#"):
                    k, v = line.split("=", 1)
                    if k.strip() and v.strip() and not os.environ.get(k.strip()):
                        os.environ[k.strip()] = v.strip().strip('"').strip("'")
            return


def token():
    need = ["YT_CLIENT_ID", "YT_CLIENT_SECRET", "YT_REFRESH_TOKEN"]
    if any(not os.environ.get(k) for k in need):
        sys.exit("Thiếu YT_CLIENT_ID / YT_CLIENT_SECRET / YT_REFRESH_TOKEN (xem channel-studio/config/HUONG_DAN_KHOA_API.md)")
    r = requests.post("https://oauth2.googleapis.com/token", data={
        "client_id": os.environ["YT_CLIENT_ID"], "client_secret": os.environ["YT_CLIENT_SECRET"],
        "refresh_token": os.environ["YT_REFRESH_TOKEN"], "grant_type": "refresh_token"}, timeout=30)
    r.raise_for_status()
    return {"Authorization": "Bearer " + r.json()["access_token"]}


def get(h, path, **params):
    r = requests.get(f"{API}/{path}", headers=h, params=params, timeout=30)
    if not r.ok:
        sys.exit(f"LỖI API {path}: {r.status_code} {r.text[:200]}")
    return r.json()


def resolve_channel(h, ref):
    ref = ref.strip()
    m = re.search(r"(UC[\w-]{22})", ref)
    params = {"part": "snippet,statistics,contentDetails"}
    if m:
        params["id"] = m.group(1)
    else:
        handle = re.sub(r"^https?://(www\.)?youtube\.com/", "", ref).split("/")[0]
        params["forHandle"] = handle if handle.startswith("@") else "@" + handle
    items = get(h, "channels", **params).get("items", [])
    if not items:
        sys.exit(f"Không tìm thấy kênh: {ref}")
    return items[0]


def iso_dur(s):
    m = re.match(r"P(?:(\d+)D)?T?(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?", s or "")
    d, hh, mm, ss = (int(x or 0) for x in m.groups()) if m else (0, 0, 0, 0)
    return d * 86400 + hh * 3600 + mm * 60 + ss


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    load_env()
    ref = sys.argv[1]
    out = Path(sys.argv[2] if len(sys.argv) > 2 else ".")
    n = int(sys.argv[3]) if len(sys.argv) > 3 else 100
    out.mkdir(parents=True, exist_ok=True)
    h = token()
    ch = resolve_channel(h, ref)
    uploads = ch["contentDetails"]["relatedPlaylists"]["uploads"]
    ids, page = [], None
    while len(ids) < n:
        p = get(h, "playlistItems", part="contentDetails", playlistId=uploads, maxResults=50, **({"pageToken": page} if page else {}))
        ids += [i["contentDetails"]["videoId"] for i in p.get("items", [])]
        page = p.get("nextPageToken")
        if not page:
            break
    vids = []
    for i in range(0, len(ids[:n]), 50):
        v = get(h, "videos", part="snippet,statistics,contentDetails", id=",".join(ids[i:i + 50]))
        for it in v.get("items", []):
            s = it.get("statistics", {})
            vids.append({"id": it["id"], "title": it["snippet"]["title"], "published": it["snippet"]["publishedAt"],
                         "sec": iso_dur(it["contentDetails"].get("duration")), "views": int(s.get("viewCount", 0)),
                         "likes": int(s.get("likeCount", 0)) if "likeCount" in s else None,
                         "comments": int(s.get("commentCount", 0)) if "commentCount" in s else None})
    vids.sort(key=lambda x: x["published"], reverse=True)
    longs = [v for v in vids if v["sec"] > 180]
    shorts = [v for v in vids if v["sec"] <= 180]
    def stats(vs):
        if not vs:
            return {}
        avg10 = sum(v["views"] for v in vs[:10]) / min(10, len(vs))
        med = st.median(v["views"] for v in vs)
        for v in vs:
            v["x_median"] = round(v["views"] / med, 2) if med else None
            v["viral_5x_avg10"] = v["views"] >= 5 * avg10
        first = datetime.fromisoformat(vs[-1]["published"].replace("Z", "+00:00"))
        months = max(1, (datetime.now(timezone.utc) - first).days / 30.4)
        return {"n": len(vs), "median_views": med, "avg10": round(avg10), "median_minutes": round(st.median(v["sec"] for v in vs) / 60, 1),
                "share_3x": round(sum(v["views"] >= 3 * med for v in vs) / len(vs), 3), "viral_count": sum(v["viral_5x_avg10"] for v in vs),
                "uploads_per_month": round(len(vs) / months, 1),
                "likes_per_1000": round(1000 * sum(v["likes"] or 0 for v in vs) / max(1, sum(v["views"] for v in vs)), 1)}
    res = {"channel": {"id": ch["id"], "title": ch["snippet"]["title"], "created": ch["snippet"]["publishedAt"][:10],
                       "subs": ch["statistics"].get("subscriberCount"), "views": ch["statistics"].get("viewCount"),
                       "videos": ch["statistics"].get("videoCount")},
           "long": stats(longs), "shorts": stats(shorts), "fetched_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
           "videos": vids}
    slug = re.sub(r"[^\w-]+", "_", ch["snippet"]["title"]).strip("_")[:40] or ch["id"]
    (out / f"{slug}_api.json").write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
    c, L = res["channel"], res["long"]
    lines = [f"# {c['title']} (YouTube Data API, {res['fetched_at'][:10]})", "",
             f"Tạo kênh {c['created']} · {c['subs']} sub · {c['videos']} video · {c['views']} lượt xem", "",
             "| Loại | n | Trung vị view | TB 10 gần nhất | % ≥3× trung vị | Số viral (≥5× TB10) | Phút (trung vị) | Video/tháng | Like/1000 view |",
             "|---|---|---|---|---|---|---|---|---|"]
    for name, s in (("Video dài", L), ("Shorts", res["shorts"])):
        if s:
            lines.append(f"| {name} | {s['n']} | {s['median_views']:,.0f} | {s['avg10']:,} | {s['share_3x']*100:.0f}% | {s['viral_count']} | {s['median_minutes']} | {s['uploads_per_month']} | {s['likes_per_1000']} |")
    lines += ["", "## 10 video dài nổi bật nhất (theo bội số so với trung vị kênh)", "", "| Ngày | View | ×trung vị | Phút | Tiêu đề |", "|---|---|---|---|---|"]
    for v in sorted(longs, key=lambda v: -(v.get("x_median") or 0))[:10]:
        lines.append(f"| {v['published'][:10]} | {v['views']:,} | {v['x_median']} | {round(v['sec']/60)} | [{v['title'][:70]}](https://youtu.be/{v['id']}) |")
    (out / f"{slug}_api.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
