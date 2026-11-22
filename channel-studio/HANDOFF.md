# Clay & Lapis: ghi chú bàn giao giữa các phiên (cập nhật 22/11/2026)

Đọc file này trước khi làm tiếp. Toàn bộ tài liệu nằm trong thư mục `channel-studio/` của repo OpenMontage, nhánh `ccr-6640cec8-2anthl`.

## Mục tiêu
Kênh YouTube tiếng Anh, người xem Mỹ, ngách **lịch sử cổ đại và thần thoại** (phim tài liệu dài), giọng AI, phụ đề 11 ngôn ngữ (có tiếng Việt). Mục tiêu đầu tiên: đủ điều kiện kiếm tiền YouTube (YPP). Từ 01/02/2027, kênh mới cần 1.000 sub + 8.000 giờ xem trong 365 ngày, hoặc 20 triệu view Shorts trong 90 ngày. Tránh vi phạm chính sách "inauthentic content" (nội dung rập khuôn) và "reused content" (nội dung dùng lại).

## Quyết định đã chốt
- Tên kênh: **Clay & Lapis** (`01_channel_setup.md`). Kênh quản lý bằng máy thật ở VN, quốc gia cư trú khai Việt Nam. Không dùng AdsPower hay proxy Mỹ cho tài khoản kênh.
- Nhịp đăng: 4–8 video dài/tháng (1–2/tuần) + 30–60 Shorts/tháng cắt từ video dài. Hẹn giờ cố định. Anh tải lên mỗi Chủ nhật, vì video tải lên qua API từ dự án chưa xác minh sẽ bị khóa ở chế độ riêng tư.
- Video thử: Concept A "The Lost Lines" (Gilgamesh), HyperFrames, cách dựng Atelier, phương án Standard. Kịch bản: Phần 1 đã duyệt ("Five thousand"). Phần 2 đã duyệt (bỏ S4.8). **Mục tiêu cả video 35–40 phút.**
- Giọng: Gemini `gemini-3.8-flash-tts` (chưa chọn giọng cụ thể, sẽ nghe thử 3 giọng ở đoạn S0.4). ElevenLabs là phương án phụ. **Gói miễn phí của ElevenLabs không được dùng thương mại.**
- Bảng theo dõi Notion: "Clay & Lapis – Video Pipeline" (data source `collection://4201dcd7-7c95-8188-8452-000b17602005`).
- Tác vụ hẹn giờ tự động: anh **đã đồng ý**, nhưng **chỉ tạo sau khi video thử đạt yêu cầu** (`04_automation_plan.md`).

## Môi trường `video-channel-studio`
- Network secrets: Gemini (`generativelanguage.googleapis.com`, header `x-goog-api-key`) **chạy OK**. ElevenLabs (`api.elevenlabs.io`, `xi-api-key`) **đang lưu sai**: anh dán mã ID thay vì khóa `sk_…`, cần mở lại form để anh dán khóa đúng.
- Biến môi trường: `YT_CLIENT_ID`, `YT_CLIENT_SECRET`, `YT_REFRESH_TOKEN`. Anh đã thêm ngày 22/11/2026. Đây là OAuth Personal mode, quyền `youtube.force-ssl` và `yt-analytics.readonly`. Quyền Drive phải xin riêng (Google không cho xin chung với YouTube) rồi lưu vào `GDRIVE_REFRESH_TOKEN`, hiện chưa làm.
- Kiểm tra: `python3 channel-studio/tools/check_apis.py`
- Khi gọi công cụ cần khóa ở biến môi trường (ví dụ gemini_tts list_voices), đặt khóa giả `GEMINI_API_KEY=proxy-injected`. Proxy sẽ thay bằng khóa thật.

## Việc tiếp theo (theo thứ tự)
1. Chạy `check_apis.py`. Đạt là thấy tên kênh, số sub, và Analytics OK.
2. Mở lại form khóa ElevenLabs khi anh có khóa `sk_…`.
3. Làm 3 mẫu giọng Gemini cho đoạn S0.4 (`03_script_part1.md`) để anh chọn.
4. Kiểm 3 điểm còn treo ở Phần 2: S3.5, S4.1, S4.6 (dùng bản dịch Thompson 1928, cần host archive.org).
5. Viết Phần 3 (chương 5–7) và Phần 4 (chương 8–9). Mỗi phần gửi anh duyệt.
6. Phân cảnh → lấy ảnh Wikimedia (chỉ dùng Public domain, CC BY, CC BY-SA; không dùng ảnh British Museum vì giấy phép NC) → giọng đọc → render HyperFrames → gói đăng.

## Cổng duyệt của OpenMontage (bắt buộc)
Các bước proposal, script, scene_plan, assets, publish phải có anh duyệt. Checkpoint nằm trong `channel-studio/projects/gilgamesh-pilot/`. Thư mục `projects/` của OpenMontage bị gitignore, nên khi làm tiếp phải chép bản lưu này về `OpenMontage/projects/`.
