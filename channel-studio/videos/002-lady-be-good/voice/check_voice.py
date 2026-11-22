# Usage (from OpenMontage root): python check_voice.py <wav> [<wav> ...]
# File name must start with the section id (S5.5.wav, S5.5_Algenib.wav). Compares whisper transcript with script.json.
# Runs at Idle priority on 2 CPU threads so the machine stays usable.
import ctypes, difflib, json, re, subprocess, sys
from pathlib import Path
import numpy as np
from faster_whisper import WhisperModel

ctypes.windll.kernel32.SetPriorityClass(ctypes.windll.kernel32.GetCurrentProcess(), 0x40)  # IDLE_PRIORITY_CLASS
ref = {s["id"]: s["text"] for s in json.loads(Path("projects/lady-be-good/artifacts/script.json").read_text(encoding="utf-8"))["sections"]}
norm = lambda t: re.findall(r"[a-z0-9']+", t.replace("[long pause]", " ").replace("[pause]", " ").replace("-", " ").lower())
model = WhisperModel("small.en", device="cpu", compute_type="int8", cpu_threads=2)
for f in sys.argv[1:]:
    sid = Path(f).stem.split("_")[0]
    raw = subprocess.run(["ffmpeg", "-loglevel", "error", "-i", f, "-f", "f32le", "-ac", "1", "-ar", "16000", "-"],
                         capture_output=True, check=True).stdout
    segs, _ = model.transcribe(np.frombuffer(raw, np.float32), beam_size=5, language="en")
    R, H = norm(ref[sid]), norm(" ".join(s.text for s in segs))
    sm = difflib.SequenceMatcher(a=R, b=H, autojunk=False)
    diffs = [f"{op}: '{' '.join(R[i1:i2])}' -> '{' '.join(H[j1:j2])}'" for op, i1, i2, j1, j2 in sm.get_opcodes() if op != "equal"]
    print(json.dumps({"file": Path(f).name, "id": sid, "match_pct": round(sm.ratio() * 100, 1),
                      "ref_words": len(R), "heard_words": len(H), "diffs": diffs}, ensure_ascii=False), flush=True)
