# Render nhanh trên máy của anh

Dùng khi video đã duyệt xong phân cảnh và tài nguyên, và anh muốn xuất MP4 bằng máy tính của mình (thư mục `C:\Users\Admin\HDRE AI\ClayLapis`), không render trên cloud. Các cờ lệnh dưới đây lấy từ `hyperframes/skills/hyperframes-cli/references/preview-render.md`.

## 1. Chuẩn bị gói dựng (phía tôi, trước khi bàn giao)
- Toàn bộ dự án HyperFrames của video nằm trong `channel-studio/videos/NNN-slug/render/`, gồm: `index.html`, thư mục `compositions/` chia theo chương, và thư mục `assets/`.
- **Giọng đọc:** lưu thành MP3 theo từng đoạn hoặc từng chương, mỗi file dưới 20 MB. Một file WAV 40 phút nặng hơn 100 MB nên không đưa lên git được.
- **Ảnh:** JPG đã nén, cạnh dài khoảng 2.560 px trở xuống. **Nhạc:** MP3.
- Chạy `npx hyperframes lint` và `npx hyperframes check` trên cloud. Phải đạt cả hai trước khi bàn giao.
- **Dung lượng:** GitHub chặn file trên 100 MB, và `session_end.py` tự loại các file trên 95 MB. Nếu cả gói vượt khoảng 300 MB thì chuyển qua Google Drive (`GDRIVE_REFRESH_TOKEN`), không đưa lên git.

## 2. Các bước trên máy anh
1. Mở Claude Code Local tại thư mục ClayLapis, gõ "làm tiếp". Script mở phiên sẽ `git pull` nhánh `ccr-6640cec8-2anthl` về.
2. Lần đầu dùng, kiểm tra máy:
   ```
   cd "C:\Users\Admin\HDRE AI\ClayLapis\OpenMontage\channel-studio\videos\NNN-slug\render"
   npx hyperframes doctor
   ```
3. **Bản nháp** để xem nhanh nhịp và hình:
   ```
   npx hyperframes render --quality draft --output draft.mp4
   ```
4. **Bản cuối:**
   ```
   npx hyperframes render --quality delivery --fps 30 --gpu --output final.mp4
   ```
   - `--gpu`: dùng card đồ họa để nén video (NVIDIA NVENC, Intel QSV, AMD…). Nếu báo lỗi GPU thì bỏ cờ này.
   - Giữ **30 fps**. Dùng 60 fps thì thời gian render tăng gấp đôi mà phim tài liệu không cần.
   - `--workers`: mặc định là `auto`. Mỗi worker mở một Chrome, tốn khoảng 256 MB RAM. Máy 16 GB RAM có thể thử `--workers 6`. Máy ít RAM thì giảm số này.
5. **Video dài (35–40 phút): render từng chương rồi ghép.** Chương nào lỗi chỉ cần render lại chương đó:
   ```
   npx hyperframes render -c compositions/ch01.html --quality delivery --gpu -o out/ch01.mp4
   ...
   (tạo file list.txt, mỗi dòng: file 'out/ch01.mp4')
   ffmpeg -f concat -safe 0 -i list.txt -c copy final.mp4
   ```
6. **Kiểm tra trước khi tải lên YouTube:**
   - Đo thời lượng bằng `ffprobe final.mp4`. Phải khớp `data-duration` của composition.
   - Xem lướt toàn bộ video, kiểm tra không có khung hình đen và tiếng khớp hình.
   - Dòng thứ 2 của bản tóm tắt sau khi render cho biết thời gian từng công đoạn (capture, encode). Ghi các số này vào HANDOFF để lần sau ước tính trước.

## 3. Mẹo tăng tốc
- Cắm sạc. Đóng Chrome và các phần mềm nặng khác.
- Cập nhật driver card đồ họa nếu dùng `--gpu`.
- Không render cùng lúc trên cloud và trên máy cho cùng một video.
- Nếu `capture` chiếm phần lớn thời gian: giảm hiệu ứng nặng (blur, filter, 3D) trong composition. Nếu `encode` chậm: dùng `--gpu`.

## 4. Sau khi render
Tải `final.mp4` lên YouTube. Phần gói đăng (tiêu đề, mô tả, thumbnail, 11 phụ đề) nằm ở `channel-studio/videos/NNN-slug/package/`. Không đưa `final.mp4` lên git.
