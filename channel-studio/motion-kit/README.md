# Bộ chuyển động ICYFOX v2 + VFX (motion kit)

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

## VFX chuyên dụng (bật khi cần)
Khóa `vfx` của cảnh, 17 hiệu ứng: không khí (rain, snow, sandstorm, fog, smoke, embers, rays, caustics, searchlight, alarm) và sự kiện
(shake, explosion, lightning, glitch, filmburn, sparks, radio). Cách dùng, luật, công thức theo chủ đề: `edit-library.md` §10, `genre-recipes.md` §4.
```json
{"type": "photo", "dur": 8, "src": "storm.jpg", "credit": "…", "vfx": ["rain", {"fx": "lightning", "at": 2.5}]}
```
- Mã: `vfx.py`. Tài nguyên tự sinh: `python vfx_assets.py` → `vfx/tex/*.png` (14 kết cấu lặp liền mép) và `sfx/synth/*.mp3` (8 tiếng). Không dùng file của ai.
- Chia khối dựng: mỗi composition tối đa 6 cảnh (`"chunk": N` để đổi), hoặc ngắt ở cảnh `"chapter": true`. File ra: `compositions/part0.html`, `part1.html`…
- Luật an toàn: ≤ 3 lần lóe/giây (WCAG 2.3.1), ≤ 2 lớp không khí/cảnh, 2 cú lớn cần cảnh ≥ 8 giây.

## Tài nguyên đi kèm
- `sfx/`: 14 tiếng (whoosh ×3, impact ×2, pop, ping, chime, typing, key-press, riser, glitch ×3), Pixabay Content License (dùng thương mại được); `sfx/synth/`: 8 tiếng tự tổng hợp. Chỉ thêm tiếng CC0, CC BY hoặc Pixabay License, ghi vào `sfx/CREDITS.md`.
- `vendor/gsap-3.14.2.min.js`: máy cloud không tải được CDN và lúc render không được tải mạng.

## Đã kiểm
- v1 (`demo/plan.json`, 23/11/2026): static 0%, pct_still 4,1% (`demo/metrics.txt`, `demo/grid.jpg`).
- v2 (`demo/plan_v2.json`, thể loại war, 9 cảnh, 74,4 giây): kết quả ở `demo/metrics_v2.txt`, `demo/loudness_v2.txt`, `demo/grid_v2.jpg`, `demo/sfx_cues_v2.json`.

## Giới hạn
- Chưa có cảnh video thật (stock footage), cảnh 3D, chuyển cảnh shader: thêm từ HyperFrames registry khi cần (`motion-graphics.md` §4).
- Bản đồ là nền lưới tự dựng; video 002 có `tools/make_maps.py` cho nền SVG thật.
- Đã xử lý: kit tự chia composition nên không còn cảnh báo lớp nặng (demo VFX 12 cảnh: lint 0 lỗi, 0 cảnh báo).
- VFX là lớp 2D trên ảnh, không phải mô phỏng 3D: khói/lửa không tương tác với vật trong ảnh. Cảnh 3D thật vẫn cần three.js hoặc Blender.
