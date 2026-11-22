# ICYFOX (dự án Clay & Lapis): ghi chú bàn giao (cập nhật 22/11/2026)

Đọc file này trước khi làm tiếp. Quy trình đầy đủ nằm trong skill `hoang-dung-clay-lapis-studio` (`.claude/skills/hoang-dung-clay-lapis-studio/SKILL.md`). **Đọc mục 0 "Tiêu chuẩn làm việc" trước.** Mở phiên bằng `bash .claude/skills/hoang-dung-clay-lapis-studio/scripts/session_start.sh`.

## Thay đổi quan trọng (22/11/2026, cuối ngày)
- **Phạm vi chủ đề đã mở rộng thành 5 trụ cột kể chuyện** (`references/content-pillars.md`): bí ẩn Trái Đất và đại dương, sinh tồn và thám hiểm, chiến tranh, thảm họa, thế giới cổ đại và thần thoại. Gilgamesh vẫn là video thử thuộc trụ cột P5.
- **Phân tích kênh nào cũng dùng YouTube Data API trước:** `scripts/research/yt_api_channel.py`. Đã chạy cho @WartimeStories, kết quả ở `channel-studio/research/2026-11-22-wartimestories/Wartime_Stories_api.md`: 158 video dài, trung vị 459K view, 10 video gần nhất trung bình 225K (đang giảm), 21 video viral, dài 38,8 phút.
- **Anh muốn phân tích lại @WartimeStories cho đúng chuẩn**, theo `references/request-playbooks.md` mục A: báo cáo, kế hoạch 90 ngày, kịch bản video đầu tiên, Notion, git. Báo cáo cũ `BAO_CAO.md` do phiên trên máy anh tạo hiện chỉ nằm trên máy anh (chưa đẩy lên git).

## Trạng thái API (22/11/2026)
- **Gemini:** OK. Network secret, header `x-goog-api-key`. Thấy model `gemini-3.8-flash-tts`.
- **YouTube OAuth + Data API + Analytics:** **OK** (22/11/2026, đã bật API trong dự án 979474479924). Kênh **ICYFOX** (0 sub, 0 video). Anh đã chốt giữ tên ICYFOX.
- **OpenAI:** OK (Network secret `api.openai.com`, Bearer). Có model giọng và model ảnh.
- **Drive:** chưa cấu hình. Cần xin quyền riêng (`drive.file`), lưu vào `GDRIVE_REFRESH_TOKEN`. Không gấp.
- **ElevenLabs:** **OK** (22/11/2026). Gói **free**, đã dùng 0/10.000 ký tự. Gói miễn phí **không được dùng cho video đăng kênh**, chỉ dùng để nghe thử giọng. Muốn dùng giọng ElevenLabs trong video thì anh cần nâng lên gói trả phí.

## Video đang làm
| Video | Thư mục | Bước hiện tại | Đang chờ gì |
|---|---|---|---|
| 001 Gilgamesh: The Lost Lines (video thử) | `channel-studio/videos/001-gilgamesh-lost-lines/` · project `gilgamesh-pilot` | Kịch bản: Phần 1 và 2 đã duyệt (1.867 từ, khoảng 15:46). Phần 3 và 4 chưa viết. Bản đồ 16 repo: references/toolbox-repos.md của skill | Tôi: kiểm S3.5, S4.1, S4.6, làm 3 mẫu giọng, viết Phần 3 |

## Quyết định mới trong phiên trước
- Kênh YouTube **giữ tên ICYFOX**. Clay & Lapis là tên dự án.
- Có file mẫu khóa API: `channel-studio/config/api_keys.env.example` và hướng dẫn `channel-studio/config/HUONG_DAN_KHOA_API.md`. Máy local dùng `OpenMontage/.env`.
- Thử mẫu giọng S0.4: **ElevenLabs "Brian" đạt** (file nằm trên máy cloud cũ, không lên git). **Gemini lỗi 404**: công cụ `gemini_tts` gọi API v1, model chỉ có ở v1beta, phải sửa công cụ. **OpenAI 429**: tài khoản chưa nạp tiền.
- Đã tạo skill `hoang-dung-clay-lapis-studio` và sắp xếp lại thư mục `channel-studio/`.
- Mục tiêu video thử: 35–40 phút. Đã bỏ đoạn S4.8 ("wasteland" không kiểm được bài gốc).

## Việc tiếp theo (theo thứ tự)
0. **Nếu anh gửi link kênh đối thủ:** làm đủ `request-playbooks.md` mục A trong cùng lượt trả lời.
1. Chạy `check_apis.py`. Đạt là thấy tên kênh, số sub, và Analytics OK. Nếu lỗi, tra bảng sự cố trong `references/environment-and-apis.md`.
2. Làm 3 mẫu giọng Gemini cho đoạn S0.4 (`videos/001-gilgamesh-lost-lines/script_part1.md`), gửi anh chọn.
3. Kiểm S3.5 (Enkidu can ngăn), S4.1 ("để Enkidu đi trước"), S4.6 ("trước khi các vị thần biết chuyện") bằng bản dịch Thompson 1928 (cần mở host archive.org).
4. Viết Phần 3: chương 5 (Ishtar và Bò Trời), chương 6 (Enkidu chết), chương 7 (tận cùng thế giới).
5. Viết Phần 4: chương 8 (Hồng thủy, George Smith 1872, Atrahasis, so sánh với Kinh Thánh) và chương 9 (Dream Tablet 2021, Fragmentarium với bản chép năm 130 TCN, bác bỏ tin "tìm thấy mộ" năm 2003, Tablet XII, kêu gọi theo dõi kênh).
6. Phân cảnh → tài nguyên → render HyperFrames → gói đăng. **Đo thời gian render và chi phí.**
7. Khi video thử đạt: tạo các tác vụ hẹn giờ theo `references/automation.md` (anh đã đồng ý).

## Việc anh cần làm
- Xác minh tài khoản tại youtube.com/verify, để tải được video trên 15 phút.
- Nạp tiền OpenAI nếu muốn dùng giọng hoặc ảnh của OpenAI.

## Số đo đã có
- Giọng Gemini: 25 token/giây âm thanh. 9 USD/1 triệu token đến 31/12/2026, 18 USD từ 01/01/2027.
- Thời gian render và hạn mức Claude: chưa đo.
