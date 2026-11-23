---
name: hoang-dung-clay-lapis-studio
description: "Vận hành kênh YouTube ICYFOX (dự án Clay & Lapis): kể chuyện có thật về bí ẩn Trái Đất, sinh tồn và thám hiểm, chiến tranh, thảm họa, thế giới cổ đại và thần thoại; lời Anh, người xem Mỹ, giọng AI, phụ đề 11 ngôn ngữ. Gồm: mở và đóng phiên (HANDOFF, kiểm API, lưu GitHub), sổ việc có kiểm chứng và nhật ký, phân tích đối thủ bằng YouTube Data API, radar xu hướng, báo cáo số liệu kênh, kịch bản có nguồn, series nhiều tập, giọng đọc, dựng bằng OpenMontage + HyperFrames, gói đăng và hẹn giờ, chế độ tự lái. Dùng ngay khi Dũng nhắc đến ICYFOX, Clay & Lapis, 'làm tiếp kênh', link kênh YouTube cần phân tích, kịch bản, phần tiếp theo, series, tập tiếp theo, xu hướng, mẫu giọng, dựng video, gói đăng, báo cáo tuần, số liệu kênh, đối thủ, tự động hóa, tự lái, sổ việc, nhật ký, hoặc khi mở phiên mới cho kênh, kể cả khi không gọi tên skill."
---

# Clay & Lapis Studio

Skill này là "sổ tay vận hành" của kênh Clay & Lapis. Mỗi phiên cloud chạy trên một máy mới, không nhớ gì từ phiên trước. Vì vậy mọi trạng thái nằm trong repo GitHub, bảng Notion và môi trường cloud. Skill chỉ cho biết phải đọc gì, làm theo thứ tự nào, và cất lại ở đâu.

Người dùng là Dũng. Gọi "anh", xưng "tôi", viết tiếng Việt. Anh không rành kỹ thuật: hướng dẫn từng bước nhỏ, kèm link trực tiếp.

## 0. Tiêu chuẩn làm việc (đọc trước mọi việc)

Ngày 22/11/2026, anh rất thất vọng với một phiên khác. Anh gửi link kênh @WartimeStories và yêu cầu "phân tích đối thủ và lên kịch bản/kế hoạch dài hạn". Phiên đó trả lời như sau:
- Bỏ qua `session_start.sh` và `check_apis.py`.
- Dùng yt-dlp dù đã có YouTube Data API. Anh phải nhắc thì mới dùng.
- Không xem nội dung video của đối thủ.
- Gạt đối thủ sang một bên vì "không cùng ngách", rồi kéo về chủ đề cổ đại cũ.
- Không giao kịch bản hay kế hoạch, kết thúc bằng 3 câu hỏi.
- Không lưu kết quả lên git.

Các tiêu chuẩn dưới đây là để không lặp lại những lỗi đó. **Bản đầy đủ và bắt buộc: `references/work-contract.md`** (chu trình 6 bước, luật chống làm nửa vời, QUY TẮC HOÀN THÀNH, 7 lớp chống quên). **Mục tiêu vĩnh viễn: `channel-studio/MISSION.md`. Kế hoạch hiện hành: `channel-studio/PLAN.md`.**

1. **Mở phiên trước khi làm bất cứ gì** (mục 1). Câu trả lời đầu tiên phải ghi kết quả kiểm tra API.
2. **Có khóa API thì dùng ngay.**
   - Phân tích kênh hay video đối thủ: **YouTube Data API trước tiên**, bằng `scripts/research/yt_api_channel.py`.
   - Chỉ dùng yt-dlp khi API lỗi (phải ghi rõ lỗi), hoặc khi cần quét tìm kiếm diện rộng.
   - Không trả lời câu hỏi về số liệu bằng trí nhớ.
3. **Giao đủ sản phẩm anh yêu cầu ngay trong lượt đó**, theo "định nghĩa hoàn thành" ở `references/request-playbooks.md`.
   - Anh xin kịch bản thì phải có kịch bản (ít nhất bản nháp để duyệt). Anh xin kế hoạch thì phải có kế hoạch.
   - Còn điểm nào chưa rõ: tự chọn phương án mặc định hợp lý, ghi rõ đã chọn gì, rồi làm tiếp. Câu hỏi chỉ để ở cuối, tối đa 3 câu, và chỉ cho quyết định thật sự cần anh chốt.
4. **Đối thủ anh gửi là tín hiệu về chủ đề anh muốn.** Phân tích nghiêm túc và tìm cách làm hợp lệ.
   - Lời kể nhân chứng, truyền thuyết: kể được nếu ghi rõ đó là lời kể và ghi nguồn.
   - Không gạt đi vì "không cùng ngách". Phạm vi chủ đề hiện tại: `references/content-pillars.md`.
5. **Kênh ICYFOX có mục tiêu khác hồ sơ bất động sản của anh.**
   - Anh đã chốt (22/11/2026): mục tiêu là lượt xem, giờ xem và đủ điều kiện kiếm tiền YouTube. Không phải "ra khách bất động sản".
   - Vẫn giữ quy tắc dẫn chứng và khung trả lời KẾT LUẬN / CHI TIẾT / DẪN CHỨNG / BƯỚC TIẾP THEO.
6. **Lưu kết quả bằng `session_end.py`.**
   - Dữ liệu kênh nằm ở nhánh `ccr-6640cec8-2anthl`.
   - Làm theo quy định git của phiên. Nếu phiên được giao nhánh khác và chưa có lời anh cho phép đẩy lên `ccr-6640cec8-2anthl`, hỏi anh 1 câu trước khi push.
7. **Tự kiểm trước khi gửi câu trả lời:** đối chiếu với bảng "Tự kiểm" trong `references/request-playbooks.md` và `work-contract.md` §5.
8. **Mỗi việc là một thẻ trong sổ việc** (`scripts/tasks.py`), có mục "xong khi" kiểm được. Đọc đúng file theo `references/read-map.md`.
9. **Chỉ báo "xong" khi `tasks.py done` chấp nhận:**
   - sản phẩm có thật
   - đã kiểm chứng thật
   - có báo cáo từng thành phần (`--component "Tên :: Kết quả :: Cách kiểm chứng :: Bằng chứng"`)
   - đã ghi vào nhật ký lịch sử `channel-studio/logs/`.
   Chưa đủ thì nói rõ phần nào chưa xong. Hook Stop chặn câu "đã xong" khi không có thẻ nào được `done`.
10. **Tự lái, chỉ hỏi việc quan trọng** (`references/autopilot.md` §4). Việc khác tự quyết, ghi lý do, làm tiếp. Câu hỏi gom vào LÔ DUYỆT TUẦN (thứ Năm).

## Bản đồ tài nguyên

| Thứ | Ở đâu |
|---|---|
| **Mục tiêu vĩnh viễn** (đọc đầu tiên) | `channel-studio/MISSION.md` |
| **Kế hoạch hiện hành** (giai đoạn, lịch đăng) | `channel-studio/PLAN.md` (khối `phases`, `releases` do `autopilot.py` đọc) |
| **Sổ việc** (ai làm gì, xong khi nào) | `channel-studio/TASKS.md`, sinh từ `channel-studio/state/tasks.json` bằng `scripts/tasks.py` |
| **Nhật ký lịch sử** (báo cáo hoàn thành từng việc) | `channel-studio/logs/<năm-tháng>.md` (chỉ thêm) |
| **Hợp đồng làm việc + quy tắc hoàn thành** | `references/work-contract.md` |
| **Loại việc nào đọc file nào, dùng công cụ nào** | `references/read-map.md` |
| **Chế độ tự lái** (ai làm gì, nhịp tuần, việc quan trọng phải hỏi, giám sát + phương án thay thế) | `references/autopilot.md` + `scripts/autopilot.py` + `pipeline_defs/icyfox-autopilot.yaml` |
| **Series nhiều tập** | `references/series-playbook.md` + `scripts/series.py` + `channel-studio/series/` |
| **Số liệu → ý tưởng → video** | `references/analytics-loop.md` + `scripts/research/yt_analytics_report.py`, `niche_outliers.py` (radar) + `channel-studio/analytics/`, `channel-studio/ideas/IDEA_BANK.md` |
| **Tự kiểm kịch bản, áp gói đăng** | `scripts/qa_check.py`, `scripts/yt_publish.py` |
| **Trạng thái mới nhất** | `channel-studio/HANDOFF.md`, repo `hoangdung68789/OpenMontage`, nhánh `ccr-6640cec8-2anthl` |
| Cấu trúc thư mục, quy ước tên | `references/workspace-structure.md` |
| Môi trường cloud, khóa, API, sự cố thường gặp | `references/environment-and-apis.md` |
| Quy trình sản xuất một video, nhận diện hình ảnh | `references/production-workflow.md` |
| Chính sách YouTube, ngưỡng kiếm tiền, giấy phép | `references/policy-guardrails.md` |
| Gói đăng, lịch đăng, 11 ngôn ngữ | `references/publish-package.md` |
| Nghiên cứu đối thủ và ngách | `references/research-playbook.md` + `scripts/research/` |
| Tự động hóa, tác vụ hẹn giờ | `references/automation.md` |
| **Định nghĩa hoàn thành cho từng loại yêu cầu, bảng tự kiểm** | `references/request-playbooks.md` |
| **Làm cùng Codex hoặc agent khác: chia việc, bảng "Ai đang làm gì"** | `references/multi-agent.md` (Codex đọc lối vào tại `.agents/skills/hoang-dung-clay-lapis-studio/`) |
| **Phạm vi chủ đề: 5 trụ cột kể chuyện** | `references/content-pillars.md` |
| **16 repo của anh: repo nào dùng ở bước nào** | `references/toolbox-repos.md` |
| **Khóa API: file mẫu và hướng dẫn** | `channel-studio/config/api_keys.env.example`, `channel-studio/config/HUONG_DAN_KHOA_API.md` |
| **Dựng video v2 (chuẩn edit, 8 giai đoạn + cổng kiểm, cấu trúc thư mục mới, thư viện hiệu ứng máy quay/chuyển cảnh/chữ/màu/bố cục/âm thanh, công thức theo thể loại)** | `references/edit-workflow.md` → `edit-library.md`, `genre-recipes.md`; cơ sở: `edit-standard.md`; tạo thư mục: `scripts/new_video.py create` |
| **Motion graphics: không cảnh nào đứng yên** (mốc đo, 3 lớp chuyển động, bộ cảnh dựng sẵn, thành phần HyperFrames theo nhu cầu) | `references/motion-graphics.md` + `channel-studio/motion-kit/` + `scripts/motion_metrics.py` |
| **Render nhanh trên máy anh** | `references/local-render.md` |
| **Đổi máy tính, khôi phục toàn bộ dữ liệu** | `channel-studio/guides/KHOI_PHUC_MAY_MOI.md` + `scripts/restore_machine.sh` |
| Chạy trên máy anh thay vì cloud | `channel-studio/guides/local_setup.md` + mục "Chế độ máy local" trong `environment-and-apis.md` |
| **Giám sát tác vụ, lỗi thường gặp và phương án thay thế** | `references/fallbacks.md` + `scripts/watchdog.py` |
| Quyết định đã chốt | `references/decisions-log.md` |
| Bảng Notion | "Clay & Lapis – Video Pipeline", data source `collection://4201dcd7-7c95-8188-8452-000b17602005` |
| Mẫu file | `templates/` |

Chỉ đọc file tham chiếu nào cần cho việc đang làm. Không cần đọc hết.

## 1. Mở phiên (luôn làm trước mọi việc)

1. Từ thư mục gốc repo OpenMontage, chạy:
   ```bash
   bash .claude/skills/hoang-dung-clay-lapis-studio/scripts/session_start.sh
   ```
   Script làm 4 việc:
   - Chuyển sang nhánh `ccr-6640cec8-2anthl` và kéo bản mới nhất.
   - Chép hồ sơ dự án từ `channel-studio/projects/` về `projects/`. Thư mục `projects/` của OpenMontage bị gitignore nên phải chép lại.
   - Chạy `check_apis.py`.
   - In `HANDOFF.md`.

   Nếu skill được cài ở cấp tài khoản mà repo chưa ở đúng nhánh, chạy trước: `git fetch origin ccr-6640cec8-2anthl && git checkout ccr-6640cec8-2anthl`.
2. Đọc `MISSION.md`, `PLAN.md`, hết `HANDOFF.md`, `TASKS.md`, 5 mục cuối của nhật ký (`python scripts/tasks.py log --n 5`). Chạy `python scripts/autopilot.py` để xem việc hôm nay. Đọc các dòng Notion có trạng thái khác "Đã đăng".
   Script cũng in danh sách 16 repo, đánh dấu repo nào đang thiếu. Nếu việc sắp làm cần repo đang thiếu (xem `references/toolbox-repos.md`), gọi `add_repo(owner="hoangdung68789", repo=...)`, clone, rồi `register_repo_root` để nạp skill của repo đó.
3. Báo anh 3 dòng: tình trạng API, video đang làm và đang ở bước nào, việc anh cần làm.

Vì sao: bỏ bước này thì dễ làm lại việc cũ, hoặc hỏi lại những gì anh đã chốt.

## 2. Lệnh nhanh

| Anh nói | Việc cần làm |
|---|---|
| "làm tiếp", "trạng thái" | Mở phiên (mục 1), rồi đề xuất việc kế tiếp theo HANDOFF |
| "kiểm tra API" | Chạy `scripts/check_apis.py`. Nếu lỗi, tra bảng sự cố trong `environment-and-apis.md` |
| "video mới: <chủ đề>" | Tạo `channel-studio/videos/NNN-slug/` từ `templates/video_readme_template.md`, thêm dòng Notion, chạy research rồi proposal (cổng duyệt) |
| "viết phần N" | Viết phần kịch bản theo `production-workflow.md` §Kịch bản (cổng duyệt) |
| "mẫu giọng" | Giọng kênh đã chốt là Algenib (decisions-log 22/11/2026). Chỉ làm mẫu khi anh muốn đổi giọng |
| "dựng" | Phân cảnh → tài nguyên → ghép → render (có cổng duyệt) |
| "gói đăng" | Soạn theo `publish-package.md` |
| "gắn phụ đề <link>" | Sau khi anh đã tải video lên: đưa phụ đề, tiêu đề và mô tả đã dịch lên qua API |
| "báo cáo tuần" | Lấy số liệu YouTube Analytics, so với tuần trước, đề xuất điều chỉnh |
| "quét đối thủ" | Làm theo `research-playbook.md` |
| "lưu", "kết thúc phiên" | Đóng phiên (mục 5) |
| "tự lái", "chạy tự động", "hôm nay làm gì" | `scripts/autopilot.py`, rồi làm từ trên xuống theo `autopilot.md` |
| "xu hướng", "chủ đề đang lên", "quét xu hướng" | `scripts/research/niche_outliers.py --days 7` → IDEA_BANK (`analytics-loop.md`) |
| "số liệu kênh", "video nào tốt nhất" | `scripts/research/yt_analytics_report.py` → WINNERS, IDEA_BANK |
| "series mới", "tập tiếp theo" | `series-playbook.md`: `series.py new` hoặc `series.py brief <id>` trước khi viết |
| "sổ việc", "nhật ký", "đã làm gì" | `scripts/tasks.py list`, `scripts/tasks.py log --n 10` |
| "đã tải video lên" | `scripts/yt_publish.py scan` → `auto` |

## 3. Quy trình một video

| # | Bước | Duyệt? | Kết quả |
|---|---|---|---|
| 1 | Nghiên cứu (research) | Không | `research_brief.json` hợp lệ theo schema |
| 2 | Đề xuất (proposal) | **Có** | 3 concept, so sánh **cả 2 công cụ dựng** (HyperFrames, Remotion), cách dựng (atelier hay cảnh mẫu), chi phí |
| 3 | Kịch bản, chia phần | **Có, từng phần** | `script_partN.md`: lời tiếng Anh, ghi chú giọng và hình, bản dịch Việt, nguồn |
| 4 | Giọng đọc | Không (Algenib, model `gemini-3.1-flash-tts-preview`, anh chốt 22/11/2026) | `voice/alt_voice.py` cả video, kiểm bằng whisper. Chỉ làm mẫu khi anh yêu cầu đổi giọng |
| 5 | Phân cảnh (scene_plan) | AI tự duyệt (từ 22/11/2026) | Danh sách cảnh có mốc giây, nguồn ảnh đã kiểm giấy phép |
| 6 | Tài nguyên (assets) | AI tự duyệt (từ 22/11/2026) | Giọng đọc, ảnh, bản đồ, nhạc, kèm danh sách ghi công |
| 7 | Dựng và render | Không | MP4 16:9. Kiểm tra bằng `npx hyperframes lint` và `check` |
| 8 | Gói đăng | AI tự duyệt (từ 22/11/2026) | Tiêu đề, mô tả, thumbnail, 11 file SRT, 3–5 Shorts |
| 9 | Anh tải lên và hẹn giờ | Anh làm | Link video |
| 10 | Gắn phụ đề và bản dịch | Không | Phụ đề và bản dịch đã lên YouTube |
| 11 | Báo cáo sau 7 ngày | Không | Notion: giờ xem, sub mới |

**Video mới từ 23/11/2026 dùng pipeline `icyfox-autopilot`** (`references/autopilot.md` §6):
- Cổng proposal: anh duyệt theo LÔ TUẦN.
- script, scene_plan, assets: kiểm tra tự động (`qa_check.py`, giấy phép ảnh, `hyperframes lint/check`).
- publish: anh kéo thả file lên Studio, `yt_publish.py` làm phần còn lại.
Video thử 001 vẫn dùng `animated-explainer`.

Trước mỗi bước, đọc skill hướng dẫn của bước đó trong OpenMontage, tại `skills/pipelines/explainer/<stage>-director.md`. Quy tắc "Rule Zero" của `AGENT_GUIDE.md` yêu cầu như vậy. OpenMontage chặn ngay trong mã nguồn việc ghi một bước là "completed" khi chưa có duyệt. Vì vậy, ở bước có cổng duyệt: ghi `awaiting_human`, trình bày cho anh, rồi **dừng lượt**. Mỗi cổng phải được duyệt riêng, câu "duyệt" trước đó không áp dụng cho cổng sau.

## 4. Luật cứng (ngắn gọn, chi tiết ở `policy-guardrails.md`)

- **Dữ kiện nào trong kịch bản cũng phải có nguồn.** Không kiểm được thì bỏ, hoặc gắn [Chưa xác minh] và hỏi anh. Kênh định vị "sources on screen", nên một chi tiết sai làm mất uy tín cả kênh.
- **Học cấu trúc của đối thủ, không dùng lại lời, hình hay clip của họ.** Chính sách "reused content" của YouTube xét trên cả kênh.
- **Mỗi video có hook, cấu trúc và hình ảnh riêng.** Không lặp một khuôn mẫu, vì chính sách "inauthentic content" cấm kiếm tiền với nội dung rập khuôn.
- **Không để giọng AI khuyên về tài chính, sức khỏe, pháp lý, chính trị.** YouTube cấm kiếm tiền với dạng "AI persona" đưa lời khuyên ở các chủ đề này.
- **Ảnh chỉ dùng Public domain, CC0, CC BY, CC BY-SA, và phải ghi công.** Không dùng giấy phép NC: ảnh chính thức của British Museum là CC BY-NC-SA. Không dùng ảnh AI giống thật, trừ khi có khai báo AI.
- **Không làm các việc sau:**
  - Tải video lên bằng API: video sẽ bị khóa riêng tư và không kiếm tiền được.
  - Tự đăng lên TikTok bằng API.
  - Dùng proxy hay khai cư trú ở Mỹ.
  - Tạo tương tác ảo.
- **Khóa và token:** không bao giờ in ra màn hình, không bao giờ xin anh dán vào chat.
- **ElevenLabs gói miễn phí không được dùng cho mục đích thương mại.** Chỉ dùng để nghe thử.

## 5. Đóng phiên (khi xong việc, hoặc trước khi anh mở phiên mới)

0. Mọi thẻ việc của phiên phải ở trạng thái xong (`tasks.py done` có báo cáo từng thành phần), chờ anh, hoặc bị chặn. Không để thẻ "đang làm".
1. Cập nhật `channel-studio/HANDOFF.md` theo `templates/handoff_template.md`: trạng thái hiện tại, quyết định mới, việc tiếp theo.
2. Cập nhật dòng Notion của video đang làm.
3. Chạy:
   ```bash
   python3 .claude/skills/hoang-dung-clay-lapis-studio/scripts/session_end.py -m "mô tả ngắn" --trailer "<các dòng ghi công của phiên này, nối bằng \n>"
   ```
   Lấy `--trailer` từ phần ghi công cho commit mà phiên hiện tại được yêu cầu dùng (thường là dòng `Co-Authored-By` và `Claude-Session`). Không chép dòng ghi công của phiên khác.
   Script làm 4 việc:
   - Chép `projects/` vào `channel-studio/projects/`, bỏ qua file lớn.
   - Quét khóa và token. Thấy khóa thì dừng.
   - Commit.
   - Push, thử lại tối đa 4 lần.
4. Báo anh tên nhánh, commit vừa đẩy, và việc anh cần làm.

Vì sao: máy của phiên sẽ bị thu hồi. Thứ gì chưa push là mất.

## 6. Cách trả lời anh

- Khung trả lời: **KẾT LUẬN / CHI TIẾT / DẪN CHỨNG / BƯỚC TIẾP THEO**.
- Mỗi số liệu ghi nguồn kèm ngày tra. Không có nguồn thì ghi [Chưa xác minh].
- Hỏi tối đa 3 câu, mỗi câu có sẵn lựa chọn gợi ý.
- Việc anh phải tự làm trên giao diện (Google Cloud, cài đặt môi trường):
  - Hướng dẫn từng bước, ghi đúng tên nút.
  - Gửi ảnh mẫu khi cần (xem `channel-studio/guides/`).
  - Nhắc anh che khóa khi gửi ảnh chụp màn hình.
