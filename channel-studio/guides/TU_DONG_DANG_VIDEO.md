# AI có tự đăng video lên kênh ICYFOX được không?

Tra ngày 22/11/2026. Phân loại theo quy tắc dẫn chứng: SỰ THẬT (có nguồn) / NHẬN ĐỊNH / GIẢ THUYẾT CẦN THỬ.

## 1. Vì sao hiện tại anh vẫn phải tự kéo thả file
- **SỰ THẬT:** "For videos that have been locked as private due to upload via an unverified API service, you will not be able to appeal." Cách khắc phục YouTube đưa ra: tải lại qua dịch vụ API đã xác minh hoặc qua app/web YouTube. Dự án API cũng "can also apply for an API audit". Nguồn: [YouTube Help 7300965](https://support.google.com/youtube/answer/7300965).
- **SỰ THẬT:** Điều khoản YouTube cấm "access the Service using any automated means (such as robots, botnets or scrapers)", trừ công cụ tìm kiếm công khai, hoặc khi có văn bản cho phép trước của YouTube. Nguồn: [YouTube Terms of Service](https://www.youtube.com/static?template=terms).
- **Chưa rõ (cần thử):** kết quả tìm kiếm cho thấy tài liệu videos.insert bản tiếng Anh hiện tại có thể đã bỏ câu "bị giới hạn ở chế độ riêng tư", trong khi bản cũ và trang 7300965 vẫn ghi giới hạn này. Phiên cloud không mở được developers.google.com nên chưa đọc được bản gốc. Nguồn: [kết quả tìm kiếm trỏ tới trang videos.insert](https://developers.google.com/youtube/v3/docs/videos/insert), [Quota and Compliance Audits](https://developers.google.com/youtube/data/guides/quota_and_compliance_audits).

## 2. Các phương án
| # | Phương án | AI tự đăng hoàn toàn? | Chi phí | Rủi ro | Anh phải làm |
|---|---|---|---|---|---|
| A | **Thử thật 1 lần** (GIẢ THUYẾT CẦN THỬ): tải 1 clip thử 5 giây qua API của dự án ICYFOX ở chế độ "Không công khai", đọc lại trạng thái, rồi xóa | Nếu YouTube không ép về "Riêng tư" thì **có, dùng được ngay** | Hạn mức API | Nếu bị khóa: chỉ clip thử bị khóa, không bị gậy (trang 7300965 nói không có gậy) | Trả lời "thử" để cho phép |
| B | **Audit API của chính anh** (cách chính thức): nộp form [YouTube API Services – Audit and Quota Extension](https://support.google.com/youtube/contact/yt_api_form) | Có, sau khi được duyệt | Miễn phí | Không công bố thời gian xét; có thể bị từ chối | Cần trang web https + trang chính sách quyền riêng tư + điều khoản + video quay màn hình toàn bộ quá trình tải lên (form yêu cầu). AI soạn sẵn hết, anh chỉ nộp |
| C | **Dịch vụ trung gian đã có API được duyệt** (Upload-Post, Buffer, Ayrshare…) | Theo quảng cáo của họ là có | Upload-Post: miễn phí 10 video/tháng, 24 USD/tháng gói Basic; Ayrshare: từ 149 USD/tháng (theo [bài so sánh](https://www.blotato.com/blog/social-media-api), [Upload-Post](https://www.upload-post.com/youtube-api/), [Buffer](https://buffer.com/resources/best-social-media-apis/)). **Cần kiểm lại trên trang của từng hãng** | Phải cấp quyền kênh cho bên thứ ba. Các nguồn trên đều là blog của chính hãng | Chọn dịch vụ, đăng ký, kết nối kênh (việc quan trọng: tiền + quyền tài khoản) |
| D | AI điều khiển trình duyệt bấm tải lên trong Studio | Có | 0 | **Trái điều khoản "automated means"**, có thể mất kênh | **Không làm** |
| E | Giữ như hiện tại: anh kéo thả, AI làm phần còn lại | Gần như | 0 | Không | Khoảng 10 phút mỗi tuần |

## 3. Khuyến nghị (NHẬN ĐỊNH)
1. **Làm A trước.** Một lần thử là biết chắc, rủi ro thấp nhất. Nếu đạt, sửa `yt_publish.py` để tự tải lên, hết phải kéo thả.
2. Nếu A bị khóa: **làm B và E song song**. Nộp audit, trong lúc chờ thì anh vẫn kéo thả.
3. **C** chỉ dùng khi B bị từ chối, và phải được anh chốt vì có chi phí và phải giao quyền kênh.
4. **Không bao giờ dùng D.** Kênh là tài sản chính (MISSION §3: an toàn kênh đứng đầu).

## 4. KẾT QUẢ THỬ THẬT (22/11/2026, anh cho phép)
Script: `.claude/skills/hoang-dung-clay-lapis-studio/scripts/yt_upload_probe.py`. Số liệu gốc: `research/2026-11-22-api-upload-test/result.json`.
| Giờ (VN) | Sự kiện | Chế độ hiển thị | Trạng thái |
|---|---|---|---|
| 23:50:47 | Tải clip đen 5 giây (15 KB) qua `videos.insert`, yêu cầu "Không công khai". Token chỉ có quyền `youtube.force-ssl` + `yt-analytics.readonly` | **unlisted** (Không công khai) | uploaded |
| 23:51:24 | YouTube xử lý xong | **unlisted** | processed, không có failureReason hay rejectionReason |
| 23:52:24 | Đọc lại lần cuối | **unlisted** | processed |
| 23:52:26 | Xóa video `hS2xk7efOCA` | — | HTTP 204, đọc lại: không còn video |

**Kết luận (SỰ THẬT trong phạm vi đã thử):** video tải lên qua API của dự án ICYFOX **không bị ép về Riêng tư**, cả lúc tải lẫn sau khi xử lý xong.
**Giới hạn (NHẬN ĐỊNH):**
- Chỉ quan sát được khoảng 1,5 phút sau khi xử lý xong.
- Trang trợ giúp 7300965 vẫn mô tả việc khóa, nên không loại trừ được trường hợp khóa xảy ra muộn hơn sau một lần rà soát.
- Chưa thử chế độ hẹn giờ công khai (`publishAt`).

**Việc tiếp theo:** thử 24 giờ (clip Không công khai, sau 24 giờ đọc lại rồi xóa). Đạt thì thêm chức năng tự tải lên vào `yt_publish.py`. Short đầu tiên (01/12) sẽ dùng chế độ hẹn giờ, kèm phương án dự phòng: anh kéo thả nếu video bị khóa.
