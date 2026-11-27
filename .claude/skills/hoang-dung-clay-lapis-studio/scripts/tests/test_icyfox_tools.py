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


def test_voicestudio_client_parses_segments_and_blocks_noncommercial(tmp_path):
    import importlib.util
    spec = importlib.util.spec_from_file_location("vs", S / "voice" / "voicestudio_tts.py")
    vs = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(vs)
    md = tmp_path / "p.md"
    md.write_text("# x\n### S0.1 · 0:00 · a\n> Hello there. [pause] World.\n- Giọng: x\n### S0.2 · b\n> Second line.\n", encoding="utf-8")
    segs = vs.segments(md)
    assert [s["id"] for s in segs] == ["S0.1", "S0.2"] and "[pause]" not in segs[0]["text"]
    for bad in ("omnivoice", "tts-1", "audio-cpp", "unknown-engine"):
        with pytest.raises(SystemExit):
            vs.gate(bad)
    assert vs.gate("voxcpm2")[0] == "apache-2.0"


def test_render_gate_rejects_static_video_and_accepts_moving(ws):
    """Cổng chuyển động: video đứng yên 8 giây bị từ chối, video luôn chuyển động được nhận."""
    still, moving = ws / "still.mp4", ws / "moving.mp4"
    frame = ws / "f.png"   # một khung chi tiết, lặp 8 giây, toàn khung I để file > 100 KB
    subprocess.run(["ffmpeg", "-v", "error", "-f", "lavfi", "-i", "testsrc2=s=640x360:d=1", "-frames:v", "1", str(frame)], check=True)
    subprocess.run(["ffmpeg", "-v", "error", "-loop", "1", "-i", str(frame), "-t", "8", "-r", "30", "-c:v", "libx264", "-g", "1",
                    "-pix_fmt", "yuv420p", str(still)], check=True)
    subprocess.run(["ffmpeg", "-v", "error", "-f", "lavfi", "-i", "testsrc2=s=640x360:d=8:r=30", "-c:v", "libx264", "-b:v", "2M",
                    str(moving)], check=True)
    comp = "--component", "Render :: 8 giây, 640x360 :: motion_metrics.py chạy trong tasks.py :: {}"
    for name, expect in (("still.mp4", 2), ("moving.mp4", 0)):
        run(ws, S / "tasks.py", "add", f"render {name}", "--type", "render", "--dod", "đạt mốc chuyển động")
    r = run(ws, S / "tasks.py", "done", "T-001", "--evidence", "still.mp4", "--summary", "Render thử video đứng yên",
            comp[0], comp[1].format("still.mp4"))
    assert r.returncode == 2 and "chưa đạt mốc chuyển động" in r.stdout, r.stdout
    r = run(ws, S / "tasks.py", "done", "T-002", "--evidence", "moving.mp4", "--summary", "Render thử video chuyển động",
            comp[0], comp[1].format("moving.mp4"))
    assert r.returncode == 0, r.stdout + r.stderr


def test_motion_kit_validate_and_build(tmp_path):
    kit = S.parents[3] / "channel-studio" / "motion-kit" / "icyfox_motion.py"
    if not kit.exists():
        pytest.skip("không có motion-kit")
    plan = {"scenes": [{"type": "title", "dur": 5, "text": "T"}, {"type": "quote", "dur": 6, "text": "a b c", "by": "x"},
                       {"type": "stat", "dur": 5, "value": 12, "label": "x"}]}
    pf = tmp_path / "p.json"
    pf.write_text(json.dumps(plan))
    r = subprocess.run([sys.executable, str(kit), "build", str(pf), str(tmp_path / "out")], capture_output=True, text=True)
    assert r.returncode == 0, r.stdout + r.stderr
    body = (tmp_path / "out" / "compositions" / "part0.html").read_text(encoding="utf-8")
    assert 'window.__timelines["part0"]' in body and "Math.random" not in body and (tmp_path / "out" / "assets" / "gsap.min.js").exists()
    bad = {"scenes": [{"type": "photo", "dur": 30, "src": "x.jpg"}]}   # thiếu ghi công
    pf.write_text(json.dumps(bad))
    r = subprocess.run([sys.executable, str(kit), "validate", str(pf)], capture_output=True, text=True)
    assert r.returncode == 2 and "ghi công" in r.stdout


def test_motion_kit_v2_rules_transitions_style_and_sfx(tmp_path):
    kit = S.parents[3] / "channel-studio" / "motion-kit" / "icyfox_motion.py"
    if not kit.exists():
        pytest.skip("không có motion-kit")

    def call(cmd, plan, *extra):
        pf = tmp_path / "p.json"
        pf.write_text(json.dumps(plan))
        return subprocess.run([sys.executable, str(kit), cmd, str(pf), *map(str, extra)], capture_output=True, text=True, encoding="utf-8")

    scenes = [{"type": "title", "dur": 5, "text": "The *Lost* Patrol"}, {"type": "stat", "dur": 5, "value": 9, "label": "days", "big": True},
              {"type": "quote", "dur": 6, "text": "We walked on.", "by": "x"}, {"type": "stat", "dur": 5, "value": 3, "label": "men", "payoff": True},
              {"type": "quote", "dur": 6, "text": "No water left.", "by": "y"}]
    # chuyển cảnh liền nhau trùng kiểu và cắt thẳng quá 1/3 -> hỏng
    bad = [dict(s, transition="cut") if i else s for i, s in enumerate(scenes)]
    r = call("validate", {"genre": "war", "scenes": bad})
    assert r.returncode == 2 and "1/3" in r.stdout
    # chữ không kịp đọc -> hỏng
    r = call("validate", {"scenes": [{"type": "quote", "dur": 3, "text": " ".join(["word"] * 20), "by": "x"}]})
    assert r.returncode == 2
    # style lạ -> hỏng; style hợp lệ -> đạt và đổi bộ chuyển cảnh
    assert call("validate", {"genre": "war", "style": {"nope": 1}, "scenes": scenes}).returncode == 2
    r = call("build", {"genre": "mystery", "style": {"trans": ["dissolve", "dip"]}, "scenes": scenes}, tmp_path / "out")
    assert r.returncode == 0, r.stdout + r.stderr
    cues = json.loads((tmp_path / "out" / "sfx_cues.json").read_text(encoding="utf-8"))
    used = {t for t in cues["transitions"] if t != "none"}
    assert used <= {"dissolve", "dip"} and len(used) == 2
    assert all(a != b for a, b in zip(cues["transitions"][1:], cues["transitions"][2:]))
    kinds = [c["kind"] for c in cues["cues"]]
    assert kinds.count("riser") == 1 and "land" in kinds
    for c in cues["cues"]:                                             # đỉnh âm rơi sau hình đúng 1 khung
        if c["kind"] != "riser" and c["start"] > 0:
            assert abs(c["start"] + c["peak_offset"] - (c["t_picture"] + 1 / 30)) < .01, c
    body = (tmp_path / "out" / "compositions" / "part0.html").read_text(encoding="utf-8")
    assert 'class="w acc"' in body or "acc" in body                    # từ *nhấn* được tô màu
    assert "Math.random" not in body and "Date.now" not in body


def test_new_video_scaffold_and_autopilot_reads_v2(tmp_path):
    r = run(tmp_path, S / "new_video.py", "create", "009-test", "--title", "A Test", "--genre", "war", "--root", tmp_path)
    assert r.returncode == 0, r.stdout + r.stderr
    v = tmp_path / "009-test"
    for p in ("00_brief/script_outline.md", "02_storyboard/motion_plan.json", "03_assets/CREDITS.md", "06_review/REVIEW.md", "03_assets/audio/vo"):
        assert (v / p).exists(), p
    assert json.loads((v / "02_storyboard/motion_plan.json").read_text(encoding="utf-8"))["genre"] == "war"
    (v / "README.md").write_text("đã sửa", encoding="utf-8")
    run(tmp_path, S / "new_video.py", "create", "009-test", "--title", "B", "--genre", "war", "--root", tmp_path)
    assert (v / "README.md").read_text(encoding="utf-8") == "đã sửa"          # không ghi đè
    sys.path.insert(0, str(S))
    import autopilot
    assert autopilot.stage_of(v)[1] == 1
    (v / "01_script" / "script_part1.md").write_text("x", encoding="utf-8")
    assert autopilot.stage_of(v)[1] == 2
    cues = tmp_path / "c.json"
    cues.write_text(json.dumps({"genre": "war", "transitions": ["none", "dip"], "cues": [{"t_picture": 1.0, "start": .9, "kind": "land", "file": "a/b.mp3", "volume": .5, "scene": "s0"}]}))
    assert run(tmp_path, S / "new_video.py", "cuesheet", cues, v / "05_sound/CUE_SHEET.md").returncode == 0
    assert "tiêu đề đáp" in (v / "05_sound/CUE_SHEET.md").read_text(encoding="utf-8")


def test_vfx_rules_chunking_and_assets(tmp_path):
    kit = S.parents[3] / "channel-studio" / "motion-kit" / "icyfox_motion.py"
    if not kit.exists():
        pytest.skip("không có motion-kit")

    def call(cmd, plan, *extra):
        pf = tmp_path / "p.json"
        pf.write_text(json.dumps(plan))
        return subprocess.run([sys.executable, str(kit), cmd, str(pf), *map(str, extra)], capture_output=True, text=True, encoding="utf-8")

    q = lambda t, **k: dict({"type": "quote", "dur": 7, "text": t, "by": "x"}, **k)
    # lóe > 3 lần / giây: tia chớp (2 lần) + nổ (1) + chuyển cảnh flash (1) trong 1 giây -> hỏng
    bad = {"genre": "war", "scenes": [q("a b", dur=9, vfx=[{"fx": "lightning", "at": 8.6}]),
                                      q("c d", transition="flash", vfx=[{"fx": "explosion", "at": 0.1}])]}
    r = call("validate", bad)
    assert r.returncode == 2 and "WCAG" in r.stdout
    assert call("validate", {"scenes": [q("a", vfx=["rain", "fog", "snow"])]}).returncode == 2        # > 2 lớp không khí
    assert call("validate", {"scenes": [q("a", vfx=["lava"])]}).returncode == 2                       # tên lạ
    assert call("validate", {"scenes": [q("a", vfx=[{"fx": "shake", "at": 20}])]}).returncode == 2   # ngoài cảnh
    r = call("validate", {"genre": "ancient", "scenes": [q("a", vfx=["caustics"])]})
    assert r.returncode == 0 and "cảnh báo" in r.stdout                                             # ngoài bảng thể loại: chỉ cảnh báo
    # dựng: 8 cảnh -> 2 composition (chunk 6, hoặc ngắt ở chapter), mốc thời gian tương đối, kết cấu + tiếng được chép
    scenes = [q(f"line {i}", vfx=(["rain", {"fx": "lightning", "at": 3}] if i == 2 else ["embers"] if i == 7 else []), chapter=(i == 4))
              for i in range(8)]
    r = call("build", {"genre": "survival", "scenes": scenes}, tmp_path / "out")
    assert r.returncode == 0, r.stdout + r.stderr
    out = tmp_path / "out"
    parts = sorted(p.name for p in (out / "compositions").glob("part*.html"))
    assert parts == ["part0.html", "part1.html"]
    p1 = (out / "compositions" / "part1.html").read_text(encoding="utf-8")
    import re as _re
    times = [float(x) for x in _re.findall(r",(-?\d+\.\d+)\);", p1)]
    assert times and min(times) >= -0.01 and max(times) < 40                                       # tương đối theo composition
    for f in ("assets/vfx/rain.png", "assets/vfx/embers.png", "assets/sfx/thunder.mp3"):
        assert (out / f).exists(), f
    idx = (out / "index.html").read_text(encoding="utf-8")
    assert 'data-composition-src="compositions/part1.html"' in idx
    real = (S.parents[3] / "channel-studio" / "motion-kit" / "sfx" / "real" / "rain-loop.mp3").exists()
    assert ("rain-loop.mp3" in idx) == real                                                        # tiếng nền tổng hợp tắt (24/11)
    cues = json.loads((out / "sfx_cues.json").read_text(encoding="utf-8"))["cues"]
    th = [c for c in cues if c["kind"] == "thunder"][0]
    assert real or th["volume"] <= .6 * .45 + 1e-6                                                 # sấm tổng hợp nhỏ
    assert all('data-duration=' in a for a in _re.findall(r"<audio[^>]+>", idx))                   # mọi tiếng có độ dài
    body = (out / "compositions" / "part0.html").read_text(encoding="utf-8")
    assert "Math.random" not in body and "Date.now" not in body


def test_real_sound_override_and_seamless_loop(tmp_path, monkeypatch):
    mk = S.parents[3] / "channel-studio" / "motion-kit"
    if not (mk / "freesound_fetch.py").exists():
        pytest.skip("không có motion-kit")
    sys.path.insert(0, str(mk))
    import numpy as np
    import freesound_fetch as ff_
    import icyfox_motion as im
    sr = 48000
    t = np.arange(int(40 * sr)) / sr
    x = np.stack([np.sin(2 * np.pi * 3.3 * t) * .5] * 2, 1).astype(np.float32)   # tín hiệu không tuần hoàn theo 30 s
    y = ff_.loop_seamless(x, sr)
    assert len(y) == 30 * sr
    assert abs(float(y[0, 0] - y[-1, 0])) < 5 * float(np.abs(np.diff(y[:, 0])).mean()) + 1e-3   # chỗ nối liền
    with pytest.raises(ValueError):
        ff_.loop_seamless(x[: 20 * sr], sr)                                                  # quá ngắn: từ chối
    # có sfx/real/<tên>.mp3 thì kit dùng bản thật thay bản tổng hợp
    monkeypatch.setattr(im, "SFX_DIR", tmp_path)
    (tmp_path / "synth").mkdir()
    (tmp_path / "synth" / "boom.mp3").write_bytes(b"x")
    assert im.sfx_path("synth/boom") == tmp_path / "synth" / "boom.mp3"
    (tmp_path / "real").mkdir()
    (tmp_path / "real" / "boom.mp3").write_bytes(b"x")
    assert im.sfx_path("synth/boom") == tmp_path / "real" / "boom.mp3"
    assert im.sfx_path("whoosh") == tmp_path / "whoosh.mp3"


def test_yt_channel_selects_second_channel_keys_and_data_dir(ws):
    import os
    code = f"import sys; sys.path.insert(0, {str(S)!r}); import icyfox_common as c; print(c.CS.name, *c.yt_vars())"
    base = {k: v for k, v in os.environ.items() if k != "YT_CHANNEL"}
    out = lambda env: subprocess.run([PY, "-c", code], cwd=ws, env=env, capture_output=True, text=True).stdout.split()
    assert out(base) == ["channel-studio", "YT_CLIENT_ID", "YT_CLIENT_SECRET", "YT_REFRESH_TOKEN"]
    assert out({**base, "YT_CHANNEL": "us"}) == ["channel-studio-us", "YT_US_CLIENT_ID", "YT_US_CLIENT_SECRET", "YT_US_REFRESH_TOKEN"]
