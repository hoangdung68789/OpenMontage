# Sơ đồ thư mục ICYFOX trên máy anh (bản đầy đủ, tra 22/11/2026 tối, cập nhật 23:59)

- Đường dẫn gốc: `C:\Users\Admin\HDRE AI\ClayLapis\OpenMontage\`
- Chuẩn đối chiếu: `.claude/skills/hoang-dung-clay-lapis-studio/references/workspace-structure.md`
- Kết quả: **có 22/23 thư mục chuẩn**. Thiếu `channel-studio/shorts/`, sẽ tạo ở T-005.
- **6 vấn đề ở mục 6: đã xử lý xong 5, mục 6.5 giữ nguyên có lý do.** Đã bổ sung giám sát tác vụ (mục 7).

Ký hiệu: ✅ có · ⏳ chưa có, sẽ tạo ở bước sau · ⚠️ có vấn đề (mục 6) · 🔒 không lên git

---

## 1. Ba nơi lưu trên máy anh

```
C:\Users\Admin\
├── .claude\scheduled-tasks\              ← tác vụ hẹn giờ của app Claude (ngoài repo)
│   ├── icyfox-san-xuat-9h-17h\SKILL.md       09:00 + 17:00 mỗi ngày, chế độ tự lái
│   └── icyfox-bao-cao-tuan-cn-9h\SKILL.md    Chủ nhật 09:00, báo cáo số liệu
│
└── HDRE AI\ClayLapis\OpenMontage\        ← repo GitHub hoangdung68789/OpenMontage, nhánh ccr-6640cec8-2anthl
    ├── .env                         🔒 khóa API: 6/7 khóa (thiếu GDRIVE_REFRESH_TOKEN, thẻ T-012)
    ├── .claude\                     ← bộ não ICYFOX (mục 2)
    ├── channel-studio\              ← toàn bộ tài liệu kênh, 32 MB (mục 3)
    ├── projects\                    🔒 hồ sơ dự án OpenMontage đang dùng (mục 5)
    ├── pipeline_defs\icyfox-autopilot.yaml   quy trình tự lái dạng OpenMontage
    └── (phần mềm OpenMontage: tools\, lib\, skills\, schemas\, remotion-composer\,
         backlot\, ink-theater\, styles\, tests\, docs\, AGENT_GUIDE.md, CLAUDE.md…)
```

## 2. `.claude\`: skill, hook, lệnh

```
.claude\
├── settings.json                 ✅ 3 hook: đầu phiên, mỗi lượt, cuối lượt (đã chạy thật)
├── .icyfox_session               🔒 dấu phiên của hook
├── launch.json, commands\        (lệnh chung của OpenMontage)
└── skills\hoang-dung-clay-lapis-studio\
    ├── SKILL.md                  bộ luật vận hành kênh
    ├── references\  (19 file)    quy trình (mới: fallbacks.md = bảng phương án thay thế F0–F10)
    │   ├── work-contract.md      hợp đồng làm việc, quy tắc báo "xong"
    │   ├── read-map.md           việc nào đọc file nào, dùng công cụ nào
    │   ├── autopilot.md          chế độ tự lái (anh giao toàn quyền 22/11)
    │   ├── workspace-structure.md  chuẩn thư mục (file đối chiếu của sơ đồ này)
    │   ├── analytics-loop.md     từ số liệu ra ý tưởng, chấm điểm
    │   ├── content-pillars.md    5 trụ cột P1–P5
    │   ├── production-workflow.md, publish-package.md, series-playbook.md
    │   ├── research-playbook.md, request-playbooks.md, policy-guardrails.md
    │   ├── decisions-log.md, multi-agent.md, automation.md
    │   └── environment-and-apis.md, local-render.md, toolbox-repos.md
    ├── templates\  (4 file)      mẫu HANDOFF, README video, phần kịch bản, lời mở phiên
    └── scripts\
        ├── session_start.sh, session_end.py   mở và đóng phiên (đồng bộ projects, đẩy GitHub)
        ├── tasks.py              sổ việc + kiểm "xong"
        ├── autopilot.py          lập chương trình làm việc mỗi phiên
        ├── qa_check.py           tự kiểm kịch bản (đếm từ, nguồn)
        ├── yt_publish.py         áp gói đăng, hẹn giờ
        ├── series.py, check_apis.py, yt_authorize_desktop.py
        ├── restore_machine.sh, icyfox_common.py
        ├── hooks\                run.sh, pulse.py
        ├── research\  (8 file)   niche_outliers.py (radar), yt_analytics_report.py (báo cáo),
        │                         story_scan.py, niche_scan.py, deep_scan.py, deep_analyze.py,
        │                         summarize.py, yt_api_channel.py
        ├── watchdog.py           giám sát: thẻ treo, quá hạn, lỗi log tác vụ nền (mới 22/11)
        └── tests\test_icyfox_tools.py   9/9 đạt
```

## 3. `channel-studio\`: tài liệu kênh (lên GitHub)

```
channel-studio\
├── MISSION.md        ✅ mục tiêu vĩnh viễn (chỉ anh sửa)
├── PLAN.md           ✅ kế hoạch, lịch đăng (khối releases)
├── HANDOFF.md        ✅ trạng thái mới nhất
├── TASKS.md          ✅ sổ việc (tự sinh từ state\tasks.json)
├── README.md         ✅ bản đồ ngắn
│
├── state\tasks.json              ✅ dữ liệu sổ việc
├── state\jobs\*.log              ✅ log tác vụ nền (watchdog.py soát lỗi), mới 22/11
├── logs\2026-11.md               ✅ nhật ký hoàn thành từng việc
├── ideas\IDEA_BANK.md            ✅ 8 ý tưởng Sẵn sàng
│
├── analytics\                    ✅
│   ├── reports\2026-11-22\       report.md, data.json
│   ├── WINNERS.md                video thắng, quy luật
│   └── video_map.json            YouTube ID → video
│
├── series\SERIES_INDEX.md        ✅ (chưa có series nào) ⚠️ mục 6.3
├── channel\                      ✅ channel_setup.md, automation_plan.md
├── config\                       ✅ api_keys.env.example, HUONG_DAN_KHOA_API.md
├── guides\                       ✅ file này + KHOI_PHUC_MAY_MOI.md, local_setup.md,
│                                    PROMPT_CAP_NHAT_MAY_TINH.md, hướng dẫn .env và Gemini (html/png)
│
├── research\                     ✅
│   ├── 2026-11-22-radar\              RADAR.md, outliers.json (radar lần 1, 21:17)
│   ├── 2026-11-22-ideas\              evidence.json (bằng chứng I-004..I-010)
│   ├── 2026-11-22-story-niches\       story_scan.json, summary.md, Yesterday_api.*
│   ├── 2026-11-22-wartimestories\     13 mục: BAO_CAO.md, KE_HOACH_90_NGAY.md, api, phụ đề, bình luận
│   ├── deep_scan\deep.json            ⚠️ mục 6.5 (tên thiếu ngày)
│   ├── niche_scan\                    channels.json, search.json ⚠️ mục 6.5
│   └── competitor_thumbnails_grid.jpg
│
├── projects\                     ✅ bản sao hồ sơ OpenMontage (mục 5) ⚠️ mục 6.1
│   ├── gilgamesh-pilot\
│   └── lady-be-good\
│
├── videos\                       ✅ (mục 4)
│   ├── 001-gilgamesh-lost-lines\
│   └── 002-lady-be-good\
│
└── shorts\                       ⏳ chưa có: tạo khi làm 10 Shorts đầu (T-005, hạn 30/11)
```

## 4. Thư mục video

```
videos\
├── 001-gilgamesh-lost-lines\     đăng 25/12 · P5 · project gilgamesh-pilot
│   ├── README.md, proposal.md    (proposal.md thay cho script_outline.md, autopilot chấp nhận)
│   ├── script_part1.md           chờ duyệt, chưa có .qa.md ⚠️ mục 6.4
│   ├── script_part2.md + .qa.md  ĐÃ DUYỆT 22/11
│   ├── script_part3.md, part4    ⏳ chưa viết (T-009, T-010)
│   └── package\                  chỉ có .gitkeep (chưa tới bước gói đăng)
│
└── 002-lady-be-good\             đăng 11/12 · P2+P3 · project lady-be-good
    ├── README.md, script_outline.md
    ├── script_part1..4.md + .qa.md   QA ĐẠT cả 4 phần, ĐÃ DUYỆT 22/11/2026
    ├── script_full_ready.txt     đủ 4 phần
    ├── yt_search_2026-11-22.json
    ├── voice\                    T-025: alt_voice.py (model 3.1, công cụ hiện hành), narrate.py (3.8, cũ), check_voice.py,
    │                             narration_report.py, voice_samples.py, check_voice.jsonl, prompt_S5.5.txt
    ├── shorts\, render\          ⏳ bước sau
    └── package\                  ⏳ bước sau
```

Một thư mục video khi làm xong sẽ có:
```
README.md · script_outline.md · script_partN.md (+ .qa.md) · script_full_ready.txt
voice\ · shorts\ · render\ (RENDERED.txt) · package\ (title.txt, description.md, tags.txt,
thumbnail.png, subtitles\*.srt, i18n.json, publish_at.txt, UPLOADED.txt)
```

## 5. Hồ sơ dự án OpenMontage: hai bản đồng bộ

```
OpenMontage\projects\<id>\  🔒 (bản đang làm)  ── session_end.py chép sang ──▶  channel-studio\projects\<id>\  (lên git)
                                                ◀── session_start.sh chép về ──
Bỏ qua khi chép: assets\video\, renders\, file .wav (từ 22/11, file trên máy giữ nguyên), file > 20 MB.

gilgamesh-pilot\   573 KB   project.json, checkpoint_research/proposal, decision_log, events.jsonl,
                            artifacts\ (research_brief, proposal_packet, decision_log), assets\audio\samples\
lady-be-good\      27 MB    project.json, checkpoint_research/proposal/script,
                            artifacts\ (research_brief, proposal_packet, script.json),
                            assets\audio\narration_g31\ (10/31 WAV model 3.1, đang làm, WAV 🔒) + narration\ (8 đoạn 3.8, chỉ tham khảo) + voice_samples\,
                            assets\images\, music\, video\ 🔒, renders\ 🔒
```

## 6. Vấn đề phát hiện và cách đã xử lý (cập nhật 22/11/2026 23:59)

| # | Mức | Vấn đề | Bằng chứng | Đã xử lý |
|---|---|---|---|---|
| 6.1 | **Cao** | **File âm thanh đang lên git, trái luật "WAV dài không lên git".** Đã có 17 file (8 WAV lời đọc + mẫu giọng), khoảng 28 MB. Khi đủ 31 đoạn lời đọc, git sẽ có thêm khoảng 40 MB nữa, và mỗi lần đọc lại một đoạn lại thêm một bản mới. Repo phình to mãi | `git ls-files` trong `channel-studio/projects/lady-be-good/assets/audio/`; `session_end.py` chỉ bỏ qua `video`, `renders` và file > 20 MB | **ĐÃ XỬ LÝ:** `session_end.py` bỏ .wav khi chép và gỡ .wav khỏi git (`git rm --cached`), file trên máy giữ nguyên; bản .mp3 mẫu vẫn lên. Không viết lại lịch sử. Sao lưu WAV lên Drive ở T-012 |
| 6.2 | Thấp | Dòng đầu 4 phần kịch bản 002 vẫn ghi "chờ duyệt", trong khi HANDOFF ghi anh đã duyệt cả kịch bản ngày 22/11 | dòng 1 các file `script_part1..4.md`; HANDOFF dòng 63, 75 | **ĐÃ XỬ LÝ:** dòng đầu 4 phần ghi "ĐÃ DUYỆT 22/11/2026" |
| 6.3 | Thấp | README video 002 và ý tưởng I-001, I-006 ghi series "Documented", nhưng chưa có series nào được đăng ký | `series/SERIES_INDEX.md`: "(chưa có series)" | **ĐÃ XỬ LÝ:** AI chốt "Documented" là nhãn phong cách, không phải series nhiều tập; ghi `decisions-log.md`, README 002, IDEA_BANK |
| 6.4 | Thấp | 001 Phần 1 "chờ duyệt", chưa có báo cáo `.qa.md`; Phần 3–4 chưa viết. Dòng Notion 001 chưa đổi sang ngày 25/12 | dòng 1 `script_part1.md`; HANDOFF dòng 87 | **ĐÃ XỬ LÝ:** `qa_check.py` Phần 1 → QA ĐẠT (786 từ, nguồn 10/12 đoạn, trùng đối thủ 0%), dòng đầu ghi AI TỰ DUYỆT 22/11/2026. Dòng Notion 001 đã đổi sang 25/12 |
| 6.6 | Trung bình | `PLAN.md` vẫn ghi "thứ Năm gửi anh LÔ DUYỆT TUẦN" và "ghi rõ trong lô duyệt tuần", trái với MISSION và HANDOFF (anh giao toàn quyền 22/11, bỏ lô duyệt tuần). Tự lái đọc PLAN có thể vẫn chờ anh duyệt | `PLAN.md` dòng 10, 49; `MISSION.md` dòng 14 | **ĐÃ XỬ LÝ:** PLAN dòng 10 đã theo MISSION; bỏ chữ "lô duyệt tuần" còn sót ở autopilot.py, qa_check.py, read-map, analytics-loop, series-playbook |
| 6.5 | Thấp | `research/deep_scan/`, `niche_scan/` và ảnh `competitor_thumbnails_grid.jpg` không theo quy ước tên `<ngày>-<việc>` | ls `research/` | **GIỮ NGUYÊN:** các script quét đang ghi vào đúng các đường dẫn này; đổi tên làm hỏng script mà không được lợi gì |

Đã kiểm và **không có vấn đề**: `.env`, `.icyfox_session` và `OpenMontage/projects/` được git bỏ qua đúng; không có file nào trên 5 MB trên git; hook chạy; test 8/8; 2 tác vụ hẹn giờ có lời nhắn mới.

## 7. Giám sát tác vụ (anh yêu cầu 22/11/2026: "tự động giám sát tác vụ, bắt lỗi và tìm phương pháp thay thế")

| Thành phần | Ở đâu | Làm gì |
|---|---|---|
| Log tác vụ nền | `channel-studio/state/jobs/<ngày>-<việc>.log` | Mọi tác vụ chạy lâu ghi log ở đây |
| Bộ dò | `.claude/skills/hoang-dung-clay-lapis-studio/scripts/watchdog.py` | Thẻ "đang làm" quá 6 giờ không cập nhật, thẻ quá hạn, thẻ bị chặn, lỗi ở đuôi log (11 mẫu lỗi F0–F10) |
| Bảng phương án thay thế | `references/fallbacks.md` | Mỗi lỗi: dấu hiệu, cách thay thế, điều không được làm |
| Gắn vào tự lái | `autopilot.py` + tác vụ hẹn giờ 09:00/17:00 | Kết quả watchdog lên đầu chương trình làm việc; phiên tự lái xử lý mục "Giám sát" trước |
| Kiểm thử | `scripts/tests/test_icyfox_tools.py` | 9/9 đạt, gồm bài thử thẻ treo, quá hạn, lỗi F1 và F10 |

Lần chạy thật đầu tiên (22/11 23:50–23:59): bắt được lỗi 429 của lời đọc 002 ở S3.3. Gọi thử thấy trả 200, nên xếp là giới hạn theo phút (F10) và chạy tiếp. Lần sau API báo `PerDay` (F1): script tự dừng đúng, không thử lại vô ích; chạy lại sau 15:00 ngày 23/11.

