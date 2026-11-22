# Môi trường cloud, khóa và API

## Môi trường `video-channel-studio` (cá nhân, dùng cho cả 16 repo của anh)
- **Mạng: giới hạn.** Các host đã mở:
  - YouTube: www.youtube.com, youtube.com, m.youtube.com, i.ytimg.com
  - Google: www.googleapis.com, youtube.googleapis.com, oauth2.googleapis.com, youtubeanalytics.googleapis.com, generativelanguage.googleapis.com, support.google.com, blog.youtube, trends.google.com
  - TikTok: www.tiktok.com, tiktok.com, developers.tiktok.com, open.tiktokapis.com, ads.tiktok.com
  - Ảnh: commons.wikimedia.org, upload.wikimedia.org, collectionapi.metmuseum.org, images.metmuseum.org
  - Nhạc: pixabay.com, cdn.pixabay.com
  - Tài liệu: soas-repository.worktribe.com
  - Trình quản lý gói (pip, npm) được bật.
- **Script cài đặt** (chạy khi máy mới khởi động): cài yt-dlp, jsonschema, google-auth, google-auth-oauthlib, google-api-python-client, và `pip install -r OpenMontage/requirements.txt`.
- **Network secrets.** Proxy tự gắn khóa vào request, tôi không thấy giá trị:
  | Host | Header | Ghi chú |
  |---|---|---|
  | generativelanguage.googleapis.com | `x-goog-api-key` (không có tiền tố) | Gemini. Anh nhập trong cài đặt: loại "Bearer", Tên tiêu đề `x-goog-api-key`, Tiền tố để trống. Form `request_credential` **không** lưu được header này |
  | api.elevenlabs.io | `xi-api-key` | Lưu được qua `request_credential`. Khóa phải bắt đầu bằng `sk_`. Ngày 22/11/2026 anh lỡ dán mã ID nên cần lưu lại |
- **Biến môi trường:** `YT_CLIENT_ID`, `YT_CLIENT_SECRET`, `YT_REFRESH_TOKEN`, sau này thêm `GDRIVE_REFRESH_TOKEN`. **Chỉ có hiệu lực khi phiên khởi động.** Phiên đang chạy không thấy biến vừa thêm.
- **Công cụ đòi khóa ở biến môi trường** (ví dụ `gemini_tts list_voices` đọc `GEMINI_API_KEY`): chạy với `GEMINI_API_KEY=proxy-injected`. Proxy sẽ ghi đè header bằng khóa thật. Làm tương tự với `ELEVENLABS_API_KEY`.

## Kiểm tra
```bash
python3 .claude/skills/hoang-dung-clay-lapis-studio/scripts/check_apis.py
```
Kết quả đạt:
1. Gemini thấy được model `gemini-3.8-flash-tts`.
2. Đổi được token OAuth.
3. Thấy tên kênh và số sub.
4. Drive OK, hoặc "chưa cấu hình".
5. Analytics OK.

## YouTube OAuth: cách đã làm được (22/11/2026)
1. **Personal mode** tại https://console.cloud.google.com/auth/overview/personal. Không cần publish, không cần xác minh, quyền không hết hạn sau 7 ngày, nhưng chỉ tài khoản tạo dự án mới cấp quyền được.
   - Không dùng chế độ External: ở trạng thái Testing, quyền hết hạn sau 7 ngày, và anh không publish được.
   - Chế độ Personal chỉ chọn được khi tạo mới. Không đổi được từ External.
2. **Loại client:** Web application. Redirect URI: `https://developers.google.com/oauthplayground`.
3. **Bật 3 API trong dự án:** YouTube Data API v3, YouTube Analytics API, Google Drive API.
4. **Lấy refresh token trên OAuth Playground:**
   - Bấm ⚙: chọn Server-side, Offline, tick "Use your own OAuth credentials", dán Client ID và Client secret.
   - Ô scopes chỉ dán: `https://www.googleapis.com/auth/youtube.force-ssl https://www.googleapis.com/auth/yt-analytics.readonly`
   - Bấm Authorize, rồi bấm Exchange, chép **Refresh token** (bắt đầu bằng `1//`).
5. **Lưu ý về quyền Drive:** Google **không cho xin quyền YouTube chung với `drive.file`** (lỗi 400 invalid_request "scopes that cannot be requested together"). Muốn dùng Drive thì xin riêng một lần với `https://www.googleapis.com/auth/drive.file`, lưu vào biến `GDRIVE_REFRESH_TOKEN`.
6. **Đổi token:** POST `https://oauth2.googleapis.com/token` với `grant_type=refresh_token`. Xem hàm `google_token()` trong `scripts/check_apis.py`.

## Hạn mức YouTube Data API (tra 22/11/2026)
- Mặc định 10.000 đơn vị/ngày cho mọi phương thức, trừ upload và search.
- `captions.insert` = 400 đơn vị. Một video đủ 11 phụ đề = 4.400 đơn vị.
- `videos.update` (tiêu đề và mô tả đã dịch) = 50 đơn vị.
- **Shorts chỉ gắn phụ đề EN + VI** (800 đơn vị) để không hết hạn mức.
- `videos.insert` có hạn mức riêng nhưng **không dùng**: video tải lên từ dự án chưa xác minh bị khóa riêng tư, không kháng nghị được.

## Sự cố thường gặp
| Hiện tượng | Nguyên nhân | Cách xử lý |
|---|---|---|
| Gemini báo 403 "Permission denied on the service" | Chưa có khóa, hoặc header sai | Kiểm tra Network secret: header `x-goog-api-key`, tiền tố để trống |
| `request_credential` báo "header_name names a header a saved credential is never sent in" | Form không hỗ trợ `x-goog-api-key` | Hướng dẫn anh nhập trong cài đặt (có ảnh mẫu `channel-studio/guides/gemini_secret_guide.png`) |
| ElevenLabs báo "API key ID used as API key" | Anh dán mã ID | Tạo khóa mới bắt đầu bằng `sk_`, mở lại form |
| Kiểm tra báo "Chưa có biến môi trường YT_…" | Biến mới thêm, phiên chưa khởi động lại | Lưu công việc (đóng phiên), rồi anh mở phiên mới |
| Lỗi đổi token: `invalid_grant` | Token bị thu hồi hoặc hết hạn (6 tháng không dùng, hoặc ứng dụng ở chế độ Testing) | Lấy lại refresh token trên Playground |
| `client_user_mismatch` | Cấp quyền bằng tài khoản khác tài khoản tạo dự án Personal | Đăng nhập đúng tài khoản sở hữu kênh và dự án |
| yt-dlp báo "Sign in to confirm you're not a bot" khi lấy số liệu từng video | YouTube chặn IP của máy chủ | Lấy danh sách kênh bằng yt-dlp chế độ flat (vẫn chạy). Số liệu chi tiết dùng YouTube Data API. **Không** vượt kiểm tra bằng cookie |
| Met Museum API trả 410 | `/v1/search` đã ngừng từ 01/10/2026 | Dùng `/public/collection/v1.1/search` (có offset và limit) |
| Kho SOAS trả 403 kèm "Just a moment…" | Cloudflare chặn truy cập tự động | Nhờ anh tải PDF bằng trình duyệt rồi gửi lên. Không vượt kiểm tra |
| Host bị chặn ("no rule allows host") | Host chưa được mở | `get_environment`, rồi `update_environment` thêm đúng host đó |
