"""Hook nhắc mục tiêu và việc cho Claude Code (cấu hình trong OpenMontage/.claude/settings.json).

  pulse.py session   # SessionStart (startup, resume, clear, compact): in mục tiêu, kế hoạch, hợp đồng, sổ việc, series
  pulse.py prompt    # UserPromptSubmit: nhắc ngắn mỗi lượt anh gửi yêu cầu
  pulse.py stop      # Stop: chặn 1 lần nếu còn thẻ việc 'đang làm' của phiên này, hoặc còn thay đổi chưa lưu git

Đầu vào: JSON của Claude Code qua stdin. Đầu ra: chữ thường (được đưa vào ngữ cảnh) hoặc JSON {"decision":"block"} cho Stop.
Không bao giờ làm hỏng phiên: lỗi gì cũng thoát 0.
"""
import json
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
try:
    from icyfox_common import CS, ROOT, load_json, now_vn, pulse_block, utf8  # noqa: E402
    import autopilot  # noqa: E402
except Exception:  # pragma: no cover
    sys.exit(0)

SESSION_FILE = ROOT / ".claude" / ".icyfox_session"
SKILL_REL = ".claude/skills/hoang-dung-clay-lapis-studio"
CONTRACT = (
    "HỢP ĐỒNG LÀM VIỆC (mỗi yêu cầu, kể cả nhỏ): "
    "1) nhắc mục tiêu, 2) đọc đúng file theo references/read-map.md, "
    "3) tạo/nhận thẻ việc: scripts/tasks.py add|start (có 'xong khi'), "
    "4) làm thật bằng công cụ/API thật đến khi xong, 5) tasks.py done --evidence (script tự kiểm), "
    "6) trả lời theo khung KẾT LUẬN/CHI TIẾT/DẪN CHỨNG/BƯỚC TIẾP THEO + lưu bằng session_end.py. "
    "Chỉ dừng khi: xong có bằng chứng, việc thật sự cần anh quyết (tasks.py wait), hoặc bị chặn sau >= 2 cách thử (tasks.py block)."
)


def read_stdin():
    try:
        raw = sys.stdin.read()
        return json.loads(raw) if raw.strip() else {}
    except Exception:
        return {}


def remember_session(inp):
    sid = inp.get("session_id")
    if sid:
        try:
            SESSION_FILE.parent.mkdir(parents=True, exist_ok=True)
            SESSION_FILE.write_text(sid, encoding="utf-8")
        except OSError:
            pass
    return sid


def tasks():
    return load_json(CS / "state" / "tasks.json", {"tasks": []}).get("tasks", [])


def session(inp):
    remember_session(inp)
    out = ["=== ICYFOX: nhắc tự động đầu phiên (hook SessionStart) ===", "",
           "MỤC TIÊU VĨNH VIỄN (channel-studio/MISSION.md):", pulse_block(CS / "MISSION.md") or "(thiếu MISSION.md)", "",
           "KẾ HOẠCH HIỆN HÀNH (channel-studio/PLAN.md):", pulse_block(CS / "PLAN.md") or "(thiếu PLAN.md)", "", CONTRACT, ""]
    try:
        a = autopilot.agenda()
        out.append(f"VIỆC HÔM NAY ({a['date']}, giai đoạn: {a['phase']}):")
        out += [f"  [{'GẤP' if p == 1 else 'nên' if p == 2 else 'tiếp'}] {g}: {t}" for p, g, t in a["items"][:10]] or ["  (không có việc gấp)"]
        if a["waiting"]:
            out.append("  Đang chờ anh: " + "; ".join(a["waiting"][:4]))
        if a["blocked"]:
            out.append("  Bị chặn: " + "; ".join(a["blocked"][:4]))
    except Exception as e:  # agenda lỗi không được làm hỏng phiên
        out.append(f"(autopilot.py lỗi: {e})")
    out += ["", "Đọc tiếp: channel-studio/HANDOFF.md, channel-studio/TASKS.md, skill hoang-dung-clay-lapis-studio (SKILL.md mục 0), "
            f"{SKILL_REL}/references/work-contract.md. Mở phiên: bash {SKILL_REL}/scripts/session_start.sh"]
    if inp.get("source") == "compact":
        out.insert(1, "!! Ngữ cảnh vừa được nén: đọc lại TASKS.md và thẻ việc đang làm trước khi tiếp tục. Không làm lại việc đã xong.")
    print("\n".join(out)[:9500])


def prompt(inp):
    remember_session(inp)
    mission = pulse_block(CS / "MISSION.md").splitlines()
    out = ["[ICYFOX nhắc mỗi lượt] " + (mission[0].lstrip("- ") if mission else "Mục tiêu: channel-studio/MISSION.md"), CONTRACT]
    ts = tasks()
    act = [t for t in ts if t["status"] in ("doing", "waiting", "blocked")]
    if act:
        out.append("Thẻ việc đang mở: " + "; ".join(f"{t['id']} [{t['status']}] {t['title']}" for t in act[:6]))
    try:
        a = autopilot.agenda()
        urgent = [t for p, g, t in a["items"] if p == 1][:3]
        if urgent:
            out.append("GẤP theo kế hoạch: " + " | ".join(urgent))
    except Exception:
        pass
    out.append("Yêu cầu mới của anh → tạo thẻ việc trước khi làm. Đừng hỏi lại điều đã có trong MISSION/PLAN/HANDOFF/decisions-log.")
    print("\n".join(out)[:4000])


DONE_RX = re.compile(r"(?<!chưa )(?<!không )(đã xong|đã hoàn thành|hoàn thành xong|đã hoàn tất|xong hết|đã làm xong|all done|completed)",
                     re.IGNORECASE)


def last_reply_claims_done(inp):
    """Đọc câu trả lời cuối của AI (transcript JSONL). Trả về cụm từ 'đã xong' nếu có."""
    text = inp.get("last_assistant_message") or ""
    tp = inp.get("transcript_path")
    if not text and tp and Path(tp).is_file():
        try:
            lines = Path(tp).read_text(encoding="utf-8", errors="ignore").splitlines()[-200:]
            for raw in reversed(lines):
                e = json.loads(raw)
                if e.get("type") == "assistant":
                    content = e.get("message", {}).get("content", [])
                    parts = [c.get("text", "") for c in content if isinstance(c, dict) and c.get("type") == "text"]
                    if parts:
                        text = "\n".join(parts)
                        break
        except Exception:
            return None
    m = DONE_RX.search(text or "")
    return m.group(0) if m else None


def stop(inp):
    if inp.get("stop_hook_active"):
        return  # đã nhắc 1 lần, không chặn mãi
    sid = inp.get("session_id") or ""
    mine = [t for t in tasks() if t["status"] == "doing" and (not sid or t.get("session") in (sid, None, "manual"))]
    reasons = []
    if mine:
        reasons.append("Còn thẻ việc 'đang làm': " + "; ".join(f"{t['id']} {t['title']} (xong khi: {t.get('dod', '')})" for t in mine[:5])
                       + ". Làm tiếp đến khi `tasks.py done --evidence ...` đạt. Nếu thật sự cần anh quyết: `tasks.py wait <id> --question`. "
                       "Nếu bị chặn sau >= 2 cách thử: `tasks.py block <id> --reason --tried`.")
    try:
        r = subprocess.run(["git", "status", "--porcelain", "--", "channel-studio", SKILL_REL, ".agents", ".claude/settings.json"],
                           cwd=ROOT, capture_output=True, text=True, timeout=15)
        dirty = [l for l in r.stdout.splitlines() if l.strip()]
    except Exception:
        dirty = []
    claim = last_reply_claims_done(inp)
    if claim:
        from datetime import timedelta
        cutoff = (now_vn() - timedelta(hours=12)).strftime("%Y-%m-%d %H:%M")
        done_here = [t for t in tasks() if t["status"] == "done" and t.get("updated", "") >= cutoff]
        if not done_here:
            reasons.append(f"Câu trả lời vừa rồi báo \"{claim}\" nhưng sổ việc không có thẻ nào được `tasks.py done` (đạt kiểm tra, "
                           "có báo cáo từng thành phần) trong phiên này. Hoặc chạy `tasks.py done ... --summary --component ...` cho việc "
                           "đã thật sự xong, hoặc sửa câu trả lời: nói rõ phần nào CHƯA xong (quy tắc hoàn thành, work-contract.md §3).")
    if dirty:
        reasons.append(f"Có {len(dirty)} file chưa lưu git (ví dụ: {dirty[0][3:]}). Chạy session_end.py để đẩy lên GitHub "
                       "(nếu là thay đổi của agent khác đang làm thì ghi rõ và bỏ qua).")
    if reasons:
        print(json.dumps({"decision": "block", "reason": "[ICYFOX] Chưa được dừng: " + " | ".join(reasons)}, ensure_ascii=False))


def main():
    utf8()
    mode = sys.argv[1] if len(sys.argv) > 1 else "prompt"
    inp = read_stdin()
    try:
        {"session": session, "prompt": prompt, "stop": stop}.get(mode, prompt)(inp)
    except Exception:
        pass


if __name__ == "__main__":
    main()
