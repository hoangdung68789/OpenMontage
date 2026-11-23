"""Bộ điều phối tự lái của ICYFOX: đọc kế hoạch, sổ việc, series, số liệu, rồi in việc phải làm tiếp theo thứ tự ưu tiên.

  python autopilot.py              # in "chương trình làm việc" (agenda) hôm nay
  python autopilot.py --json       # dạng máy đọc
  python autopilot.py --brief      # bản rút gọn (hook dùng)

Phiên tự động hằng ngày chạy lệnh này rồi làm lần lượt từ trên xuống, đến khi hết việc hoặc tới chỗ phải hỏi anh.
Quy tắc ưu tiên và thời hạn: references/autopilot.md.
"""
import json
import re
import sys
from datetime import date, datetime, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from icyfox_common import CS, data_block, load_env, load_json, now_vn, utf8  # noqa: E402
import watchdog  # noqa: E402

PLAN = CS / "PLAN.md"
# Số ngày tối thiểu trước ngày đăng (NHẬN ĐỊNH, chỉnh trong references/autopilot.md nếu đổi)
LEAD = {"outline": 14, "script": 9, "render": 4, "package": 2}
SHORTS_BUFFER_DAYS = 7     # luôn có sẵn Shorts đủ cho 7 ngày tới
RADAR_MAX_AGE = 2          # quét xu hướng tối đa 2 ngày một lần
REPORT_MAX_AGE = 8         # báo cáo số liệu kênh hằng tuần (tác vụ Chủ nhật 09:00), quá 8 ngày là trễ


def d(s):
    return datetime.strptime(s, "%Y-%m-%d").date()


def today():
    return now_vn().date()


def approved(f):
    head = "\n".join(Path(f).read_text(encoding="utf-8", errors="ignore").splitlines()[:8])
    return bool(re.search(r"ĐÃ DUYỆT|QA ĐẠT|APPROVED", head))


def video_dir(code):
    hits = sorted((CS / "videos").glob(f"{code}-*"))
    return hits[0] if hits else None


def stage_of(vd):
    """Đoán bước hiện tại của một video từ file có trong thư mục."""
    if vd is None:
        return "chưa có thư mục", 0
    outline = [p for p in (vd / "script_outline.md", vd / "proposal.md") if p.exists()]
    parts = sorted(vd.glob("script_part*.md"))
    pkg = vd / "package"
    if (pkg / "UPLOADED.txt").exists():
        return "anh đã tải lên", 6
    if (pkg / "title.txt").exists() and (pkg / "description.md").exists():
        return "gói đăng xong", 5
    if (vd / "render" / "RENDERED.txt").exists():
        return "đã render", 4
    if parts and all(approved(p) for p in parts) and (vd / "script_full_ready.txt").exists():
        return "kịch bản đủ", 3
    if parts:
        return f"đang viết kịch bản ({sum(approved(p) for p in parts)}/{len(parts)} phần đạt)", 2
    if outline and any(approved(p) for p in outline):
        return "dàn ý đã duyệt", 1.5
    if outline:
        return "dàn ý chờ duyệt", 1
    return "chưa có dàn ý", 0


def latest_dir_date(pattern):
    best = None
    for p in CS.glob(pattern):
        m = re.match(r"(\d{4}-\d{2}-\d{2})", p.name)
        if m:
            best = max(best or m.group(1), m.group(1))
    return d(best) if best else None


def agenda():
    t = today()
    items = []   # (ưu tiên 1-3, nhóm, nội dung)
    phases = data_block(PLAN, "phases")
    cur = [p for p in phases if d(p[0]) <= t <= d(p[1])]
    phase = f"{cur[0][2]} ({cur[0][0]} → {cur[0][1]}): {cur[0][3]}" if cur else None
    if not cur and phases and t < d(phases[0][0]):
        phase = f"sắp bắt đầu {phases[0][2]} từ {phases[0][0]}: {phases[0][3]}"
    elif not phases:
        phase = "PLAN.md chưa có khối phases"
    if phases and t > d(phases[-1][1]):
        items.append((1, "Kế hoạch", "KẾ HOẠCH ĐÃ HẾT HẠN: lập kế hoạch kỳ mới ngay (request-playbooks mục B), dựa trên báo cáo số liệu"))
        phase = "HẾT HẠN"
    elif phases and (d(phases[-1][1]) - t).days <= 14:
        items.append((2, "Kế hoạch", f"Kế hoạch hết hạn ngày {phases[-1][1]}: chuẩn bị kế hoạch kỳ tới"))

    # Sổ việc
    db = load_json(CS / "state" / "tasks.json", {"tasks": []})
    ts = db.get("tasks", [])
    for x in ts:
        if x["status"] == "doing":
            items.append((1, "Sổ việc", f"{x['id']} đang làm dở: {x['title']} (xong khi: {x.get('dod', '')})"))
        elif x["status"] == "todo" and x.get("due") and d(x["due"]) <= t + timedelta(days=2):
            items.append((1, "Sổ việc", f"{x['id']} sắp/đã tới hạn {x['due']}: {x['title']}"))
    waiting = [x for x in ts if x["status"] == "waiting"]
    blocked = [x for x in ts if x["status"] == "blocked"]

    # Lịch đăng video dài
    releases = [(d(r[0]), r[1], r[2]) for r in data_block(PLAN, "releases")]
    upcoming = [r for r in releases if r[0] >= t][:4]
    rel_lines = []
    for when, code, title in upcoming:
        left = (when - t).days
        vd = video_dir(code)
        st, lvl = stage_of(vd)
        need = None
        if lvl < 1.5 and left <= LEAD["outline"]:
            need = "dàn ý + hook: AI tự chốt, ghi HANDOFF"
        elif lvl < 3 and left <= LEAD["script"]:
            need = "viết xong toàn bộ kịch bản và chạy qa_check"
        elif lvl < 4 and left <= LEAD["render"]:
            need = "giọng đọc + dựng + render"
        elif lvl < 5 and left <= LEAD["package"]:
            need = "gói đăng"
        rel_lines.append(f"{code} {title} | đăng {when:%d/%m} (còn {left} ngày) | {st}")
        if need:
            items.append((1 if left <= LEAD["render"] else 2, "Lịch đăng", f"{code} TRỄ TIẾN ĐỘ (còn {left} ngày): {need}"))
        elif lvl < 5:
            items.append((3, "Lịch đăng", f"{code}: làm bước kế tiếp sau '{st}'"))

    # Shorts
    ready = list((CS / "videos").glob("*/shorts/*.mp4")) + list((CS / "shorts").glob("*/*.mp4"))
    scripted = list((CS / "videos").glob("*/shorts/S*.md")) + list((CS / "shorts").glob("*/S*.md"))
    shorts_start = d("2026-12-01")
    if t + timedelta(days=SHORTS_BUFFER_DAYS) >= shorts_start and len(ready) < SHORTS_BUFFER_DAYS:
        items.append((1 if t >= shorts_start - timedelta(days=3) else 2, "Shorts",
                      f"Kho Shorts có {len(ready)} video dựng xong, {len(scripted)} kịch bản: cần đủ {SHORTS_BUFFER_DAYS} ngày đăng"))

    # Series
    for p in sorted((CS / "series").glob("*/series.json")):
        s = load_json(p, {})
        if s.get("status") in ("planned", "running"):
            nx = next((e for e in sorted(s["episodes"], key=lambda e: e["n"]) if e["status"] != "published"), None)
            if nx:
                fin = " (TẬP CUỐI: phải khép mọi tuyến)" if nx["n"] == s["planned_episodes"] else ""
                items.append((2, "Series", f"{s['title']}: tập {nx['n']}/{s['planned_episodes']}{fin} đang ở bước '{nx['status']}'. "
                                           f"Trước khi viết: series.py brief {s['id']}"))
            elif s.get("status") == "running":
                items.append((1, "Series", f"{s['title']}: mọi tập đã đăng, chạy series.py end"))

    # Dữ liệu
    radar = latest_dir_date("research/*-radar")
    if not radar or (t - radar).days >= RADAR_MAX_AGE:
        items.append((2, "Dữ liệu", f"Quét xu hướng (radar) {'chưa từng chạy' if not radar else 'lần cuối ' + str(radar)}: "
                                    "python scripts/research/niche_outliers.py --days 7"))
    vmap = load_json(CS / "analytics" / "video_map.json", {})
    rep = latest_dir_date("analytics/reports/*")
    if vmap and (not rep or (t - rep).days >= REPORT_MAX_AGE):
        items.append((1, "Dữ liệu", f"Báo cáo số liệu kênh quá hạn (lần cuối {rep}): python scripts/research/yt_analytics_report.py"))
    ideas = CS / "ideas" / "IDEA_BANK.md"
    n_ready = len(re.findall(r"\|\s*Sẵn sàng\s*\|", ideas.read_text(encoding="utf-8"))) if ideas.exists() else 0
    if n_ready < 4:
        items.append((2, "Ý tưởng", f"Kho ý tưởng chỉ có {n_ready} ý tưởng 'Sẵn sàng' (cần >= 4): bổ sung từ radar + báo cáo"))

    # Nhịp tuần: thứ Năm gom lô duyệt, thứ Bảy gom gói tải lên
    wd = t.weekday()
    if wd == 3:
        items.append((1, "AI", "Hôm nay thứ Năm: AI tự chốt lô tuần sau (chủ đề + dàn ý + hook), ghi HANDOFF; không gửi anh duyệt (anh giao quyền 22/11/2026)"))
    if wd == 5:
        import os
        load_env()
        if os.environ.get("YT_AUDIT_APPROVED") == "1":
            items.append((1, "AI", "Hôm nay thứ Bảy: tự tải video tuần sau bằng `yt_publish.py upload <thư mục video>` (đã qua audit)"))
        else:
            items.append((1, "Anh", "Hôm nay thứ Bảy: chuẩn bị GÓI TẢI LÊN tuần sau (danh sách file theo thứ tự + link), báo anh 1 tin. Bỏ bước này khi audit API được duyệt (channel/api-audit/DON_AUDIT.md)"))
    items += watchdog.scan()  # việc treo, quá hạn, lỗi log tác vụ nền (references/fallbacks.md)
    items.sort(key=lambda x: x[0])
    return {"date": str(t), "phase": phase, "items": items, "releases": rel_lines,
            "waiting": [f"{x['id']}: {x['title']} — {x.get('question', '')}" for x in waiting],
            "blocked": [f"{x['id']}: {x['title']} — {x.get('reason', '')}" for x in blocked]}


BACKUP_IDLE_HOURS = 8   # phiên cloud dự phòng chỉ làm việc khi nhánh không có commit nào trong 8 giờ qua


def backup_check():
    """Phiên cloud dự phòng: máy anh vừa làm (có commit trong BACKUP_IDLE_HOURS giờ) thì bỏ qua để không chạy trùng."""
    import subprocess
    import time as _t
    branch = "ccr-6640cec8-2anthl"
    subprocess.run(["git", "fetch", "-q", "origin", branch], cwd=CS.parent, capture_output=True, timeout=120)
    r = subprocess.run(["git", "log", "-1", "--format=%ct|%h|%s", f"origin/{branch}"], cwd=CS.parent, capture_output=True, text=True)
    if r.returncode != 0 or "|" not in r.stdout:
        print("RUN: không đọc được commit cuối (lỗi git), làm việc như bình thường")
        return 0
    ts, h, subj = r.stdout.strip().split("|", 2)
    hours = (_t.time() - int(ts)) / 3600
    if hours < BACKUP_IDLE_HOURS:
        print(f"SKIP: commit cuối {h} cách đây {hours:.1f} giờ (< {BACKUP_IDLE_HOURS} giờ), máy anh hoặc phiên khác đang làm. Kết thúc phiên dự phòng.")
        return 3
    print(f"RUN: commit cuối {h} cách đây {hours:.1f} giờ (>= {BACKUP_IDLE_HOURS} giờ), máy anh có thể đang tắt. Phiên cloud làm thay.")
    return 0


def main():
    utf8()
    if "--backup-check" in sys.argv:
        sys.exit(backup_check())
    a = agenda()
    if "--json" in sys.argv:
        print(json.dumps(a, ensure_ascii=False, indent=1))
        return
    brief = "--brief" in sys.argv
    print(f"CHƯƠNG TRÌNH LÀM VIỆC {a['date']} · Giai đoạn: {a['phase']}")
    if a["releases"]:
        print("Lịch đăng video dài sắp tới:")
        for r in a["releases"][: 2 if brief else 4]:
            print("  -", r)
    print("Việc theo thứ tự ưu tiên:" if a["items"] else "Không có việc gấp: làm việc 'Chưa làm' có ưu tiên cao nhất trong TASKS.md")
    for p, g, txt in a["items"][: 6 if brief else 50]:
        print(f"  [{'GẤP' if p == 1 else 'nên' if p == 2 else 'tiếp'}] {g}: {txt}")
    if a["waiting"]:
        print("Đang chờ anh:", "; ".join(a["waiting"][:3]))
    if a["blocked"]:
        print("Bị chặn:", "; ".join(a["blocked"][:3]))


if __name__ == "__main__":
    main()
