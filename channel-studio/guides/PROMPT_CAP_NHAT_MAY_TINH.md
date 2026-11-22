# Lời nhắn cho phiên Claude Code trên máy anh: cập nhật hệ thống ICYFOX mới (22/11/2026)

**Cách dùng:**
1. Mở Claude Code trong thư mục `C:\Users\Admin\HDRE AI\ClayLapis\OpenMontage`.
2. Dán nguyên khối dưới đây.
3. Khi phiên báo đã kéo bản mới về, **thoát Claude Code (gõ `/exit`) rồi mở lại trong đúng thư mục đó** để bật 3 hook nhắc việc.
4. Dán lại khối này một lần nữa, để phiên làm tiếp từ bước 4.

```
Cập nhật hệ thống ICYFOX mới từ GitHub và làm thẻ T-018. Dùng skill hoang-dung-clay-lapis-studio. Làm đúng thứ tự, không bỏ bước, không báo xong khi chưa kiểm chứng.

1. LƯU VIỆC DỞ TRƯỚC: nếu git status có thay đổi chưa lưu, chạy
   python .claude/skills/hoang-dung-clay-lapis-studio/scripts/session_end.py -m "Lưu việc dở trước khi cập nhật" --trailer "<dòng ghi công của phiên này>"
   Nếu push bị từ chối: git fetch origin ccr-6640cec8-2anthl && git merge --no-edit FETCH_HEAD, xử lý xung đột giữ cả hai phía, rồi chạy lại. Không dùng --force.

2. KÉO BẢN MỚI: bash .claude/skills/hoang-dung-clay-lapis-studio/scripts/session_start.sh
   Kiểm tra commit mới nhất là a0e4add hoặc mới hơn (git log --oneline -3).
   Cài thư viện nếu thiếu: python -m pip install requests pytest

3. BẬT HOOK: file .claude/settings.json mới có 3 hook (SessionStart, UserPromptSubmit, Stop).
   Báo tôi thoát Claude Code (/exit) rồi mở lại trong thư mục OpenMontage. Dừng ở đây, chờ tôi mở lại.

4. KIỂM HOOK (sau khi mở lại):
   - Đầu phiên phải thấy khối "=== ICYFOX: nhắc tự động đầu phiên" (mục tiêu, kế hoạch, việc hôm nay).
   - Chạy thử: echo '{}' | bash .claude/skills/hoang-dung-clay-lapis-studio/scripts/hooks/run.sh prompt
   - Chạy: python -m pytest -q -p no:cacheprovider .claude/skills/hoang-dung-clay-lapis-studio/scripts/tests   (phải đạt 7/7)
   - Nếu hook không chạy trên Windows (Git Bash, đường dẫn có khoảng trắng): xem /hooks hoặc chạy claude --debug, sửa lệnh trong .claude/settings.json cho chạy được, kiểm lại, rồi lưu git. Ghi lỗi nguyên văn vào nhật ký.

5. ĐỌC: channel-studio/MISSION.md, PLAN.md, HANDOFF.md, TASKS.md, .claude/skills/hoang-dung-clay-lapis-studio/references/work-contract.md và references/autopilot.md.

6. LÀM THẺ T-018: python .claude/skills/hoang-dung-clay-lapis-studio/scripts/tasks.py start T-018 --owner claude-local
   - Sửa lời nhắn của tác vụ icyfox-san-xuat-9h-17h (file ~/.claude/scheduled-tasks/icyfox-san-xuat-9h-17h/SKILL.md, hoặc nơi app Claude desktop lưu tác vụ) thành nguyên văn lời nhắn trong references/autopilot.md §8. Giữ nguyên giờ chạy 09:00 và 17:00.
   - Sửa tác vụ icyfox-bao-cao-tuan-cn-9h: dùng python .claude/skills/hoang-dung-clay-lapis-studio/scripts/research/yt_analytics_report.py, ghi vào channel-studio/analytics/reports/<ngày>/, rồi làm tiếp theo references/analytics-loop.md §3. Giữ nguyên giờ Chủ nhật 09:00.
   - Kiểm 2 tác vụ chạy trong thư mục OpenMontage, để hook có hiệu lực.
   - KHÔNG tạo thêm tác vụ mới. KHÔNG tạo tác vụ trên cloud.
   - Đọc lại 2 file tác vụ để xác nhận nội dung đã đổi.

7. BÁO XONG ĐÚNG QUY TẮC (work-contract.md §3):
   python .claude/skills/hoang-dung-clay-lapis-studio/scripts/tasks.py done T-018 --evidence channel-studio/HANDOFF.md .claude/settings.json --summary "..." --component "Kéo bản mới :: ... :: ... :: ..." --component "Hook :: ... :: ... :: ..." --component "Tác vụ sản xuất :: ... :: ... :: ..." --component "Tác vụ báo cáo :: ... :: ... :: ..." --remaining "..."
   (Mỗi component gồm 4 trường: Tên :: Kết quả cụ thể :: Cách đã kiểm chứng :: Bằng chứng. Đường dẫn bằng chứng phải tồn tại trong repo. File tác vụ nằm ngoài repo thì chép phần lời nhắn đã sửa vào HANDOFF mục "Tự động hóa" và dùng HANDOFF làm bằng chứng.)
   Cập nhật HANDOFF, rồi chạy session_end.py để đẩy lên nhánh ccr-6640cec8-2anthl.

8. TRẢ LỜI TÔI theo khung KẾT LUẬN / CHI TIẾT / DẪN CHỨNG / BƯỚC TIẾP THEO, kèm bảng Thành phần | Kết quả | Cách kiểm chứng | Bằng chứng. Phần nào chưa xong thì ghi rõ "CHƯA XONG – lý do". Sau đó chạy autopilot.py và làm tiếp việc GẤP đầu tiên. Lưu ý: thẻ T-019, Phần 1 kịch bản 002 hỏng QA vì chỉ có 753 từ, không phải 1.270 như file ghi.
```
