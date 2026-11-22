"""THỬ: YouTube có ép video tải lên qua API của dự án ICYFOX về "Riêng tư" không? (anh cho phép ngày 22/11/2026)

  python yt_upload_probe.py upload [--out <thư mục>]          # tạo clip đen 5 giây, tải lên ở chế độ Không công khai
  python yt_upload_probe.py poll <video_id> [--minutes 6] [--delete] [--out <thư mục>]   # đọc lại trạng thái định kỳ, rồi xóa

Không in token. Kết quả ghi vào <out>/result.json (mặc định channel-studio/research/<ngày>-api-upload-test/).
"""
import argparse
import json
import subprocess
import sys
import time
from pathlib import Path

import requests

sys.path.insert(0, str(Path(__file__).resolve().parent))
from icyfox_common import CS, now_vn, rel, utf8, yt_headers  # noqa: E402

DATA = "https://www.googleapis.com/youtube/v3"
UP = "https://www.googleapis.com/upload/youtube/v3/videos"


def outdir(a):
    d = Path(a.out) if a.out else CS / "research" / f"{now_vn():%Y-%m-%d}-api-upload-test"
    d.mkdir(parents=True, exist_ok=True)
    return d


def save(d, key, val):
    f = d / "result.json"
    data = json.loads(f.read_text(encoding="utf-8")) if f.exists() else {}
    data[key] = val
    f.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")


def status(h, vid):
    r = requests.get(f"{DATA}/videos", headers=h, params={"part": "status,processingDetails,snippet", "id": vid}, timeout=30)
    if not r.ok:
        return {"http": r.status_code, "error": r.text[:300]}
    items = r.json().get("items", [])
    if not items:
        return {"found": False}
    v = items[0]
    return {"found": True, "privacyStatus": v["status"].get("privacyStatus"), "uploadStatus": v["status"].get("uploadStatus"),
            "failureReason": v["status"].get("failureReason"), "rejectionReason": v["status"].get("rejectionReason"),
            "processingStatus": v.get("processingDetails", {}).get("processingStatus"), "title": v["snippet"].get("title")}


def main():
    utf8()
    ap = argparse.ArgumentParser()
    sp = ap.add_subparsers(dest="cmd", required=True)
    u = sp.add_parser("upload")
    u.add_argument("--out")
    p = sp.add_parser("poll")
    p.add_argument("video_id")
    p.add_argument("--minutes", type=float, default=6)
    p.add_argument("--delete", action="store_true")
    p.add_argument("--out")
    a = ap.parse_args()
    d = outdir(a)
    h, scopes = yt_headers()
    if a.cmd == "upload":
        clip = d / "icyfox-api-test.mp4"
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "lavfi", "-i", "color=c=black:s=1280x720:d=5:r=30",
                        "-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo", "-t", "5", "-c:v", "libx264", "-pix_fmt", "yuv420p",
                        "-c:a", "aac", "-shortest", str(clip)], check=True)
        body = {"snippet": {"title": "ICYFOX API test (will be deleted)", "description": "Automated upload test. Deleted within minutes.",
                            "categoryId": "22"},
                "status": {"privacyStatus": "unlisted", "selfDeclaredMadeForKids": False}}
        size = clip.stat().st_size
        r = requests.post(UP, params={"uploadType": "resumable", "part": "snippet,status"},
                          headers={**h, "Content-Type": "application/json; charset=UTF-8",
                                   "X-Upload-Content-Type": "video/mp4", "X-Upload-Content-Length": str(size)},
                          json=body, timeout=60)
        rec = {"at_vn": now_vn().strftime("%Y-%m-%d %H:%M:%S"), "scopes": scopes, "clip_bytes": size, "requested_privacy": "unlisted",
               "init_http": r.status_code}
        if not r.ok:
            rec["init_error"] = r.text[:500]
            save(d, "upload", rec)
            print(json.dumps(rec, ensure_ascii=False, indent=1))
            sys.exit(2)
        r2 = requests.put(r.headers["Location"], headers={**h, "Content-Type": "video/mp4"}, data=clip.read_bytes(), timeout=300)
        rec["put_http"] = r2.status_code
        if not r2.ok:
            rec["put_error"] = r2.text[:500]
            save(d, "upload", rec)
            print(json.dumps(rec, ensure_ascii=False, indent=1))
            sys.exit(2)
        j = r2.json()
        rec.update({"video_id": j["id"], "returned_privacy": j["status"].get("privacyStatus"),
                    "returned_uploadStatus": j["status"].get("uploadStatus")})
        rec["readback"] = status(h, j["id"])
        save(d, "upload", rec)
        clip.unlink()  # không giữ file thử
        print(json.dumps(rec, ensure_ascii=False, indent=1))
        return
    # poll
    timeline, end = [], time.time() + a.minutes * 60
    while True:
        s = status(h, a.video_id)
        s["at_vn"] = now_vn().strftime("%H:%M:%S")
        timeline.append(s)
        print(json.dumps(s, ensure_ascii=False), flush=True)
        if time.time() >= end or (s.get("processingStatus") in ("succeeded", "failed") and len(timeline) >= 4):
            break
        time.sleep(30)
    save(d, "poll", timeline)
    if a.delete:
        r = requests.delete(f"{DATA}/videos", headers=h, params={"id": a.video_id}, timeout=30)
        after = status(h, a.video_id)
        save(d, "delete", {"http": r.status_code, "error": r.text[:300] if not r.ok else "", "after": after,
                           "at_vn": now_vn().strftime("%Y-%m-%d %H:%M:%S")})
        print("delete:", r.status_code, "| sau khi xóa:", after)
    print("Đã ghi", rel(d / "result.json"))


if __name__ == "__main__":
    main()
