# Công thức dựng theo thể loại / chủ đề

Mỗi chủ đề có "ngữ pháp hình ảnh" riêng: màu phim, kiểu chữ, nhịp cắt, chuyển cảnh, âm thanh. Người xem nhận ra thể loại trong vài giây đầu nhờ những thứ này; trộn sai (ví dụ chữ tròn vui cho chuyện chiến tranh) làm mất uy tín.

Cách dùng: ghi `"genre": "<preset>"` trong `motion_plan.json`. Muốn khác preset thì thêm `"style": {...}` (khóa hợp lệ: bg, ink, accent, accent2, display, body, mono, title_case, grade, tint, flicker, weave, shot, trans, text_fx). `icyfox_motion.py presets` in danh sách preset.

Phân loại căn cứ: [Đ] = đo/tra được (nguồn ở `edit-standard.md` §3); [N] = nhận định nghề, cần kiểm bằng số liệu giữ chân của kênh (`yt_analytics_report.py`, đường giữ chân theo phút).

## 1. Năm trụ cột của kênh
### P3 Chiến tranh, quân sự → preset `war`
- **Cảm giác cần có:** tư liệu thật, căng, có sức nặng; người xem tin vì thấy giấy tờ, bản đồ, con số.
- **Màu:** ngả đơn sắc ấm (grayscale .35 + sepia .22), tương phản cao; nhấn đỏ gạch `#C8423A` cho mất mát, vàng đồng `#C9A54C` cho nhãn. [N]
- **Chữ:** Oswald in hoa (chữ hẹp kiểu quân đội), Space Mono cho mã số, ngày, tọa độ.
- **Nhịp:** góc máy 5,5 s; cắt nhanh hơn ở chiến đấu, chậm hẳn ở mất mát.
- **Chuyển cảnh:** dip (sau tin dữ), whip (đổi mặt trận), flash (nổ, pháo, va chạm), wipe (sang tài liệu), blurswap.
- **Cảnh hay dùng:** map tuyến đường + stat khoảng cách; document biên bản (MACR, điện tín); timeline; triptych vật chứng.
- **Âm thanh:** impact trầm cho nổ/va chạm, whoosh ngắn, gõ máy chữ cho điện tín; nhạc trầm, dây, ít giai điệu.
- **Tránh:** vệt máu, thi thể có vết thương (giới hạn quảng cáo, xem `policy-guardrails.md`); nhạc anh hùng ca khi nói về người chết.

### P1 Bí ẩn Trái Đất, đại dương → preset `mystery`
- **Cảm giác:** tò mò, lạnh, chậm; mỗi tiết lộ là phần thưởng.
- **Màu:** lạnh, giảm bão hòa (saturate .62, brightness .86), tông xanh biển; nhấn xanh ngọc `#5FB3C9`.
- **Chữ:** Playfair Display (có chân, cổ điển, như hồ sơ cũ), kiểu hiện `greyink` (mực đậm dần như câu hỏi đang hình thành).
- **Nhịp:** góc máy 7 s, khoảng lặng dài hơn trước câu tiết lộ.
- **Chuyển cảnh:** dissolve, blurswap, iris (thu vào điểm bí ẩn trên bản đồ), dip. Không flash.
- **Cảnh hay dùng:** map với iris vào tọa độ; photo với rack (kéo nét: mờ → rõ = "bí ẩn được làm rõ"); quote lời nhân chứng.
- **Âm thanh:** whoosh điện ảnh dài, ping cho mốc; nền ambient trầm, ít nhịp.
- **Tránh:** giật gân kiểu "lời nguyền"; mỗi bí ẩn phải kết bằng lời giải có nguồn (`content-pillars.md`).

### P4 Thảm họa, sự cố kỹ thuật → preset `disaster`
- **Cảm giác:** điều tra, chính xác, từng bước dẫn tới sự cố.
- **Màu:** tương phản cao, hơi giảm bão hòa, nhấn cam cảnh báo `#E8893A`, đỏ cho thời điểm hỏng.
- **Chữ:** Archivo Black (đậm, kiểu biển báo), IBM Plex Mono cho thông số; hiện kiểu `letters`.
- **Nhịp:** góc máy 5 s, cắt thẳng nhiều hơn (điều tra), dồn nhanh ở phút sự cố.
- **Chuyển cảnh:** cut, whip, wipe (sang sơ đồ), dip, blurswap.
- **Cảnh hay dùng:** timeline đếm ngược tới sự cố; stat (tốc độ, áp suất, số người); split thiết kế vs thực tế; sơ đồ 3D (three.js) khi có.
- **Âm thanh:** key-press cho thông số, impact khô; nhạc nhịp đều như đồng hồ.
- **Tránh:** hình nạn nhân; thảm họa mới còn tranh chấp pháp lý.

### P5 Cổ đại, thần thoại (Clay & Lapis) → preset `ancient`
- **Cảm giác:** trang trọng, ấm, cổ; như xem hiện vật trong bảo tàng.
- **Màu:** sepia .42, ấm đất nung `#B5734A` + nhấn xanh lapis `#1F4E8C` (bảng màu Clay & Lapis bắt buộc cho P5).
- **Chữ:** EB Garamond (tiêu đề), Montserrat (phụ đề).
- **Nhịp:** chậm nhất, góc máy 7,5 s; rung khung rất nhẹ (0,4).
- **Chuyển cảnh:** dissolve, iris, wipe (như lật bảng đất sét), blurswap. Không flash, không whip.
- **Cảnh hay dùng:** document cho bảng đất sét, tô dòng chữ hình nêm; photo hiện vật với pan chậm; quote câu sử thi.
- **Âm thanh:** chime thay pop, whoosh điện ảnh; nhạc nhạc cụ cổ hoặc drone.

### P2 Sinh tồn, thám hiểm → preset `survival`
- **Cảm giác:** khắc nghiệt, lạnh, thời gian cạn dần.
- **Màu:** lạnh, giảm bão hòa (.72), tông băng `#9FC9DE`, nhấn cam pháo sáng `#E8893A` cho hy vọng/cứu hộ.
- **Chữ:** League Gothic in hoa (hẹp, như nhật ký đoàn thám hiểm), kiểu `letters`.
- **Nhịp:** 6 s; dùng timeline "ngày thứ N" làm xương sống.
- **Chuyển cảnh:** dissolve (ngày trôi), whip, dip, wipe, cut.
- **Cảnh hay dùng:** map tuyến đi + điểm dừng; stat (nhiệt độ, số ngày, khẩu phần); quote nhật ký bằng typewriter.
- **Âm thanh:** gió, whoosh, pop mỗi điểm dừng; nhạc tăng dần theo ngày.

## 2. Thể loại khác (khi kênh mở rộng hoặc video lai)
| Thể loại | Preset gốc | `style` gợi ý | Ghi chú dựng |
|---|---|---|---|
| Án mạng, điều tra có thật (true crime) | `mystery` | `{"accent":"#B83A3A","grade":"saturate(.5) contrast(1.18) brightness(.82)","text_fx":"typewriter"}` | Hồ sơ, ảnh chứng cứ, timeline giờ; không hình nạn nhân; cẩn trọng pháp lý với người còn sống |
| Tiểu sử nhân vật | `ancient` hoặc `war` theo thời kỳ | `{"shot":6.5,"trans":["dissolve","dip","wipe","blurswap"]}` | lower third mỗi lần nhân vật mới; timeline cuộc đời; pull ở kết |
| Khoa học, giải thích | `disaster` | `{"grade":"contrast(1.05) saturate(1)","accent":"#3FA7D6","trans":["cut","wipe","iris","blurswap"],"flicker":0,"weave":0}` | Bỏ hạt film/rung khung (cần sạch); stat và split nhiều; sơ đồ |
| Top-N, danh sách | `disaster` | `{"trans":["whip","wipe","cut","blurswap"],"shot":4.5}` | title số thứ tự mỗi mục (`big`), nhịp đều, payoff ở mục số 1 |
| Kinh dị, chuyện rợn (chỉ chuyện có thật) | `mystery` | `{"bg":"#08090B","grade":"saturate(.35) contrast(1.25) brightness(.75)","flicker":.05,"trans":["dip","blurswap","cut"]}` | Khoảng lặng trước tiết lộ; tránh jump-scare âm lượng to |
| Thể thao, kỷ lục | `disaster` | `{"accent":"#F2C230","shot":4.0,"trans":["whip","flash","cut","wipe"]}` | stat nhiều, punch theo nhịp nhạc |
| Hàng hải, đắm tàu | `disaster` | `{"tint":"rgba(30,70,110,.2)","accent":"#E8893A"}` | map tuyến tàu, timeline phút chìm |
| Hàng không | `war` (thời chiến) / `disaster` (dân sự) | — | split thiết kế/xác máy bay; map đường bay |

Khi gặp thể loại mới: chọn preset gần nhất, đổi tối đa 4 khóa `style`, ghi lý do vào `02_storyboard/STORYBOARD.md`; nếu dùng ≥ 2 video thì thêm preset mới vào `GENRES` trong `icyfox_motion.py` và vào bảng này.

## 3. Kiểm hiệu quả theo thể loại (vòng số liệu)
- Sau mỗi video: lấy đường giữ chân (Analytics) và đánh dấu các mốc chuyển cảnh/cao trào lấy từ `sfx_cues.json`. Chỗ tụt > 5 điểm % trong 10 giây → ghi vào `06_review/REVIEW.md` loại cảnh và hiệu ứng tại đó.
- Mỗi 3 video cùng thể loại: so giữ chân 30 giây đầu và trung bình thời lượng xem. Thay đổi preset chỉ khi có số liệu, ghi vào `decisions-log.md`.
- Các nhận định [N] ở trên là GIẢ THUYẾT CẦN THỬ cho tới khi có số liệu kênh.
