"""Cấp quyền một lần cho kênh YouTube. Chạy trên MÁY CỦA ANH, không chạy trong container.

Chuẩn bị:
    pip install google-auth-oauthlib
    Tải file client OAuth (loại Desktop app) từ Google Cloud Console, đặt tên client_secret.json

Chạy:
    python yt_authorize.py client_secret.json

Trình duyệt sẽ mở ra. Đăng nhập đúng tài khoản sở hữu kênh, chọn đúng kênh, rồi bấm cho phép.
Kết quả lưu vào yt_token.json ngay trên máy anh. KHÔNG gửi file đó qua chat.
"""
import json
import sys

from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = [
    # Quản lý video: phụ đề, tiêu đề/mô tả đã dịch, danh sách phát, thumbnail, lịch đăng
    "https://www.googleapis.com/auth/youtube.force-ssl",
    # Chỉ đọc số liệu Analytics để làm báo cáo tuần
    "https://www.googleapis.com/auth/yt-analytics.readonly",
    # Chỉ các file do ứng dụng này tạo trên Google Drive: nơi giao video thành phẩm
    "https://www.googleapis.com/auth/drive.file",
]

client_file = sys.argv[1] if len(sys.argv) > 1 else "client_secret.json"
flow = InstalledAppFlow.from_client_secrets_file(client_file, SCOPES)
creds = flow.run_local_server(port=0, access_type="offline", prompt="consent")

with open("yt_token.json", "w", encoding="utf-8") as f:
    json.dump(
        {
            "client_id": creds.client_id,
            "client_secret": creds.client_secret,
            "refresh_token": creds.refresh_token,
        },
        f,
        indent=1,
    )
print("Đã lưu yt_token.json. Chép 3 giá trị trong file vào biến môi trường, KHÔNG gửi qua chat.")
