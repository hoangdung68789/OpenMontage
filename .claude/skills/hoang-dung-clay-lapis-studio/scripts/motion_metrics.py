"""Đo độ chuyển động của video (QA trước khi trình anh, và so với đối thủ).

Dùng: python motion_metrics.py a.mp4 [b.mp4 ...]
In mỗi file: static_pct (freezedetect -60dB, d=3), longest_static, sec_per_change
(đổi hình: cắt hoặc hòa tan, chênh ảnh xám 64x36 cách 1 s > 18), pct_still (giây gần như không đổi).
Mốc đối thủ 23/11/2026: channel-studio/research/2026-11-23-motion/BAO_CAO_CHUYEN_DONG.md
"""
import pathlib, re, subprocess, sys
import numpy as np

W, H = 64, 36


def metrics(p):
    d = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p],
                             capture_output=True, text=True).stdout)
    fz = subprocess.run(["ffmpeg", "-nostats", "-hide_banner", "-i", p, "-an", "-vf",
                         "scale=480:-2,freezedetect=n=-60dB:d=3", "-f", "null", "-"],
                        capture_output=True, text=True, encoding="utf-8", errors="ignore").stderr
    fr = [float(x) for x in re.findall(r"freeze_duration: ([\d.]+)", fz)]
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", p, "-an", "-vf", f"fps=2,scale={W}:{H},format=gray",
                          "-f", "rawvideo", "-"], capture_output=True).stdout
    f = np.frombuffer(raw, np.uint8).reshape(-1, H, W).astype(np.float32)
    diff = np.abs(f[2:] - f[:-2]).mean(axis=(1, 2))  # chênh lệch cách 1 giây
    ev, last = 0, -99
    for i, v in enumerate(diff):
        if v > 18 and i - last > 3:
            ev, last = ev + 1, i
    return {"sec": round(d, 1), "static_pct": round(100 * sum(fr) / d, 1), "longest_static": round(max(fr, default=0), 1),
            "sec_per_change": round(d / max(ev, 1), 1), "pct_still": round(100 * float(np.mean(diff <= 1.0)), 1)}


if __name__ == "__main__":
    for p in sys.argv[1:]:
        m = metrics(p)
        assert 0 <= m["static_pct"] <= 100.5, m
        print(pathlib.Path(p).name, m, flush=True)
