# Kiểm định demo v2 (23/11/2026, cloud, HyperFrames 0.8.171)

Kế hoạch: `plan_v2.json` (thể loại war, 9 cảnh, 74,4 giây, ảnh của video 002). Render draft: 350 giây.

## Số đo
| Mục | Kết quả | Mốc | Đạt |
|---|---|---|---|
| validate | 48 thay đổi thị giác (trung bình 1,5 s), khoảng trống lớn nhất 5,9 s | ≤ 8 s | ✔ |
| Chuyển cảnh | 8 mối nối: dip, whip, flash, wipe, blurswap, dip, whip, flash; không lặp liền; cắt/lóe 2/8 | ≤ 1/3 | ✔ |
| SFX | 17 tiếng, 13,7/phút, 1 riser | ≤ 15/phút, ≤ 1 riser | ✔ |
| hyperframes lint | 0 lỗi (30 cảnh báo: file lớn, 30 lớp nặng) | 0 lỗi | ✔ |
| hyperframes check | 51/51 chữ đạt WCAG AA, chuyển động 0 lỗi | đạt | ✔ |
| motion_metrics (`metrics_v2.txt`) | static_pct 0%, longest_static 0 s, pct_still 4,1% | ≤ 2%, < 4 s, ≤ 25% | ✔ |
| Tiếng (`loudness_v2.txt`) | −14,0 LUFS, đỉnh −3,5 dBTP (trước: −11,25 LUFS, −1,43 dBTP) | −14 ±1, ≤ −1 dBTP | ✔ |

## Lỗi tìm thấy và đã sửa
| # | Mức | Lỗi | Sửa | Kiểm lại |
|---|---|---|---|---|
| 1 | P0 | lint: cảnh vào bằng whip/iris/wipe thiếu `opacity:1` ở đích → máy render lạnh có thể ra khung trống | thêm `opacity:1` vào đích tween | lint 0 lỗi |
| 2 | P1 | Tiêu đề trên ảnh sáng: tương phản 1,06–2,25:1 | lớp tối `tscrim` sau tiêu đề; từ nhấn pha 30% trắng | 51/51 AA |
| 3 | P1 | Thanh tên "Lady Be Good" đè phụ đề góc dưới trái (grid khung 2) | thanh tên lên góc trên-trái trong vùng an toàn | `lowerthird_v2.jpg` |
| 4 | P2 | "sand ." dấu cách trước dấu chấm (dấu câu sau từ nhấn thành từ riêng) | dấu câu dính vào khối từ nhấn | `grid_v2.jpg` khung 15 |
| 5 | P1 | validate: cắt/lóe 3/8 > 1/3, SFX 15/phút | đổi bộ chuyển cảnh war/disaster; một whoosh cho cả cụm triptych | validate đạt |

## Còn lại
- 30 lớp nặng trong một composition; video 30 phút phải chia composition theo chương (ngưỡng rủi ro khoảng 40).
- Ô cuối của lưới đen vì lưới 16 ô dài 80 giây, video 74,4 giây (không phải lỗi).
