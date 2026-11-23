"""Phụ đề EN cho 002 từ lời kịch bản + mốc từng từ (faster-whisper) của file giọng thật.
Chạy từ gốc OpenMontage: PYTHONUTF8=1 python channel-studio/videos/002-lady-be-good/render/tools/srt.py
Ra: channel-studio/videos/002-lady-be-good/package/subtitles/en.srt
"""
import difflib
import json
import re
import subprocess

import numpy as np
from pathlib import Path

from faster_whisper import WhisperModel

HERE = Path(__file__).resolve().parent
RENDER = HERE.parent
ROOT = HERE.parents[4]
PROJ = ROOT / "projects" / "lady-be-good"
OUT = RENDER.parent / "package" / "subtitles" / "en.srt"
MAXC = 84  # 2 dòng × 42 ký tự


def norm(w):
    return re.sub(r"[^a-z0-9]", "", w.lower())


def chunks(text):
    """Cắt câu thành cụm ≤ MAXC ký tự, ưu tiên ngắt ở dấu câu. Trả về list[list[từ]]."""
    out = []
    for sent in re.split(r"(?<=[.!?])\s+", text):
        words = sent.split()
        cur = []
        for w in words:
            if cur and len(" ".join(cur + [w])) > MAXC:
                # lùi về dấu phẩy gần nhất nếu có, để cụm không đứt giữa ý
                cut = max((i for i, x in enumerate(cur[:-1]) if x[-1] in ",;:"), default=None)
                if cut is not None and cut >= 3:
                    out.append(cur[:cut + 1])
                    cur = cur[cut + 1:]
                else:
                    out.append(cur)
                    cur = []
            cur.append(w)
        if cur:
            out.append(cur)
    return out


def two_lines(words):
    s = " ".join(words)
    if len(s) <= 42:
        return s
    best = min(range(1, len(words)), key=lambda i: abs(len(" ".join(words[:i])) - len(s) / 2))
    return " ".join(words[:best]) + "\n" + " ".join(words[best:])


def ts(t):
    ms = int(round(t * 1000))
    return f"{ms // 3600000:02d}:{ms // 60000 % 60:02d}:{ms // 1000 % 60:02d},{ms % 1000:03d}"


def word_times(script_words, wh):
    """Mốc (start, end) cho từng từ kịch bản: khớp với từ whisper bằng difflib, nội suy chỗ không khớp."""
    a = [norm(w) for w in script_words]
    b = [norm(w["w"]) for w in wh]
    anchors = {}
    for blk in difflib.SequenceMatcher(None, a, b, autojunk=False).get_matching_blocks():
        for k in range(blk.size):
            anchors[blk.a + k] = (wh[blk.b + k]["s"], wh[blk.b + k]["e"])
    keys = sorted(anchors)
    assert len(keys) >= 0.8 * len(a), f"khớp quá ít: {len(keys)}/{len(a)}"
    res = []
    for i in range(len(a)):
        if i in anchors:
            res.append(anchors[i])
            continue
        lo = max((k for k in keys if k < i), default=None)
        hi = min((k for k in keys if k > i), default=None)
        t0 = anchors[lo][1] if lo is not None else wh[0]["s"]
        t1 = anchors[hi][0] if hi is not None else wh[-1]["e"]
        n0 = lo if lo is not None else -1
        n1 = hi if hi is not None else len(a)
        f = (i - n0) / (n1 - n0)
        t = t0 + (t1 - t0) * f
        res.append((t, t))
    return res


def pcm(path):
    # shortcut: tự giải mã bằng ffmpeg vì bản av cài sẵn không nhận tham số metadata_errors của faster-whisper 1.2.1
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(path), "-ac", "1", "-ar", "16000", "-f", "f32le", "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32)


def main():
    tl = json.loads((RENDER / "timeline.json").read_text(encoding="utf-8"))
    start = {s["id"]: s["start"] for s in tl["sections"]}
    script = json.loads((PROJ / "artifacts" / "script.json").read_text(encoding="utf-8"))
    model = WhisperModel("small.en", device="cpu", compute_type="int8", cpu_threads=4)
    cues = []
    for sec in script["sections"]:
        text = re.sub(r"\s+", " ", sec["text"].replace("[pause]", " ")).strip()
        segs, _ = model.transcribe(pcm(PROJ / "assets" / "audio" / "narration_clone" / f"{sec['id']}.wav"),
                                   word_timestamps=True, language="en", beam_size=5)
        wh = [{"w": w.word, "s": w.start, "e": w.end} for s in segs for w in s.words]
        words = text.split()
        times = word_times(words, wh)
        k = 0
        for ch in chunks(text):
            t0, t1 = times[k][0], times[k + len(ch) - 1][1]
            cues.append([start[sec["id"]] + t0, start[sec["id"]] + t1, two_lines(ch)])
            k += len(ch)
        assert k == len(words)
        print(sec["id"], len(words), "từ,", len(wh), "từ whisper")
    for i, c in enumerate(cues):  # tối thiểu 1 s, không chồng cue sau
        nxt = cues[i + 1][0] if i + 1 < len(cues) else c[1] + 2
        c[1] = min(max(c[1] + 0.25, c[0] + 1.0), nxt - 0.05)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("\n".join(f"{i + 1}\n{ts(a)} --> {ts(b)}\n{t}\n" for i, (a, b, t) in enumerate(cues)), encoding="utf-8")
    print(OUT, len(cues), "cue")


if __name__ == "__main__":
    main()
