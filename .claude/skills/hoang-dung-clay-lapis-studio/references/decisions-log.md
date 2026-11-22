# Nhật ký quyết định (mới nhất ở cuối)

| Ngày | Quyết định | Lý do hoặc căn cứ |
|---|---|---|
| 22/11/2026 | Kênh mới, tiếng Anh, người xem Mỹ, giọng AI, phụ đề 11 ngôn ngữ (có tiếng Việt, dạng phụ đề bật/tắt chứ không in cứng lên hình) | Anh chọn. Giá quảng cáo phụ thuộc nơi người xem ở (YouTube Help) |
| 22/11/2026 | Ngách: lịch sử cổ đại và thần thoại, phim dài | Quét 7 ngách: ngách này có trung vị và tỉ lệ vượt trội cao nhất. Đã loại các ngách tài chính, sức khỏe, pháp lý, chính trị (chính sách AI persona) |
| 22/11/2026 | Không dùng proxy Mỹ hay AdsPower cho tài khoản kênh. Quốc gia cư trú khai Việt Nam | Chính sách YouTube về Country of residence, chống tương tác ảo |
| 22/11/2026 | Nhịp đăng: 4–8 video dài + 30–60 Shorts mỗi tháng | Chính sách inauthentic content. Số liệu tần suất đăng của ngách |
| 22/11/2026 | Tên kênh Clay & Lapis | Tra YouTube không thấy kênh trùng tên |
| 22/11/2026 | Video thử: Concept A "The Lost Lines" (Gilgamesh), HyperFrames, atelier, phương án Standard | Anh duyệt |
| 22/11/2026 | Kịch bản Phần 1 đã duyệt ("Five thousand years ago"). Phần 2 đã duyệt, bỏ S4.8. Thời lượng theo nội dung, 35–40 phút | Anh duyệt. Không độn chữ cho đủ giờ |
| 22/11/2026 | Theo dõi bằng Notion. Đồng ý tạo tác vụ hẹn giờ sau khi video thử đạt | Anh đồng ý |
| 22/11/2026 | YouTube OAuth dùng Personal mode + OAuth Playground. Quyền Drive xin riêng | Anh không publish được ứng dụng External. Google không cho xin quyền YouTube chung với drive.file |
| 22/11/2026 | Lưu toàn bộ lên GitHub: repo OpenMontage, nhánh `ccr-6640cec8-2anthl`, thư mục `channel-studio/`. Có skill này | Anh đồng ý |
| 22/11/2026 | Kênh YouTube **giữ tên ICYFOX**. "Clay & Lapis" là tên dự án và bộ nhận diện | Anh chọn. NHẬN ĐỊNH: tên ICYFOX không gợi ngách lịch sử, nên cần banner, câu định vị và tên danh sách phát để bù |
| 22/11/2026 | **Mở rộng chủ đề thành 5 trụ cột kể chuyện** (bí ẩn Trái Đất, sinh tồn và thám hiểm, chiến tranh, thảm họa, thế giới cổ đại và thần thoại) | Anh yêu cầu. Quét 12 nhóm chủ đề. Kênh Yesterday: 14 tháng tuổi, 169K sub, trung vị 617K view (`content-pillars.md`) |
| 22/11/2026 | **Thêm tiêu chuẩn làm việc** (SKILL.md mục 0, `request-playbooks.md`) và đặt YouTube Data API làm mặc định khi phân tích đối thủ | Anh phản ánh phiên phân tích @WartimeStories làm thiếu và sai hướng |
| 22/11/2026 | **Nhịp đăng: tối thiểu 1, tối đa 2 video mỗi ngày, tổng 30–60 video mỗi 30 ngày.** Cách chia: 8 video dài (thứ Ba, thứ Sáu) + khoảng 38 Shorts. Shorts bắt đầu từ 01/12/2026. Lên 2 video dài mỗi tuần từ 01/01/2027 nếu đạt cổng ngày 28/12 | Anh yêu cầu. Khớp với quyết định 4–8 video dài + 30–60 Shorts. Không làm video dài mỗi ngày vì chính sách inauthentic content và số liệu đối thủ (đăng gấp 4 lần thì trung vị giảm từ 503K xuống 313K). Chi tiết: `research/2026-11-22-wartimestories/KE_HOACH_90_NGAY.md` |
| 22/11/2026 | Khóa API trên máy local để trong `OpenMontage/.env` (theo mẫu `channel-studio/config/api_keys.env.example`). Trên cloud dùng Network secrets và biến môi trường | Anh yêu cầu file cấu hình. OpenMontage tự đọc `.env` |
