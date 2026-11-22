# Đơn audit API YouTube: bỏ bước anh kéo thả MP4

**Mục đích:** khi Google duyệt audit, AI tự tải video lên và hẹn giờ (`yt_publish.py upload`), anh không phải kéo thả nữa.
**Lý do phải audit:** video tải lên qua API từ dự án chưa audit bị khóa Riêng tư, không kháng nghị được, không kiếm tiền được ([YouTube Help 7300965](https://support.google.com/youtube/answer/7300965)).
**Form nộp:** https://support.google.com/youtube/contact/yt_api_form (đã đọc trường của form ngày 22/11/2026; mục 6 của form chưa đọc được).
**Thời gian duyệt:** Google không ghi ([trang audit](https://developers.google.com/youtube/v3/guides/quota_and_compliance_audits)). Duyệt hay không: [Chưa xác minh].

## Anh cần làm (khoảng 30 phút, một lần)
1. **Đưa 3 trang trong `site/` lên mạng** (cần link https công khai). AI làm được bằng GitHub Pages nếu anh đồng ý tạo một repo công khai chỉ chứa 3 trang này.
2. **Quay màn hình 1–2 phút** (form bắt buộc với công cụ nội bộ, không có tài khoản demo): chạy `yt_publish.py upload` với 1 clip thử 10 giây, rồi mở YouTube Studio thấy video đã lên và có gói đăng. Clip thử sẽ bị khóa Riêng tư vì chưa audit; Google ghi rõ trường hợp này **không bị gậy** (Help 7300965). Đưa video quay màn hình lên YouTube ở chế độ Không công khai, lấy link.
3. **Chụp 4 ảnh:** trang chính sách riêng tư; trang chủ có link chính sách; màn hình đồng ý Google (consent screen) lúc ủy quyền; trang Google quản lý quyền truy cập (để chứng minh thu hồi được).
4. **Điền form** theo bảng dưới (chép phần tiếng Anh), thay các ô `[ANH ĐIỀN]`, bấm gửi.
5. **Khi Google báo duyệt:** thêm dòng `YT_AUDIT_APPROVED=1` vào `.env`. Từ đó AI tự tải lên.

## Bảng trả lời form (chép nguyên phần tiếng Anh)

| Mục form | Trả lời |
|---|---|
| Request Type | Complete a compliance audit to request for additional quota |
| Applying as | As an individual user |
| Full Legal Name | `[ANH ĐIỀN: họ tên theo giấy tờ]` |
| Organization's Legal Name | self |
| Primary Website | `[link trang index.html sau khi đưa lên]` |
| Legal address | `[ANH ĐIỀN: Other / Vietnam, địa chỉ]` |
| Category | Creator Tools and Services |
| Organization Size / Type | Independent Developer/Sole Proprietor |
| Primary Contact | `[ANH ĐIỀN: tên, email Google của kênh]` |
| Describe your work (100–5000 ký tự) | I run one YouTube channel, ICYFOX, that publishes long-form documentary storytelling (true history, survival, disasters, ancient world) in English. ICYFOX Publisher is a private command-line tool I use only for my own channel. It uploads my finished videos as Private, then sets the title, description, tags, thumbnail, caption files in 11 languages and a scheduled publish time that I chose. It also reads my own channel's analytics to plan future videos. Nobody else signs in to it; it is not offered to other users. |
| Target audience | Internal Users |
| Monetization of the API client | Free service (we do not charge users) |
| Google representative | No, I do not have a Google representative |
| How did you learn about the API | Google Developer Documentation |
| API Client Name | ICYFOX Publisher (không chứa chữ "YouTube": đúng luật form) |
| Name contains "YouTube"? | No |
| Primary Access URL | `[link trang index.html]` |
| Privacy Policy URL | `[link trang privacy.html]` |
| Terms of Service URL | `[link trang terms.html]` |
| Publicly accessible? | No |
| Demo account | Để trống. Ghi vào Special Instructions: Internal command-line tool for a single channel; no demo account. An end-to-end screencast is provided in Supporting Materials. |
| Number of projects | 1 |
| Google Cloud Project Number | `[ANH ĐIỀN: số dự án, xem console.cloud.google.com → trang chủ dự án]` |
| Use Case Category | Video Uploading & Account Management; Analytics & Reporting; Internal Company Tool |
| Requires Google sign-in (OAuth)? | Yes |
| Expected usage | Fewer than 1,000 requests/day |
| Ảnh bắt buộc | privacy.png, homepage.png, terms.png (hoặc PDF của terms.html) |
| Ảnh theo điều kiện | OAuth: consent screen + scopes + trang thu hồi quyền. Upload: link quay màn hình ở bước 2 (form ghi ảnh tĩnh không đủ) và có thể đính kèm file `yt_publish.py` (form chấp nhận "a complete, working upload script") |
| Quota: endpoints | youtube.videos.insert, youtube.videos.update, youtube.thumbnails.set, youtube.captions.insert |
| Total quota | No change / Default quota (10k quota points) |
| Justification | Up to 2 uploads per day for one channel. Each video: 1 insert, 1 update, 1 thumbnail, 11 caption tracks (about 4,600 units). Default quota is enough; we only need uploads to be allowed to be public after review. |

Chọn "No change / Default quota": kênh đăng tối đa 2 video mỗi ngày, hạn mức mặc định đủ dùng (100 lượt `videos.insert` mỗi ngày). Google có chấp nhận đơn audit chỉ để mở khóa mà không xin thêm hạn mức hay không: [Chưa xác minh].

## Tool đã đáp ứng luật nhà phát triển (Developer Policies, đọc 22/11/2026)
- Chỉ dùng 1 dự án Google Cloud cho 1 công cụ. Không đưa khóa vào mã nguồn công khai (khóa nằm trong `.env`, git bỏ qua).
- Tải lên ở chế độ Riêng tư, chỉ hẹn giờ công khai theo ngày chủ kênh đã chốt trong `PLAN.md`. Không tự thêm chữ vào mô tả.
- Chỉ dùng phạm vi quyền đang cần: `youtube.force-ssl` (đã gồm quyền tải lên) và `yt-analytics.readonly`.
- Thu hồi quyền: trang Google https://myaccount.google.com/permissions; chính sách riêng tư ghi cách thu hồi và xóa dữ liệu trong 7 ngày.
