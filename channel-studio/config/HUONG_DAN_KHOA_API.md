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
