---
name: hoang-dung-clay-lapis-studio
description: "Vận hành kênh YouTube ICYFOX (kể chuyện có thật: bí ẩn Trái Đất, sinh tồn và thám hiểm, chiến tranh, thảm họa, thế giới cổ đại và thần thoại; dự án Clay & Lapis). Gồm: phân tích đối thủ bằng YouTube Data API, kế hoạch, kịch bản, giọng đọc, dựng video bằng OpenMontage + HyperFrames, gói đăng, phụ đề, báo cáo. Dùng khi Dũng nhắc đến ICYFOX, Clay & Lapis, kênh YouTube, đối thủ, kịch bản, dựng video, hoặc khi làm tiếp việc trong channel-studio/."
---

# ICYFOX Studio: lối vào cho Codex và các agent khác

Bản gốc của skill này nằm ở **`.claude/skills/hoang-dung-clay-lapis-studio/`**, dùng chung với Claude Code. File này chỉ là lối vào cho Codex, để không phải giữ 2 bản nội dung.

Codex không có hook nhắc việc như Claude Code, nên **mỗi lần nhận việc** phải tự làm các bước sau:
0. Đọc `channel-studio/MISSION.md` (mục tiêu vĩnh viễn), `channel-studio/PLAN.md` (kế hoạch), `channel-studio/TASKS.md` (sổ việc) và `.claude/skills/hoang-dung-clay-lapis-studio/references/work-contract.md` (hợp đồng làm việc + QUY TẮC HOÀN THÀNH). Đặt biến `ICYFOX_AGENT=codex`.
1. Đọc toàn bộ `.claude/skills/hoang-dung-clay-lapis-studio/SKILL.md` và làm theo, đặc biệt **mục 0 "Tiêu chuẩn làm việc"**.
2. Đọc `.claude/skills/hoang-dung-clay-lapis-studio/references/multi-agent.md`: quy tắc làm việc cùng Claude, gồm bảng "Ai đang làm gì" trong HANDOFF.
3. Các script nằm ở `.claude/skills/hoang-dung-clay-lapis-studio/scripts/`: `session_start.sh`, `session_end.py`, `check_apis.py`, `research/yt_api_channel.py`…
4. Nhận việc: `python .claude/skills/hoang-dung-clay-lapis-studio/scripts/tasks.py start T-xxx --owner codex`. Xong việc: `tasks.py done T-xxx --evidence … --summary … --component "Tên :: Kết quả :: Cách kiểm chứng :: Bằng chứng" --check "<lệnh test>"`. Chỉ được báo xong khi lệnh này chấp nhận.
5. Khóa API trên máy local nằm trong `OpenMontage/.env`, và git bỏ qua file này. Không in khóa ra màn hình, không xin khóa qua chat.
