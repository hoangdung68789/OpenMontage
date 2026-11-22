#!/usr/bin/env bash
# Chạy pulse.py bằng Python có sẵn. Trên Windows, "python3" có thể chỉ là lối tắt mở Microsoft Store nên phải thử lần lượt.
# Không bao giờ làm hỏng phiên: thiếu Python thì in nhắc thủ công và thoát 0.
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
for c in python3 python py; do
  if command -v "$c" >/dev/null 2>&1 && "$c" -c "import sys; sys.exit(0 if sys.version_info >= (3, 8) else 1)" </dev/null >/dev/null 2>&1; then
    PYTHONIOENCODING=utf-8 exec "$c" "$DIR/pulse.py" "$@"
  fi
done
echo "[ICYFOX] Không chạy được Python để nhắc việc. Đọc thủ công: channel-studio/MISSION.md, PLAN.md, TASKS.md."
exit 0
