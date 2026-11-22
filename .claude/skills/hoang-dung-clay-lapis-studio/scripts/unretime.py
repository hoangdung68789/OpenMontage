# Usage: unretime.py <file>  -> absolute visual cues back to +Ns, restore word-count placeholder (so retime.py can run again)
import re, sys
from pathlib import Path
p = Path(sys.argv[1]); t = p.read_text(encoding="utf-8")
def sec(s): m, x = s.split(":"); return int(m)*60+int(x)
parts = re.split(r"(?m)^(### .*)$", t); out = [parts[0]]
for i in range(1, len(parts), 2):
    head, body = parts[i], parts[i+1]
    s0 = sec(re.match(r"### S[\d.]+ · ([\d:]+)–", head).group(1))
    body = re.sub(r"(?m)^(  - )(\d\d:\d\d):", lambda k: f"{k.group(1)}+{sec(k.group(2))-s0}s:", body)
    out += [head, body]
t = "".join(out)
t = re.sub(r"- Số từ: \*\*khoảng \d+\*\* \(đếm bằng máy\)\. Đọc xong lúc .*", "- Số từ: tính bằng máy khi chạy QA (xem dòng tiêu đề). Mốc giờ tính lại bằng máy.", t)
p.write_text(t, encoding="utf-8"); print("ok")
