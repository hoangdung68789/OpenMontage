"""Dựng dự án HyperFrames cho 002 Lady Be Good từ lời đọc thật + beats.py.

python channel-studio/videos/002-lady-be-good/render/tools/build.py   (chạy từ gốc OpenMontage)
- Đọc độ dài thật từng file lời đọc (projects/lady-be-good/assets/audio/narration_clone/<id>.wav).
- Mốc hình trong beats.py ghi theo giờ ước tính của kịch bản; quy đổi theo tỉ lệ sang độ dài thật.
- Ghi render/index.html, render/compositions/chN.html, render/assets/{img,audio}, render/timeline.json.
- Trộn tiếng (giọng + nhạc nền) bằng ffmpeg thành một file assets/audio/mix.mp3, -14 LUFS.
"""
import html
import json
import math
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from beats import BEATS, CHAPTERS, CREW, MUSIC, PHOTOS  # noqa: E402
from geo import PLACES, REGIONS, proj  # noqa: E402

ROOT = HERE.parents[4]  # OpenMontage
RENDER = HERE.parent
PROJ = ROOT / "projects" / "lady-be-good"
VO = PROJ / "assets" / "audio" / "narration_clone"
W, H = 1920, 1080
XF = 0.8          # thời gian hòa hình giữa hai cảnh
GAP = 0.7         # lặng giữa hai đoạn lời
CARD = 4.0        # thẻ chương
LEAD = 0.6        # mở đầu trước lời đầu tiên
BG, INK, PAPER = "#1B1714", "#F1EBE0", "#E8DFCC"
TERRA, LAPIS, GOLD, ORANGE, RED = "#B5734A", "#1F4E8C", "#C9A54C", "#E8893A", "#C8423A"
esc = html.escape


def dur(p):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)],
                                capture_output=True, text=True, check=True).stdout)


def mmss(s):
    m, x = s.split(":")
    return int(m) * 60 + float(x)


# ---------- bố cục thời gian ----------
script = {s["id"]: s for s in json.loads((PROJ / "artifacts" / "script.json").read_text(encoding="utf-8"))["sections"]}
plan, t = [], LEAD
for ci, (num, title, sids) in enumerate(CHAPTERS):
    ch = {"num": num, "title": title, "start": t, "card": None, "sections": []}
    if num > 0:
        ch["card"] = (t, CARD)
        t += CARD
    for sid in sids:
        d = dur(VO / f"{sid}.wav")
        ch["sections"].append({"id": sid, "start": t, "dur": d})
        t += d + GAP
    ch["end"] = t
    plan.append(ch)
TOTAL = round(t + 2.5, 2)  # giữ khung cuối 2,5 s
plan[-1]["end"] = TOTAL - XF  # chương cuối kéo tới hết video, không rơi về nền trống


def beat_times(sec):
    """[(abs_start, spec)] theo tỉ lệ giờ ước tính trong kịch bản."""
    s0, s1 = script[sec["id"]]["start_seconds"], script[sec["id"]]["end_seconds"]
    out = []
    for est, spec in BEATS[sec["id"]]:
        f = min(max((mmss(est) - s0) / (s1 - s0), 0), 0.97)
        out.append([sec["start"] + f * sec["dur"], spec])
    out[0][0] = sec["start"] - 0.35  # cảnh đầu đoạn vào trong khoảng lặng trước lời
    return out


# ---------- vẽ từng loại cảnh ----------
class Scene:
    def __init__(self, cid):
        self.cid, self.n, self.html, self.js, self.css = cid, 0, [], [], set()

    def nid(self):
        self.n += 1
        return f"{self.cid}b{self.n}"


def fade_in(sc, bid, T):
    sc.js.append(f'tl.fromTo("#{bid}f",{{opacity:0}},{{opacity:1,duration:{XF},ease:"sine.inOut"}},{T:.3f});')


def text_in(sel, at, dy=24, d=0.9):
    return f'tl.fromTo("{sel}",{{opacity:0,y:{dy}}},{{opacity:1,y:0,duration:{d},ease:"power3.out"}},{at:.3f});'


def img_wh(name):
    out = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v", "-show_entries", "stream=width,height",
                          "-of", "csv=p=0", str(PROJ / "assets" / "images" / "commons" / name)], capture_output=True, text=True).stdout
    w, h = out.strip().split(",")[:2]
    return int(w), int(h)


def r_photo(sc, bid, T, D, p):
    ph = PHOTOS[p["img"]]
    big = ph["w"] >= 1200 and not p.get("print")
    push = p.get("push", "in")
    s0, s1 = (1.0, 1.07) if push == "in" else (1.07, 1.0)
    x1 = {"left": -40, "right": 40}.get(push, 0)
    if big:
        inner = f'<div class="ph-full" id="{bid}p"><img src="assets/img/{ph["file"]}" alt=""></div><div class="vig"></div>'
        sc.js.append(f'tl.fromTo("#{bid}p",{{scale:{s0},x:0}},{{scale:{s1},x:{x1},duration:{D:.3f},ease:"none"}},{T:.3f});')
    else:
        rot = p.get("rot", -1.2)
        w, h = img_wh(ph["file"])
        k = min(1000 / w, 640 / h, 2.2)  # ảnh nhỏ phóng tới khung 1000x640, tối đa 2,2 lần để khỏi vỡ
        inner = (f'<div class="desk"></div><div class="ph-print" id="{bid}p"><img src="assets/img/{ph["file"]}" alt="" style="width:{w * k:.0f}px;height:{h * k:.0f}px"></div>')
        sc.js.append(f'tl.fromTo("#{bid}p",{{scale:0.96,rotation:{rot},y:16}},{{scale:1.03,rotation:{rot * 0.4:.2f},y:0,duration:{D:.3f},ease:"none"}},{T:.3f});')
    cap = f'<div class="cap" id="{bid}c">{esc(p["cap"])}</div>' if p.get("cap") else ""
    if cap:
        sc.js.append(text_in(f"#{bid}c", T + 1.0))
    credit = f'<div class="credit">{esc(ph["credit"])}</div>'
    return inner + cap + credit


def r_title(sc, bid, T, D, p):
    style = p.get("style", "big")
    sub = f'<div class="t-sub" id="{bid}s">{esc(p["sub"])}</div>' if p.get("sub") else ""
    bg = '<div class="sand"></div>' if p.get("sand") else ""
    sc.js.append(text_in(f"#{bid}t", T + 0.5, 30, 1.2))
    sc.js.append(f'tl.fromTo("#{bid}r",{{scaleX:0}},{{scaleX:1,duration:1.2,ease:"power2.inOut"}},{T + 0.7:.3f});')
    if sub:
        sc.js.append(text_in(f"#{bid}s", T + 1.3, 16))
    if p.get("fade_out"):
        sc.js.append(f'tl.to("#{bid}t",{{opacity:0,duration:1.2,ease:"sine.in"}},{T + D - 1.8:.3f});')
    return (f'{bg}<div class="t-wrap t-{style}"><div class="t-main" id="{bid}t">{esc(p["text"])}</div>'
            f'<div class="t-rule" id="{bid}r"></div>{sub}</div>')


def r_quote(sc, bid, T, D, p):
    words = p["text"].split()
    spans = " ".join(f'<span class="w" id="{bid}w{i}">{esc(w)}</span>' for i, w in enumerate(words))
    span = min(D * 0.45, 0.28 * len(words))
    sc.js.append(f'tl.fromTo("#{bid}k",{{y:30,rotation:-1.5,opacity:0}},{{y:0,rotation:-0.6,opacity:1,duration:1.0,ease:"power2.out"}},{T + 0.2:.3f});')
    sc.js.append(f'tl.fromTo("#{bid}k .w",{{opacity:0}},{{opacity:1,duration:0.35,stagger:{span / max(len(words), 1):.3f},ease:"none"}},{T + 1.0:.3f});')
    sc.js.append(text_in(f"#{bid}s", T + 1.2 + span, 12))
    date = f'<div class="q-date">{esc(p["date"])}</div>' if p.get("date") else ""
    label = f'<div class="q-label">{esc(p.get("label", "Diary of 2Lt. Robert Toner"))}</div>'
    return (f'<div class="desk"></div><div class="nb" id="{bid}k">{label}{date}<div class="q-text">{spans}</div></div>'
            f'<div class="q-src" id="{bid}s">{esc(p["src"])}</div>')


def crew_card(c, cid, cls=""):
    return (f'<div class="cc {cls}" id="{cid}"><div class="cc-rank">{esc(c[0])}</div><div class="cc-name">{esc(c[1])}</div>'
            f'<div class="cc-role">{esc(c[2])}</div></div>')


def r_cards(sc, bid, T, D, p):
    names = p.get("show") or [c[1] for c in CREW]
    by = {c[1]: c for c in CREW}
    groups = p.get("groups") or [names]
    out = '<div class="cc-grid compact">' if p.get("compact") else '<div class="cc-grid">'
    k = 0
    order = []
    for gi, g in enumerate(groups):
        lab = f'<div class="cc-glabel">{esc(p["glabels"][gi])}</div>' if p.get("glabels") else ""
        out += f'<div class="cc-group">{lab}<div class="cc-row">'
        for nm in g:
            cls = ("hi" if nm in p.get("hi", []) else "")
            out += crew_card(by[nm], f"{bid}c{k}", cls)
            order.append(f"#{bid}c{k}")
            k += 1
        out += "</div></div>"
    out += "</div>"
    span = min(D * 0.55, 0.9 * len(order)) if p.get("slow") else min(D * 0.3, 0.25 * len(order))
    sc.js.append(f'tl.fromTo([{",".join(json.dumps(o) for o in order)}],{{opacity:0,y:30}},{{opacity:1,y:0,duration:0.7,stagger:{span / max(len(order), 1):.3f},ease:"power3.out"}},{T + 0.5:.3f});')
    for o, nm in zip(order, sum(groups, [])):
        if nm in p.get("dim", []):
            sc.js.append(f'tl.to("{o}",{{opacity:0.28,duration:1.0}},{T + 1.2 + span:.3f});')
    title = f'<div class="cc-title" id="{bid}h">{esc(p["title"])}</div>' if p.get("title") else ""
    if title:
        sc.js.append(text_in(f"#{bid}h", T + 0.3, 12))
    return title + out


def r_chips(sc, bid, T, D, p):
    out = f'<div class="chip-title" id="{bid}h">{esc(p.get("title", ""))}</div><div class="chips">'
    for i, (val, src) in enumerate(p["items"]):
        name, _, num = val.rpartition(" · ")  # "Shelley · 21 mi" -> tên dòng nhỏ, số dòng to
        nm = f'<div class="chip-n">{esc(name)}</div>' if name else ""
        out += f'<div class="chip" id="{bid}c{i}">{nm}<div class="chip-v"{' style="font-size:60px"' if len(num) > 12 else ''}>{esc(num)}</div><div class="chip-s">{esc(src)}</div></div>'
    out += "</div>"
    if p.get("note"):
        out += f'<div class="chip-note" id="{bid}n">{esc(p["note"])}</div>'
        sc.js.append(text_in(f"#{bid}n", T + 0.6 + 0.8 * len(p["items"]), 10))
    sc.js.append(text_in(f"#{bid}h", T + 0.3, 12))
    sc.js.append(f'tl.fromTo("#{bid} .chip",{{opacity:0,y:40}},{{opacity:1,y:0,duration:0.8,stagger:0.8,ease:"power3.out"}},{T + 0.6:.3f});')
    return out


def r_chain(sc, bid, T, D, p):
    out = '<div class="chain">'
    for i, s in enumerate(p["items"]):
        out += (f'<div class="link" id="{bid}l{i}">{esc(s)}</div>' + (f'<div class="arrow" id="{bid}a{i}">→</div>' if i < len(p["items"]) - 1 else ""))
    out += "</div>"
    step = (D * 0.7) / len(p["items"])
    for i in range(len(p["items"])):
        sc.js.append(f'tl.fromTo("#{bid}l{i}",{{opacity:0.15,borderColor:"#4a3b30"}},{{opacity:1,borderColor:"{ORANGE}",duration:0.6}},{T + 0.5 + i * step:.3f});')
        if i < len(p["items"]) - 1:
            sc.js.append(f'tl.fromTo("#{bid}a{i}",{{opacity:0}},{{opacity:1,duration:0.4}},{T + 0.5 + i * step + step * 0.6:.3f});')
    if p.get("fade_end"):
        sc.js.append(f'tl.to("#{bid} .chain",{{opacity:0.12,duration:1.5}},{T + D - 2.2:.3f});')
    title = f'<div class="chip-title" id="{bid}h">{esc(p["title"])}</div>' if p.get("title") else ""
    if title:
        sc.js.append(text_in(f"#{bid}h", T + 0.2, 12))
    return title + out


def r_compare(sc, bid, T, D, p):
    out = '<div class="cmp">'
    for i, (head, body) in enumerate(p["items"]):
        out += f'<div class="sheet" id="{bid}s{i}"><div class="sheet-h">{esc(head)}</div><div class="sheet-b">{esc(body)}</div></div>'
    out += "</div>"
    sc.js.append(f'tl.fromTo("#{bid} .sheet",{{opacity:0,y:40,rotation:(i)=>i?1.2:-1.2}},{{opacity:1,y:0,duration:0.9,stagger:1.2,ease:"power3.out"}},{T + 0.4:.3f});')
    if p.get("note"):
        out += f'<div class="chip-note" id="{bid}n">{esc(p["note"])}</div>'
        sc.js.append(text_in(f"#{bid}n", T + 2.8, 10))
    return out


# --- bản đồ ---
def pt(region, at):
    lon, lat = PLACES[at] if isinstance(at, str) else at
    return proj(region, lon, lat)


def cam_xy(region, cam):
    x, y = pt(region, (cam[0], cam[1]))
    s = cam[2]
    return W / 2 - x * s, H / 2 - y * s, s


def poly_len(ps):
    return sum(math.dist(a, b) for a, b in zip(ps, ps[1:]))


def r_map(sc, bid, T, D, p):
    reg = p.get("region", "med")
    mw, mh = REGIONS[reg]["size"]
    c0 = cam_xy(reg, p["cam"])
    c1 = cam_xy(reg, p.get("cam2", p["cam"]))
    s = c1[2]
    sc.js.append(f'tl.fromTo("#{bid}m",{{x:{c0[0]:.1f},y:{c0[1]:.1f},scale:{c0[2]}}},{{x:{c1[0]:.1f},y:{c1[1]:.1f},scale:{c1[2]},duration:{D:.3f},ease:"sine.inOut"}},{T:.3f});')
    svg, k = [], 0
    for it in p.get("items", []):
        k += 1
        eid = f"{bid}i{k}"
        at = T + it.get("t", 0.15) * D
        kind = it["k"]
        col = it.get("color", ORANGE)
        if kind in ("pin", "label"):
            x, y = pt(reg, it["at"])
            fs = it.get("fs", 30) / s
            if kind == "pin":
                svg.append(f'<g id="{eid}"><circle cx="{x:.1f}" cy="{y:.1f}" r="{18 / s:.1f}" fill="{col}" opacity="0.25"/>'
                           f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{8 / s:.1f}" fill="{col}"/>')
            else:
                svg.append(f'<g id="{eid}">')
            if it.get("text"):
                dx, dy = it.get("off", (16, -14))
                anchor = it.get("anchor", "start")
                svg.append(f'<text x="{x + dx / s:.1f}" y="{y + dy / s:.1f}" font-size="{fs:.1f}" fill="{it.get("tc", INK)}" text-anchor="{anchor}" '
                           f'class="{"mlab-big" if it.get("big") else "mlab"}" stroke="#121519" stroke-width="{5 / s:.1f}" paint-order="stroke">{esc(it["text"])}</text>')
            svg.append("</g>")
            sc.js.append(f'tl.fromTo("#{eid}",{{opacity:0}},{{opacity:1,duration:0.8}},{at:.3f});')
        elif kind == "route":
            ps = [pt(reg, a) for a in it["pts"]]
            d = "M" + "L".join(f"{x:.1f},{y:.1f}" for x, y in ps)
            L = poly_len(ps)
            wdt = it.get("w", 4) / s
            if it.get("dash"):
                svg.append(f'<path id="{eid}" d="{d}" fill="none" stroke="{col}" stroke-width="{wdt:.2f}" stroke-dasharray="{14 / s:.1f} {10 / s:.1f}" stroke-linecap="round"/>')
                sc.js.append(f'tl.fromTo("#{eid}",{{opacity:0}},{{opacity:0.9,duration:1.0}},{at:.3f});')
            else:
                svg.append(f'<path id="{eid}" d="{d}" fill="none" stroke="{col}" stroke-width="{wdt:.2f}" stroke-linecap="round" stroke-linejoin="round" '
                           f'stroke-dasharray="{L:.1f}" stroke-dashoffset="{L:.1f}"/>')
                sc.js.append(f'tl.fromTo("#{eid}",{{attr:{{"stroke-dashoffset":{L:.1f}}}}},{{attr:{{"stroke-dashoffset":0}},duration:{it.get("d", 2.5)},ease:"power1.inOut"}},{at:.3f});')
            if it.get("text"):
                (x1, y1), (x2, y2) = ps[len(ps) // 2 - 1 if len(ps) > 2 else 0], ps[len(ps) // 2]
                mx, my = (x1 + x2) / 2, (y1 + y2) / 2
                svg.append(f'<text id="{eid}t" x="{mx + 14 / s:.1f}" y="{my:.1f}" font-size="{it.get("fs", 28) / s:.1f}" fill="{INK}" class="mlab" '
                           f'stroke="#121519" stroke-width="{5 / s:.1f}" paint-order="stroke">{esc(it["text"])}</text>')
                sc.js.append(f'tl.fromTo("#{eid}t",{{opacity:0}},{{opacity:1,duration:0.8}},{at + it.get("d", 2.5) * 0.6:.3f});')
        elif kind == "dot":
            ps = [pt(reg, a) for a in it["pts"]]
            L = poly_len(ps) or 1
            dd = it.get("d", 3.0)
            svg.append(f'<g id="{eid}"><circle id="{eid}h" cx="{ps[0][0]:.1f}" cy="{ps[0][1]:.1f}" r="{22 / s:.1f}" fill="{ORANGE}" opacity="0.25"/>'
                       f'<circle id="{eid}c" cx="{ps[0][0]:.1f}" cy="{ps[0][1]:.1f}" r="{10 / s:.1f}" fill="{ORANGE}"/></g>')
            sc.js.append(f'tl.fromTo("#{eid}",{{opacity:0}},{{opacity:1,duration:0.5}},{at:.3f});')
            if len(ps) > 1:
                kf = ",".join(f'{{attr:{{cx:{b[0]:.1f},cy:{b[1]:.1f}}},duration:{dd * math.dist(a, b) / L:.3f}}}' for a, b in zip(ps, ps[1:]))
                for part in ("h", "c"):
                    sc.js.append(f'tl.to("#{eid}{part}",{{keyframes:[{kf}],ease:"none"}},{at + 0.3:.3f});')
        elif kind == "ring":
            x, y = pt(reg, it["at"])
            g = [f'<circle class="{eid}r" cx="{x:.1f}" cy="{y:.1f}" r="{10 / s:.1f}" fill="none" stroke="{it.get("color", GOLD)}" stroke-width="{3 / s:.1f}"/>' for _ in range(4)]
            svg.append(f'<g id="{eid}">' + "".join(g) + "</g>")
            sc.js.append(f'tl.fromTo(".{eid}r",{{attr:{{r:{10 / s:.1f}}},opacity:0.9}},{{attr:{{r:{it.get("r", 260) / s:.1f}}},opacity:0,duration:2.4,stagger:0.6,ease:"power1.out"}},{at:.3f});')
        elif kind == "area":
            x, y = pt(reg, it["at"])
            svg.append(f'<circle id="{eid}" cx="{x:.1f}" cy="{y:.1f}" r="{it["r"]:.1f}" fill="{col}" fill-opacity="0.18" stroke="{col}" stroke-width="{3 / s:.1f}" stroke-dasharray="{10 / s:.1f} {8 / s:.1f}"/>')
            sc.js.append(f'tl.fromTo("#{eid}",{{opacity:0,attr:{{r:{it["r"] * 0.6:.1f}}}}},{{opacity:1,attr:{{r:{it["r"]:.1f}}},duration:1.4,ease:"power2.out"}},{at:.3f});')
        elif kind == "steps":
            ps = [pt(reg, a) for a in it["pts"]]
            L = poly_len(ps)
            n = it.get("n", 18)
            dots = []
            for i in range(n):
                dist, acc = L * i / max(n - 1, 1), 0
                for a, b in zip(ps, ps[1:]):
                    seg = math.dist(a, b)
                    if acc + seg >= dist or b == ps[-1]:
                        f = (dist - acc) / seg if seg else 0
                        x, y = a[0] + (b[0] - a[0]) * f, a[1] + (b[1] - a[1]) * f
                        break
                    acc += seg
                off = (6 if i % 2 else -6) / s
                dots.append(f'<ellipse class="{eid}d" cx="{x + off:.1f}" cy="{y:.1f}" rx="{5 / s:.1f}" ry="{8 / s:.1f}" fill="{it.get("color", PAPER)}"/>')
            svg.append(f'<g id="{eid}">' + "".join(dots) + "</g>")
            sc.js.append(f'tl.fromTo(".{eid}d",{{opacity:0}},{{opacity:0.9,duration:0.3,stagger:{it.get("d", 4.0) / n:.3f}}},{at:.3f});')
            if it.get("erase"):
                sc.js.append(f'tl.to(".{eid}d",{{opacity:0,duration:0.6,stagger:{it.get("d", 4.0) / n:.3f}}},{T + D * it["erase"]:.3f});')
        elif kind == "sand":
            svg.append(f'<rect id="{eid}" x="0" y="0" width="{mw}" height="{mh}" fill="#c9a27a"/>')
            sc.js.append(f'tl.fromTo("#{eid}",{{opacity:0}},{{opacity:{it.get("o", 0.35)},duration:2.0}},{at:.3f});')
    notes = ""
    for i, (txt, when) in enumerate(p.get("notes", [])):
        notes += f'<div class="mapnote" id="{bid}n{i}">{esc(txt)}</div>'
        sc.js.append(f'tl.fromTo("#{bid}n{i}",{{opacity:0,y:12}},{{opacity:1,y:0,duration:0.8}},{T + when * D:.3f});')
        if i + 1 < len(p.get("notes", [])):
            sc.js.append(f'tl.to("#{bid}n{i}",{{opacity:0,duration:0.5}},{T + p["notes"][i + 1][1] * D - 0.6:.3f});')
    head = f'<div class="maphead" id="{bid}h">{esc(p["head"])}</div>' if p.get("head") else ""
    if head:
        sc.js.append(text_in(f"#{bid}h", T + 0.4, 12))
    credit = '<div class="credit">Map: Natural Earth (public domain) · positions approximate</div>'
    return (f'<div class="mapcam" id="{bid}m" style="width:{mw}px;height:{mh}px"><img src="assets/maps/{reg}.svg" width="{mw}" height="{mh}" alt="">'
            f'<svg viewBox="0 0 {mw} {mh}" width="{mw}" height="{mh}">{"".join(svg)}</svg></div><div class="mapvig"></div>{head}{notes}{credit}')


from illus import ILLUS  # noqa: E402

RENDER_FN = {"photo": r_photo, "title": r_title, "quote": r_quote, "cards": r_cards, "chips": r_chips, "chain": r_chain,
             "compare": r_compare, "map": r_map}


def render_beat(sc, T, D, p):
    bid = sc.nid()
    k = p["k"]
    if k == "illus":
        body = ILLUS[p["name"]](sc, bid + "x", T, D, p)  # tiền tố x: id hình minh họa không trùng id khung cảnh
        cap = f'<div class="cap" id="{bid}c">{esc(p["cap"])}</div>' if p.get("cap") else ""
        if cap:
            sc.js.append(text_in(f"#{bid}c", T + 1.0))
        body += cap + ('<div class="credit">Illustration</div>' if p.get("mark", True) else "")
    else:
        body = RENDER_FN[k](sc, bid, T, D, p)
    fade_in(sc, bid, T)
    sc.html.append(f'<div id="{bid}" class="clip beat" data-start="{T:.3f}" data-duration="{D:.3f}" style="z-index:{sc.n + 1}">'
                   f'<div class="bf" id="{bid}f">{body}</div></div>')


# ---------- ghi file ----------
CSS = (HERE / "style.css").read_text(encoding="utf-8")
(RENDER / "compositions").mkdir(exist_ok=True)
img_dir = RENDER / "assets" / "img"
img_dir.mkdir(parents=True, exist_ok=True)
for ph in PHOTOS.values():
    src = PROJ / "assets" / "images" / "commons" / ph["file"]
    dst = img_dir / ph["file"]
    if not dst.exists() or dst.stat().st_mtime < src.stat().st_mtime:
        shutil.copy2(src, dst)

hosts, timeline = [], []
for ch in plan:
    cid = f"ch{ch['num']}"
    sc = Scene(cid)
    c0 = ch["start"]
    items = []
    if ch["card"]:
        items.append([ch["card"][0], {"k": "title", "style": "chapter", "text": ch["title"], "sub": f"CHAPTER {ch['num']}"}])
    for sec in ch["sections"]:
        items += beat_times(sec)
    for i, (t0, spec) in enumerate(items):
        t1 = items[i + 1][0] if i + 1 < len(items) else ch["end"]
        T, D = t0 - c0, (t1 - t0) + XF
        render_beat(sc, T, D, spec)
        timeline.append({"t": round(t0, 2), "d": round(t1 - t0, 2), "k": spec["k"], "what": spec.get("text") or spec.get("img") or spec.get("name") or spec.get("head") or ""})
    cdur = ch["end"] - c0 + XF
    body = "\n".join(sc.html)
    js = "\n".join(sc.js)
    (RENDER / "compositions" / f"{cid}.html").write_text(
        f'<template>\n<style>\n{CSS}\n</style>\n<div id="root" data-composition-id="{cid}" data-width="{W}" data-height="{H}" data-duration="{cdur:.3f}">\n'
        f'{body}\n</div>\n<script>\nconst tl = gsap.timeline({{ paused: true }});\n{js}\nwindow.__timelines["{cid}"] = tl;\n</script>\n</template>\n',
        encoding="utf-8")
    hosts.append(f'<div id="{cid}" data-composition-id="{cid}" data-composition-src="compositions/{cid}.html" data-start="{c0:.3f}" '
                 f'data-duration="{cdur:.3f}" data-track-index="1" data-track-kind="graphics" data-width="{W}" data-height="{H}" style="z-index:{ch["num"] + 1}"></div>')

# ---------- trộn tiếng ----------
aud = RENDER / "assets" / "audio"
aud.mkdir(parents=True, exist_ok=True)
mix = aud / "mix.mp3"
inputs, filt, labels = [], [], []
for ch in plan:
    for sec in ch["sections"]:
        i = inputs.count("-i")
        inputs += ["-i", str(VO / f"{sec['id']}.wav")]
        ms = int(sec["start"] * 1000)
        filt.append(f"[{i}:a]aresample=48000,aformat=channel_layouts=stereo,adelay={ms}|{ms}[v{i}]")
        labels.append(f"[v{i}]")
filt.append(f"{''.join(labels)}amix=inputs={len(labels)}:normalize=0,apad=whole_dur={TOTAL},asplit=2[vo][vok]")
mlabels = []
for j, (track, a, b, gain) in enumerate(MUSIC):
    i = inputs.count("-i")
    inputs += ["-stream_loop", "-1", "-i", str(PROJ / "assets" / "music" / track)]  # bài ngắn hơn chương thì lặp
    st = plan[a]["start"] - (LEAD if a == 0 else 0)
    en = plan[b]["end"] + (2.5 if b == len(plan) - 1 else 0.8)
    ln = en - st
    ms = int(st * 1000)
    filt.append(f"[{i}:a]aresample=48000,aformat=channel_layouts=stereo,atrim=0:{ln:.2f},afade=t=in:d=2,afade=t=out:st={ln - 3:.2f}:d=3,volume={gain},adelay={ms}|{ms}[m{j}]")
    mlabels.append(f"[m{j}]")
filt.append(f"{''.join(mlabels)}amix=inputs={len(mlabels)}:normalize=0,apad=whole_dur={TOTAL}[bed]")
filt.append("[bed][vok]sidechaincompress=threshold=0.03:ratio=6:attack=20:release=600[duck]")
filt.append(f"[duck][vo]amix=inputs=2:normalize=0,atrim=0:{TOTAL},loudnorm=I=-14:TP=-1.5:LRA=11[out]")
cmd = ["ffmpeg", "-v", "error", "-y", *inputs, "-filter_complex", ";".join(filt), "-map", "[out]", "-ar", "48000", "-b:a", "192k", str(mix)]
if "--no-audio" not in sys.argv:
    subprocess.run(cmd, check=True)

idx = f"""<!doctype html>
<html lang="en" data-resolution="landscape">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=1920, height=1080" />
<script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
<style>
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
html, body {{ margin: 0; width: 1920px; height: 1080px; overflow: hidden; background: {BG}; }}
#root {{ position: relative; width: 100%; height: 100%; background: {BG}; }}
</style>
</head>
<body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{TOTAL}" data-width="{W}" data-height="{H}">
{chr(10).join(hosts)}
<audio id="mix" class="clip" src="assets/audio/mix.mp3" data-start="0" data-duration="{TOTAL}" data-track-index="0" data-volume="1"></audio>
</div>
<script>
window.__timelines = window.__timelines || {{}};
window.__timelines["main"] = gsap.timeline({{ paused: true }});
</script>
</body>
</html>
"""
(RENDER / "index.html").write_text(idx, encoding="utf-8")
(RENDER / "timeline.json").write_text(json.dumps({"total": TOTAL, "chapters": [{k: c[k] for k in ("num", "title", "start", "end")} for c in plan],
                                                  "sections": [{"id": s["id"], "start": round(s["start"], 2), "dur": round(s["dur"], 2)} for c in plan for s in c["sections"]],
                                                  "beats": timeline}, ensure_ascii=False, indent=1), encoding="utf-8")
print(json.dumps({"total_s": TOTAL, "total": f"{int(TOTAL // 60)}:{TOTAL % 60:05.2f}", "beats": len(timeline), "chapters": len(plan)}))
