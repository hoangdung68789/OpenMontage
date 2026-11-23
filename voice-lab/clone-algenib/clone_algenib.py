"""Clone giọng Algenib bằng engine của VoiceStudio: VoxCPM2 hoặc Qwen3-TTS Base (cả hai trọng số Apache-2.0).

voice-lab/VoiceStudio/.venv/Scripts/python.exe voice-lab/clone-algenib/clone_algenib.py <script.json> <section_id>
    [--engine voxcpm2|qwen3] [--ref algenib_ref] [--out X.wav] [--chunk] [--instruct "..."] [--steps 10]
--ref: tên mẫu trong thư mục này (<ref>.wav + <ref>.txt), cắt bằng make_ref.py từ giọng Gemini 3.1 Algenib.
--chunk: đọc từng câu, chèn khoảng lặng theo nhịp Gemini (đo 23/11: lặng chiếm 25–35% thời lượng).
"""
import argparse
import json
import os
import re
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "VoiceStudio" / "backend"))

import numpy as np  # noqa: E402
import soundfile as sf  # noqa: E402

# Khoảng lặng sau mỗi khúc (giây): đo trên 10 đoạn Gemini của 002, trung bình 0,55–1,1 s mỗi chỗ nghỉ
GAP = {"sentence": 0.55, "pause": 1.0, "long pause": 1.7, "end": 0.3}

ap = argparse.ArgumentParser()
ap.add_argument("script")
ap.add_argument("sid")
ap.add_argument("--engine", choices=["voxcpm2", "qwen3"], default="voxcpm2")
ap.add_argument("--ref", default="algenib_ref")
ap.add_argument("--seed", type=int, default=7)
ap.add_argument("--out")
ap.add_argument("--chunk", action="store_true")
ap.add_argument("--instruct")
ap.add_argument("--steps", type=int, default=10)
ap.add_argument("--gap-scale", type=float, default=1.0, help="nhân khoảng lặng giữa câu (chỉ tách ở cuối câu nên bù chỗ nghỉ ở dấu phẩy)")
a = ap.parse_args()

sec = {s["id"]: s for s in json.loads(Path(a.script).read_text(encoding="utf-8"))["sections"]}[a.sid]
text = sec.get("tts_text") or sec.get("text")
assert text, f"{a.sid}: không thấy lời đọc trong {list(sec)}"
out = Path(a.out) if a.out else HERE / f"{a.sid}_{a.engine}.wav"


def pieces(t):
    """[(câu, khoảng lặng sau nó)]: tách ở [pause]/[long pause] rồi ở cuối câu."""
    res = []
    for part, tag in re.findall(r"(.*?)(?:\[(long pause|pause)\]|$)", t, re.S):
        sents = [s for s in re.split(r"(?<=[.!?…])\s+", " ".join(part.split())) if s.strip()]
        for i, s in enumerate(sents):
            res.append((s, GAP[tag] if (tag and i == len(sents) - 1) else GAP["sentence"]))
    if res:
        res[-1] = (res[-1][0], GAP["end"])
    return res


chunks = pieces(text) if a.chunk else [(" ".join(re.sub(r"\[[^\]]*\]", " ", text).split()), 0.0)]
assert chunks and all(c for c, _ in chunks)

if a.engine == "qwen3":
    os.environ.setdefault("VOICESTUDIO_QWEN_CUDA_MODEL", str(Path.home() / ".cache" / "qwen3-tts" / "1.7B-Base"))
    from services.qwen_cuda import QwenCUDABackend as Engine
else:
    from services.tts_backend import VoxCPM2Backend as Engine
eng = Engine()
ok, msg = eng.is_available()
assert ok, msg
ref_wav, ref_txt = HERE / f"{a.ref}.wav", (HERE / f"{a.ref}.txt").read_text(encoding="utf-8").strip()
t0, parts = time.time(), []
for c, gap in chunks:
    kw = dict(language="en", ref_audio=str(ref_wav))
    if a.engine == "qwen3":  # Qwen cần ref_text, không có num_step/instruct
        kw.update(ref_text=ref_txt, seed=a.seed)
    elif a.instruct:
        kw.update(num_step=a.steps, guidance_scale=2.0, instruct=a.instruct)  # chế độ có chỉ dẫn: mẫu chỉ lấy âm sắc, bỏ ref_text
    else:
        kw.update(num_step=a.steps, guidance_scale=2.0, ref_text=ref_txt)
    parts += [eng.generate(c, **kw).cpu().squeeze(0).numpy(), np.zeros(int(gap * a.gap_scale * eng.sample_rate), np.float32)]
wav = np.concatenate(parts)
# torchaudio.save cần torchcodec, DLL của nó không nạp được trên Windows (WinError 127) nên ghi bằng soundfile
sf.write(str(out), wav, eng.sample_rate, subtype="PCM_16")
print(json.dumps({"out": str(out), "chunks": len(chunks), "seconds": round(len(wav) / eng.sample_rate, 2),
                  "render_s": round(time.time() - t0, 1), "sr": eng.sample_rate}, ensure_ascii=False))
