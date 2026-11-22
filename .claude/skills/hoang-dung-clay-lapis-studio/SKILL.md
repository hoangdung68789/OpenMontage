---
name: hoang-dung-clay-lapis-studio
description: "Vận hành trọn quy trình kênh YouTube Clay & Lapis (lịch sử cổ đại và thần thoại, lời thoại tiếng Anh, người xem Mỹ, giọng AI, phụ đề 11 ngôn ngữ). Gồm: mở và đóng phiên đúng cách (đọc HANDOFF, khôi phục hồ sơ dự án, kiểm tra API, lưu GitHub), phân tích đối thủ, chọn chủ đề, viết kịch bản có nguồn theo từng phần, làm mẫu giọng, dựng video bằng OpenMontage + HyperFrames, soạn gói đăng (tiêu đề, mô tả, thumbnail, hashtag, phụ đề), gắn phụ đề và đọc số liệu qua YouTube API, cập nhật bảng Notion. Dùng ngay khi Dũng nhắc đến Clay & Lapis, 'làm tiếp kênh', video lịch sử, thần thoại, Gilgamesh, Lưỡng Hà, phần kịch bản tiếp theo, mẫu giọng, gói đăng, kiểm tra API kênh, báo cáo tuần, quét đối thủ, hoặc khi mở phiên mới cho kênh, kể cả khi không gọi tên skill."
---

# Clay & Lapis Studio

Skill này là "sổ tay vận hành" của kênh Clay & Lapis. Mỗi phiên cloud chạy trên một máy mới, không nhớ gì từ phiên trước. Vì vậy mọi trạng thái nằm trong repo GitHub, bảng Notion và môi trường cloud. Skill chỉ cho biết phải đọc gì, làm theo thứ tự nào, và cất lại ở đâu.

Người dùng là Dũng. Gọi "anh", xưng "tôi", viết tiếng Việt. Anh không rành kỹ thuật: hướng dẫn từng bước nhỏ, kèm link trực tiếp.

## Bản đồ tài nguyên

| Thứ | Ở đâu |
|---|---|
| **Trạng thái mới nhất** (đọc đầu tiên) | `channel-studio/HANDOFF.md`, repo `hoangdung68789/OpenMontage`, nhánh `ccr-6640cec8-2anthl` |
| Cấu trúc thư mục, quy ước tên | `references/workspace-structure.md` |
| Môi trường cloud, khóa, API, sự cố thường gặp | `references/environment-and-apis.md` |
| Quy trình sản xuất một video, nhận diện hình ảnh | `references/production-workflow.md` |
| Chính sách YouTube, ngưỡng kiếm tiền, giấy phép | `references/policy-guardrails.md` |
| Gói đăng, lịch đăng, 11 ngôn ngữ | `references/publish-package.md` |
| Nghiên cứu đối thủ và ngách | `references/research-playbook.md` + `scripts/research/` |
| Tự động hóa, tác vụ hẹn giờ | `references/automation.md` |
| **16 repo của anh: repo nào dùng ở bước nào** | `references/toolbox-repos.md` |
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
2. Đọc hết `HANDOFF.md`. Đọc các dòng Notion có trạng thái khác "Đã đăng".
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
| "mẫu giọng" | Làm 3 mẫu giọng Gemini cho đoạn khó đọc nhất (cổng duyệt) |
| "dựng" | Phân cảnh → tài nguyên → ghép → render (có cổng duyệt) |
| "gói đăng" | Soạn theo `publish-package.md` |
| "gắn phụ đề <link>" | Sau khi anh đã tải video lên: đưa phụ đề, tiêu đề và mô tả đã dịch lên qua API |
| "báo cáo tuần" | Lấy số liệu YouTube Analytics, so với tuần trước, đề xuất điều chỉnh |
| "quét đối thủ" | Làm theo `research-playbook.md` |
| "lưu", "kết thúc phiên" | Đóng phiên (mục 5) |

## 3. Quy trình một video

| # | Bước | Duyệt? | Kết quả |
|---|---|---|---|
| 1 | Nghiên cứu (research) | Không | `research_brief.json` hợp lệ theo schema |
| 2 | Đề xuất (proposal) | **Có** | 3 concept, so sánh **cả 2 công cụ dựng** (HyperFrames, Remotion), cách dựng (atelier hay cảnh mẫu), chi phí |
| 3 | Kịch bản, chia phần | **Có, từng phần** | `script_partN.md`: lời tiếng Anh, ghi chú giọng và hình, bản dịch Việt, nguồn |
| 4 | Mẫu giọng | **Có** | 3 mẫu 30–60 giây |
| 5 | Phân cảnh (scene_plan) | **Có** | Danh sách cảnh có mốc giây, nguồn ảnh đã kiểm giấy phép |
| 6 | Tài nguyên (assets) | **Có** | Giọng đọc, ảnh, bản đồ, nhạc, kèm danh sách ghi công |
| 7 | Dựng và render | Không | MP4 16:9. Kiểm tra bằng `npx hyperframes lint` và `check` |
| 8 | Gói đăng | **Có** (bước publish) | Tiêu đề, mô tả, thumbnail, 11 file SRT, 3–5 Shorts |
| 9 | Anh tải lên và hẹn giờ | Anh làm | Link video |
| 10 | Gắn phụ đề và bản dịch | Không | Phụ đề và bản dịch đã lên YouTube |
| 11 | Báo cáo sau 7 ngày | Không | Notion: giờ xem, sub mới |

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
