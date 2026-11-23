"""Đo nét giọng để so clone với Gemini: cao độ (F0), độ rộng ngữ điệu, tốc độ, khoảng lặng, độ sáng.

voice-lab/VoiceStudio/.venv/Scripts/python.exe voice_profile.py <wav> [<wav> ...]
"""
import json
import subprocess
import sys

import librosa
import numpy as np


def load(p, sr=16000):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", p, "-f", "f32le", "-ac", "1", "-ar", str(sr), "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32).copy(), sr


for p in sys.argv[1:]:
    y, sr = load(p)
    f0, voiced, _ = librosa.pyin(y, fmin=60, fmax=400, sr=sr, frame_length=1024)
    f0 = f0[voiced & ~np.isnan(f0)]
    semis = 12 * np.log2(f0 / np.median(f0))
    rms = librosa.feature.rms(y=y, frame_length=1024, hop_length=256)[0]
    silent = rms < 0.1 * np.median(rms[rms > 0])
    # khoảng lặng > 0,25 s
    runs, n = [], 0
    for s in silent:
        n = n + 1 if s else (runs.append(n) or 0)
    runs.append(n)
    pauses = [r * 256 / sr for r in runs if r * 256 / sr > 0.25]
    cent = librosa.feature.spectral_centroid(y=y, sr=sr)[0]
    print(json.dumps({
        "file": p.replace("\\", "/").split("/")[-1],
        "dur_s": round(len(y) / sr, 2),
        "f0_median_hz": round(float(np.median(f0)), 1),
        "f0_range_semitones_p10_p90": round(float(np.percentile(semis, 90) - np.percentile(semis, 10)), 2),
        "pauses_gt_0.25s": len(pauses),
        "pause_total_s": round(sum(pauses), 2),
        "speech_s": round(len(y) / sr - sum(pauses), 2),
        "brightness_centroid_hz": round(float(np.median(cent)), 0),
    }, ensure_ascii=False))
