"""Cắt đoạn giọng mẫu Algenib ~15 s đúng ranh giới câu + lời đọc khớp (để clone)."""
import json
import subprocess
import sys
from pathlib import Path

from faster_whisper import WhisperModel

src, out_dir = Path(sys.argv[1]), Path(sys.argv[2])
out_dir.mkdir(parents=True, exist_ok=True)
# F6: PyAV lỗi trên máy này, giải mã bằng ffmpeg ra float32 16 kHz mono
import numpy as np
pcm = subprocess.run(["ffmpeg", "-v", "error", "-i", str(src), "-f", "f32le", "-ac", "1", "-ar", "16000", "-"], capture_output=True, check=True).stdout
segs, _ = WhisperModel("small.en", device="cpu", compute_type="int8", cpu_threads=2).transcribe(np.frombuffer(pcm, np.float32), language="en")
picked, end = [], 0.0
for s in segs:
    if s.end > 20.0:
        break
    picked.append(s.text.strip())
    end = s.end
    if end >= 12.0 and s.text.strip().endswith((".", "!", "?")):
        break
assert picked and 8.0 <= end <= 20.0, (end, picked)
wav = out_dir / "algenib_ref.wav"
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(src), "-t", f"{end + 0.25:.2f}", "-ac", "1", "-ar", "24000", str(wav)], check=True)
text = " ".join(picked)
(out_dir / "algenib_ref.txt").write_text(text + "\n", encoding="utf-8")
print(json.dumps({"wav": str(wav), "seconds": round(end + 0.25, 2), "text": text}, ensure_ascii=False))
