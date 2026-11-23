# Bộ chuyển động ICYFOX v2 (motion kit)

Sinh dự án HyperFrames từ kế hoạch cảnh, theo chuẩn edit. Quy trình: `.claude/skills/hoang-dung-clay-lapis-studio/references/edit-workflow.md`. Thư viện hiệu ứng (khóa nào, dùng khi nào, kết hợp ra sao): `edit-library.md`. Công thức theo thể loại: `genre-recipes.md`. Mốc đo chuyển động: `motion-graphics.md`.

## Lệnh
```bash
python channel-studio/motion-kit/icyfox_motion.py presets                       # thể loại, chuyển cảnh, kiểu chữ
python channel-studio/motion-kit/icyfox_motion.py validate <motion_plan.json>   # luật nhịp, chuyển cảnh, chữ đọc kịp, SFX, ghi công
python channel-studio/motion-kit/icyfox_motion.py build <motion_plan.json> <thư_mục_ra>
cd <thư_mục_ra> && npx -y hyperframes@0.8.171 lint . && npx -y hyperframes@0.8.171 check . && npx -y hyperframes@0.8.171 render . -q draft -o renders/x.mp4
python channel-studio/motion-kit/icyfox_motion.py finish renders/x.mp4 final.mp4  # −14 LUFS, đỉnh −1 dBTP
python .claude/skills/hoang-dung-clay-lapis-studio/scripts/motion_metrics.py final.mp4
```

## Kế hoạch cảnh (`motion_plan.json`)
```json
{"genre": "war", "seed": 23, "assets_dir": "../03_assets/img",
 "style": {"accent": "#B83A3A"},
 "voice": "../03_assets/audio/vo/full.wav", "music": "../03_assets/audio/music/bed.mp3", "voice_regions": [[0.5, 70]],
 "scenes": [
  {"type": "title", "dur": 6, "src": "a.jpg", "text": "The *Bomber* the Desert Swallowed", "letterbox": true},
  {"type": "photo", "dur": 12, "src": "a.jpg", "credit": "USAF · PD", "lower": {"title": "Lady Be Good", "sub": "B-24D"}},
  {"type": "map", "dur": 9, "route": [[420,300],[1500,860]], "places": [[420,300,"SOLUCH"],[1500,860,"WRECK"]]},
  {"type": "document", "dur": 9, "src": "macr.png", "credit": "NARA · PD", "highlights": [[8,47,84,3,1.5]]},
  {"type": "split", "dur": 8, "srcs": ["a.jpg","b.jpg"], "labels": ["1943","1958"], "credit": "…"},
  {"type": "triptych", "dur": 8, "srcs": ["a.jpg","b.jpg","c.jpg"], "credit": "…"},
  {"type": "timeline", "dur": 9, "items": [{"date": "1943", "label": "Last radio call"}]},
  {"type": "stat", "dur": 6, "value": 440, "label": "miles", "big": true, "payoff": true},
  {"type": "quote", "dur": 9, "text": "We only saw *sand*.", "by": "— DIARY", "text_fx": "typewriter", "transition": "dip"}
 ]}
```
- `dur` lấy theo giọng thật của đoạn (manifest của `voicestudio_tts.py`).
- `transition` ép chuyển cảnh vào cảnh đó; không ghi thì kit xoay vòng theo thể loại, không lặp liền, cắt/lóe ≤ 1/3.
- `*từ*` = từ nhấn (màu accent pha sáng để đạt tương phản).
- SFX tự đặt theo nguyên nhân (chuyển cảnh, tiêu đề đáp, điểm bản đồ, số lớn, chữ gõ, cao trào). Danh sách ra `sfx_cues.json`; bảng đọc được: `new_video.py cuesheet`.

## Tài nguyên đi kèm
- `sfx/`: 11 tiếng (whoosh ×3, impact ×2, pop, ping, chime, typing, key-press, riser), Pixabay Content License (dùng thương mại được). Chỉ thêm tiếng CC0, CC BY hoặc Pixabay License, ghi vào `sfx/CREDITS.md`.
- `vendor/gsap-3.14.2.min.js`: máy cloud không tải được CDN và lúc render không được tải mạng.

## Đã kiểm
- v1 (`demo/plan.json`, 23/11/2026): static 0%, pct_still 4,1% (`demo/metrics.txt`, `demo/grid.jpg`).
- v2 (`demo/plan_v2.json`, thể loại war, 9 cảnh, 74,4 giây): kết quả ở `demo/metrics_v2.txt`, `demo/loudness_v2.txt`, `demo/grid_v2.jpg`, `demo/sfx_cues_v2.json`.

## Giới hạn
- Chưa có cảnh video thật (stock footage), cảnh 3D, chuyển cảnh shader: thêm từ HyperFrames registry khi cần (`motion-graphics.md` §4).
- Bản đồ là nền lưới tự dựng; video 002 có `tools/make_maps.py` cho nền SVG thật.
- HyperFrames cảnh báo khi một composition có nhiều lớp nặng (blur, gradient tròn, clip-path); demo v2 có 30 (ngưỡng rủi ro khoảng 40). Video dài hơn nên chia thành nhiều composition theo chương.
