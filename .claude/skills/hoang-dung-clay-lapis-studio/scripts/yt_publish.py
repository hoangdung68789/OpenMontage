"""Áp gói đăng lên video ANH ĐÃ TẢI LÊN (để Riêng tư) và hẹn giờ công khai, bằng YouTube Data API.

Vì sao không tự tải lên: video tải lên qua API từ dự án chưa được Google kiểm duyệt (audit) bị khóa Riêng tư vĩnh viễn
(policy-guardrails.md). Nên quy trình là: anh kéo thả file MP4 vào YouTube Studio, để Riêng tư, KHÔNG cần điền gì.
YouTube lấy tên file làm tiêu đề (ví dụ "002-lady-be-good"), script nhận ra và làm phần còn lại.

  python yt_publish.py scan                                   # liệt kê video Riêng tư có tiêu đề dạng mã gói (002-..., S01-...)
  python yt_publish.py apply <thư_mục_video_hoặc_short> --video-id <ID> [--publish-at "2026-12-11 21:00"] [--dry-run]
  python yt_publish.py auto [--dry-run]                       # khớp tự động mọi video Riêng tư với gói đăng rồi áp
  python yt_publish.py upload <thư_mục_video> [--file X.mp4] [--publish-at ...] [--dry-run]
                                                              # SAU KHI QUA AUDIT (YT_AUDIT_APPROVED=1): AI tự tải lên + áp gói + hẹn giờ

Áp gồm: tiêu đề, mô tả, thẻ, danh mục, ngôn ngữ, bản dịch tiêu đề/mô tả (package/i18n.json), thumbnail (package/thumbnail.png|jpg),
phụ đề (package/subtitles/<mã ngôn ngữ>.srt, bỏ qua ngôn ngữ đã có), hẹn giờ (publishAt: giờ Việt Nam → UTC).
Giờ đăng: --publish-at, hoặc package/publish_at.txt, hoặc ngày trong khối releases của PLAN.md lúc 21:00 giờ Việt Nam.
Sau khi áp: ghi package/UPLOADED.txt và analytics/video_map.json (để báo cáo số liệu biết video thuộc trụ cột/series nào).
Hạn mức: videos.update 50, thumbnails.set 50, captions.insert 400 mỗi ngôn ngữ (11 ngôn ngữ ≈ 4.400; mặc định 10.000/ngày).
[Cần thử với video đầu tiên] YouTube có cho đặt publishAt qua API cho video tải bằng Studio khi dự án chưa audit hay không.
"""
import argparse
import json
import re
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from icyfox_common import CS, api, data_block, load_json, now_vn, rel, save_json, utf8, yt_headers  # noqa: E402

DATA = "https://www.googleapis.com/youtube/v3"
UPLOAD = "https://www.googleapis.com/upload/youtube/v3"
CODE_RX = re.compile(r"^(\d{3}|S\d{2,3})-[a-z0-9-]+$")


def find_dir(code_title):
    code = code_title.split("-")[0]
    for base in (CS / "videos", CS / "shorts"):
        for d in sorted(base.glob(f"{code}-*")):
            if d.name == code_title or code_title.startswith(d.name) or d.name.startswith(code_title):
                return d
        hits = sorted(base.glob(f"{code}-*"))
        if hits and base.name == "videos" and code.isdigit():
            return hits[0]
    return None


def publish_time(vdir, override):
    s = override
    pf = vdir / "package" / "publish_at.txt"
    if not s and pf.exists():
        s = pf.read_text(encoding="utf-8").strip()
    if not s:
        code = vdir.name.split("-")[0]
        for r in data_block(CS / "PLAN.md", "releases"):
            if r[1] == code:
                s = f"{r[0]} 21:00"
    if not s:
        return None
    local = datetime.strptime(s, "%Y-%m-%d %H:%M").replace(tzinfo=timezone(timedelta(hours=7)))
    if local <= now_vn() + timedelta(minutes=30):
        sys.exit(f"Giờ đăng {s} đã qua hoặc quá gần. Sửa package/publish_at.txt")
    return local.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"), s


def private_uploads(h):
    ok, j = api(h, f"{DATA}/channels", {"part": "contentDetails", "mine": "true"})
    pl = j["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]
    ok, j = api(h, f"{DATA}/playlistItems", {"part": "contentDetails", "playlistId": pl, "maxResults": 50}, fatal=False)
    ids = [it["contentDetails"]["videoId"] for it in (j.get("items", []) if ok else [])]
    if not ids:
        return []
    ok, j = api(h, f"{DATA}/videos", {"part": "snippet,status", "id": ",".join(ids)})
    return [v for v in j.get("items", []) if v["status"]["privacyStatus"] == "private" and CODE_RX.match(v["snippet"]["title"].strip().lower())]


def apply(h, vdir, vid, when, dry):
    import requests
    pkg = vdir / "package"
    need = [pkg / "title.txt", pkg / "description.md", pkg / "tags.txt"]
    miss = [rel(p) for p in need if not p.exists()]
    if miss:
        sys.exit("Gói đăng thiếu: " + ", ".join(miss))
    title = pkg.joinpath("title.txt").read_text(encoding="utf-8").strip()
    if len(title) > 100:
        sys.exit(f"Tiêu đề {len(title)} ký tự > 100")
    desc = pkg.joinpath("description.md").read_text(encoding="utf-8").strip()
    tags = [x.strip() for x in re.split(r"[,\n]", pkg.joinpath("tags.txt").read_text(encoding="utf-8")) if x.strip()]
    cat = (pkg / "category.txt").read_text(encoding="utf-8").strip() if (pkg / "category.txt").exists() else "27"
    i18n = load_json(pkg / "i18n.json", {})
    body = {"id": vid, "snippet": {"title": title, "description": desc, "tags": tags, "categoryId": cat,
                                   "defaultLanguage": "en", "defaultAudioLanguage": "en"},
            "status": {"privacyStatus": "private", "selfDeclaredMadeForKids": False}}
    if when:
        body["status"]["publishAt"] = when[0]
    if i18n:
        body["localizations"] = {k: {"title": v["title"][:100], "description": v["description"]} for k, v in i18n.items()}
    parts = "snippet,status" + (",localizations" if i18n else "")
    thumb = next((p for p in (pkg / "thumbnail.png", pkg / "thumbnail.jpg") if p.exists()), None)
    subs = sorted((pkg / "subtitles").glob("*.srt")) if (pkg / "subtitles").exists() else []
    units = 50 + (50 if thumb else 0) + 400 * len(subs)
    print(f"Video {vid} ← {rel(vdir)}\n  Tiêu đề: {title}\n  Hẹn giờ: {when[1] + ' (giờ VN)' if when else 'KHÔNG (để Riêng tư)'}\n"
          f"  Thẻ: {len(tags)} · Bản dịch: {len(i18n)} ngôn ngữ · Thumbnail: {rel(thumb) if thumb else 'không có'} · Phụ đề: {len(subs)} file\n"
          f"  Hạn mức ước tính: {units} đơn vị")
    if dry:
        print("  (chạy thử, chưa gửi gì)")
        return
    r = requests.put(f"{DATA}/videos", params={"part": parts}, headers={**h, "Content-Type": "application/json"}, json=body, timeout=60)
    if not r.ok:
        sys.exit(f"videos.update lỗi {r.status_code}: {r.text[:300]}")
    done = ["metadata" + (" + hẹn giờ" if when else "")]
    if thumb:
        r = requests.post(f"{UPLOAD}/thumbnails/set", params={"videoId": vid}, headers={**h, "Content-Type": "image/png" if thumb.suffix == ".png" else "image/jpeg"},
                          data=thumb.read_bytes(), timeout=120)
        done.append("thumbnail" if r.ok else f"thumbnail LỖI {r.status_code} {r.text[:150]}")
    if subs:
        ok, j = api(h, f"{DATA}/captions", {"part": "snippet", "videoId": vid}, fatal=False)
        have = {c["snippet"]["language"] for c in (j.get("items", []) if ok else [])}
        for s in subs:
            lang = s.stem
            if lang in have:
                continue
            meta = {"snippet": {"videoId": vid, "language": lang, "name": "", "isDraft": False}}
            r = requests.post(f"{UPLOAD}/captions", params={"part": "snippet", "uploadType": "multipart"}, headers=h,
                              files={"metadata": (None, json.dumps(meta), "application/json"),
                                     "media": (s.name, s.read_bytes(), "application/octet-stream")}, timeout=120)
            done.append(f"phụ đề {lang}" + ("" if r.ok else f" LỖI {r.status_code} {r.text[:120]}"))
    stamp = now_vn().strftime("%Y-%m-%d %H:%M")
    (pkg / "UPLOADED.txt").write_text(f"video_id={vid}\napplied_at_vn={stamp}\npublish_at_vn={when[1] if when else ''}\nresult={'; '.join(done)}\n",
                                      encoding="utf-8")
    vm = load_json(CS / "analytics" / "video_map.json", {})
    readme = (vdir / "README.md").read_text(encoding="utf-8") if (vdir / "README.md").exists() else ""
    pillar = (re.search(r"\b(P[1-5])\b", readme) or [None, ""])[1]
    vm[vid] = {**vm.get(vid, {}), "video_dir": rel(vdir), "title": title, "pillar": vm.get(vid, {}).get("pillar") or pillar,
               "kind": "short" if vdir.name.startswith("S") else "long", "publish_at_vn": when[1] if when else ""}
    save_json(CS / "analytics" / "video_map.json", vm)
    print("  Đã áp:", "; ".join(done))


def find_mp4(vdir, given):
    if given:
        return Path(given)
    readme = (vdir / "README.md").read_text(encoding="utf-8") if (vdir / "README.md").exists() else ""
    pid = (re.search(r"Project ID[^`]*`([\w-]+)`", readme) or [None, ""])[1]
    cands = []
    if pid:
        cands += sorted((CS.parent / "projects" / pid / "renders").glob("*final*.mp4"))
    cands += sorted((vdir / "render").glob("*.mp4"))
    return cands[-1] if cands else None


def upload(h, vdir, mp4, dry):
    """Tải MP4 lên (Riêng tư, tiêu đề = mã gói) rồi áp gói đăng + hẹn giờ. Trả về video ID."""
    import os
    import requests
    if not mp4 or not mp4.exists():
        sys.exit(f"Không thấy file MP4 cho {rel(vdir)}. Dùng --file <đường dẫn>")
    if (vdir / "package" / "UPLOADED.txt").exists():
        sys.exit(f"{rel(vdir)} đã tải lên rồi (package/UPLOADED.txt). Không tải trùng.")
    size = mp4.stat().st_size
    print(f"Tải lên {mp4} ({size / 1e6:.1f} MB) → Riêng tư, tiêu đề \"{vdir.name}\", hạn mức 100 đơn vị")
    if dry:
        print("  (chạy thử, chưa gửi gì)")
        return None
    # Chặn tải khi chưa qua audit: video tải từ dự án chưa audit bị khóa Riêng tư vĩnh viễn (YouTube Help 7300965)
    if os.environ.get("YT_AUDIT_APPROVED") != "1":
        sys.exit("Chưa bật YT_AUDIT_APPROVED=1 trong .env. Thử thật ngày 22/11/2026 (T-028, T-030): video tải qua API không bị khóa, "
                 "hẹn giờ tự chuyển Công khai (guides/TU_DONG_DANG_VIDEO.md §4). Bật cờ theo thẻ T-032.")
    meta = {"snippet": {"title": vdir.name, "categoryId": "27", "defaultLanguage": "en", "defaultAudioLanguage": "en"},
            "status": {"privacyStatus": "private", "selfDeclaredMadeForKids": False}}
    r = requests.post(f"{UPLOAD}/videos", params={"uploadType": "resumable", "part": "snippet,status"},
                      headers={**h, "Content-Type": "application/json", "X-Upload-Content-Type": "video/mp4",
                               "X-Upload-Content-Length": str(size)}, json=meta, timeout=60)
    if not r.ok:
        sys.exit(f"videos.insert lỗi {r.status_code}: {r.text[:300]}")
    # shortcut: một lần PUT cả file, không nối lại khi rớt mạng giữa chừng; nếu hay rớt thì đổi sang gửi từng khúc 256 KB×n
    with open(mp4, "rb") as f:
        r = requests.put(r.headers["Location"], headers={**h, "Content-Type": "video/mp4"}, data=f, timeout=6 * 3600)
    if not r.ok:
        sys.exit(f"Tải file lỗi {r.status_code}: {r.text[:300]}")
    vid = r.json()["id"]
    print(f"  Đã tải: https://youtu.be/{vid}")
    return vid


def main():
    utf8()
    ap = argparse.ArgumentParser()
    sp = ap.add_subparsers(dest="cmd", required=True)
    sp.add_parser("scan")
    p = sp.add_parser("apply")
    p.add_argument("vdir")
    p.add_argument("--video-id", required=True)
    p.add_argument("--publish-at")
    p.add_argument("--dry-run", action="store_true")
    p = sp.add_parser("auto")
    p.add_argument("--dry-run", action="store_true")
    p = sp.add_parser("upload")
    p.add_argument("vdir")
    p.add_argument("--file")
    p.add_argument("--publish-at")
    p.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    h, scopes = yt_headers()
    if a.cmd == "upload":
        vdir = Path(a.vdir)
        when = publish_time(vdir, a.publish_at)
        vid = upload(h, vdir, find_mp4(vdir, a.file), a.dry_run)
        if vid:
            apply(h, vdir, vid, when, False)
        return
    if a.cmd == "apply":
        vdir = Path(a.vdir)
        apply(h, vdir, a.video_id, publish_time(vdir, a.publish_at), a.dry_run)
        return
    vids = private_uploads(h)
    if not vids:
        print("Không có video Riêng tư nào mang tiêu đề dạng mã gói (ví dụ 002-lady-be-good). Anh chưa tải lên, hoặc đã đổi tên.")
        return
    for v in vids:
        code_title = v["snippet"]["title"].strip().lower()
        vdir = find_dir(code_title)
        print(f"- {v['id']} \"{code_title}\" → {rel(vdir) if vdir else 'KHÔNG tìm thấy gói đăng'}")
        if a.cmd == "auto" and vdir:
            apply(h, vdir, v["id"], publish_time(vdir, None), a.dry_run)


if __name__ == "__main__":
    main()
