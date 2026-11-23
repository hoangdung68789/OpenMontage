"""Hình minh họa SVG vẽ tay cho 002 (ghi "Illustration" ở góc), không giả ảnh thật. Mỗi hàm trả HTML và thêm tween vào sc.js."""
import math

INK, PAPER, TERRA, GOLD, ORANGE, RED, NIGHT = "#F1EBE0", "#E8DFCC", "#B5734A", "#C9A54C", "#E8893A", "#C8423A", "#0f1216"


def svg(body, bg=NIGHT):
    return f'<svg class="illus" viewBox="0 0 1920 1080" width="1920" height="1080"><rect width="1920" height="1080" fill="{bg}"/>{body}</svg>'


def stars(n=70, seed=3):
    out, x = [], seed
    for i in range(n):  # giả ngẫu nhiên cố định, không dùng Math.random
        x = (x * 1103515245 + 12345) % 2147483648
        cx, cy = x % 1920, (x // 1920) % 640
        out.append(f'<circle cx="{cx}" cy="{cy}" r="{1 + i % 3 * 0.6:.1f}" fill="{INK}" opacity="{0.25 + (i % 5) * 0.12:.2f}"/>')
    return "".join(out)


def parachute(i, x, y, s=1.0):
    return (f'<g id="{i}" transform="translate({x},{y}) scale({s})"><path d="M-60,0 Q0,-70 60,0 Q30,-10 0,-4 Q-30,-10 -60,0Z" fill="{PAPER}" opacity="0.9"/>'
            f'<path d="M-58,0 L0,80 M58,0 L0,80 M-20,-4 L0,80 M20,-4 L0,80" stroke="{PAPER}" stroke-width="1.5" opacity="0.7"/>'
            f'<rect x="-6" y="80" width="12" height="22" rx="4" fill="{TERRA}"/></g>')


def p_parachutes(sc, bid, T, D, p):
    n = p.get("n", 9)
    g = []
    for i in range(n):
        x, y0 = 260 + i * 175, 120 + (i * 137) % 260
        g.append(f'<g id="{bid}p{i}">{parachute(f"{bid}q{i}", x, y0, 0.8 + (i % 3) * 0.12)}</g>')
        sc.js.append(f'tl.fromTo("#{bid}p{i}",{{y:-260,opacity:0}},{{y:{420 + (i % 4) * 60},opacity:1,duration:{D:.3f},ease:"none"}},{T + i * 0.25:.3f});')
    return svg(stars() + "".join(g))


def p_sky(sc, bid, T, D, p):
    body = stars(110)
    if p.get("sunset"):
        body = (f'<defs><linearGradient id="{bid}g" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#151a24"/><stop offset="0.7" stop-color="#4a2c22"/>'
                f'<stop offset="1" stop-color="#b5734a"/></linearGradient></defs><rect width="1920" height="1080" fill="url(#{bid}g)"/>'
                f'<circle id="{bid}s" cx="960" cy="880" r="90" fill="{ORANGE}" opacity="0.9"/><rect y="900" width="1920" height="180" fill="#121519"/>')
        sc.js.append(f'tl.fromTo("#{bid}s",{{attr:{{cy:860}}}},{{attr:{{cy:990}},duration:{D:.3f},ease:"none"}},{T:.3f});')
    if p.get("lights"):
        for i, (x, y) in enumerate([(640, 300), (1180, 220), (1420, 420)]):
            body += f'<circle id="{bid}l{i}" cx="{x}" cy="{y}" r="16" fill="{ORANGE}"/><circle cx="{x}" cy="{y}" r="60" fill="{ORANGE}" opacity="0.15"/>'
            sc.js.append(f'tl.fromTo("#{bid}l{i}",{{opacity:0.2}},{{opacity:1,duration:0.9,yoyo:true,repeat:3,ease:"sine.inOut"}},{T + 0.4 + i * 0.5:.3f});')
    body += '<rect y="1000" width="1920" height="80" fill="#0b0d10"/>'
    return svg(body)


def p_clock(sc, bid, T, D, p):
    h, m = map(int, p.get("time", "00:12").split(":"))
    cx, cy, r = 960, 520, 300
    ticks = "".join(f'<line x1="{cx + (r - 30) * math.sin(math.radians(a)):.1f}" y1="{cy - (r - 30) * math.cos(math.radians(a)):.1f}" '
                    f'x2="{cx + (r - 8) * math.sin(math.radians(a)):.1f}" y2="{cy - (r - 8) * math.cos(math.radians(a)):.1f}" stroke="{INK}" stroke-width="{6 if a % 30 == 0 else 2}"/>'
                    for a in range(0, 360, 6))
    am, ah = m * 6, (h % 12) * 30 + m * 0.5
    body = (f'<circle cx="{cx}" cy="{cy}" r="{r + 26}" fill="#1e1a17" stroke="#3a2e25" stroke-width="10"/><circle cx="{cx}" cy="{cy}" r="{r}" fill="#121519"/>{ticks}'
            f'<g id="{bid}h"><line x1="{cx}" y1="{cy}" x2="{cx}" y2="{cy - 170}" stroke="{PAPER}" stroke-width="14" stroke-linecap="round"/></g>'
            f'<g id="{bid}m"><line x1="{cx}" y1="{cy}" x2="{cx}" y2="{cy - 250}" stroke="{ORANGE}" stroke-width="8" stroke-linecap="round"/></g>'
            f'<circle cx="{cx}" cy="{cy}" r="16" fill="{ORANGE}"/><text x="{cx}" y="{cy + 160}" text-anchor="middle" font-family="Space Mono" font-size="54" fill="{GOLD}">{h:02d}:{m:02d}</text>')
    sc.js.append(f'tl.fromTo("#{bid}m",{{svgOrigin:"{cx} {cy}",rotation:{am - 40}}},{{rotation:{am},duration:2.4,ease:"power2.out",svgOrigin:"{cx} {cy}"}},{T + 0.3:.3f});')
    sc.js.append(f'tl.fromTo("#{bid}h",{{svgOrigin:"{cx} {cy}",rotation:{ah - 3}}},{{rotation:{ah},duration:2.4,ease:"power2.out",svgOrigin:"{cx} {cy}"}},{T + 0.3:.3f});')
    return svg(body, "#14110f")


def p_adf(sc, bid, T, D, p):
    cx, cy = 960, 520
    if p.get("loop"):
        body = (f'<g stroke="{PAPER}" stroke-width="10" fill="none"><ellipse id="{bid}a" cx="{cx}" cy="{cy - 80}" rx="140" ry="140"/></g>'
                f'<line x1="{cx}" y1="{cy + 60}" x2="{cx}" y2="{cy + 240}" stroke="{PAPER}" stroke-width="12"/>'
                f'<line id="{bid}l" x1="160" y1="{cy - 80}" x2="1760" y2="{cy - 80}" stroke="{GOLD}" stroke-width="5" stroke-dasharray="1600" stroke-dashoffset="1600"/>'
                f'<text x="{cx}" y="{cy + 330}" text-anchor="middle" font-size="44" fill="{INK}" font-family="Inter" font-weight="700" letter-spacing="6">LOOP ANTENNA · ONE LINE, TWO ENDS</text>')
        sc.js.append(f'tl.fromTo("#{bid}a",{{attr:{{rx:140}}}},{{attr:{{rx:20}},duration:2.0,yoyo:true,repeat:1,ease:"sine.inOut"}},{T + 0.4:.3f});')
        sc.js.append(f'tl.fromTo("#{bid}l",{{attr:{{"stroke-dashoffset":1600}}}},{{attr:{{"stroke-dashoffset":0}},duration:2.5,ease:"power1.inOut"}},{T + 1.2:.3f});')
        return svg(body)
    ticks = "".join(f'<text x="{cx + 230 * math.sin(math.radians(a)):.1f}" y="{cy + 12 - 230 * math.cos(math.radians(a)):.1f}" text-anchor="middle" font-size="34" fill="{INK}" font-family="Space Mono">{a // 10:02d}</text>'
                    for a in range(0, 360, 30))
    body = (f'<circle cx="{cx}" cy="{cy}" r="300" fill="#1e1a17" stroke="#3a2e25" stroke-width="12"/>{ticks}'
            f'<g id="{bid}n"><path d="M{cx},{cy - 190} L{cx + 18},{cy} L{cx},{cy + 150} L{cx - 18},{cy}Z" fill="{ORANGE}"/></g>'
            f'<text x="{cx}" y="{cy + 400}" text-anchor="middle" font-size="44" fill="{INK}" font-family="Inter" font-weight="700" letter-spacing="6">RADIO COMPASS · NOT WORKING</text>')
    sc.js.append(f'tl.fromTo("#{bid}n",{{svgOrigin:"{cx} {cy}",rotation:-8}},{{rotation:4,duration:3.0,ease:"sine.inOut",svgOrigin:"{cx} {cy}"}},{T + 0.3:.3f});')
    return svg(body, "#14110f")


def p_compass(sc, bid, T, D, p):
    cx, cy, deg = 960, 540, p.get("deg", 330)
    lab = "".join(f'<text x="{cx + 330 * math.sin(math.radians(a)):.1f}" y="{cy + 14 - 330 * math.cos(math.radians(a)):.1f}" text-anchor="middle" font-size="44" font-weight="700" fill="{INK}" font-family="Inter">{t}</text>'
                  for a, t in [(0, "N"), (90, "E"), (180, "S"), (270, "W")])
    body = (f'<circle cx="{cx}" cy="{cy}" r="380" fill="none" stroke="#3a2e25" stroke-width="6"/><circle cx="{cx}" cy="{cy}" r="280" fill="none" stroke="#3a2e25" stroke-width="2"/>{lab}'
            f'<g id="{bid}n"><path d="M{cx},{cy - 290} L{cx + 22},{cy} L{cx - 22},{cy}Z" fill="{GOLD}"/><path d="M{cx},{cy + 290} L{cx + 22},{cy} L{cx - 22},{cy}Z" fill="{ORANGE}"/></g>'
            f'<text id="{bid}t" x="{cx + 560}" y="{cy}" font-size="60" fill="{GOLD}" font-family="Space Mono">{deg}°</text>'
            f'<text id="{bid}u" x="{cx + 560}" y="{cy + 80}" font-size="60" fill="{ORANGE}" font-family="Space Mono">{(deg + 180) % 360}°</text>')
    sc.js.append(f'tl.fromTo("#{bid}n",{{svgOrigin:"{cx} {cy}",rotation:{deg - 60}}},{{rotation:{deg},duration:2.5,ease:"power2.out",svgOrigin:"{cx} {cy}"}},{T + 0.3:.3f});')
    sc.js.append(f'tl.fromTo("#{bid}t",{{opacity:0}},{{opacity:1,duration:0.6}},{T + 2.6:.3f});')
    sc.js.append(f'tl.fromTo("#{bid}u",{{opacity:0}},{{opacity:1,duration:0.6}},{T + D * 0.55:.3f});')
    return svg(body, "#14110f")


def p_flare(sc, bid, T, D, p):
    col = RED if p.get("red") else ORANGE
    body = (stars(60) + f'<rect y="840" width="1920" height="240" fill="#16130f"/><rect x="560" y="850" width="800" height="12" fill="#2a2119"/>'
            f'<g id="{bid}f"><circle cx="960" cy="840" r="10" fill="{col}"/><circle cx="960" cy="840" r="80" fill="{col}" opacity="0.18"/></g>'
            f'<path id="{bid}t" d="M960,840 Q950,640 960,340" stroke="{col}" stroke-width="3" fill="none" opacity="0.5" stroke-dasharray="560" stroke-dashoffset="560"/>')
    gap = max((D - 5) / 3, 4.5)
    for k in range(3):  # mỗi lần: bay lên rồi tắt
        t0 = T + 0.4 + k * gap
        sc.js.append(f'tl.fromTo("#{bid}f",{{y:0,opacity:1}},{{y:-500,opacity:1,duration:2.6,ease:"power2.out",immediateRender:{str(k == 0).lower()}}},{t0:.3f});')
        sc.js.append(f'tl.fromTo("#{bid}t",{{attr:{{"stroke-dashoffset":560}},opacity:0.5}},{{attr:{{"stroke-dashoffset":0}},duration:2.6,ease:"power2.out",immediateRender:{str(k == 0).lower()}}},{t0:.3f});')
        sc.js.append(f'tl.to(["#{bid}f","#{bid}t"],{{opacity:0,duration:1.4}},{t0 + 2.8:.3f});')
    return svg(body)


def p_fuel(sc, bid, T, D, p):
    cx, cy = 960, 600
    arc = f'M{cx - 300},{cy} A300,300 0 0 1 {cx + 300},{cy}'
    body = (f'<path d="{arc}" fill="none" stroke="#3a2e25" stroke-width="40"/><path d="M{cx - 300},{cy} A300,300 0 0 1 {cx - 212},{cy - 212}" fill="none" stroke="{RED}" stroke-width="40"/>'
            f'<text x="{cx - 330}" y="{cy + 70}" font-size="50" fill="{INK}" font-family="Space Mono">E</text><text x="{cx + 300}" y="{cy + 70}" font-size="50" fill="{INK}" font-family="Space Mono">F</text>'
            f'<g id="{bid}n"><line x1="{cx}" y1="{cy}" x2="{cx}" y2="{cy - 260}" stroke="{ORANGE}" stroke-width="10" stroke-linecap="round"/></g><circle cx="{cx}" cy="{cy}" r="22" fill="{ORANGE}"/>'
            f'<text x="{cx}" y="{cy + 160}" text-anchor="middle" font-size="44" fill="{INK}" font-family="Inter" font-weight="700" letter-spacing="8">FUEL</text>')
    sc.js.append(f'tl.fromTo("#{bid}n",{{svgOrigin:"{cx} {cy}",rotation:-30}},{{rotation:-86,duration:{max(D - 1.5, 2):.2f},ease:"power1.in",svgOrigin:"{cx} {cy}"}},{T + 0.3:.3f});')
    return svg(body, "#14110f")


def p_engines(sc, bid, T, D, p):
    body = (f'<path d="M260,560 L1660,560 L1660,600 L260,600Z" fill="#3a2e25"/><rect x="900" y="300" width="120" height="600" rx="50" fill="#2b231d"/>')
    for i, x in enumerate([420, 700, 1220, 1500]):
        body += (f'<rect x="{x - 50}" y="520" width="100" height="160" rx="24" fill="#2b231d" stroke="#5a4636" stroke-width="4"/>'
                 f'<circle id="{bid}e{i}" cx="{x}" cy="500" r="34" fill="{ORANGE}"/><text x="{x}" y="760" text-anchor="middle" font-family="Space Mono" font-size="36" fill="{INK}">{i + 1}</text>')
    for k, i in enumerate([0, 3, 1]):
        sc.js.append(f'tl.fromTo("#{bid}e{i}",{{opacity:1}},{{opacity:0.12,duration:0.6}},{T + 1.2 + k * (D - 3) / 3:.3f});')
    body += f'<text x="960" y="900" text-anchor="middle" font-family="Inter" font-weight="700" font-size="40" letter-spacing="8" fill="{INK}">FOUR ENGINES</text>'
    return svg(body, "#14110f")


def p_ground(sc, bid, T, D, p):
    if p.get("dunes"):
        body = (f'<defs><linearGradient id="{bid}g" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#d9b98f"/><stop offset="1" stop-color="#e9d2ad"/></linearGradient></defs>'
                f'<rect width="1920" height="1080" fill="url(#{bid}g)"/>'
                f'<g id="{bid}d"><path d="M-100,620 Q300,420 700,600 T1500,560 T2100,600 L2100,1080 L-100,1080Z" fill="#c9a27a"/>'
                f'<path d="M-100,800 Q400,620 900,780 T2100,760 L2100,1080 L-100,1080Z" fill="#b5895e"/></g>')
        sc.js.append(f'tl.fromTo("#{bid}d",{{x:0}},{{x:-60,duration:{D:.3f},ease:"none"}},{T:.3f});')
        if p.get("steps"):
            for i in range(12):
                x, y = 300 + i * 120, 900 - i * 14
                body += f'<ellipse class="{bid}s" cx="{x}" cy="{y + (8 if i % 2 else -8)}" rx="12" ry="20" fill="#8a6a49"/>'
            sc.js.append(f'tl.fromTo(".{bid}s",{{opacity:0.9}},{{opacity:0,duration:0.8,stagger:0.35}},{T + 1.0:.3f});')
        return svg(body, "#d9b98f")
    body = (f'<defs><linearGradient id="{bid}g" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2a3140"/><stop offset="0.55" stop-color="#c58b5a"/>'
            f'<stop offset="0.62" stop-color="#e8c08a"/></linearGradient></defs><rect width="1920" height="680" fill="url(#{bid}g)"/>'
            f'<circle id="{bid}s" cx="1300" cy="700" r="70" fill="#f3d6a0"/><rect y="660" width="1920" height="420" fill="#7a5f45"/>'
            + "".join(f'<circle cx="{(i * 397) % 1920}" cy="{700 + (i * 131) % 360}" r="{2 + i % 4}" fill="#5a4636"/>' for i in range(90)))
    sc.js.append(f'tl.fromTo("#{bid}s",{{attr:{{cy:720}}}},{{attr:{{cy:600}},duration:{D:.3f},ease:"none"}},{T:.3f});')
    return svg(body)


def p_shelter(sc, bid, T, D, p):
    body = (f'<rect width="1920" height="1080" fill="#d9b98f"/><rect y="760" width="1920" height="320" fill="#c9a27a"/>'
            f'<g id="{bid}t"><path d="M560,780 Q960,420 1360,780Z" fill="{PAPER}" stroke="#8a6a49" stroke-width="4"/>'
            f'<line x1="960" y1="560" x2="960" y2="790" stroke="#5a4636" stroke-width="8"/></g><circle cx="1600" cy="200" r="90" fill="#fff4d6" opacity="0.9"/>')
    sc.js.append(f'tl.fromTo("#{bid}t",{{svgOrigin:"960 780",scaleY:0.2,opacity:0}},{{scaleY:1,opacity:1,duration:1.6,ease:"power2.out",svgOrigin:"960 780"}},{T + 0.3:.3f});')
    return svg(body)


def p_notebook(sc, bid, T, D, p):
    mode = p.get("mode", "flip")
    if mode == "small":
        body = (f'<rect width="1920" height="1080" fill="#7a5f45"/><g id="{bid}b"><rect x="760" y="300" width="400" height="520" rx="12" fill="#3a2e25"/>'
                f'<rect x="790" y="330" width="340" height="460" rx="6" fill="none" stroke="#5a4636" stroke-width="3"/>'
                f'<text x="960" y="580" text-anchor="middle" font-family="EB Garamond" font-style="italic" font-size="64" fill="{PAPER}">{p.get("label", "")}</text></g>')
        sc.js.append(f'tl.fromTo("#{bid}b",{{y:40,opacity:0}},{{y:0,opacity:1,duration:1.2,ease:"power2.out"}},{T + 0.3:.3f});')
        return svg(body)
    lines = "".join(f'<line x1="{x0 + 50}" y1="{y}" x2="{x0 + 470}" y2="{y}" stroke="#1F4E8C" stroke-opacity="0.25" stroke-width="2"/>'
                    for x0 in (440, 960) for y in range(330, 820, 54))
    body = (f'<rect width="1920" height="1080" fill="#2a2119"/><g id="{bid}b"><rect x="430" y="250" width="1060" height="620" rx="10" fill="#3a2e25"/>'
            f'<rect x="440" y="260" width="520" height="600" fill="{PAPER}"/><rect x="960" y="260" width="520" height="600" fill="#efe7d6"/>{lines}'
            f'<rect id="{bid}p" x="960" y="260" width="520" height="600" fill="{PAPER}" stroke="#d6cbb4"/></g>')
    if mode == "flip":
        sc.js.append(f'tl.fromTo("#{bid}p",{{svgOrigin:"960 560",scaleX:1}},{{scaleX:-1,duration:1.8,ease:"power2.inOut",svgOrigin:"960 560"}},{T + 1.0:.3f});')
    else:  # close: hạ sáng dần
        sc.js.append(f'tl.fromTo("#{bid}b",{{opacity:1}},{{opacity:0.25,duration:{max(D - 1, 2):.2f},ease:"sine.in"}},{T + 0.5:.3f});')
    return svg(body)


def p_rig(sc, bid, T, D, p):
    body = (f'<rect width="1920" height="1080" fill="#d9b98f"/><rect y="800" width="1920" height="280" fill="#c9a27a"/>'
            f'<g id="{bid}r" fill="none" stroke="#2a2119" stroke-width="10"><path d="M860,800 L940,260 L1060,260 L1140,800"/>'
            f'<path d="M880,660 L1120,660 M900,520 L1100,520 M920,390 L1080,390 M880,660 L1100,520 M1120,660 L900,520 M900,520 L1080,390 M1100,520 L920,390"/></g>'
            f'<text id="{bid}y" x="1400" y="420" font-family="EB Garamond" font-size="150" font-weight="600" fill="#2a2119">{p.get("year", "")}</text>')
    sc.js.append(f'tl.fromTo("#{bid}r",{{opacity:0,y:30}},{{opacity:1,y:0,duration:1.4,ease:"power2.out"}},{T + 0.2:.3f});')
    sc.js.append(f'tl.fromTo("#{bid}y",{{opacity:0}},{{opacity:1,duration:1.0}},{T + 1.0:.3f});')
    return svg(body)


def plane(x, y, s=1.0, col="#2a2119"):
    return (f'<g transform="translate({x},{y}) scale({s})" fill="{col}"><path d="M-120,0 L120,0 L130,8 L-120,10Z"/><path d="M-20,2 L-60,-70 L-40,-70 L20,2Z"/>'
            f'<path d="M-20,8 L-60,80 L-40,80 L20,8Z"/><path d="M-110,4 L-130,-26 L-118,-26 L-100,4Z"/></g>')


def heli(x, y, s=1.0, col="#2a2119"):
    return (f'<g transform="translate({x},{y}) scale({s})" fill="{col}"><ellipse cx="0" cy="0" rx="60" ry="26"/><rect x="40" y="-6" width="110" height="10"/>'
            f'<rect x="-100" y="-40" width="200" height="6"/><rect x="-4" y="-40" width="8" height="16"/></g>')


def p_planes(sc, bid, T, D, p):
    body = f'<rect width="1920" height="1080" fill="#e2c9a0"/><rect y="760" width="1920" height="320" fill="#c9a27a"/>'
    if p.get("kind") == "search":
        body += f'<g id="{bid}a">{plane(0, 300, 1.4)}</g><g id="{bid}b">{heli(0, 480, 1.0)}</g><g id="{bid}c">{heli(0, 560, 0.8)}</g>'
        for k, (a, b, d) in enumerate([(-300, 2200, 1.0), (2200, -300, 1.3), (-300, 2200, 1.6)]):
            sc.js.append(f'tl.fromTo("#{bid}{"abc"[k]}",{{x:{a}}},{{x:{b},duration:{D * d * 0.8:.2f},ease:"none"}},{T:.3f});')
    else:
        body += f'<g id="{bid}a">{plane(0, 330, 0.8)}</g>'
        sc.js.append(f'tl.fromTo("#{bid}a",{{x:-300}},{{x:2200,duration:{D:.3f},ease:"none"}},{T:.3f});')
    return svg(body)


ILLUS = {"parachutes": p_parachutes, "sky": p_sky, "clock": p_clock, "adf": p_adf, "compass": p_compass, "flare": p_flare,
         "fuel": p_fuel, "engines": p_engines, "ground": p_ground, "shelter": p_shelter, "notebook": p_notebook, "rig": p_rig,
         "planes": p_planes}
