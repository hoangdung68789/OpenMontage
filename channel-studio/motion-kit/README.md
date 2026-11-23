# Bộ chuyển động ICYFOX (motion kit)

Bộ này sinh dự án HyperFrames trong đó **mọi cảnh luôn chuyển động**. Quy tắc và mốc đo: `.claude/skills/hoang-dung-clay-lapis-studio/references/motion-graphics.md`.

## Dùng
```bash
python channel-studio/motion-kit/icyfox_motion.py validate <motion_plan.json>          # kiểm trước: khoảng trống <= 8 s, ảnh có ghi công
python channel-studio/motion-kit/icyfox_motion.py build <motion_plan.json> <thư_mục_ra>
cd <thư_mục_ra> && npx hyperframes lint . && npx hyperframes check . && npx hyperframes render . -q draft -o renders/x.mp4
python .claude/skills/hoang-dung-clay-lapis-studio/scripts/motion_metrics.py renders/x.mp4   # static_pct <= 2, longest < 4, pct_still <= 25
```

## Kế hoạch cảnh (`motion_plan.json`)
```json
{"seed": 11, "assets_dir": "thư mục ảnh", "audio": "đường dẫn mix.mp3 (tùy chọn)",
 "scenes": [
  {"type": "title", "dur": 5, "text": "THE BOMBER", "sub": "CHAPTER 1"},
  {"type": "photo", "dur": 14, "src": "a.jpg", "caption": "…", "credit": "U.S. Air Force · public domain", "details": [[35, 55, 2.2]]},
  {"type": "document", "dur": 10, "src": "macr.png", "credit": "NARA · public domain", "highlights": [[8, 47, 84, 3, 1.5]]},
  {"type": "map", "dur": 10, "route": [[420,300],[1180,640]], "places": [[420,300,"SOLUCH"]], "caption": "…"},
  {"type": "stat", "dur": 6, "value": 440, "label": "miles into the Sahara"},
  {"type": "quote", "dur": 8, "text": "…", "by": "— DIARY, 1943"}
 ]}
```
- `dur`: lấy theo độ dài giọng đọc thật của đoạn (manifest của `voicestudio_tts.py`). Các cảnh nối nhau bằng hòa hình 0,7 giây.
- `details`: [x%, y%, độ phóng] là chỗ cận chi tiết trong ảnh. Không ghi thì bộ tự chọn.
- `highlights`: [x%, y%, rộng%, cao%, giây] tính theo ảnh tài liệu. Phải rơi vào khung đầu (toàn trang), nếu không bộ sẽ báo lỗi.
- `route` và `places`: tọa độ pixel trên khung 1920x1080.

## Đã kiểm (23/11/2026, cloud, HyperFrames 0.8.171)
- `demo/plan.json`: 6 cảnh, 49,5 giây, dùng ảnh của 002.
- `lint` 0 lỗi. `check` đạt, chữ đạt WCAG AA. Render draft mất 2 phút 33 giây.
- `demo/metrics.txt`: static_pct 0%, longest_static 0 s, pct_still 4,1%, sec_per_change 8,2 s.
- Ảnh: `demo/grid.jpg` (8 khung), `demo/document_highlight.jpg` (vệt tô đi theo tài liệu).

## Giới hạn hiện tại
- Chưa có cảnh 3D, cảnh video thật (stock footage), hay chuyển cảnh shader. Khi cần thì thêm thành phần HyperFrames theo bảng ở motion-graphics.md §4.
- Bản đồ đang là nền lưới tự dựng, chưa có địa hình thật. Video 002 có `tools/make_maps.py` dùng làm nền SVG thật được.
- Vị trí vệt tô tài liệu phải đo theo từng tài liệu.
- GSAP 3.14.2 để sẵn ở `vendor/` (giấy phép "Standard no-charge" của GSAP), vì máy cloud không tải được từ CDN và lúc render không được tải gì từ mạng.
