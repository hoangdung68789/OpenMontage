"""Đóng phiên làm việc kênh Clay & Lapis. Chạy từ thư mục gốc repo OpenMontage.

    python3 .claude/skills/hoang-dung-clay-lapis-studio/scripts/session_end.py -m "mô tả ngắn"

1) chép projects/<id>/ -> channel-studio/projects/<id>/ (bỏ assets/video, renders, file > 20 MB)
2) quét khóa/token trong các file sắp commit -> có thì dừng
3) git add -f channel-studio + skill, commit (kèm --trailer nếu phiên yêu cầu dòng ghi công), push (thử lại tối đa 4 lần)
"""
import argparse
import os
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

BRANCH = "ccr-6640cec8-2anthl"
SKILL_REL = ".claude/skills/hoang-dung-clay-lapis-studio"
SKIP_DIRS = {"video", "renders", "__pycache__", "node_modules", ".cache"}
MAX_BYTES = 20 * 1024 * 1024
SECRET_PATTERNS = [
    r"AIza[0-9A-Za-z_\-]{30,}",          # khóa Google / Gemini
    r"sk_[0-9a-f]{32,}",                 # khóa ElevenLabs
    r"GOCSPX-[0-9A-Za-z_\-]{10,}",       # client secret Google
    r"1//0[0-9A-Za-z_\-]{30,}",          # refresh token Google
    r"ya29\.[0-9A-Za-z_\-]{20,}",        # access token Google
]


def run(cmd, check=True):
    return subprocess.run(cmd, check=check, text=True, capture_output=True)


def mirror_projects():
    src_root, dst_root = Path("projects"), Path("channel-studio/projects")
    if not src_root.is_dir():
        return []
    copied = []
    for proj in sorted(p for p in src_root.iterdir() if p.is_dir()):
        for f in proj.rglob("*"):
            if not f.is_file() or SKIP_DIRS & set(f.relative_to(proj).parts):
                continue
            if f.stat().st_size > MAX_BYTES:
                print(f"  bỏ qua file lớn: {f}")
                continue
            dst = dst_root / proj.name / f.relative_to(proj)
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(f, dst)
        copied.append(proj.name)
    return copied


def scan_secrets(paths):
    hits = []
    rx = re.compile("|".join(SECRET_PATTERNS))
    for root in paths:
        for f in Path(root).rglob("*"):
            if f.is_file() and f.stat().st_size < 5 * 1024 * 1024:
                try:
                    text = f.read_text(encoding="utf-8", errors="ignore")
                except OSError:
                    continue
                if rx.search(text):
                    hits.append(str(f))
    return hits


def scan_secrets_files(files):
    rx = re.compile("|".join(SECRET_PATTERNS))
    return [f for f in files if Path(f).stat().st_size < 5 * 1024 * 1024
            and rx.search(Path(f).read_text(encoding="utf-8", errors="ignore"))]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("-m", "--message", required=True, help="mô tả ngắn cho commit (tiếng Anh hoặc Việt)")
    ap.add_argument("--trailer", default="",
                    help="các dòng ghi công mà phiên hiện tại được yêu cầu thêm vào cuối commit (mỗi dòng cách nhau \\n)")
    ap.add_argument("--no-push", action="store_true")
    a = ap.parse_args()
    if not Path("AGENT_GUIDE.md").exists():
        sys.exit("Hãy chạy từ thư mục gốc repo OpenMontage.")
    if run(["git", "branch", "--show-current"]).stdout.strip() != BRANCH:
        sys.exit(f"Đang không ở nhánh {BRANCH}. Chạy session_start.sh trước.")

    print("== 1. Sao lưu hồ sơ dự án:", ", ".join(mirror_projects()) or "(không có)")
    print("== 2. Chuẩn bị commit (loại file .env) và quét khóa/token")
    # sinh lại các file tự sinh để khớp dữ liệu
    here = Path(__file__).resolve().parent
    for cmd in (["tasks.py", "render"], ["series.py", "render"]):
        run([sys.executable, str(here / cmd[0]), cmd[1]], check=False)
    doing = [l for l in run([sys.executable, str(here / "tasks.py"), "list"], check=False).stdout.splitlines() if "[Đang làm]" in l]
    if doing:
        print("  CẢNH BÁO: còn thẻ 'Đang làm' (hoàn thành, chờ anh, hoặc bị chặn trước khi đóng phiên):")
        for l in doing:
            print("   ", l)
    extra = [".agents/skills/hoang-dung-clay-lapis-studio", ".claude/settings.json", "CLAUDE.md", "AGENTS.md",
             "pipeline_defs/icyfox-autopilot.yaml", ".gitignore"]
    paths = ["channel-studio", SKILL_REL] + [p for p in extra if Path(p).exists()]
    run(["git", "add", "-f"] + paths)
    staged = [f for f in run(["git", "diff", "--cached", "--name-only"]).stdout.splitlines() if f]
    junk = [f for f in staged if "__pycache__" in f or f.endswith((".pyc", ".icyfox_session")) or "/.pytest_cache/" in f]
    if junk:
        run(["git", "reset", "-q", "--"] + junk)
        staged = [f for f in staged if f not in junk]
    envs = [f for f in staged if (Path(f).name == ".env" or Path(f).name.endswith(".env")) and not f.endswith(".example")]
    if envs:
        run(["git", "reset", "-q", "--"] + envs)
        print("  đã loại khỏi commit:", ", ".join(envs))
    staged = [f for f in staged if f not in envs and Path(f).is_file()]
    big = [f for f in staged if Path(f).stat().st_size > 95 * 1024 * 1024]
    if big:
        run(["git", "reset", "-q", "--"] + big)
        print("  đã loại file > 95 MB (GitHub chặn > 100 MB, hãy dùng Google Drive):", ", ".join(big))
        staged = [f for f in staged if f not in big]
    hits = scan_secrets_files(staged)
    if hits:
        run(["git", "reset", "-q"])
        sys.exit("DỪNG: có thể có khóa/token trong: " + ", ".join(hits))
    print("  không thấy khóa/token")

    print("== 3. Commit")
    if not run(["git", "diff", "--cached", "--quiet"], check=False).returncode:
        print("  không có thay đổi để commit")
    else:
        trailer = a.trailer.replace("\\n", "\n").strip()
        msg = a.message + ("\n\n" + trailer if trailer else "")
        run(["git", "commit", "-q", "-m", msg])
        print(" ", run(["git", "log", "--oneline", "-1"]).stdout.strip())

    if a.no_push:
        return
    print("== 4. Push")
    for i in range(4):
        r = run(["git", "push", "-u", "origin", BRANCH], check=False)
        if r.returncode == 0:
            print("  đã đẩy lên origin/" + BRANCH)
            return
        print(f"  lỗi push (lần {i + 1}): {r.stderr.strip()[:200]}")
        time.sleep(2 ** (i + 1))
    sys.exit("Push thất bại sau 4 lần. Nếu nhánh trên GitHub có commit mới: git fetch origin "
             f"{BRANCH} && git merge --no-edit FETCH_HEAD rồi chạy lại.")


if __name__ == "__main__":
    main()
