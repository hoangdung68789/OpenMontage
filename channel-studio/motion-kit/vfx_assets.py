"""Sinh tài nguyên VFX của motion kit: kết cấu hình (PNG) và âm thanh (MP3), tự tạo hoàn toàn bằng toán
(numpy), không lấy file của ai, nên không có ràng buộc giấy phép. Chạy lại cho kết quả y hệt (seed cố định).

  python vfx_assets.py            # sinh vào vfx/tex/ và sfx/synth/ (bỏ qua file đã có)
  python vfx_assets.py --force    # sinh lại tất cả

Kết cấu đều lặp liền mép (tileable) nhờ lọc nhiễu trong miền tần số (FFT là phép tuần hoàn), nên có thể trượt
vô hạn bằng background-position mà không thấy đường nối. Âm thanh nền (mưa, gió, lửa, dưới nước) cũng lặp liền.
"""
import subprocess
import sys
import wave
from pathlib import Path

import numpy as np
from PIL import Image

HERE = Path(__file__).resolve().parent
TEX = HERE / "vfx" / "tex"
SYN = HERE / "sfx" / "synth"
SR = 48000


# ---------------------------------------------------------------- hình
def fnoise(h, w, beta, seed, ax=1.0, ay=1.0, lo=1.0):
    """Nhiễu 1/f^beta tuần hoàn (lặp liền mép). ax, ay kéo giãn theo trục (ax<1 = vệt ngang)."""
    r = np.random.default_rng(seed)
    F = np.fft.fft2(r.standard_normal((h, w)))
    ky = np.fft.fftfreq(h)[:, None] * h / ay
    kx = np.fft.fftfreq(w)[None, :] * w / ax
    k = np.sqrt(kx ** 2 + ky ** 2)
    k[0, 0] = 1
    n = np.real(np.fft.ifft2(F / np.maximum(k, lo) ** beta))
    return (n - n.min()) / (n.max() - n.min())


def smooth(x, a, b):
    t = np.clip((x - a) / (b - a), 0, 1)
    return t * t * (3 - 2 * t)


def rgba(alpha, color):
    a = np.clip(alpha, 0, 1)
    img = np.zeros(a.shape + (4,), np.uint8)
    img[..., :3] = np.array(color, np.uint8)
    img[..., 3] = (a * 255).astype(np.uint8)
    return Image.fromarray(img, "RGBA")


def rgba_rgb(rgb, alpha):
    img = np.dstack([np.clip(rgb, 0, 255), np.clip(alpha, 0, 1) * 255]).astype(np.uint8)
    return Image.fromarray(img, "RGBA")


def splat(h, w, pts, rad, seed_vals=None):
    """Chấm mềm (gauss) đặt có quấn mép."""
    a = np.zeros((h, w))
    for (y, x, r, v) in pts:
        R = int(r * 3) + 1
        ys = (np.arange(-R, R + 1) + int(y)) % h
        xs = (np.arange(-R, R + 1) + int(x)) % w
        yy, xx = np.meshgrid(np.arange(-R, R + 1), np.arange(-R, R + 1), indexing="ij")
        a[np.ix_(ys, xs)] += v * np.exp(-(yy ** 2 + xx ** 2) / (2 * r * r))
    return a


def tex_fog():
    n = fnoise(512, 1024, 1.9, 11)
    return rgba(smooth(n, .35, .9) * .85, (214, 220, 226))


def tex_smoke():
    n = fnoise(1024, 1024, 1.7, 12, ay=.8)
    d = fnoise(1024, 1024, 2.4, 13)
    a = smooth(n * .7 + d * .3, .3, .85)
    return rgba(a * .9, (150, 146, 140))


def tex_rain():
    h, w = 512, 512
    r = np.random.default_rng(14)
    a = np.zeros((h, w))
    for _ in range(260):
        x, y, L = r.integers(0, w), r.integers(0, h), r.integers(24, 90)
        v = r.uniform(.25, .8)
        ys = (np.arange(L) + y) % h
        a[ys, x] += v * np.linspace(.2, 1, L)
        if r.random() < .5:
            a[ys, (x + 1) % w] += v * .4 * np.linspace(.2, 1, L)
    return rgba(np.clip(a, 0, 1), (205, 215, 228))


def tex_snow(seed=15, n=220, rmin=1.2, rmax=3.6):
    r = np.random.default_rng(seed)
    pts = [(r.uniform(0, 512), r.uniform(0, 512), r.uniform(rmin, rmax), r.uniform(.5, 1)) for _ in range(n)]
    return rgba(np.clip(splat(512, 512, pts, None) * 1.4, 0, 1), (246, 248, 252))


def tex_embers():
    r = np.random.default_rng(16)
    pts = [(r.uniform(0, 512), r.uniform(0, 512), r.uniform(.9, 2.4), r.uniform(.6, 1)) for _ in range(70)]
    a = np.clip(splat(512, 512, pts, None) * 1.6, 0, 1)
    halo = np.clip(splat(512, 512, [(y, x, rr * 4, v * .25) for y, x, rr, v in pts], None), 0, 1)
    al = np.clip(a + halo, 0, 1)
    rgb = np.dstack([np.full_like(al, 255), 120 + 120 * a, 40 + 120 * a ** 2])
    return rgba_rgb(rgb, al)


def tex_sand():
    n = fnoise(512, 1024, 1.25, 17, ax=.3)
    g = fnoise(512, 1024, .6, 18, ax=.3)
    a = smooth(n, .3, .85) * .7 + smooth(g, .6, .95) * .3
    return rgba(a * .9, (196, 160, 112))


def tex_caustics():
    n = fnoise(512, 512, 2.0, 19)
    m = fnoise(512, 512, 2.0, 20)
    c = (1 - np.abs(np.sin(n * 18))) ** 6 * .7 + (1 - np.abs(np.sin(m * 14))) ** 8 * .5
    return rgba(np.clip(c, 0, 1) * .85, (190, 240, 255))


def tex_static():
    r = np.random.default_rng(21)
    v = r.random((256, 256))
    v = np.repeat(v, 2, axis=1)   # hạt hơi bè ngang như TV analog
    return Image.fromarray((v * 255).astype(np.uint8), "L").convert("RGBA")


def tex_rays():
    h, w = 1080, 1920
    yy, xx = np.mgrid[0:h, 0:w]
    ox, oy = -200, -300
    ang = np.arctan2(yy - oy, xx - ox)
    dist = np.hypot(yy - oy, xx - ox)
    r = np.random.default_rng(22)
    t = np.linspace(0, np.pi / 2, 900)
    prof = np.zeros_like(t)
    for _ in range(14):
        c, wd = r.uniform(.15, 1.35), r.uniform(.008, .04)
        prof += r.uniform(.4, 1) * np.exp(-((t - c) / wd) ** 2)
    a = np.interp(ang, t, prof) * np.exp(-dist / 1500) * smooth(dist, 0, 300)
    return rgba(np.clip(a, 0, 1) * .75, (255, 236, 200))


def tex_glow():
    yy, xx = np.mgrid[-256:256, -256:256]
    d = np.hypot(yy, xx) / 256
    n = fnoise(512, 512, 1.5, 23)
    d = d * (0.85 + .3 * n)
    a = np.clip(1 - d, 0, 1) ** 1.6
    core = np.clip(1 - d * 2.2, 0, 1)
    rgb = np.dstack([np.full_like(a, 255), 150 + 105 * core, 40 + 200 * core ** 2])
    return rgba_rgb(rgb, a)


def tex_burn():
    yy, xx = np.mgrid[-512:512, -512:512]
    d = np.hypot(yy, xx) / 512
    n = fnoise(1024, 1024, 1.8, 24)
    e = d + (n - .5) * .6
    a = smooth(1 - e, .0, .5)
    hot = smooth(1 - e, .35, .8)
    rgb = np.dstack([np.full_like(a, 255), 110 + 145 * hot, 20 + 220 * hot ** 2])
    return rgba_rgb(rgb, a)


def tex_beam():
    h, w = 500, 1800
    yy, xx = np.mgrid[0:h, 0:w]
    half = 18 + xx * .13
    a = smooth(half - np.abs(yy - h / 2), 0, half * .6) * np.exp(-xx / 1400) * smooth(xx, 0, 60)
    return rgba(np.clip(a, 0, 1) * .8, (240, 244, 255))


def tex_lens():
    """Bụi bẩn trên ống kính: hiện lên khi có ánh sáng mạnh (nổ, chớp)."""
    r = np.random.default_rng(25)
    pts = [(r.uniform(0, 540), r.uniform(0, 960), r.uniform(3, 14), r.uniform(.15, .5)) for _ in range(90)]
    a = np.clip(splat(540, 960, pts, None), 0, 1) * (.5 + .5 * fnoise(540, 960, 1.6, 26))
    return rgba(a, (255, 244, 225))


TEXTURES = {"fog": tex_fog, "smoke": tex_smoke, "rain": tex_rain, "snow": tex_snow, "snow_far": lambda: tex_snow(27, 420, .7, 1.6),
            "embers": tex_embers, "sand": tex_sand, "caustics": tex_caustics, "static": tex_static, "rays": tex_rays,
            "glow": tex_glow, "burn": tex_burn, "beam": tex_beam, "lens": tex_lens}


# ---------------------------------------------------------------- tiếng
def noise(n, seed):
    return np.random.default_rng(seed).standard_normal(n)


def band(x, lo=None, hi=None, order=1.0):
    """Lọc trong miền tần số (tuần hoàn: vòng lặp liền nếu x là cả vòng)."""
    X = np.fft.rfft(x)
    f = np.fft.rfftfreq(len(x), 1 / SR)
    g = np.ones_like(f)
    if hi:
        g /= np.sqrt(1 + (f / hi) ** (2 * order))
    if lo:
        g *= (f / lo) ** order / np.sqrt(1 + (f / lo) ** (2 * order))
    return np.fft.irfft(X * g, len(x))


def pink(n, seed):
    X = np.fft.rfft(noise(n, seed))
    f = np.fft.rfftfreq(n, 1 / SR)
    f[0] = 1
    return np.fft.irfft(X / np.sqrt(f), n)


def lfo(n, cycles, seed, depth=1.0):
    """Đường biến thiên chậm, số chu kỳ nguyên trên cả vòng -> lặp liền."""
    t = np.arange(n) / n
    r = np.random.default_rng(seed)
    v = sum(r.uniform(.3, 1) * np.sin(2 * np.pi * c * t + r.uniform(0, 6.3)) for c in cycles)
    v = (v - v.min()) / (v.max() - v.min())
    return 1 - depth + depth * v


def clicks(n, count, seed, dec_ms=(2, 8), amp=(.2, 1), hp=2000):
    r = np.random.default_rng(seed)
    y = np.zeros(n)
    for _ in range(count):
        p, L = r.integers(0, n), int(SR * r.uniform(*dec_ms) / 1000 * 5)
        env = np.exp(-np.arange(L) / (L / 5)) * r.uniform(*amp)
        idx = (p + np.arange(L)) % n
        y[idx] += env * r.standard_normal(L)
    return band(y, lo=hp)


def norm(x, peak_db=-3.0):
    return x / (np.max(np.abs(x)) + 1e-9) * 10 ** (peak_db / 20)


def fade(x, a=.01, b=.05):
    A, B = int(a * SR), int(b * SR)
    x = x.copy()
    x[:A] *= np.linspace(0, 1, A)
    x[-B:] *= np.linspace(1, 0, B)
    return x


def s_rain(sec=30):
    n = SR * sec
    bed = band(pink(n, 31), lo=500, hi=7000) * lfo(n, [3, 7, 11], 32, .25)
    return norm(bed * .7 + clicks(n, 2600, 33, (1, 4), (.1, .6), 2500) * .9, -9)


def s_wind(sec=30):
    n = SR * sec
    x = noise(n, 41)
    lo, hi = band(x, hi=350, order=2), band(x, lo=300, hi=1500)
    m = lfo(n, [2, 3, 5], 42, .9)
    return norm((lo * (1 - m) * 1.6 + hi * m) * lfo(n, [1, 4, 6], 43, .6), -9)


def s_fire(sec=30):
    n = SR * sec
    roar = band(pink(n, 51), hi=500, order=2) * lfo(n, [5, 9, 13], 52, .4)
    return norm(roar * .5 + clicks(n, 900, 53, (3, 15), (.1, 1), 1200), -8)


def s_underwater(sec=30):
    n = SR * sec
    bed = band(noise(n, 61), hi=220, order=2) * lfo(n, [2, 5], 62, .5)
    r = np.random.default_rng(63)
    t = np.arange(int(SR * .08)) / SR
    for _ in range(40):   # bọt khí: tiếng chirp đi lên
        f0 = r.uniform(400, 900)
        b = np.sin(2 * np.pi * (f0 * t + f0 * 4 * t ** 2)) * np.exp(-t / .02) * r.uniform(.1, .4)
        p = r.integers(0, n)
        bed[(p + np.arange(len(t))) % n] += b
    return norm(bed, -10)


def s_static(sec=3):
    n = SR * sec
    x = band(noise(n, 71), lo=900, hi=4500) * (0.5 + .5 * (np.random.default_rng(72).random(n // 480 + 1).repeat(480)[:n] > .3))
    return norm(fade(x, .02, .3), -8)


def s_thunder(sec=7):
    n = SR * sec
    t = np.arange(n) / SR
    crack = band(noise(n, 81), lo=800) * np.exp(-t / .06)
    rumble = band(noise(n, 82), hi=140, order=2) * np.clip(t / .35, 0, 1) * np.exp(-t / 1.9)
    m = band(noise(n, 83), hi=4, order=2)
    rumble *= 0.55 + .45 * (m - m.min()) / (m.max() - m.min())   # cuộn sấm lên xuống
    return norm(fade(crack * .5 + rumble * 2.5, .001, .8), -2)


def s_boom(sec=4):
    n = SR * sec
    t = np.arange(n) / SR
    f = 30 + 55 * np.exp(-t / .25)
    sub = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / .9)
    body = band(noise(n, 91), hi=400, order=2) * np.exp(-t / .6)
    snap = band(noise(n, 92), lo=1500) * np.exp(-t / .03)
    return norm(fade(sub * 1.2 + body * 1.6 + snap * .4, .001, .5), -1.5)


def s_sparks(sec=2):
    n = SR * sec
    t = np.arange(n) / SR
    return norm(fade(clicks(n, 260, 101, (1, 5), (.2, 1), 3000) * np.exp(-t / .6), .001, .2), -6)


SOUNDS = {"rain-loop": s_rain, "wind-loop": s_wind, "fire-loop": s_fire, "underwater-loop": s_underwater,
          "radio-static": s_static, "thunder": s_thunder, "boom": s_boom, "sparks": s_sparks}


def write_mp3(y, path):
    tmp = path.with_suffix(".wav")
    with wave.open(str(tmp), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes((np.clip(y, -1, 1) * 32767).astype("<i2").tobytes())
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(tmp), "-c:a", "libmp3lame", "-b:a", "160k", str(path)], check=True)
    tmp.unlink()


def main(force=False):
    TEX.mkdir(parents=True, exist_ok=True)
    SYN.mkdir(parents=True, exist_ok=True)
    for name, fn in TEXTURES.items():
        p = TEX / f"{name}.png"
        if force or not p.exists():
            fn().save(p, optimize=True)
            print(f"  hình  {p.name:18} {p.stat().st_size // 1024} KB")
    for name, fn in SOUNDS.items():
        p = SYN / f"{name}.mp3"
        if force or not p.exists():
            write_mp3(fn(), p)
            print(f"  tiếng {p.name:18} {p.stat().st_size // 1024} KB")
    print(f"Xong: {len(TEXTURES)} kết cấu ở {TEX}, {len(SOUNDS)} tiếng ở {SYN}")


if __name__ == "__main__":
    main("--force" in sys.argv)
