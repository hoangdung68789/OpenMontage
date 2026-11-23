"""Bằng chứng (c) cho một CHỦ ĐỀ: có >= 3 kênh độc lập có video cùng chủ đề đạt VIRAL (>= 5 lần TB 10 video của kênh) trong cửa sổ?

  python topic_check.py "<truy vấn tiếng Anh>" [--days 7] [--min-minutes 4] [--out <thư mục>]

Hạn mức: 1 search (100 đơn vị) + khoảng 2 đơn vị mỗi kênh. Ghi <out>/topic_<slug>.json.
"""
import argparse
import json
import re
import statistics as st
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from icyfox_common import CS, api, iso_dur, now_vn, rel, utf8, yt_headers  # noqa: E402

API = "https://www.googleapis.com/youtube/v3"


def main():
    utf8()
    ap = argparse.ArgumentParser()
    ap.add_argument("query")
    ap.add_argument("--days", type=int, default=7)
    ap.add_argument("--min-minutes", type=float, default=4)
    ap.add_argument("--out")
    a = ap.parse_args()
    h, _ = yt_headers()
    after = (datetime.now(timezone.utc) - timedelta(days=a.days)).strftime("%Y-%m-%dT%H:%M:%SZ")
    ok, j = api(h, f"{API}/search", {"part": "snippet", "type": "video", "q": a.query, "order": "viewCount",
                                     "publishedAfter": after, "maxResults": 25, "relevanceLanguage": "en", "regionCode": "US"})
    ids = [it["id"]["videoId"] for it in j.get("items", []) if it["id"].get("videoId")]
    ok, j = api(h, f"{API}/videos", {"part": "snippet,statistics,contentDetails", "id": ",".join(ids)}) if ids else (True, {"items": []})
    vids = [v for v in j.get("items", []) if iso_dur(v["contentDetails"]["duration"]) >= a.min_minutes * 60]
    rows = []
    for v in vids:
        cid = v["snippet"]["channelId"]
        ok, c = api(h, f"{API}/channels", {"part": "contentDetails", "id": cid}, fatal=False)
        up = c["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"] if ok and c.get("items") else None
        recent = []
        if up:
            ok, p = api(h, f"{API}/playlistItems", {"part": "contentDetails", "playlistId": up, "maxResults": 12}, fatal=False)
            rid = [x["contentDetails"]["videoId"] for x in (p.get("items", []) if ok else [])]
            ok, s = api(h, f"{API}/videos", {"part": "statistics", "id": ",".join(rid)}, fatal=False) if rid else (False, {})
            recent = [int(x["statistics"].get("viewCount", 0)) for x in (s.get("items", []) if ok else []) if x["id"] != v["id"]][:10]
        views = int(v["statistics"].get("viewCount", 0))
        avg10 = st.mean(recent) if len(recent) >= 5 else None
        ratio = round(views / avg10, 2) if avg10 else None
        rows.append({"id": v["id"], "title": v["snippet"]["title"], "channel": v["snippet"]["channelTitle"], "channel_id": cid,
                     "published": v["snippet"]["publishedAt"], "views": views, "ratio": ratio,
                     "viral": bool(ratio and ratio >= 5), "url": f"https://www.youtube.com/watch?v={v['id']}"})
    viral_channels = sorted({r["channel"] for r in rows if r["viral"]})
    res = {"query": a.query, "checked_at_vn": now_vn().strftime("%Y-%m-%d %H:%M"), "published_after_utc": after,
           "videos": rows, "viral_channels": viral_channels, "evidence_c": len(viral_channels) >= 3}
    out = Path(a.out) if a.out else CS / "research" / f"{now_vn():%Y-%m-%d}-trend"
    out.mkdir(parents=True, exist_ok=True)
    f = out / f"topic_{re.sub(r'[^a-z0-9]+', '-', a.query.lower()).strip('-')[:40]}.json"
    f.write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"'{a.query}': {len(rows)} video >= {a.min_minutes} phút trong {a.days} ngày; kênh có video VIRAL: {len(viral_channels)} "
          f"({', '.join(viral_channels[:6])}) → bằng chứng (c): {'ĐẠT' if res['evidence_c'] else 'chưa đạt'}. File: {rel(f)}")
    for r in sorted(rows, key=lambda r: -(r["ratio"] or 0))[:5]:
        print(f"   x{r['ratio']} {r['views']:,} {r['channel']} | {r['title'][:70]}")


if __name__ == "__main__":
    main()
