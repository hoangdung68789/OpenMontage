"""Phép chiếu chung cho nền bản đồ và lớp chấm/đường (equirectangular, co theo cos vĩ độ giữa)."""
import math

# bbox = (lon0, lon1, lat0, lat1); 100 px mỗi độ vĩ
REGIONS = {
    "med": {"bbox": (6.0, 34.0, 21.0, 44.0)},
    "lakes": {"bbox": (-93.0, -80.0, 40.5, 49.5)},
}
for r in REGIONS.values():
    lon0, lon1, lat0, lat1 = r["bbox"]
    r["k"] = math.cos(math.radians((lat0 + lat1) / 2))
    r["size"] = (round((lon1 - lon0) * 100 * r["k"]), round((lat1 - lat0) * 100))


def proj(region, lon, lat):
    r = REGIONS[region]
    lon0, _, _, lat1 = r["bbox"]
    return (lon - lon0) * 100 * r["k"], (lat1 - lat) * 100


# Tọa độ: Wikipedia API prop=coordinates (tra 23/11/2026) trừ chỗ ghi khác
PLACES = {
    "benghazi": (20.07, 32.12),        # [chưa tra API] tọa độ thành phố, chỉ để đặt nhãn
    "benina": (20.2694, 32.0972),      # Benina International Airport
    "soluch": (20.25, 31.67),          # [chưa tra API] thị trấn Suluq, đặt nhãn
    "naples": (14.27, 40.85),          # [chưa tra API] đặt nhãn
    "wreck": (24.0242, 26.7127),       # Lady Be Good (aircraft)
    "wheelus": (13.2803, 32.895),      # Wheelus Air Base
    "tripoli": (13.19, 32.89),
    "tobruk": (23.96, 32.08),          # [chưa tra API] đặt nhãn
    "kufra": (23.2833, 24.1833),       # Kufra
    "calanscio": (22.6, 28.6),         # vị trí nhãn biển cát Calanscio (minh họa)
    "lake_linden": (-88.4081, 47.1953),  # Lake Linden, Michigan
}
