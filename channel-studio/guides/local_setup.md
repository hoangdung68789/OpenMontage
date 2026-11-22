# Chạy kênh Clay & Lapis bằng Claude Code trên máy tính của anh (không qua cloud)

Tài liệu này có 2 phần: phần A anh tự làm, phần B anh giao cho Claude Code trên máy làm.

## Khác biệt so với phiên cloud
| | Cloud (đang dùng) | Máy của anh (local) |
|---|---|---|
| Máy phải bật | Không | **Có**, trong suốt thời gian làm việc |
| Khóa và token | Lưu trong cài đặt môi trường, proxy tự gắn | **Biến môi trường trên máy anh**, anh tự đặt |
| Mạng | Chỉ các host đã mở | Không giới hạn |
| yt-dlp lấy số liệu từng video | Bị YouTube chặn vì nghi bot | Mạng nhà ít bị chặn hơn [nhận định, cần thử] |
| Render video | Chạy trên máy cloud | Chạy bằng CPU của máy anh |
| Blender (blender-skills) | Không có | Dùng được nếu anh cài Blender |
| Tác vụ hẹn giờ tự động | Có | Vẫn tạo trên cloud. Phiên local chỉ chạy khi anh mở |
| Repo, skill, Notion | Như nhau: cùng nhánh GitHub `ccr-6640cec8-2anthl` | Như nhau |

**Lưu ý:** không làm cùng lúc ở cloud và ở máy local trên cùng nhánh. Mỗi lần mở phiên, `session_start.sh` kéo bản mới nhất về. Đóng phiên thì đẩy lên.

---

## A. Việc anh tự làm (khoảng 10–15 phút)

1. **Cài Git**
   - Windows: tải tại https://git-scm.com/download/win, cứ bấm Next để giữ mặc định. Git có kèm Git Bash, Claude Code dùng Git Bash để chạy lệnh.
   - macOS: mở Terminal, gõ `git --version`. Máy sẽ tự đề nghị cài công cụ cần thiết.
2. **Cài Claude Code**, chọn 1 trong 2 cách:
   - **Ứng dụng Claude Desktop (dễ nhất):** tải tại https://claude.ai/download → đăng nhập → tab **Code** → ở ô môi trường chọn **Local** → **Open folder** → chọn thư mục ở bước 3.
   - **Dòng lệnh:**
     - Windows (PowerShell): `irm https://claude.ai/install.ps1 | iex`
     - macOS: `curl -fsSL https://claude.ai/install.sh | bash`

     Sau đó vào thư mục ở bước 3 và gõ `claude`.
3. **Tạo một thư mục trống** cho kênh: Windows `C:\ClayLapis`, macOS `~/ClayLapis`. Cả 16 repo sẽ nằm cạnh nhau trong thư mục này.
4. **Đặt khóa vào biến môi trường của máy.** Anh tự gõ trong cửa sổ PowerShell hoặc Terminal riêng. **Không dán khóa vào khung chat với Claude.**
   - Windows (PowerShell), mỗi dòng một lệnh, thay phần trong ngoặc kép bằng giá trị thật:
     ```
     setx GEMINI_API_KEY "AIza..."
     setx ELEVENLABS_API_KEY "sk_..."
     setx YT_CLIENT_ID "....apps.googleusercontent.com"
     setx YT_CLIENT_SECRET "GOCSPX-..."
     setx YT_REFRESH_TOKEN "1//0..."
     ```
   - macOS: thêm các dòng `export GEMINI_API_KEY="AIza..."` (và tương tự cho 4 biến còn lại) vào cuối file `~/.zshrc`.
   - Đặt xong, **đóng hẳn rồi mở lại** Claude Code để nó đọc biến mới.

## B. Câu lệnh đầu tiên dán cho Claude Code trên máy

```
Đây là máy local của tôi để làm kênh Clay & Lapis. Hãy clone repo hoangdung68789/OpenMontage (nhánh ccr-6640cec8-2anthl) vào thư mục hiện tại, rồi đọc channel-studio/guides/local_setup.md phần C và làm theo để cài đặt máy. Hỏi tôi trước khi cài phần mềm hệ thống.
```

---

## C. Hướng dẫn cho Claude Code trên máy (cài đặt)

Làm theo thứ tự. Hỏi anh trước khi cài phần mềm hệ thống. Không in giá trị của khóa ra màn hình.

1. **Clone 15 repo còn lại** vào cùng thư mục cha với OpenMontage, mỗi repo một thư mục cùng tên:
   yt-dlp, Agent-Reach, agent-skills, awesome-opus5-5-videos, blender-skills, CLI-Anything, motion-design-skill, hyperframes, remotion, three.js, GSAP, whisperX, seek-tune, replica-skill, gsap-skills.
   Tất cả của owner `hoangdung68789` (tên repo trên GitHub viết thường, ví dụ `agent-reach`, `cli-anything`, `gsap`, `whisperx`). Dùng `git clone --depth 50`. Clone repo riêng tư sẽ cần anh đăng nhập GitHub (Git Credential Manager mở trình duyệt).
2. **Phần mềm hệ thống** (kiểm tra trước, chỉ cài phần còn thiếu):
   | Phần mềm | Windows (winget) | macOS (Homebrew) |
   |---|---|---|
   | Python 3.11 trở lên | `winget install Python.Python.3.12` | `brew install python@3.12` |
   | Node.js 22 | `winget install OpenJS.NodeJS.LTS` | `brew install node@22` |
   | ffmpeg | `winget install Gyan.FFmpeg` | `brew install ffmpeg` |

   Tên gói winget và brew có thể đã thay đổi, nên kiểm lại bằng `winget search` hoặc `brew search` trước khi cài. Cài xong thì mở lại terminal.
3. **Thư viện Python** (từ thư mục cha):
   ```
   python -m pip install yt-dlp jsonschema requests google-auth google-auth-oauthlib google-api-python-client
   python -m pip install -r OpenMontage/requirements.txt
   ```
4. **Skill**
   - Skill có sẵn trong repo, ở `OpenMontage/.claude/skills/hoang-dung-clay-lapis-studio/`. Mở Claude Code trong thư mục OpenMontage là skill tự nạp.
   - Muốn dùng ở mọi thư mục thì chép thư mục skill đó vào `~/.claude/skills/`.
   - Nếu anh đăng nhập bằng tài khoản claude.ai đã lưu skill, skill cũng có thể tự có [chưa xác minh với phiên local].
5. **Notion:** nếu chưa có công cụ Notion trong phiên, hướng dẫn anh kết nối Notion cho Claude Code theo tài liệu MCP của Claude Code [chưa xác minh cách làm cụ thể].
6. **Kiểm tra:** từ thư mục OpenMontage, chạy bằng Git Bash trên Windows:
   ```
   bash .claude/skills/hoang-dung-clay-lapis-studio/scripts/session_start.sh
   ```
   Kết quả đạt:
   - Đủ 16 repo.
   - Gemini OK.
   - ElevenLabs OK (ghi rõ gói gì).
   - Thấy tên kênh.
   - Analytics OK.
7. **HyperFrames:** chạy `npx hyperframes --help` một lần để tải công cụ. Lần render đầu sẽ tải thêm trình duyệt headless.
8. **Báo anh** những gì đã cài, những gì còn thiếu. Từ đây làm việc theo skill `hoang-dung-clay-lapis-studio`. Đóng phiên bằng `python .claude/skills/hoang-dung-clay-lapis-studio/scripts/session_end.py -m "..."`. Push dùng tài khoản GitHub của anh.
