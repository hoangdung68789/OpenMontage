#!/usr/bin/env bash
# Mở phiên làm việc kênh Clay & Lapis. Chạy từ thư mục gốc repo OpenMontage.
# 1) chuyển sang nhánh làm việc và kéo bản mới nhất
# 2) khôi phục hồ sơ dự án OpenMontage (projects/ bị gitignore) từ channel-studio/projects/
# 3) kiểm tra API  4) in HANDOFF.md
set -u
BRANCH="ccr-6640cec8-2anthl"
SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

if [ ! -d .git ] || [ ! -f AGENT_GUIDE.md ]; then
  echo "Hãy chạy script này từ thư mục gốc repo OpenMontage." >&2; exit 1
fi

echo "== 1. Nhánh làm việc: $BRANCH"
git fetch -q origin "$BRANCH" 2>/dev/null || echo "(không fetch được, dùng bản cục bộ)"
if [ "$(git branch --show-current)" != "$BRANCH" ]; then
  git checkout -q "$BRANCH" 2>/dev/null || git checkout -q -b "$BRANCH" "origin/$BRANCH"
fi
git pull -q --ff-only origin "$BRANCH" 2>/dev/null || echo "(không pull được fast-forward, kiểm tra git status)"
git log --oneline -1

echo "== 2. Khôi phục hồ sơ dự án"
if [ -d channel-studio/projects ]; then
  mkdir -p projects
  for d in channel-studio/projects/*/; do
    [ -d "$d" ] || continue
    name="$(basename "$d")"
    mkdir -p "projects/$name"
    cp -rn "$d". "projects/$name/" 2>/dev/null || cp -r "$d". "projects/$name/"
    echo "  projects/$name"
  done
fi

echo "== 2b. Bộ công cụ (16 repo, xem references/toolbox-repos.md)"
PARENT="$(cd .. && pwd)"
for r in OpenMontage hyperframes gsap-skills GSAP motion-design-skill three.js remotion whisperX yt-dlp \
         Agent-Reach awesome-opus5-5-videos agent-skills CLI-Anything blender-skills seek-tune replica-skill; do
  found=""
  for d in "$PARENT"/*/; do
    [ "$(basename "$d" | tr 'A-Z' 'a-z')" = "$(echo "$r" | tr 'A-Z' 'a-z')" ] && found="$d"
  done
  if [ -n "$found" ]; then echo "  [có]   $r"; else echo "  [thiếu] $r  -> add_repo(owner=\"hoangdung68789\", repo=\"$(echo "$r" | tr 'A-Z' 'a-z')\") nếu cần"; fi
done

echo "== 3. Kiểm tra API"
python3 -c "import requests" 2>/dev/null || pip install -q requests
python3 "$SKILL_DIR/scripts/check_apis.py" || echo "(kiểm tra API lỗi, xem references/environment-and-apis.md)"

echo "== 4. HANDOFF.md"
cat channel-studio/HANDOFF.md 2>/dev/null || echo "(chưa có channel-studio/HANDOFF.md)"
