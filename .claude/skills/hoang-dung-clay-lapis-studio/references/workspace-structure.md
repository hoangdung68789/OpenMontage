# Cấu trúc thư mục và quy ước

## Nơi lưu trữ
| Loại | Nơi lưu | Ghi chú |
|---|---|---|
| Tài liệu, kịch bản, hồ sơ dự án, số liệu nghiên cứu | GitHub `hoangdung68789/OpenMontage`, nhánh `ccr-6640cec8-2anthl`, thư mục `channel-studio/` | Bền. Đẩy lên cuối mỗi phiên |
| Skill này | Cùng repo và nhánh: `.claude/skills/hoang-dung-clay-lapis-studio/`. Có thể cài thêm ở cấp tài khoản claude.ai (file `.skill`) | Sửa skill thì sửa ở repo, rồi đóng gói lại |
| Trạng thái từng video | Notion "Clay & Lapis – Video Pipeline" | Anh xem được trên điện thoại |
| File lớn (MP4, WAV dài) | Google Drive (biến `GDRIVE_REFRESH_TOKEN`, xin quyền riêng) hoặc tạm trong container | **Không đưa lên git.** GitHub chặn file trên 100 MB, và repo sẽ phình to |
| Khóa và token | Cài đặt môi trường `video-channel-studio` | Không bao giờ nằm trong file |

## Cây thư mục `channel-studio/`
```
channel-studio/
├── MISSION.md                 # MỤC TIÊU VĨNH VIỄN: đọc đầu tiên. Chỉ anh sửa
├── PLAN.md                    # kế hoạch hiện hành; khối phases + releases (autopilot.py đọc)
├── HANDOFF.md                 # trạng thái mới nhất: đọc đầu phiên, cập nhật cuối phiên
├── TASKS.md                   # sổ việc (tự sinh, đừng sửa tay)
├── README.md                  # bản đồ ngắn
├── state/
│   └── tasks.json             # dữ liệu sổ việc (scripts/tasks.py quản lý)
├── logs/
│   └── YYYY-MM.md             # NHẬT KÝ LỊCH SỬ: báo cáo hoàn thành từng việc (tasks.py ghi, chỉ thêm)
├── ideas/
│   └── IDEA_BANK.md           # kho ý tưởng có bằng chứng + điểm
├── analytics/
│   ├── reports/YYYY-MM-DD/    # report.md + data.json (yt_analytics_report.py)
│   ├── WINNERS.md             # video thắng và quy luật rút ra
│   └── video_map.json         # YouTube ID → thư mục video, trụ cột, series, tập, kiểu hook
├── series/
│   ├── SERIES_INDEX.md        # mọi series, tập kế tiếp, tập cuối (tự sinh)
│   └── <series-id>/           # series.json (nguồn) + SERIES.md (tự sinh)
├── channel/
│   ├── channel_setup.md       # tên kênh, About, từ khóa, danh sách phát, cài đặt tải lên, checklist YPP, lịch đăng
│   └── automation_plan.md     # kế hoạch tự động hóa
├── motion-kit/                # BỘ CHUYỂN ĐỘNG: icyfox_motion.py (validate/build), vendor/gsap, demo/ (lưới khung + số đo)
├── videos/
│   └── NNN-slug/              # mỗi video dài một thư mục, ví dụ 002-lady-be-good
│       ├── README.md          # trạng thái, trụ cột (P1–P5), series/tập nếu có, link Notion
│       ├── script_outline.md  # dàn ý + hook (dòng đầu ghi ĐÃ DUYỆT <ngày> khi anh duyệt lô tuần)
│       ├── script_partN.md    # kịch bản theo phần; dòng đầu có "QA ĐẠT <ngày>" khi qa_check.py đạt
│       ├── script_partN.qa.md # báo cáo tự kiểm
│       ├── script_full_ready.txt # đánh dấu kịch bản đủ các phần (autopilot đọc)
│       ├── voice/             # ghi chú giọng (file âm thanh không lên git)
│       ├── shorts/            # Shorts cắt từ video này: SNN-slug.md (+ .mp4 không lên git)
│       ├── render/motion_plan.json # kế hoạch chuyển động từng cảnh (icyfox_motion.py validate)
│       ├── render/            # dự án HyperFrames + RENDERED.txt (đường dẫn MP4, dung lượng, thời gian render)
│       └── package/           # title.txt, description.md, tags.txt, category.txt, thumbnail.png (< 2 MB),
│                              # subtitles/<mã ngôn ngữ>.srt, i18n.json, publish_at.txt, UPLOADED.txt (yt_publish.py ghi)
├── shorts/
│   └── SNN-slug/              # Shorts độc lập (giai đoạn 1): kịch bản + package/ như trên
├── projects/                  # bản sao của OpenMontage projects/<project-id>/ (checkpoint, artifacts)
├── research/                  # quét ngách, đối thủ, radar xu hướng (<ngày>-radar/RADAR.md)
├── config/                    # mẫu khóa API + hướng dẫn
└── guides/                    # ảnh và hướng dẫn cho anh
```

**Tên file MP4 khi render = mã gói** (ví dụ `002-lady-be-good.mp4`, `S03-foo-fighters-name.mp4`). Anh kéo thả lên Studio, YouTube lấy tên file làm tiêu đề, `yt_publish.py` dựa vào đó để nhận ra video.

## Quy ước
- **Tên thư mục video:** `NNN-slug`, đánh số tăng dần, slug tiếng Anh viết thường có gạch nối. **Project ID của OpenMontage** dùng slug ngắn, ví dụ `gilgamesh-pilot`. Ghi cặp tên này trong README của video.
- **Kịch bản:** mỗi phần khoảng 1.000–1.300 từ (8–10 phút đọc). Đầu file ghi trạng thái: `chờ duyệt` hoặc `ĐÃ DUYỆT <ngày>`.
- **Hồ sơ dự án:** OpenMontage bắt buộc artifacts nằm ở `OpenMontage/projects/<id>/`, nhưng thư mục này bị gitignore. Đầu phiên `session_start.sh` chép từ `channel-studio/projects/` về. Cuối phiên `session_end.py` chép ngược lại, bỏ qua `assets/video`, `renders/` và file trên 20 MB.
- **Khi `git add` thư mục `channel-studio/projects/`** phải dùng `-f`, vì `.gitignore` có dòng `projects/` khớp với mọi thư mục tên `projects`. Script đã xử lý việc này.

## Bảng Notion: các cột
Video (tiêu đề) · Status (Ý tưởng → Nghiên cứu → Viết kịch bản → Chờ duyệt → Đang dựng → Chờ đăng → Đã lên lịch → Đã đăng) · Loại (Video dài / Short) · Chủ đề · Thời lượng (phút) · Ngày đăng · Link YouTube · Link Drive · Việc cần anh làm · Chi phí (USD) · Giờ xem 7 ngày · Sub mới 7 ngày · Mã (CLAY-VID-n).
Khi tạo dòng mới: dùng `notion-create-pages` với `parent.data_source_id = 4201dcd7-7c95-8188-8452-000b17602005`.
