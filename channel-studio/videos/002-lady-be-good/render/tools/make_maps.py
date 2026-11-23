"""Vẽ nền bản đồ SVG cho 002 từ Natural Earth (phạm vi công cộng, naturalearthdata.com).

python make_maps.py <thư mục geojson> <thư mục ra assets/maps>
Ghi med.svg (Địa Trung Hải + Libya) và lakes.svg (Michigan), cùng phép chiếu với tools/geo.py.
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from geo import REGIONS, proj  # noqa: E402

src, out = Path(sys.argv[1]), Path(sys.argv[2])
out.mkdir(parents=True, exist_ok=True)
SEA, LAND, LIBYA, BORDER, COAST = "#121519", "#2b231d", "#3a2d22", "#5a4636", "#7a5a40"


def rings(geom):
    polys = geom["coordinates"] if geom["type"] == "MultiPolygon" else [geom["coordinates"]]
    for poly in polys:
        for ring in poly:
            yield ring


def path_d(region, ring_iter):
    lon0, lon1, lat0, lat1 = REGIONS[region]["bbox"]
    parts = []
    for ring in ring_iter:
        xs = [p[0] for p in ring]
        ys = [p[1] for p in ring]
        if max(xs) < lon0 - 3 or min(xs) > lon1 + 3 or max(ys) < lat0 - 3 or min(ys) > lat1 + 3:
            continue
        pts, last = [], None
        for lon, lat in ring:
            x, y = proj(region, lon, lat)
            q = (round(x), round(y))
            if q != last:
                pts.append(f"{q[0]},{q[1]}")
                last = q
        if len(pts) > 2:
            parts.append("M" + "L".join(pts) + "Z")
    return "".join(parts)


land = json.loads((src / "ne_50m_land.geojson").read_text(encoding="utf-8"))
countries = json.loads((src / "ne_50m_admin_0_countries.geojson").read_text(encoding="utf-8"))
lakes = json.loads((src / "ne_10m_lakes.geojson").read_text(encoding="utf-8"))

for region in REGIONS:
    w, h = REGIONS[region]["size"]
    land_d = path_d(region, (r for f in land["features"] for r in rings(f["geometry"])))
    border_d = path_d(region, (r for f in countries["features"] for r in rings(f["geometry"])))
    libya = [f for f in countries["features"] if f["properties"].get("ADM0_A3") == "LBY"]
    libya_d = path_d(region, (r for f in libya for r in rings(f["geometry"]))) if region == "med" else ""
    big = [f for f in lakes["features"] if (f["properties"].get("scalerank") or 9) <= 1]
    lakes_d = path_d(region, (r for f in big for r in rings(f["geometry"]))) if region == "lakes" else ""
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">'
           f'<rect width="{w}" height="{h}" fill="{SEA}"/>'
           f'<path d="{land_d}" fill="{LAND}" stroke="{COAST}" stroke-width="2" stroke-linejoin="round"/>'
           + (f'<path d="{libya_d}" fill="{LIBYA}"/>' if libya_d else "")
           + f'<path d="{border_d}" fill="none" stroke="{BORDER}" stroke-width="1.6" stroke-dasharray="6 5"/>'
           + (f'<path d="{lakes_d}" fill="{SEA}" stroke="{COAST}" stroke-width="2"/>' if lakes_d else "")
           + "</svg>")
    (out / f"{region}.svg").write_text(svg, encoding="utf-8")
    print(region, w, h, round(len(svg) / 1024), "KB")
