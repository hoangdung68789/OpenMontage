# Làm việc cùng lúc với Codex (và các agent khác)

Anh dùng nhiều trợ lý AI trên cùng một repo, cùng nhánh `ccr-6640cec8-2anthl`: Claude Code (cloud và trên máy), OpenAI Codex. Mục tiêu là tăng tốc độ mà **không ghi đè lên việc của nhau**.

## Chia việc (đề xuất, anh có thể đổi)
| Agent | Mạnh ở việc gì | Giao việc gì |
|---|---|---|
| **Claude** (trưởng dự án) | Nghiên cứu, phân tích, kịch bản, giữ các bước duyệt, giao tiếp với anh | Phân tích đối thủ, kế hoạch, kịch bản, phân cảnh, gói đăng, báo cáo tuần, cập nhật HANDOFF và Notion |
| **Codex** (kỹ thuật) | Viết và sửa mã, test, xử lý lỗi công cụ | Sửa lỗi `gemini_tts` (v1beta), viết script gắn phụ đề (`captions.insert`, `videos.update`), dựng composition HyperFrames theo phân cảnh đã duyệt, viết test cho script |

Bảng trên là NHẬN ĐỊNH. Sau 2 tuần, xem bên nào làm việc nào nhanh và đúng hơn rồi chỉnh.

## Quy tắc chống đụng nhau
1. **Mỗi việc chỉ một agent làm.**
   - Trước khi bắt đầu: chạy `session_start.sh` (kéo bản mới nhất), mở `channel-studio/HANDOFF.md`, xem bảng **"Ai đang làm gì"**.
   - Không nhận việc đang có agent khác giữ.
2. **Ghi tên khi nhận việc:** thêm 1 dòng vào bảng (agent, việc, file sẽ sửa, giờ bắt đầu), rồi lưu ngay bằng `session_end.py`.
3. **Khi làm xong:** xóa dòng đó, cập nhật "Việc tiếp theo", rồi lưu bằng `session_end.py`.
4. **Push bị từ chối** (agent khác vừa đẩy): `git fetch origin ccr-6640cec8-2anthl && git merge --no-edit FETCH_HEAD`, xử lý xung đột nếu có, rồi push lại. Không dùng `--force`.
5. **Không cùng lúc sửa** `HANDOFF.md`, `SKILL.md` hay cùng một file kịch bản. File chung thì sửa nhỏ và lưu ngay.

## Khóa API
- **Trên máy anh:** Claude và Codex đọc chung file `OpenMontage/.env`. Git bỏ qua file này, `session_end.py` cũng tự loại các file `.env` ra khỏi commit.
- **Codex cloud** (chạy trên máy chủ của OpenAI): khóa phải nhập trong cài đặt môi trường của Codex. Không dán vào chat.
- **Không đưa khóa vào file nào trong repo.** `session_end.py` quét khóa và dừng commit nếu phát hiện.

## Lưu ý về dữ liệu
Codex đọc toàn bộ repo, tức là mã nguồn và tài liệu kênh được gửi cho OpenAI xử lý. Repo hiện không chứa khóa hay dữ liệu cá nhân nhạy cảm. Giữ nguyên như vậy.
