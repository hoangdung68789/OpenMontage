# Tự động hóa và tác vụ hẹn giờ

**Đang chạy (22/11/2026, anh yêu cầu):** 2 tác vụ trên máy local, app Claude desktop: `icyfox-san-xuat-9h-17h` (cron `0 9,17 * * *`) và `icyfox-bao-cao-tuan-cn-9h` (cron `0 9 * * 0`). Lời nhắn đầy đủ: `~/.claude/scheduled-tasks/<taskId>/SKILL.md`. Bảng cloud bên dưới là phương án cũ, chưa tạo.

**Điều kiện để tạo tác vụ hẹn giờ:** anh đã đồng ý (22/11/2026), nhưng **chỉ tạo khi video thử đạt yêu cầu**, nghĩa là đã render xong và đo được thời gian, chi phí. Trước khi tạo, xác nhận lại với anh 1 dòng.

## Lịch (giờ Việt Nam, `CRON_TZ=Asia/Ho_Chi_Minh`)
Chạy trên môi trường `video-channel-studio`, mỗi lần chạy mở một phiên mới (`create_new_session_on_fire`), bật thông báo đẩy về điện thoại. Giờ dưới đây đã lệch phút để tránh giờ chẵn, bận.

| Tác vụ | Cron đề xuất | Lời nhắn cho phiên |
|---|---|---|
| Đề xuất chủ đề tháng | `CRON_TZ=Asia/Ho_Chi_Minh 13 10 1 * *` | "Dùng skill hoang-dung-clay-lapis-studio. Mở phiên. Quét ngách và đối thủ theo research-playbook. Đề xuất 4–8 chủ đề tháng tới kèm bằng chứng. Thêm vào Notion trạng thái Ý tưởng. Đóng phiên." |
| Kịch bản tuần | `CRON_TZ=Asia/Ho_Chi_Minh 17 14 * * 1` | "Dùng skill hoang-dung-clay-lapis-studio. Mở phiên. Lấy video kế tiếp trong Notion có trạng thái đã duyệt chủ đề. Nghiên cứu, rồi viết phần kịch bản tiếp theo. Đặt trạng thái Chờ duyệt. Đóng phiên." |
| Gắn phụ đề cho video mới | `CRON_TZ=Asia/Ho_Chi_Minh 41 9,21 * * *` | "Dùng skill hoang-dung-clay-lapis-studio. Mở phiên. Tìm video mới trên kênh (danh sách uploads) chưa có phụ đề. Gắn phụ đề và bản dịch từ gói đăng. Cập nhật Notion. Đóng phiên." |
| Báo cáo tuần | `CRON_TZ=Asia/Ho_Chi_Minh 23 19 * * 0` | "Dùng skill hoang-dung-clay-lapis-studio. Mở phiên. Lấy số liệu Analytics 7 và 28 ngày: giờ xem, sub, thời gian xem trung bình, tỉ lệ bấm thumbnail. So với tuần trước. Đề xuất 1–3 điều chỉnh. Ghi số liệu 7 ngày vào Notion. Đóng phiên." |

Dựng video không chạy theo lịch. Bước này bắt đầu khi anh duyệt kịch bản, trong phiên anh đang trả lời.

## Những gì không tự động
- **Bước duyệt:** OpenMontage chặn trong mã nguồn, và đây cũng là lớp bảo vệ trước chính sách nội dung rập khuôn. Gửi thông báo, chờ anh trả lời "duyệt".
- **Tải video lên YouTube:** API khóa video ở chế độ riêng tư. Anh tải lên mỗi Chủ nhật. Khi kênh ổn định có thể nộp đơn kiểm duyệt API, nhưng kết quả không chắc.
- **TikTok:** ngoài phạm vi hiện tại.

## Chi phí cần theo dõi
- Giọng Gemini cho 4–8 video/tháng: khoảng 2,4–9,8 USD (tính theo giá 2027).
- Hạn mức gói Claude của anh mà các phiên tự động dùng: **đo ở tháng đầu**, ghi vào HANDOFF.
