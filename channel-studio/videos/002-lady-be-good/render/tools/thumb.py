"""Thumbnail 1280x720 cho 002: ảnh xác máy bay giữa sa mạc (USAF, public domain) + 3 chữ to.
Chạy: PYTHONUTF8=1 python channel-studio/videos/002-lady-be-good/render/tools/thumb.py
"""
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
IMG = ROOT / "projects" / "lady-be-good" / "assets" / "images" / "commons" / "Lady_Be_Good_Wreckage_Discovery.jpg"
FONTS = ROOT.parents[1] / "Fonts" / "capcut"
OUT = HERE.parents[1] / "package"
W, H = 1280, 720

im = Image.open(IMG).convert("L")
k = max(W / im.width, H / im.height) * 1.25
im = im.resize((round(im.width * k), round(im.height * k)), Image.LANCZOS)
x0, y0 = 40, (im.height - H) // 2  # máy bay nằm bên trái, chừa cát trống bên phải cho chữ
im = im.crop((x0, y0, x0 + W, y0 + H))
im = ImageEnhance.Contrast(im).enhance(1.35)
base = Image.merge("RGB", [im.point(lambda v: min(255, v * 1.05)), im, im.point(lambda v: v * 0.86)])  # sepia nhẹ

shade = Image.new("L", (W, H))
d = ImageDraw.Draw(shade)
for x in range(W):  # tối dần sang phải để chữ nổi
    d.line([(x, 0), (x, H)], fill=int(max(0, 215 * (x - W * 0.38) / (W * 0.62))))
base = Image.composite(Image.new("RGB", (W, H), (20, 16, 13)), base, shade)

dr = ImageDraw.Draw(base)
big = ImageFont.truetype(str(FONTS / "Anton-Regular.ttf"), 150)
small = ImageFont.truetype(str(FONTS / "Montserrat-ExtraBold.ttf"), 44)


def text(xy, s, font, fill):
    sh = Image.new("RGBA", (W, H))
    ImageDraw.Draw(sh).text((xy[0] + 4, xy[1] + 6), s, font=font, fill=(0, 0, 0, 200))
    base.paste(sh.filter(ImageFilter.GaussianBlur(6)), (0, 0), sh.filter(ImageFilter.GaussianBlur(6)))
    dr.text(xy, s, font=font, fill=fill)


def right(y, s, font, fill):
    text((W - 60 - dr.textlength(s, font=font), y), s, font, fill)


right(120, "NO ONE", big, (241, 235, 224))
right(290, "ABOARD", big, (232, 137, 58))
dr.rectangle([W - 118, 488, W - 60, 494], fill=(200, 66, 58))
right(515, "LOST 1943 · FOUND 1958", small, (241, 235, 224))
OUT.mkdir(parents=True, exist_ok=True)
base.save(OUT / "thumbnail.jpg", quality=90)
print(OUT / "thumbnail.jpg", (OUT / "thumbnail.jpg").stat().st_size // 1024, "KB")
