# Bộ công cụ: 16 repo của anh và vai trò trong quy trình

Anh gắn 16 repo vào phiên để có đủ kỹ năng. Mỗi repo có vai trò riêng. Có repo dùng thường xuyên, có repo chỉ dùng khi cần.

## Cách để repo có trong phiên
- **Đầy đủ nhất:** khi tạo phiên mới, chọn cả 16 repo (giống phiên ngày 22/11/2026). Skill trong từng repo (`skills/`, `.claude/skills/`) sẽ tự nạp.
- **Gọn hơn:** chỉ chọn `OpenMontage`. Thiếu repo nào thì gọi `add_repo(owner="hoangdung68789", repo="<tên>")`, clone theo lệnh trả về, rồi `register_repo_root` để nạp skill của repo đó.
- `session_start.sh` liệt kê repo nào có, repo nào thiếu. Repo nằm cạnh thư mục OpenMontage, ví dụ `/home/user/<Tên>`.

## Bản đồ repo theo bước sản xuất
| Repo (owner hoangdung68789) | Vai trò | Dùng ở bước | Cách dùng | Trạng thái trên cloud (22/11/2026) | Lưu ý |
|---|---|---|---|---|---|
| **OpenMontage** | Xương sống: pipeline, công cụ (gemini_tts, pixabay_music, video_compose), checkpoint, cổng duyệt | Mọi bước | `AGENT_GUIDE.md`, `pipeline_defs/animated-explainer.yaml`, `skills/pipelines/explainer/*` | Đã dùng, chạy được | `projects/` bị gitignore, phải sao lưu sang `channel-studio/projects/` |
| **hyperframes** | Công cụ dựng chính (HTML + GSAP thành MP4), dựng cả Shorts | 7 Dựng | Skill `/hyperframes`, `/hyperframes-cli`, `/hyperframes-registry`, `/media-use`. Lệnh `npx hyperframes lint`, `check`, `render` | Công cụ đã nhận diện được. **Chưa render thử** | Không chạy `npx skills add … --all` trong repo hyperframes (sẽ xóa thư mục `skills/`). Render phải cho kết quả giống nhau mỗi lần: không `Date.now()`, không random, không fetch khi render |
| **gsap-skills** | Kỹ thuật viết animation GSAP cho composition | 7 Dựng | Skill `gsap-core`, `gsap-timeline`, `gsap-plugins`, `gsap-performance`, `gsap-utils` | Có | Đọc trước khi viết timeline |
| **GSAP** | Mã nguồn thư viện, để tra API và plugin | 7 Dựng | Đọc `src/`, docs khi cần | Có | Không cần build |
| **motion-design-skill** | Nguyên tắc chuyển động: nhịp, easing, chuyển cảnh | 5 Phân cảnh, 7 Dựng | `skills/motion-design/SKILL.md` (gồm director, patterns, reference) | Có | Theo nhận diện "chậm, có chủ đích" của kênh |
| **three.js** | Cảnh 3D trong HyperFrames (ziggurat, tấm bảng xoay) | 5–7 (tùy chọn) | Mã nguồn thư viện. Các skill `threejs-*` (fundamentals, geometry, materials, lighting, animation…) nằm trong `OpenMontage/.claude/skills` | Có | Chỉ dùng khi cảnh 3D thật sự đáng công. Mô hình 3D phải có giấy phép dùng thương mại |
| **remotion** | Công cụ dựng thay thế. Phụ đề chữ chạy theo từng từ cho Shorts | 2 Đề xuất (phải trình bày như một lựa chọn), 7 (nếu anh chọn) | Skill `remotion-captions` (trong `remotion/.claude/skills`), `remotion-best-practices` (trong OpenMontage). `OpenMontage/remotion-composer` cần `npm install` | Chưa cài | Đề xuất luôn phải nêu cả HyperFrames lẫn Remotion |
| **whisperX** | Căn thời gian phụ đề theo từng từ từ file giọng đọc. Chép lời từ file video anh gửi | 8 Gói đăng (SRT), Nghiên cứu | `pip install whisperx` (chạy CPU được, chậm). Cần mở host `huggingface.co` để tải model | Chưa cài | Cách thay thế không cần model: đọc giọng theo từng đoạn, biết độ dài từng đoạn, rồi chia câu theo tỉ lệ |
| **yt-dlp** | Quét kênh và video đối thủ (chế độ flat) | Nghiên cứu | `scripts/research/*.py` | Chạy được | Số liệu từng video bị chặn kiểm tra bot: **không vượt**, dùng YouTube Data API |
| **Agent-Reach** | Lấy nội dung web có cấu trúc | Nghiên cứu (tùy chọn) | Đọc README trước khi dùng | Chưa dùng | Chỉ dùng cho nội dung công khai. **Không** dùng tính năng vượt tường đăng nhập, cookie hay kiểm tra bot |
| **awesome-opus5-5-videos** | Thư viện 703 prompt video dựng bằng code | 2 Đề xuất, 5 Phân cảnh (lấy cảm hứng kỹ thuật) | `prompts/`, `data/videos.json` | Có | Chỉ học kỹ thuật. Không chép thiết kế, vì quy tắc atelier và chính sách reused content |
| **agent-skills** | Kỹ năng kỹ sư: debug, test, review code, CI | Khi viết hoặc sửa script tự động (gắn phụ đề, báo cáo, tác vụ hẹn giờ) | Skill `debugging-and-error-recovery`, `test-driven-development`, `code-review-and-quality` | Có | Không dùng cho nội dung video |
| **CLI-Anything** | CLI cho phần mềm (kdenlive, shotcut, audacity, gimp, inkscape, musescore, obs…) | Dự phòng | `cli-hub install <tên>`. Cần cài phần mềm tương ứng | Chưa dùng | Hiện ffmpeg + HyperFrames đã đủ |
| **blender-skills** | 94 skill 3D (archviz, historical-worlds, lighting, camera) | Cảnh 3D cao cấp (tùy chọn) | Cần **Blender + Blender MCP chạy trên máy anh**. Cloud không có Blender | Không dùng được trên cloud | Muốn dùng thì phải gắn máy anh (Remote Control) |
| **seek-tune** | Nhận diện bài hát kiểu Shazam | Kiểm nhạc nền (tùy chọn) | Cần cài và cần API Spotify | Ưu tiên thấp | Không thay thế được Content ID của YouTube |
| **replica-skill** | Nhân bản ứng dụng | Không thuộc quy trình kênh | — | Không dùng | Có thể dùng sau nếu làm website cho kênh |
| **OmniVoice** (thêm 22/11/2026, công khai, chỉ đọc) | Mô hình chuyển văn bản thành giọng nói (TTS) hơn 600 ngôn ngữ, nhân bản giọng. Mã nguồn Apache-2.0 | Dự phòng cho bước giọng đọc | Cloud: `GIT_LFS_SKIP_SMUDGE=1 git clone --depth 1 https://github.com/hoangdung68789/omnivoice /home/user/hoangdung68789/omnivoice`. Chạy cần PyTorch, nên có GPU, tải trọng số từ huggingface.co | Máy anh: submodule `voice-lab/OmniVoice` (23/11/2026) | **Trọng số CC-BY-NC, không dùng thương mại**: trang Hugging Face k2-fsa/OmniVoice ghi "The pre-trained model is licensed under the CC-BY-NC" (đã kiểm 23/11/2026). Kênh ICYFOX kiếm tiền nên **không dùng giọng này trong video đăng kênh** |
| **VoiceStudio** (thêm 22/11/2026, công khai, chỉ đọc, 156 MB) | Ứng dụng giọng nói chạy trên máy: nhân bản giọng, lồng tiếng, đọc truyện, chép lời. Mặc định dùng OmniVoice, có thêm nhiều engine khác trong Model Manager. Ứng dụng theo AGPL-3.0 | Dự phòng cho bước giọng đọc khi hết hạn mức Gemini; lồng tiếng các bản ngôn ngữ khác (tùy chọn) | Cloud: `GIT_LFS_SKIP_SMUDGE=1 git clone --depth 1 https://github.com/hoangdung68789/voicestudio /home/user/hoangdung68789/voicestudio`. Máy anh: tải bản cài đặt trong mục Releases | Máy anh: submodule `voice-lab/VoiceStudio`, môi trường CUDA đã cài, engine VoxCPM2 (trọng số Apache-2.0) dùng để clone Algenib, xem `voice-lab/README.md` (23/11/2026) | Giấy phép AGPL chỉ áp cho ứng dụng. **Mỗi engine có giấy phép trọng số riêng**: phải kiểm trong Model Manager, chỉ chọn engine cho phép dùng thương mại. Không dùng nhân bản giọng người thật nếu chưa có sự đồng ý |

## Gợi ý theo việc
- **Dựng một chương:** motion-design-skill (định nhịp) → `/hyperframes` + gsap-skills (viết composition) → `npx hyperframes lint` và `check` → render.
- **Phụ đề chuẩn:** gemini_tts theo từng đoạn → whisperX căn từng từ (hoặc chia câu theo tỉ lệ) → 11 file SRT.
- **Shorts có chữ chạy:** HyperFrames (skill `captions-overlay` trong repo hyperframes) hoặc Remotion (`remotion-captions`).
- **Cảnh 3D:** three.js trong HyperFrames. Blender chỉ khi đã gắn máy anh.
