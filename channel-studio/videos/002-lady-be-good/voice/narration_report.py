# Usage (from OpenMontage root): python narration_report.py <narration_dir> <check_voice.jsonl> <out.md>
# Joins measured duration + loudness (ffmpeg ebur128) with whisper match lines from check_voice.py into one table.
import json, re, subprocess, sys, wave
from pathlib import Path

d, checks, out = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
secs = json.loads(Path("projects/lady-be-good/artifacts/script.json").read_text(encoding="utf-8"))["sections"]
chk = {}
for line in checks.read_text(encoding="utf-8").splitlines():
    if line.startswith("{"):
        j = json.loads(line); chk[j["id"]] = j
rows, total, est, low = [], 0.0, 0, []
for s in secs:
    p = d / f"{s['id']}.wav"
    if not p.exists():
        rows.append(f"| {s['id']} | THIẾU FILE | | | | |"); low.append(s["id"]); continue
    with wave.open(str(p)) as w:
        dur = w.getnframes() / w.getframerate()
    lufs = re.findall(r"I:\s+(-?[\d.]+) LUFS", subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", str(p), "-af", "ebur128", "-f", "null", "-"],
                                                               capture_output=True, text=True).stderr)[-1]
    j = chk.get(s["id"], {})
    m = j.get("match_pct", "chưa kiểm")
    if not isinstance(m, float) or m < 90:
        low.append(s["id"])
    total += dur; est += s["end_seconds"] - s["start_seconds"]
    rows.append(f"| {s['id']} | {dur:.1f} s | {s['end_seconds'] - s['start_seconds']} s | {lufs} | {m} | {'; '.join(j.get('diffs', []))[:220]} |")
md = ["# Báo cáo lời đọc 002 (Algenib, gemini-3.8-flash-tts)", "",
      f"- Tổng độ dài thật: **{int(total // 60)}:{int(total % 60):02d}** (kịch bản ước tính {est // 60}:{est % 60:02d}).",
      f"- Đoạn cần nghe lại (khớp < 90% hoặc thiếu): {', '.join(low) or 'không có'}.",
      "- Khớp = whisper small.en so với kịch bản. Whisper ghi số bằng chữ số (\"12th\", \"1943\") nên đoạn nhiều số sẽ bị tính lệch dù đọc đúng.", "",
      "| Đoạn | Độ dài thật | Kịch bản | LUFS | Khớp % | Chỗ lệch (máy nghe) |", "|---|---|---|---|---|---|", *rows]
out.write_text("\n".join(md) + "\n", encoding="utf-8")
print(f"{len(secs)} đoạn, tổng {total:.0f}s, cần nghe lại: {low}")
