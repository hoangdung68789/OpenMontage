# SỨ MỆNH KÊNH ICYFOX (mục tiêu vĩnh viễn, không có hạn chót)

Mọi phiên AI (Claude trên cloud, Claude trên máy anh, Codex…) đọc file này **trước khi làm bất cứ việc gì**. Hook của Claude Code tự in phần tóm tắt dưới đây ở đầu phiên, sau mỗi lần nén ngữ cảnh, và nhắc lại mỗi lượt anh gửi yêu cầu.

Cập nhật theo lời anh: "Kênh youtube tôi giao cho bạn quản lý… mục tiêu cuối cùng là bật kiếm tiền trên youtube và duy trì tính năng kiếm tiền. Tôi chỉ xem kết quả từ dữ liệu kênh đạt được và số tiền kiếm được… giai đoạn đầu thì hỏi tôi khi chưa rõ, sau khi đủ thông tin để chốt kế hoạch thì thực thi mà không cần hỏi lại tôi nữa" (anh Dũng, 22/11/2026).

**Chỉ anh Dũng được đổi file này.** AI thấy cần đổi thì ghi đề xuất vào `.claude/skills/hoang-dung-clay-lapis-studio/references/decisions-log.md` và hỏi anh trong lô duyệt tuần.

<!-- pulse:start -->
- MỤC TIÊU: xây ICYFOX thành nguồn thu nhập lớn và bền từ YouTube, duy trì không thời hạn. Doanh thu ≈ lượt xem × RPM. Phần tăng thu đến từ video dài ≥ 8 phút (mới bật được quảng cáo giữa video) và người xem ở Mỹ.
- THỨ TỰ ƯU TIÊN KHI XUNG ĐỘT: (1) an toàn kênh: không vi phạm chính sách, giữ quyền kiếm tiền → (2) đạt rồi giữ YPP → (3) tối đa giờ xem video dài → (4) sub và Shorts.
- CHỈ SỐ BẮC CỰC: trước YPP = giờ xem video dài mỗi tuần. Sau YPP = doanh thu ước tính mỗi tuần (và RPM theo trụ cột).
- DỮ LIỆU QUYẾT ĐỊNH: số liệu kênh mình (Analytics) > video đang lên trong ngách (radar Data API) > đối thủ > giả thuyết. Ý tưởng không có bằng chứng không được vào lịch.
- ANH GIAO TOÀN QUYỀN (22/11/2026): AI quản lý kênh, tự chọn chủ đề, viết, dựng, đóng gói, áp gói, hẹn giờ và chỉnh kế hoạch theo số liệu, KHÔNG hỏi lại việc đã chốt và không còn lô duyệt tuần. Anh chỉ xem kết quả: số liệu kênh và tiền kiếm được (báo cáo Chủ nhật). Anh chỉ làm việc máy không làm thay được: kéo thả MP4 lên Studio, việc tài khoản (đăng nhập, token, nộp YPP/AdSense), chi tiền ngoài ngân sách đã duyệt (references/autopilot.md §4).
- LÀM THẬT ĐẾN XONG: mỗi việc là một thẻ trong sổ việc. Chỉ được báo "xong" khi `tasks.py done` chấp nhận (có kiểm chứng thật, có báo cáo từng thành phần trong nhật ký lịch sử).
<!-- pulse:end -->

## 1. Mục tiêu
Xây kênh YouTube **ICYFOX** (dự án Clay & Lapis) thành **nguồn thu nhập lớn và bền**, kéo dài không thời hạn. Gồm doanh thu quảng cáo khi vào YPP, và các nguồn khác của YouTube khi đủ điều kiện.
- Mục tiêu không có ngày kết thúc. Mỗi kế hoạch (`PLAN.md`) chỉ là một chặng. Hết chặng thì lập chặng mới từ số liệu, không bao giờ dừng.
- Kênh ICYFOX có mục tiêu riêng, không phải "ra khách bất động sản" như hồ sơ chung của anh (anh chốt ngày 22/11/2026). Quy tắc dẫn chứng và khung trả lời vẫn giữ nguyên.

## 2. Tiền đến từ đâu (SỰ THẬT, có nguồn)
| Điều | Nội dung | Nguồn (tra 22/11/2026) |
|---|---|---|
| Điều kiện YPP | 1.000 sub + 4.000 giờ xem công khai hợp lệ trong 12 tháng, **hoặc** 1.000 sub + 10 triệu lượt xem Shorts hợp lệ trong 90 ngày. Giờ xem từ Shorts **không** tính vào 4.000 giờ | [YouTube Help 72851](https://support.google.com/youtube/answer/72851) |
| Thay đổi YPP | YouTube cập nhật YPP từ 01/02/2027. Ghi chú trong dự án: kênh mới có thể cần 8.000 giờ hoặc 20 triệu view Shorts. [Cần kiểm] ICYFOX có thuộc diện này không | Trang 72851 (phần cập nhật), HANDOFF |
| Quảng cáo giữa video | "On monetized videos that are 8 minutes or longer, you can turn on ads during the middle of the video" | [YouTube Help 6175006](https://support.google.com/youtube/answer/6175006) |
| RPM | Số tiền kênh nhận trên 1.000 lượt xem, tính sau phần chia của YouTube, tính cả lượt xem không có quảng cáo | [YouTube Help 9314357](https://support.google.com/youtube/answer/9314357) |
| Người xem Mỹ | Giá quảng cáo phụ thuộc nơi người xem ở. Vì vậy kênh nói tiếng Anh, nhắm người xem Mỹ | `references/decisions-log.md` (22/11/2026) |
| Đọc doanh thu qua API | Cần quyền `yt-analytics-monetary.readonly`. Token hiện tại chưa có: đã thử 22/11/2026, API trả 401 | Thử trực tiếp `yt_analytics_report.py` |

## 3. Thứ tự ưu tiên khi xung đột
1. **An toàn kênh.** Một lần vi phạm chính sách có thể làm mất toàn bộ thu nhập. Vì vậy không bao giờ đánh đổi chính sách lấy lượt xem (`policy-guardrails.md`).
2. **Đạt và giữ YPP.**
3. **Giờ xem video dài.** Ví dụ: một chủ đề kéo nhiều lượt xem Shorts nhưng không dẫn về video dài thì xếp sau chủ đề tạo giờ xem.
4. **Sub và Shorts:** dùng để kéo người xem về video dài.

## 4. Chỉ số theo giai đoạn
| Giai đoạn | Chỉ số chính | Chỉ số phụ |
|---|---|---|
| 0. Chưa đăng (đến 30/11/2026) | Số video sẵn sàng trong kho (Shorts ≥ 7 ngày, video dài theo lịch) | Thời gian và chi phí sản xuất mỗi video |
| 1. Trước YPP | Giờ xem video dài mỗi tuần | Tỉ lệ giữ chân (%), sub ròng, giờ xem 7 ngày đầu của từng video |
| 2. Sau YPP | Doanh thu ước tính mỗi tuần | RPM theo trụ cột và theo series, giờ xem |

## 5. Ranh giới không bao giờ vượt để kiếm tiền
- Không tạo tương tác ảo. Không dùng proxy hay khai cư trú ở Mỹ. Không tải lại nội dung của người khác.
- Không làm video rập khuôn hàng loạt: mỗi video có hook, cấu trúc và hình ảnh riêng (chính sách "inauthentic content").
- Không bịa dữ kiện. Không giật tít sai sự thật.
- Không tải video lên bằng API khi dự án chưa qua audit (video sẽ bị khóa Riêng tư vĩnh viễn).
- Chi tiết: `.claude/skills/hoang-dung-clay-lapis-studio/references/policy-guardrails.md`.

## 6. Vòng phát triển liên tục
Tìm (radar xu hướng + số liệu kênh) → chọn (kho ý tưởng có bằng chứng) → làm (viết, dựng, đóng gói) → đăng → đo (báo cáo 7 ngày) → học (video thắng, quy luật) → tìm tiếp.
Chi tiết: `references/analytics-loop.md` và `references/autopilot.md`.

## 7. Ai được đổi gì
| File | Ai đổi | Khi nào |
|---|---|---|
| `MISSION.md` | Chỉ anh | Khi anh muốn đổi mục tiêu |
| `PLAN.md` | AI tự đổi theo số liệu, ghi lý do vào decisions-log (anh giao quyền 22/11/2026) | Đổi nhịp đăng, đổi trụ cột, lập chặng mới |
| `TASKS.md` / `state/tasks.json` | AI, qua `tasks.py` | Liên tục |
| `series/` | AI, qua `series.py` | Theo `series-playbook.md` |
| `ideas/IDEA_BANK.md`, `analytics/` | AI | Theo `analytics-loop.md` |
| `logs/` (nhật ký lịch sử) | Chỉ `tasks.py` ghi thêm | Không ai sửa hay xóa |
