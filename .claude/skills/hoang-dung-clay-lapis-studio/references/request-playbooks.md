# Định nghĩa hoàn thành cho từng loại yêu cầu

Mỗi loại yêu cầu có một danh sách việc bắt buộc. Một câu trả lời chỉ gồm câu hỏi hoặc kế hoạch mà không có sản phẩm thì **chưa hoàn thành**. Chỉ dừng giữa chừng ở 3 trường hợp: tới cổng duyệt của OpenMontage, cần anh quyết định thật sự, hoặc hệ thống yêu cầu xác nhận.

## A. "Phân tích đối thủ <link> và lên kịch bản / kế hoạch"
Ví dụ: `https://www.youtube.com/@WartimeStories … phân tích đối thủ và lên kịch bản/kế hoạch dài hạn`.

| # | Việc bắt buộc | Lệnh hoặc nguồn |
|---|---|---|
| 1 | Mở phiên, kiểm tra API | `session_start.sh`. Ghi kết quả vào câu trả lời |
| 2 | **Số liệu thật bằng YouTube Data API** | `python scripts/research/yt_api_channel.py <link> channel-studio/research/<ngày>-<kênh> 200` (dùng `python` trên Windows, `python3` trên cloud): view, like, bình luận, thời lượng, ngày đăng, trung vị, % video ≥3×, video viral, nhịp đăng, 10 video nổi bật |
| 3 | Quy luật tiêu đề và thumbnail | Tiêu đề của 10 video nổi bật. Lưới thumbnail `i.ytimg.com/vi/<id>/hqdefault.jpg` ghép bằng ffmpeg, xem trực tiếp |
| 4 | **Nội dung 2–3 video nổi bật nhất**: cách mở đầu (60 giây đầu), cấu trúc hồi, nhịp, cách kết | Phụ đề: `yt-dlp --skip-download --write-auto-subs --sub-langs en <url>` (máy local thường lấy được). Mô tả và mốc chương lấy từ API (`snippet.description`). Nếu bị chặn: nói rõ, rồi phân tích từ mô tả, mốc chương và tiêu đề |
| 5 | Xếp vào trụ cột của ICYFOX | `content-pillars.md`. Chủ đề nằm ngoài trụ cột thì đề xuất **cách làm hợp lệ**: lời kể nhân chứng có ghi nguồn, truyền thuyết ghi rõ là truyền thuyết. Không gạt đi |
| 6 | **Sản phẩm giao** (lưu file) | (a) `BAO_CAO.md`: số liệu, công thức tiêu đề, thumbnail, cấu trúc, nên học và không nên học. (b) `KE_HOACH_90_NGAY.md`: 12 tuần, 8–12 chủ đề cụ thể kèm bằng chứng, nhịp đăng, chỉ số và ngưỡng quyết định. (c) **Kịch bản video đầu tiên**: dàn ý chương, hook 60 giây viết đầy đủ, nguồn. Đây là cổng duyệt script, toàn văn viết sau khi anh duyệt. (d) Thêm các chủ đề vào Notion, trạng thái "Ý tưởng" |
| 7 | Lưu | `session_end.py`, theo mục 6 của SKILL.md |
| 8 | Câu hỏi | Ở cuối, tối đa 3 câu, mỗi câu có phương án mặc định **đã được áp dụng sẵn** |

## B. "Lên kế hoạch / chiến lược kênh"
1. Số liệu kênh ICYFOX qua YouTube Analytics (nếu đã có video), số liệu từ các lần quét gần nhất trong `research/`, và các trụ cột trong `content-pillars.md`.
2. Giao `KE_HOACH_<n>_NGAY.md`: lịch theo tuần, chủ đề cụ thể kèm bằng chứng, nhịp đăng, ngân sách (chi phí giọng đọc), chỉ số và ngưỡng để nhân rộng hoặc dừng.
3. Thêm chủ đề vào Notion. Lưu git.

## C. "Viết kịch bản" hoặc "viết phần N"
1. Đọc proposal, research_brief và phần trước đã duyệt.
2. Giao `script_partN.md` theo mẫu: lời tiếng Anh, ghi chú giọng, ghi chú hình, bản dịch Việt, nguồn, số từ và thời lượng.
3. Mọi dữ kiện có nguồn. Chi tiết chưa kiểm được ghi vào mục "Cần kiểm", không đọc giọng.
4. Ghi checkpoint `awaiting_human`. Lưu git. Dừng chờ anh duyệt (cổng duyệt script).

## D. "Mẫu giọng", "dựng", "gói đăng", "gắn phụ đề", "báo cáo tuần"
Làm theo `production-workflow.md`, `publish-package.md` và `automation.md`. Mỗi việc kết thúc bằng file thật (MP3, MP4, SRT, MD) đã gửi anh hoặc đã lưu, kèm đường dẫn.

## Tự kiểm trước khi gửi câu trả lời
| Câu hỏi | Nếu "không" |
|---|---|
| Đã chạy `session_start.sh` (hoặc `check_apis.py`) và ghi kết quả chưa? | Chạy ngay |
| Số liệu YouTube lấy từ **Data API** chưa? | Chạy `yt_api_channel.py` |
| Đã giao **đủ mọi sản phẩm** anh xin (báo cáo, kế hoạch, kịch bản…) chưa? | Làm nốt, đừng thay bằng câu hỏi |
| Có đang kéo anh về chủ đề cũ thay vì làm theo yêu cầu mới không? | Làm theo yêu cầu mới, cập nhật HANDOFF |
| Mọi số liệu đều có nguồn và ngày tra chưa? | Bổ sung, hoặc ghi [Chưa xác minh] |
| Đã lưu git và cập nhật Notion chưa? | Chạy `session_end.py`, cập nhật Notion |
| Câu hỏi cuối có thật sự cần không, và đã có phương án mặc định chưa? | Bỏ câu hỏi thừa |
