"""Thay tiếng tự tổng hợp (sfx/synth/) bằng bản thu thật CC0 từ Freesound.

  python freesound_fetch.py search            # chỉ tìm, in ứng viên (không tải)
  python freesound_fetch.py fetch [--only rain-loop,boom] [--pick 1]   # tải, xử lý, ghi sfx/real/ + CREDITS
  python freesound_fetch.py fetch --replace   # tải lại cả file đã có

Khóa: biến môi trường FREESOUND_API_KEY; nếu không có, gửi khóa giả để proxy của môi trường cloud chèn khóa thật
(Network secret cho freesound.org). Chỉ nhận giấy phép "Creative Commons 0" (lọc ngay trong truy vấn, kiểm lại khi tải).
Tải bản preview-hq-mp3 (API cho tải bằng khóa; file gốc cần OAuth2).

Xử lý sau khi tải:
- tiếng nền (…-loop): cắt 30 giây, nối vòng bằng crossfade đuôi vào đầu (không nghe chỗ nối), chuẩn -24 LUFS;
- tiếng sự kiện: cắt khoảng lặng đầu, giữ tối đa 8 giây, fade cuối, đỉnh -1 dBFS.
Kit tự dùng sfx/real/<tên>.mp3 nếu có, không thì dùng sfx/synth/<tên>.mp3.
"""
import argparse
import json
import os
import subprocess
import sys
import tempfile
import urllib.parse
import urllib.request
from datetime import date
from pathlib import Path

HERE = Path(__file__).resolve().parent
REAL = HERE / "sfx" / "real"
API = "https://freesound.org/apiv2"
CC0 = "Creative Commons 0"
# tên đích -> (truy vấn, khoảng thời lượng giây, là vòng lặp?)
TARGETS = {
    "rain-loop": ("rain heavy ambience", (34, 900), True),
    "wind-loop": ("wind desert howling ambience", (34, 900), True),
    "fire-loop": ("fire crackling burning ambience", (34, 900), True),
    "underwater-loop": ("underwater ambience bubbles", (34, 900), True),
    "radio-static": ("radio static noise interference", (1, 20), False),
    "thunder": ("thunder clap rumble", (3, 30), False),
    "boom": ("explosion distant boom", (1.5, 15), False),
    "sparks": ("electric sparks", (0.5, 10), False),
}
FIELDS = "id,name,username,license,duration,previews,url,avg_rating,num_downloads,samplerate"


def call(url):
    key = os.environ.get("FREESOUND_API_KEY", "proxy-injects-real-key")
    req = urllib.request.Request(url, headers={"Authorization": f"Token {key}", "User-Agent": "icyfox-motion-kit"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read()


def search(name, n=5):
    q, (dmin, dmax), _ = TARGETS[name]
    params = {"query": q, "filter": f'license:"{CC0}" duration:[{dmin} TO {dmax}]', "fields": FIELDS,
              "sort": "rating_desc", "page_size": str(n)}
    data = json.loads(call(f"{API}/search/text/?{urllib.parse.urlencode(params)}"))
    return [r for r in data.get("results", []) if r.get("license", "").endswith("/zero/1.0/") or CC0 in r.get("license", "")]


def ff(*args):
    subprocess.run(["ffmpeg", "-v", "error", "-y", *map(str, args)], check=True)


def read_wav(path):
    import wave
    import numpy as np
    with wave.open(str(path), "rb") as w:
        ch, n = w.getnchannels(), w.getnframes()
        x = np.frombuffer(w.readframes(n), "<i2").astype(np.float32) / 32768
    return x.reshape(-1, ch)


def write_wav(path, x, sr=48000):
    import wave
    import numpy as np
    with wave.open(str(path), "wb") as w:
        w.setnchannels(x.shape[1])
        w.setsampwidth(2)
        w.setframerate(sr)
        w.writeframes((np.clip(x, -1, 1) * 32767).astype("<i2").tobytes())


def loop_seamless(x, sr=48000, length=30.0, xf=2.0):
    """Vòng lặp liền: lấy length+xf giây, trộn xf giây cuối (giảm dần) với xf giây đầu (tăng dần) theo công suất bằng nhau."""
    import numpy as np
    L, F = int(length * sr), int(xf * sr)
    if len(x) < L + F:
        raise ValueError(f"bản thu ngắn hơn {length + xf:.0f} giây, không làm vòng lặp được")
    a = x[:L + F].copy()
    t = np.linspace(0, np.pi / 2, F)[:, None]
    head = a[:F] * np.sin(t) + a[L:L + F] * np.cos(t)    # đầu mới = đầu tăng dần + đuôi giảm dần
    return np.concatenate([head, a[F:L]])


def process(src, dst, loop):
    with tempfile.TemporaryDirectory() as td:
        td = Path(td)
        if loop:
            ff("-i", src, "-t", "34", "-ac", "2", "-ar", "48000", td / "a.wav")
            write_wav(td / "l.wav", loop_seamless(read_wav(td / "a.wav")))
            ff("-i", td / "l.wav", "-af", "loudnorm=I=-24:TP=-2", "-ar", "48000", td / "out.wav")
        else:
            ff("-i", src, "-ac", "2", "-ar", "48000", "-af",
               "silenceremove=start_periods=1:start_threshold=-45dB,atrim=0:8,afade=t=out:st=7.2:d=0.8", td / "t.wav")
            x = read_wav(td / "t.wav")
            write_wav(td / "out.wav", x * (0.89 / max(float(abs(x).max()), 1e-6)))   # đỉnh -1 dBFS
        ff("-i", td / "out.wav", "-c:a", "libmp3lame", "-b:a", "192k", dst)


def credit(rows):
    p = HERE / "sfx" / "CREDITS.md"
    s = p.read_text(encoding="utf-8")
    head = "## sfx/real/ (bản thu thật, Freesound, CC0)"
    if head not in s:
        s += f"\n\n{head}\nCC0: dùng thương mại, không bắt buộc ghi công; vẫn ghi lại nguồn để truy vết.\n\n| File | Freesound | Tác giả | Giấy phép | Ngày tải |\n|---|---|---|---|---|\n"
    for r in rows:
        line = f"| {r['file']} | {r['url']} | {r['username']} | CC0 1.0 | {date.today().isoformat()} |"
        if r["url"] not in s:
            s = s.rstrip("\n") + "\n" + line + "\n"
    p.write_text(s, encoding="utf-8")


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("cmd", choices=["search", "fetch"])
    ap.add_argument("--only", default="")
    ap.add_argument("--pick", type=int, default=1, help="lấy ứng viên thứ mấy (1 = điểm cao nhất)")
    ap.add_argument("--replace", action="store_true")
    a = ap.parse_args(argv)
    names = [n for n in TARGETS if not a.only or n in a.only.split(",")]
    REAL.mkdir(parents=True, exist_ok=True)
    rows, fails = [], []
    for name in names:
        try:
            res = search(name)
        except Exception as e:   # lỗi mạng/khóa: báo rõ, không thay bằng thứ khác
            fails.append(f"{name}: {e}")
            continue
        if a.cmd == "search":
            print(f"\n{name}:")
            for i, r in enumerate(res, 1):
                print(f"  {i}. {r['name'][:60]} | {r['duration']:.1f}s | ★{r.get('avg_rating', 0):.1f} | {r['num_downloads']} lượt tải | {r['url']}")
            continue
        dst = REAL / f"{name}.mp3"
        if dst.exists() and not a.replace:
            print(f"  giữ  {dst.name} (đã có)")
            continue
        if len(res) < a.pick:
            fails.append(f"{name}: không có ứng viên CC0 thứ {a.pick}")
            continue
        r = res[a.pick - 1]
        with tempfile.TemporaryDirectory() as td:
            raw = Path(td) / "raw.mp3"
            raw.write_bytes(call(r["previews"]["preview-hq-mp3"]))
            process(raw, dst, TARGETS[name][2])
        rows.append({"file": f"sfx/real/{dst.name}", "url": r["url"], "username": r["username"]})
        print(f"  tải  {dst.name} <- {r['name'][:50]} ({r['username']}, CC0) {r['url']}")
    if rows:
        credit(rows)
    for f in fails:
        print("  LỖI", f)
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
