#!/usr/bin/env bash
# KHÔI PHỤC TOÀN BỘ DỮ LIỆU ICYFOX TRÊN MÁY MỚI (Windows Git Bash, macOS, Linux).
# Chạy trong thư mục cha của kênh (ví dụ "C:\Users\<tên>\HDRE AI\ClayLapis"), hoặc ngay trong OpenMontage:
#   bash restore_machine.sh [--core] [--no-pip] [--no-tests]
#     --core      chỉ clone các repo dùng thường xuyên (nhanh hơn); mặc định clone đủ 16 repo
#     --no-pip    bỏ qua cài thư viện Python
#     --no-tests  bỏ qua chạy kiểm thử công cụ
# Script KHÔNG cài phần mềm hệ thống (Python, Node, ffmpeg) và KHÔNG đụng tới khóa API: chỉ báo còn thiếu gì.
# Hướng dẫn đầy đủ: channel-studio/guides/KHOI_PHUC_MAY_MOI.md
set -u
BRANCH="ccr-6640cec8-2anthl"
OWNER="hoangdung68789"
CORE="OpenMontage hyperframes gsap-skills motion-design-skill remotion yt-dlp whisperX"
ALL="OpenMontage hyperframes gsap-skills GSAP motion-design-skill three.js remotion whisperX yt-dlp Agent-Reach awesome-opus5-5-videos agent-skills CLI-Anything blender-skills seek-tune replica-skill"
REPOS="$ALL"; PIP=1; TESTS=1
for a in "$@"; do
  case "$a" in --core) REPOS="$CORE";; --no-pip) PIP=0;; --no-tests) TESTS=0;; esac
done
MISSING=()

# 0. Xác định thư mục cha
if [ -f AGENT_GUIDE.md ] && [ -d channel-studio ]; then cd ..; fi
PARENT="$(pwd)"
echo "== 0. Thư mục kênh: $PARENT"
command -v git >/dev/null 2>&1 || { echo "THIẾU git. Cài Git for Windows: https://git-scm.com/download/win (macOS: xcode-select --install)"; exit 1; }

# 1. OpenMontage, đúng nhánh dữ liệu kênh
echo "== 1. OpenMontage (nhánh $BRANCH)"
if [ ! -d OpenMontage/.git ]; then
  git clone -q -b "$BRANCH" "https://github.com/$OWNER/OpenMontage.git" OpenMontage || { echo "Clone thất bại: kiểm tra mạng hoặc đăng nhập GitHub (Git Credential Manager mở trình duyệt)"; exit 1; }
fi
cd OpenMontage
git fetch -q origin "$BRANCH" && git checkout -q "$BRANCH" 2>/dev/null || git checkout -q -b "$BRANCH" "origin/$BRANCH"
git pull -q --ff-only origin "$BRANCH" || echo "  (không pull fast-forward được: có thay đổi cục bộ, xem git status)"
echo "  commit: $(git log --oneline -1)"
cd "$PARENT"

# 2. Các repo còn lại, nằm cạnh OpenMontage
echo "== 2. Repo bộ công cụ"
for r in $REPOS; do
  [ "$r" = "OpenMontage" ] && continue
  found=""
  for d in "$PARENT"/*/; do [ "$(basename "$d" | tr 'A-Z' 'a-z')" = "$(echo "$r" | tr 'A-Z' 'a-z')" ] && found="$d"; done
  if [ -n "$found" ]; then echo "  [có]   $r"; continue; fi
  if git clone -q --depth 50 "https://github.com/$OWNER/$(echo "$r" | tr 'A-Z' 'a-z').git" "$r" 2>/dev/null; then
    echo "  [mới]  $r"
  else
    echo "  [LỖI]  $r (clone thất bại)"; MISSING+=("repo $r")
  fi
done

# 3. Phần mềm hệ thống (chỉ kiểm, không cài)
echo "== 3. Phần mềm hệ thống"
PY=""; for c in python3 python py; do "$c" -c "import sys; sys.exit(0 if sys.version_info >= (3, 10) else 1)" </dev/null >/dev/null 2>&1 && PY="$c" && break; done
[ -n "$PY" ] && echo "  [có]   Python ($("$PY" --version 2>&1))" || { echo "  [THIẾU] Python 3.10+  (Windows: winget install -e --id Python.Python.3.12)"; MISSING+=("Python"); }
command -v node >/dev/null 2>&1 && echo "  [có]   Node.js $(node --version)" || { echo "  [THIẾU] Node.js (Windows: winget install -e --id OpenJS.NodeJS.LTS)"; MISSING+=("Node.js"); }
command -v ffmpeg >/dev/null 2>&1 && echo "  [có]   ffmpeg" || { echo "  [THIẾU] ffmpeg (Windows: winget install -e --id Gyan.FFmpeg)"; MISSING+=("ffmpeg"); }
command -v claude >/dev/null 2>&1 && echo "  [có]   Claude Code (dòng lệnh)" || echo "  [?]    Không thấy lệnh claude: dùng tab Code trong app Claude desktop là đủ"
echo "  (Tên gói winget có thể đổi: kiểm bằng winget search <tên> trước khi cài)"

# 4. Thư viện Python
if [ -n "$PY" ] && [ "$PIP" = 1 ]; then
  echo "== 4. Thư viện Python"
  "$PY" -m pip install -q -r OpenMontage/requirements.txt requests pytest yt-dlp google-auth-oauthlib && echo "  đã cài" || { echo "  [LỖI] pip install"; MISSING+=("thư viện Python"); }
fi

# 5. Khóa API: chỉ tạo file mẫu, không đọc, không in
echo "== 5. Khóa API (OpenMontage/.env)"
if [ -f OpenMontage/.env ]; then
  echo "  [có]   OpenMontage/.env (không in nội dung)"
else
  cp OpenMontage/channel-studio/config/api_keys.env.example OpenMontage/.env
  echo "  [MỚI]  Đã tạo OpenMontage/.env từ mẫu: ANH TỰ MỞ BẰNG NOTEPAD VÀ DÁN KHÓA (không dán vào chat)"
  MISSING+=("khóa API trong OpenMontage/.env")
fi

# 6. Hồ sơ dự án + kiểm tra API + mục tiêu/kế hoạch/việc hôm nay
echo "== 6. Mở phiên (session_start.sh)"
cd OpenMontage
LOG="$(mktemp 2>/dev/null || echo restore_session.log)"
bash .claude/skills/hoang-dung-clay-lapis-studio/scripts/session_start.sh >"$LOG" 2>&1
grep -m1 -A1 "^== 1\." "$LOG" | tail -1 | sed 's/^/  /'
awk '/^== 3\./{f=1;next} /^== 4\./{f=0} f' "$LOG" | sed 's/^/  /'
echo "  (nhật ký đầy đủ của session_start: $LOG)"

# 7. Kiểm thử công cụ
if [ -n "$PY" ] && [ "$TESTS" = 1 ]; then
  echo "== 7. Kiểm thử công cụ ICYFOX"
  "$PY" -m pytest -q -p no:cacheprovider .claude/skills/hoang-dung-clay-lapis-studio/scripts/tests 2>&1 | tail -1
fi

echo "== 8. Còn phải làm"
if [ ${#MISSING[@]} -eq 0 ]; then echo "  (không thiếu gì ở bước 1–5)"; else for m in "${MISSING[@]}"; do echo "  - $m"; done; fi
cat <<'EOF'
  - Thoát Claude Code rồi mở lại trong thư mục OpenMontage để bật 3 hook nhắc việc (.claude/settings.json).
  - Tạo lại 2 tác vụ hẹn giờ trên app Claude desktop (KHÔNG có trong GitHub): lời nhắn ở
    .claude/skills/hoang-dung-clay-lapis-studio/references/autopilot.md §8; giờ chạy 09:00 + 17:00 hằng ngày và Chủ nhật 09:00.
  - Tắt 2 tác vụ đó trên máy cũ (nếu máy cũ còn chạy) để không chạy trùng.
  - Kết nối Notion cho Claude Code nếu phiên chưa có công cụ Notion.
EOF
