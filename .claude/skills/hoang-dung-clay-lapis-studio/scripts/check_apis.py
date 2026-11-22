"""Kiểm tra các API sau khi cấu hình. Chạy trong container: python3 check_apis.py
Script không in ra khóa hay token. Chỉ in kết quả: OK hoặc lỗi.
"""
import datetime
import os

import requests

def gemini():
    # Khóa Gemini do proxy tự gắn vào header x-goog-api-key (Network secret), không đọc ở đây.
    r = requests.get("https://generativelanguage.googleapis.com/v1beta/models", timeout=30)
    if r.ok:
        names = [m["name"] for m in r.json().get("models", []) if "tts" in m["name"]]
        return f"OK – model giọng đọc thấy được: {', '.join(names) or '(không có model TTS trong danh sách)'}"
    return f"LỖI {r.status_code}: {r.text[:160]}"

def google_token(refresh_var="YT_REFRESH_TOKEN"):
    need = ["YT_CLIENT_ID", "YT_CLIENT_SECRET", refresh_var]
    missing = [k for k in need if not os.environ.get(k)]
    if missing:
        return None, f"Chưa có biến môi trường: {', '.join(missing)}"
    r = requests.post("https://oauth2.googleapis.com/token", data={
        "client_id": os.environ["YT_CLIENT_ID"],
        "client_secret": os.environ["YT_CLIENT_SECRET"],
        "refresh_token": os.environ[refresh_var],
        "grant_type": "refresh_token"}, timeout=30)
    if not r.ok:
        return None, f"LỖI đổi token {r.status_code}: {r.json().get('error', r.text[:120])}"
    return r.json()["access_token"], "OK"

def main():
    print("1. Gemini API:", gemini())
    tok, msg = google_token()
    print("2. YouTube OAuth:", msg)
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
    main()
