"""Giám sát tác vụ ICYFOX: tìm việc treo, quá hạn, lỗi trong log tác vụ nền, và chỉ ra phương án thay thế.

  python watchdog.py                 # in báo cáo; mã thoát 1 nếu có việc GẤP
  python watchdog.py <log> [<log>]   # soát thêm log ngoài channel-studio/state/jobs/
  python watchdog.py --json

Tác vụ nền chạy lâu (lời đọc, render, quét) ghi log vào channel-studio/state/jobs/<ngày>-<việc>.log.
Bảng phương án thay thế (mã F1..F9): references/fallbacks.md. Phiên tự lái 09:00/17:00 chạy file này đầu tiên
(autopilot.py gọi scan() và đưa kết quả lên đầu chương trình làm việc).
"""
import json
import re
import sys
from datetime import datetime, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from icyfox_common import CS, load_json, now_vn, utf8  # noqa: E402

STALL_HOURS = 6   # thẻ "đang làm" không cập nhật quá ngần này giờ = nghi treo
TAIL_LINES = 60   # chỉ đọc đuôi log: lỗi cũ đã xử lý nằm phía trên
# (mã phương án, mẫu lỗi, tên lỗi). Thứ tự = ưu tiên khớp; F0 là lỗi chưa có trong bảng.
SIGNATURES = [
    ("F1", r"PerDay|hết hạn mức ngày", "Gemini hết hạn mức ngày"),
    ("F2", r"gemini_tts\S*.*404|404.*generativelanguage", "gemini_tts.py lỗi 404"),
    ("F3", r"quotaExceeded|dailyLimitExceeded", "YouTube API hết hạn mức"),
    ("F4", r"HTTP Error 429|Sign in to confirm", "yt-dlp bị chặn (429)"),
    ("F5", r"\b401\b.*(nalytics|monetary|revenue|doanh thu)", "Không đọc được doanh thu (401)"),
    ("F6", r"InvalidDataError|av\.error|PyAV", "Whisper/PyAV không đọc được file"),
    ("F7", r"hyperframes.*(error|fail)|lint.*error", "HyperFrames render lỗi"),
    ("F8", r"MemoryError|out of memory|CUDA out of memory", "Máy quá tải"),
    ("F9", r"lỗi push|push.*(rejected|failed)|failed to push", "Push GitHub lỗi"),
    ("F10", r"(?<!\d)429(?!\d)|RESOURCE_EXHAUSTED|rate limit", "Bị giới hạn tốc độ (429 theo phút)"),
    ("F0", r"Traceback|\bLỖI\b|\bERROR\b|\bError:", "Lỗi chưa có trong bảng"),
]


def _ts(s):
    try:
        return datetime.strptime(s[:16], "%Y-%m-%d %H:%M").replace(tzinfo=now_vn().tzinfo)
    except (TypeError, ValueError):
        return None


def check_tasks(now):
    out = []
    for x in load_json(CS / "state" / "tasks.json", {"tasks": []}).get("tasks", []):
        st, tid, title = x.get("status"), x.get("id"), x.get("title", "")[:70]
        if st == "doing":
            up = _ts(x.get("updated") or x.get("created"))
            if up and now - up > timedelta(hours=STALL_HOURS):
                out.append((1, "Giám sát", f"{tid} NGHI TREO: 'đang làm' mà {int((now - up).total_seconds() // 3600)} giờ chưa cập nhật: {title}. "
                                          "Kiểm tác vụ nền của thẻ; lỗi thì tra fallbacks.md, hết đường thì chuyển 'blocked' kèm lý do"))
        if st in ("todo", "doing") and x.get("due") and str(x["due"]) < now.strftime("%Y-%m-%d"):
            out.append((1, "Giám sát", f"{tid} QUÁ HẠN {x['due']}: {title}. Làm ngay hoặc dời hạn có ghi lý do"))
        if st == "blocked":
            out.append((2, "Giám sát", f"{tid} bị chặn: {x.get('reason', '')[:90]}. Thử phương án thay thế trong fallbacks.md"))
    return out


def check_log(path):
    """Trả (mã, tên lỗi, dòng lỗi) cho lỗi khớp đầu tiên ở đuôi log, hoặc None nếu log sạch."""
    try:
        tail = Path(path).read_text(encoding="utf-8", errors="ignore").splitlines()[-TAIL_LINES:]
    except OSError:
        return None
    for code, rx, name in SIGNATURES:
        for line in reversed(tail):
            if re.search(rx, line):
                return code, name, line.strip()[:160]
    return None


def check_jobs(extra=()):
    out = []
    logs = sorted((CS / "state" / "jobs").glob("*.log")) + [Path(p) for p in extra]
    for p in logs:
        hit = check_log(p)
        if hit:
            code, name, line = hit
            out.append((1, "Giám sát", f"{p.name}: {name} [{code}] → làm theo references/fallbacks.md mục {code}. Dòng lỗi: {line}"))
    return out


def scan(extra_logs=()):
    now = now_vn()
    return sorted(check_tasks(now) + check_jobs(extra_logs), key=lambda x: x[0])


def main():
    utf8()
    extra = [a for a in sys.argv[1:] if not a.startswith("--")]
    items = scan(extra)
    if "--json" in sys.argv:
        print(json.dumps(items, ensure_ascii=False, indent=1))
    else:
        print(f"GIÁM SÁT {now_vn():%Y-%m-%d %H:%M}: " + (f"{len(items)} vấn đề" if items else "không có việc treo, quá hạn hay lỗi"))
        for p, _, txt in items:
            print(f"  [{'GẤP' if p == 1 else 'nên'}] {txt}")
    sys.exit(1 if any(p == 1 for p, _, _ in items) else 0)


if __name__ == "__main__":
    main()
