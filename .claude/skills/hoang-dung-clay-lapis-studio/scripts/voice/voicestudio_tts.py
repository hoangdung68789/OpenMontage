"""Giọng đọc ICYFOX bằng VoiceStudio (anh chốt 23/11/2026: "sử dụng repo voicestudio để tạo voice").

VoiceStudio chạy trên máy anh: app desktop, hoặc backend `uv run uvicorn backend.main:app --port 3900`.
Script gọi API kiểu OpenAI của nó: POST {base}/v1/audio/speech. Gọi từ chính máy đó (loopback) thì không cần khóa.

  python voicestudio_tts.py check   [--base http://127.0.0.1:3900]
  python voicestudio_tts.py sample  --text "..." --out mau.wav [--engine voxcpm2] [--voice <hồ sơ giọng>] [--instruct "..."]
  python voicestudio_tts.py narrate <script_partN.md> --out-dir <thư mục> [--engine voxcpm2] [--voice icyfox-narrator] [--only S1.1,S1.2]

GIẤY PHÉP (bắt buộc, kênh ICYFOX có kiếm tiền):
- Chỉ dùng engine có trọng số theo giấy phép cho phép thương mại (Apache-2.0, MIT), theo thẻ mô hình gốc.
  Nguồn: voicestudio/backend/config/model_licenses.json. VoiceStudio ghi "unreviewed", tức chưa tự xác nhận quyền
  thương mại, nên mỗi engine vẫn phải đối chiếu thẻ mô hình gốc trước khi đăng video.
- CẤM OmniVoice (mặc định của VoiceStudio: CC-BY-NC, không thương mại), audio.cpp Breeze, OuteTTS, PocketTTS bản chuyển đổi.
- Không nhân bản giọng người thật. Giọng kênh là giọng tự thiết kế (voice design của VoxCPM2), lưu thành hồ sơ "icyfox-narrator".
"""
import argparse
import json
import re
import subprocess
import sys
import time
import wave
from pathlib import Path

import requests

# engine id của VoiceStudio -> (giấy phép trọng số theo model_licenses.json, link thẻ mô hình)
ALLOWED = {
    "voxcpm2": ("apache-2.0", "https://huggingface.co/openbmb/VoxCPM2"),
    "kittentts": ("apache-2.0", "https://huggingface.co/KittenML/kitten-tts-mini-0.8"),
    "cosyvoice": ("apache-2.0", "https://huggingface.co/FunAudioLLM/Fun-CosyVoice3-0.5B-2512"),
    "moss-tts-nano": ("apache-2.0", "https://huggingface.co/OpenMOSS-Team/MOSS-TTS-Nano-100M"),
    "ming-tts": ("mit", "https://huggingface.co/inclusionAI/Ming-3.0-tts-0.5b"),
}
BLOCKED = {"omnivoice", "omnivoice-gguf", "omnivoice-subprocess", "audio-cpp", "pockettts", "tts-1", "tts-1-hd",
           "gpt-4o-mini-tts"}  # tts-1… là bí danh của engine đang bật (thường là OmniVoice) nên cũng cấm


def gate(engine):
    if engine in BLOCKED or engine not in ALLOWED:
        sys.exit(f"Engine '{engine}' không nằm trong danh sách được phép dùng thương mại: {', '.join(ALLOWED)}. "
                 "OmniVoice (mặc định) là CC-BY-NC, cấm dùng cho video kiếm tiền.")
    return ALLOWED[engine]


def utf8():
    for s in (sys.stdout, sys.stderr):
        try:
            s.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass


def speech(base, engine, text, voice=None, instruct=None, fmt="wav", timeout=900):
    body = {"model": engine, "input": text, "response_format": fmt}
    if voice:
        body["voice"] = voice
    if instruct:
        body["instruct"] = instruct
    r = requests.post(f"{base}/v1/audio/speech", json=body, timeout=timeout)
    if not r.ok:
        raise RuntimeError(f"VoiceStudio {r.status_code}: {r.text[:300]}")
    return r.content


def wav_seconds(path):
    try:
        with wave.open(str(path)) as w:
            return round(w.getnframes() / float(w.getframerate()), 2)
    except Exception:
        r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)],
                           capture_output=True, text=True)
        return round(float(r.stdout.strip() or 0), 2)


def segments(md):
    """Đọc script_partN.md: mỗi '### S1.2 · …' là một đoạn; lời đọc là các dòng bắt đầu bằng '> '."""
    out, cur = [], None
    for line in Path(md).read_text(encoding="utf-8").splitlines():
        m = re.match(r"^###\s+(S[\d.]+)", line)
        if m:
            cur = {"id": m.group(1), "text": []}
            out.append(cur)
        elif line.startswith("> ") and cur is not None:
            cur["text"].append(line[2:].strip())
    for s in out:
        t = " ".join(s["text"])
        t = re.sub(r"\[pause\]", "... ", t)  # ngừng nhẹ, engine nào cũng đọc được
        s["text"] = re.sub(r"\s+", " ", t).strip()
    return [s for s in out if s["text"]]


def main():
    utf8()
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--base", default="http://127.0.0.1:3900")
    sp = ap.add_subparsers(dest="cmd", required=True)
    sp.add_parser("check")
    s = sp.add_parser("sample")
    s.add_argument("--text", required=True)
    s.add_argument("--out", required=True)
    n = sp.add_parser("narrate")
    n.add_argument("script")
    n.add_argument("--out-dir", required=True)
    n.add_argument("--only", default="")
    for p in (s, n):
        p.add_argument("--engine", default="voxcpm2")
        p.add_argument("--voice", default=None, help="hồ sơ giọng trong VoiceStudio, ví dụ icyfox-narrator")
        p.add_argument("--instruct", default=None, help="chỉ dẫn phong cách đọc")
    a = ap.parse_args()

    if a.cmd == "check":
        try:
            r = requests.get(f"{a.base}/v1/models", timeout=20)
        except requests.RequestException as e:
            sys.exit(f"Không kết nối được VoiceStudio ở {a.base}: {e}. Mở app VoiceStudio (hoặc chạy backend cổng 3900) rồi thử lại.")
        ids = [m.get("id") for m in r.json().get("data", [])] if r.ok else []
        print(f"VoiceStudio OK ({a.base}). Engine/model thấy được: {', '.join(ids) or '(trống)'}")
        ok = [e for e in ALLOWED if e in ids]
        print("Engine được phép dùng thương mại đang có:", ", ".join(ok) or "CHƯA CÓ, cài VoxCPM2 trong Model Catalogue")
        return

    lic, card = gate(a.engine)
    if a.cmd == "sample":
        Path(a.out).parent.mkdir(parents=True, exist_ok=True)
        t0 = time.time()
        Path(a.out).write_bytes(speech(a.base, a.engine, a.text, a.voice, a.instruct))
        print(f"Đã tạo {a.out}: {wav_seconds(a.out)} giây, mất {time.time() - t0:.1f} giây ({a.engine}, {lic})")
        return

    segs = segments(a.script)
    only = {x.strip() for x in a.only.split(",") if x.strip()}
    out = Path(a.out_dir)
    out.mkdir(parents=True, exist_ok=True)
    man_f = out / "manifest.json"
    man = json.loads(man_f.read_text(encoding="utf-8")) if man_f.exists() else {"segments": {}}
    man.update({"engine": a.engine, "license": lic, "model_card": card, "voice": a.voice, "instruct": a.instruct,
                "source_script": str(a.script)})
    done = 0
    for sg in segs:
        if only and sg["id"] not in only:
            continue
        f = out / f"{sg['id']}.wav"
        if f.exists() and f.stat().st_size > 1000:
            continue  # chạy lại thì làm tiếp đoạn còn thiếu
        t0 = time.time()
        try:
            f.write_bytes(speech(a.base, a.engine, sg["text"], a.voice, a.instruct))
        except Exception as e:  # dừng sạch, ghi lỗi, lần sau chạy tiếp
            man["last_error"] = f"{sg['id']}: {e}"
            man_f.write_text(json.dumps(man, ensure_ascii=False, indent=1), encoding="utf-8")
            sys.exit(f"Lỗi ở {sg['id']}: {e}")
        words = len(sg["text"].split())
        secs = wav_seconds(f)
        man["segments"][sg["id"]] = {"file": f.name, "words": words, "seconds": secs,
                                     "wpm": round(words / secs * 60, 1) if secs else None, "gen_seconds": round(time.time() - t0, 1)}
        done += 1
        print(f"  {sg['id']}: {secs} giây, {words} từ")
    man.pop("last_error", None)
    tot = sum(v["seconds"] or 0 for v in man["segments"].values())
    man["total_seconds"] = round(tot, 1)
    man_f.write_text(json.dumps(man, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"Xong {done} đoạn mới; tổng {len(man['segments'])}/{len(segs)} đoạn, {tot / 60:.1f} phút. Manifest: {man_f}")


if __name__ == "__main__":
    main()
