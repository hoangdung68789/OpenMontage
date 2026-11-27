# Hướng dẫn cấu hình khóa API (kênh ICYFOX, dự án Clay & Lapis)

File mẫu: `channel-studio/config/api_keys.env.example`. Cập nhật lần cuối 22/11/2026.

## 1. Danh sách khóa và trạng thái

| Biến | Dịch vụ | Dùng để | Lấy ở đâu | Dạng khóa | Trạng thái 22/11/2026 |
|---|---|---|---|---|---|
| `GEMINI_API_KEY` | Google AI Studio | Giọng đọc chính | https://aistudio.google.com/apikey | `AIza…` | ✅ Khóa đúng. ⚠️ Công cụ `gemini_tts` của OpenMontage gọi model qua API v1 nên báo 404, phải chuyển sang v1beta. **Lỗi này nằm ở công cụ, không phải ở khóa.** Tôi sẽ sửa |
| `OPENAI_API_KEY` | OpenAI | Giọng phụ, vẽ minh họa | https://platform.openai.com/api-keys | `sk-…` | ✅ Khóa đúng. ❌ **Tài khoản chưa có tiền nạp** (lỗi 429 "no credits") |
| `ELEVENLABS_API_KEY` | ElevenLabs | Giọng tham khảo | elevenlabs.io → Developers → API Keys | `sk_…` | ✅ Chạy được, gói **free**. Không dùng cho video đăng kênh |
| `YT_CLIENT_ID` | Google OAuth | Đăng nhập API YouTube | Google Cloud → Clients (Personal mode, Web application) | `….apps.googleusercontent.com` | ✅ |
| `YT_CLIENT_SECRET` | Google OAuth | Như trên | Như trên | `GOCSPX-…` | ✅ |
| `YT_REFRESH_TOKEN` | Google OAuth | Phụ đề, bản dịch, Analytics | OAuth Playground (quyền YouTube) | `1//0…` | ✅ Kênh ICYFOX |
| `GDRIVE_REFRESH_TOKEN` | Google OAuth | Giao file video (tùy chọn) | OAuth Playground (chỉ quyền `drive.file`) | `1//0…` | Chưa làm |

## 2. Trên máy tính (Claude Code local): dùng file `.env`

1. Trong thư mục `OpenMontage`, chép file `channel-studio\config\api_keys.env.example` thành **`OpenMontage\.env`**.
   - Windows: mở File Explorer → bật **View → Show → File name extensions** (để thấy đuôi file) → chép file → đổi tên thành `.env`.
   - Có thể gõ lệnh: `copy channel-studio\config\api_keys.env.example .env`
2. Mở `.env` bằng **Notepad**, dán từng khóa ngay sau dấu `=`:
   ```
   GEMINI_API_KEY=AIzaSy...
   ```
   Không có dấu cách, không có dấu nháy. Dòng nào chưa có khóa thì để trống.
3. Lưu file.
4. Kiểm tra (trong thư mục `OpenMontage`):
   ```
   python .claude/skills/hoang-dung-clay-lapis-studio/scripts/check_apis.py
   ```
   - Các công cụ của OpenMontage tự đọc `.env` ở thư mục gốc repo.
   - Script kiểm tra cũng đọc file này.
5. **An toàn:**
   - `.env` đã nằm trong `.gitignore`, và script đóng phiên tự loại mọi file `.env` ra khỏi commit, nên file không lên GitHub.
   - Không gửi file này cho ai. Không dán nội dung của nó vào chat.

**Cách thay thế** (không dùng file): đặt biến môi trường của Windows bằng `setx GEMINI_API_KEY "AIza..."`, rồi mở lại Claude Code. Nếu cùng một khóa có ở cả 2 nơi, **biến môi trường được ưu tiên** hơn `.env`.

## 3. Trên cloud (claude.ai/code): không dùng file `.env`

Vào cài đặt môi trường **video-channel-studio** (bấm tên môi trường trên thanh tiêu đề phiên → Edit):

| Khóa | Nhập ở đâu | Cách điền |
|---|---|---|
| Gemini | **Thông tin bí mật cho mạng** | Loại: Bearer · Trang web: `generativelanguage.googleapis.com` · Tên tiêu đề: `x-goog-api-key` · **Tiền tố: để trống** · Giá trị: khóa (ảnh mẫu: `guides/gemini_secret_guide.png`) |
| OpenAI | Thông tin bí mật cho mạng (hoặc nhờ Claude mở form) | Trang web: `api.openai.com` · Loại Bearer, giữ mặc định (`Authorization: Bearer`) |
| ElevenLabs | Thông tin bí mật cho mạng (hoặc nhờ Claude mở form) | Trang web: `api.elevenlabs.io` · Tên tiêu đề: `xi-api-key` · Tiền tố: để trống |
| YT_CLIENT_ID, YT_CLIENT_SECRET, YT_REFRESH_TOKEN (GDRIVE_REFRESH_TOKEN) | **Biến môi trường** | Mỗi dòng dạng `TÊN=giá trị`. Chỉ có hiệu lực từ **phiên mới** |

Với Network secrets, proxy tự gắn khóa vào request, Claude không thấy được giá trị.

## 3b. Kênh thứ hai (tài khoản YouTube ở Mỹ, thêm 27/11/2026)

Dùng để xem số liệu, đăng video và quản lý video của kênh Mỹ, tách hẳn khỏi ICYFOX.

1. Đăng nhập **tài khoản Mỹ** (trên đúng trình duyệt hoặc môi trường Mỹ), vào https://console.cloud.google.com, tạo dự án mới.
2. Mở APIs & Services → Library, bật **YouTube Data API v3** và **YouTube Analytics API**.
3. Vào Google Auth Platform:
   - Branding: chọn External.
   - Audience: bấm **Publish app** (In production). Nếu để Testing, refresh token tự hết hạn sau 7 ngày.
4. Vào Clients → Create client, chọn loại **Desktop app**. Tải file JSON, đổi tên thành `client_secret.json`, đặt trong thư mục `OpenMontage`.
5. Chạy `python .claude/skills/hoang-dung-clay-lapis-studio/scripts/yt_authorize_desktop.py client_secret.json`.
   - Đăng nhập tài khoản Mỹ, chọn đúng kênh, rồi cho phép mọi quyền.
   - Thấy "Google hasn't verified this app" thì bấm Advanced → Go to….
6. Chép 3 giá trị trong `yt_token.json` vào `.env` dưới tên **`YT_US_CLIENT_ID`, `YT_US_CLIENT_SECRET`, `YT_US_REFRESH_TOKEN`**. Xong thì xóa `yt_token.json` và `client_secret.json`.
7. Kiểm tra (PowerShell):
   ```
   $env:YT_CHANNEL='US'; python .claude/skills/hoang-dung-clay-lapis-studio/scripts/check_apis.py; Remove-Item Env:YT_CHANNEL
   ```

**Cách chọn kênh:** đặt `YT_CHANNEL=US` cho từng lệnh, không ghi vào `.env`.
- Có `YT_CHANNEL=US`: script dùng khóa `YT_US_*` và đọc/ghi dữ liệu trong `channel-studio-us/` (số liệu, gói đăng, video_map, sổ việc), không lẫn với ICYFOX.
- Không đặt: mọi thứ chạy như cũ, trên kênh ICYFOX.
- Riêng `research/yt_api_channel.py` (phân tích đối thủ) luôn dùng khóa ICYFOX. Script này chỉ đọc dữ liệu công khai nên kênh nào cũng như nhau.

**Đăng video qua API:** dự án Google mới chưa qua audit, nên video tải lên bị khóa ở chế độ Riêng tư. Muốn đăng công khai thì phải nộp đơn audit riêng cho dự án này (mẫu: `channel/api-audit/DON_AUDIT.md`).

## 4. Đổi khóa, thu hồi khóa
- **Khóa bị lộ:** xóa ngay ở trang của dịch vụ (AI Studio, OpenAI, ElevenLabs), tạo khóa mới, rồi cập nhật lại `.env` hoặc cài đặt cloud.
- **Thu hồi quyền YouTube và Drive:** tài khoản Google → Bảo mật → Kết nối với bên thứ ba → xóa ứng dụng. Sau đó lấy lại refresh token trên OAuth Playground.
- **Refresh token Google tự hết hạn** nếu 6 tháng không dùng.

## 5. Sự cố thường gặp
| Lỗi | Cách xử lý |
|---|---|
| Gemini 403 "Permission denied on the service" | Sai header hoặc chưa có khóa (trên cloud: tiền tố phải để trống) |
| Gemini 404 "Model 'gemini-3.8-flash-tts' not found… v1beta" | Lỗi của công cụ (phiên bản API), không phải khóa |
| OpenAI 429 "You have no credits remaining" | Nạp tiền tại https://platform.openai.com/settings/organization/billing |
| ElevenLabs "API key ID used as API key" | Dán nhầm mã ID. Tạo khóa mới và chép khóa `sk_…` trong cửa sổ hiện ra lúc tạo |
| YouTube 403 "API has not been used in project … or it is disabled" | Bật API trong đúng dự án chứa mã OAuth (link có trong thông báo lỗi) |
| Kiểm tra báo "Chưa có biến môi trường YT_…" | Cloud: mở phiên mới. Máy local: kiểm tra lại file `.env` |
