# Usage: retime.py <script_partN.md> <start MM:SS>  -> fills section times, +Ns visual cues, title range, word count
import re, sys
from pathlib import Path
p = Path(sys.argv[1]); t = p.read_text(encoding="utf-8")
def sec(s): m, x = s.split(":"); return int(m)*60+int(x)
def fmt(n): return f"{n//60:02d}:{n%60:02d}"
cur = start = sec(sys.argv[2])
parts = re.split(r"(?m)^(### .*)$", t); out = [parts[0]]
for i in range(1, len(parts), 2):
    head, body = parts[i], parts[i+1]
    m = re.match(r"### (S[\d.]+) · [\d:]+–[\d:]+ · (.*)", head)
    nar = " ".join(l[2:] for l in body.splitlines() if l.startswith("> "))
    n = len(re.findall(r"[a-z0-9']+", nar.replace("[pause]", " ").replace("[long pause]", " ").lower()))
    dur = round(n/125*60 + nar.count("[pause]")*0.6 + nar.count("[long pause]")*1.2)
    n0 = cur
    body = re.sub(r"(?m)^(  - )\+(\d+)s:", lambda k: k.group(1)+fmt(min(n0+int(k.group(2)), n0+dur-1))+":", body)
    out += [f"### {m.group(1)} · {fmt(n0)}–{fmt(n0+dur)} · {m.group(2)}", body]; cur = n0 + dur
t = "".join(out)
words = len(re.findall(r"[a-z0-9']+", "\n".join(l[2:] for l in t.splitlines() if l.startswith("> ")).replace("[pause]", " ").lower()))
t = re.sub(r"(Phần \d/4 \()[\d:]+–[\d:]+\)", lambda k: f"{k.group(1)}{fmt(start)}–{fmt(cur)})", t, count=1)
t = t.replace("- Số từ: tính bằng máy khi chạy QA (xem dòng tiêu đề). Mốc giờ tính lại bằng máy.",
              f"- Số từ: **khoảng {words}** (đếm bằng máy). Đọc xong lúc **khoảng {fmt(cur)}** (125 từ/phút, đã tính chỗ ngừng; căn lại theo giọng thật).")
p.write_text(t, encoding="utf-8"); print(words, fmt(start), "->", fmt(cur))
