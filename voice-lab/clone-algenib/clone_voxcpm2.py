"""Clone giọng Algenib bằng engine VoxCPM2 của VoiceStudio (trọng số Apache-2.0).

Chạy bằng Python của VoiceStudio:
  voice-lab/VoiceStudio/.venv/Scripts/python.exe voice-lab/clone-algenib/clone_voxcpm2.py <script.json> <section_id> [<out.wav>]
Mẫu giọng: algenib_ref.wav + algenib_ref.txt cùng thư mục (cắt từ S0.1 của video 002, Gemini 3.1 Algenib).
"""
import json
import re
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "VoiceStudio" / "backend"))

import soundfile as sf  # noqa: E402
from services.tts_backend import VoxCPM2Backend  # noqa: E402

script, sid = Path(sys.argv[1]), sys.argv[2]
out = Path(sys.argv[3]) if len(sys.argv) > 3 else HERE / f"{sid}_voxcpm2.wav"
secs = {s["id"]: s for s in json.loads(script.read_text(encoding="utf-8"))["sections"]}
sec = secs[sid]
text = sec.get("tts_text") or sec.get("text") or sec.get("narration")
assert text, f"{sid}: không thấy lời đọc trong {list(sec)}"
text = " ".join(re.sub(r"\[[^\]]*\]", " ", text).split())  # thẻ [pause] của Gemini, VoxCPM2 đọc thành chữ

eng = VoxCPM2Backend()
ok, msg = eng.is_available()
assert ok, msg
t0 = time.time()
wav = eng.generate(
    text,
    language="en",
    ref_audio=str(HERE / "algenib_ref.wav"),
    ref_text=(HERE / "algenib_ref.txt").read_text(encoding="utf-8").strip(),
    num_step=10,
    guidance_scale=2.0,
)
# torchaudio.save cần torchcodec, DLL của nó không nạp được trên Windows (WinError 127) nên ghi bằng soundfile
sf.write(str(out), wav.cpu().squeeze(0).numpy(), eng.sample_rate, subtype="PCM_16")
print(json.dumps({"out": str(out), "seconds": round(wav.shape[-1] / eng.sample_rate, 2),
                  "render_s": round(time.time() - t0, 1), "sr": eng.sample_rate}, ensure_ascii=False))
