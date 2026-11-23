# Gói đăng và lịch đăng

## Thành phần một gói (lưu ở `channel-studio/videos/NNN-slug/package/`)
| File | Nội dung |
|---|---|
| `title.txt` | Tiêu đề tiếng Anh, dưới khoảng 70 ký tự. Dòng thứ 2 trở đi: 2 phương án dự phòng |
| `description.md` | Theo mẫu bên dưới |
| `tags.txt` | 10–15 từ khóa, cách nhau bằng dấu phẩy |
| `hashtags.txt` | 3 hashtag, đặt ở cuối mô tả |
| `subtitles/<lang>.srt` | 11 file: en (gốc), vi, es, pt-BR, hi, id, fr, de, ja, ko, ar. Mốc giờ lấy từ file giọng thật (cắt theo đoạn hoặc chạy speech-to-text) |
| `localizations.json` | Tiêu đề và mô tả dịch sang 10 ngôn ngữ, đúng dạng cho `videos.update` (`localizations`) |
| `thumbnail.png` (và `thumbnail_b.png`) | 1280×720, dưới 2 MB |
| `upload_checklist.md` | Checklist cho anh, ghi đúng tên nút |
| File video | Nằm trên Drive hoặc trong container. **Không đưa lên git** |

Tôi tự dịch phụ đề, không gọi API dịch. Tên riêng giữ nguyên dạng phiên âm quốc tế.

## Mẫu mô tả video
```
<2–3 câu tóm tắt, chứa từ khóa chính ngay câu đầu>

CHAPTERS
00:00 <Mở đầu>
02:20 Chapter 1 – ...
...

Sources: <tên các nguồn chính, không link>.   ← chỉ khi có nguồn tổng hợp; không có thì bỏ dòng này
Music: "<bài 1>", "<bài 2>" by <tác giả> (<nguồn>), licensed under CC BY 4.0 (http://creativecommons.org/licenses/by/4.0/)
<chỉ khi có ảnh/clip CC BY hoặc CC BY-SA: 1 dòng> Images: <tác giả> / <giấy phép>, via Wikimedia Commons

#history #mythology #<chủ đề>
```
- **Anh chốt 23/11/2026: mô tả gọn.** KHÔNG ghi danh sách nguồn có link (SOURCES); chỉ 1 dòng "Sources:" tổng hợp tên nguồn nếu có, không có thì bỏ, không ghi công ảnh public domain, không có đoạn "HOW WE MAKE VIDEOS"/cách làm video. Chỉ giữ dòng ghi công mà giấy phép bắt buộc: nhạc CC BY (Kevin MacLeod...) và ảnh CC BY/BY-SA nếu có. Nguồn vẫn lưu trong repo (kịch bản, `render/tools`, `_manifest.json`) để tự kiểm.
- Mốc chương bắt đầu từ `00:00`. Cần ít nhất 3 chương, mỗi chương dài từ 10 giây [theo quy định chapters của YouTube, cần kiểm lại khi dùng].

## Khai báo AI khi tải lên
Giọng tổng hợp đọc trên nền hình minh họa hoặc ảnh di vật thật thì theo hướng dẫn của YouTube không bắt buộc khai báo. Nhưng khai báo không ảnh hưởng người xem hay kiếm tiền, nên **chọn Yes nếu có bất kỳ hình AI nào**.

## Shorts
- Mỗi video dài cắt 3–5 Shorts dọc 9:16, dưới 60 giây. Mỗi Short là một khoảnh khắc hoàn chỉnh (một phát hiện, một ngộ nhận, một cảnh).
- Chữ ở 3 giây đầu là câu hook.
- Mô tả Short có link về video gốc (tính năng "Related video" trong Studio).
- Phụ đề chỉ có EN + VI để giữ hạn mức API.

## Lịch đăng (đã chốt 22/11/2026)
| Loại | Số lượng | Giờ Mỹ (ET) | Giờ VN (đến 13/03/2027: ET+12, từ 14/03/2027: ET+11) |
|---|---|---|---|
| Video dài | 1–2 mỗi tuần (thứ Ba, thứ Sáu) | 09:00 | 21:00, sau đó 20:00 |
| Shorts | 1–2 mỗi ngày | 12:00 và 18:00 | 00:00 và 06:00, sau đó 23:00 và 05:00 |

- Anh tải lên và chọn **Schedule** mỗi Chủ nhật.
- Sau 30 ngày, xem báo cáo "When your viewers are on YouTube" trong Analytics để chỉnh giờ đăng.

## Sau khi anh tải lên (gắn phụ đề và bản dịch)
1. Anh gửi link hoặc ID video, video đã đặt ngôn ngữ là English.
2. Đưa 11 file SRT lên bằng `captions.insert` (part=snippet; snippet: videoId, language, name; media là file .srt).
3. Gọi `videos.update` (part=localizations,snippet) với `defaultLanguage=en` và `localizations` lấy từ `localizations.json`.
4. Kiểm tra bằng `captions.list` và `videos.list`. Ghi kết quả vào Notion.
