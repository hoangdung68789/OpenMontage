"""Sổ việc ICYFOX. Mọi việc (anh giao, hoặc autopilot tự giao) là một thẻ việc có định nghĩa hoàn thành.

  python tasks.py add "Tiêu đề" --type script --dod "Điều kiện xong, kiểm được" [--owner claude]
                  [--video 002-lady-be-good] [--series deep-jungle] [--prio 1|2|3] [--due 2026-11-30]
  python tasks.py start T-003                     # đang làm (gắn phiên hiện tại)
  python tasks.py wait  T-003 --question "..."    # chờ anh quyết (chỉ cho việc thật sự cần anh)
  python tasks.py block T-003 --reason "..." --tried "cách 1; cách 2"   # bị chặn: phải ghi >= 2 cách đã thử
  python tasks.py done  T-003 --evidence <file|thư mục> [...] [--check "lệnh kiểm"]
         --summary "Đã làm gì, kết quả chính"
         --component "Tên phần :: Kết quả (số liệu cụ thể) :: Cách đã kiểm chứng :: Bằng chứng (đường dẫn hoặc link)"   (lặp lại cho từng phần)
         [--remaining "việc còn lại hoặc rủi ro (ghi 'không có' nếu không có)"]
  python tasks.py drop  T-003 --reason "..."
  python tasks.py note  T-003 "ghi chú"
  python tasks.py list [--all] | next | render | log [--n 5]

Trạng thái: todo · doing · waiting (chờ anh) · blocked · done · dropped.
QUY TẮC HOÀN THÀNH (references/work-contract.md §3): `done` chỉ được nhận khi
  (1) bằng chứng qua kiểm tra tự động theo loại việc, (2) lệnh --check (nếu có) chạy đạt,
  (3) có báo cáo TỪNG THÀNH PHẦN (đủ 4 trường, bằng chứng tồn tại thật).
Không đạt thì báo lỗi, thẻ giữ nguyên. Đạt thì ghi đầy đủ vào nhật ký lịch sử channel-studio/logs/<năm-tháng>.md.
Mỗi lần đổi, file channel-studio/TASKS.md được sinh lại (đừng sửa tay).
"""
import argparse
import os
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from icyfox_common import CS, ROOT, load_json, now_vn, rel, save_json, utf8  # noqa: E402

DB = CS / "state" / "tasks.json"
MD = CS / "TASKS.md"
SESSION_FILE = ROOT / ".claude" / ".icyfox_session"
STATUSES = ["doing", "waiting", "blocked", "todo", "done", "dropped"]
LABEL = {"todo": "Chưa làm", "doing": "Đang làm", "waiting": "Chờ anh", "blocked": "Bị chặn",
         "done": "Xong", "dropped": "Bỏ"}
TYPES = {
    "research": "Nghiên cứu, quét xu hướng, kiểm dữ kiện",
    "competitor": "Phân tích kênh đối thủ (playbook A)",
    "ideas": "Cập nhật kho ý tưởng",
    "plan": "Lập hoặc sửa kế hoạch",
    "outline": "Dàn ý + hook (đề xuất video)",
    "script": "Kịch bản một phần",
    "series": "Cập nhật hồ sơ series",
    "voice": "Giọng đọc, mẫu giọng",
    "scene": "Phân cảnh, tài nguyên",
    "render": "Dựng, render",
    "shorts": "Shorts",
    "package": "Gói đăng",
    "publish": "Áp gói đăng lên video anh đã tải",
    "analytics": "Báo cáo số liệu kênh",
    "code": "Viết hoặc sửa mã (bắt buộc --check)",
    "ops": "Việc vận hành khác",
}


def words(p):
    try:
        return len(re.findall(r"[A-Za-zÀ-ỹ0-9']+", Path(p).read_text(encoding="utf-8", errors="ignore")))
    except OSError:
        return 0


def text(p):
    try:
        return Path(p).read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return ""


def expand(paths):
    files = []
    for p in paths:
        p = Path(p)
        files += [f for f in p.rglob("*") if f.is_file()] if p.is_dir() else [p]
    return files


def has_sources(t):
    return bool(re.search(r"(?im)^\s*(#+\s*)?.*(nguồn|sources?)\b", t)) and len(re.findall(r"https?://", t)) >= 2


def dod_check(task, paths, check_cmd):
    """Trả về danh sách lỗi. Rỗng = đạt."""
    errs = []
    resolved = []
    for p in paths:
        q = Path(p) if Path(p).is_absolute() else ROOT / p
        if not q.exists():
            errs.append(f"không tồn tại: {p}")
        elif q.is_file() and q.stat().st_size == 0:
            errs.append(f"file rỗng: {p}")
        elif q.is_dir() and not any(q.iterdir()):
            errs.append(f"thư mục rỗng: {p}")
        else:
            resolved.append(q)
    if not paths:
        errs.append("chưa đưa bằng chứng (--evidence)")
    trivial = {"HANDOFF.md", "TASKS.md", "tasks.json"}
    if resolved and all(q.name in trivial for q in resolved):
        errs.append("bằng chứng chỉ là HANDOFF/TASKS: phải là sản phẩm thật")
    files = expand(resolved)
    names = [f.name for f in files]
    md = [f for f in files if f.suffix.lower() == ".md"]
    t = task["type"]
    if t == "script":
        ok = [f for f in md if words(f) >= 400 and has_sources(text(f))]
        if not ok:
            errs.append("kịch bản cần file .md >= 400 từ, có mục Nguồn/Sources với >= 2 link")
    elif t == "outline":
        if not [f for f in md if words(f) >= 150]:
            errs.append("dàn ý cần file .md >= 150 từ")
    elif t == "competitor":
        for pat, what in [(r"_api\.json$", "*_api.json (số liệu Data API)"), (r"^BAO_CAO.*\.md$", "BAO_CAO*.md"),
                          (r"^KE_HOACH.*\.md$", "KE_HOACH*.md")]:
            if not any(re.search(pat, n) for n in names):
                errs.append(f"thiếu {what}")
    elif t == "plan":
        if not [f for f in md if words(f) >= 300 and re.search(r"\d{1,2}/\d{1,2}|\d{4}-\d{2}-\d{2}", text(f))]:
            errs.append("kế hoạch cần file .md >= 300 từ có ngày cụ thể")
    elif t in ("research", "ideas"):
        if not any(len(re.findall(r"https?://", text(f))) >= 3 or f.suffix == ".json" for f in files):
            errs.append("nghiên cứu cần file có >= 3 link nguồn hoặc file .json số liệu")
    elif t == "analytics":
        if not any(n.endswith(".md") for n in names) or not any(n.endswith(".json") for n in names):
            errs.append("báo cáo số liệu cần cả report .md và data .json")
    elif t == "series":
        if "series.json" not in names:
            errs.append("cần series.json đã cập nhật")
    elif t == "voice":
        if not any(f.suffix.lower() in (".mp3", ".wav", ".m4a", ".ogg", ".flac") for f in files):
            errs.append("cần file âm thanh")
    elif t in ("render", "shorts"):
        vids = [f for f in files if f.suffix.lower() in (".mp4", ".mov", ".webm")]
        if t == "render" and not [v for v in vids if v.stat().st_size > 100_000]:
            errs.append("cần file video > 100 KB")
        for v in vids:   # CỔNG CHUYỂN ĐỘNG (references/motion-graphics.md §1): không nhận video đứng yên
            if v.stat().st_size <= 100_000:
                continue
            r = subprocess.run([sys.executable, str(Path(__file__).resolve().parent / "motion_metrics.py"), str(v)],
                               capture_output=True, text=True)
            m = re.search(r"\{.*\}", r.stdout)
            if not m:
                errs.append(f"không đo được chuyển động của {v.name}: {(r.stdout + r.stderr)[-200:]}")
                continue
            met = __import__("ast").literal_eval(m.group(0))
            bad = [f"{k}={met[k]} (mốc {lim})" for k, lim, ok in (
                ("static_pct", "<= 2", met["static_pct"] <= 2), ("longest_static", "< 4", met["longest_static"] < 4),
                ("pct_still", "<= 25", met["pct_still"] <= 25)) if not ok]
            if bad:
                errs.append(f"{v.name} chưa đạt mốc chuyển động: " + ", ".join(bad) + " (xem motion-graphics.md)")
        if t == "shorts" and not (vids or md):
            errs.append("cần video Short hoặc kịch bản Short .md")
    elif t == "package":
        for need in ("title.txt", "description.md", "tags.txt"):
            if need not in names:
                errs.append(f"gói đăng thiếu {need}")
    elif t == "code" and not check_cmd:
        errs.append("việc code phải có --check \"lệnh chạy test/kiểm\" và lệnh đó phải chạy đạt")
    if check_cmd:
        r = subprocess.run(check_cmd, shell=True, cwd=ROOT, capture_output=True, text=True)
        if r.returncode != 0:
            errs.append(f"lệnh kiểm thất bại (mã {r.returncode}): {(r.stdout + r.stderr)[-400:]}")
    return errs


LOGDIR = CS / "logs"


def parse_components(items):
    """Mỗi thành phần: 'Tên :: Kết quả :: Cách kiểm chứng :: Bằng chứng'. Trả về (danh sách, lỗi)."""
    comps, errs = [], []
    if not items:
        errs.append("thiếu báo cáo từng thành phần (--component \"Tên :: Kết quả :: Cách kiểm chứng :: Bằng chứng\")")
    for raw in items or []:
        parts = [p.strip() for p in raw.split("::")]
        if len(parts) != 4 or not all(parts):
            errs.append(f"thành phần thiếu trường (cần đủ 4, ngăn bằng '::'): {raw}")
            continue
        name, result, how, ev = parts
        if len(result) < 8 or len(how) < 8:
            errs.append(f"'{name}': kết quả và cách kiểm chứng phải cụ thể (có số liệu/lệnh), không viết chung chung")
        for e in [x.strip() for x in ev.split(",") if x.strip()]:
            if not e.startswith("http"):
                q = Path(e) if Path(e).is_absolute() else ROOT / e
                if not q.exists():
                    errs.append(f"'{name}': bằng chứng không tồn tại: {e}")
        comps.append({"name": name, "result": result, "verified_by": how, "evidence": ev})
    return comps, errs


def history(t, kind, body):
    """Ghi nhật ký lịch sử (không bao giờ xóa, chỉ thêm)."""
    LOGDIR.mkdir(parents=True, exist_ok=True)
    f = LOGDIR / f"{now_vn():%Y-%m}.md"
    if not f.exists():
        f.write_text(f"# Nhật ký lịch sử công việc ICYFOX — {now_vn():%m/%Y}\n\n"
                     "Ghi tự động bởi tasks.py. Chỉ thêm, không sửa, không xóa. Mỗi mục 'HOÀN THÀNH' đã qua kiểm tra tự động.\n",
                     encoding="utf-8")
    head = (f"\n## {now_vn():%Y-%m-%d %H:%M} · {t['id']} · {kind} · {t['title']}\n\n"
            f"- Người làm: {t.get('owner', '')} · Phiên: {session_id()} · Loại việc: {t['type']}"
            + (f" · Video: {t['video']}" if t.get("video") else "") + (f" · Series: {t['series']}" if t.get("series") else "")
            + f"\n- Xong khi (định nghĩa hoàn thành): {t.get('dod', '')}\n")
    with f.open("a", encoding="utf-8") as fh:
        fh.write(head + body + "\n")
    return f


def remote_next():
    """Đọc số thẻ kế tiếp trên GitHub (nhánh kênh) để máy anh và cloud không cấp trùng số. Lỗi gì cũng trả 0."""
    try:
        br = "ccr-6640cec8-2anthl"
        subprocess.run(["git", "fetch", "-q", "origin", br], cwd=ROOT, capture_output=True, timeout=60)
        r = subprocess.run(["git", "show", f"origin/{br}:channel-studio/state/tasks.json"], cwd=ROOT, capture_output=True, text=True, timeout=30)
        import json as _j
        d = _j.loads(r.stdout) if r.returncode == 0 else {}
        ids = [int(t["id"][2:]) for t in d.get("tasks", []) if t.get("id", "").startswith("T-")]
        return max([d.get("next", 0)] + [i + 1 for i in ids])
    except Exception:
        return 0


def session_id():
    try:
        return SESSION_FILE.read_text(encoding="utf-8").strip() or "manual"
    except OSError:
        return os.environ.get("ICYFOX_SESSION", "manual")


def load():
    return load_json(DB, {"version": 1, "next": 1, "tasks": []})


def save(db):
    save_json(DB, db)
    render(db)


def find(db, tid):
    tid = tid.upper() if tid.upper().startswith("T-") else f"T-{int(tid):03d}"
    for t in db["tasks"]:
        if t["id"] == tid:
            return t
    sys.exit(f"Không có thẻ {tid}")


def touch(t, status=None):
    if status:
        t["status"] = status
    t["updated"] = now_vn().strftime("%Y-%m-%d %H:%M")


def order(t):
    return (STATUSES.index(t["status"]), t.get("prio", 2), t.get("due") or "9999", t["id"])


def line(t):
    extra = t.get("question") or t.get("reason") or ""
    link = " · ".join(x for x in [t.get("video"), t.get("series")] if x)
    return (f"| {t['id']} | {LABEL[t['status']]} | {t.get('owner', '')} | {t['title']} | {t['type']} | "
            f"{link} | {t.get('due') or ''} | {t.get('dod', '')} | {extra} |")


def render(db=None):
    db = db or load()
    ts = sorted(db["tasks"], key=order)
    out = ["# Sổ việc ICYFOX", "",
           "Tự sinh từ `state/tasks.json`. **Đừng sửa tay**: dùng `python .claude/skills/hoang-dung-clay-lapis-studio/scripts/tasks.py`.",
           f"Cập nhật: {now_vn().strftime('%Y-%m-%d %H:%M')} (giờ Việt Nam).", ""]
    head = ["| ID | Trạng thái | Ai | Việc | Loại | Video / series | Hạn | Xong khi | Câu hỏi / lý do |",
            "|---|---|---|---|---|---|---|---|---|"]
    for st, title in [("doing", "Đang làm"), ("waiting", "Chờ anh quyết"), ("blocked", "Bị chặn"),
                      ("todo", "Chưa làm (theo ưu tiên)")]:
        rows = [line(t) for t in ts if t["status"] == st]
        out += [f"## {title} ({len(rows)})", ""] + ((head + rows) if rows else ["(không có)"]) + [""]
    done = sorted([t for t in ts if t["status"] == "done"], key=lambda t: t.get("updated", ""), reverse=True)[:15]
    out += ["## Xong gần đây", ""]
    out += [f"- {t['id']} {t['title']} ({t.get('updated', '')}): " + ", ".join(t.get("evidence", [])) for t in done] or ["(chưa có)"]
    MD.write_text("\n".join(out) + "\n", encoding="utf-8")


def main():
    utf8()
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sp = ap.add_subparsers(dest="cmd", required=True)
    a = sp.add_parser("add")
    a.add_argument("title")
    a.add_argument("--type", required=True, choices=sorted(TYPES))
    a.add_argument("--dod", required=True, help="xong khi nào (cụ thể, kiểm được)")
    a.add_argument("--owner", default=os.environ.get("ICYFOX_AGENT", "claude"))
    a.add_argument("--video")
    a.add_argument("--series")
    a.add_argument("--prio", type=int, default=2, choices=[1, 2, 3])
    a.add_argument("--due")
    a.add_argument("--start", action="store_true", help="nhận làm luôn")
    for name in ("start", "wait", "block", "done", "drop", "note"):
        p = sp.add_parser(name)
        p.add_argument("id")
        if name == "wait":
            p.add_argument("--question", required=True)
        if name == "block":
            p.add_argument("--reason", required=True)
            p.add_argument("--tried", required=True, help="các cách đã thử, cách nhau bằng ';' (>= 2)")
        if name == "done":
            p.add_argument("--evidence", nargs="+", default=[])
            p.add_argument("--check", default="")
            p.add_argument("--summary", required=True, help="đã làm gì, kết quả chính (cụ thể)")
            p.add_argument("--component", action="append", default=[],
                           help="'Tên :: Kết quả :: Cách kiểm chứng :: Bằng chứng' (lặp lại cho từng phần)")
            p.add_argument("--remaining", default="không có")
        if name == "drop":
            p.add_argument("--reason", required=True)
        if name == "note":
            p.add_argument("text")
        if name == "start":
            p.add_argument("--owner")
    ls = sp.add_parser("list")
    ls.add_argument("--all", action="store_true")
    lg = sp.add_parser("log")
    lg.add_argument("--n", type=int, default=5)
    sp.add_parser("next")
    sp.add_parser("render")
    sp.add_parser("types")
    x = ap.parse_args()
    db = load()

    if x.cmd == "types":
        for k, v in TYPES.items():
            print(f"{k:11} {v}")
        return
    if x.cmd == "render":
        render(db)
        print("Đã sinh lại", rel(MD))
        return
    if x.cmd == "log":
        files = sorted(LOGDIR.glob("*.md"))
        if not files:
            print("(chưa có nhật ký)")
            return
        entries = files[-1].read_text(encoding="utf-8").split("\n## ")
        print(("\n## ".join(entries[-x.n:])) if len(entries) > 1 else entries[0])
        return
    if x.cmd == "add":
        local_ids = [int(t["id"][2:]) + 1 for t in db["tasks"] if t["id"].startswith("T-")]
        db["next"] = max([db["next"], remote_next()] + local_ids)
        tid = f"T-{db['next']:03d}"
        db["next"] += 1
        t = {"id": tid, "title": x.title, "type": x.type, "dod": x.dod, "owner": x.owner, "status": "todo",
             "prio": x.prio, "due": x.due, "video": x.video, "series": x.series,
             "created": now_vn().strftime("%Y-%m-%d %H:%M"), "evidence": [], "log": []}
        if x.start:
            t["session"] = session_id()
            touch(t, "doing")
        else:
            touch(t)
        db["tasks"].append(t)
        save(db)
        print(f"{tid} [{LABEL[t['status']]}] {x.title}\n  Xong khi: {x.dod}")
        return
    if x.cmd in ("list", "next"):
        ts = sorted(db["tasks"], key=order)
        if x.cmd == "next":
            ts = [t for t in ts if t["status"] in ("doing", "todo")][:5]
        elif not x.all:
            ts = [t for t in ts if t["status"] not in ("done", "dropped")]
        for t in ts:
            extra = t.get("question") or t.get("reason") or ""
            print(f"{t['id']} [{LABEL[t['status']]}] p{t.get('prio', 2)} {t.get('owner', '')}: {t['title']}"
                  + (f" | hạn {t['due']}" if t.get("due") else "") + (f" | {extra}" if extra else ""))
            print(f"      Xong khi: {t.get('dod', '')}")
        if not ts:
            print("(sổ việc trống)")
        return

    t = find(db, x.id)
    log = t.setdefault("log", [])
    if x.cmd == "start":
        t["session"] = session_id()
        if x.owner:
            t["owner"] = x.owner
        t.pop("question", None)
        touch(t, "doing")
    elif x.cmd == "wait":
        t["question"] = x.question
        touch(t, "waiting")
        history(t, "CHỜ ANH QUYẾT", f"- Câu hỏi cho anh: {x.question}\n")
    elif x.cmd == "block":
        tried = [s for s in x.tried.split(";") if s.strip()]
        if len(tried) < 2:
            sys.exit("Phải thử ít nhất 2 cách trước khi báo bị chặn (--tried \"cách 1; cách 2\").")
        t["reason"] = f"{x.reason} | đã thử: {x.tried}"
        touch(t, "blocked")
        history(t, "BỊ CHẶN", f"- Lý do (thông báo lỗi nguyên văn, đã che khóa): {x.reason}\n"
                + "".join(f"- Đã thử: {s.strip()}\n" for s in tried))
    elif x.cmd == "done":
        if t["status"] == "done":
            sys.exit(f"{t['id']} đã xong từ trước ({t.get('updated')}). Không ghi lại.")
        errs = dod_check(t, x.evidence, x.check)
        comps, cerrs = parse_components(x.component)
        errs += cerrs
        if len(x.summary.strip()) < 15:
            errs.append("--summary quá ngắn: ghi rõ đã làm gì, kết quả chính")
        if errs:
            print(f"CHƯA ĐẠT, KHÔNG ĐƯỢC BÁO XONG. {t['id']} vẫn giữ trạng thái '{LABEL[t['status']]}':")
            for e in errs:
                print("  -", e)
            print(f"Định nghĩa hoàn thành: {t.get('dod', '')}")
            sys.exit(2)
        t["evidence"] = [rel(ROOT / p if not Path(p).is_absolute() else p) for p in x.evidence]
        t["report"] = {"summary": x.summary, "components": comps, "remaining": x.remaining, "check": x.check}
        for k in ("question", "reason"):
            t.pop(k, None)
        touch(t, "done")
        body = [f"- Tóm tắt: {x.summary}", "", "| Thành phần | Kết quả | Cách đã kiểm chứng | Bằng chứng |", "|---|---|---|---|"]
        body += [f"| {c['name']} | {c['result']} | {c['verified_by']} | {c['evidence']} |" for c in comps]
        body += ["", "- Kiểm tra tự động của tasks.py: ĐẠT (loại '" + t["type"] + "')"
                 + (f"; lệnh kiểm `{x.check}`: ĐẠT" if x.check else ""),
                 "- File bằng chứng: " + ", ".join(t["evidence"]),
                 f"- Còn lại / rủi ro: {x.remaining}"]
        lf = history(t, "HOÀN THÀNH", "\n".join(body) + "\n")
        print(f"Đã ghi nhật ký: {rel(lf)}")
    elif x.cmd == "drop":
        t["reason"] = x.reason
        touch(t, "dropped")
        history(t, "BỎ", f"- Lý do: {x.reason}\n")
    elif x.cmd == "note":
        touch(t)
        history(t, "GHI CHÚ / ĐÍNH CHÍNH", f"- {x.text}\n")
    log.append(f"{t['updated']} {x.cmd}" + (f": {x.text}" if x.cmd == "note" else ""))
    save(db)
    print(f"{t['id']} -> {LABEL[t['status']]}: {t['title']}")


if __name__ == "__main__":
    main()
