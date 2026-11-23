# Kiểm định demo VFX (23/11/2026, cloud, HyperFrames 0.8.171)

Kế hoạch: `plan_vfx.json`: 12 cảnh, 82,9 giây, đủ 17 VFX, ngắt chương ở cảnh 7 → 2 composition (part0 0–43,28 s, part1 43,08–82,86 s). Render draft 538 giây.

## Số đo
| Mục | Kết quả | Mốc | Đạt |
|---|---|---|---|
| validate | đạt; 6 cảnh báo "ngoài bảng thể loại" (cố ý: demo đủ 17 VFX trong thể loại war) | — | ✔ |
| hyperframes lint | 0 lỗi, 0 cảnh báo (bản v2 chưa chia khối: 30 cảnh báo) | 0 lỗi | ✔ |
| hyperframes check | 26/26 chữ đạt WCAG AA; chuyển động 0 lỗi | đạt | ✔ |
| motion_metrics (`metrics_vfx.txt`) | static_pct 0%, longest_static 0 s, pct_still 0,6% | ≤ 2%, < 4 s, ≤ 25% | ✔ |
| Khung đen (blackdetect ≥ 0,1 s) | 0 đoạn, kể cả chỗ nối 2 composition | 0 | ✔ |
| Tiếng (`loudness_vfx.txt`) | −14,2 LUFS, đỉnh −1,4 dBTP | −14 ±1, ≤ −1 | ✔ |
| Nhấp nháy | lóe nhiều nhất 2 lần/giây (tia sét); báo động 0,9 Hz | ≤ 3/giây | ✔ |

## Lỗi tìm thấy và đã sửa
| # | Mức | Lỗi | Sửa | Kiểm lại |
|---|---|---|---|---|
| 1 | P0 | Tia sét: 2 tween cùng phần tử → tua lạnh có thể sai trạng thái (lint) | gộp thành 1 tween keyframes | lint 0 cảnh báo |
| 2 | P1 | Tiếng hiệu ứng không ghi độ dài → lint báo 21 chỗ chồng track | đo độ dài file (ffprobe), xếp track tránh chồng | lint 0 cảnh báo |
| 3 | P1 | Quả cầu lửa vô hình trên ảnh sáng (hòa trộn screen) | hòa trộn thường; khói nổ tối lại | `grid_vfx.jpg` ô 3 |
| 4 | P1 | Đèn pha vô hình trên ảnh ban ngày | đèn pha tự kèm lớp đêm | `grid_vfx.jpg` ô 2 |
| 5 | P2 | Báo động đỏ quá mờ (0,2) | 0,35, vẫn 0,9 Hz | `lightning_alarm_vfx.jpg` |
| 6 | P2 | Đỉnh tiếng −0,8 dBTP (vượt −1) | đích giới hạn đỉnh −1,5 | −1,4 dBTP |
| 7 | P1 | Kế hoạch tương đối theo thư mục đang đứng → mẫu `new_video` lấy sai ảnh | đường dẫn tính theo thư mục của kế hoạch | test |

## Giới hạn còn lại
- VFX là lớp 2D chồng lên ảnh: khói, lửa không tương tác với vật trong ảnh; cảnh 3D thật cần three.js hoặc Blender.
- Âm thanh tự tổng hợp nghe "sạch" hơn bản thu thật; nếu cần chân thực hơn, thay bằng bản CC0 ghi trong `sfx/CREDITS.md`.
