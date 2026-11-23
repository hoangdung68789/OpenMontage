"""Bộ VFX chuyên dụng cho motion kit (bật khi cần, không mặc định).

Mỗi cảnh trong motion_plan.json có thể có khóa "vfx": danh sách tên hoặc {"fx": tên, ...tham số}.
  "vfx": ["rain", {"fx": "lightning", "at": 3.2}, {"fx": "explosion", "at": 6.0, "x": 62, "y": 48, "power": 1}]

Hai nhóm:
- KHÔNG KHÍ (chạy suốt cảnh hoặc trong [at, at+dur]): rain, snow, sandstorm, fog, smoke, embers, rays, caustics,
  searchlight (tự kèm lớp đêm), alarm. Tối đa 2 lớp mỗi cảnh. Tham số: amount (0.2–1), at, dur.
- SỰ KIỆN (tại thời điểm at): shake, explosion, lightning, glitch, filmburn, sparks, radio. Tham số: at, dur, power, x, y (%).

Kết cấu hình tự sinh (vfx_assets.py -> vfx/tex/*.png), không dùng blur/radial-gradient/clip-path, nên không làm tăng
"lớp nặng" mà HyperFrames cảnh báo. Âm thanh: tự tổng hợp (sfx/synth/*.mp3) + glitch-1..3 (Pixabay License).
An toàn nhấp nháy: không quá 3 lần lóe trong 1 giây (WCAG 2.3.1); báo động đỏ ≤ 1 nhịp/giây (0,9 Hz), độ đậm ≤ 0,35.
Hướng dẫn dùng theo thể loại: references/edit-library.md §10 và genre-recipes.md §4.
"""
import math

ATMOS = {"rain", "snow", "sandstorm", "fog", "smoke", "embers", "rays", "caustics", "searchlight", "alarm"}
EVENTS = {"shake", "explosion", "lightning", "glitch", "filmburn", "sparks", "radio"}
ALL = ATMOS | EVENTS
FLASHERS = {"explosion": [0.0], "lightning": [0.0, 0.42]}   # thời điểm lóe (để kiểm 3 lần/giây)
SOUND = {"boom": ["synth/boom"], "thunder": ["synth/thunder"], "sparks": ["synth/sparks"], "static": ["synth/radio-static"],
         "glitch": ["glitch-1", "glitch-2", "glitch-3"]}
LOOPS = {"rain": ("synth/rain-loop", .22), "snow": ("synth/wind-loop", .10), "sandstorm": ("synth/wind-loop", .26),
         "embers": ("synth/fire-loop", .16), "caustics": ("synth/underwater-loop", .22)}
# bảng VFX hợp với từng thể loại (ngoài bảng thì validate cảnh báo, không chặn)
PALETTE = {
    "war": {"smoke", "embers", "searchlight", "rain", "fog", "shake", "explosion", "sparks", "radio", "filmburn", "sandstorm"},
    "mystery": {"fog", "caustics", "rays", "rain", "lightning", "glitch", "radio", "filmburn"},
    "disaster": {"smoke", "embers", "alarm", "rain", "fog", "shake", "explosion", "sparks", "glitch", "radio"},
    "ancient": {"rays", "embers", "sandstorm", "fog", "filmburn", "shake"},
    "survival": {"snow", "sandstorm", "rain", "fog", "lightning", "shake", "embers"},
}

CSS = """
.shk { position:absolute; inset:0; }
.vfx { position:absolute; pointer-events:none; z-index:4; }
.tw, .safe, .lt { z-index:6; }
.vfx-full { inset:0; }
.vfx-tile { inset:-25%; background-repeat:repeat; }
.vfx-screen { mix-blend-mode:screen; }
.vfx-glow, .vfx-burn { width:1100px; height:1100px; margin:-550px 0 0 -550px; background-size:contain; background-repeat:no-repeat;
  background-position:center; opacity:0; }
.vfx-burn { mix-blend-mode:screen; }
.vfx-deb { width:10px; height:7px; background:#1b1612; border-radius:2px; opacity:0; }
.vfx-spark { width:4px; height:4px; border-radius:50%; background:#FFD58A; box-shadow:0 0 6px 2px rgba(255,170,60,.8); opacity:0; }
.vfx-slice { left:0; right:0; mix-blend-mode:difference; opacity:0; }
"""


def norm(item):
    p = {"fx": item} if isinstance(item, str) else dict(item)
    return p


def tex(name):
    return f"assets/vfx/{name}.png"


def span(sc, p, default_dur=None):
    t0 = sc.T + float(p.get("at", 0))
    d = float(p.get("dur", default_dur if default_dur is not None else sc.D - float(p.get("at", 0))))
    return t0, max(d, .1)


def tile(sc, vid, name, size, opacity, blend=True, rot=0, extra=""):
    st = (f"background-image:url({tex(name)});background-size:{size};opacity:0;"
          + (f"transform:rotate({rot}deg);" if rot else "") + extra)
    sc.html.append(f'<div class="vfx vfx-tile{" vfx-screen" if blend else ""}" id="{vid}" style="{st}"></div>')


def drift(sc, sel, t0, d, dx, dy, opacity, fade=.6):
    sc.a(f'tl.fromTo("{sel}",{{backgroundPosition:"0px 0px"}},{{backgroundPosition:"{dx * d:.0f}px {dy * d:.0f}px",duration:{d:.3f},ease:"none"}},{t0:.3f});')
    f = min(fade, d / 4)
    sc.a(f'tl.fromTo("{sel}",{{opacity:0}},{{opacity:{opacity:.3f},duration:{f:.3f},ease:"sine.out"}},{t0:.3f});')
    sc.a(f'tl.to("{sel}",{{opacity:0,duration:{f:.3f},ease:"sine.in"}},{t0 + d - f:.3f});')


def loop_sound(sc, fx, t0, d, amount):
    if fx in LOOPS:
        f, v = LOOPS[fx]
        sc.amb.append((t0, d, f, round(v * (.6 + .4 * amount), 3)))


# ---------------------------------------------------------------- không khí
def fx_rain(sc, p, rnd, k):
    a, (t0, d) = float(p.get("amount", .7)), span(sc, p)
    sc.html.append(f'<div class="vfx vfx-full" id="{sc.id}v{k}dim" style="background:rgba(8,14,24,.28);opacity:0"></div>')
    sc.a(f'tl.fromTo("#{sc.id}v{k}dim",{{opacity:0}},{{opacity:{a:.2f},duration:.6}},{t0:.3f});')
    tile(sc, f"{sc.id}v{k}a", "rain", "300px 300px", .5 * a, rot=12)
    tile(sc, f"{sc.id}v{k}b", "rain", "512px 512px", .8 * a, rot=12)
    drift(sc, f"#{sc.id}v{k}a", t0, d, 0, 900, .5 * a)
    drift(sc, f"#{sc.id}v{k}b", t0, d, 0, 1500, .8 * a)
    loop_sound(sc, "rain", t0, d, a)


def fx_snow(sc, p, rnd, k):
    a, (t0, d) = float(p.get("amount", .7)), span(sc, p)
    tile(sc, f"{sc.id}v{k}a", "snow_far", "512px 512px", .7 * a)
    tile(sc, f"{sc.id}v{k}b", "snow", "512px 512px", .9 * a)
    drift(sc, f"#{sc.id}v{k}a", t0, d, 12, 45, .7 * a)
    drift(sc, f"#{sc.id}v{k}b", t0, d, -20, 110, .9 * a)
    sc.a(f'tl.fromTo("#{sc.id}v{k}b",{{x:-30}},{{x:30,duration:2.4,ease:"sine.inOut",repeat:{max(int(d / 2.4) - 1, 0)},yoyo:true}},{t0:.3f});')
    loop_sound(sc, "snow", t0, d, a)


def fx_sandstorm(sc, p, rnd, k):
    a, (t0, d) = float(p.get("amount", .7)), span(sc, p)
    sc.html.append(f'<div class="vfx vfx-full" id="{sc.id}v{k}t" style="background:rgba(170,120,60,.5);mix-blend-mode:soft-light;opacity:0"></div>')
    sc.a(f'tl.fromTo("#{sc.id}v{k}t",{{opacity:0}},{{opacity:{a:.2f},duration:.8}},{t0:.3f});')
    tile(sc, f"{sc.id}v{k}a", "sand", "1600px 800px", .45 * a, blend=False)
    tile(sc, f"{sc.id}v{k}b", "sand", "900px 450px", .35 * a, blend=False)
    drift(sc, f"#{sc.id}v{k}a", t0, d, -380, 20, .45 * a)
    drift(sc, f"#{sc.id}v{k}b", t0, d, -720, -10, .35 * a)
    loop_sound(sc, "sandstorm", t0, d, a)


def fx_fog(sc, p, rnd, k):
    a, (t0, d) = float(p.get("amount", .6)), span(sc, p)
    tile(sc, f"{sc.id}v{k}a", "fog", "2000px 1000px", .45 * a, blend=False)
    tile(sc, f"{sc.id}v{k}b", "fog", "1400px 700px", .3 * a, blend=False)
    drift(sc, f"#{sc.id}v{k}a", t0, d, 35, 0, .45 * a, 1.2)
    drift(sc, f"#{sc.id}v{k}b", t0, d, -22, 4, .3 * a, 1.2)


def fx_smoke(sc, p, rnd, k):
    a, (t0, d) = float(p.get("amount", .6)), span(sc, p)
    mask = "-webkit-mask-image:linear-gradient(0deg,#000 0%,#000 30%,transparent 85%);mask-image:linear-gradient(0deg,#000 0%,#000 30%,transparent 85%);"
    tile(sc, f"{sc.id}v{k}a", "smoke", "1200px 1200px", .55 * a, blend=False, extra=mask)
    tile(sc, f"{sc.id}v{k}b", "smoke", "800px 800px", .35 * a, blend=False, extra=mask)
    drift(sc, f"#{sc.id}v{k}a", t0, d, 25, -55, .55 * a, 1.0)
    drift(sc, f"#{sc.id}v{k}b", t0, d, -15, -90, .35 * a, 1.0)


def fx_embers(sc, p, rnd, k):
    a, (t0, d) = float(p.get("amount", .7)), span(sc, p)
    tile(sc, f"{sc.id}v{k}a", "embers", "512px 512px", .9 * a)
    tile(sc, f"{sc.id}v{k}b", "embers", "300px 300px", .6 * a)
    drift(sc, f"#{sc.id}v{k}a", t0, d, 18, -130, .9 * a)
    drift(sc, f"#{sc.id}v{k}b", t0, d, -10, -70, .6 * a)
    sc.a(f'tl.fromTo("#{sc.id}v{k}a",{{x:-25}},{{x:25,duration:1.9,ease:"sine.inOut",repeat:{max(int(d / 1.9) - 1, 0)},yoyo:true}},{t0:.3f});')
    loop_sound(sc, "embers", t0, d, a)


def fx_rays(sc, p, rnd, k):
    a, (t0, d) = float(p.get("amount", .6)), span(sc, p)
    sc.html.append(f'<div class="vfx vfx-full vfx-screen" id="{sc.id}v{k}" style="background-image:url({tex("rays")});'
                   f'background-size:cover;transform-origin:0 0;opacity:0"></div>')
    sc.a(f'tl.fromTo("#{sc.id}v{k}",{{rotation:-2}},{{rotation:2,duration:{d:.3f},ease:"sine.inOut"}},{t0:.3f});')
    n = max(int(d / 3.2), 1)
    sc.a(f'tl.fromTo("#{sc.id}v{k}",{{opacity:0}},{{opacity:{.75 * a:.2f},duration:1.6,ease:"sine.inOut",repeat:{2 * n - 1},yoyo:true}},{t0:.3f});')


def fx_caustics(sc, p, rnd, k):
    a, (t0, d) = float(p.get("amount", .6)), span(sc, p)
    sc.html.append(f'<div class="vfx vfx-full" id="{sc.id}v{k}t" style="background:rgba(20,90,130,.6);mix-blend-mode:soft-light;opacity:0"></div>')
    sc.a(f'tl.fromTo("#{sc.id}v{k}t",{{opacity:0}},{{opacity:{a:.2f},duration:.8}},{t0:.3f});')
    tile(sc, f"{sc.id}v{k}a", "caustics", "700px 700px", .45 * a)
    tile(sc, f"{sc.id}v{k}b", "caustics", "1100px 1100px", .3 * a)
    drift(sc, f"#{sc.id}v{k}a", t0, d, 30, 18, .45 * a)
    drift(sc, f"#{sc.id}v{k}b", t0, d, -20, 26, .3 * a)
    loop_sound(sc, "caustics", t0, d, a)


def fx_searchlight(sc, p, rnd, k):
    a, (t0, d) = float(p.get("amount", .7)), span(sc, p)
    sc.html.append(f'<div class="vfx vfx-full" id="{sc.id}v{k}n" style="background:rgba(4,8,22,.62);opacity:0"></div>')   # lớp đêm
    sc.a(f'tl.fromTo("#{sc.id}v{k}n",{{opacity:0}},{{opacity:{a:.2f},duration:.6}},{t0:.3f});')
    for j, (x, r0, r1, per) in enumerate([(560, -62, -118, 5.5), (1360, -112, -70, 6.5)]):
        vid = f"{sc.id}v{k}{j}"
        sc.html.append(f'<div class="vfx vfx-screen" id="{vid}" style="left:{x}px;top:1100px;width:1800px;height:500px;margin-top:-250px;'
                       f'background-image:url({tex("beam")});background-size:100% 100%;transform-origin:0 50%;opacity:0"></div>')
        sc.a(f'tl.fromTo("#{vid}",{{rotation:{r0}}},{{rotation:{r1},duration:{per / 2:.2f},ease:"sine.inOut",repeat:{max(int(d / (per / 2)) - 1, 0)},yoyo:true}},{t0:.3f});')
        sc.a(f'tl.fromTo("#{vid}",{{opacity:0}},{{opacity:{.6 * a:.2f},duration:.8}},{t0:.3f});')
        sc.a(f'tl.to("#{vid}",{{opacity:0,duration:.6}},{t0 + d - .6:.3f});')


def fx_alarm(sc, p, rnd, k):
    a, (t0, d) = float(p.get("amount", .6)), span(sc, p)
    sc.html.append(f'<div class="vfx vfx-full" id="{sc.id}v{k}" style="background:linear-gradient(90deg,rgba(200,30,20,.9),rgba(200,30,20,0) 30%,'
                   f'rgba(200,30,20,0) 70%,rgba(200,30,20,.9));mix-blend-mode:screen;opacity:0"></div>')
    beats = max(int(d / 1.1), 1)   # 1 nhịp / 1,1 giây: dưới ngưỡng nhấp nháy
    sc.a(f'tl.fromTo("#{sc.id}v{k}",{{opacity:0}},{{opacity:{min(.35, .4 * a):.2f},duration:.55,ease:"sine.inOut",repeat:{2 * beats - 1},yoyo:true}},{t0:.3f});')


# ---------------------------------------------------------------- sự kiện
def shake_on(sc, t, dur, power, rnd):
    kf, n = [], max(int(dur / .05), 4)
    for j in range(n):
        dec = (1 - j / n) ** 1.6
        kf.append(f'{{x:{rnd.uniform(-1, 1) * 22 * power * dec:.1f},y:{rnd.uniform(-1, 1) * 16 * power * dec:.1f},'
                  f'rotation:{rnd.uniform(-1, 1) * .8 * power * dec:.2f},duration:.05,ease:"none"}}')
    kf.append('{x:0,y:0,rotation:0,duration:.08}')
    sc.a(f'tl.to("#{sc.id}shk",{{keyframes:[{",".join(kf)}]}},{t:.3f});')


def fx_shake(sc, p, rnd, k):
    t0, d = span(sc, p, .6)
    shake_on(sc, t0, min(d, 1.5), float(p.get("power", .8)), rnd)
    sc.ev(t0)


def lens(sc, k, t, peak):
    sc.html.append(f'<div class="vfx vfx-full vfx-screen" id="{sc.id}v{k}lens" style="background-image:url({tex("lens")});background-size:cover;opacity:0"></div>')
    sc.a(f'tl.fromTo("#{sc.id}v{k}lens",{{opacity:{peak:.2f}}},{{opacity:0,duration:1.4,ease:"power2.out"}},{t:.3f});')


def fx_explosion(sc, p, rnd, k):
    t0, _ = span(sc, p, 2.5)
    pw, x, y = float(p.get("power", 1)), float(p.get("x", 50)), float(p.get("y", 55))
    sid = f"{sc.id}v{k}"
    sc.html.append(f'<div class="vfx vfx-full" id="{sid}fl" style="background:#FFE2B8;mix-blend-mode:screen;opacity:0"></div>')
    sc.html.append(f'<div class="vfx vfx-glow" id="{sid}g" style="left:{x}%;top:{y}%;background-image:url({tex("glow")})"></div>')
    sc.html.append(f'<div class="vfx vfx-glow" id="{sid}sm" style="left:{x}%;top:{y}%;background-image:url({tex("smoke")});filter:brightness(.45);border-radius:50%;'
                   f'-webkit-mask-image:linear-gradient(0deg,transparent,#000 30%,#000 70%,transparent);mask-image:linear-gradient(0deg,transparent,#000 30%,#000 70%,transparent)"></div>')
    sc.a(f'tl.fromTo("#{sid}fl",{{opacity:{.55 * pw:.2f}}},{{opacity:0,duration:.3,ease:"power2.out"}},{t0:.3f});')
    sc.a(f'tl.fromTo("#{sid}g",{{scale:.15,opacity:1}},{{scale:{1.4 + .8 * pw:.2f},opacity:0,duration:1.3,ease:"expo.out"}},{t0:.3f});')
    sc.a(f'tl.fromTo("#{sid}sm",{{scale:.3,opacity:0}},{{scale:1.6,opacity:.7,duration:1.2,ease:"power2.out"}},{t0 + .15:.3f});')
    sc.a(f'tl.to("#{sid}sm",{{y:-120,opacity:0,duration:2.2,ease:"sine.in"}},{t0 + 1.35:.3f});')
    for j in range(12):   # mảnh vỡ: bay ra rồi rơi theo trọng lực
        ang = rnd.uniform(0, 2 * math.pi)
        v = rnd.uniform(260, 620) * pw
        dx, dy = math.cos(ang) * v, math.sin(ang) * v - 200
        sc.html.append(f'<div class="vfx vfx-deb" id="{sid}d{j}" style="left:{x}%;top:{y}%"></div>')
        sc.a(f'tl.fromTo("#{sid}d{j}",{{x:0,y:0,rotation:0,opacity:1}},{{keyframes:[{{x:{dx * .6:.0f},y:{dy * .6:.0f},rotation:{rnd.uniform(-400, 400):.0f},duration:.45,ease:"power2.out"}},'
             f'{{x:{dx:.0f},y:{dy + 520:.0f},opacity:0,duration:.85,ease:"power2.in"}}]}},{t0:.3f});')
    lens(sc, k, t0, .55 * pw)
    shake_on(sc, t0, .9, pw, rnd)
    sc.cue(t0, "boom", .7)
    sc.ev(t0)


def bolt_path(rnd, x0, y0, y1):
    pts, x, y = [(x0, y0)], x0, y0
    while y < y1:
        y += rnd.uniform(40, 90)
        x += rnd.uniform(-55, 55)
        pts.append((x, min(y, y1)))
    return "M" + " L".join(f"{a:.0f},{b:.0f}" for a, b in pts)


def fx_lightning(sc, p, rnd, k):
    t0, _ = span(sc, p, 1.5)
    sid = f"{sc.id}v{k}"
    x = float(p.get("x", rnd.uniform(25, 75))) / 100 * 1920
    sc.html.append(f'<div class="vfx vfx-full" id="{sid}fl" style="background:#DCE6FF;mix-blend-mode:screen;opacity:0"></div>')
    sc.html.append(f'<svg class="vfx vfx-full" id="{sid}b" viewBox="0 0 1920 1080" style="opacity:0"><path d="{bolt_path(rnd, x, -10, rnd.uniform(520, 760))}" '
                   f'fill="none" stroke="#F4F7FF" stroke-width="5" stroke-linejoin="round"/><path d="{bolt_path(rnd, x, -10, 420)}" fill="none" stroke="#F4F7FF" '
                   f'stroke-width="2" opacity=".7"/></svg>')
    # 2 lần lóe cách 0,42 s (< 3 lần/giây), viết thành MỘT tween keyframes để tua tới đâu cũng đúng
    sc.a(f'tl.fromTo("#{sid}fl",{{opacity:0}},{{keyframes:[{{opacity:.7,duration:.001}},{{opacity:0,duration:.22,ease:"power2.out"}},'
         f'{{opacity:0,duration:.199}},{{opacity:.45,duration:.001}},{{opacity:0,duration:.22,ease:"power2.out"}}]}},{t0:.3f});')
    sc.a(f'tl.fromTo("#{sid}b",{{opacity:0}},{{keyframes:[{{opacity:1,duration:.001}},{{opacity:0,duration:.16}},'
         f'{{opacity:0,duration:.259}},{{opacity:1,duration:.001}},{{opacity:0,duration:.16}}]}},{t0:.3f});')
    lens(sc, k, t0, .4)
    sc.cue(t0 + .3, "thunder", .6)     # tiếng sấm đến sau ánh chớp
    sc.ev(t0)


def fx_glitch(sc, p, rnd, k):
    t0, d = span(sc, p, .5)
    d = min(d, 1.0)
    sid = f"{sc.id}v{k}"
    cols = ["#00E5FF", "#FF2D6F", "#FFFFFF", "#7CFF4F"]
    for j in range(6):
        sc.html.append(f'<div class="vfx vfx-slice" id="{sid}s{j}" style="top:0;height:{rnd.randint(8, 60)}px;background:{cols[j % 4]}"></div>')
    steps = max(int(d / (2 / 30)), 2)
    for st in range(steps):
        t = t0 + st * 2 / 30
        for j in range(6):
            on = rnd.random() < .55
            sc.a(f'tl.set("#{sid}s{j}",{{y:{rnd.randint(0, 1040)},x:{rnd.randint(-80, 80)},opacity:{rnd.uniform(.35, .8) if on else 0:.2f}}},{t:.3f});')
        sc.a(f'tl.set("#{sc.id}shk",{{x:{rnd.randint(-24, 24)}}},{t:.3f});')
    for j in range(6):
        sc.a(f'tl.set("#{sid}s{j}",{{opacity:0}},{t0 + steps * 2 / 30:.3f});')
    sc.a(f'tl.set("#{sc.id}shk",{{x:0}},{t0 + steps * 2 / 30:.3f});')
    sc.cue(t0, "glitch", .45)
    sc.ev(t0)


def fx_filmburn(sc, p, rnd, k):
    t0, d = span(sc, p, 1.4)
    sid = f"{sc.id}v{k}"
    x, y = float(p.get("x", rnd.choice([12, 88]))), float(p.get("y", rnd.uniform(20, 80)))
    sc.html.append(f'<div class="vfx vfx-burn" id="{sid}" style="left:{x}%;top:{y}%;background-image:url({tex("burn")})"></div>')
    sc.a(f'tl.fromTo("#{sid}",{{scale:.3,opacity:0}},{{keyframes:[{{scale:1.6,opacity:.95,duration:{d * .45:.2f},ease:"power2.in"}},'
         f'{{scale:3.2,opacity:0,duration:{d * .55:.2f},ease:"power1.out"}}]}},{t0:.3f});')
    sc.ev(t0)


def fx_sparks(sc, p, rnd, k):
    t0, _ = span(sc, p, 1.5)
    sid, x, y = f"{sc.id}v{k}", float(p.get("x", 50)), float(p.get("y", 60))
    for j in range(16):
        ang = rnd.uniform(-math.pi * .95, -math.pi * .05)
        v = rnd.uniform(180, 420)
        dx, dy = math.cos(ang) * v, math.sin(ang) * v
        sc.html.append(f'<div class="vfx vfx-spark" id="{sid}p{j}" style="left:{x}%;top:{y}%"></div>')
        sc.a(f'tl.fromTo("#{sid}p{j}",{{x:0,y:0,opacity:1}},{{keyframes:[{{x:{dx * .7:.0f},y:{dy * .7:.0f},duration:.35,ease:"power2.out"}},'
             f'{{x:{dx:.0f},y:{dy + 380:.0f},opacity:0,duration:.75,ease:"power2.in"}}]}},{t0 + j * .015:.3f});')
    sc.cue(t0, "sparks", .4)
    sc.ev(t0)


def fx_radio(sc, p, rnd, k):
    """Nhiễu sóng: lớp nhiễu TV mờ + tiếng radio rè (đọc điện đàm, băng ghi âm, máy quay cũ)."""
    t0, d = span(sc, p, 1.2)
    sid = f"{sc.id}v{k}"
    sc.html.append(f'<div class="vfx vfx-tile" id="{sid}" style="background-image:url({tex("static")});background-size:512px 512px;mix-blend-mode:overlay;opacity:0"></div>')
    steps = max(int(d / (2 / 30)), 2)
    for st in range(steps):   # độ mờ thấp và đổi vị trí, không đổi độ sáng mạnh -> không tính là lóe
        sc.a(f'tl.set("#{sid}",{{opacity:{rnd.uniform(.12, .22):.2f},backgroundPosition:"{rnd.randint(0, 511)}px {rnd.randint(0, 511)}px"}},{t0 + st * 2 / 30:.3f});')
    sc.a(f'tl.set("#{sid}",{{opacity:0}},{t0 + steps * 2 / 30:.3f});')
    sc.cue(t0, "static", .35)
    sc.ev(t0)


FX = {n: globals()[f"fx_{n}"] for n in ALL}


def apply(sc, rnd):
    for k, item in enumerate(sc.s.get("vfx") or []):
        p = norm(item)
        FX[p["fx"]](sc, p, rnd, k)


def check(plan, genre):
    """Trả (lỗi, cảnh báo) cho khóa vfx của kế hoạch."""
    errs, warns, flashes, t = [], [], [], 0.0
    pal = PALETTE.get(genre)
    for i, s in enumerate(plan.get("scenes", [])):
        items = [norm(x) for x in (s.get("vfx") or [])]
        dur = float(s.get("dur", 0))
        for p in items:
            name = p.get("fx")
            if name not in ALL:
                errs.append(f"cảnh {i}: vfx '{name}' không có (có: {', '.join(sorted(ALL))})")
                continue
            at = float(p.get("at", 0))
            if not 0 <= at < dur:
                errs.append(f"cảnh {i}: vfx '{name}' at={at} nằm ngoài cảnh (0–{dur})")
            if not .1 <= float(p.get("amount", .6)) <= 1:
                errs.append(f"cảnh {i}: vfx '{name}' amount phải trong 0,1–1")
            if pal and name not in pal:
                warns.append(f"cảnh {i}: '{name}' không nằm trong bảng VFX của thể loại '{genre}' (genre-recipes.md §4): kiểm lý do")
            for dt in FLASHERS.get(name, []):
                flashes.append(t + at + dt)
            if s.get("transition") == "flash":
                flashes.append(t)
        atm = [p["fx"] for p in items if p.get("fx") in ATMOS]
        if len(atm) > 2:
            errs.append(f"cảnh {i}: {len(atm)} lớp không khí > 2 ({', '.join(atm)}): rối hình")
        big = [p["fx"] for p in items if p.get("fx") in ("explosion", "lightning")]
        if len(big) > 1 and dur < 8:
            errs.append(f"cảnh {i}: {len(big)} sự kiện lớn trong cảnh {dur} giây: mỗi cú phải có chỗ thở (≥ 8 giây cho 2 cú)")
        t += dur
    flashes.sort()
    for j, a in enumerate(flashes):
        if sum(1 for b in flashes[j:] if b - a < 1.0) > 3:
            errs.append(f"hơn 3 lần lóe trong 1 giây quanh {a:.1f} s: nguy cơ động kinh (WCAG 2.3.1)")
            break
    return errs, warns
