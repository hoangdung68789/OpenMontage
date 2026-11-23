"""ICYFOX MOTION KIT v2: dựng dự án HyperFrames từ kế hoạch cảnh (motion_plan.json), theo chuẩn edit
(.claude/skills/hoang-dung-clay-lapis-studio/references/edit-standard.md, edit-library.md, genre-recipes.md).

  python icyfox_motion.py validate <plan.json>               # kiểm kế hoạch (mã thoát 2 nếu hỏng)
  python icyfox_motion.py build <plan.json> <thư_mục_ra>      # sinh index.html + compositions/partN.html (chia khối) + assets + sfx_cues.json
  python icyfox_motion.py finish <vào.mp4> <ra.mp4>           # chuẩn hóa tiếng -14 LUFS, đỉnh -1 dBTP (2 lượt loudnorm), in số đo
  python icyfox_motion.py presets                             # liệt kê preset thể loại, chuyển cảnh, hiệu ứng chữ

v2 so với v1:
- Thể loại (genre): mỗi chủ đề có màu, chữ, nhịp, bộ chuyển cảnh, màu phim, bảng âm thanh riêng (GENRES).
- Chuyển cảnh: cut, dip, dissolve, whip, blurswap, iris, wipe, flash. Tự xoay vòng, không 2 mối nối liền nhau cùng kiểu,
  cắt thẳng tối đa 1/3 (motion.md của hyperframes).
- Chữ: đáp xuống rồi ĐỨNG YÊN (không trôi, không phóng), 4 kiểu hiện chữ (blurword, greyink, letters, typewriter),
  từ bọc *dấu sao* được tô màu nhấn; lower third; khung cinema (letterbox).
- Máy quay: push, pull, pan, tilt, punch-in, rack (kéo nét), lớp chiều sâu (nền mờ trôi ngược = parallax).
- Hiệu ứng hình: màu phim theo thể loại (CSS filter + lớp tông), hạt film, nhấp nháy, rung khung nhẹ, vệt sáng, viền tối.
- Bố cục: title, photo, document, map, stat, quote, split, triptych, timeline.
- Âm thanh: tự đặt hiệu ứng âm thanh có nguyên nhân (chuyển cảnh, số đáp, chữ gõ, cao trào), xoay vòng 2–3 bản,
  đỉnh âm sau hình 1 khung; nhạc nền tự hạ khi có lời (ducking); giọng đọc; rồi `finish` chuẩn hóa -14 LUFS.
VFX chuyên dụng (khóa "vfx", bật khi cần): xem vfx.py.
Render xác định: không Math.random/Date.now, không tải mạng lúc render, GSAP để sẵn trong vendor/.
"""
import html
import json
import random
import re
import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import vfx  # noqa: E402  bộ VFX chuyên dụng (vfx.py)

HERE = Path(__file__).resolve().parent
SFX_DIR = HERE / "sfx"
W, H, FPS = 1920, 1080, 30
MAX_GAP = 8.0
SHOT = 6.5
esc = html.escape
TYPES = {"title", "photo", "document", "map", "stat", "quote", "split", "triptych", "timeline"}
TRANSITIONS = ["cut", "dip", "dissolve", "whip", "blurswap", "iris", "wipe", "flash"]
TEXT_FX = ["blurword", "greyink", "letters", "typewriter"]

# ---- Thể loại: màu, chữ, nhịp, chuyển cảnh, màu phim, âm thanh (chi tiết và lý do: genre-recipes.md) ----
GENRES = {
    "war": dict(name="Chiến tranh (P3)", bg="#14130F", ink="#ECE6DA", accent="#C8423A", accent2="#C9A54C",
                display="Oswald", body="Inter", mono="Space Mono", title_case="upper",
                grade="grayscale(.35) sepia(.22) contrast(1.16) brightness(.94)", tint="rgba(120,96,60,.18)",
                flicker=.05, weave=1.2, shot=5.5, trans=["dip", "whip", "flash", "wipe", "blurswap"],
                sfx=dict(whoosh=["whoosh", "whoosh-short"], impact=["impact-bass-1", "impact-bass-2"], land="impact-bass-2",
                         type="typing", pop="pop"), text_fx="blurword"),
    "mystery": dict(name="Bí ẩn (P1)", bg="#0E1216", ink="#E6EEF2", accent="#5FB3C9", accent2="#C9A54C",
                    display="Playfair Display", body="Inter", mono="IBM Plex Mono", title_case="title",
                    grade="saturate(.62) contrast(1.12) brightness(.86)", tint="rgba(40,90,120,.22)",
                    flicker=.02, weave=.5, shot=7.0, trans=["dissolve", "blurswap", "iris", "dip"],
                    sfx=dict(whoosh=["whoosh-cinematic", "whoosh"], impact=["impact-bass-2"], land="impact-bass-2",
                             type="typing", pop="ping"), text_fx="greyink"),
    "disaster": dict(name="Thảm họa, sự cố kỹ thuật (P4)", bg="#121212", ink="#F2F0EC", accent="#E8893A", accent2="#C8423A",
                     display="Archivo Black", body="Inter", mono="IBM Plex Mono", title_case="upper",
                     grade="contrast(1.2) saturate(.85) brightness(.95)", tint="rgba(140,70,30,.14)",
                     flicker=.02, weave=.6, shot=5.0, trans=["cut", "whip", "wipe", "dip", "blurswap"],
                     sfx=dict(whoosh=["whoosh-short", "whoosh"], impact=["impact-bass-1"], land="impact-bass-1",
                              type="key-press", pop="pop"), text_fx="letters"),
    "ancient": dict(name="Cổ đại, thần thoại (P5)", bg="#1B1714", ink="#F1EBE0", accent="#1F4E8C", accent2="#B5734A",
                    display="EB Garamond", body="Montserrat", mono="IBM Plex Mono", title_case="title",
                    grade="sepia(.42) contrast(1.06) brightness(1.02) saturate(.9)", tint="rgba(181,115,74,.16)",
                    flicker=.015, weave=.4, shot=7.5, trans=["dissolve", "iris", "wipe", "blurswap"],
                    sfx=dict(whoosh=["whoosh-cinematic", "whoosh"], impact=["impact-bass-2"], land="impact-bass-2",
                             type="typing", pop="chime"), text_fx="blurword"),
    "survival": dict(name="Sinh tồn, thám hiểm (P2)", bg="#10161A", ink="#EEF2F4", accent="#9FC9DE", accent2="#E8893A",
                     display="League Gothic", body="Inter", mono="Space Mono", title_case="upper",
                     grade="saturate(.72) contrast(1.1) brightness(.95)", tint="rgba(90,130,160,.18)",
                     flicker=.02, weave=.8, shot=6.0, trans=["dissolve", "whip", "dip", "wipe", "cut"],
                     sfx=dict(whoosh=["whoosh", "whoosh-short"], impact=["impact-bass-1"], land="impact-bass-2",
                              type="typing", pop="pop"), text_fx="letters"),
}
GENRES["default"] = dict(GENRES["ancient"], name="Mặc định")
STYLE_KEYS = {"bg", "ink", "accent", "accent2", "display", "body", "mono", "title_case", "grade", "tint",
              "flicker", "weave", "shot", "trans", "text_fx"}


def genre_of(plan):
    """Preset thể loại + ghi đè theo video (khóa "style" trong kế hoạch, xem genre-recipes.md §3)."""
    g = dict(GENRES.get(plan.get("genre", "default"), GENRES["default"]))
    g.update({k: v for k, v in (plan.get("style") or {}).items() if k in STYLE_KEYS})
    return g


def css(g):
    return vfx.CSS + f"""
#root {{ position:relative; width:{W}px; height:{H}px; overflow:hidden; background:{g['bg']}; color:{g['ink']}; font-family:"{g['body']}",sans-serif; }}
.sc {{ position:absolute; inset:0; overflow:hidden; background:{g['bg']}; }}
.cam, .lay {{ position:absolute; inset:0; transform-origin:50% 50%; }}
.media {{ position:absolute; inset:0; filter:{g['grade']}; }}
.tint {{ position:absolute; inset:0; background:{g['tint']}; mix-blend-mode:soft-light; pointer-events:none; }}
.desk {{ position:absolute; inset:-10%; background:radial-gradient(ellipse at 50% 45%, {g['bg']}00 0%, {g['bg']} 72%), #2c2620; }}
.depth {{ position:absolute; inset:-12%; background-size:cover; background-position:center; filter:blur(22px) brightness(.45) {g['grade']}; }}
.print {{ position:absolute; left:50%; top:50%; transform:translate(-50%,-50%); }}
.print .pw {{ position:relative; display:inline-block; }}
.print img {{ display:block; height:760px; width:auto; max-width:1500px; object-fit:contain; border:14px solid #E8DFCC; background:#E8DFCC; box-shadow:0 30px 90px rgba(0,0,0,.65); }}
.full {{ position:absolute; inset:0; background-size:cover; background-position:center; }}
.vig {{ position:absolute; inset:0; pointer-events:none; background:radial-gradient(ellipse at center, rgba(0,0,0,0) 50%, rgba(0,0,0,.82) 100%); }}
.grain {{ position:absolute; inset:-50%; opacity:.16; pointer-events:none; mix-blend-mode:overlay;
  background-image:url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='240' height='240'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='.9' numOctaves='2' stitchTiles='stitch'/></filter><rect width='100%' height='100%' filter='url(%23n)'/></svg>"); }}
.flick {{ position:absolute; inset:0; background:#000; opacity:0; pointer-events:none; }}
.dust i {{ position:absolute; border-radius:50%; background:rgba(255,248,236,.8); filter:blur(.6px); }}
.leak {{ position:absolute; inset:-20%; pointer-events:none; mix-blend-mode:screen; opacity:0;
  background:radial-gradient(ellipse at 15% 30%, rgba(255,170,90,.55) 0%, rgba(255,120,60,0) 45%); }}
.dipov {{ position:absolute; inset:0; background:#000; opacity:0; pointer-events:none; }}
.flashov {{ position:absolute; inset:0; background:#FFF6E8; opacity:0; pointer-events:none; mix-blend-mode:screen; }}
.lbox {{ position:absolute; left:0; right:0; height:0; background:#000; z-index:9; }}
.safe {{ position:absolute; left:192px; right:192px; top:108px; bottom:108px; }}
.cap {{ position:absolute; left:0; bottom:0; max-width:1280px; font-family:"{g['body']}",sans-serif; font-size:44px; line-height:1.28;
  padding:14px 22px; background:rgba(0,0,0,.55); border-left:5px solid {g['accent2']}; }}
.credit {{ position:absolute; right:0; bottom:-56px; font:20px/1 "{g['body']}",sans-serif; letter-spacing:.06em; color:{g['ink']}; background:rgba(8,8,8,.78); padding:8px 14px; border-radius:4px; }}
.tscrim {{ position:absolute; inset:0; pointer-events:none; background:linear-gradient(180deg, rgba(0,0,0,.25) 0%, rgba(0,0,0,.72) 32%, rgba(0,0,0,.72) 68%, rgba(0,0,0,.25) 100%); }}
.tw {{ position:absolute; inset:0; display:flex; flex-direction:column; align-items:center; justify-content:center; text-align:center; }}
.tmain {{ font-family:"{g['display']}",serif; font-size:{int(H * .095)}px; line-height:1.05; letter-spacing:.02em; max-width:1500px; }}
.trule {{ width:360px; height:4px; background:{g['accent2']}; margin:28px 0 22px; transform-origin:50% 50%; }}
.tsub {{ font:600 30px/1 "{g['body']}",sans-serif; letter-spacing:.32em; color:{g['accent2']}; text-transform:uppercase; }}
.acc {{ color:color-mix(in srgb, {g['accent']} 70%, #ffffff); }}   /* chữ nhấn sáng hơn màu gốc để đạt tương phản 3:1 trên nền tối */
.w, .ch {{ display:inline-block; white-space:pre; }}
.lt {{ position:absolute; left:192px; top:108px; }}   /* thanh tên ở trên-trái: không đè phụ đề dưới-trái */
.lt .bar {{ position:absolute; left:0; top:0; bottom:0; width:100%; background:rgba(0,0,0,.72); transform-origin:0 50%; }}
.lt .l1 {{ position:relative; font-family:"{g['display']}",serif; font-size:52px; padding:14px 26px 4px; }}
.lt .l2 {{ position:relative; font:600 24px/1 "{g['mono']}",monospace; letter-spacing:.14em; color:{g['accent2']}; padding:4px 26px 16px; text-transform:uppercase; }}
.hl {{ position:absolute; background:rgba(232,180,60,.55); border-bottom:3px solid #B07D1E; mix-blend-mode:multiply; transform-origin:0 50%; }}
.mapbg {{ position:absolute; inset:-15%; background:radial-gradient(ellipse at 40% 40%, #2b3a4a 0%, #121a22 72%); }}
.mapgrid {{ position:absolute; inset:-15%; background-image:linear-gradient(rgba(255,255,255,.06) 1px, transparent 1px), linear-gradient(90deg, rgba(255,255,255,.06) 1px, transparent 1px); background-size:120px 120px; }}
.mlab {{ font:600 26px "{g['body']}",sans-serif; fill:{g['ink']}; paint-order:stroke; stroke:#0c1116; stroke-width:6px; letter-spacing:.08em; }}
.num {{ font-family:"{g['display']}",serif; font-size:230px; line-height:1; color:{g['ink']}; font-variant-numeric:tabular-nums; }}
.nlab {{ font:600 34px/1.3 "{g['body']}",sans-serif; letter-spacing:.18em; color:{g['accent2']}; text-transform:uppercase; margin-top:18px; }}
.q {{ max-width:1400px; font-family:"{g['display']}",serif; font-style:italic; font-size:66px; line-height:1.3; }}
.qby {{ font:600 26px "{g['mono']}",monospace; letter-spacing:.2em; color:{g['accent2']}; margin-top:34px; }}
.panel {{ position:absolute; overflow:hidden; box-shadow:0 24px 70px rgba(0,0,0,.6); }}
.panel .full {{ inset:-6%; }}
.plab {{ position:absolute; left:20px; bottom:18px; font:600 24px "{g['mono']}",monospace; letter-spacing:.12em; background:rgba(0,0,0,.7); padding:8px 14px; }}
.divider {{ position:absolute; left:50%; top:120px; bottom:120px; width:4px; margin-left:-2px; background:{g['accent2']}; transform-origin:50% 0; }}
.tl-line {{ position:absolute; left:200px; right:200px; top:560px; height:3px; background:{g['ink']}; opacity:.35; }}
.tl-fill {{ position:absolute; left:200px; top:560px; height:3px; width:1520px; background:{g['accent2']}; transform-origin:0 50%; }}
.tl-item {{ position:absolute; top:450px; width:300px; margin-left:-150px; text-align:center; }}
.tl-item .d {{ font-family:"{g['display']}",serif; font-size:58px; }}
.tl-item .dot {{ width:20px; height:20px; border-radius:50%; background:{g['accent']}; margin:20px auto 18px; }}
.tl-item .t {{ font:500 26px/1.3 "{g['body']}",sans-serif; }}
"""


class Scene:
    def __init__(self, idx, spec, start, g):
        self.i, self.s, self.T, self.g = idx, spec, start, g
        self.D = float(spec["dur"])
        self.id = f"s{idx}"
        self.html, self.js, self.events, self.sfx = [], [], [start], []
        self.amb = []   # âm thanh nền của VFX: (bắt đầu, dài, file, âm lượng)

    def ev(self, t):
        self.events.append(round(t, 3))

    def a(self, line):
        self.js.append(line)

    def cue(self, t, kind, vol=0.42):
        self.sfx.append((round(t, 3), kind, vol))


def words_html(text, cls="w"):
    """Từ bọc *dấu sao* được tô màu nhấn (một từ có nghĩa, edit-standard 2.4)."""
    out = []
    for m in re.finditer(r"\*([^*]+)\*(\S*)|(\S+)", text):
        if m.group(3):
            out.append(f'<span class="{cls}">{esc(m.group(3))}</span>')
        else:   # dấu câu dính sau từ nhấn giữ trong cùng khối, không thành từ riêng
            out.append(f'<span class="{cls}"><span class="acc">{esc(m.group(1))}</span>{esc(m.group(2))}</span>')
    return " ".join(out)


def case(g, t):
    return t.upper() if g["title_case"] == "upper" else t


def text_reveal(sc, sel, at, fx, n_words):
    """Hiện chữ rồi ĐỨNG YÊN. Trả về thời điểm chữ hiện xong."""
    if fx == "blurword":
        sc.a(f'tl.fromTo("{sel} .w",{{opacity:0,filter:"blur(6px)"}},{{opacity:1,filter:"blur(0px)",duration:.13,stagger:.067,ease:"power2.out"}},{at:.3f});')
        end = at + .13 + .067 * n_words
    elif fx == "greyink":
        sc.a(f'tl.fromTo("{sel} .w",{{opacity:.18}},{{opacity:1,duration:.2,stagger:.085,ease:"none"}},{at:.3f});')
        end = at + .2 + .085 * n_words
    elif fx == "letters":
        sc.a(f'tl.fromTo("{sel} .ch",{{opacity:.0,filter:"blur(3px)"}},{{opacity:1,filter:"blur(0px)",duration:.12,stagger:.045,ease:"power2.out"}},{at:.3f});')
        end = at + .12 + .045 * n_words
    else:  # typewriter
        sc.a(f'tl.fromTo("{sel} .ch",{{opacity:0}},{{opacity:1,duration:.01,stagger:.055,ease:"none"}},{at:.3f});')
        end = at + .055 * n_words
        sc.cue(at, "type", .30)
    sc.ev(at)
    return end


def chars_html(text):
    out = []
    ch = lambda t: "".join(f'<span class="ch">{esc(c)}</span>' for c in t)
    for m in re.finditer(r"\*([^*]+)\*(\S*)|(\S+)", text):
        if m.group(3):
            out.append(f'<span class="w">{ch(m.group(3))}</span>')
        else:
            out.append(f'<span class="w"><span class="acc">{ch(m.group(1))}</span>{ch(m.group(2))}</span>')
    return " ".join(out)


def text_block(sc, sel_id, text, fx, cls):
    n = len(text.replace("*", "")) if fx in ("letters", "typewriter") else len(text.split())
    inner = chars_html(text) if fx in ("letters", "typewriter") else words_html(text)
    return f'<div class="{cls}" id="{sel_id}">{inner}</div>', n


def ambient(sc, rnd, n_dust=22):
    """Không khí: bụi trôi, hạt film, nhấp nháy, vệt sáng lọt. Phủ cả thời lượng cảnh."""
    T, D, sid, g = sc.T, sc.D, sc.id, sc.g
    dots = []
    for k in range(n_dust):
        x, y, r = rnd.uniform(0, W), rnd.uniform(0, H), rnd.uniform(1.2, 3.4)
        dots.append(f'<i id="{sid}d{k}" style="left:{x:.0f}px;top:{y:.0f}px;width:{r:.1f}px;height:{r:.1f}px;opacity:{rnd.uniform(.12, .5):.2f}"></i>')
        sc.a(f'tl.fromTo("#{sid}d{k}",{{x:0,y:0}},{{x:{rnd.uniform(-60, 60):.0f},y:{rnd.uniform(-140, -40):.0f},duration:{D:.3f},ease:"none"}},{T:.3f});')
    sc.html.append(f'<div class="dust">{"".join(dots)}</div><div class="grain" id="{sid}g"></div>'
                   f'<div class="flick" id="{sid}f"></div><div class="leak" id="{sid}k_leak"></div>')
    sc.a(f'tl.fromTo("#{sid}g",{{x:0,y:0}},{{x:{rnd.randint(80, 160)},y:{rnd.randint(60, 140)},duration:{D:.3f},ease:"steps({max(int(D * 12), 1)})"}},{T:.3f});')
    if g["flicker"] > 0:
        n = max(int(D * 3), 2)
        kf = ",".join(f'{{opacity:{rnd.uniform(0, g["flicker"]):.3f},duration:{D / n:.3f},ease:"none"}}' for _ in range(n))
        sc.a(f'tl.to("#{sid}f",{{keyframes:[{kf}]}},{T:.3f});')
    sc.a(f'tl.fromTo("#{sid}k_leak",{{opacity:0,x:-80}},{{opacity:.55,x:120,duration:{min(D, 6) / 2:.3f},ease:"sine.inOut",yoyo:true,repeat:1}},{T + rnd.uniform(0, max(D - 6, 0)):.3f});')


def weave(sc, sel, rnd):
    """Rung khung nhẹ kiểu phim nhựa (biên độ theo thể loại), trên lớp riêng để không đụng tween máy quay."""
    amp = sc.g["weave"]
    if amp <= 0:
        return
    n = max(int(sc.D * 4), 2)
    kf = ",".join(f'{{x:{rnd.uniform(-amp, amp):.2f},y:{rnd.uniform(-amp, amp):.2f},duration:{sc.D / n:.3f},ease:"none"}}' for _ in range(n))
    sc.a(f'tl.to("{sel}",{{keyframes:[{kf}]}},{sc.T:.3f});')


def camera(sc, sel, rnd, kind, t0=None, d=None, s0=1.0, s1=None):
    t0 = sc.T if t0 is None else t0
    d = sc.D if d is None else d
    if kind == "punch":   # phóng gấp đầu khung (cắt bên trong cảnh), rồi trôi chậm
        sc.a(f'tl.set("{sel}",{{scale:{s0 * 1.22:.3f}}},{t0:.3f});')
        sc.a(f'tl.fromTo("{sel}",{{x:0,y:0}},{{x:{rnd.uniform(-30, 30):.0f},y:{rnd.uniform(-20, 20):.0f},duration:{d:.3f},ease:"none"}},{t0:.3f});')
        return
    if kind == "rack":    # kéo nét: nhòe -> nét trong 1 giây, rồi đẩy chậm
        sc.a(f'tl.fromTo("{sel}",{{filter:"blur(8px)"}},{{filter:"blur(0px)",duration:1.0,ease:"power2.out"}},{t0:.3f});')
        kind = "push"
    s_from = {"pull": s0 * 1.14}.get(kind, s0)
    s_to = s1 or {"push": s0 * 1.1, "pull": s0, "panl": s0 * 1.08, "panr": s0 * 1.08, "tilt": s0 * 1.08}[kind]
    x0, x1 = {"panl": (45, -45), "panr": (-45, 45)}.get(kind, (0, 0))
    y0, y1 = {"tilt": (40, -40)}.get(kind, (rnd.uniform(-10, 10), rnd.uniform(-10, 10)))
    sc.a(f'tl.fromTo("{sel}",{{scale:{s_from:.3f},x:{x0},y:{y0:.0f}}},{{scale:{s_to:.3f},x:{x1},y:{y1:.0f},duration:{d:.3f},ease:"sine.inOut"}},{t0:.3f});')


def overlay_extras(sc, rnd):
    """Lower third, khung cinema: gắn được vào mọi cảnh."""
    s, sid, T, g = sc.s, sc.id, sc.T, sc.g
    if s.get("letterbox"):
        sc.html.append(f'<div class="lbox" id="{sid}lb1" style="top:0"></div><div class="lbox" id="{sid}lb2" style="bottom:0"></div>')
        sc.a(f'tl.fromTo(["#{sid}lb1","#{sid}lb2"],{{height:0}},{{height:118,duration:.6,ease:"power2.inOut"}},{T + .1:.3f});')
    lt = s.get("lower")
    if lt:
        at = T + float(lt.get("at", 1.2))
        hold = .5 + .3 * len((lt["title"] + " " + lt.get("sub", "")).split())
        sc.html.append(f'<div class="lt" id="{sid}lt"><div class="bar" id="{sid}ltb"></div><div class="l1">{words_html(lt["title"])}</div>'
                       f'<div class="l2" id="{sid}lt2">{esc(lt.get("sub", ""))}</div></div>')
        sc.a(f'tl.fromTo("#{sid}ltb",{{scaleX:0}},{{scaleX:1,duration:.45,ease:"expo.out"}},{at:.3f});')
        sc.a(f'tl.fromTo("#{sid}lt .l1 .w",{{opacity:0,filter:"blur(6px)"}},{{opacity:1,filter:"blur(0px)",duration:.13,stagger:.067}},{at + .2:.3f});')
        sc.a(f'tl.fromTo("#{sid}lt2",{{opacity:0}},{{opacity:1,duration:.25}},{at + .45:.3f});')
        out = min(at + .6 + max(hold, 3.0), T + sc.D - .6)
        sc.a(f'tl.to("#{sid}lt",{{opacity:0,filter:"blur(6px)",duration:.22,ease:"power3.in"}},{out:.3f});')
        sc.ev(at)
        sc.ev(out)


def caption(sc, at):
    s = sc.s
    parts = []
    if s.get("caption"):
        parts.append(f'<div class="cap" id="{sc.id}c">{words_html(s["caption"])}</div>')
    if s.get("credit"):
        parts.append(f'<div class="credit">{esc(s["credit"])}</div>')
    if parts:
        sc.html.append(f'<div class="safe">{"".join(parts)}</div>')
    if s.get("caption"):
        sc.a(f'tl.fromTo("#{sc.id}c",{{opacity:0,filter:"blur(8px)"}},{{opacity:1,filter:"blur(0px)",duration:.2,ease:"power2.out"}},{at:.3f});')
        sc.ev(at)


# ---------------------------- Loại cảnh ----------------------------
def r_title(sc, rnd):
    s, sid, T, g = sc.s, sc.id, sc.T, sc.g
    fx = s.get("text_fx", "blurword")
    block, n = text_block(sc, f"{sid}t", case(g, s["text"]), fx, "tmain")
    bg = f'<div class="full media" style="background-image:url({esc(s["src"])})"></div><div class="tint"></div><div class="vig"></div><div class="tscrim"></div>' if s.get("src") else '<div class="desk"></div>'
    sc.html.append(f'<div class="cam" id="{sid}k">{bg}</div><div class="tw">{block}<div class="trule" id="{sid}r"></div>'
                   f'<div class="tsub" id="{sid}u">{esc(s.get("sub", ""))}</div></div>')
    camera(sc, f"#{sid}k", rnd, "push")                      # chuyển động nằm ở nền; chữ đáp rồi đứng yên
    end = text_reveal(sc, f"#{sid}t", T + .5, fx, n)
    sc.a(f'tl.fromTo("#{sid}r",{{scaleX:0}},{{scaleX:1,duration:.7,ease:"expo.out"}},{end:.3f});')
    sc.a(f'tl.fromTo("#{sid}u",{{opacity:0,filter:"blur(6px)"}},{{opacity:1,filter:"blur(0px)",duration:.2}},{end + .25:.3f});')
    sc.ev(end + .25)
    sc.cue(T + .5, "land", .5)


def shots_for(sc, shot=SHOT):
    n = max(1, round(sc.D / shot))
    return [(sc.T + k * sc.D / n, sc.D / n) for k in range(n)]


def r_photo(sc, rnd, framed=True):
    s, sid, g = sc.s, sc.id, sc.g
    src = esc(s["src"])
    shots = shots_for(sc, g["shot"])
    focus = s.get("details") or []
    moves = s.get("moves") or ["push", "panl", "punch", "rack", "panr", "tilt"]
    for k, (t, d) in enumerate(shots):
        if k == 0:
            marks = "".join(f'<div class="hl" id="{sid}h{j}" style="left:{x}%;top:{y}%;width:{w}%;height:{h}%"></div>'
                            for j, (x, y, w, h, _a) in enumerate(s.get("highlights", [])))
            front = (f'<div class="print"><div class="pw"><img src="{src}" alt="">{marks}</div></div>' if framed
                     else f'<div class="full media" style="background-image:url({src})"></div>')
            depth = f'<div class="lay" id="{sid}dp"><div class="depth" style="background-image:url({src})"></div></div>' if framed else ""
            sc.html.append(f'<div class="cam" id="{sid}k0">{depth}<div class="lay" id="{sid}wv0"><div class="lay" id="{sid}fr0">{front}</div></div><div class="tint"></div></div>')
            camera(sc, f"#{sid}fr0", rnd, "push", t, d + .7)
            if framed:   # lớp chiều sâu: nền mờ trôi ngược chiều -> cảm giác parallax
                sc.a(f'tl.fromTo("#{sid}dp",{{x:60,scale:1.05}},{{x:-60,scale:1.12,duration:{d + .7:.3f},ease:"sine.inOut"}},{t:.3f});')
            weave(sc, f"#{sid}wv0", rnd)
        else:
            fx_, fy, z = focus[k - 1] if k - 1 < len(focus) else (rnd.uniform(30, 70), rnd.uniform(30, 70), rnd.uniform(1.9, 2.6))
            mv = moves[k % len(moves)]
            sc.html.append(f'<div class="cam" id="{sid}k{k}" style="opacity:0"><div class="lay" id="{sid}m{k}" style="transform-origin:{fx_:.0f}% {fy:.0f}%">'
                           f'<div class="full media" style="background-image:url({src});background-size:contain;background-repeat:no-repeat;background-color:{g["bg"]}"></div></div><div class="tint"></div></div>')
            sc.a(f'tl.set("#{sid}k{k}",{{opacity:1}},{t:.3f});' if mv == "punch" else
                 f'tl.fromTo("#{sid}k{k}",{{opacity:0}},{{opacity:1,duration:.5,ease:"sine.inOut"}},{t:.3f});')
            camera(sc, f"#{sid}m{k}", rnd, mv, t, d + .5, s0=z)
            sc.ev(t)
    sc.html.append('<div class="vig"></div>')
    caption(sc, sc.T + .8)


def r_document(sc, rnd):
    r_photo(sc, rnd, framed=True)
    first = shots_for(sc, sc.g["shot"])[0][1]
    for j, (x, y, w, h, at) in enumerate(sc.s.get("highlights", [])):
        if at > first - 1:
            raise SystemExit(f"{sc.id}: vệt tô {j} ở giây {at} rơi vào khung cận chi tiết (khung toàn trang dài {first:.1f} s)")
        sc.a(f'tl.fromTo("#{sc.id}h{j}",{{scaleX:0,opacity:1}},{{scaleX:1,duration:.9,ease:"power2.inOut"}},{sc.T + at:.3f});')
        sc.ev(sc.T + at)


def r_map(sc, rnd):
    s, sid, T, D, g = sc.s, sc.id, sc.T, sc.D, sc.g
    pts = s["route"]
    path = "M" + " L".join(f"{x},{y}" for x, y in pts)
    L = sum(((pts[i + 1][0] - pts[i][0]) ** 2 + (pts[i + 1][1] - pts[i][1]) ** 2) ** .5 for i in range(len(pts) - 1))
    labels = "".join(f'<g id="{sid}p{j}" opacity="0"><circle cx="{x}" cy="{y}" r="9" fill="{g["accent"]}"/>'
                     f'<text class="mlab" x="{x + 16}" y="{y - 14}">{esc(n)}</text></g>' for j, (x, y, n) in enumerate(s.get("places", [])))
    bg = (f'<div class="full media" style="background-image:url({esc(s["src"])})"></div>' if s.get("src")
          else '<div class="mapbg"></div><div class="mapgrid"></div>')
    sc.html.append(f'<div class="cam" id="{sid}k">{bg}<div class="vig"></div><svg viewBox="0 0 {W} {H}" width="{W}" height="{H}" style="position:absolute;inset:0">'
                   f'<path id="{sid}r" d="{path}" fill="none" stroke="{g["accent2"]}" stroke-width="5" stroke-dasharray="{L:.0f}" stroke-dashoffset="{L:.0f}" stroke-linecap="round"/>'
                   f'{labels}<circle id="{sid}m" r="12" fill="{g["ink"]}" cx="{pts[0][0]}" cy="{pts[0][1]}"/></svg></div>')
    camera(sc, f"#{sid}k", rnd, "push", s1=1.18)
    draw_t, draw_d = T + .8, max(D - 2.0, 2.0)
    sc.a(f'tl.to("#{sid}r",{{attr:{{"stroke-dashoffset":0}},duration:{draw_d:.3f},ease:"none"}},{draw_t:.3f});')
    seg = draw_d / max(len(pts) - 1, 1)
    kf = ",".join(f'{{attr:{{cx:{x},cy:{y}}},duration:{seg:.3f},ease:"none"}}' for x, y in pts[1:])
    sc.a(f'tl.to("#{sid}m",{{keyframes:[{kf}]}},{draw_t:.3f});')
    for j in range(len(s.get("places", []))):
        at = draw_t + j * draw_d / max(len(s["places"]), 1)
        sc.a(f'tl.fromTo("#{sid}p{j}",{{opacity:0,scale:.6,transformOrigin:"50% 50%"}},{{opacity:1,scale:1,duration:.45,ease:"back.out(1.6)"}},{at:.3f});')
        sc.ev(at)
        sc.cue(at, "pop", .28)
    k = 0.0
    while k < D:
        sc.ev(T + k)
        k += 4.0
    caption(sc, T + .8)


def r_stat(sc, rnd):
    s, sid, T, g = sc.s, sc.id, sc.T, sc.g
    bg = f'<div class="full media" style="background-image:url({esc(s["src"])})"></div><div class="tint"></div><div class="vig"></div>' if s.get("src") else '<div class="desk"></div>'
    sc.html.append(f'<div class="cam" id="{sid}k">{bg}</div><div class="tw"><div class="num" id="{sid}n">0</div>'
                   f'<div class="nlab" id="{sid}l">{esc(s["label"])}</div></div>')
    camera(sc, f"#{sid}k", rnd, "pull")
    val, dec, dur = float(s["value"]), int(s.get("decimals", 0)), 1.4
    sc.a(f'(function(){{var o={{v:0}};tl.to(o,{{v:{val},duration:{dur},ease:"power2.out",onUpdate:function(){{'
         f'document.querySelector("#{sid}n").textContent=o.v.toLocaleString("en-US",{{maximumFractionDigits:{dec},minimumFractionDigits:{dec}}})}}}},{T + .4:.3f});}})();')
    sc.ev(T + .4)
    sc.cue(T + .4 + dur, "impact" if s.get("big") else "pop", .45)
    sc.a(f'tl.fromTo("#{sid}l",{{opacity:0,filter:"blur(6px)"}},{{opacity:1,filter:"blur(0px)",duration:.2}},{T + .4 + dur + .1:.3f});')
    sc.ev(T + .4 + dur)


def r_quote(sc, rnd):
    s, sid, T, D, g = sc.s, sc.id, sc.T, sc.D, sc.g
    fx = s.get("text_fx", g["text_fx"])
    block, n = text_block(sc, f"{sid}q", s["text"], fx, "q")
    sc.html.append(f'<div class="cam" id="{sid}k"><div class="desk"></div></div><div class="tw">{block}'
                   f'<div class="qby" id="{sid}b">{esc(s.get("by", ""))}</div></div>')
    camera(sc, f"#{sid}k", rnd, "panr")
    end = text_reveal(sc, f"#{sid}q", T + .5, fx, n)
    k = .5
    while T + k < end:
        sc.ev(T + k)
        k += 2.0
    sc.a(f'tl.fromTo("#{sid}b",{{opacity:0}},{{opacity:1,duration:.25}},{end + .3:.3f});')
    sc.ev(end + .3)


def r_split(sc, rnd):
    """So sánh 2 ảnh: vạch chia tự vẽ, 2 khung lia ngược chiều, nhãn hiện lần lượt."""
    s, sid, T, D = sc.s, sc.id, sc.T, sc.D
    a, b = s["srcs"][:2]
    la, lb = (s.get("labels") or ["", ""])[:2]
    sc.html.append(f'<div class="cam" id="{sid}k"><div class="desk"></div>'
                   f'<div class="panel" id="{sid}pa" style="left:150px;top:140px;width:780px;height:800px"><div class="full media" id="{sid}ia" style="background-image:url({esc(a)})"></div><div class="tint"></div><div class="plab">{esc(la)}</div></div>'
                   f'<div class="panel" id="{sid}pb" style="left:990px;top:140px;width:780px;height:800px"><div class="full media" id="{sid}ib" style="background-image:url({esc(b)})"></div><div class="tint"></div><div class="plab">{esc(lb)}</div></div>'
                   f'<div class="divider" id="{sid}dv"></div></div>')
    sc.a(f'tl.fromTo("#{sid}pa",{{opacity:0,x:-60}},{{opacity:1,x:0,duration:.7,ease:"expo.out"}},{T + .3:.3f});')
    sc.a(f'tl.fromTo("#{sid}pb",{{opacity:0,x:60}},{{opacity:1,x:0,duration:.7,ease:"expo.out"}},{T + 1.6:.3f});')
    sc.a(f'tl.fromTo("#{sid}dv",{{scaleY:0}},{{scaleY:1,duration:.8,ease:"power2.inOut"}},{T + 1.0:.3f});')
    sc.a(f'tl.fromTo("#{sid}ia",{{x:-30,scale:1.05}},{{x:30,scale:1.12,duration:{D:.3f},ease:"sine.inOut"}},{T:.3f});')
    sc.a(f'tl.fromTo("#{sid}ib",{{x:30,scale:1.12}},{{x:-30,scale:1.05,duration:{D:.3f},ease:"sine.inOut"}},{T:.3f});')
    camera(sc, f"#{sid}k", rnd, "push", s1=1.04)
    for t in (T + .3, T + 1.0, T + 1.6):
        sc.ev(t)
    caption(sc, T + 2.2)


def r_triptych(sc, rnd):
    s, sid, T, D = sc.s, sc.id, sc.T, sc.D
    srcs = s["srcs"][:3]
    gap = D / (len(srcs) + 1)
    panels = "".join(f'<div class="panel" id="{sid}p{j}" style="left:{140 + j * 560}px;top:200px;width:520px;height:680px;opacity:0">'
                     f'<div class="full media" id="{sid}i{j}" style="background-image:url({esc(src)})"></div><div class="tint"></div></div>' for j, src in enumerate(srcs))
    sc.html.append(f'<div class="cam" id="{sid}k"><div class="desk"></div>{panels}</div>')
    for j in range(len(srcs)):
        at = T + .3 + j * min(gap, 1.6)
        sc.a(f'tl.fromTo("#{sid}p{j}",{{opacity:0,y:50}},{{opacity:1,y:0,duration:.7,ease:"expo.out"}},{at:.3f});')
        sc.a(f'tl.fromTo("#{sid}i{j}",{{scale:1.04}},{{scale:1.14,duration:{D:.3f},ease:"none"}},{T:.3f});')
        sc.ev(at)
        if j == 0:
            sc.cue(at, "whoosh", .22)   # một tiếng cho cả cụm, không mỗi khung một tiếng
    camera(sc, f"#{sid}k", rnd, "panl", s1=1.05)
    caption(sc, T + .3 + len(srcs) * 1.6)


def r_timeline(sc, rnd):
    s, sid, T, D = sc.s, sc.id, sc.T, sc.D
    items = s["items"]
    n = len(items)
    xs = [200 + (1520 * (j + .5) / n) for j in range(n)]
    cells = "".join(f'<div class="tl-item" id="{sid}e{j}" style="left:{x:.0f}px;opacity:0"><div class="d">{esc(it["date"])}</div><div class="dot"></div>'
                    f'<div class="t">{words_html(it["label"])}</div></div>' for j, (x, it) in enumerate(zip(xs, items)))
    sc.html.append(f'<div class="cam" id="{sid}k"><div class="desk"></div><div class="tl-line"></div><div class="tl-fill" id="{sid}fl"></div>{cells}</div>')
    camera(sc, f"#{sid}k", rnd, "panl", s1=1.06)
    step = (D - 1.5) / n
    sc.a(f'tl.fromTo("#{sid}fl",{{scaleX:0}},{{scaleX:1,duration:{D - 1.0:.3f},ease:"none"}},{T + .5:.3f});')
    for j in range(n):
        at = T + .5 + j * step
        sc.a(f'tl.fromTo("#{sid}e{j}",{{opacity:0,y:30}},{{opacity:1,y:0,duration:.6,ease:"expo.out"}},{at:.3f});')
        sc.ev(at)
        sc.cue(at, "pop", .25)


RENDER = {"title": r_title, "photo": r_photo, "document": r_document, "map": r_map, "stat": r_stat, "quote": r_quote,
          "split": r_split, "triptych": r_triptych, "timeline": r_timeline}


def pick_transitions(plan, g):
    """Chuyển cảnh: theo kế hoạch nếu có, nếu không xoay vòng bộ của thể loại, không lặp liền nhau."""
    out, prev, pool, k = [], None, g["trans"], 0
    for i, s in enumerate(plan["scenes"]):
        if i == 0:
            out.append("none")
            continue
        t = s.get("transition")
        if not t:
            t = pool[k % len(pool)]
            if t == prev:
                k += 1
                t = pool[k % len(pool)]
            k += 1
        out.append(t)
        prev = t
    return out


OVERLAP = {"cut": 0.0, "flash": 0.0, "dip": 0.12, "dissolve": 0.7, "whip": 0.3, "blurswap": 0.2, "iris": 0.5, "wipe": 0.6, "none": 0.0}


def apply_transition(sc, prev, kind, rnd):
    sid, T = sc.id, sc.T
    if kind == "none":
        return
    if kind == "cut":
        sc.a(f'tl.set("#{sid}",{{opacity:1}},{T:.3f});')
    elif kind == "dissolve":
        sc.a(f'tl.fromTo("#{sid}",{{opacity:0}},{{opacity:1,duration:.7,ease:"sine.inOut"}},{T:.3f});')
    elif kind == "dip":            # hình cũ tối ~40% trong 3 khung rồi cắt
        sc.html.append(f'<div class="dipov" id="{sid}dip"></div>')
        prev.html.append(f'<div class="dipov" id="{prev.id}dipout"></div>')
        prev.a(f'tl.fromTo("#{prev.id}dipout",{{opacity:0}},{{opacity:.45,duration:{3 / FPS:.3f},ease:"none"}},{T - 3 / FPS:.3f});')
        sc.a(f'tl.set("#{sid}",{{opacity:1}},{T:.3f});')
        sc.a(f'tl.fromTo("#{sid}dip",{{opacity:.35}},{{opacity:0,duration:.25,ease:"power2.out"}},{T:.3f});')
    elif kind == "whip":
        d = rnd.choice([-1, 1])
        prev.a(f'tl.to("#{prev.id}",{{x:{-d * 420},filter:"blur(18px)",duration:.28,ease:"power3.in"}},{T:.3f});')
        sc.a(f'tl.fromTo("#{sid}",{{opacity:1,x:{d * 520},filter:"blur(18px)"}},{{opacity:1,x:0,filter:"blur(0px)",duration:.3,ease:"power3.out"}},{T + .02:.3f});')
    elif kind == "blurswap":
        prev.a(f'tl.to("#{prev.id}",{{opacity:0,filter:"blur(8px)",duration:.18,ease:"power2.in"}},{T:.3f});')
        sc.a(f'tl.fromTo("#{sid}",{{opacity:0,filter:"blur(8px)"}},{{opacity:1,filter:"blur(0px)",duration:.15,ease:"power2.out"}},{T + .05:.3f});')
    elif kind == "iris":
        sc.a(f'tl.fromTo("#{sid}",{{opacity:1,clipPath:"circle(0% at 50% 50%)"}},{{opacity:1,clipPath:"circle(75% at 50% 50%)",duration:.5,ease:"power2.inOut"}},{T:.3f});')
    elif kind == "wipe":
        sc.a(f'tl.fromTo("#{sid}",{{opacity:1,clipPath:"inset(0% 100% 0% 0%)"}},{{opacity:1,clipPath:"inset(0% 0% 0% 0%)",duration:.6,ease:"power2.inOut"}},{T:.3f});')
    elif kind == "flash":          # lóe sáng rồi cắt (tiếng nổ, ánh chớp)
        sc.html.append(f'<div class="flashov" id="{sid}fl_ov"></div>')
        sc.a(f'tl.set("#{sid}",{{opacity:1}},{T:.3f});')
        sc.a(f'tl.fromTo("#{sid}fl_ov",{{opacity:.95}},{{opacity:0,duration:.35,ease:"power2.out"}},{T:.3f});')
    sc.ev(T)
    sound = {"whip": ("whoosh", .45), "wipe": ("whoosh", .32), "iris": ("whoosh", .28), "flash": ("impact", .5)}.get(kind)
    if sound:
        sc.cue(T, *sound)


def plan_scenes(plan):
    g = genre_of(plan)
    rnd = random.Random(plan.get("seed", 7))
    trans = pick_transitions(plan, g)
    out, t = [], 0.0
    for i, s in enumerate(plan["scenes"]):
        if i > 0:
            t -= OVERLAP[trans[i]]
        sc = Scene(i, s, t, g)
        sc.trans = trans[i]
        RENDER[s["type"]](sc, rnd)
        overlay_extras(sc, rnd)
        ambient(sc, rnd)
        vfx.apply(sc, random.Random(plan.get("seed", 7) * 1000 + i))
        if i > 0:
            apply_transition(sc, out[-1], trans[i], rnd)
        if s.get("payoff"):           # cao trào: riser dồn vào impact, một lần
            sc.cue(max(sc.T - 2.4, 0), "riser", .35)
            sc.cue(sc.T, "impact", .55)
        out.append(sc)
        t += sc.D
    return out, t, g, trans


def validate(plan):
    errs = []
    if plan.get("genre", "default") not in GENRES:
        errs.append(f"thể loại '{plan.get('genre')}' không có (có: {', '.join(GENRES)})")
    style = plan.get("style") or {}
    bad = sorted(set(style) - STYLE_KEYS)
    if bad:
        errs.append(f"style: khóa không dùng được {bad} (dùng được: {', '.join(sorted(STYLE_KEYS))})")
    if any(t not in TRANSITIONS for t in style.get("trans", [])):
        errs.append(f"style.trans: có chuyển cảnh lạ (có: {', '.join(TRANSITIONS)})")
    if style.get("text_fx") and style["text_fx"] not in TEXT_FX:
        errs.append(f"style.text_fx: '{style['text_fx']}' không có (có: {', '.join(TEXT_FX)})")
    for i, s in enumerate(plan.get("scenes", [])):
        if s.get("type") not in TYPES:
            errs.append(f"cảnh {i}: loại '{s.get('type')}' không có (có: {', '.join(sorted(TYPES))})")
        if float(s.get("dur", 0)) < 3:
            errs.append(f"cảnh {i}: dài < 3 giây")
        if s.get("type") in ("photo", "document", "split", "triptych") and not s.get("credit"):
            errs.append(f"cảnh {i}: ảnh thiếu ghi công (credit)")
        if s.get("transition") and s["transition"] not in TRANSITIONS:
            errs.append(f"cảnh {i}: chuyển cảnh '{s['transition']}' không có (có: {', '.join(TRANSITIONS)})")
        txt = s.get("text") or ""
        if s.get("type") in ("title", "quote") and float(s.get("dur", 0)) < .5 + .3 * len(txt.split()) + 1.0:
            errs.append(f"cảnh {i}: chữ {len(txt.split())} từ cần >= {.5 + .3 * len(txt.split()) + 1.0:.1f} giây để đọc kịp")
    verr, vwarn = vfx.check(plan, plan.get("genre", "default"))
    errs += verr
    if errs:
        return errs, None
    scenes, total, g, trans = plan_scenes(plan)
    seams = trans[1:]
    for a, b in zip(seams, seams[1:]):
        if a == b:
            errs.append(f"2 mối nối liền nhau cùng kiểu '{a}' (edit-standard 2.3)")
            break
    if seams and sum(x in ("cut", "flash") for x in seams) > max(1, len(seams) / 3):
        errs.append(f"cắt thẳng/lóe sáng {sum(x in ('cut', 'flash') for x in seams)}/{len(seams)} mối nối > 1/3")
    evs = sorted(e for sc in scenes for e in sc.events) + [total]
    worst = max((b - a, a) for a, b in zip(evs, evs[1:]))
    if worst[0] > MAX_GAP + 1e-6:
        errs.append(f"có đoạn {worst[0]:.1f} giây không có thay đổi đọc được (bắt đầu {worst[1]:.1f} s), tối đa {MAX_GAP} s")
    cues = [c for sc in scenes for c in sc.sfx]
    per_min = len(cues) / max(total / 60, 1e-6)
    if per_min > 15:
        errs.append(f"hiệu ứng âm thanh {per_min:.0f}/phút > 15 (ít và chính xác, edit-standard 2.7)")
    if sum(1 for c in cues if c[1] == "riser") > 1:
        errs.append("riser dùng quá 1 lần")
    used = sorted(set(seams))
    return errs, {"genre": g["name"], "total": round(total, 2), "scenes": len(scenes), "changes": len(evs) - 1,
                  "sec_per_change": round(total / max(len(evs) - 1, 1), 1), "max_gap": round(worst[0], 1),
                  "transitions": used, "sfx": len(cues), "sfx_per_min": round(per_min, 1), "warnings": vwarn,
                  "vfx": sorted({vfx.norm(x)["fx"] for sc in scenes for x in (sc.s.get("vfx") or [])})}


def file_len(f):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(f)], capture_output=True, text=True)
    try:
        return float(r.stdout.strip())
    except ValueError:
        return 2.0


def peak_offset(f):
    """Giây tính từ đầu file tới đỉnh âm (để đỉnh rơi sau hình 1 khung)."""
    try:
        raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(f), "-ac", "1", "-ar", "8000", "-f", "s16le", "-"], capture_output=True).stdout
        import numpy as np
        a = np.abs(np.frombuffer(raw, np.int16))
        return float(a.argmax()) / 8000 if len(a) else 0.0
    except Exception:
        return 0.0


def resolve_cues(scenes, g, out):
    """Biến cue trừu tượng (whoosh, impact, pop, land, type, riser) thành file thật, xoay vòng bản thu, canh đỉnh."""
    rot = {}
    files = []
    for sc in scenes:
        for t, kind, vol in sc.sfx:
            names = {"whoosh": g["sfx"]["whoosh"], "impact": g["sfx"]["impact"], "land": [g["sfx"]["land"]],
                     "type": [g["sfx"]["type"]], "pop": [g["sfx"]["pop"]], "riser": ["riser"], **vfx.SOUND}[kind]
            name = names[rot.get(kind, 0) % len(names)]
            rot[kind] = rot.get(kind, 0) + 1
            src = SFX_DIR / f"{name}.mp3"
            if not src.exists():
                continue
            dst = out / "assets" / "sfx" / src.name
            dst.parent.mkdir(parents=True, exist_ok=True)
            if not dst.exists():
                shutil.copy(src, dst)
            pk = peak_offset(src)
            ln = file_len(src)
            start = max(t + 1 / FPS - pk, 0) if kind != "riser" else t
            files.append({"t_picture": t, "start": round(start, 3), "kind": kind, "file": f"assets/sfx/{src.name}", "volume": vol,
                          "scene": sc.id, "peak_offset": round(pk, 3), "len": round(ln, 3)})
    return files


CHUNK = 6   # số cảnh tối đa mỗi composition (HyperFrames: nhiều lớp nặng trong một composition có thể ra khung đen)


def chunk(plan, scenes):
    """Chia cảnh thành nhiều composition: tối đa plan["chunk"] cảnh, hoặc ngắt ở cảnh có "chapter": true."""
    n = int(plan.get("chunk", CHUNK))
    parts = []
    for sc in scenes:
        if not parts or len(parts[-1]) >= n or (sc.s.get("chapter") and parts[-1]):
            parts.append([])
        parts[-1].append(sc)
    return parts


def shift(line, t0):
    """Đổi mốc thời gian tuyệt đối (tham số cuối của tl.*) sang mốc trong composition."""
    m = re.search(r",(-?\d+(?:\.\d+)?)\);(\}\)\(\);)?$", line)
    if not m:
        raise ValueError(f"dòng timeline không có mốc thời gian: {line[:80]}")
    return line[:m.start()] + f",{float(m.group(1)) - t0:.3f});" + (m.group(2) or "")


def build(plan, out):
    out = Path(out)
    (out / "compositions").mkdir(parents=True, exist_ok=True)
    (out / "assets").mkdir(exist_ok=True)
    shutil.copy(HERE / "vendor" / "gsap-3.14.2.min.js", out / "assets" / "gsap.min.js")
    base = Path(plan.get("assets_dir", "."))

    def take(p):
        src = Path(p) if Path(p).is_absolute() else base / p
        dst = out / "assets" / src.name
        if not dst.exists():
            shutil.copy(src, dst)
        return f"assets/{src.name}"
    for s in plan["scenes"]:
        if s.get("src"):
            s["src"] = take(s["src"])
        if s.get("srcs"):
            s["srcs"] = [take(x) for x in s["srcs"]]
    scenes, total, g, trans = plan_scenes(plan)
    parts = chunk(plan, scenes)
    hosts = []
    for k, part in enumerate(parts):
        t0 = part[0].T
        dur = max(sc.T + sc.D for sc in part) - t0
        cid = f"part{k}"
        clips = "\n".join(f'<div id="{sc.id}" class="clip sc" data-start="{sc.T - t0:.3f}" data-duration="{sc.D:.3f}" style="z-index:{sc.i + 1};opacity:{1 if sc.i == 0 else 0}">'
                          f'<div class="shk" id="{sc.id}shk">' + "".join(sc.html) + "</div></div>" for sc in part)
        js = "\n".join(shift(line, t0) for sc in part for line in sc.js)
        (out / "compositions" / f"{cid}.html").write_text(
            f'<template>\n<style>{css(g)}</style>\n<div id="root" data-composition-id="{cid}" data-width="{W}" data-height="{H}" data-duration="{dur:.3f}">\n'
            f'{clips}\n</div>\n<script>\nconst tl = gsap.timeline({{ paused: true }});\n{js}\nwindow.__timelines["{cid}"] = tl;\n</script>\n</template>\n',
            encoding="utf-8")
        hosts.append(f'<div id="{cid}" data-composition-id="{cid}" data-composition-src="compositions/{cid}.html" data-start="{t0:.3f}" data-duration="{dur:.3f}" '
                     f'data-track-index="{100 + k}" data-track-kind="graphics" data-width="{W}" data-height="{H}" style="z-index:{k + 1}"></div>')
    used_tex = sorted({m for sc in scenes for h in sc.html for m in re.findall(r"assets/vfx/(\w+)\.png", h)})
    if used_tex:
        (out / "assets" / "vfx").mkdir(exist_ok=True)
        for t in used_tex:
            shutil.copy(HERE / "vfx" / "tex" / f"{t}.png", out / "assets" / "vfx" / f"{t}.png")
    cues = resolve_cues(scenes, g, out)
    audio = []
    free = {}   # xếp track: tiếng chồng nhau thì sang track khác (track 3..)
    for k, c in enumerate(sorted(cues, key=lambda c: c["start"])):
        tr = next(t for t in range(3, 40) if free.get(t, -1) <= c["start"])
        free[tr] = c["start"] + c["len"] + .01
        audio.append(f'<audio id="sfx{k}" class="clip" src="{c["file"]}" data-start="{c["start"]:.3f}" data-duration="{c["len"]:.3f}" '
                     f'data-track-index="{tr}" data-volume="{c["volume"]}"></audio>')
    k = 0
    for sc in scenes:   # âm thanh nền của VFX (mưa, gió, lửa, dưới nước): file 30 giây, nối tiếp nếu cảnh dài hơn
        for t0, d, f, v in sc.amb:
            src = SFX_DIR / f"{f}.mp3"
            dst = out / "assets" / "sfx" / src.name
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy(src, dst)
            pos = 0.0
            while pos < d - .05:
                seg = min(29.5, d - pos)
                audio.append(f'<audio id="amb{k}" class="clip" src="assets/sfx/{src.name}" data-start="{t0 + pos:.3f}" data-duration="{seg:.3f}" '
                             f'data-track-index="{40 + k % 2}" data-volume="{v}" data-fade-in="0.6" data-fade-out="0.8"></audio>')
                pos += seg
                k += 1
    voice = plan.get("voice")
    if voice:
        audio.append(f'<audio id="vo" class="clip" src="{take(voice)}" data-start="{plan.get("voice_start", .6)}" data-track-index="0" data-volume="1"></audio>')
    music = plan.get("music")
    if music:   # nhạc nền: hạ xuống 0,35 khi có lời (ducking), lên lại khi hết
        pts = [{"t": 0, "v": 1.0}]
        for a, b in plan.get("voice_regions", []):
            pts += [{"t": max(a - .3, 0), "v": 1.0}, {"t": a, "v": .35}, {"t": b, "v": .35}, {"t": b + .4, "v": 1.0}]
        lane = json.dumps({"version": 1, "lanes": [{"target": "volume", "points": pts}]}).replace('"', "&quot;")
        audio.append(f'<audio id="bgm" class="clip" src="{take(music)}" data-start="0" data-duration="{total:.3f}" data-track-index="1" '
                     f'data-volume="{plan.get("music_volume", .5)}" data-fade-in="0.4" data-fade-out="1.5" data-automation="{lane}"></audio>')
    (out / "index.html").write_text(
        f'<!doctype html>\n<html lang="en" data-resolution="landscape">\n<head>\n<meta charset="UTF-8" />\n'
        f'<meta name="viewport" content="width={W}, height={H}" />\n<script src="assets/gsap.min.js"></script>\n'
        f'<style>* {{ margin:0; padding:0; box-sizing:border-box; }} html, body {{ width:{W}px; height:{H}px; overflow:hidden; background:{g["bg"]}; }}'
        f' #root {{ position:relative; width:100%; height:100%; background:{g["bg"]}; }}</style>\n</head>\n<body>\n'
        f'<div id="root" data-composition-id="main" data-start="0" data-duration="{total:.3f}" data-width="{W}" data-height="{H}">\n'
        + "\n".join(hosts) + "\n"
        + "\n".join(audio) + '\n</div>\n'
        f'<script>\nwindow.__timelines = window.__timelines || {{}};\nwindow.__timelines["main"] = gsap.timeline({{ paused: true }});\n</script>\n</body>\n</html>\n',
        encoding="utf-8")
    (out / "sfx_cues.json").write_text(json.dumps({"genre": plan.get("genre", "default"), "transitions": trans, "cues": cues},
                                                  ensure_ascii=False, indent=1), encoding="utf-8")
    return total, len(cues)


def finish(src, dst):
    """Chuẩn hóa tiếng 2 lượt: -14 LUFS, đỉnh thật -1 dBTP; hình giữ nguyên."""
    r = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", src, "-af", "loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json",
                        "-f", "null", "-"], capture_output=True, text=True)
    m = json.loads(r.stderr[r.stderr.rfind("{"):r.stderr.rfind("}") + 1])
    af = (f"loudnorm=I=-14:TP=-1.5:LRA=11:measured_I={m['input_i']}:measured_TP={m['input_tp']}:measured_LRA={m['input_lra']}:"
          f"measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", src, "-c:v", "copy", "-af", af, "-ar", "48000", "-c:a", "aac", "-b:a", "192k", dst], check=True)
    r2 = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", dst, "-af", "ebur128=peak=true", "-f", "null", "-"], capture_output=True, text=True)
    i = re.findall(r"I:\s+(-?[\d.]+) LUFS", r2.stderr)
    tp = re.findall(r"Peak:\s+(-?[\d.]+) dBFS", r2.stderr)
    print(f"Tiếng: trước {m['input_i']} LUFS / đỉnh {m['input_tp']} dBTP -> sau {i[-1] if i else '?'} LUFS / đỉnh {tp[-1] if tp else '?'} dBTP. File: {dst}")


def main():
    for s in (sys.stdout, sys.stderr):
        try:
            s.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    if cmd == "presets":
        for k, g in GENRES.items():
            print(f"{k:9} {g['name']}: chữ {g['display']}/{g['body']}, nhấn {g['accent']}, khung ~{g['shot']} s, chuyển cảnh {g['trans']}")
        print("Chuyển cảnh:", ", ".join(TRANSITIONS), "| Hiệu ứng chữ:", ", ".join(TEXT_FX), "| Loại cảnh:", ", ".join(sorted(TYPES)))
        return
    if cmd == "finish" and len(sys.argv) >= 4:
        finish(sys.argv[2], sys.argv[3])
        return
    if cmd not in ("validate", "build") or len(sys.argv) < 3:
        sys.exit(__doc__)
    plan_path = Path(sys.argv[2]).resolve()
    plan = json.loads(plan_path.read_text(encoding="utf-8"))
    ad = plan.get("assets_dir", ".")   # tính theo thư mục của kế hoạch; nếu không có thì theo thư mục đang đứng
    if not Path(ad).is_absolute():
        plan["assets_dir"] = str(plan_path.parent / ad) if (plan_path.parent / ad).exists() else str(Path(ad).resolve())
    errs, rep = validate(json.loads(json.dumps(plan)))
    if errs:
        print("KẾ HOẠCH HỎNG:")
        for e in errs:
            print("  -", e)
        sys.exit(2)
    print(f"Kế hoạch đạt ({rep['genre']}): {rep['scenes']} cảnh, {rep['total']} giây, {rep['changes']} thay đổi "
          f"(trung bình {rep['sec_per_change']} giây), khoảng trống lớn nhất {rep['max_gap']} giây; chuyển cảnh {rep['transitions']}; "
          f"hiệu ứng âm thanh {rep['sfx']} ({rep['sfx_per_min']}/phút); VFX {rep['vfx'] or 'không'}")
    for w in rep["warnings"]:
        print("  cảnh báo:", w)
    if cmd == "build":
        if len(sys.argv) < 4:
            sys.exit("Thiếu thư mục ra")
        total, n = build(plan, sys.argv[3])
        print(f"Đã dựng {sys.argv[3]} ({total:.1f} giây, {n} hiệu ứng âm thanh). Tiếp: npx hyperframes lint, check, render; finish; motion_metrics.py")


if __name__ == "__main__":
    main()
