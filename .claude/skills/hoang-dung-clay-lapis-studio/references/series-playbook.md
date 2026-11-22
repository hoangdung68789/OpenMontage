# Series nhiều tập: nhớ tập đã làm, viết tiếp đúng mạch, kết thúc đúng chỗ

Ví dụ: series "thám hiểm rừng sâu" gồm tập 1 → tập 2 → tập 3 (KẾT THÚC), rồi bắt đầu một câu chuyện mới.
Bộ nhớ series nằm trong git, không nằm trong trí nhớ của AI: `channel-studio/series/<id>/series.json`, do `scripts/series.py` quản lý.

## 1. Khi nào làm series (NHẬN ĐỊNH, chỉnh theo số liệu)
- Câu chuyện có từ 2 hồi tách bạch trở lên, mỗi hồi đủ 25–40 phút có nguồn. Ví dụ: một cuộc thám hiểm dài nhiều tháng, một chiến dịch nhiều giai đoạn.
- Gộp vào 1 video sẽ dài quá khoảng 45 phút, hoặc phải cắt bỏ phần hay.
- Dàn ý tập 1 đứng được một mình: người xem chỉ xem tập 1 vẫn nhận đủ giá trị.
- Không làm series để kéo dài cho có. Chính sách inauthentic content xét cả kênh, và tập độn chữ làm tụt tỉ lệ giữ chân.

## 2. Độ dài và điểm kết thúc
- Chốt số tập **ngay khi tạo series**: 2–6 tập (`series.py new … --episodes N`). Mỗi tập ghi 1 dòng mạch (`--arc`).
- Tập N là **TẬP CUỐI**. `series.py` từ chối thêm tập N+1.
- **Kéo dài** chỉ khi có số liệu (ví dụ: tập 1 có giờ xem 7 ngày gấp 2 lần trung vị kênh) **và** ghi lý do vào HANDOFF + báo cáo Chủ nhật (AI tự quyết từ 22/11/2026): `series.py extend <id> --to N --reason "số liệu"`. Tối đa 6 tập.
- **Rút ngắn**: nếu tập 1 sau 7 ngày dưới 0,5 lần trung vị kênh, gộp các tập còn lại vào tập cuối. Ghi vào decisions-log.

## 3. Quy trình mỗi tập
1. **Trước khi viết:** `python SK/scripts/series.py brief <id>`. Dán phần "Câu chuyện đến nay", "Tập trước kết ở đâu", "Tuyến đang mở" và "Dữ kiện phải nhất quán" vào đầu `script_outline.md` của tập, mục "Bối cảnh series".
2. **Viết theo yêu cầu bắt buộc** mà `brief` in ra:
   - Tập 2 trở đi: mở bằng đoạn nhắc lại tối đa 45 giây, có ý mới, không chép lời tập trước.
   - Tập chưa phải tập cuối: kết bằng cliffhanger, không khép tuyến chính.
   - **Tập cuối:** khép mọi tuyến đang mở, nói rõ "This is the final part of …", giới thiệu câu chuyện mới.
3. **Viết xong và QA đạt:** `series.py episode <id> <n> --status approved --title "…" --video-dir videos/NNN-slug --summary "…" --cliffhanger "…" --open "tuyến mới" --close TH1`.
4. **Dữ kiện cần nhất quán** (tên, ngày, số người, địa danh): `series.py fact <id> "…" --source "link" --ep n`.
5. **Sau khi đăng:** `series.py episode <id> <n> --status published --youtube-id … --date YYYY-MM-DD`. Thêm vào `analytics/video_map.json` các trường series và episode (`yt_publish.py` ghi phần còn lại).
6. **Sau khi tập cuối đã đăng:** `series.py end <id> --next "<câu chuyện kế tiếp>"`. Series chuyển sang ĐÃ KẾT THÚC, không sửa được nữa. Câu chuyện kế tiếp phải có trong IDEA_BANK hoặc PLAN.

## 4. Trên YouTube
- Tiêu đề: `<Tiêu đề riêng của tập> (Part n of N)`. Danh sách phát riêng cho series, sắp đúng thứ tự.
- Mô tả: link tập trước, link danh sách phát. Màn hình kết thúc trỏ sang tập sau, khi tập sau đã đăng.
- Shorts cắt từ series trỏ về **Part 1**.
- Lịch: mỗi tập cách nhau 3–7 ngày, giữ đúng thứ tự đăng (`series.py` chặn đăng sai thứ tự).

## 5. Lệnh nhanh
| Việc | Lệnh |
|---|---|
| Xem mọi series | `python SK/scripts/series.py status` |
| Bối cảnh để viết tập kế | `python SK/scripts/series.py brief <id>` |
| Tạo series | `python SK/scripts/series.py new <id> --title … --pillar P2 --episodes 3 --premise … --arc "…\|…\|…"` |
| Kết thúc | `python SK/scripts/series.py end <id> --next "…"` |
