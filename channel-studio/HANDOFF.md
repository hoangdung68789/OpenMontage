# ICYFOX (dự án Clay & Lapis): ghi chú bàn giao (cập nhật 22/11/2026)

**Đọc trước: `MISSION.md` (mục tiêu vĩnh viễn) → `PLAN.md` (kế hoạch) → file này → `TASKS.md` (sổ việc) → `references/work-contract.md` (hợp đồng làm việc).** Việc hôm nay: `python3 .claude/skills/hoang-dung-clay-lapis-studio/scripts/autopilot.py`.

Đọc file này trước khi làm tiếp. Quy trình đầy đủ nằm trong skill `hoang-dung-clay-lapis-studio` (`.claude/skills/hoang-dung-clay-lapis-studio/SKILL.md`). **Đọc mục 0 "Tiêu chuẩn làm việc" trước.** Mở phiên bằng `bash .claude/skills/hoang-dung-clay-lapis-studio/scripts/session_start.sh`.

## MỚI NHẤT
- **22/11/2026 23:59: thử hẹn giờ công khai qua API ĐẠT** (T-030). Clip tự chuyển Công khai đúng giờ hẹn, đã xóa. Việc tiếp theo là **T-032**: bật `YT_AUDIT_APPROVED=1` trong `.env` trên máy anh rồi tải thật Short đầu tiên. Chi tiết: `guides/TU_DONG_DANG_VIDEO.md` §4b.

## HỆ THỐNG MỚI (22/11/2026, tối): tự lái, sổ việc có kiểm chứng, chống quên
- **Mục tiêu vĩnh viễn:** `channel-studio/MISSION.md`. **Kế hoạch:** `channel-studio/PLAN.md` (khối phases và releases).
- **Hợp đồng làm việc + QUY TẮC HOÀN THÀNH:** `references/work-contract.md`.
  - Mỗi việc là một thẻ `scripts/tasks.py`.
  - Chỉ báo xong khi `tasks.py done` chấp nhận: kiểm chứng thật, báo cáo từng thành phần, ghi nhật ký `channel-studio/logs/<tháng>.md`.
- **Hook** trong `OpenMontage/.claude/settings.json` chỉ chạy khi mở Claude Code trong thư mục OpenMontage (máy anh):
  - SessionStart in mục tiêu, kế hoạch, việc hôm nay.
  - UserPromptSubmit nhắc mỗi lượt.
  - Stop chặn khi còn việc dở, chưa lưu, hoặc báo "xong" sai.
  - Phiên cloud không có hook: `session_start.sh` in nội dung tương đương.
- **Bản đồ đọc file:** `references/read-map.md`. **Series:** `references/series-playbook.md` + `scripts/series.py`.
- **Tự lái:** `references/autopilot.md` + `scripts/autopilot.py` + pipeline `icyfox-autopilot`. **Anh giao toàn quyền 22/11/2026:** AI tự quản lý kênh tới bật và giữ kiếm tiền, không còn lô duyệt tuần, không hỏi lại việc đã chốt. Anh chỉ xem báo cáo Chủ nhật (số liệu + doanh thu), kéo thả MP4 lên Studio, làm việc tài khoản và chi tiền ngoài ngân sách.
- **Số liệu:**
  - Radar xu hướng `scripts/research/niche_outliers.py`. Lần chạy đầu: `research/2026-11-22-radar/RADAR.md`, 67 video, 3 ứng viên.
  - Báo cáo kênh `scripts/research/yt_analytics_report.py`.
  - Kho ý tưởng `ideas/IDEA_BANK.md`. Video thắng `analytics/WINNERS.md`.
- **Đăng:** `scripts/yt_publish.py` áp gói đăng và hẹn giờ cho video anh đã tải lên Studio (để Riêng tư). [Cần thử với Short đầu tiên] API có cho đặt `publishAt` hay không.
- **Tự kiểm kịch bản:** `scripts/qa_check.py`.
- **Kiểm thử công cụ:** `python -m pytest -q .claude/skills/hoang-dung-clay-lapis-studio/scripts/tests` (6 bài, đạt 22/11/2026).

## Thay đổi quan trọng (22/11/2026, cuối ngày)
- **Phạm vi chủ đề đã mở rộng thành 5 trụ cột kể chuyện** (`references/content-pillars.md`): bí ẩn Trái Đất và đại dương, sinh tồn và thám hiểm, chiến tranh, thảm họa, thế giới cổ đại và thần thoại. Gilgamesh vẫn là video thử thuộc trụ cột P5.
- **Phân tích kênh nào cũng dùng YouTube Data API trước:** `scripts/research/yt_api_channel.py`. Đã chạy cho @WartimeStories, kết quả ở `channel-studio/research/2026-11-22-wartimestories/Wartime_Stories_api.md`: 158 video dài, trung vị 459K view, 10 video gần nhất trung bình 225K (đang giảm), 21 video viral, dài 38,8 phút.
- **ĐÃ XONG (22/11, phiên trên máy anh):** phân tích lại @WartimeStories theo playbook mục A.
  - Báo cáo: `research/2026-11-22-wartimestories/BAO_CAO.md`. Bản cũ đổi tên thành `BAO_CAO_v1_cu.md`.
  - Kế hoạch: `KE_HOACH_90_NGAY.md` **bản 2**. Anh yêu cầu 1–2 video mỗi ngày, 30–60 video mỗi 30 ngày, **tính cả Shorts** (anh xác nhận 22/11).
    - Chia thành 8 video dài (thứ Ba, thứ Sáu, 21:00 giờ Việt Nam) + khoảng 38 Shorts mỗi 30 ngày.
    - Shorts bắt đầu 01/12. Video dài đầu tiên 11/12. Từ 01/01/2027 lên 2 video dài mỗi tuần, nếu qua được cổng kiểm ngày 28/12.
    - Tuần này (23–30/11) phải làm sẵn 10 Shorts đầu và đo thời gian render.
  - Phụ đề 2 video top: `subs/`.
  - Dàn ý và hook video 002 Lady Be Good: `videos/002-lady-be-good/script_outline.md`, trạng thái `awaiting_human`.
  - Notion: thêm 9 dòng (002–010).
  - Hướng đi: series "Documented", gồm chuyện lạ thời chiến **có hồ sơ thật** (P3 kết hợp P1/P2). Đây là khoảng trống đối thủ để lại.
- **Mốc YPP:** kênh mới từ 01/02/2027 cần 8.000 giờ xem. [Cần kiểm] ICYFOX có thuộc diện "kênh mới" không.
- `check_apis.py` đã được sửa để in tiếng Việt trên console Windows (trước đó lỗi `gbk`).

## Tự động hóa (tạo 22/11/2026 theo yêu cầu anh)
- Tác vụ hẹn giờ trên máy anh (app Claude desktop, mục Scheduled):
  - `icyfox-san-xuat-9h-17h`: cron `0 9,17 * * *` (09:00 và 17:00 mỗi ngày). **Chế độ tự lái** từ 22/11/2026 (T-018).
  - `icyfox-bao-cao-tuan-cn-9h`: cron `0 9 * * 0` (Chủ nhật 09:00). Báo cáo bằng `yt_analytics_report.py` vào `analytics/reports/<ngày>/`, rồi làm tiếp `analytics-loop.md` §3.
- Chỉ chạy khi app Claude đang mở; app đóng thì chạy khi mở lại. Không tự duyệt, không tải video lên.
- T-018 xong 22/11/2026 (phiên trên máy anh): sửa bằng công cụ scheduled-tasks của app, giờ chạy giữ nguyên, không tạo tác vụ mới, không tạo trên cloud. Chưa có lần chạy nào (list_task_runs = 0), nên thư mục chạy thật sẽ kiểm ở lần chạy 23/11 09:00; lời nhắn đã ghi rõ thư mục.
- Lời nhắn tác vụ sản xuất (nguyên văn autopilot.md §8, thêm 1 dòng cho máy Windows):
  ```
  [nguyên văn khối lời nhắn ở references/autopilot.md §8]
  (Máy anh, Windows: thư mục làm việc C:\Users\Admin\HDRE AI\ClayLapis\OpenMontage, đã có repo, không cần clone. Nếu lỗi encoding thì đặt PYTHONUTF8=1. Trả lời tiếng Việt, gọi "anh", xưng "tôi".)
  ```
- Lời nhắn tác vụ báo cáo (tóm tắt 6 bước): mở phiên → `tasks.py add "Báo cáo tuần <ngày>" --type analytics ... --start` → `yt_analytics_report.py --days 28` (report.md + data.json + WINNERS.md; số liệu API không có thì ghi "API không cung cấp") → làm hết `analytics-loop.md` §3 → `tasks.py done` có component → session_end.py → gửi anh ≤ 8 dòng. Chỉ đọc số liệu, không tạo thêm tác vụ.
- Bản đầy đủ nằm ở `~/.claude/scheduled-tasks/<id>/SKILL.md` trên máy anh.

## Ai đang làm gì
Xem `channel-studio/TASKS.md` (sinh từ `state/tasks.json`). Nhận việc: `tasks.py start <id> --owner <claude|codex>`. Quy tắc: `references/multi-agent.md`.

## Cảnh báo QA (22/11/2026, tối)
- **002 Phần 1 HỎNG QA (đã xử lý 22/11, T-019):** file từng ghi "khoảng 1.270 từ, đọc xong 10:40", thật ra 753 từ. Đã tính lại mốc giờ theo số từ thật, bỏ các câu không có nguồn; nay 740 từ, 00:00–06:08, QA ĐẠT.
  - Từ nay `qa_check.py` tự đối chiếu số từ ghi trong file với số từ thật.
- **002 từ Phần 2:** mỗi phần tự kiểm bằng `qa_check.py`. Anh đã duyệt cả kịch bản 1 lần (22/11) thay vì từng phần, theo yêu cầu "chỉ hỏi việc quan trọng". Project `lady-be-good` vẫn dùng pipeline `animated-explainer`, nên cổng script cần đúng 1 lần duyệt đó.

## Trạng thái API (22/11/2026)
- **Gemini:** OK. Network secret, header `x-goog-api-key`. Thấy model `gemini-3.8-flash-tts`.
- **YouTube OAuth + Data API + Analytics:** **OK** (22/11/2026, đã bật API trong dự án 979474479924). Kênh **ICYFOX** (0 sub, 0 video). Anh đã chốt giữ tên ICYFOX.
- **OpenAI:** OK (Network secret `api.openai.com`, Bearer). Có model giọng và model ảnh.
- **Drive:** chưa cấu hình. Cần xin quyền riêng (`drive.file`), lưu vào `GDRIVE_REFRESH_TOKEN`. Không gấp.
- **ElevenLabs:** **OK** (22/11/2026). Gói **free**, đã dùng 0/10.000 ký tự. Gói miễn phí **không được dùng cho video đăng kênh**, chỉ dùng để nghe thử giọng. Muốn dùng giọng ElevenLabs trong video thì anh cần nâng lên gói trả phí.

## Video đang làm
| Video | Thư mục | Bước hiện tại | Đang chờ gì |
|---|---|---|---|
| 002 Lady Be Good (đăng dự kiến 11/12) | `channel-studio/videos/002-lady-be-good/` · project `lady-be-good` (research + proposal đã ghi checkpoint) | Kịch bản 4 phần anh đã duyệt 22/11. Giọng Algenib anh chốt 22/11; đang tạo lời đọc 31 đoạn (T-025) | AI: lời đọc → phân cảnh → tài nguyên → dựng → gói đăng (tự duyệt). Anh: kéo thả MP4 khi xong |
| 001 Gilgamesh: The Lost Lines (video thử) | `channel-studio/videos/001-gilgamesh-lost-lines/` · project `gilgamesh-pilot` | Kịch bản: Phần 1 và 2 đã duyệt (1.867 từ, khoảng 15:46). Phần 3 và 4 chưa viết. Bản đồ 16 repo: references/toolbox-repos.md của skill | Tôi: kiểm S3.5, S4.1, S4.6, làm 3 mẫu giọng, viết Phần 3 |

## Quyết định mới trong phiên trước
- Kênh YouTube **giữ tên ICYFOX**. Clay & Lapis là tên dự án.
- Có file mẫu khóa API: `channel-studio/config/api_keys.env.example` và hướng dẫn `channel-studio/config/HUONG_DAN_KHOA_API.md`. Máy local dùng `OpenMontage/.env`.
- Thử mẫu giọng S0.4: **ElevenLabs "Brian" đạt** (file nằm trên máy cloud cũ, không lên git). **Gemini lỗi 404**: công cụ `gemini_tts` gọi API v1, model chỉ có ở v1beta, phải sửa công cụ. **OpenAI 429**: tài khoản chưa nạp tiền.
- Đã tạo skill `hoang-dung-clay-lapis-studio` và sắp xếp lại thư mục `channel-studio/`.
- Mục tiêu video thử: 35–40 phút. Đã bỏ đoạn S4.8 ("wasteland" không kiểm được bài gốc).

## Việc tiếp theo (theo thứ tự)
0. **Nếu anh gửi link kênh đối thủ:** làm đủ `request-playbooks.md` mục A trong cùng lượt trả lời.
0a. **002: lời đọc làm lại bằng `gemini-3.1-flash-tts-preview` giọng Algenib (anh chốt 22/11 23:50)** vì 3.8 hết 10 lượt/ngày. Ra `projects/lady-be-good/assets/audio/narration_g31/` bằng `voice/alt_voice.py` (chạy lại là làm tiếp đoạn còn thiếu, tự dừng khi hết lượt). Thư mục `narration/` (8 đoạn bằng 3.8) chỉ để tham khảo, không dùng trong video. Kiểm bằng `check_voice.py` + `narration_report.py`. `gemini_tts.py` còn 404 (T-002, của Codex). 001 dời sang 25/12 (dòng Notion đã đổi 22/11). **Tiến độ 22/11 23:59: 10/31 đoạn (S0.1–S3.2), hết lượt ngày (429 PerDay).** Chạy lại cùng lệnh sau 15:00 giờ VN, ghi log vào `channel-studio/state/jobs/<ngày>-voice-002-g31.log`. Gói miễn phí khoảng 10 đoạn/ngày nên cần thêm khoảng 2 ngày (dự kiến xong 24/11), vẫn kịp lịch đăng 11/12.
0a2. **Giám sát tác vụ (anh yêu cầu 22/11):** `autopilot.py` đã gồm `watchdog.py` (thẻ treo, quá hạn, lỗi log `state/jobs/`); gặp lỗi tra `references/fallbacks.md` (F0–F10). Sơ đồ thư mục: `guides/SO_DO_THU_MUC.md` (mục 6 đã xử lý, mục 7 giám sát).
0b. Lấy lại phụ đề video `QkRRERFPfEM` (lần trước bị lỗi 429).
0c. **T-007 (radar lần 2): KHÔNG chạy trước 23/11/2026 21:17 giờ VN.** Radar lần 1 tra lúc 22/11 21:17; cần cách 24–48 giờ mới đo được đà tăng. Phiên tự lái 23/11 lúc 09:00 và 17:00 bỏ qua thẻ này. Lần hợp lệ đầu tiên là phiên 24/11 09:00 (khoảng 36 giờ, vẫn kịp hạn 24/11). Làm: `niche_outliers.py --days 7`, rồi so lượt xem 3 video `BwyM7aGf8p0`, `R2gNUN0ljTc`, `3NE-Cz96W7E` với `research/2026-11-22-radar/outliers.json`. Video nào còn tăng thì gắn nhãn "ĐANG LÊN – ĐÃ KIỂM CHỨNG" trong IDEA_BANK.
1. Chạy `check_apis.py`. Đạt là thấy tên kênh, số sub, và Analytics OK. Nếu lỗi, tra bảng sự cố trong `references/environment-and-apis.md`.
2. Làm 3 mẫu giọng Gemini cho đoạn S0.4 (`videos/001-gilgamesh-lost-lines/script_part1.md`), gửi anh chọn.
3. Kiểm S3.5 (Enkidu can ngăn), S4.1 ("để Enkidu đi trước"), S4.6 ("trước khi các vị thần biết chuyện") bằng bản dịch Thompson 1928 (cần mở host archive.org).
4. Viết Phần 3: chương 5 (Ishtar và Bò Trời), chương 6 (Enkidu chết), chương 7 (tận cùng thế giới).
5. Viết Phần 4: chương 8 (Hồng thủy, George Smith 1872, Atrahasis, so sánh với Kinh Thánh) và chương 9 (Dream Tablet 2021, Fragmentarium với bản chép năm 130 TCN, bác bỏ tin "tìm thấy mộ" năm 2003, Tablet XII, kêu gọi theo dõi kênh).
6. Phân cảnh → tài nguyên → render HyperFrames → gói đăng. **Đo thời gian render và chi phí.**
7. Khi video thử đạt: tạo các tác vụ hẹn giờ theo `references/automation.md` (anh đã đồng ý).

## Việc anh cần làm
- Xác minh tài khoản tại youtube.com/verify, để tải được video trên 15 phút.
- Nạp tiền OpenAI nếu muốn dùng giọng hoặc ảnh của OpenAI.

## Số đo đã có
- Giọng Gemini: 25 token/giây âm thanh. 9 USD/1 triệu token đến 31/12/2026, 18 USD từ 01/01/2027.
- Thời gian render và hạn mức Claude: chưa đo.
