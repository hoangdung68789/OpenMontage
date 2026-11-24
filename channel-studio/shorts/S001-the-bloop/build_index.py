"""Sinh render/index.html (HyperFrames 1080x1920) cho S001 The Bloop từ build/timeline.json + build/words.json.
python build_index.py   (chạy trong thư mục S001-the-bloop)
"""
import json
import random
from pathlib import Path

HERE = Path(__file__).resolve().parent
TL = json.loads((HERE / "build/timeline.json").read_text())
WORDS = json.loads((HERE / "build/words.json").read_text())
SEG = {s["id"]: s for s in TL["segments"]}
TOTAL = TL["total"]
W, H = 1080, 1920

# Sửa chữ whisper nghe sai (lời thật theo script.md), gộp số tách đôi
FIX = {"Oh,": "NOAA", "Ships": "Ship's"}
words = []
for w in WORDS:
    t = FIX.get(w["w"], w["w"])
    if t.startswith(",") and words:
        words[-1]["w"] += t
        words[-1]["e"] = w["e"]
        continue
    if t.lower().startswith("quake") and words and words[-1]["w"].lower() == "ice":
        words[-1]["w"] = "ice" + t
        words[-1]["e"] = w["e"]
        continue
    words.append({"w": t, "s": w["s"], "e": w["e"]})


def at(token, after=0.0):
    """Mốc bắt đầu của từ đầu tiên chứa token, sau thời điểm after."""
    for w in words:
        if w["s"] >= after and token.lower() in w["w"].lower():
            return w["s"]
    raise KeyError(token)


B = {k: (SEG[k]["start"], SEG[k]["start"] + SEG[k]["dur"]) for k in SEG}
b2s, b4s, b5s, b6s = B["B2"][0], B["B4"][0], B["B5"][0], B["B6"][0]
blo_s, blo_e = B["BLOOP"]

# Phụ đề: nhóm 3 từ, ngắt ở dấu câu; bỏ B1 (chữ hook đã là câu đó) và đoạn tiếng Bloop
groups, cur = [], []
for w in words:
    if w["s"] < b2s - 0.05:
        continue
    cur.append(w)
    if len(cur) == 3 or w["w"][-1] in ".,?!:":
        groups.append(cur)
        cur = []
if cur:
    groups.append(cur)
caps = []
for i, g in enumerate(groups):
    s = g[0]["s"]
    e = groups[i + 1][0]["s"] if i + 1 < len(groups) else g[-1]["e"] + 0.4
    e = min(e, g[-1]["e"] + 0.6)
    caps.append((round(s, 3), round(max(e - s, 0.35), 3), " ".join(x["w"] for x in g).rstrip(",")))

# Bụi biển (lớp không khí): vị trí cố định theo seed
rnd = random.Random(1997)
snow = [(rnd.uniform(0, W), rnd.uniform(0, H), rnd.uniform(3, 9), rnd.uniform(.15, .55), rnd.uniform(-160, -60)) for _ in range(46)]

shots = [  # id, src, start, dur, media_start, rate, zoom từ→đến, origin
    ("v1", "jelly.mp4", 0.0, b2s, 7.0, 1, (1.06, 1.18), "50% 30%"),
    ("v4a", "isopod.mp4", b4s, B["B4"][1] - b4s, 0.0, 1, (1.04, 1.22), "50% 55%"),  # bỏ phim bạch tuộc: ghi "Footage: Ocean Exploration Trust", PD không chắc
    ("v5", "antarctica_sat.mp4", b5s, B["B5"][1] - b5s, 0.0, 0.85, (1.12, 1.22), "50% 70%"),
    ("v6", "calving.mp4", b6s, TOTAL - b6s, 0.0, 1, (1.04, 1.14), "50% 60%"),
]

theory = [("A SECRET MILITARY TEST?", at("military", b4s) - 0.35), ("A SHIP'S ENGINE?", at("engine", b4s) - 0.35),
          ("A GIANT SQUID?", at("squid", b4s) - 0.35), ("SOMETHING UNKNOWN?", at("unknown", b4s) - 0.35)]
t_nobody = at("nobody", b4s)
t_2005 = at("2005", b5s)
t_ant = at("Antarctica", b5s)
t_ice = at("icequake", b6s)
t_monster = at("monster", b6s)
t_bloopname = at("Bloop", b2s)
t_mics = at("Microphones", b2s)

css = f"""
* {{ margin:0; padding:0; box-sizing:border-box; }}
html, body {{ width:{W}px; height:{H}px; overflow:hidden; background:#02070d; }}
#root {{ position:relative; width:{W}px; height:{H}px; overflow:hidden; background:#02070d; font-family:Montserrat,sans-serif; color:#EEF4F7; }}
.shot {{ position:absolute; inset:0; opacity:0; }}
.shot video {{ position:absolute; left:0; top:0; width:{W}px; height:{H}px; object-fit:cover; }}
.shade {{ position:absolute; inset:0; background:linear-gradient(180deg, rgba(2,7,13,.55) 0%, rgba(2,7,13,0) 22%, rgba(2,7,13,0) 52%, rgba(2,7,13,.78) 100%); }}
#v5w .shade {{ background:linear-gradient(180deg, rgba(2,7,13,.8) 0%, rgba(2,7,13,.62) 40%, rgba(2,7,13,.55) 60%, rgba(2,7,13,.85) 100%); }}
#v6w .shade {{ background:linear-gradient(180deg, rgba(2,7,13,.85) 0%, rgba(2,7,13,.6) 34%, rgba(2,7,13,.15) 56%, rgba(2,7,13,.82) 100%); }}
.vig {{ position:absolute; inset:0; background:radial-gradient(ellipse at 50% 45%, rgba(0,0,0,0) 45%, rgba(0,0,0,.55) 100%); pointer-events:none; }}
.snow i {{ position:absolute; border-radius:50%; background:#cfe6f2; display:block; }}
.gfx {{ position:absolute; inset:0; opacity:0; background:radial-gradient(ellipse at 50% 40%, #0b2740 0%, #04111d 60%, #02070d 100%); }}
.hook {{ position:absolute; left:70px; right:70px; top:760px; font-family:"Archivo Black",sans-serif; font-size:92px; line-height:1.02; letter-spacing:.005em; text-transform:uppercase; text-shadow:0 6px 30px rgba(0,0,0,.8); }}
.hook b {{ color:#7FD3F2; font-weight:400; }}
.badge {{ position:absolute; left:70px; top:640px; font:800 40px Montserrat,sans-serif; letter-spacing:.3em; color:#7FD3F2; }}
.cap {{ position:absolute; left:80px; right:80px; top:1170px; text-align:center; font:800 62px/1.15 Montserrat,sans-serif; color:#fff; text-shadow:0 0 18px rgba(0,0,0,.9), 0 4px 6px rgba(0,0,0,.9); }}
.title {{ position:absolute; left:60px; right:60px; text-align:center; font-family:"Archivo Black",sans-serif; text-transform:uppercase; text-shadow:0 6px 30px rgba(0,0,0,.85); }}
.kicker {{ position:absolute; left:0; right:0; text-align:center; font:700 34px Montserrat,sans-serif; letter-spacing:.32em; color:#7FD3F2; text-transform:uppercase; text-shadow:0 0 14px rgba(0,0,0,.95), 0 2px 4px rgba(0,0,0,.9); }}
.theory {{ position:absolute; left:70px; right:70px; font-family:"Archivo Black",sans-serif; font-size:76px; line-height:1.05; text-transform:uppercase; text-shadow:0 6px 26px rgba(0,0,0,.9); }}
.spec {{ position:absolute; left:90px; top:560px; width:900px; height:700px; overflow:hidden; border:3px solid rgba(127,211,242,.55); border-radius:10px; box-shadow:0 30px 80px rgba(0,0,0,.6); }}
.spec img {{ width:900px; height:700px; display:block; }}
.playhead {{ position:absolute; top:0; bottom:0; left:0; width:5px; background:#fff; box-shadow:0 0 22px #7FD3F2; }}
.tag {{ position:absolute; left:0; right:0; top:250px; text-align:center; font:800 36px Montserrat,sans-serif; letter-spacing:.38em; color:#7FD3F2; }}
.src {{ position:absolute; left:0; right:0; top:1290px; text-align:center; font:600 28px Montserrat,sans-serif; color:rgba(238,244,247,.75); letter-spacing:.08em; }}
"""

h = []
a = h.append
a(f'<div id="root" data-composition-id="main" data-start="0" data-duration="{TOTAL}" data-width="{W}" data-height="{H}">')
# Lớp phim
for i, (sid, src, s, d, ms, rate, _, _) in enumerate(shots):
    a(f'<div class="shot" id="{sid}w" style="z-index:{2 + i}{';opacity:1' if s == 0 else ''}"><video id="{sid}" class="clip" src="assets/video/{src}" data-start="{s:.3f}" '
      f'data-duration="{d:.3f}" data-media-start="{ms}" data-playback-rate="{rate}" data-track-index="{1 + i}" muted playsinline></video>'
      f'<div class="shade"></div></div>')
# Cảnh đồ họa B2 (sóng âm, micro cách xa) và B3 (phổ tần tiếng thật)
cx, cy = 540, 620
rings = "".join(f'<circle id="r{k}" cx="{cx}" cy="{cy}" r="40" fill="none" stroke="#7FD3F2" stroke-width="4" opacity="0"/>' for k in range(5))
a(f'<div class="gfx" id="g2" style="z-index:8"><svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" style="position:absolute;inset:0">'
  + "".join(f'<line x1="0" y1="{y}" x2="{W}" y2="{y}" stroke="#1d4766" stroke-width="1" opacity=".5"/>' for y in range(140, H, 120))
  + "".join(f'<line x1="{x}" y1="0" x2="{x}" y2="{H}" stroke="#1d4766" stroke-width="1" opacity=".5"/>' for x in range(60, W, 120))
  + rings
  + f'<line id="link" x1="150" y1="900" x2="930" y2="900" stroke="#FFD27A" stroke-width="5" stroke-dasharray="18 14" pathLength="1000" stroke-dashoffset="1000"/>'
  + '<circle id="h1" cx="150" cy="900" r="18" fill="#FFD27A" opacity="0"/><circle id="h2" cx="930" cy="900" r="18" fill="#FFD27A" opacity="0"/>'
  + f'<circle cx="{cx}" cy="{cy}" r="16" fill="#fff"/></svg>'
  + '<div class="kicker" id="k2" style="top:300px;opacity:0">South Pacific · NOAA hydrophones</div>'
  + '<div class="title" id="dist" style="top:960px;font-size:64px;color:#FFD27A;opacity:0">2,000+ miles apart</div>'
  + '<div class="title" id="bname" style="top:380px;font-size:150px;opacity:0">"The Bloop"</div></div>')
a('<div class="gfx" id="g3" style="z-index:9"><div class="kicker" style="top:330px">NOAA recording · 1997</div>'
  '<div class="title" style="top:400px;font-size:84px">The real sound</div>'
  '<div class="spec" id="spec"><img src="assets/img/spectrum.png" alt="Spectrogram of the Bloop recording"><div class="playhead" id="ph"></div></div>'
  '<div class="src" style="top:1290px" id="g3s">Sped up 16× · Source: NOAA PMEL</div></div>')
# Bụi biển
a('<div class="snow" id="snow" style="position:absolute;inset:0;z-index:12;pointer-events:none">'
  + "".join(f'<i id="s{k}" style="left:{x:.0f}px;top:{y:.0f}px;width:{r:.1f}px;height:{r:.1f}px;opacity:{o:.2f}"></i>' for k, (x, y, r, o, _) in enumerate(snow))
  + '</div><div class="vig" style="z-index:13"></div>')
# Chữ
a('<div id="hookw" style="position:absolute;inset:0;z-index:20"><div class="badge" id="badge">PACIFIC OCEAN · 1997</div>'
  '<div class="hook" id="hook">The ocean made <b>a sound</b> no one could explain</div></div>')
for k, (txt, s) in enumerate(theory):
    a(f'<div class="theory" id="t{k}" style="z-index:21;top:{300 + k * 190}px;opacity:0">{txt}</div>')
a('<div class="title" id="y2005" style="z-index:21;top:330px;font-size:220px;color:#FFD27A;opacity:0">2005</div>')
a('<div class="kicker" id="kant" style="z-index:21;top:590px;font-size:38px;letter-spacing:.2em;opacity:0">Closer to Antarctica</div>')
a('<div class="title" id="iq" style="z-index:21;top:330px;font-size:150px;color:#BFE9FF;opacity:0">Icequake</div>')
a('<div class="title" id="mon" style="z-index:22;top:620px;font-size:104px;line-height:1.02;opacity:0">The monster<br>was <span style="color:#7FD3F2">ice.</span></div>')
a('<div class="tag" id="tag" style="z-index:22;opacity:0">EARTH\'S UNSOLVED #1</div>')
a('<div class="src" id="credit" style="z-index:22;top:1090px;opacity:0">Sources: NOAA Ocean Service · NOAA PMEL</div>')
# Phụ đề (một host captions)
a('<div id="caps" style="position:absolute;inset:0;z-index:30" data-track-kind="captions">')
for k, (s, d, txt) in enumerate(caps):
    a(f'<div class="cap clip" id="c{k}" data-start="{s}" data-duration="{d}" data-track-index="20">{txt}</div>')
a('</div>')
# Âm thanh
a(f'<audio id="vo" class="clip" src="assets/audio/narration.wav" data-start="0" data-duration="{TOTAL}" data-track-index="30" data-volume="1"></audio>')
a(f'<audio id="bed" class="clip" src="assets/audio/bed.mp3" data-start="0" data-duration="{TOTAL}" data-track-index="31" data-volume="0.16"></audio>')
for k, t in enumerate([b2s, b4s, b5s, b6s]):
    a(f'<audio id="wh{k}" class="clip" src="assets/audio/whoosh-cinematic.mp3" data-start="{max(t - 0.35, 0):.3f}" data-duration="1.6" data-track-index="{32 + k}" data-volume="0.35"></audio>')
a(f'<audio id="hit" class="clip" src="assets/audio/impact-bass-1.mp3" data-start="{t_monster - 0.1:.3f}" data-duration="{TOTAL - t_monster + 0.1:.3f}" data-track-index="36" data-volume="0.55"></audio>')
a('</div>')

js = ["const tl = gsap.timeline({ paused: true });"]
j = js.append
X = 0.45  # hòa hình
for sid, src, s, d, ms, rate, (z0, z1), org in shots:
    j(f'tl.set("#{sid}w",{{transformOrigin:"{org}"}},0);')
    j(f'tl.fromTo("#{sid}w",{{opacity:0}},{{opacity:1,duration:{X},ease:"none"}},{s:.3f});' if s > 0 else f'tl.set("#{sid}w",{{opacity:1}},0);')
    j(f'tl.fromTo("#{sid}w",{{scale:{z0}}},{{scale:{z1},duration:{d:.3f},ease:"none"}},{s:.3f});')
    j(f'tl.to("#{sid}w",{{opacity:0,duration:{X},ease:"none"}},{s + d - 0.02:.3f});')
# B2
g2s, g2e = b2s, B["B3"][0]
j(f'tl.fromTo("#g2",{{opacity:0}},{{opacity:1,duration:{X}}},{g2s - 0.2:.3f}); tl.to("#g2",{{opacity:0,duration:{X}}},{g2e:.3f});')
j(f'tl.to("#k2",{{opacity:1,duration:.5}},{g2s + .3:.3f});')
for k in range(5):
    j(f'tl.fromTo("#r{k}",{{attr:{{r:30}},opacity:.9}},{{attr:{{r:560}},opacity:0,duration:3.2,ease:"sine.out",repeat:3,repeatDelay:.0}},{g2s + .4 + k * .65:.3f});')
j(f'tl.to(["#h1","#h2"],{{opacity:1,duration:.4,stagger:.25}},{t_mics:.3f}); tl.to("#link",{{attr:{{"stroke-dashoffset":0}},duration:1.4,ease:"power2.inOut"}},{t_mics + .3:.3f});')
j(f'tl.fromTo("#dist",{{opacity:0,y:30}},{{opacity:1,y:0,duration:.6,ease:"power3.out"}},{t_mics + 1.2:.3f});')
j(f'tl.to("#k2",{{opacity:0,duration:.3}},{t_bloopname - .3:.3f});')
j(f'tl.fromTo("#bname",{{opacity:0,scale:.8}},{{opacity:1,scale:1,duration:.5,ease:"back.out(2)"}},{t_bloopname:.3f}); tl.to("#bname",{{scale:1.08,duration:{g2e - t_bloopname:.3f},ease:"none"}},{t_bloopname + .5:.3f});')
# B3 + tiếng Bloop
g3s = B["B3"][0]
j(f'tl.fromTo("#g3",{{opacity:0}},{{opacity:1,duration:{X}}},{g3s - 0.1:.3f}); tl.to("#g3",{{opacity:0,duration:{X}}},{blo_e:.3f});')
j(f'tl.fromTo("#spec",{{scale:.92}},{{scale:1.06,duration:{blo_e - g3s:.3f},ease:"none"}},{g3s:.3f});')
j(f'tl.fromTo("#ph",{{x:0}},{{x:895,duration:{blo_e - blo_s:.3f},ease:"none"}},{blo_s:.3f});')
# Hook
j('tl.fromTo("#hook",{scale:1},{scale:1.06,duration:5.4,ease:"none",transformOrigin:"0% 50%"},0);')
j(f'tl.to("#hookw",{{opacity:0,duration:.4}},{b2s - .45:.3f});')
# Giả thuyết
for k, (txt, s) in enumerate(theory):
    j(f'tl.fromTo("#t{k}",{{opacity:0,x:-60}},{{opacity:1,x:0,duration:.35,ease:"power3.out"}},{s:.3f});')
    if k:
        j(f'tl.to("#t{k - 1}",{{opacity:.38,duration:.3}},{s:.3f});')
j(f'tl.to(["#t0","#t1","#t2","#t3"],{{opacity:0,duration:.4}},{t_nobody - .1:.3f});')
# B5
j(f'tl.fromTo("#kant",{{opacity:0,y:20}},{{opacity:1,y:0,duration:.5}},{t_ant - .2:.3f});')
j(f'tl.fromTo("#y2005",{{opacity:0,scale:1.25}},{{opacity:1,scale:1,duration:.5,ease:"power3.out"}},{t_2005 - .1:.3f}); tl.to(["#y2005","#kant"],{{opacity:0,duration:.4}},{B["B5"][1] - .4:.3f});')
# B6
j(f'tl.fromTo("#iq",{{opacity:0,y:40}},{{opacity:1,y:0,duration:.5,ease:"power3.out"}},{t_ice - .1:.3f}); tl.to("#iq",{{opacity:0,duration:.4}},{t_monster - .5:.3f});')
j(f'tl.fromTo("#mon",{{opacity:0,scale:.9}},{{opacity:1,scale:1,duration:.6,ease:"power3.out"}},{t_monster - .05:.3f}); tl.to("#mon",{{scale:1.05,duration:{TOTAL - t_monster - .6:.3f},ease:"none"}},{t_monster + .55:.3f});')
j(f'tl.to("#tag",{{opacity:1,duration:.5}},{t_ice + 1.2:.3f}); tl.to("#credit",{{opacity:1,duration:.4}},{t_monster + .7:.3f});')
# Bụi trôi suốt video
for k, (x, y, r, o, dy) in enumerate(snow):
    j(f'tl.fromTo("#s{k}",{{y:0}},{{y:{dy:.0f},x:{(k % 7 - 3) * 6},duration:{TOTAL},ease:"none"}},0);')
j('window.__timelines = window.__timelines || {}; window.__timelines["main"] = tl;')

html = (f'<!doctype html>\n<html lang="en" data-resolution="portrait">\n<head>\n<meta charset="UTF-8" />\n'
        f'<meta name="viewport" content="width={W}, height={H}" />\n<script src="assets/gsap.min.js"></script>\n'
        f'<style>{css}</style>\n</head>\n<body>\n' + "\n".join(h) + "\n<script>\n" + "\n".join(js) + "\n</script>\n</body>\n</html>\n")
(HERE / "render/index.html").write_text(html, encoding="utf-8")
print("captions", len(caps), "total", TOTAL, "theory", [round(s, 2) for _, s in theory], "2005", t_2005, "ice", t_ice, "monster", t_monster)
