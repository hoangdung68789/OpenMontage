# Bản đồ đọc: loại việc nào thì đọc file nào, dùng công cụ nào, giao gì

Mọi đường dẫn tính từ gốc repo OpenMontage. `SK` = `.claude/skills/hoang-dung-clay-lapis-studio`. `CS` = `channel-studio`.
Luôn đọc trước: `CS/MISSION.md` → `CS/PLAN.md` → `CS/HANDOFF.md` → `CS/TASKS.md` → `SK/references/work-contract.md`. Hook đã in phần tóm tắt, nhưng việc lớn thì phải đọc file gốc.
Trên Windows dùng `python`, trên cloud dùng `python3`.

## 1. Bảng tra theo loại việc
| Việc (anh nói / autopilot giao) | Đọc bắt buộc (theo thứ tự) | Công cụ / script | Repo, skill hỗ trợ | Sản phẩm (xong khi) | Loại thẻ |
|---|---|---|---|---|---|
| Mở phiên, "làm tiếp", "trạng thái" | Bốn file trên, `CS/logs/<tháng>.md` (5 mục cuối) | `bash SK/scripts/session_start.sh`, `SK/scripts/autopilot.py` | — | Báo anh 3 dòng: API, việc hôm nay, việc chờ anh | ops |
| Phân tích kênh đối thủ (link) | `SK/references/request-playbooks.md` mục A, `research-playbook.md`, `content-pillars.md` | `SK/scripts/research/yt_api_channel.py`, `yt-dlp --write-auto-subs` (phụ đề), ffmpeg (lưới thumbnail) | yt-dlp | `BAO_CAO.md`, `KE_HOACH_*.md`, dàn ý + hook video đầu, dòng Notion | competitor |
| Tìm chủ đề, xu hướng, "video đang được quan tâm" | `analytics-loop.md`, `content-pillars.md`, `CS/ideas/IDEA_BANK.md`, radar gần nhất `CS/research/*-radar/RADAR.md` | `SK/scripts/research/niche_outliers.py --days 7`, `story_scan.py` | — | `RADAR.md` mới + ý tưởng có bằng chứng trong IDEA_BANK | research / ideas |
| Báo cáo kênh mình, "số liệu", "báo cáo tuần" | `analytics-loop.md`, `CS/analytics/WINNERS.md`, báo cáo trước | `SK/scripts/research/yt_analytics_report.py` (+ `--studio-csv` nếu anh gửi file CTR) | — | `CS/analytics/reports/<ngày>/report.md` + `data.json`, cập nhật WINNERS và IDEA_BANK | analytics |
| Lập hoặc sửa kế hoạch | `MISSION.md`, `PLAN.md`, `KE_HOACH_90_NGAY.md`, báo cáo số liệu mới nhất, IDEA_BANK, `decisions-log.md` | `autopilot.py` | — | `PLAN.md` (khối phases và releases) + `KE_HOACH_*.md` + dòng decisions-log | plan |
| Video mới (đề xuất, dàn ý) | `SK/scripts/new_video.py create NNN-slug --title … --genre …` (tạo thư mục v2), `production-workflow.md`, `content-pillars.md`, `policy-guardrails.md`, `OpenMontage/skills/pipelines/explainer/research-director.md` và `proposal-director.md`, `AGENT_GUIDE.md` | OpenMontage pipeline `icyfox-autopilot` (`pipeline_defs/icyfox-autopilot.yaml`) | OpenMontage | `CS/videos/NNN-slug/README.md`, `script_outline.md` (hook 60 giây đầy đủ, chương, nguồn) → AI tự duyệt, ghi HANDOFF (anh giao toàn quyền 22/11/2026) | outline |
| Series: tập mới hoặc tập tiếp | `series-playbook.md`, `CS/series/<id>/SERIES.md` | **`SK/scripts/series.py brief <id>`** (bắt buộc), `series.py episode …` | — | Kịch bản tập + `series.json` đã cập nhật (tóm tắt, cliffhanger, tuyến) | series + script |
| Viết phần kịch bản | `script_outline.md` đã duyệt, phần trước, `templates/script_section_template.md`, `explainer/script-director.md` | `SK/scripts/qa_check.py <file> --mark` | — | `script_partN.md` QA ĐẠT | script |
| Mẫu giọng, giọng đọc | `references/decisions-log.md` (dòng 23/11 VoiceStudio), `references/toolbox-repos.md` (VoiceStudio), `production-workflow.md` §Giọng | **`SK/scripts/voice/voicestudio_tts.py check|sample|narrate`** (VoiceStudio trên máy anh, engine VoxCPM2, hồ sơ `icyfox-narrator`); dự phòng `OpenMontage/tools/audio/gemini_tts.py` | VoiceStudio (KHÔNG dùng OmniVoice: CC-BY-NC) | File WAV theo đoạn + `manifest.json` (engine, giấy phép, giây, từ/phút) | voice |
| Phân cảnh, tài nguyên, dựng (chủ đề khó: thêm `edit-library.md` §10 VFX) | **`references/edit-workflow.md`**, `edit-library.md`, `genre-recipes.md`, `motion-graphics.md`, `CS/motion-kit/README.md`, `production-workflow.md`, `toolbox-repos.md`, `explainer/scene-director.md`, `asset-director.md`, `compose-director.md` | `npx hyperframes lint`, `check`, `render` | hyperframes, gsap-skills, motion-design-skill, three.js | `render/` + MP4 + `render/RENDERED.txt` (đường dẫn, dung lượng, thời gian render) | scene / render |
| Shorts | `KE_HOACH_90_NGAY.md` §3, `publish-package.md` | HyperFrames (skill captions-overlay) hoặc Remotion (`remotion-captions`) | hyperframes, remotion | `CS/shorts/SNN-slug/` gồm kịch bản, MP4, `package/` (có `publish_at.txt`) | shorts |
| Gói đăng | `publish-package.md` | — | — | `package/` có title.txt, description.md, tags.txt, thumbnail, `subtitles/*.srt`, `i18n.json`, `publish_at.txt` | package |
| Áp gói lên video anh đã tải, hẹn giờ, phụ đề | `autopilot.md` §3, `publish-package.md` | `SK/scripts/yt_publish.py scan` → `auto` | — | `package/UPLOADED.txt`, `CS/analytics/video_map.json` | publish |
| Sửa công cụ, viết mã (thường giao Codex) | `multi-agent.md`, file mã liên quan, test có sẵn | pytest, `tasks.py done --check "<lệnh test>"` | agent-skills (debugging, TDD) | Mã + test chạy đạt | code |
| Đổi máy, cài máy mới, khôi phục | `CS/guides/KHOI_PHUC_MAY_MOI.md`, `CS/guides/local_setup.md` | `SK/scripts/restore_machine.sh` (Git Bash) | — | API OK, 8/8 kiểm thử đạt, 2 tác vụ hẹn giờ tạo lại, hook chạy | ops |
| Đóng phiên, "lưu" | SKILL.md mục 5 | `SK/scripts/session_end.py -m "…" --trailer "…"` | — | Commit đã đẩy lên nhánh `ccr-6640cec8-2anthl` | ops |

## 2. Tài nguyên dùng chung
| Tài nguyên | Ở đâu |
|---|---|
| Khóa API | Cloud: Network secrets + biến môi trường. Máy anh: `OpenMontage/.env` (mẫu `CS/config/api_keys.env.example`) |
| Số liệu đối thủ đã có | `CS/research/2026-11-22-wartimestories/` (API, phụ đề, bình luận), `CS/research/2026-11-22-story-niches/` |
| Radar xu hướng | `CS/research/<ngày>-radar/RADAR.md` + `outliers.json` |
| Kho ý tưởng | `CS/ideas/IDEA_BANK.md` |
| Video thắng và quy luật | `CS/analytics/WINNERS.md` |
| Series | `CS/series/SERIES_INDEX.md`, `CS/series/<id>/SERIES.md` |
| Nhật ký lịch sử | `CS/logs/<năm-tháng>.md` |
| Bảng Notion | data source `collection://4201dcd7-7c95-8188-8452-000b17602005` |
| 16 repo | `SK/references/toolbox-repos.md` |

## 3. Đường dự phòng khi lỗi (thử hết trước khi báo bị chặn)
| Lỗi | Cách 1 | Cách 2 | Cách 3 |
|---|---|---|---|
| Data API 403 hoặc hết hạn mức | Đọc thông báo: API chưa bật thì hướng dẫn anh bật | Hết hạn mức thì giảm `--pillars` và `--per-query`, chạy lại hôm sau | yt-dlp chế độ flat (chỉ lấy tiêu đề và lượt xem) |
| yt-dlp bị YouTube nghi bot | Dùng Data API thay thế | Phụ đề: chạy trên máy anh | Phân tích từ mô tả và mốc chương (API) |
| Analytics không có số liệu | Kênh mới hoặc trễ 1–3 ngày: dùng radar và đối thủ | Thu hẹp khoảng ngày | Ghi "GIẢ THUYẾT" |
| Gemini TTS 404 | Sửa công cụ sang API v1beta (việc của Codex) | ElevenLabs gói trả phí (nếu anh đã nâng) | OpenAI TTS (cần nạp tiền) |
| Render chậm hoặc lỗi | `--quality draft` để kiểm | `npx hyperframes doctor` | Render trên máy anh (`local-render.md`) |
| `videos.update` bị từ chối khi hẹn giờ | Đọc lỗi nguyên văn | Áp metadata, để anh tự bấm hẹn giờ | Ghi vào HANDOFF, đề xuất audit API |
| Push git bị từ chối | `git fetch origin ccr-6640cec8-2anthl && git merge --no-edit FETCH_HEAD` | Xử lý xung đột từng file | Không bao giờ dùng `--force` |
| Tác vụ nền lỗi, treo, hết hạn mức; tìm phương án thay thế | `fallbacks.md` | `SK/scripts/watchdog.py` | — | thẻ `tasks.py` (lỗi, đã thử gì, khi nào chạy lại), `CS/state/jobs/*.log` | — |
