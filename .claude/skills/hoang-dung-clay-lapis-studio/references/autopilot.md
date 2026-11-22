# Chế độ tự lái của ICYFOX

Anh yêu cầu (22/11/2026): "Tôi muốn tất cả đều tự động hóa… chỉ những yếu tố quan trọng mới cần hỏi tôi. AI tự tìm chủ đề đang nổi lên theo thời gian thực, tự viết kịch bản, tự dựng video, rồi đăng lên YouTube."

## 1. Ai làm gì
| Việc | Ai làm | Công cụ |
|---|---|---|
| Tìm chủ đề đang lên (radar 2 ngày/lần), đọc số liệu kênh, chọn ý tưởng | AI | `niche_outliers.py`, `yt_analytics_report.py`, IDEA_BANK |
| Dàn ý, hook, kịch bản đầy đủ, tự kiểm | AI | OpenMontage pipeline `icyfox-autopilot`, `qa_check.py` |
| Giọng đọc, phân cảnh, tài nguyên, dựng, render | AI | gemini_tts, HyperFrames |
| Shorts, gói đăng (tiêu đề, mô tả, thẻ, thumbnail, 11 phụ đề, bản dịch, giờ đăng) | AI | `publish-package.md` |
| Chọn chủ đề và dàn ý tuần sau (thay lô duyệt tuần, bỏ từ 22/11/2026): AI tự chốt theo kế hoạch + số liệu, ghi vào HANDOFF | AI | IDEA_BANK, radar, Analytics |
| **Xem kết quả**: báo cáo Chủ nhật (số liệu kênh, doanh thu) | **Anh** | `yt_analytics_report.py` |
| **Kéo thả file MP4 của tuần vào YouTube Studio, để Riêng tư, không cần điền gì** | **Anh** (khoảng 10 phút, thứ Bảy hoặc Chủ nhật) | YouTube Studio |
| Áp tiêu đề, mô tả, thumbnail, phụ đề, bản dịch, hẹn giờ công khai | AI | `yt_publish.py auto` |
| Báo cáo, học từ video thắng, chỉnh kế hoạch | AI | `analytics-loop.md` |
| Các "việc quan trọng" ở §4 | Anh quyết | — |

### Vì sao anh vẫn phải tự kéo thả file lên YouTube
Video tải lên bằng API từ dự án Google chưa qua kiểm duyệt (audit) bị khóa ở chế độ Riêng tư, không kháng nghị được, và không kiếm tiền được ([YouTube Help 7300965](https://support.google.com/youtube/answer/7300965), đã ghi trong `policy-guardrails.md`). Dùng trình duyệt tự động để tải lên thay anh thì trái Điều khoản của YouTube về truy cập tự động. Vì vậy:
- **Bây giờ:** anh kéo thả. AI làm mọi phần còn lại qua API.
- **Sau này (tùy chọn):** nộp đơn audit API của YouTube. AI soạn sẵn nội dung đơn, anh nộp. Google có duyệt hay không: [Chưa xác minh].
- **[Cần thử với video đầu tiên]:** API có cho đặt `publishAt` (hẹn giờ công khai) trên video anh tải bằng Studio hay không. Nếu bị từ chối: AI vẫn áp metadata, phụ đề và thumbnail, anh chỉ bấm hẹn giờ.

## 2. Vòng hằng ngày (phiên tự động)
1. `session_start.sh` (kéo bản mới nhất, kiểm API, in HANDOFF).
2. `python3 SK/scripts/autopilot.py`: in việc theo thứ tự ưu tiên (trễ tiến độ so với ngày đăng, Shorts tồn kho, series, radar, báo cáo, lô duyệt, gói tải lên).
3. Làm từ trên xuống. Mỗi việc là một thẻ trong `tasks.py`, theo `work-contract.md`. Làm đến khi hết việc, hoặc gặp một việc ở §4.
4. `yt_publish.py scan`: có video Riêng tư mới mang tên mã gói thì `yt_publish.py auto`.
5. `session_end.py`. Gửi anh **1 tin ngắn**: đã làm gì (bảng thành phần), việc anh cần làm (nếu có).

**Thời hạn trước ngày đăng** (trong `autopilot.py`, NHẬN ĐỊNH):
| Mốc | Trước ngày đăng |
|---|---|
| Dàn ý được duyệt | 14 ngày |
| Kịch bản đủ, QA đạt | 9 ngày |
| Render xong | 4 ngày |
| Gói đăng xong | 2 ngày |
| Shorts tồn kho | Luôn đủ cho 7 ngày |

## 3. Nhịp tuần
| Ngày (giờ Việt Nam) | Việc |
|---|---|
| Chủ nhật 09:00 (tác vụ trên máy anh) | Báo cáo số liệu kênh (`yt_analytics_report.py`) và cập nhật WINNERS, IDEA_BANK |
| 2 ngày một lần | Radar xu hướng |
| Thứ Năm | AI tự chốt lô tuần sau (mẫu ở §5), ghi vào HANDOFF. **Không gửi anh duyệt** (anh giao quyền 22/11/2026) |
| **Thứ Bảy** | **GÓI TẢI LÊN** gửi anh: danh sách file MP4 theo thứ tự, link tải (Drive hoặc thư mục trên máy anh) |
| Sau khi anh tải lên | `yt_publish.py auto`: áp gói, hẹn giờ, phụ đề. Báo anh danh sách đã hẹn giờ |

## 4. Việc quan trọng: CHỈ những việc này mới hỏi anh
Cập nhật 22/11/2026 theo lời anh: "Kênh youtube tôi giao cho bạn quản lý… mục tiêu cuối cùng là bật kiếm tiền trên youtube và duy trì tính năng kiếm tiền. Tôi chỉ xem kết quả từ dữ liệu kênh đạt được và số tiền kiếm được… giai đoạn đầu thì hỏi tôi khi chưa rõ, sau khi đủ thông tin để chốt kế hoạch thì thực thi mà không cần hỏi lại tôi nữa" (anh Dũng, 22/11/2026). Lô duyệt tuần đã bỏ. Kế hoạch 90 ngày đã chốt, nên mọi việc trong kế hoạch AI tự làm.
1. *(Đã bỏ: lô duyệt tuần.)*
2. **Cờ "CẦN ANH XEM"** của `qa_check.py`: AI tự chọn phương án an toàn (bỏ hoặc làm nhẹ đoạn đó, theo `policy-guardrails.md`), ghi vào HANDOFF. Chỉ hỏi khi bỏ đoạn đó làm hỏng cả video.
3. **Tiền:** khoản chi mới ngoài ngân sách, nâng gói (ElevenLabs, OpenAI…). Ngân sách giọng Gemini khoảng 9 USD/tháng đã được duyệt (KE_HOACH_90_NGAY §4).
4. **Tài khoản và quyền:** cần anh đăng nhập, xác minh, bật API, cấp lại token, xử lý cảnh cáo hay vi phạm của YouTube.
5. **Đổi tên kênh hoặc nhận diện kênh.** Đổi nhịp đăng, trụ cột, series theo số liệu thì AI tự làm, ghi lý do vào decisions-log và nêu trong báo cáo Chủ nhật.
6. **Mâu thuẫn với MISSION** hoặc chính sách.

Mọi việc khác AI **tự quyết, ghi lý do vào HANDOFF hoặc decisions-log, rồi làm tiếp**. Câu hỏi gom vào lô duyệt tuần, trừ khi gấp (mục 2 và 4).

## 5. Mẫu LÔ DUYỆT TUẦN (1 tin nhắn, anh trả lời "duyệt" hoặc "duyệt, trừ …")
```
LÔ DUYỆT TUẦN <ngày> → <ngày>
Video dài:
 1) <mã> <tiêu đề> · đăng <ngày> · trụ cột · bằng chứng nhu cầu (link + số + ngày tra)
    Hook 60 giây: <đoạn văn>
    Dàn ý: <5–8 dòng chương>
    Rủi ro / cờ: <không có | …>
Shorts tuần sau: <7–8 dòng tiêu đề + nguồn>
Thay đổi so với kế hoạch: <không có | đổi X sang Y vì …>
Cần anh quyết: <không có | câu hỏi kèm phương án mặc định>
```
Khi anh duyệt: ghi `ĐÃ DUYỆT <ngày> (lô tuần)` ở dòng đầu `script_outline.md`, checkpoint proposal của OpenMontage chuyển `completed` với bằng chứng duyệt, ghi decisions-log, rồi sản xuất tiếp không hỏi thêm.

## 6. Cổng duyệt của OpenMontage trong chế độ tự lái
Pipeline `pipeline_defs/icyfox-autopilot.yaml` là bản sao của `animated-explainer`. Chỉ khác cổng duyệt của người, theo yêu cầu của anh:
| Bước | Cổng | Thay bằng |
|---|---|---|
| proposal | Tự động (anh giao quyền 22/11/2026) | Ý tưởng có bằng chứng nhu cầu trong IDEA_BANK; ghi duyệt `auto` kèm trích lời anh |
| script | Tự động | `qa_check.py` ĐẠT. Gặp "CẦN ANH XEM" thì dừng, đưa vào lô duyệt |
| scene_plan | Tự động | Mọi ảnh có giấy phép thương mại và ghi công (`policy-guardrails.md`) |
| assets | Tự động | Giọng đọc dài khớp kịch bản ±10%; `npx hyperframes lint` + `check` đạt |
| publish | **Giữ:** anh tải file lên | `yt_publish.py` làm phần còn lại |

Video thử 001 Gilgamesh vẫn dùng `animated-explainer` (đã duyệt từng phần).

## 7. Nơi render
- **Cloud:** chưa đo. Giai đoạn 0 phải render thử 3 phút, ghi thời gian vào `render/RENDERED.txt` và HANDOFF.
- **Máy anh:** `local-render.md`. Có thể đặt Task Scheduler của Windows tự `git pull` và render ban đêm. Cài 1 lần, AI soạn sẵn lệnh.
- **File MP4 không lên git.** Đưa lên Google Drive (cần `GDRIVE_REFRESH_TOKEN`) hoặc để trên máy anh. Gói tải lên chỉ đường tới file.

## 8. Tác vụ hẹn giờ
**Đang có (22/11/2026):** trên máy anh, app Claude desktop: `icyfox-san-xuat-9h-17h` (09:00 và 17:00) và `icyfox-bao-cao-tuan-cn-9h` (Chủ nhật 09:00).
- Không tạo thêm trên cloud, vì sẽ chạy trùng.
- Tác vụ sản xuất dùng lời nhắn dưới đây. Phiên trên máy anh cập nhật file `~/.claude/scheduled-tasks/icyfox-san-xuat-9h-17h/SKILL.md` (thẻ T-018).
- Máy anh mở Claude Code trong thư mục OpenMontage nên **có đủ 3 hook** nhắc mục tiêu và chặn báo "xong" sai.

Lời nhắn:
```
Dùng skill hoang-dung-clay-lapis-studio, chế độ tự lái. Nếu phiên chưa có repo hoangdung68789/OpenMontage thì add_repo,
clone, checkout nhánh ccr-6640cec8-2anthl. Chạy bash .claude/skills/hoang-dung-clay-lapis-studio/scripts/session_start.sh,
rồi python3 .claude/skills/hoang-dung-clay-lapis-studio/scripts/autopilot.py. Làm lần lượt các việc theo references/autopilot.md
và references/work-contract.md, đến khi hết việc hoặc gặp việc quan trọng ở autopilot.md §4. Mỗi việc là một thẻ tasks.py.
Chỉ báo xong khi tasks.py done chấp nhận. Cuối phiên chạy session_end.py, rồi gửi anh 1 tin ngắn: bảng thành phần đã làm và việc anh cần làm.
```
