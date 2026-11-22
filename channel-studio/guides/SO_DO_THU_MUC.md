# Sơ đồ thư mục ICYFOX trên máy anh (tra 22/11/2026)

Đường dẫn gốc: `C:\Users\Admin\HDRE AI\ClayLapis\OpenMontage\`
Chuẩn đối chiếu: `.claude/skills/hoang-dung-clay-lapis-studio/references/workspace-structure.md`
Kết quả: **có 22/23 thư mục chuẩn**. Chỉ thiếu `shorts/`, sẽ được tạo khi làm Shorts (thẻ T-005).

## 1. Toàn cảnh

```
OpenMontage/
├── .env                          ← khóa API (6/7 khóa, thiếu GDRIVE_REFRESH_TOKEN, thẻ T-012). KHÔNG lên git
├── .claude/
│   ├── settings.json             ← 3 hook nhắc việc (đầu phiên, mỗi lượt, cuối lượt)
│   └── skills/hoang-dung-clay-lapis-studio/
│       ├── SKILL.md              ← bộ luật vận hành kênh
│       ├── references/           ← quy trình: autopilot, work-contract, read-map, workspace-structure…
│       └── scripts/              ← tasks.py, autopilot.py, session_start.sh, session_end.py,
│                                   qa_check.py, yt_publish.py, research/ (radar, báo cáo), hooks/, tests/
├── projects/                     ← hồ sơ dự án OpenMontage đang dùng (KHÔNG lên git; chép qua lại với channel-studio/projects/)
│   ├── gilgamesh-pilot/
│   └── lady-be-good/
└── channel-studio/               ← mọi tài liệu kênh (lên GitHub cuối mỗi phiên). Chi tiết ở mục 2
```

## 2. Thư mục `channel-studio/`

```
channel-studio/
├── MISSION.md        ✅ mục tiêu vĩnh viễn (chỉ anh sửa)
├── PLAN.md           ✅ kế hoạch hiện hành, lịch đăng
├── HANDOFF.md        ✅ trạng thái mới nhất, đọc đầu phiên
├── TASKS.md          ✅ sổ việc (tự sinh)
├── README.md         ✅ bản đồ ngắn
│
├── state/            ✅ tasks.json: dữ liệu sổ việc
├── logs/             ✅ 2026-11.md: nhật ký hoàn thành từng việc
├── ideas/            ✅ IDEA_BANK.md: 8 ý tưởng Sẵn sàng
│
├── analytics/        ✅ số liệu kênh
│   ├── reports/2026-11-22/   report.md + data.json
│   ├── WINNERS.md            video thắng, quy luật
│   └── video_map.json        YouTube ID → video
│
├── series/           ✅ SERIES_INDEX.md
├── channel/          ✅ channel_setup.md, automation_plan.md
├── config/           ✅ mẫu khóa API + hướng dẫn
├── guides/           ✅ hướng dẫn cho anh (có file này)
│
├── research/         ✅ nghiên cứu (27 file)
│   ├── 2026-11-22-radar/            radar xu hướng lần 1
│   ├── 2026-11-22-ideas/            bằng chứng 7 ý tưởng mới
│   ├── 2026-11-22-story-niches/     quét 12 nhóm chủ đề
│   ├── 2026-11-22-wartimestories/   phân tích đối thủ + KẾ HOẠCH 90 NGÀY
│   ├── deep_scan/, niche_scan/
│   └── competitor_thumbnails_grid.jpg
│
├── projects/         ✅ bản sao hồ sơ OpenMontage (gilgamesh-pilot, lady-be-good)
│
├── videos/           ✅ mỗi video dài một thư mục NNN-slug
│   ├── 001-gilgamesh-lost-lines/    đăng 25/12 · P5
│   │   ├── README.md, proposal.md
│   │   ├── script_part1.md          (chờ duyệt)
│   │   ├── script_part2.md + .qa.md (ĐÃ DUYỆT)
│   │   └── package/
│   └── 002-lady-be-good/            đăng 11/12 · P2+P3
│       ├── README.md, script_outline.md
│       ├── script_part1..4.md + .qa.md
│       ├── script_full_ready.txt    kịch bản đủ 4 phần
│       └── voice/                   lời đọc (đang làm, T-025)
│
└── shorts/           ⏳ CHƯA CÓ: tạo khi làm 10 Shorts đầu (T-005, hạn 30/11)
```

## 3. Một thư mục video khi làm xong sẽ có

```
videos/NNN-slug/
├── README.md              trạng thái, trụ cột, link Notion
├── script_outline.md      dàn ý + hook
├── script_partN.md        kịch bản từng phần (+ .qa.md tự kiểm)
├── script_full_ready.txt  đánh dấu đủ các phần
├── voice/                 ghi chú giọng (file âm thanh không lên git)
├── shorts/                Shorts cắt từ video này
├── render/                dự án HyperFrames + RENDERED.txt
└── package/               title.txt, description.md, tags.txt, thumbnail.png,
                           subtitles/*.srt, i18n.json, publish_at.txt, UPLOADED.txt
```

Ký hiệu: ✅ đã có · ⏳ chưa có, sẽ tạo ở bước sau.
File MP4 và WAV dài không nằm trên git. Chúng ở `OpenMontage/projects/<id>/` hoặc Google Drive (khi xong T-012).
