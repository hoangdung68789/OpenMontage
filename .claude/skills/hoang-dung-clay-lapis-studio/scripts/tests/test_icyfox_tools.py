"""Kiểm thử các công cụ ICYFOX (sổ việc, quy tắc hoàn thành, series, hook, autopilot) trong thư mục tạm.

    python -m pytest -q .claude/skills/hoang-dung-clay-lapis-studio/scripts/tests
"""
import json
import subprocess
import sys
from pathlib import Path

import pytest

S = Path(__file__).resolve().parents[1]
PY = sys.executable


def run(ws, *args, stdin=""):
    return subprocess.run([PY, *map(str, args)], cwd=ws, input=stdin, capture_output=True, text=True, encoding="utf-8")


@pytest.fixture()
def ws(tmp_path):
    (tmp_path / "channel-studio").mkdir()
    (tmp_path / ".claude").mkdir()
    (tmp_path / "AGENT_GUIDE.md").write_text("x", encoding="utf-8")
    subprocess.run(["git", "init", "-q", "."], cwd=tmp_path)
    return tmp_path


def test_done_requires_evidence_components_and_logs(ws):
    assert run(ws, S / "tasks.py", "add", "Viết phần 1", "--type", "script", "--dod", ">=400 từ, có nguồn", "--start").returncode == 0
    f = ws / "p1.md"
    f.write_text("ngắn", encoding="utf-8")
    r = run(ws, S / "tasks.py", "done", "T-001", "--evidence", "p1.md", "--summary", "Viết phần 1 xong rồi đó")
    assert r.returncode == 2 and "KHÔNG ĐƯỢC BÁO XONG" in r.stdout
    f.write_text("# P1\n" + "word " * 450 + "\n## Sources\n- https://a.org\n- https://b.org\n", encoding="utf-8")
    r = run(ws, S / "tasks.py", "done", "T-001", "--evidence", "p1.md", "--summary", "Viết phần 1, 450 từ, 2 nguồn",
            "--component", "Lời thoại :: ok :: xem :: p1.md")
    assert r.returncode == 2 and "cụ thể" in r.stdout
    r = run(ws, S / "tasks.py", "done", "T-001", "--evidence", "p1.md", "--summary", "Viết phần 1, 450 từ, 2 nguồn",
            "--component", "Lời thoại :: 450 từ, 1 phần :: đếm từ bằng tasks.py :: p1.md")
    assert r.returncode == 0, r.stdout + r.stderr
    log = next((ws / "channel-studio" / "logs").glob("*.md")).read_text(encoding="utf-8")
    assert "HOÀN THÀNH" in log and "450 từ, 1 phần" in log
    db = json.loads((ws / "channel-studio" / "state" / "tasks.json").read_text(encoding="utf-8"))
    assert db["tasks"][0]["status"] == "done" and db["tasks"][0]["report"]["components"]


def test_code_task_needs_passing_check_and_block_needs_two_tries(ws):
    run(ws, S / "tasks.py", "add", "Sửa công cụ", "--type", "code", "--dod", "test đạt")
    (ws / "x.py").write_text("print(1)", encoding="utf-8")
    args = ["done", "T-001", "--evidence", "x.py", "--summary", "Sửa công cụ và chạy test",
            "--component", "Mã :: sửa 1 hàm, thêm 1 test :: chạy lệnh kiểm bên dưới :: x.py"]
    assert run(ws, S / "tasks.py", *args).returncode == 2
    assert run(ws, S / "tasks.py", *args, "--check", f'"{PY}" -c "import sys; sys.exit(1)"').returncode == 2
    assert run(ws, S / "tasks.py", *args, "--check", f'"{PY}" -c "pass"').returncode == 0
    run(ws, S / "tasks.py", "add", "Việc khác", "--type", "ops", "--dod", "x")
    assert run(ws, S / "tasks.py", "block", "T-002", "--reason", "lỗi 404", "--tried", "một cách").returncode != 0
    assert run(ws, S / "tasks.py", "block", "T-002", "--reason", "lỗi 404", "--tried", "cách 1; cách 2").returncode == 0


def test_series_lifecycle_enforces_end(ws):
    sp = S / "series.py"
    assert run(ws, sp, "new", "deep-jungle", "--title", "Deep Jungle", "--pillar", "P2", "--episodes", "3",
               "--premise", "p", "--arc", "a|b|c").returncode == 0
    assert run(ws, sp, "episode", "deep-jungle", "4", "--status", "planned").returncode != 0
    assert run(ws, sp, "episode", "deep-jungle", "2", "--status", "published", "--summary", "s", "--cliffhanger", "c").returncode != 0
    assert run(ws, sp, "episode", "deep-jungle", "1", "--status", "published", "--summary", "s1", "--cliffhanger", "c1",
               "--open", "Ai cắt radio?").returncode == 0
    assert run(ws, sp, "episode", "deep-jungle", "2", "--status", "published", "--summary", "s2", "--cliffhanger", "c2").returncode == 0
    b = run(ws, sp, "brief", "deep-jungle").stdout
    assert "TẬP CUỐI" in b and "c2" in b and "Ai cắt radio?" in b
    assert run(ws, sp, "episode", "deep-jungle", "3", "--status", "published", "--summary", "s3").returncode == 0
    assert run(ws, sp, "end", "deep-jungle", "--next", "x").returncode != 0          # còn tuyến mở
    assert run(ws, sp, "episode", "deep-jungle", "3", "--close", "TH1").returncode == 0
    assert run(ws, sp, "end", "deep-jungle", "--next", "Shackleton").returncode == 0
    assert run(ws, sp, "episode", "deep-jungle", "3", "--summary", "y").returncode != 0  # đã kết thúc
    assert "ĐÃ KẾT THÚC" in (ws / "channel-studio" / "series" / "SERIES_INDEX.md").read_text(encoding="utf-8")


def test_stop_hook_blocks_open_task_and_false_done_claim(ws):
    hook = S / "hooks" / "pulse.py"
    run(ws, S / "tasks.py", "add", "Đang dở", "--type", "ops", "--dod", "x", "--start")
    r = run(ws, hook, "stop", stdin=json.dumps({"session_id": "s"}))
    assert '"decision": "block"' in r.stdout and "Đang dở" in r.stdout
    assert run(ws, hook, "stop", stdin=json.dumps({"session_id": "s", "stop_hook_active": True})).stdout.strip() == ""
    tr = ws / "t.jsonl"
    tr.write_text(json.dumps({"type": "assistant", "message": {"content": [{"type": "text", "text": "Đã hoàn thành mọi việc."}]}}), encoding="utf-8")
    run(ws, S / "tasks.py", "drop", "T-001", "--reason", "thử")
    r = run(ws, hook, "stop", stdin=json.dumps({"session_id": "s", "transcript_path": str(tr)}))
    assert "Đã hoàn thành" in r.stdout and '"decision": "block"' in r.stdout
    tr.write_text(json.dumps({"type": "assistant", "message": {"content": [{"type": "text", "text": "Phần 2 chưa hoàn thành."}]}}), encoding="utf-8")
    r = run(ws, hook, "stop", stdin=json.dumps({"session_id": "s", "transcript_path": str(tr)}))
    assert "báo" not in r.stdout


def test_session_and_prompt_hooks_print_mission_and_agenda(ws):
    (ws / "channel-studio" / "MISSION.md").write_text("<!-- pulse:start -->\n- MỤC TIÊU: kiếm tiền YouTube\n<!-- pulse:end -->\n", encoding="utf-8")
    (ws / "channel-studio" / "PLAN.md").write_text(
        "<!-- pulse:start -->\n- Nhịp: 1–2 video/ngày\n<!-- pulse:end -->\n<!-- phases\n2000-01-01|2000-01-02|0. Cũ|x\n-->\n"
        "<!-- releases\n2999-01-01|002|Test\n-->\n", encoding="utf-8")
    out = run(ws, S / "hooks" / "pulse.py", "session", stdin=json.dumps({"session_id": "abc", "source": "compact"})).stdout
    assert "kiếm tiền YouTube" in out and "KẾ HOẠCH ĐÃ HẾT HẠN" in out and "nén" in out
    assert (ws / ".claude" / ".icyfox_session").read_text(encoding="utf-8") == "abc"
    out = run(ws, S / "hooks" / "pulse.py", "prompt", stdin="{}").stdout
    assert "kiếm tiền YouTube" in out and "HỢP ĐỒNG" in out


def test_analytics_report_finds_winners_from_replay(ws):
    vids = {f"vid{i:08d}"[:11]: {"id": f"vid{i:08d}"[:11], "title": f"Video {i}", "published": "2026-12-01",
                                  "seconds": 2100 if i < 4 else 50, "privacy": "public", "lifetime_views": 1000} for i in range(7)}
    ids = list(vids)
    first7 = {v: {"views": [900, 1000, 1100, 4000, 100, 120, 600][k], "estimatedMinutesWatched": [6000, 6600, 7200, 30000, 50, 60, 300][k],
                  "subscribersGained": 3} for k, v in enumerate(ids)}
    life = [{"video": v, "views": 2000, "estimatedMinutesWatched": 9000, "averageViewDuration": 600, "averageViewPercentage": 38.5,
             "subscribersGained": 5, "likes": 1, "shares": 0, "comments": 0} for v in ids]
    ret = {ids[3]: [{"elapsedVideoTimeRatio": r / 100, "audienceWatchRatio": max(0.05, 1 - r / 90), "relativeRetentionPerformance": 0.5}
                    for r in range(1, 101)]}
    raw = {"fetched_at_vn": "x", "start": "2026-12-01", "end": "2026-12-28", "channel": {"title": "ICYFOX", "stats": {"subscriberCount": "10"}},
           "videos": vids, "daily": [{"day": "2026-12-01", "views": 10, "estimatedMinutesWatched": 60, "subscribersGained": 1, "subscribersLost": 0}],
           "per_video": life, "per_video_lifetime": life, "traffic": [{"insightTrafficSourceType": "YT_SEARCH", "views": 5, "estimatedMinutesWatched": 9}],
           "country": [], "content_type": [], "revenue": {"error": "401"}, "first7": first7, "retention": ret}
    (ws / "channel-studio" / "analytics").mkdir(parents=True)
    (ws / "channel-studio" / "analytics" / "video_map.json").write_text(json.dumps({ids[3]: {"pillar": "P3", "series": "documented"}}), encoding="utf-8")
    data = ws / "d.json"
    data.write_text(json.dumps({"raw": raw}), encoding="utf-8")
    r = run(ws, S / "research" / "yt_analytics_report.py", "--replay", data, "--out", ws / "out")
    assert r.returncode == 0, r.stderr
    rep = (ws / "out" / "report.md").read_text(encoding="utf-8")
    assert "THẮNG" in rep and "Video 3" in rep and "P3" in rep and "Rơi mạnh nhất" in rep
    winners = (ws / "channel-studio" / "analytics" / "WINNERS.md").read_text(encoding="utf-8")
    assert "Video 6" in rep and "Video 3" in winners and "Video 6" in winners and "Video 0" not in winners


def test_qa_check_catches_false_word_count(ws):
    f = ws / "part.md"
    body = "# Part 1 · chờ duyệt\n\n### S1 · 0:00–1:00 · x\n> " + "word " * 760 + "\n- Nguồn: a\n\n- Số từ: **khoảng 1.270**\n\n## Nguồn\n- https://a.org\n- https://b.org\n- https://c.org\n"
    f.write_text(body, encoding="utf-8")
    r = run(ws, S / "qa_check.py", f)
    assert r.returncode == 2 and "lệch" in r.stdout
    f.write_text(body.replace("khoảng 1.270", "760"), encoding="utf-8")
    r = run(ws, S / "qa_check.py", f, "--mark")
    assert r.returncode == 0 and "QA ĐẠT" in f.read_text(encoding="utf-8").splitlines()[0]


def test_skill_frontmatter_fits_claude_ai_limits():
    """claude.ai từ chối lưu skill nếu description > 1024 ký tự, name > 64, hoặc có dấu < >."""
    import re
    for skill in (S.parent / "SKILL.md", S.parents[3] / ".agents" / "skills" / "hoang-dung-clay-lapis-studio" / "SKILL.md"):
        fm = skill.read_text(encoding="utf-8").split("---")[1]
        name = re.search(r"(?m)^name:\s*(.+)$", fm).group(1).strip()
        desc = re.search(r'(?m)^description:\s*"(.*)"\s*$', fm).group(1)
        assert len(name) <= 64 and len(desc) <= 1024 and "<" not in desc and ">" not in desc, (skill, len(desc))


def test_watchdog_flags_stalled_overdue_and_log_errors(ws):
    (ws / "channel-studio" / "state" / "jobs").mkdir(parents=True)
    tasks = {"version": 1, "next": 3, "tasks": [
        {"id": "T-001", "title": "Lời đọc", "status": "doing", "updated": "2020-01-01 09:00", "due": None},
        {"id": "T-002", "title": "Gói đăng", "status": "todo", "updated": "2099-01-01 09:00", "due": "2020-01-02"},
        {"id": "T-003", "title": "Đã xong", "status": "done", "updated": "2020-01-01 09:00", "due": "2020-01-02"}]}
    (ws / "channel-studio" / "state" / "tasks.json").write_text(json.dumps(tasks), encoding="utf-8")
    (ws / "channel-studio" / "state" / "jobs" / "voice.log").write_text(
        "S0.1 OK 60.8s\nS2.1 LỖI 429 {'quotaId': 'GenerateRequestsPerDayPerProjectPerModel'}\n", encoding="utf-8")
    (ws / "channel-studio" / "state" / "jobs" / "clean.log").write_text("S0.1 OK\nS0.2 OK\n", encoding="utf-8")
    (ws / "channel-studio" / "state" / "jobs" / "rate.log").write_text('S3.3 LỖI 429 {\n    "code": 429,\n', encoding="utf-8")
    r = run(ws, S / "watchdog.py")
    assert r.returncode == 1, r.stdout + r.stderr
    assert "T-001 NGHI TREO" in r.stdout and "T-002 QUÁ HẠN" in r.stdout and "T-003" not in r.stdout
    assert "voice.log" in r.stdout and "[F1]" in r.stdout and "clean.log" not in r.stdout
    assert "rate.log: Bị giới hạn tốc độ" in r.stdout and "[F10]" in r.stdout


def test_backup_check_skips_when_recent_commit(tmp_path):
    """Phiên cloud dự phòng: có commit mới trên nhánh thì SKIP (mã 3), lâu không có commit thì RUN (mã 0)."""
    import os
    remote, work = tmp_path / "remote.git", tmp_path / "work"
    subprocess.run(["git", "init", "-q", "--bare", str(remote)], check=True)
    subprocess.run(["git", "init", "-q", "-b", "ccr-6640cec8-2anthl", str(work)], check=True)
    (work / "channel-studio").mkdir()
    (work / "AGENT_GUIDE.md").write_text("x")
    env = {**os.environ, "GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@t", "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@t"}
    def commit(date):
        e = {**env, "GIT_AUTHOR_DATE": date, "GIT_COMMITTER_DATE": date}
        subprocess.run(["git", "add", "-A"], cwd=work, check=True)
        subprocess.run(["git", "commit", "-q", "--allow-empty", "-m", "x"], cwd=work, env=e, check=True)
        subprocess.run(["git", "push", "-q", str(remote), "ccr-6640cec8-2anthl"], cwd=work, check=True)
    subprocess.run(["git", "remote", "add", "origin", str(remote)], cwd=work, check=True)
    commit("2001-01-01T00:00:00")
    assert run(work, S / "autopilot.py", "--backup-check").returncode == 0
    commit("now" if False else __import__("datetime").datetime.now().isoformat(timespec="seconds"))
    assert run(work, S / "autopilot.py", "--backup-check").returncode == 3
