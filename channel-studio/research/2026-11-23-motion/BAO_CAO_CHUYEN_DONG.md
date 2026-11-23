# Báo cáo chuyển động: 5 kênh nổi bật so với ICYFOX 002 (23/11/2026)

Yêu cầu của anh (23/11): "tìm các kênh nổi bật xoay quanh chủ đề liên quan đến kênh của tôi, tìm các video có chuyển động để phân tích".

## Cách làm
- Chọn video bằng YouTube Data API (23/11/2026): trong 50 video mới nhất của mỗi kênh, lấy video dài ≥ 8 phút có nhiều lượt xem nhất. Danh sách ở `videos.json`.
- Tải 2 đoạn hình (không tiếng, 480p): 0–3 phút (mở đầu) và 15–20 phút (giữa video). Đo xong đã xóa.
- Đo bằng `scripts/motion_metrics.py`:
  - `static_pct`: phần trăm thời lượng đứng yên ≥ 3 s (ffmpeg freezedetect −60 dB).
  - `sec_per_change`: trung bình bao nhiêu giây thì đổi hình (cắt hoặc hòa tan).
  - `pct_still`: phần trăm số giây gần như không đổi.
- Xem lưới khung hình (3 s/khung) để phân loại kiểu chuyển động.
- Video 002 được cắt đúng 2 đoạn tương ứng để so.

## Kết quả đo

| Kênh (sub) | Video (lượt xem) | Đoạn | Đứng yên ≥3 s | Lâu nhất | Đổi hình mỗi | Giây gần như không đổi |
|---|---|---|---|---|---|---|
| Fall of Civilizations (1,52 tr) | The Sumerians (41,2 tr) | 0–3' | 0% | 0 s | 4,7 s | 0% |
| | | 15–20' | 0% | 0 s | 3,6 s | 0,2% |
| Real Time History (770 N) | Desert Storm (7,6 tr) | 0–3' | 0% | 0 s | 4,1 s | 3,4% |
| | | 15–20' | 3,5% | 6,8 s | 4,8 s | 14,9% |
| Johnny Harris (8,02 tr) | Is Fascism Back? (7,95 tr) | 0–3' | 0% | 0 s | 3,0 s | 1,1% |
| | | 15–20' | 0% | 0 s | 3,3 s | 0,7% |
| Uncharted Mysteries (310 N) | Greatest Discoveries of 2026 (1,31 tr) | 0–3' | 0% | 0 s | 6,0 s | 28,8% |
| | | 15–20' | 0% | 0 s | 10,7 s | 22,1% |
| Wartime Stories (856 N) | West Virginia Woods (760 N) | 0–3' | 0% | 0 s | 90 s* | 81,0% |
| | | 15–20' | 1,1% | 3,2 s | > 300 s* | 14,7% |
| **ICYFOX 002 Lady Be Good** | — | 0–3' | **14,7%** | **11,4 s** | 25,7 s | 52,2% |
| | | 15–20' | **71,1%** | **22,6 s** | 16,7 s | **82,1%** |

\* Wartime Stories dùng tranh minh họa tối, mỗi cảnh dài nhưng các lớp luôn trôi, nên không có đoạn nào đứng yên ≥ 3 s.

## Kiểu chuyển động từng kênh (xem lưới khung hình)
- **Fall of Civilizations:** quay thật cảnh hoang mạc (timelapse trời chuyển màu, mây trôi). Tranh khắc, chân dung, bản đồ cổ được đẩy máy chậm và lia dọc. Mỗi hình 4–10 s, hòa tan mềm. Đây là kiểu gần nhất với chủ đề cổ đại của ICYFOX.
- **Real Time History:** bản đồ hoạt họa là chính. Tiêu đề góc trái, ký hiệu đơn vị hiện dần từng cái, lưới ô vùng vẽ dần, máy lia trên bản đồ. Xen phim tư liệu. Thẻ số liệu nền tối có biểu tượng hiện lần lượt.
- **Johnny Harris:** người dẫn trên hình, phỏng vấn chuyên gia, phim tư liệu đen trắng, cảnh quay tay trên bàn (thẻ, sách). Nhịp nhanh nhất, đổi hình mỗi ~3 s. ICYFOX không có người dẫn, nên chỉ học nhịp, không học kiểu hình.
- **Uncharted Mysteries:** ảnh di vật đặt trong khung bo góc trên nền đen, có bụi bay. Máy đẩy vào rất chậm, mỗi ảnh 6–12 s, xen ảnh toàn cảnh bảo tàng. Kiểu "ảnh tĩnh + Ken Burns" giống ICYFOX nhất về cách làm, và vẫn không có đoạn đứng yên ≥ 3 s.
- **Wartime Stories:** tranh minh họa 2D tối màu tách lớp: tiền cảnh trượt, sương trôi, mắt phát sáng, máy lia ngang. Một cảnh giữ 30–90 s, chuyển cảnh bằng hòa qua màn đen.

## Kết luận cho ICYFOX
1. Cả 5 kênh đều có tỉ lệ đứng yên ≥ 3 s từ 0% đến 3,5%, đoạn lâu nhất ≤ 6,8 s. ICYFOX 002 có 14,7% ở phần mở đầu và 71,1% ở phần giữa. Lỗi chính là **phần thân video đứng yên**, không phải phần mở đầu.
2. Kênh dựa trên ảnh tĩnh (Uncharted Mysteries, Fall of Civilizations) đổi hình mỗi 3,6–10,7 s. ICYFOX 002 là 16,7–25,7 s, chậm hơn khoảng 2–4 lần.
3. Giữ một cảnh lâu vẫn được nếu khung hình luôn trôi (Wartime Stories). Vì vậy luật quan trọng nhất là **không đứng yên**, sau đó mới tới đổi hình thường xuyên.

## Mục tiêu đưa vào quy trình (thay mốc 6–10 s ước lượng trước đây)
- `static_pct` (đứng yên ≥ 3 s) **≤ 2%** trên toàn video, đoạn đứng yên lâu nhất **< 4 s**. Freezedetect với d=4 phải ra rỗng.
- `sec_per_change` **5–8 s** (mức của Uncharted Mysteries và Fall of Civilizations). Một ảnh không giữ quá 12 s; ảnh dài thì cắt sang cận chi tiết của chính ảnh đó.
- `pct_still` **≤ 25%** (Uncharted Mysteries 22–29%).
- Kỹ thuật lấy từ đối thủ, hợp với ICYFOX:
  - Ảnh di vật: khung bo góc trên nền tối, bụi trôi, đẩy máy chậm.
  - Bản đồ: ký hiệu hiện dần từng cái theo lời, vùng tô dần.
  - Thẻ số liệu: biểu tượng hiện lần lượt.
  - Cảnh mở đầu: hình có chuyển động thật (mây, cát, nước) nếu tìm được video Public domain hoặc CC.

Học cấu trúc, không dùng lại hình hay clip của đối thủ (luật "reused content").
