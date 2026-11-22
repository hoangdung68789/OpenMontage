# Clay & Lapis: ghi chú bàn giao (cập nhật 22/11/2026)

Đọc file này trước khi làm tiếp. Quy trình đầy đủ nằm trong skill `hoang-dung-clay-lapis-studio` (`.claude/skills/hoang-dung-clay-lapis-studio/SKILL.md`). Mở phiên bằng `bash .claude/skills/hoang-dung-clay-lapis-studio/scripts/session_start.sh`.

## Trạng thái API (22/11/2026)
- **Gemini:** OK. Network secret, header `x-goog-api-key`. Thấy model `gemini-3.8-flash-tts`.
- **YouTube OAuth:** anh đã thêm `YT_CLIENT_ID`, `YT_CLIENT_SECRET`, `YT_REFRESH_TOKEN` (Personal mode, quyền `youtube.force-ssl` và `yt-analytics.readonly`). **Chưa kiểm tra được**, vì phiên cũ khởi động trước khi có biến. Việc đầu tiên của phiên mới: xác nhận bằng `check_apis.py`.
- **Drive:** chưa cấu hình. Cần xin quyền riêng (`drive.file`), lưu vào `GDRIVE_REFRESH_TOKEN`. Không gấp.
- **ElevenLabs:** đang lưu sai (anh dán mã ID). Khi anh có khóa `sk_…` thì mở lại form `request_credential` (host `api.elevenlabs.io`, header `xi-api-key`). Gói miễn phí không được dùng thương mại.

## Video đang làm
| Video | Thư mục | Bước hiện tại | Đang chờ gì |
|---|---|---|---|
| 001 Gilgamesh: The Lost Lines (video thử) | `channel-studio/videos/001-gilgamesh-lost-lines/` · project `gilgamesh-pilot` | Kịch bản: Phần 1 và 2 đã duyệt (1.867 từ, khoảng 15:46). Phần 3 và 4 chưa viết | Tôi: kiểm S3.5, S4.1, S4.6, làm 3 mẫu giọng, viết Phần 3 |

## Quyết định mới trong phiên trước
- Đã tạo skill `hoang-dung-clay-lapis-studio` và sắp xếp lại thư mục `channel-studio/`.
- Mục tiêu video thử: 35–40 phút. Đã bỏ đoạn S4.8 ("wasteland" không kiểm được bài gốc).

## Việc tiếp theo (theo thứ tự)
1. Chạy `check_apis.py`. Đạt là thấy tên kênh, số sub, và Analytics OK. Nếu lỗi, tra bảng sự cố trong `references/environment-and-apis.md`.
2. Làm 3 mẫu giọng Gemini cho đoạn S0.4 (`videos/001-gilgamesh-lost-lines/script_part1.md`), gửi anh chọn.
3. Kiểm S3.5 (Enkidu can ngăn), S4.1 ("để Enkidu đi trước"), S4.6 ("trước khi các vị thần biết chuyện") bằng bản dịch Thompson 1928 (cần mở host archive.org).
4. Viết Phần 3: chương 5 (Ishtar và Bò Trời), chương 6 (Enkidu chết), chương 7 (tận cùng thế giới).
5. Viết Phần 4: chương 8 (Hồng thủy, George Smith 1872, Atrahasis, so sánh với Kinh Thánh) và chương 9 (Dream Tablet 2021, Fragmentarium với bản chép năm 130 TCN, bác bỏ tin "tìm thấy mộ" năm 2003, Tablet XII, kêu gọi theo dõi kênh).
6. Phân cảnh → tài nguyên → render HyperFrames → gói đăng. **Đo thời gian render và chi phí.**
7. Khi video thử đạt: tạo các tác vụ hẹn giờ theo `references/automation.md` (anh đã đồng ý).

## Việc anh cần làm
- Tạo kênh Clay & Lapis (nếu chưa có), xác minh tài khoản tại youtube.com/verify.
- Khi có khóa ElevenLabs `sk_…` thì nhắn "mở lại form ElevenLabs".

## Số đo đã có
- Giọng Gemini: 25 token/giây âm thanh. 9 USD/1 triệu token đến 31/12/2026, 18 USD từ 01/01/2027.
- Thời gian render và hạn mức Claude: chưa đo.
