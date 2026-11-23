"""KIỂM CHỨNG XU HƯỚNG: đo lại các video của một lần radar trước (thời điểm 2) và gắn nhãn theo định nghĩa của anh.

  python trend_verify.py <outliers.json cũ> [--new <outliers.json mới>] [--window-days 7] [--out <TREND.md>]

Định nghĩa (hồ sơ của anh):
- MỚI: đăng trong window-days ngày tính tới lúc tra.
- Bằng chứng (b): cùng một video, số liệu ở >= 2 thời điểm cho thấy tăng. Ở đây yêu cầu thêm: tốc độ tăng giữa 2 lần đo
  >= 30% tốc độ trung bình kể từ khi đăng (đà còn mạnh, không phải đã đạt đỉnh).
- Bằng chứng (c): >= 3 kênh độc lập có video cùng chủ đề đạt VIRAL (>= 5 lần TB 10 video gần nhất của chính kênh) trong cửa sổ.
- VIRAL (một video): >= 5 lần TB 10 video gần nhất của kênh đó (radar đã tính).
Nhãn: ĐANG LÊN – ĐÃ KIỂM CHỨNG = MỚI + >= 2 bằng chứng độc lập; TÍN HIỆU SỚM = MỚI + 1 bằng chứng; còn lại loại.
Video bị cờ ngoài phạm vi (hư cấu, lịch sử giả, true crime...) không được đưa vào đề xuất.
"""
import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from icyfox_common import api, now_vn, rel, utf8, yt_headers  # noqa: E402

API = "https://www.googleapis.com/youtube/v3"


def main():
    utf8()
    ap = argparse.ArgumentParser()
    ap.add_argument("old")
    ap.add_argument("--new")
    ap.add_argument("--window-days", type=int, default=7)
    ap.add_argument("--out")
    a = ap.parse_args()
    old = json.loads(Path(a.old).read_text(encoding="utf-8"))
    vids = {v["id"]: v for v in old["videos"]}
    h, _ = yt_headers()
    now_utc = datetime.now(timezone.utc)
    t1_utc = datetime.strptime(old["checked_at_vn"], "%Y-%m-%d %H:%M").replace(tzinfo=timezone.utc) - (now_vn().utcoffset())
    ids = list(vids)
    cur = {}
    for i in range(0, len(ids), 50):
        ok, j = api(h, f"{API}/videos", {"part": "statistics", "id": ",".join(ids[i:i + 50])}, fatal=False)
        for it in (j.get("items", []) if ok else []):
            cur[it["id"]] = int(it["statistics"].get("viewCount", 0))
    gap_h = max((now_utc - t1_utc).total_seconds() / 3600, 0.1)
    rows = []
    for vid, v in vids.items():
        if vid not in cur:
            continue
        pub = datetime.fromisoformat(v["published"].replace("Z", "+00:00"))
        age_h = max((now_utc - pub).total_seconds() / 3600, 1)
        gain = cur[vid] - v["views"]
        rate_recent = gain / gap_h
        rate_life = cur[vid] / age_h
        momentum = rate_recent / rate_life if rate_life else 0
        is_new = (now_utc - pub).days < a.window_days
        ev_b = gain > 0 and momentum >= 0.3
        rows.append({**v, "views_t1": v["views"], "views_t2": cur[vid], "gain": gain, "gap_h": round(gap_h, 1),
                     "rate_recent": round(rate_recent, 1), "momentum": round(momentum, 2), "is_new": is_new, "ev_b": ev_b,
                     "viral": v.get("label") == "VIRAL"})
    # Bằng chứng (c) theo cụm chủ đề: anh/AI gán chủ đề bằng từ khóa trong file topics (nếu có), mặc định theo trụ cột
    out = Path(a.out) if a.out else Path(a.old).parent.parent / f"{now_vn():%Y-%m-%d}-trend" / "TREND.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    (out.parent / "trend_rows.json").write_text(json.dumps({"t1_vn": old["checked_at_vn"], "t2_vn": now_vn().strftime("%Y-%m-%d %H:%M"),
                                                            "rows": rows}, ensure_ascii=False, indent=1), encoding="utf-8")
    good = [r for r in rows if not r.get("flags")]
    good.sort(key=lambda r: (-(r["ev_b"] + r["viral"]), -r["rate_recent"]))
    L = [f"# Kiểm chứng xu hướng ICYFOX — đo lần 1: {old['checked_at_vn']}, đo lần 2: {now_vn():%Y-%m-%d %H:%M} (giờ VN)", "",
         f"Nguồn: YouTube Data API v3 videos.list (lượt xem tại 2 thời điểm, cách {gap_h:.1f} giờ). Video bị cờ ngoài phạm vi đã bỏ.",
         "Cột (b): tăng giữa 2 lần đo và đà >= 0,3 lần tốc độ trung bình từ khi đăng. VIRAL: >= 5 lần TB 10 video của kênh.", "",
         "| Video | Kênh | Trụ cột | Đăng | Xem lần 1 → lần 2 | Tăng/giờ gần đây | Đà | (b) | VIRAL | MỚI |",
         "|---|---|---|---|---|---|---|---|---|---|"]
    for r in good[:30]:
        L.append(f"| [{r['title'][:70]}]({r['url']}) | {r['channel']} | {','.join(r['pillars'])} | {r['published'][:10]} | "
                 f"{r['views_t1']:,} → {r['views_t2']:,} | {r['rate_recent']:,} | {r['momentum']} | {'có' if r['ev_b'] else '-'} | "
                 f"{'có' if r['viral'] else '-'} | {'có' if r['is_new'] else 'quá 7 ngày'} |")
    L += ["", "Nhãn cuối cùng (ĐANG LÊN – ĐÃ KIỂM CHỨNG / TÍN HIỆU SỚM) gắn theo CHỦ ĐỀ trong file đề xuất, sau khi gom bằng chứng (c).", ""]
    out.write_text("\n".join(L), encoding="utf-8")
    print(f"Đã lưu {rel(out)}; {len(rows)} video đo lại, cách {gap_h:.1f} giờ")
    for r in good[:12]:
        print(f"  b={'Y' if r['ev_b'] else '-'} viral={'Y' if r['viral'] else '-'} new={'Y' if r['is_new'] else '-'} "
              f"+{r['gain']:>8,} ({r['rate_recent']:>8,}/h, đà {r['momentum']}) {r['pillars']} {r['title'][:60]}")


if __name__ == "__main__":
    main()
