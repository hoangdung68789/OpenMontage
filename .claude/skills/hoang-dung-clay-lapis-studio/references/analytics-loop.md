# Vòng số liệu: AI tự tìm video được quan tâm nhất và dùng nó để làm video tiếp theo

Mục tiêu (`MISSION.md`): mọi quyết định về chủ đề, tiêu đề, thumbnail, độ dài và nhịp đăng đều dựa trên số liệu thật mà AI tự lấy và tự phân tích.

## 1. Ba nguồn số liệu (thứ tự tin cậy)
| # | Nguồn | Script | Cho biết gì | Tần suất |
|---|---|---|---|---|
| 1 | **Kênh mình**: YouTube Analytics API | `scripts/research/yt_analytics_report.py` | Giờ xem, giữ chân %, thời gian xem TB, sub, nguồn lưu lượng, quốc gia, đường giữ chân, 7 ngày đầu của từng video | Thứ Hai hằng tuần. Thêm một lần 7 ngày sau mỗi video dài |
| 2 | **Thị trường lúc này**: radar Data API | `scripts/research/niche_outliers.py --days 7` | Video mới (≤ 7 ngày) đang có đà trong 5 trụ cột, nhãn VIRAL (≥ 5 lần TB 10 video của chính kênh đó), lượt xem/giờ | 2 ngày một lần. Chạy lại để có số liệu 2 thời điểm |
| 3 | **Đối thủ**: Data API | `scripts/research/yt_api_channel.py` | Quy luật dài hạn của kênh lớn | Khi anh gửi link, hoặc mỗi tháng 1 kênh |

**Giới hạn đã kiểm thật (22/11/2026):**
- API **không** có số lần hiển thị thumbnail và CTR (truy vấn bị trả 400). Lấy từ YouTube Studio: Analytics → Advanced mode → Export → file `Table data.csv`. Rồi chạy `yt_analytics_report.py --studio-csv "<file>"`. Đây là một trong các việc anh làm, gộp vào lúc anh tải video mỗi tuần.
- Doanh thu (`estimatedRevenue`) bị trả 401 vì thiếu quyền `yt-analytics-monetary.readonly`. Sau khi vào YPP: xin lại refresh token có thêm quyền này (OAuth Playground, như lần đầu), cập nhật `YT_REFRESH_TOKEN`.

## 2. Định nghĩa (NHẬN ĐỊNH, xem lại khi kênh có ≥ 10 video dài)
- **Video THẮNG (kênh mình):**
  - Video dài: giờ xem 7 ngày đầu ≥ 2 lần trung vị các video dài.
  - Shorts: lượt xem 7 ngày đầu ≥ 2 lần trung vị Shorts.
  - Cần ít nhất 3 video cùng loại mới xét.
- **Video YẾU:** ≤ 0,5 lần trung vị.
- **Ứng viên thị trường:** radar gắn nhãn VIRAL hoặc VƯỢT TRỘI, ≥ 20.000 lượt xem, không bị cờ ngoài phạm vi (hư cấu, lịch sử giả, true crime…).
- **ĐANG LÊN – ĐÃ KIỂM CHỨNG:** đủ 2 bằng chứng. Ví dụ: radar 2 lần cách 24–48 giờ cho thấy lượt xem tăng, cộng nhãn VIRAL.

## 3. Từ số liệu đến video (bắt buộc làm hết, không dừng ở báo cáo)
1. **Video thắng** → viết vào `analytics/WINNERS.md`, cột "Quy luật":
   - chủ đề, trụ cột, dạng (lẻ hay series)
   - công thức tiêu đề, kiểu thumbnail, kiểu hook (giây 0–30)
   - độ dài, nguồn lưu lượng chính, mốc giữ chân rơi mạnh.
   Sau đó tạo **2–3 ý tưởng "cùng gen"** trong `ideas/IDEA_BANK.md`: cùng sức hút, **khác chủ đề và cách làm** (không tự sao chép, tránh nội dung rập khuôn).
2. **Video yếu** → ghi 1 giả thuyết (tiêu đề, thumbnail, hook hay chủ đề) và 1 thử nghiệm cho video kế tiếp. Ghi trong IDEA_BANK, mục "Thử nghiệm".
3. **Ứng viên radar** → thêm vào IDEA_BANK kèm link, lượt xem, giờ tra, nhãn. Chấm điểm (mục 4). Đạt thì chuyển "Sẵn sàng".
4. **Series thắng:** tập 1 thắng thì cân nhắc kéo dài (`series-playbook.md` §2). Series yếu thì rút ngắn.
5. **Kế hoạch:** ý tưởng "Sẵn sàng" có điểm cao nhất thay chủ đề chưa viết có điểm thấp nhất trong PLAN, ghi vào HANDOFF và nêu trong báo cáo Chủ nhật (lô duyệt tuần đã bỏ 22/11/2026).
6. **Trụ cột:** sau 8 video dài, trụ cột dưới 50% trụ cột mạnh nhất thì giảm tần suất (`KE_HOACH_90_NGAY.md` §5).

## 4. Chấm điểm ý tưởng (0–5 mỗi tiêu chí, nhân lại; ≥ 27 điểm thì "Sẵn sàng")
- **Nhu cầu (N):** 5 = kênh mình đã thắng với chủ đề cùng gen, hoặc radar VIRAL ≥ 100K. 3 = đối thủ ≥ 3 lần TB. 1 = chỉ là giả thuyết.
- **Phù hợp (P):** 5 = đúng trụ cột, có hồ sơ thật, an toàn quảng cáo. 0 = ngoài phạm vi hoặc rủi ro chính sách (loại luôn).
- **Khả thi (K):** 5 = đủ nguồn và ảnh có giấy phép, làm trong 2 ngày. 1 = thiếu nguồn hoặc thiếu hình.
- Ghi điểm dạng `N×P×K = …`. Ý tưởng theo mùa (ví dụ Lễ Tạ ơn) phải xong trước dịp đó ít nhất 14 ngày, không kịp thì để năm sau.

## 5. Nơi lưu
| File | Nội dung |
|---|---|
| `analytics/reports/<ngày>/report.md` + `data.json` | Báo cáo kênh từng lần |
| `analytics/WINNERS.md` | Video thắng và quy luật (chỉ thêm) |
| `analytics/video_map.json` | YouTube ID → thư mục video, trụ cột, series, tập, kiểu hook (`yt_publish.py` ghi; AI bổ sung "hook") |
| `research/<ngày>-radar/` | Radar xu hướng |
| `ideas/IDEA_BANK.md` | Kho ý tưởng có bằng chứng và điểm |
