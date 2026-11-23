# Motion graphics của ICYFOX: không cảnh nào đứng yên

> **Bản v2 (23/11/2026):** quy trình dựng đầy đủ ở `edit-workflow.md`, thư viện hiệu ứng ở `edit-library.md`, công thức theo thể loại ở `genre-recipes.md`. File này giữ mốc đo chuyển động và 3 lớp chuyển động (vẫn bắt buộc).

**Vì sao:** video 002 đạt khoảng 60 điểm. Phần mất điểm chủ yếu do phần lớn là ảnh tĩnh: phần giữa video đứng yên 71%, trong khi 5 kênh đối thủ chỉ 0–3,5% (`channel-studio/research/2026-11-23-motion/BAO_CAO_CHUYEN_DONG.md`). Nguyên nhân kỹ thuật: các cảnh chỉ có hiệu ứng **xuất hiện**, sau đó **đứng im**.

## 1. Mốc bắt buộc (đo bằng `scripts/motion_metrics.py`)
| Chỉ số | Mốc | Ý nghĩa |
|---|---|---|
| `static_pct` | **≤ 2%** | Phần thời lượng đứng yên ≥ 3 giây (freezedetect −60 dB) |
| `longest_static` | **< 4 giây** | Đoạn đứng yên dài nhất. `freezedetect d=4` phải ra rỗng |
| `pct_still` | **≤ 25%** | Phần số giây gần như không đổi |
| `sec_per_change` | **5–8 giây** (NHẬN ĐỊNH, lấy từ đối thủ dùng ảnh tĩnh) | Bao lâu đổi hình (cắt hoặc hòa) một lần |

`tasks.py done` cho việc loại **render** tự chạy `motion_metrics.py` trên file MP4 bằng chứng, và **từ chối** nếu không đạt 3 mốc đầu.

## 2. Ba lớp chuyển động cho mọi cảnh (luật dựng)
1. **Máy quay:** đẩy, kéo hoặc lia **suốt thời lượng cảnh**. Dùng ease `none` hoặc `sine.inOut`. Không bao giờ để transform đứng.
2. **Không khí:** bụi trôi, hạt film, vệt sáng quét. Luôn chạy, mờ, không giành sự chú ý.
3. **Nhịp:** cứ ≤ 8 giây có một **thay đổi đọc được**: đổi khung sang cận chi tiết, chữ hiện, đường vẽ, số đếm, vệt tô dòng tài liệu.
- Ảnh giữ trên 8 giây: **cắt sang cận chi tiết của chính ảnh đó** (crop + pan), hòa hình 0,7 giây.
- Cấm: rung hoặc lắc khung (nhận diện kênh là "chậm, có chủ đích"). Cấm animate `letterSpacing`, width, top (giật khi render); chỉ dùng transform và opacity.
- Render xác định: không dùng `Math.random`, `Date.now`, không tải từ mạng lúc render. GSAP để sẵn trong bộ chuyển động.

## 3. Bộ chuyển động có sẵn: `channel-studio/motion-kit/`
`icyfox_motion.py` sinh dự án HyperFrames từ **kế hoạch cảnh** (`plan.json`), tự gắn đủ 3 lớp cho mọi cảnh.
| Loại cảnh | Dùng khi | Chuyển động sinh ra |
|---|---|---|
| `title` | Thẻ chương, mở đầu | Nền đẩy chậm, chữ hiện, gạch kẻ chạy, chữ phóng nhẹ suốt cảnh |
| `photo` | Ảnh lưu trữ | Ảnh in trong khung trên bàn, đẩy máy; cứ khoảng 6,5 giây chuyển sang cận chi tiết (`details`: [x%, y%, độ phóng]) và lia |
| `document` | Hồ sơ, báo cáo, thư | Như `photo`, thêm vệt tô vàng chạy qua dòng quan trọng theo lời đọc (`highlights`: [x%, y%, w%, h%, giây], tính theo ảnh tài liệu) |
| `map` | Hành trình, địa điểm | Đường tự vẽ, chấm di chuyển theo đường, nhãn hiện dần, máy bám theo |
| `stat` | Con số | Số đếm lên, nhãn hiện, máy kéo lùi |
| `quote` | Trích lời nhân chứng, nhật ký | Từng chữ hiện theo nhịp, nền lia |

**Đã kiểm thật (23/11/2026, cloud):** bản thử 49,5 giây (6 cảnh, ảnh của 002):
- `lint` 0 lỗi, `check` đạt (19/19 chữ đạt WCAG AA). Render draft mất 2 phút 33 giây.
- **static_pct 0%, longest_static 0 s, pct_still 4,1%** (002: 71% và 82,1%). `sec_per_change` 8,2 giây.
- Lưới khung hình: `channel-studio/motion-kit/demo/grid.jpg`.

## 4. Khi cần hiệu ứng ngoài bộ: lấy từ repo của anh (đã đối chiếu tên có thật trong `hyperframes/registry`)
| Nhu cầu | Thành phần HyperFrames (`npx hyperframes add <tên>`) | Đọc thêm |
|---|---|---|
| Đẩy, kéo máy, chiều sâu | `push-in`, `pull-back-reveal`, `parallax-zoom`, `camera-rig-depth-stack`, `drift-hold` | motion-design-skill `director/choreography.md` |
| Lấy nét, chuyển tiêu điểm | `focus-rack`, block `rack-focus` | `reference/timing-easing-tables.md` |
| Không khí | `grain-overlay`, `vignette`, block `organic-light-leak-overlay`, block `snow`, block `godrays` | `patterns/ambient-continuous.md` |
| Bản đồ, hành trình | `svg-stroke-trace`, `arc-motion-path`, `offset-path-traveler`, block `nyc-paris-flight`, block `us-map-flow` | three.js (địa cầu 3D, tùy chọn) |
| Tài liệu, chú thích | `marker-highlight`, `inline-highlight`, `hw-underline`, `hw-callout-circle`, `hw-arrow`, `ink-bleed-reveal` | — |
| Chữ | `titlecard-calm`, `text-stagger`, `per-word-rise`, `typewriter`, `kinetic-center-build` | gsap-skills `gsap-timeline` |
| Số liệu | `count-up`, `number-pop-in`, block `data-chart`, block `mk-line-graph` | — |
| So sánh, chuyển cảnh | `before-after-wipe`, `comparison-split`, `match-cut`, `fade-through`, `directional-wipe` | `patterns/entrance-exit.md` |
| Ảnh động từ ảnh tĩnh | block `cinemagraph`, `paper-collage-reveal`, `pan-stations` | — |

Thứ tự đọc trước khi dựng: skill `/hyperframes` và `/hyperframes-registry` → `motion-design-skill/skills/motion-design/SKILL.md` → `director/choreography.md` → gsap-skills `gsap-timeline`, `gsap-performance`.

## 5. Quy trình (gắn vào `production-workflow.md`)
1. **Phân cảnh:** mỗi đoạn kịch bản có một mục trong `channel-studio/videos/NNN-slug/render/motion_plan.json`, gồm loại cảnh, độ dài theo giọng đọc thật, ảnh, chi tiết cận, vệt tô, nhãn bản đồ.
2. **Kiểm kế hoạch:** `python channel-studio/motion-kit/icyfox_motion.py validate motion_plan.json`. Phải đạt: khoảng trống giữa hai thay đổi ≤ 8 giây, ảnh có ghi công.
3. **Dựng:** `icyfox_motion.py build motion_plan.json render/` (thêm âm thanh qua khóa `audio`), hoặc viết composition riêng nhưng vẫn đủ 3 lớp ở mục 2.
4. **Kiểm:** `npx hyperframes lint` và `check` phải đạt.
5. **Render:** draft để xem, delivery để đăng.
6. **Đo:** `motion_metrics.py`, rồi `tasks.py done --evidence <mp4>` (tự từ chối nếu không đạt mốc).
