"""Kiểm tra các API sau khi cấu hình. Chạy trong container: python3 check_apis.py
Script không in ra khóa hay token. Chỉ in kết quả: OK hoặc lỗi.
"""
import datetime
import os

import requests
from pathlib import Path

from icyfox_common import CHANNEL, yt_vars


def load_dotenv_local():
    """Máy local: đọc OpenMontage/.env (nếu có). Không ghi đè biến môi trường đã đặt sẵn. Không in giá trị."""
    here = Path(__file__).resolve()
    candidates = [Path.cwd() / ".env"] + [p / ".env" for p in here.parents if (p / "AGENT_GUIDE.md").exists()]
    for f in candidates:
        if f.is_file():
            for line in f.read_text(encoding="utf-8", errors="ignore").splitlines():
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                k, v = line.split("=", 1)
                k, v = k.strip(), v.strip().strip('"').strip("'")
                if k and v and not os.environ.get(k):
                    os.environ[k] = v
            return str(f)
    return None

PLACEHOLDERS = {"", "proxy-injected", "dummy", "dummy-replaced-by-proxy"}


def key_header(var, header):
    """Cloud: proxy tự gắn khóa (không cần biến). Máy local: lấy khóa từ biến môi trường."""
    v = os.environ.get(var, "")
    return {} if v in PLACEHOLDERS else {header: v}


def gemini():
    h = key_header("GEMINI_API_KEY", "x-goog-api-key") or key_header("GOOGLE_API_KEY", "x-goog-api-key")
    r = requests.get("https://generativelanguage.googleapis.com/v1beta/models", headers=h, timeout=30)
    if r.ok:
        names = [m["name"] for m in r.json().get("models", []) if "tts" in m["name"]]
        return f"OK – model giọng đọc thấy được: {', '.join(names) or '(không có model TTS trong danh sách)'}"
    return f"LỖI {r.status_code}: {r.text[:160]}"

def elevenlabs():
    r = requests.get("https://api.elevenlabs.io/v1/user/subscription",
                     headers=key_header("ELEVENLABS_API_KEY", "xi-api-key"), timeout=30)
    if r.ok:
        d = r.json()
        note = " (gói miễn phí: KHÔNG dùng cho video đăng kênh)" if d.get("tier") == "free" else ""
        return f"OK – gói {d.get('tier')}, đã dùng {d.get('character_count')}/{d.get('character_limit')} ký tự{note}"
    return f"LỖI {r.status_code}: {r.text[:140]}"


def openai_check():
    r = requests.get("https://api.openai.com/v1/models",
                     headers={"Authorization": f"Bearer {os.environ['OPENAI_API_KEY']}"}
                     if os.environ.get("OPENAI_API_KEY", "") not in PLACEHOLDERS else {}, timeout=30)
    if r.ok:
        ids = [m["id"] for m in r.json().get("data", [])]
        return f"OK – {len(ids)} model (giọng: {sum('tts' in i for i in ids)}, ảnh: {sum('image' in i for i in ids)})"
    return f"LỖI {r.status_code}: {r.text[:140]}"


def google_token(refresh_var="YT_REFRESH_TOKEN", client=("YT_CLIENT_ID", "YT_CLIENT_SECRET")):
    need = [*client, refresh_var]
    missing = [k for k in need if not os.environ.get(k)]
    if missing:
        return None, f"Chưa có biến môi trường: {', '.join(missing)}"
    r = requests.post("https://oauth2.googleapis.com/token", data={
        "client_id": os.environ[client[0]],
        "client_secret": os.environ[client[1]],
        "refresh_token": os.environ[refresh_var],
        "grant_type": "refresh_token"}, timeout=30)
    if not r.ok:
        return None, f"LỖI đổi token {r.status_code}: {r.json().get('error', r.text[:120])}"
    return r.json()["access_token"], "OK"

def main():
    src = load_dotenv_local()
    print("0. Nguồn khóa:", f"file {src}" if src else "biến môi trường / proxy cloud")
    print("1. Gemini API:", gemini())
    print("1b. ElevenLabs:", elevenlabs())
    print("1c. OpenAI:", openai_check())
    cid, sec, ref = yt_vars()
    tok, msg = google_token(ref, (cid, sec))
    print(f"2. YouTube OAuth ({CHANNEL or 'ICYFOX'}):", msg)
    if not tok:
        return
    h = {"Authorization": f"Bearer {tok}"}
    r = requests.get("https://www.googleapis.com/youtube/v3/channels",
                     params={"part": "snippet,statistics", "mine": "true"}, headers=h, timeout=30)
    if r.ok and r.json().get("items"):
        c = r.json()["items"][0]
        print(f"3. Kênh: OK – {c['snippet']['title']} | sub: {c['statistics'].get('subscriberCount')} | video: {c['statistics'].get('videoCount')}")
    else:
        print("3. Kênh: LỖI", r.status_code, r.text[:160])
    # Google không cho xin quyền YouTube cùng lúc với quyền Drive, nên Drive dùng refresh token riêng.
    dtok, dmsg = google_token("GDRIVE_REFRESH_TOKEN")
    if dtok:
        r = requests.get("https://www.googleapis.com/drive/v3/files", params={"pageSize": 1},
                         headers={"Authorization": f"Bearer {dtok}"}, timeout=30)
        print("4. Google Drive (drive.file):", "OK" if r.ok else f"LỖI {r.status_code}: {r.text[:160]}")
    else:
        print("4. Google Drive: chưa cấu hình (không bắt buộc lúc này) –", dmsg)
    today = datetime.date.today()
    r = requests.get("https://youtubeanalytics.googleapis.com/v2/reports", headers=h, timeout=30, params={
        "ids": "channel==MINE", "metrics": "views",
        "startDate": str(today - datetime.timedelta(days=28)), "endDate": str(today)})
    print("5. YouTube Analytics:", "OK" if r.ok else f"LỖI {r.status_code}: {r.text[:160]}")

if __name__ == "__main__":
    import sys
    sys.stdout.reconfigure(encoding="utf-8")  # Windows console mặc định gbk/cp1252 làm vỡ tiếng Việt
    main()
