# Kế hoạch tự động hóa kênh Clay & Lapis (bản nháp, 22/11/2026)

## Phạm vi
- **Tự động:** nghiên cứu, kịch bản, giọng đọc, phân cảnh, lấy ảnh và nhạc, render, kiểm lỗi, thumbnail, tiêu đề, mô tả, 11 phụ đề, cắt Shorts, gắn phụ đề và bản dịch sau khi video đã lên kênh, báo cáo số liệu.
- **Anh giữ lại:** duyệt (các cổng duyệt của OpenMontage là bắt buộc trong mã nguồn) và tải video lên YouTube.

## Lịch chạy (giờ Việt Nam, chạy bằng scheduled task trên môi trường `video-channel-studio`)

| Khi nào | Việc tự động | Anh làm |
|---|---|---|
| Ngày 1 hằng tháng | Quét đối thủ và ngách. Đề xuất 4–8 chủ đề cho tháng tới, kèm số liệu | Duyệt danh sách (cổng proposal) |
| Thứ Hai hằng tuần | Nghiên cứu, rồi viết kịch bản tiếng Anh và bản dịch tiếng Việt cho video của tuần | Duyệt kịch bản (cổng script) |
| Ngay sau khi anh duyệt kịch bản | Giọng đọc → phân cảnh → ảnh và nhạc → render → kiểm lỗi → thumbnail, tiêu đề, mô tả, 11 phụ đề → 3–5 Shorts → tải lên Google Drive | Xem bản xem trước, duyệt (cổng scene_plan và assets) |
| Chủ nhật | — | Tải video và Shorts lên YouTube, chọn Schedule (cổng publish) |
| Mỗi ngày 2 lần | Tìm video mới trên kênh → gắn phụ đề, tiêu đề và mô tả dịch, thêm vào danh sách phát | — |
| Tối Chủ nhật | Báo cáo tuần: giờ xem, sub, thời gian xem trung bình, tỉ lệ bấm thumbnail. Đề xuất chỉnh | Đọc |

Mọi bước đều gửi thông báo về điện thoại. Trạng thái từng video theo dõi trên bảng Notion (cần anh đồng ý). File video lưu trên Google Drive (quyền `drive.file`).

## Điều kiện để bật
1. Khóa Gemini, lưu ở Network secrets.
2. YouTube OAuth, lưu ở biến môi trường. Chạy `tools/yt_authorize.py` (đã có thêm quyền Drive).
3. Mở host `youtubeanalytics.googleapis.com`. Tôi sẽ xin khi cần.
4. **Video thử đạt yêu cầu**, đo được thời gian render và tài nguyên máy trong một phiên.
5. Anh đồng ý tạo các scheduled task theo bảng trên.

## Phần không tự động được (và vì sao)
| Việc | Lý do | Hướng xử lý |
|---|---|---|
| Tải video lên YouTube | Video tải lên từ dự án API chưa được kiểm duyệt bị khóa riêng tư, không kháng nghị được | Anh tải lên mỗi tuần một lần. Khi kênh đã có lịch sử ổn định, có thể nộp đơn kiểm duyệt API (kết quả không chắc) |
| Bỏ các bước duyệt | OpenMontage chặn ngay trong mã nguồn (báo lỗi "GATE VIOLATION"). Chính sách nội dung rập khuôn của YouTube xét cả kênh | Gộp các lần duyệt, mỗi lần chỉ cần trả lời "duyệt" từ điện thoại |
| TikTok | Ứng dụng chưa kiểm duyệt chỉ đăng được ở chế độ riêng tư. Công cụ đăng cho tài khoản của mình bị ghi rõ là không chấp nhận | Ngoài phạm vi hiện tại |

## Chi phí
- Giọng đọc 4–8 video/tháng: khoảng 2,4–9,8 USD (giá Gemini năm 2027 trong trường hợp cao nhất).
- Các phiên tự động tiêu hao hạn mức sử dụng gói Claude của anh. [Chưa ước tính được, sẽ đo ở video thử]
