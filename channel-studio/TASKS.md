# Sổ việc ICYFOX

Tự sinh từ `state/tasks.json`. **Đừng sửa tay**: dùng `python .claude/skills/hoang-dung-clay-lapis-studio/scripts/tasks.py`.
Cập nhật: 2026-11-23 12:44 (giờ Việt Nam).

## Đang làm (0)

(không có)

## Chờ anh quyết (0)

(không có)

## Bị chặn (0)

(không có)

## Chưa làm (theo ưu tiên) (12)

| ID | Trạng thái | Ai | Việc | Loại | Video / series | Hạn | Xong khi | Câu hỏi / lý do |
|---|---|---|---|---|---|---|---|---|
| T-002 | Chưa làm | codex | Sửa tools/audio/gemini_tts.py dùng API v1beta (model gemini-3.8-flash-tts báo 404) | code |  | 2026-11-25 | Tạo được 1 file giọng 10 giây bằng gemini_tts; test pytest đạt |  |
| T-004 | Chưa làm | claude | Render thử 3 phút bằng HyperFrames để đo thời gian render trên cloud | render |  | 2026-11-30 | MP4 3 phút + render/RENDERED.txt ghi thời gian render, máy, dung lượng |  |
| T-005 | Chưa làm | claude | Viết và dựng 10 Shorts đầu (đăng 01–10/12) theo KE_HOACH_90_NGAY §3 | shorts |  | 2026-11-30 | 10 thư mục shorts/SNN-slug có kịch bản QA đạt, MP4, package/ có publish_at.txt |  |
| T-032 | Chưa làm | claude-local | Bật AI tự tải lên: đặt YT_AUDIT_APPROVED=1 trong OpenMontage/.env (thử thật T-028/T-030 đạt), tải thật Short đầu tiên bằng yt_publish.py upload với hẹn giờ 01/12, theo dõi 24 giờ; bị khóa thì anh kéo thả | publish |  | 2026-11-30 | UPLOADED.txt của Short đầu ghi video_id + publishAt; sau giờ hẹn đọc lại privacyStatus=public; ghi kết quả vào TU_DONG_DANG_VIDEO.md §5 |  |
| T-006 | Chưa làm | claude | Thử yt_publish.py với Short đầu tiên anh tải lên (đặt publishAt qua API) | publish |  | 2026-12-01 | package/UPLOADED.txt ghi kết quả; ghi vào HANDOFF API có cho hẹn giờ hay không |  |
| T-007 | Chưa làm | claude | Chạy lại radar sau 24–48 giờ để kiểm chứng đà tăng của ứng viên (I-001) | research |  | 2026-11-24 | RADAR.md mới + so lượt xem 2 thời điểm cho 3 ứng viên trong IDEA_BANK |  |
| T-042 | Chưa làm | claude | 002 Lady Be Good: phụ đề 10 ngôn ngữ (dịch en.srt, giữ mốc giờ) rồi đưa lên video RHKCFi3l2V0 | package | 002-lady-be-good | 2026-11-26 | package/subtitles có 10 file SRT (vi es pt-BR hi id fr de ja ko ar) cùng số cue với en.srt; yt_publish.py apply ghi đủ; captions.list đọc lại 11 ngôn ngữ |  |
| T-012 | Chưa làm | claude | Cấu hình Google Drive (GDRIVE_REFRESH_TOKEN) để chuyển file MP4 cho anh | ops |  | 2026-12-05 | check_apis.py báo Drive OK; tải thử 1 file lên thư mục ICYFOX |  |
| T-009 | Chưa làm | claude | Viết Phần 3 kịch bản 001 Gilgamesh (chương 5–7) | script | 001-gilgamesh-lost-lines | 2026-12-14 | script_part3.md QA ĐẠT (qa_check.py --mark) |  |
| T-010 | Chưa làm | claude | Viết Phần 4 kịch bản 001 Gilgamesh (chương 8–9) | script | 001-gilgamesh-lost-lines | 2026-12-16 | script_part4.md QA ĐẠT (qa_check.py --mark) |  |
| T-008 | Chưa làm | claude | Kiểm S3.5, S4.1, S4.6 của 001 bằng bản dịch Thompson 1928 (cần host archive.org) | research | 001-gilgamesh-lost-lines |  | Ghi kết quả kiểm + link nguồn vào script_part2.md mục Cần kiểm |  |
| T-011 | Chưa làm | claude | Lấy lại phụ đề video QkRRERFPfEM (lần trước lỗi 429) | research |  |  | File phụ đề trong research/2026-11-22-wartimestories/subs/ |  |

## Xong gần đây

- T-041 002 Lady Be Good: tải lên qua API + công khai ngay 23/11 (anh yêu cầu không hẹn giờ) (2026-11-23 12:44): channel-studio/videos/002-lady-be-good/package/UPLOADED.txt, channel-studio/videos/002-lady-be-good/package/READBACK.txt
- T-025 002 Lady Be Good: lời đọc cả video bằng giọng Algenib (anh chốt 22/11) (2026-11-23 12:39): channel-studio/videos/002-lady-be-good/voice/narration_report_clone.md, projects/lady-be-good/assets/audio/narration_clone/S0.1.wav
- T-039 002 Lady Be Good: dựng HyperFrames + render MP4 30 phút (2026-11-23 12:39): channel-studio/videos/002-lady-be-good/render/renders/lady-be-good.mp4, channel-studio/videos/002-lady-be-good/render/RENDERED.txt
- T-040 002 Lady Be Good: gói đăng (tiêu đề, mô tả có nguồn + ghi công, thumbnail, phụ đề EN, bản dịch tiêu đề/mô tả 10 ngôn ngữ) (2026-11-23 12:39): channel-studio/videos/002-lady-be-good/package/title.txt, channel-studio/videos/002-lady-be-good/package/description.md, channel-studio/videos/002-lady-be-good/package/tags.txt, channel-studio/videos/002-lady-be-good/package/thumbnail.jpg, channel-studio/videos/002-lady-be-good/package/subtitles/en.srt, channel-studio/videos/002-lady-be-good/package/i18n.json
- T-035 Cài VoiceStudio + OmniVoice trên máy anh, clone giọng Algenib (2026-11-23 11:20): voice-lab/README.md, voice-lab/clone-algenib/clone_algenib.py, voice-lab/clone-algenib/S1.3_clone_voxcpm2.mp3, .gitmodules, channel-studio/state/jobs/2026-11-23-clone-algenib-qa.log
- T-034 Cho AI tự chạy không cần anh nhắc: phiên cloud dự phòng khi máy anh tắt + tự chạy tiếp khi hết hạn mức + danh sách việc anh làm 1 lần (2026-11-23 11:05): .claude/skills/hoang-dung-clay-lapis-studio/scripts/autopilot.py, .claude/skills/hoang-dung-clay-lapis-studio/references/autopilot.md, .claude/skills/hoang-dung-clay-lapis-studio/references/decisions-log.md
- T-036 Tìm chủ đề đang lên liên quan kênh (radar lần 2 + kiểm chứng 2 thời điểm + cụm chủ đề), đưa vào kho ý tưởng (2026-11-23 11:05): channel-studio/research/2026-11-23-trend/DE_XUAT_CHU_DE.md, channel-studio/research/2026-11-23-trend/trend_rows.json, channel-studio/research/2026-11-23-radar/RADAR.md, channel-studio/ideas/IDEA_BANK.md
- T-037 Script giọng VoiceStudio (voicestudio_tts.py) + chặn engine không thương mại (2026-11-23 11:05): .claude/skills/hoang-dung-clay-lapis-studio/scripts/voice/voicestudio_tts.py, .claude/skills/hoang-dung-clay-lapis-studio/scripts/tests/test_icyfox_tools.py
- T-033 Sao chép repo OmniVoice + VoiceStudio vào phiên và ghi vào bản đồ repo (2026-11-23 00:04): .claude/skills/hoang-dung-clay-lapis-studio/references/toolbox-repos.md, /home/user/hoangdung68789/voicestudio/README.md, /home/user/hoangdung68789/omnivoice/README.md
- T-030 Thử hẹn giờ công khai sau 3 phút qua API (anh yêu cầu), xem có tự chuyển Công khai không, rồi xóa (2026-11-23 00:00): channel-studio/research/2026-11-22-api-upload-test/result.json, channel-studio/guides/TU_DONG_DANG_VIDEO.md, .claude/skills/hoang-dung-clay-lapis-studio/scripts/yt_upload_probe.py
- T-028 Thử tải 1 clip 5 giây qua API (Không công khai) để biết YouTube có còn ép Riêng tư không, rồi xóa clip (2026-11-22 23:53): channel-studio/research/2026-11-22-api-upload-test/result.json, .claude/skills/hoang-dung-clay-lapis-studio/scripts/yt_upload_probe.py, channel-studio/guides/TU_DONG_DANG_VIDEO.md
- T-027 Trả lời: có cách nào để AI tự đăng video lên YouTube không (kiểm chính sách + phương án) (2026-11-22 23:49): channel-studio/guides/TU_DONG_DANG_VIDEO.md
- T-026 Tự động tải video lên YouTube: lệnh upload trong yt_publish.py + hồ sơ đơn audit API (2026-11-22 23:22): channel-studio/PLAN.md
- T-019 002 Lady Be Good: viết Phần 2–4, mỗi phần qa_check ĐẠT; gộp duyệt cả kịch bản 1 lần trong lô duyệt tuần (2026-11-22 22:21): channel-studio/videos/002-lady-be-good/script_part1.md, channel-studio/videos/002-lady-be-good/script_part2.md, channel-studio/videos/002-lady-be-good/script_part3.md, channel-studio/videos/002-lady-be-good/script_part4.md, channel-studio/videos/002-lady-be-good/script_full_ready.txt, channel-studio/videos/002-lady-be-good/script_part1.qa.md, channel-studio/videos/002-lady-be-good/script_part2.qa.md, channel-studio/videos/002-lady-be-good/script_part3.qa.md, channel-studio/videos/002-lady-be-good/script_part4.qa.md
- T-024 Hướng dẫn + script khôi phục toàn bộ dữ liệu ICYFOX khi đổi máy tính (2026-11-22 22:03): channel-studio/guides/KHOI_PHUC_MAY_MOI.md, .claude/skills/hoang-dung-clay-lapis-studio/scripts/restore_machine.sh
