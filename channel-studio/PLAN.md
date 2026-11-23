# KẾ HOẠCH HIỆN HÀNH: chặng 23/11/2026 – 14/02/2027

Bản tóm tắt để AI không quên kế hoạch. Bản chi tiết (căn cứ, số liệu, ngưỡng): `research/2026-11-22-wartimestories/KE_HOACH_90_NGAY.md` (bản 2).
Hook đọc 2 khối `phases` và `releases` dưới đây để báo giai đoạn hiện tại, ngày đăng sắp tới và việc trễ tiến độ. **Sửa lịch thì sửa ở đây** và ghi lý do vào decisions-log.

<!-- pulse:start -->
- Nhịp đăng (anh chốt 22/11/2026): 1–2 video mỗi ngày, 30–60 video mỗi 30 ngày, tính cả Shorts. Ổn định: 8 video dài (thứ Ba và thứ Sáu, 21:00 giờ Việt Nam) + khoảng 38 Shorts.
- Shorts có chủ đề riêng (anh 23/11/2026): chuỗi **Earth's Unsolved** (bí ẩn Trái Đất, đại dương, vùng cực; trụ cột P1); chỉ đôi khi mới cắt từ video dài. Không để YouTube gắn nhãn AI (policy-guardrails §Khai báo AI).
- Shorts bắt đầu 01/12/2026, mỗi ngày 1 Short. Video dài đầu tiên: 002 Lady Be Good đăng công khai ngay 23/11/2026 (anh yêu cầu, không hẹn giờ). 001 Gilgamesh dời sang 25/12.
- Mốc kiểm: 28/12/2026. Lên 2 video dài mỗi tuần nếu mỗi video làm xong trong tối đa 2 ngày và không bị gắn cờ. 14/02/2027: lập chặng mới từ số liệu.
- Chế độ tự lái (anh giao toàn quyền 22/11/2026): AI tự chọn chủ đề, viết, dựng, đóng gói, tự duyệt, áp gói đăng và hẹn giờ. Không còn lô duyệt tuần. Chủ nhật gửi anh báo cáo số liệu và doanh thu.
- Tải video lên: khi Google duyệt audit API (hồ sơ `channel/api-audit/DON_AUDIT.md`), AI tự tải lên bằng `yt_publish.py upload`. Trước đó, thứ Bảy AI gửi danh sách MP4, anh kéo thả vào YouTube Studio (để Riêng tư), AI làm phần còn lại.
<!-- pulse:end -->

## Giai đoạn
<!-- phases
2026-11-23|2026-11-30|0. Chuẩn bị|Duyệt dàn ý 002; chốt giọng; render thử 3 phút để đo thời gian; làm sẵn 10 Shorts đầu; thử áp gói đăng bằng API
2026-12-01|2026-12-10|1. Khởi động|1 Short mỗi ngày lúc 21:00 giờ Việt Nam; 002 đã đăng 23/11
2026-12-11|2026-12-31|2. Tăng tốc|1 video dài mỗi thứ Sáu + 1 Short mỗi ngày; kiểm cổng ngày 28/12
2027-01-01|2027-02-14|3. Ổn định|2 video dài (thứ Ba, thứ Sáu) + 1 Short mỗi ngày; ngày 14/02 lập chặng mới
-->

| Giai đoạn | Thời gian | Việc chính |
|---|---|---|
| 0. Chuẩn bị | 23–30/11/2026 | Duyệt dàn ý 002, chốt giọng, render thử 3 phút để đo thời gian, làm sẵn 10 Shorts đầu |
| 1. Khởi động | 01–10/12/2026 | 1 Short mỗi ngày |
| 2. Tăng tốc | 11–31/12/2026 | 1 video dài mỗi thứ Sáu, 1–2 Shorts mỗi ngày |
| 3. Ổn định | 01/01–14/02/2027 | 2 video dài mỗi tuần, 1–2 Shorts mỗi ngày |

## Lịch video dài (21:00 giờ Việt Nam)
<!-- releases
2026-11-23|002|The Bomber the Desert Swallowed: Lady Be Good
2026-12-18|003|Foo Fighters: What Chased Allied Pilots in 1944
2026-12-25|001|Gilgamesh: The Lost Lines
2027-01-01|004|Ramree Island 1945: The Swamp Legend
2027-01-05|011|The Halifax Explosion 1917
2027-01-08|005|USS Cyclops 1918
2027-01-12|012|Shackleton's Endurance
2027-01-15|006|The Angels of Mons
2027-01-19|013|Tunguska 1908
2027-01-22|007|Hiroo Onoda: 29 Years in the Jungle
2027-01-26|014|The Mary Celeste
2027-01-29|008|The Battle of Los Angeles 1942
2027-02-02|015|The Lost Franklin Expedition
2027-02-05|009|Fu-Go: Japan's Balloon Bombs
2027-02-09|016|The Dyatlov Pass Incident
2027-02-12|010|Flight 19 (1945)
-->
Bằng chứng nhu cầu của từng chủ đề: KE_HOACH_90_NGAY.md mục 2. Chủ đề nào ở đó ghi [cần quét riêng] thì phải quét bằng `niche_outliers.py` hoặc `story_scan.py` trước khi viết dàn ý.

**Thay chủ đề:** autopilot được đổi một chủ đề chưa viết sang ý tưởng "Sẵn sàng" có điểm cao hơn trong `ideas/IDEA_BANK.md`, nhưng phải ghi lý do vào nhật ký và nêu trong báo cáo Chủ nhật. Không đổi nhịp đăng anh đã chốt (1–2 video mỗi ngày); ngày đăng từng video được dời khi cần, có ghi lý do.

## Ngưỡng quyết định
Theo KE_HOACH_90_NGAY.md mục 5. Ví dụ: CTR dưới 3% sau 48 giờ thì đổi thumbnail hoặc tiêu đề. Sau 8 video dài, trụ cột nào dưới 50% trụ cột mạnh nhất thì dồn lịch sang 2–3 trụ cột mạnh. CTR lấy từ file xuất của YouTube Studio vì API không có (`analytics-loop.md`).

## Khi chặng này hết
Trước ngày 31/01/2027, autopilot soạn chặng mới (request-playbooks mục B), dựa trên báo cáo số liệu kênh và radar. Mục tiêu trong `MISSION.md` không bao giờ hết hạn.
