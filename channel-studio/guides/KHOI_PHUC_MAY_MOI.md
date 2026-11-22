# Đổi máy tính: khôi phục toàn bộ dữ liệu kênh ICYFOX

Gần như mọi thứ nằm trên mạng, máy mới chỉ cần tải về. Có **4 thứ không nằm trên GitHub** (bảng dưới), phải giữ lại hoặc làm lại.
Script tự động: `.claude/skills/hoang-dung-clay-lapis-studio/scripts/restore_machine.sh`. Đã chạy thử từ thư mục trống ngày 22/11/2026: 82 giây, API đều OK, 8/8 kiểm thử đạt.

## 1. Dữ liệu nằm ở đâu
| Thứ | Nằm ở | Máy mới có tự có không |
|---|---|---|
| Kịch bản, kế hoạch, sổ việc, nhật ký, series, số liệu, skill, hook | GitHub `hoangdung68789/OpenMontage`, nhánh `ccr-6640cec8-2anthl` | **Có**, tải về bằng script |
| 15 repo công cụ (hyperframes, remotion…) | GitHub `hoangdung68789/...` | **Có**, script tải về |
| Skill trong tài khoản claude.ai | Tài khoản claude.ai của anh | **Có**, khi đăng nhập |
| Bảng Notion, kênh YouTube, dự án Google Cloud | Trên mạng | **Có** |
| **Khóa API** (`OpenMontage\.env`) | Chỉ trên máy cũ (cố ý không đưa lên GitHub) | **KHÔNG**: chép từ bản lưu, hoặc lấy lại khóa |
| **2 tác vụ hẹn giờ** (sản xuất 09:00 + 17:00, báo cáo Chủ nhật 09:00) | App Claude desktop trên máy cũ | **KHÔNG**: tạo lại (lời nhắn có trên GitHub) |
| **File lớn**: MP4, âm thanh, ảnh đã tải (`OpenMontage\projects\*\assets`, `renders`) | Ổ cứng máy cũ | **KHÔNG**: chép bằng USB/Drive, hoặc để AI làm lại |
| Lịch sử chat của các phiên trên máy cũ | `C:\Users\<tên>\.claude\` trên máy cũ | Không cần: mọi trạng thái đã nằm trong HANDOFF, TASKS, nhật ký |

## 2. Trước khi bỏ máy cũ (khoảng 10 phút)
1. Mở Claude Code trong thư mục OpenMontage, dán:
   ```
   Chuẩn bị đổi máy: chạy session_end.py để đẩy mọi thay đổi lên GitHub, rồi báo tôi commit cuối cùng và git status sạch chưa.
   ```
2. **Sao lưu file khóa** `C:\Users\Admin\HDRE AI\ClayLapis\OpenMontage\.env`: chép vào USB, hoặc dán từng khóa vào trình quản lý mật khẩu. **Không** đưa lên GitHub, không dán vào chat.
3. Nếu có video đã render chưa đăng: chép thư mục `OpenMontage\projects` và các file MP4 sang USB hoặc Google Drive.
4. Trong app Claude desktop, mục Scheduled: **tắt 2 tác vụ ICYFOX** trên máy cũ, để không chạy trùng với máy mới.

## 3. Trên máy mới
### A. Anh làm (khoảng 10 phút)
1. Cài **Git for Windows**: https://git-scm.com/download/win (cứ bấm Next).
2. Cài **app Claude desktop**: https://claude.ai/download, đăng nhập đúng tài khoản cũ.
3. Tạo thư mục trống, ví dụ `C:\Users\<tên>\HDRE AI\ClayLapis`.
4. Trong app Claude: tab **Code** → chọn **Local** → **Open folder** → chọn thư mục ở bước 3 → dán lời nhắn ở mục B.
5. Khi AI báo "đã tạo OpenMontage\.env": mở file bằng Notepad, dán khóa từ bản sao lưu (hoặc lấy lại theo mục 4), rồi lưu.
6. Khi AI bảo thoát: gõ `/exit`, mở lại tab Code ở thư mục `ClayLapis\OpenMontage`, dán lời nhắn mục B một lần nữa.

### B. Lời nhắn cho Claude Code trên máy mới
```
Đây là máy mới của tôi cho kênh ICYFOX. Khôi phục toàn bộ dữ liệu, làm đúng thứ tự, hỏi tôi trước khi cài phần mềm hệ thống, không bao giờ in hay xin khóa API trong chat.
1. Nếu thư mục hiện tại chưa có OpenMontage: git clone -b ccr-6640cec8-2anthl https://github.com/hoangdung68789/OpenMontage.git OpenMontage (nếu GitHub đòi đăng nhập thì chờ tôi đăng nhập trên trình duyệt).
2. Chạy bằng Git Bash từ thư mục chứa OpenMontage: bash OpenMontage/.claude/skills/hoang-dung-clay-lapis-studio/scripts/restore_machine.sh
3. Phần mềm nào script báo THIẾU (Python, Node.js, ffmpeg): hỏi tôi rồi cài bằng winget (kiểm tên gói bằng winget search trước), mở lại terminal, chạy lại script.
4. Nếu script vừa tạo OpenMontage/.env từ mẫu: mở file đó bằng Notepad cho tôi (notepad "OpenMontage/.env"), chờ tôi dán khóa và báo xong, rồi chạy lại script để kiểm API. Không đọc, không in nội dung file.
5. Bảo tôi thoát Claude Code và mở lại trong thư mục OpenMontage để bật 3 hook nhắc việc. Sau khi mở lại: kiểm đầu phiên có khối "ICYFOX: nhắc tự động đầu phiên".
6. Tạo lại 2 tác vụ hẹn giờ trên app Claude desktop, chạy trong thư mục OpenMontage: (a) sản xuất 09:00 và 17:00 mỗi ngày, lời nhắn nguyên văn ở .claude/skills/hoang-dung-clay-lapis-studio/references/autopilot.md §8; (b) báo cáo Chủ nhật 09:00 theo references/automation.md. Không tạo thêm tác vụ nào khác.
7. Kết nối Notion cho Claude Code nếu phiên chưa có công cụ Notion, rồi thử đọc bảng "Clay & Lapis – Video Pipeline".
8. Ghi kết quả bằng tasks.py (add --start rồi done với --component cho từng bước: repo, phần mềm, khóa, hook, tác vụ hẹn giờ, Notion), cập nhật HANDOFF mục "Tự động hóa" (máy mới), chạy session_end.py.
9. Trả lời tôi bằng bảng Thành phần | Kết quả | Cách kiểm chứng | Bằng chứng. Phần nào chưa xong ghi rõ "CHƯA XONG – lý do".
```

## 4. Nếu mất file khóa `.env`
Mỗi khóa lấy lại được, theo `channel-studio/config/HUONG_DAN_KHOA_API.md`:
| Khóa | Lấy lại ở đâu |
|---|---|
| `GEMINI_API_KEY` | aistudio.google.com → Get API key (tạo khóa mới) |
| `YT_CLIENT_ID`, `YT_CLIENT_SECRET` | Google Cloud Console, dự án 979474479924 → Credentials (client OAuth cũ vẫn dùng được) |
| `YT_REFRESH_TOKEN` | Xin lại bằng OAuth Playground như lần đầu (quyền `youtube.force-ssl` + `yt-analytics.readonly`) |
| `ELEVENLABS_API_KEY` | elevenlabs.io → Developers → API Keys (khóa bắt đầu bằng `sk_`) |
| `OPENAI_API_KEY` | platform.openai.com → API keys |
| `GDRIVE_REFRESH_TOKEN` (nếu đã cấu hình) | Xin lại bằng OAuth Playground, quyền `drive.file` riêng (không xin chung với quyền YouTube) |
Khóa cũ trên máy cũ nên thu hồi (xóa) sau khi có khóa mới, nhất là khi máy cũ đem bán hoặc cho người khác.

## 5. Dấu hiệu khôi phục đạt
- `restore_machine.sh` mục 6: Gemini, ElevenLabs, OpenAI, YouTube OAuth, Kênh ICYFOX, Analytics đều **OK**. Mục 7: **8 passed**.
- Đầu mỗi phiên mới hiện khối "=== ICYFOX: nhắc tự động đầu phiên".
- `python .claude/skills/hoang-dung-clay-lapis-studio/scripts/tasks.py list` hiện đúng sổ việc. `autopilot.py` hiện việc hôm nay.
- App Claude desktop có đúng 2 tác vụ ICYFOX. Máy cũ đã tắt tác vụ.
