"""ICYFOX MOTION KIT: dựng dự án HyperFrames có CHUYỂN ĐỘNG LIÊN TỤC từ một kế hoạch cảnh (JSON).

  python icyfox_motion.py validate <plan.json>           # kiểm kế hoạch chuyển động TRƯỚC khi dựng (mã thoát 2 nếu hỏng)
  python icyfox_motion.py build <plan.json> <thư_mục_ra>  # sinh index.html + compositions/body.html + assets
  (sau đó) npx hyperframes lint|check|render <thư_mục_ra>; python ../../.claude/skills/hoang-dung-clay-lapis-studio/scripts/motion_metrics.py out.mp4

Vì sao có kit này: video 002 đứng yên 71% ở phần giữa (đối thủ 0–3,5%), vì các cảnh chỉ có hiệu ứng XUẤT HIỆN rồi đứng.
Kit ép 3 lớp chuyển động cho MỌI cảnh, suốt thời lượng cảnh (references/motion-graphics.md):
  1. máy quay: đẩy/kéo/lia liên tục, ease "none" hoặc "sine.inOut", không bao giờ dừng
  2. không khí: bụi trôi, hạt film, vệt sáng quét (seed cố định, không Math.random)
  3. nhịp: mỗi <= 8 giây có một thay đổi đọc được (đổi khung cận chi tiết, chữ hiện, đường vẽ, số đếm)
Loại cảnh: title, photo, document, map, stat, quote. Ảnh: chỉ PD/CC0/CC BY(-SA) đã ghi công (policy-guardrails.md).
"""
import html
import json
import random
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
W, H = 1920, 1080
XF = 0.7                 # hòa hình giữa hai cảnh / hai khung
MAX_GAP = 8.0            # tối đa 8 giây giữa hai thay đổi đọc được
SHOT = 6.5               # cảnh ảnh dài hơn ~8 giây được tự chia thành khung khoảng 6,5 giây
BG, INK, PAPER, TERRA, LAPIS, GOLD = "#1B1714", "#F1EBE0", "#E8DFCC", "#B5734A", "#1F4E8C", "#C9A54C"
esc = html.escape
TYPES = {"title", "photo", "document", "map", "stat", "quote"}

CSS = f"""
#root {{ position:relative; width:{W}px; height:{H}px; overflow:hidden; background:{BG}; color:{INK}; font-family:Georgia,"Times New Roman",serif; }}
.sc {{ position:absolute; inset:0; overflow:hidden; background:{BG}; }}
.cam {{ position:absolute; inset:0; transform-origin:50% 50%; will-change:transform; }}
.desk {{ position:absolute; inset:-10%; background:radial-gradient(ellipse at 50% 45%, #3a2e25 0%, {BG} 70%); }}
.print {{ position:absolute; left:50%; top:50%; transform:translate(-50%,-50%); }}
.print .pw {{ position:relative; display:inline-block; }}
.print img {{ display:block; height:760px; width:auto; max-width:1500px; object-fit:contain; border:14px solid {PAPER}; background:{PAPER}; box-shadow:0 30px 90px rgba(0,0,0,.65); }}
.full img {{ position:absolute; inset:0; width:100%; height:100%; object-fit:cover; }}
.vig {{ position:absolute; inset:0; pointer-events:none; background:radial-gradient(ellipse at center, rgba(27,23,20,0) 48%, rgba(27,23,20,.88) 100%); }}
.grain {{ position:absolute; inset:-50%; opacity:.10; pointer-events:none; mix-blend-mode:overlay;
  background-image:url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='240' height='240'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='.9' numOctaves='2' stitchTiles='stitch'/></filter><rect width='100%' height='100%' filter='url(%23n)'/></svg>"); }}
.dust i {{ position:absolute; border-radius:50%; background:rgba(241,235,224,.75); filter:blur(.6px); }}
.sweep {{ position:absolute; top:-20%; left:-40%; width:30%; height:140%; transform:rotate(12deg);
  background:linear-gradient(90deg, rgba(255,240,210,0) 0%, rgba(255,240,210,.10) 50%, rgba(255,240,210,0) 100%); }}
.cap {{ position:absolute; left:120px; bottom:110px; max-width:1300px; font-style:italic; font-size:46px; line-height:1.25;
  padding-left:24px; border-left:4px solid {TERRA}; text-shadow:0 2px 18px rgba(0,0,0,.9); }}
.credit {{ position:absolute; right:100px; bottom:56px; font:20px/1 Arial,sans-serif; letter-spacing:.06em; color:{INK}; background:rgba(12,10,9,.78); padding:8px 14px; border-radius:4px; }}
.tw {{ position:absolute; inset:0; display:flex; flex-direction:column; align-items:center; justify-content:center; text-align:center; }}
.tmain {{ font-size:124px; font-weight:600; letter-spacing:.04em; }}
.trule {{ width:420px; height:3px; background:{TERRA}; margin:26px 0 22px; transform-origin:50% 50%; }}
.tsub {{ font:600 30px/1 Arial,sans-serif; letter-spacing:.32em; color:{GOLD}; }}
.hl {{ position:absolute; background:rgba(232,180,60,.55); border-bottom:3px solid #B07D1E; mix-blend-mode:multiply; transform-origin:0 50%; }}
.mapbg {{ position:absolute; inset:-15%; background:radial-gradient(ellipse at 40% 40%, #2b3a4a 0%, #15202b 70%); }}
.mapgrid {{ position:absolute; inset:-15%; background-image:linear-gradient(rgba(241,235,224,.06) 1px, transparent 1px), linear-gradient(90deg, rgba(241,235,224,.06) 1px, transparent 1px); background-size:120px 120px; }}
.mlab {{ font:600 26px Arial,sans-serif; fill:{INK}; paint-order:stroke; stroke:#121519; stroke-width:5px; letter-spacing:.08em; }}
.num {{ font-size:220px; font-weight:700; color:{PAPER}; font-variant-numeric:tabular-nums; }}
.nlab {{ font:600 34px/1.3 Arial,sans-serif; letter-spacing:.18em; color:{GOLD}; text-transform:uppercase; margin-top:12px; }}
.q {{ max-width:1400px; font-style:italic; font-size:64px; line-height:1.3; }}
.q .w {{ opacity:0; display:inline-block; margin-right:.25em; }}
.qby {{ font:600 28px Arial,sans-serif; letter-spacing:.2em; color:{TERRA}; margin-top:34px; }}
"""


class Scene:
    def __init__(self, idx, spec, start):
        self.i, self.s, self.T = idx, spec, start
        self.D = float(spec["dur"])
        self.id = f"s{idx}"
        self.html, self.js, self.events = [], [], [start]   # events: các mốc thay đổi đọc được (tính từ đầu video)

    def ev(self, t):
        self.events.append(round(t, 3))

    def a(self, line):
        self.js.append(line)


def ambient(sc, rnd, n_dust=26):
    """Lớp không khí: bụi trôi + hạt film + vệt sáng. Phủ TOÀN BỘ thời lượng cảnh."""
    T, D, sid = sc.T, sc.D, sc.id
    dots = []
    for k in range(n_dust):
        x, y, r = rnd.uniform(0, W), rnd.uniform(0, H), rnd.uniform(1.2, 3.4)
        dots.append(f'<i id="{sid}d{k}" style="left:{x:.0f}px;top:{y:.0f}px;width:{r:.1f}px;height:{r:.1f}px;opacity:{rnd.uniform(.15, .6):.2f}"></i>')
        dx, dy = rnd.uniform(-60, 60), rnd.uniform(-140, -40)
        sc.a(f'tl.fromTo("#{sid}d{k}",{{x:0,y:0}},{{x:{dx:.0f},y:{dy:.0f},duration:{D:.3f},ease:"none"}},{T:.3f});')
    sc.html.append(f'<div class="dust">{"".join(dots)}</div><div class="grain" id="{sid}g"></div><div class="sweep" id="{sid}w"></div>')
    steps = max(int(D * 12), 1)
    sc.a(f'tl.fromTo("#{sid}g",{{x:0,y:0}},{{x:{rnd.randint(80, 160)},y:{rnd.randint(60, 140)},duration:{D:.3f},ease:"steps({steps})"}},{T:.3f});')
    sc.a(f'tl.fromTo("#{sid}w",{{xPercent:0}},{{xPercent:{520},duration:{D:.3f},ease:"sine.inOut"}},{T:.3f});')


def camera(sc, sel, rnd, kind=None, t0=None, d=None, s0=1.0, s1=None):
    """Máy quay liên tục: push/pull/pan trái/pan phải. Không có đoạn đứng yên."""
    t0 = sc.T if t0 is None else t0
    d = sc.D if d is None else d
    kind = kind or rnd.choice(["push", "pull", "panl", "panr"])
    s1 = s1 or {"push": 1.12, "pull": 1.0, "panl": 1.10, "panr": 1.10}[kind]
    s_from = {"pull": 1.14}.get(kind, s0)
    x0, x1 = {"panl": (40, -40), "panr": (-40, 40)}.get(kind, (0, 0))
    y0, y1 = rnd.uniform(-12, 12), rnd.uniform(-12, 12)
    sc.a(f'tl.fromTo("{sel}",{{scale:{s_from},x:{x0},y:{y0:.0f}}},{{scale:{s1},x:{x1},y:{y1:.0f},duration:{d:.3f},ease:"sine.inOut"}},{t0:.3f});')


def text_in(sc, sel, at, dy=26, d=0.9):
    sc.a(f'tl.fromTo("{sel}",{{opacity:0,y:{dy}}},{{opacity:1,y:0,duration:{d},ease:"power3.out"}},{at:.3f});')
    sc.ev(at)


def caption(sc, at):
    s = sc.s
    if s.get("caption"):
        sc.html.append(f'<div class="cap" id="{sc.id}c">{esc(s["caption"])}</div>')
        text_in(sc, f"#{sc.id}c", at)
    if s.get("credit"):
        sc.html.append(f'<div class="credit">{esc(s["credit"])}</div>')


def r_title(sc, rnd):
    s, sid, T = sc.s, sc.id, sc.T
    sc.html.append(f'<div class="cam" id="{sid}k"><div class="desk"></div></div>'
                   f'<div class="tw"><div class="tmain" id="{sid}t">{esc(s["text"])}</div><div class="trule" id="{sid}r"></div>'
                   f'<div class="tsub" id="{sid}u">{esc(s.get("sub", ""))}</div></div>')
    camera(sc, f"#{sid}k", rnd, "push")
    text_in(sc, f"#{sid}t", T + 0.4, 30, 1.2)
    sc.a(f'tl.fromTo("#{sid}r",{{scaleX:0}},{{scaleX:1,duration:1.2,ease:"power2.inOut"}},{T + .7:.3f});')
    text_in(sc, f"#{sid}u", T + 1.3, 16)
    sc.a(f'tl.fromTo("#{sid}t",{{scale:1}},{{scale:1.05,duration:{sc.D:.3f},ease:"none"}},{T:.3f});')


def shots_for(sc):
    n = max(1, round(sc.D / SHOT))
    return [(sc.T + k * sc.D / n, sc.D / n) for k in range(n)]


def r_photo(sc, rnd, framed=True):
    """Ảnh: khung đầu toàn ảnh, các khung sau là CẬN CHI TIẾT của chính ảnh (crop + pan), hòa hình giữa các khung."""
    s, sid = sc.s, sc.id
    src = esc(s["src"])
    shots = shots_for(sc)
    focus = s.get("details") or []          # [[x%,y%,zoom], ...] chỗ cần cận; không có thì tự chọn
    for k, (t, d) in enumerate(shots):
        if k == 0:
            marks = "".join(f'<div class="hl" id="{sid}h{j}" style="left:{x}%;top:{y}%;width:{w}%;height:{h}%"></div>'
                            for j, (x, y, w, h, _at) in enumerate(s.get("highlights", [])))   # vệt tô nằm TRONG khung ảnh: đi theo máy quay
            inner = (f'<div class="print"><div class="pw"><img src="{src}" alt="">{marks}</div></div>' if framed
                     else f'<div class="full"><img src="{src}" alt=""></div>')
            sc.html.append(f'<div class="cam" id="{sid}k{k}"><div class="desk"></div>{inner}</div>')
            camera(sc, f"#{sid}k{k}", rnd, "push", t, d + XF)
        else:
            fx, fy, z = focus[k - 1] if k - 1 < len(focus) else (rnd.uniform(30, 70), rnd.uniform(30, 70), rnd.uniform(1.9, 2.6))
            sc.html.append(f'<div class="cam" id="{sid}k{k}" style="opacity:0;transform-origin:{fx:.0f}% {fy:.0f}%;'
                           f'background:{BG} url({src}) center/contain no-repeat"></div>')  # nền CSS: tránh 2 thẻ img trùng nguồn
            sc.a(f'tl.fromTo("#{sid}k{k}",{{opacity:0}},{{opacity:1,duration:{XF},ease:"sine.inOut"}},{t:.3f});')
            kind = rnd.choice(["panl", "panr", "push"])
            camera(sc, f"#{sid}k{k}", rnd, kind, t, d + XF, s0=z, s1=z * 1.08)
            sc.ev(t)
    sc.html.append('<div class="vig"></div>')
    caption(sc, sc.T + 0.8)


def r_document(sc, rnd):
    """Tài liệu: lia chậm + vệt tô vàng chạy qua từng dòng quan trọng theo lời đọc."""
    r_photo(sc, rnd, framed=True)   # highlights = [[x%, y%, w%, h%, giây], ...] tính theo ảnh tài liệu
    first_shot = shots_for(sc)[0][1]
    for j, (x, y, w, h, at) in enumerate(sc.s.get("highlights", [])):
        hid = f"{sc.id}h{j}"
        if at > first_shot - 1:
            raise SystemExit(f"{sc.id}: vệt tô {j} ở giây {at} rơi vào khung cận chi tiết (khung toàn tài liệu chỉ dài {first_shot:.1f} s)")
        sc.a(f'tl.fromTo("#{hid}",{{scaleX:0,opacity:1}},{{scaleX:1,duration:1.1,ease:"power2.inOut"}},{sc.T + at:.3f});')
        sc.ev(sc.T + at)


def r_map(sc, rnd):
    """Bản đồ: nền lưới, đường đi tự vẽ, chấm di chuyển theo đường, máy quay bám theo, nhãn hiện theo lời."""
    s, sid, T, D = sc.s, sc.id, sc.T, sc.D
    pts = s["route"]                         # [[x,y],...] trên khung 1920x1080
    path = "M" + " L".join(f"{x},{y}" for x, y in pts)
    L = sum(((pts[i + 1][0] - pts[i][0]) ** 2 + (pts[i + 1][1] - pts[i][1]) ** 2) ** .5 for i in range(len(pts) - 1))
    labels = "".join(f'<g id="{sid}p{j}" opacity="0"><circle cx="{x}" cy="{y}" r="9" fill="{TERRA}"/>'
                     f'<text class="mlab" x="{x + 16}" y="{y - 14}">{esc(n)}</text></g>' for j, (x, y, n) in enumerate(s.get("places", [])))
    sc.html.append(f'<div class="cam" id="{sid}k"><div class="mapbg"></div><div class="mapgrid"></div><div class="vig"></div>'
                   f'<svg viewBox="0 0 {W} {H}" width="{W}" height="{H}" style="position:absolute;inset:0">'
                   f'<path id="{sid}r" d="{path}" fill="none" stroke="{GOLD}" stroke-width="5" stroke-dasharray="{L:.0f}" stroke-dashoffset="{L:.0f}" stroke-linecap="round"/>'
                   f'{labels}<circle id="{sid}m" r="12" fill="{INK}" cx="{pts[0][0]}" cy="{pts[0][1]}"/></svg></div>')  # vig nằm DƯỚI nhãn
    camera(sc, f"#{sid}k", rnd, "push", s0=1.0, s1=1.18)
    draw_t, draw_d = T + 0.8, max(D - 2.0, 2.0)
    sc.a(f'tl.to("#{sid}r",{{attr:{{"stroke-dashoffset":0}},duration:{draw_d:.3f},ease:"none"}},{draw_t:.3f});')
    seg = draw_d / max(len(pts) - 1, 1)
    kf = ",".join(f'{{attr:{{cx:{x},cy:{y}}},duration:{seg:.3f},ease:"none"}}' for x, y in pts[1:])
    sc.a(f'tl.to("#{sid}m",{{keyframes:[{kf}]}},{draw_t:.3f});')  # 1 tween nhiều khung: không chồng tween
    places = s.get("places", [])
    for j in range(len(places)):
        at = draw_t + j * draw_d / max(len(places), 1)
        sc.a(f'tl.fromTo("#{sid}p{j}",{{opacity:0}},{{opacity:1,duration:.6}},{at:.3f});')
        sc.ev(at)
    k = 0.0
    while k < D:                                   # đường vẽ liên tục = thay đổi liên tục
        sc.ev(T + k)
        k += 4.0
    caption(sc, T + 0.8)


def r_stat(sc, rnd):
    s, sid, T = sc.s, sc.id, sc.T
    sc.html.append(f'<div class="cam" id="{sid}k"><div class="desk"></div></div><div class="tw">'
                   f'<div class="num" id="{sid}n">0</div><div class="nlab" id="{sid}l">{esc(s["label"])}</div></div>')
    camera(sc, f"#{sid}k", rnd, "pull")
    val, dec = float(s["value"]), int(s.get("decimals", 0))
    sc.a(f'(function(){{var o={{v:0}};tl.to(o,{{v:{val},duration:{min(2.6, sc.D * .5):.2f},ease:"power2.out",'
         f'onUpdate:function(){{document.querySelector("#{sid}n").textContent=o.v.toLocaleString("en-US",{{maximumFractionDigits:{dec},minimumFractionDigits:{dec}}})}}}},{T + .4:.3f});}})();')
    sc.ev(T + .4)
    text_in(sc, f"#{sid}l", T + 1.0)
    sc.a(f'tl.fromTo("#{sid}n",{{scale:1}},{{scale:1.06,duration:{sc.D:.3f},ease:"none"}},{T:.3f});')


def r_quote(sc, rnd):
    s, sid, T, D = sc.s, sc.id, sc.T, sc.D
    words = s["text"].split()
    ws = "".join(f'<span class="w">{esc(w)}</span>' for w in words)
    sc.html.append(f'<div class="cam" id="{sid}k"><div class="desk"></div></div><div class="tw"><div class="q" id="{sid}q">{ws}</div>'
                   f'<div class="qby" id="{sid}b">{esc(s.get("by", ""))}</div></div>')
    camera(sc, f"#{sid}k", rnd, "panr")
    span = min(D * .6, len(words) * .32)
    sc.a(f'tl.to("#{sid}q .w",{{opacity:1,duration:.35,stagger:{span / max(len(words), 1):.3f},ease:"none"}},{T + .5:.3f});')
    k = 0.0
    while k < span:
        sc.ev(T + .5 + k)
        k += 2.0
    text_in(sc, f"#{sid}b", T + .6 + span)
    sc.a(f'tl.fromTo("#{sid}q",{{y:10}},{{y:-10,duration:{D:.3f},ease:"none"}},{T:.3f});')


RENDER = {"title": r_title, "photo": r_photo, "document": r_document, "map": r_map, "stat": r_stat, "quote": r_quote}


def plan_scenes(plan):
    rnd = random.Random(plan.get("seed", 7))
    out, t = [], 0.0
    for i, s in enumerate(plan["scenes"]):
        sc = Scene(i, s, t)
        RENDER[s["type"]](sc, rnd)
        ambient(sc, rnd)
        out.append(sc)
        t += sc.D - XF
    return out, t + XF


def validate(plan):
    errs = []
    for i, s in enumerate(plan.get("scenes", [])):
        if s.get("type") not in TYPES:
            errs.append(f"cảnh {i}: loại '{s.get('type')}' không có (có: {', '.join(sorted(TYPES))})")
        if float(s.get("dur", 0)) < 3:
            errs.append(f"cảnh {i}: dài < 3 giây")
        if s.get("type") in ("photo", "document") and not s.get("credit"):
            errs.append(f"cảnh {i}: ảnh thiếu ghi công (credit), xem policy-guardrails.md")
    if errs:
        return errs, None
    scenes, total = plan_scenes(plan)
    evs = sorted(e for sc in scenes for e in sc.events) + [total]
    gaps = [(b - a, a) for a, b in zip(evs, evs[1:])]
    worst = max(gaps)
    if worst[0] > MAX_GAP + 1e-6:
        errs.append(f"có đoạn {worst[0]:.1f} giây không có thay đổi đọc được (bắt đầu {worst[1]:.1f} s), tối đa {MAX_GAP} s")
    return errs, {"total": round(total, 2), "scenes": len(scenes), "changes": len(evs) - 1,
                  "sec_per_change": round(total / max(len(evs) - 1, 1), 1), "max_gap": round(worst[0], 1)}


def build(plan, out):
    scenes, total = plan_scenes(plan)
    out = Path(out)
    (out / "compositions").mkdir(parents=True, exist_ok=True)
    (out / "assets").mkdir(exist_ok=True)
    shutil.copy(HERE / "vendor" / "gsap-3.14.2.min.js", out / "assets" / "gsap.min.js")
    base = Path(plan.get("assets_dir", "."))
    for s in plan["scenes"]:
        if "src" in s:
            src = (base / s["src"]) if not Path(s["src"]).is_absolute() else Path(s["src"])
            dst = out / "assets" / src.name
            if not dst.exists():
                shutil.copy(src, dst)
            s["src"] = f"assets/{src.name}"
    scenes, total = plan_scenes(plan)                  # dựng lại với đường dẫn ảnh mới
    clips = "\n".join(f'<div id="{sc.id}" class="clip sc" data-start="{sc.T:.3f}" data-duration="{sc.D:.3f}" style="z-index:{sc.i + 1}">'
                      + "".join(sc.html) + "</div>" for sc in scenes)
    fades = "\n".join(f'tl.fromTo("#{sc.id}",{{opacity:0}},{{opacity:1,duration:{XF},ease:"sine.inOut"}},{sc.T:.3f});' for sc in scenes[1:])
    js = "\n".join(line for sc in scenes for line in sc.js)
    (out / "compositions" / "body.html").write_text(
        f'<template>\n<style>{CSS}</style>\n<div id="root" data-composition-id="body" data-width="{W}" data-height="{H}" data-duration="{total:.3f}">\n'
        f'{clips}\n</div>\n<script>\nconst tl = gsap.timeline({{ paused: true }});\n{js}\n{fades}\nwindow.__timelines["body"] = tl;\n</script>\n</template>\n',
        encoding="utf-8")
    audio = ""
    if plan.get("audio"):
        a = Path(plan["audio"])
        shutil.copy(a, out / "assets" / a.name)
        audio = f'<audio id="vo" class="clip" src="assets/{a.name}" data-start="0" data-duration="{total:.3f}" data-track-index="0" data-volume="1"></audio>'
    (out / "index.html").write_text(
        f'<!doctype html>\n<html lang="en" data-resolution="landscape">\n<head>\n<meta charset="UTF-8" />\n'
        f'<meta name="viewport" content="width={W}, height={H}" />\n<script src="assets/gsap.min.js"></script>\n'
        f'<style>* {{ margin:0; padding:0; box-sizing:border-box; }} html, body {{ width:{W}px; height:{H}px; overflow:hidden; background:{BG}; }}'
        f' #root {{ position:relative; width:100%; height:100%; background:{BG}; }}</style>\n</head>\n<body>\n'
        f'<div id="root" data-composition-id="main" data-start="0" data-duration="{total:.3f}" data-width="{W}" data-height="{H}">\n'
        f'<div id="body" data-composition-id="body" data-composition-src="compositions/body.html" data-start="0" data-duration="{total:.3f}" '
        f'data-track-index="1" data-track-kind="graphics" data-width="{W}" data-height="{H}"></div>\n{audio}\n</div>\n'
        f'<script>\nwindow.__timelines = window.__timelines || {{}};\nwindow.__timelines["main"] = gsap.timeline({{ paused: true }});\n</script>\n</body>\n</html>\n',
        encoding="utf-8")
    return total


def main():
    for s in (sys.stdout, sys.stderr):
        try:
            s.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass
    if len(sys.argv) < 3 or sys.argv[1] not in ("validate", "build"):
        sys.exit(__doc__)
    plan = json.loads(Path(sys.argv[2]).read_text(encoding="utf-8"))
    errs, rep = validate(plan)
    if errs:
        print("KẾ HOẠCH CHUYỂN ĐỘNG HỎNG:")
        for e in errs:
            print("  -", e)
        sys.exit(2)
    print(f"Kế hoạch đạt: {rep['scenes']} cảnh, {rep['total']} giây, {rep['changes']} thay đổi, "
          f"trung bình {rep['sec_per_change']} giây/thay đổi, khoảng trống lớn nhất {rep['max_gap']} giây (tối đa {MAX_GAP})")
    if sys.argv[1] == "build":
        if len(sys.argv) < 4:
            sys.exit("Thiếu thư mục ra")
        total = build(plan, sys.argv[3])
        print(f"Đã dựng {sys.argv[3]} ({total:.1f} giây). Tiếp: npx hyperframes lint, check, render; rồi motion_metrics.py")


if __name__ == "__main__":
    main()
