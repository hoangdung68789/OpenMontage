# ICYFOX (dự án Clay & Lapis): ghi chú bàn giao (cập nhật 22/11/2026)

Đọc file này trước khi làm tiếp. Quy trình đầy đủ nằm trong skill `hoang-dung-clay-lapis-studio` (`.claude/skills/hoang-dung-clay-lapis-studio/SKILL.md`). **Đọc mục 0 "Tiêu chuẩn làm việc" trước.** Mở phiên bằng `bash .claude/skills/hoang-dung-clay-lapis-studio/scripts/session_start.sh`.

## Thay đổi quan trọng (22/11/2026, cuối ngày)
- **Phạm vi chủ đề đã mở rộng thành 5 trụ cột kể chuyện** (`references/content-pillars.md`): bí ẩn Trái Đất và đại dương, sinh tồn và thám hiểm, chiến tranh, thảm họa, thế giới cổ đại và thần thoại. Gilgamesh vẫn là video thử thuộc trụ cột P5.
- **Phân tích kênh nào cũng dùng YouTube Data API trước:** `scripts/research/yt_api_channel.py`. Đã chạy cho @WartimeStories, kết quả ở `channel-studio/research/2026-11-22-wartimestories/Wartime_Stories_api.md`: 158 video dài, trung vị 459K view, 10 video gần nhất trung bình 225K (đang giảm), 21 video viral, dài 38,8 phút.
- **ĐÃ XONG (22/11, phiên trên máy anh):** phân tích lại @WartimeStories theo playbook mục A.
  - Báo cáo: `research/2026-11-22-wartimestories/BAO_CAO.md`. Bản cũ đổi tên thành `BAO_CAO_v1_cu.md`.
  - Kế hoạch: `KE_HOACH_90_NGAY.md` **bản 2**. Anh yêu cầu 1–2 video mỗi ngày, 30–60 video mỗi 30 ngày, **tính cả Shorts** (anh xác nhận 22/11).
    - Chia thành 8 video dài (thứ Ba, thứ Sáu, 21:00 giờ Việt Nam) + khoảng 38 Shorts mỗi 30 ngày.
    - Shorts bắt đầu 01/12. Video dài đầu tiên 11/12. Từ 01/01/2027 lên 2 video dài mỗi tuần, nếu qua được cổng kiểm ngày 28/12.
    - Tuần này (23–30/11) phải làm sẵn 10 Shorts đầu và đo thời gian render.
  - Phụ đề 2 video top: `subs/`.
  - Dàn ý và hook video 002 Lady Be Good: `videos/002-lady-be-good/script_outline.md`, trạng thái `awaiting_human`.
  - Notion: thêm 9 dòng (002–010).
  - Hướng đi: series "Documented", gồm chuyện lạ thời chiến **có hồ sơ thật** (P3 kết hợp P1/P2). Đây là khoảng trống đối thủ để lại.
- **Mốc YPP:** kênh mới từ 01/02/2027 cần 8.000 giờ xem. [Cần kiểm] ICYFOX có thuộc diện "kênh mới" không.
- `check_apis.py` đã được sửa để in tiếng Việt trên console Windows (trước đó lỗi `gbk`).

## Tự động hóa (tạo 22/11/2026 theo yêu cầu anh)
- Tác vụ hẹn giờ trên máy anh (app Claude desktop, mục Scheduled): `icyfox-san-xuat-9h-17h` (09:00 và 17:00 mỗi ngày: làm tiếp tới cổng duyệt kế tiếp rồi dừng) và `icyfox-bao-cao-tuan-cn-9h` (Chủ nhật 09:00: báo cáo số liệu kênh, file ở `channel-studio/reports/weekly/`).
- Chỉ chạy khi app Claude đang mở; app đóng thì chạy khi mở lại. Không tự duyệt, không tải video lên.

## Trạng thái API (22/11/2026)
- **Gemini:** OK. Network secret, header `x-goog-api-key`. Thấy model `gemini-3.8-flash-tts`.
- **YouTube OAuth + Data API + Analytics:** **OK** (22/11/2026, đã bật API trong dự án 979474479924). Kênh **ICYFOX** (0 sub, 0 video). Anh đã chốt giữ tên ICYFOX.
- **OpenAI:** OK (Network secret `api.openai.com`, Bearer). Có model giọng và model ảnh.
- **Drive:** chưa cấu hình. Cần xin quyền riêng (`drive.file`), lưu vào `GDRIVE_REFRESH_TOKEN`. Không gấp.
- **ElevenLabs:** **OK** (22/11/2026). Gói **free**, đã dùng 0/10.000 ký tự. Gói miễn phí **không được dùng cho video đăng kênh**, chỉ dùng để nghe thử giọng. Muốn dùng giọng ElevenLabs trong video thì anh cần nâng lên gói trả phí.

## Video đang làm
| Video | Thư mục | Bước hiện tại | Đang chờ gì |
|---|---|---|---|
| 002 Lady Be Good (đăng dự kiến 11/12) | `channel-studio/videos/002-lady-be-good/` · project `lady-be-good` (research + proposal đã ghi checkpoint) | Dàn ý đã duyệt 22/11. Phần 1 kịch bản (chương 0–2, khoảng 1.270 từ, 00:00–10:40) đã viết | Anh duyệt `script_part1.md`; tôi kiểm 4 mục 'Cần kiểm' trong file |
| 001 Gilgamesh: The Lost Lines (video thử) | `channel-studio/videos/001-gilgamesh-lost-lines/` · project `gilgamesh-pilot` | Kịch bản: Phần 1 và 2 đã duyệt (1.867 từ, khoảng 15:46). Phần 3 và 4 chưa viết. Bản đồ 16 repo: references/toolbox-repos.md của skill | Tôi: kiểm S3.5, S4.1, S4.6, làm 3 mẫu giọng, viết Phần 3 |

## Quyết định mới trong phiên trước
- Kênh YouTube **giữ tên ICYFOX**. Clay & Lapis là tên dự án.
- Có file mẫu khóa API: `channel-studio/config/api_keys.env.example` và hướng dẫn `channel-studio/config/HUONG_DAN_KHOA_API.md`. Máy local dùng `OpenMontage/.env`.
- Thử mẫu giọng S0.4: **ElevenLabs "Brian" đạt** (file nằm trên máy cloud cũ, không lên git). **Gemini lỗi 404**: công cụ `gemini_tts` gọi API v1, model chỉ có ở v1beta, phải sửa công cụ. **OpenAI 429**: tài khoản chưa nạp tiền.
- Đã tạo skill `hoang-dung-clay-lapis-studio` và sắp xếp lại thư mục `channel-studio/`.
- Mục tiêu video thử: 35–40 phút. Đã bỏ đoạn S4.8 ("wasteland" không kiểm được bài gốc).

## Việc tiếp theo (theo thứ tự)
0. **Nếu anh gửi link kênh đối thủ:** làm đủ `request-playbooks.md` mục A trong cùng lượt trả lời.
0a. **Chờ anh duyệt Phần 1** kịch bản 002 (`videos/002-lady-be-good/script_part1.md`). Hook đã đổi "In November 1958" thành "In 1958" vì nguồn lệch tháng. Duyệt xong: viết Phần 2 (chương 3–4). Video 002 đăng trước Gilgamesh (001 dời sang 25/12 theo kế hoạch 90 ngày; dòng Notion của 001 chưa đổi ngày).
0b. Lấy lại phụ đề video `QkRRERFPfEM` (lần trước bị lỗi 429).
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
