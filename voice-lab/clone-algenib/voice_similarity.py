"""Độ giống giọng (cosine ECAPA, speechbrain/spkrec-ecapa-voxceleb) giữa mẫu Algenib và các file khác.

voice-lab/VoiceStudio/.venv/Scripts/python.exe voice_similarity.py <ref.wav> <wav> [<wav> ...]
Mốc: cùng người nói thường > 0.6, khác người thường < 0.4 (tự so thêm giọng khác làm mốc).
"""
import json
import subprocess
import sys
from pathlib import Path

import numpy as np
import torch
from speechbrain.inference.speaker import EncoderClassifier
from speechbrain.utils.fetching import LocalStrategy


def load16k(p):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", p, "-f", "f32le", "-ac", "1", "-ar", "16000", "-"],
                         capture_output=True, check=True).stdout
    return torch.from_numpy(np.frombuffer(raw, np.float32).copy()).unsqueeze(0)


enc = EncoderClassifier.from_hparams("speechbrain/spkrec-ecapa-voxceleb",
                                     savedir=str(Path.home() / ".cache" / "spkrec-ecapa-voxceleb"),
                                     local_strategy=LocalStrategy.COPY)  # Windows không cho symlink (WinError 1314)
emb = lambda p: torch.nn.functional.normalize(enc.encode_batch(load16k(p)).squeeze(), dim=0)
ref = emb(sys.argv[1])
assert abs(float(ref @ ref) - 1) < 1e-4
for p in sys.argv[2:]:
    print(json.dumps({"file": p.replace("\\", "/").split("/")[-1], "dir": Path(p).parent.name,
                      "cosine": round(float(ref @ emb(p)), 3)}, ensure_ascii=False))
