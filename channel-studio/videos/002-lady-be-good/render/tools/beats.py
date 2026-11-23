"""Dữ liệu cảnh cho 002, chép từ dòng "- Hình:" của script_part1..4.md (giờ ước tính kịch bản).
Ảnh: Wikimedia Commons, tất cả USAF/USAAF phạm vi công cộng (projects/lady-be-good/assets/images/commons/_manifest.json).
"""
GOLD, RED, PAPER = "#C9A54C", "#C8423A", "#E8DFCC"
PD = "U.S. Air Force photo · public domain"
PHOTOS = {
    "parts": {"file": "0000050606-F-1234P-014.jpg", "w": 1280, "credit": PD},
    "side": {"file": "060530-F-1234S-042.jpg", "w": 1280, "credit": PD},
    "aerial57": {"file": "376bg-ladybgood.jpg", "w": 960, "credit": PD},
    "macr": {"file": "B-24D_Lady_Be_Good_Missing_Air_Crew_Report_MACR_937_page_1.png", "w": 500, "credit": "Missing Air Crew Report 937 · USAAF · public domain"},
    "cockpit": {"file": "Co-pilot_place.jpg", "w": 330, "credit": PD},
    "headset": {"file": "Hatton_s_headset.jpg", "w": 574, "credit": PD},
    "crew": {"file": "LADY_BE_GOOD_Crew.jpg", "w": 1280, "credit": "USAAF crew photo · public domain"},
    "topdown": {"file": "Lady_Be_Good.jpg", "w": 500, "credit": PD},
    "nose": {"file": "Lady_Be_Good_Nose_Section.jpg", "w": 1280, "credit": PD},
    "window": {"file": "Lady_Be_Good_Window.jpg", "w": 960, "credit": PD},
    "discovery": {"file": "Lady_Be_Good_Wreckage_Discovery.jpg", "w": 1280, "credit": PD},
    "c2": {"file": "Lady_Be_Good_crash_photos_1960_-2.jpg", "w": 960, "credit": PD},
    "c3": {"file": "Lady_Be_Good_crash_photos_1960_-3.jpg", "w": 1280, "credit": PD},
    "c4": {"file": "Lady_Be_Good_crash_photos_1960_-4.jpg", "w": 960, "credit": PD},
    "c1": {"file": "Lady_Be_Good_crash_photos_1960_-_1.jpg", "w": 960, "credit": PD},
    "gear": {"file": "Landing_gear.jpg", "w": 500, "credit": PD},
    "nosewheel": {"file": "Nose_wheel.png", "w": 500, "credit": PD},
    "prayer": {"file": "Prayer_service.jpg", "w": 960, "credit": PD},
    "repaint": {"file": "Repaint_of_Lady_Be_Good.png", "w": 500, "credit": "B-24D 41-24301 · USAAF · public domain"},
    "repatriation": {"file": "Repatriation.jpg", "w": 960, "credit": PD},
    "rose": {"file": "Rose_with_Lady_Be_Good.png", "w": 250, "credit": PD},
    "sortie": {"file": "Sortie_report.png", "w": 330, "credit": "Declassified USAAF report · public domain"},
    "tail": {"file": "Tail_view_of_the_crashed_Consolidated_B-24D_Lady_Be_Good._.jpg", "w": 1280, "credit": PD},
    "thermos": {"file": "Thermos_with_coffee.png", "w": 250, "credit": PD},
    "turret": {"file": "Upper_turret.jpg", "w": 500, "credit": PD},
}

CREW = [
    ("1st Lt.", "William Hatton", "Pilot"), ("2nd Lt.", "Robert Toner", "Co-pilot"),
    ("2nd Lt.", "D.P. Hays", "Navigator"), ("2nd Lt.", "John Woravka", "Bombardier"),
    ("T/Sgt.", "Harold Ripslinger", "Flight engineer"), ("T/Sgt.", "Robert LaMotte", "Radio operator"),
    ("S/Sgt.", "Guy Shelley", "Gunner"), ("S/Sgt.", "Vernon Moore", "Gunner"), ("S/Sgt.", "Samuel Adams", "Gunner"),
]
FIVE = ["William Hatton", "Robert Toner", "D.P. Hays", "Robert LaMotte", "Samuel Adams"]
THREE = ["Guy Shelley", "Harold Ripslinger", "Vernon Moore"]
EIGHT = [c[1] for c in CREW if c[1] != "John Woravka"]

CHAPTERS = [
    (0, "HOOK", ["S0.1"]),
    (1, "THE NEW CREW", ["S1.1", "S1.2", "S1.3"]),
    (2, "NAPLES, 4 APRIL 1943", ["S2.1", "S2.2", "S2.3", "S2.4"]),
    (3, "FLYING PAST HOME", ["S3.1", "S3.2", "S3.3", "S3.4"]),
    (4, "INTO THE DARK", ["S4.1", "S4.2", "S4.3", "S4.4"]),
    (5, "THE DIARY", ["S5.1", "S5.2", "S5.3", "S5.4", "S5.5", "S5.6", "S5.7"]),
    (6, "FOUND", ["S6.1", "S6.2", "S6.3", "S6.4", "S6.5"]),
    (7, "WHAT THE DESERT KEPT", ["S7.1", "S7.2", "S7.3"]),
]
# (file, chương đầu, chương cuối, âm lượng) · Kevin MacLeod (incompetech.com), CC BY 4.0
MUSIC = [
    ("Lightless_Dawn.mp3", 0, 1, 0.16), ("Hiding_Your_Reality.mp3", 2, 2, 0.14), ("Unseen_Horrors.mp3", 3, 3, 0.13),
    ("Sad_Trio.mp3", 4, 4, 0.14), ("Long_Note_Two.mp3", 5, 5, 0.15), ("Lightless_Dawn.mp3", 6, 6, 0.15),
    ("Despair_and_Triumph.mp3", 7, 7, 0.14),
]

# --- bản đồ: camera (lon, lat, scale) ---
LIBYA = (22.2, 29.3, 1.25)
MEDV = (18.5, 36.4, 1.0)
WRECKV = (23.4, 27.4, 4.0)
THOUGHT = (20.45, 33.55)   # trên tia 330° từ Benina, ngoài biển (sơ đồ)
JUMP = (23.86, 26.93)      # ≈16 dặm tây bắc xác máy bay theo hướng bay 150° (sơ đồ)
FIVE_AT = (22.95, 27.85)   # ≈81 dặm từ xác máy bay [WIKI] (sơ đồ)
SHELLEY_AT = (22.6, 28.25)
RIP_AT = (22.35, 28.55)
WORAVKA_AT = (23.9, 26.85)
ASF = "Air & Space Forces Magazine"
NARA = "U.S. National Archives"
WIKI = "Wikipedia"

BEATS = {
    "S0.1": [
        ("00:00", {"k": "map", "cam": (20.4, 32.0, 2.0), "cam2": (22.6, 28.6, 1.5), "items": [
            {"k": "label", "at": "benghazi", "text": "BENGHAZI", "t": 0.05},
            {"k": "pin", "at": "wreck", "color": RED, "t": 0.55}, {"k": "ring", "at": "wreck", "t": 0.6, "color": RED}],
            "head": "LIBYA"}),
        ("00:12", {"k": "photo", "img": "discovery", "cap": "The Libyan Desert"}),
        ("00:25", {"k": "photo", "img": "nose", "push": "left"}),
        ("00:39", {"k": "map", "cam": (19.0, 34.6, 0.82), "cam2": (20.5, 33.6, 0.78), "items": [
            {"k": "pin", "at": "soluch", "text": "SOLUCH", "t": 0.02, "off": (-16, 30), "anchor": "end"},
            {"k": "pin", "at": "naples", "text": "NAPLES", "t": 0.05},
            {"k": "route", "pts": ["soluch", "naples"], "t": 0.1, "d": 2.5, "color": GOLD},
            {"k": "route", "pts": ["naples", "soluch", "wreck"], "t": 0.4, "d": 4.0},
            {"k": "pin", "at": "wreck", "color": RED, "t": 0.75}]}),
        ("00:53", {"k": "illus", "name": "parachutes", "n": 9}),
        ("01:03", {"k": "title", "style": "brand", "text": "LADY BE GOOD", "sub": "THE BOMBER THAT FLEW PAST HOME", "fade_out": True}),
    ],
    "S1.1": [
        ("01:11", {"k": "map", "cam": MEDV, "cam2": (20.2, 33.2, 1.6), "items": [
            {"k": "pin", "at": "benghazi", "text": "BENGHAZI", "t": 0.1},
            {"k": "pin", "at": "soluch", "text": "SOLUCH", "t": 0.45, "off": (16, 34)}],
            "head": "376th BOMB GROUP · LIBYA, 1943"}),
        ("01:27", {"k": "photo", "img": "repaint", "cap": "B-24D Liberator 41-24301"}),
        ("01:44", {"k": "map", "cam": MEDV, "items": [
            {"k": "pin", "at": "soluch", "text": "SOLUCH", "t": 0.02, "off": (16, 34)},
            {"k": "route", "pts": ["soluch", "naples"], "t": 0.1, "d": 3.0, "color": GOLD},
            {"k": "pin", "at": "naples", "text": "ITALY", "t": 0.4}]}),
        ("01:56", {"k": "title", "style": "stamp", "text": "41-24301", "sub": "B-24D · NEW TO THE GROUP"}),
    ],
    "S1.2": [
        ("02:08", {"k": "photo", "img": "crew", "cap": "The crew of Lady Be Good"}),
        ("02:20", {"k": "cards", "slow": True, "title": "NINE MEN"}),
        ("02:56", {"k": "cards", "title": "REMEMBER THESE NAMES", "hi": ["Vernon Moore"]}),
    ],
    "S1.3": [
        ("03:10", {"k": "title", "style": "date", "text": "4 APRIL 1943", "sub": "FIRST COMBAT MISSION"}),
        ("03:18", {"k": "map", "cam": (14.6, 40.6, 3.2), "cam2": (14.4, 40.8, 3.6), "items": [
            {"k": "pin", "at": "naples", "text": "NAPLES HARBOR", "t": 0.1}, {"k": "ring", "at": "naples", "t": 0.3}]}),
        ("03:29", {"k": "title", "style": "big", "text": "MISSION 1", "fade_out": True}),
    ],
    "S2.1": [
        ("03:37", {"k": "map", "cam": MEDV, "items": [
            {"k": "pin", "at": "soluch", "text": "SOLUCH", "t": 0.02, "off": (16, 34)},
            {"k": "route", "pts": ["soluch", "naples"], "t": 0.1, "d": 5.0, "color": GOLD, "text": "Wave 1 · Wave 2"},
            {"k": "dot", "pts": ["soluch", (18.6, 35.2)], "t": 0.35, "d": 8.0},
            {"k": "pin", "at": "naples", "text": "NAPLES", "t": 0.2}],
            "notes": [("25 B-24s in two waves", 0.1), ("Lady Be Good flies in the second wave", 0.5)]}),
        ("04:09", {"k": "illus", "name": "sky", "sunset": True, "mark": False}),
    ],
    "S2.2": [
        ("04:23", {"k": "map", "cam": (20.0, 32.4, 2.2), "items": [
            {"k": "sand", "t": 0.0, "o": 0.4}, {"k": "pin", "at": "soluch", "text": "SOLUCH", "t": 0.05, "off": (16, 34)},
            {"k": "dot", "pts": ["soluch", (19.6, 33.3)], "t": 0.3, "d": 6.0}],
            "notes": [("Sandstorm at take-off", 0.1), ("Most of the second wave turned back", 0.5)]}),
        ("04:46", {"k": "map", "cam": (17.5, 37.5, 1.3), "items": [
            {"k": "dot", "pts": [(19.0, 34.5), (15.8, 39.2)], "t": 0.05, "d": 9.0}],
            "head": "NIGHT FALLS OVER THE SEA"}),
    ],
    "S2.3": [
        ("04:58", {"k": "compare", "items": [("ACCOUNT A", "Reached the Naples area, could not bomb, turned for home"),
                                             ("ACCOUNT B", "Never found the target in the overcast")],
                   "note": "The records do not agree"}),
        ("05:23", {"k": "map", "cam": (15.5, 39.6, 2.2), "items": [
            {"k": "route", "pts": [(16.8, 37.8), "naples"], "dash": True, "t": 0.05},
            {"k": "route", "pts": [(16.8, 37.8), (15.6, 39.4)], "dash": True, "t": 0.15, "color": GOLD},
            {"k": "pin", "at": "naples", "text": "NAPLES", "t": 0.05}, {"k": "sand", "t": 0.45, "o": 0.25}],
            "notes": [("Cloud over Naples", 0.45)]}),
    ],
    "S2.4": [
        ("05:41", {"k": "photo", "img": "cockpit", "cap": "Co-pilot's seat, photographed at the wreck"}),
        ("05:52", {"k": "illus", "name": "clock", "time": "00:12"}),
        ("06:04", {"k": "map", "cam": (20.2, 32.6, 1.8), "items": [
            {"k": "pin", "at": "benina", "text": "BENINA", "t": 0.05, "color": GOLD},
            {"k": "ring", "at": "benina", "t": 0.2, "r": 500}]}),
    ],
    "S3.1": [
        ("06:08", {"k": "illus", "name": "clock", "time": "00:12", "cap": "Shortly after midnight, Hatton radios Benina"}),
        ("06:23", {"k": "illus", "name": "adf"}),
        ("06:43", {"k": "map", "cam": (20.8, 32.8, 1.6), "items": [
            {"k": "dot", "pts": [(20.4, 33.9)], "t": 0.1}], "head": "NO LIGHTS BELOW"}),
    ],
    "S3.2": [
        ("07:03", {"k": "photo", "img": "sortie", "cap": "Declassified report"}),
        ("07:23", {"k": "illus", "name": "compass", "deg": 330, "cap": "Bearing from Benina: 330°"}),
        ("07:38", {"k": "map", "cam": (20.4, 32.8, 2.2), "items": [
            {"k": "pin", "at": "benina", "text": "BENINA", "t": 0.02, "color": GOLD},
            {"k": "route", "pts": ["benina", (19.4, 34.3)], "t": 0.1, "d": 2.0, "color": GOLD, "text": "330°"},
            {"k": "dot", "pts": [THOUGHT], "t": 0.4}],
            "notes": [("Where the crew believed they were", 0.45)]}),
    ],
    "S3.3": [
        ("07:55", {"k": "illus", "name": "adf", "loop": True}),
        ("08:10", {"k": "map", "cam": (21.2, 30.8, 1.5), "items": [
            {"k": "pin", "at": "benina", "text": "BENINA", "t": 0.02, "color": GOLD},
            {"k": "route", "pts": ["benina", (19.4, 34.3)], "t": 0.05, "d": 2.0, "color": GOLD, "text": "330°"},
            {"k": "route", "pts": ["benina", (22.0, 28.6)], "t": 0.25, "d": 2.0, "text": "150°"},
            {"k": "dot", "pts": [THOUGHT, (20.9, 31.2)], "t": 0.55, "d": 3.0}],
            "notes": [("Same line, two directions", 0.2), ("Reciprocal reading", 0.55)]}),
        ("08:38", {"k": "map", "cam": (21.6, 30.4, 1.5), "items": [
            {"k": "dot", "pts": [(20.9, 31.2), (21.8, 29.6)], "t": 0.05, "d": 6.0}]}),
    ],
    "S3.4": [
        ("08:52", {"k": "illus", "name": "flare", "cap": "Flares fired over Soluch"}),
        ("09:12", {"k": "map", "cam": (20.6, 31.9, 2.4), "items": [
            {"k": "pin", "at": "soluch", "text": "SOLUCH", "t": 0.02, "color": GOLD, "off": (-16, 8), "anchor": "end"},
            {"k": "dot", "pts": [(20.0, 32.6), "soluch", (20.9, 31.1)], "t": 0.1, "d": 7.0}]}),
        ("09:32", {"k": "map", "cam": (21.4, 31.0, 1.6), "cam2": LIBYA, "items": [
            {"k": "route", "pts": [(20.0, 32.6), "soluch", "wreck"], "t": 0.05, "d": 6.0},
            {"k": "pin", "at": "wreck", "color": RED, "t": 0.75}],
            "notes": [("Two more hours, deeper into the desert", 0.2)]}),
    ],
    "S4.1": [
        ("09:40", {"k": "illus", "name": "fuel"}),
        ("09:55", {"k": "photo", "img": "c3", "cap": "Nose section at the crash site"}),
        ("10:15", {"k": "illus", "name": "engines"}),
    ],
    "S4.2": [
        ("10:30", {"k": "illus", "name": "parachutes", "n": 9}),
        ("10:45", {"k": "map", "cam": WRECKV, "items": [
            {"k": "pin", "at": JUMP, "text": "BAIL-OUT", "t": 0.05, "color": GOLD, "off": (-16, -14), "anchor": "end"},
            {"k": "route", "pts": [JUMP, "wreck"], "t": 0.15, "d": 4.0, "text": "≈16 mi"},
            {"k": "dot", "pts": [JUMP, "wreck"], "t": 0.15, "d": 4.0},
            {"k": "pin", "at": "wreck", "color": RED, "t": 0.6}]}),
        ("11:05", {"k": "illus", "name": "flare", "red": True}),
        ("11:12", {"k": "cards", "dim": ["John Woravka"], "title": "EIGHT ANSWER · ONE DOES NOT"}),
    ],
    "S4.3": [
        ("11:22", {"k": "quote", "text": "Got lost returning. Out of gas. Jumped.", "src": f"Toner diary, as published by the {NARA}"}),
        ("11:42", {"k": "quote", "text": "Can't find John. All others present.", "src": f"Toner diary, as published by the {NARA}"}),
    ],
    "S4.4": [
        ("11:56", {"k": "illus", "name": "ground", "dawn": True}),
        ("12:16", {"k": "map", "cam": WRECKV, "items": [
            {"k": "pin", "at": JUMP, "text": "BAIL-OUT", "t": 0.05, "color": GOLD, "off": (-16, -14), "anchor": "end"},
            {"k": "pin", "at": "wreck", "text": "WRECK, OUT OF SIGHT", "color": RED, "t": 0.2},
            {"k": "route", "pts": [JUMP, (22.6, 28.3)], "t": 0.5, "d": 2.5, "color": PAPER, "text": "Mediterranean?"}]}),
        ("12:44", {"k": "chips", "title": "WATER, BY THE RECORDS", "items": [("½ canteen", NARA), ("1 pint", ASF), ("1 canteen", WIKI)]}),
    ],
    "S5.1": [
        ("12:52", {"k": "map", "cam": WRECKV, "cam2": (23.3, 27.9, 2.6), "items": [
            {"k": "pin", "at": JUMP, "t": 0.02, "color": GOLD},
            {"k": "steps", "pts": [JUMP, FIVE_AT], "t": 0.1, "d": 12.0, "n": 22}],
            "head": "NORTH-WEST, ON FOOT"}),
        ("13:12", {"k": "quote", "text": "Nites are about 35 degrees", "src": f"Toner diary, as quoted by {ASF}", "label": "Diary of 2Lt. Robert Toner"}),
        ("13:32", {"k": "photo", "img": "c1", "cap": "Parts strewn as she skidded to a halt"}),
        ("13:50", {"k": "chips", "title": "LEFT BEHIND, ON PURPOSE", "items": [("Parachute arrows", ASF), ("Boots", ASF), ("Parachute cord", ASF)]}),
    ],
    "S5.2": [
        ("13:55", {"k": "map", "cam": (21.6, 30.0, 1.15), "items": [
            {"k": "pin", "at": THOUGHT, "text": "WHERE THEY THOUGHT THEY WERE", "t": 0.05, "color": GOLD},
            {"k": "pin", "at": JUMP, "text": "WHERE THEY ACTUALLY WERE", "t": 0.3, "color": RED},
            {"k": "route", "pts": [THOUGHT, JUMP], "dash": True, "t": 0.35},
            {"k": "pin", "at": "benghazi", "text": "BENGHAZI", "t": 0.6, "off": (16, -14)}],
            "notes": [("Wreck ≈ 440 mi south-east of Benghazi · " + NARA, 0.6)]}),
        ("14:45", {"k": "quote", "text": "Still going", "src": f"Toner diary, as quoted by {ASF}"}),
    ],
    "S5.3": [
        ("15:02", {"k": "illus", "name": "ground", "dunes": True}),
        ("15:22", {"k": "map", "cam": (23.1, 28.2, 2.4), "items": [
            {"k": "label", "at": "calanscio", "text": "CALANSCIO SAND SEA", "t": 0.1, "fs": 34, "tc": "#d9b98f", "anchor": "middle", "off": (0, 0)},
            {"k": "steps", "pts": [JUMP, FIVE_AT], "t": 0.02, "d": 2.0, "n": 22}]}),
        ("15:30", {"k": "quote", "text": "Good wind but continuous blowing of sand", "src": f"Toner diary, as quoted by {ASF}"}),
        ("15:42", {"k": "illus", "name": "ground", "dunes": True, "steps": True}),
    ],
    "S5.4": [
        ("15:49", {"k": "title", "style": "date", "text": "FRIDAY, APRIL 9"}),
        ("16:04", {"k": "quote", "text": "Shelley, Rip, Moore separate & try to go for help", "src": f"Toner diary, as quoted by {ASF}"}),
        ("16:19", {"k": "cards", "groups": [THREE, FIVE], "glabels": ["GO ON FOR HELP", "STAY AND WAIT"], "show": THREE + FIVE}),
        ("16:30", {"k": "illus", "name": "shelter", "cap": "One parachute left"}),
        ("16:40", {"k": "chips", "title": "DISTANCE WALKED TOGETHER", "items": [("78 mi", ASF), ("85 mi", NARA)]}),
    ],
    "S5.5": [
        ("16:48", {"k": "illus", "name": "notebook", "mode": "flip"}),
        ("17:08", {"k": "quote", "text": "Still having prayer meetings for help", "src": f"Toner diary, as quoted by {ASF}"}),
        ("17:14", {"k": "illus", "name": "sky"}),
        ("17:22", {"k": "quote", "text": "No help yet, very cold nite.", "date": "MONDAY, APRIL 12", "src": f"Toner diary, as quoted by {ASF}"}),
    ],
    "S5.6": [
        ("17:32", {"k": "illus", "name": "notebook", "mode": "close"}),
        ("17:52", {"k": "title", "style": "big", "text": "8 DAYS", "fade_out": True}),
        ("18:07", {"k": "chips", "title": "THE DIARY IS DESCRIBED BY", "items": [("Toner diary", NARA), ("Toner diary", ASF)]}),
        ("18:22", {"k": "title", "style": "date", "text": "1960", "sub": "WHERE IT WAS FOUND"}),
    ],
    "S5.7": [
        ("18:33", {"k": "map", "cam": (23.0, 28.1, 2.8), "items": [
            {"k": "pin", "at": FIVE_AT, "t": 0.02, "color": GOLD},
            {"k": "steps", "pts": [FIVE_AT, RIP_AT, (22.1, 28.85)], "t": 0.1, "d": 8.0, "n": 14, "erase": 0.8}],
            "head": "THREE GO ON"}),
        ("18:53", {"k": "illus", "name": "notebook", "mode": "small", "label": "Ripslinger"}),
        ("19:02", {"k": "map", "cam": (23.0, 28.1, 2.8), "cam2": LIBYA, "items": [{"k": "sand", "t": 0.1, "o": 0.45}]}),
        ("19:08", {"k": "illus", "name": "rig", "year": "1958"}),
    ],
    "S6.1": [
        ("19:21", {"k": "title", "style": "big", "text": "1943 → 1958", "sand": True}),
        ("19:36", {"k": "illus", "name": "planes", "kind": "survey"}),
        ("19:51", {"k": "photo", "img": "topdown", "cap": "Lady Be Good from the air"}),
        ("20:06", {"k": "chips", "title": "FIRST SIGHTED", "items": [("May 1958", f"{WIKI} · {ASF}"), ("Nov 1958", NARA)], "note": "The sources give different dates"}),
    ],
    "S6.2": [
        ("20:19", {"k": "title", "style": "date", "text": "FEBRUARY 1959", "sub": "D'ARCY OIL GEOLOGISTS REACH THE WRECK"}),
        ("20:34", {"k": "photo", "img": "side", "cap": "Broken in two behind the wings"}),
        ("20:46", {"k": "photo", "img": "turret", "cap": "Upper turret, guns still in place"}),
        ("20:54", {"k": "photo", "img": "thermos", "cap": "A thermos found in the wreck"}),
        ("21:09", {"k": "photo", "img": "headset", "cap": "Hatton's headset"}),
        ("21:19", {"k": "photo", "img": "tail", "push": "out"}),
    ],
    "S6.3": [
        ("21:24", {"k": "map", "cam": (18.6, 29.9, 0.95), "items": [
            {"k": "pin", "at": "wheelus", "text": "WHEELUS AIR BASE", "t": 0.05, "color": GOLD},
            {"k": "pin", "at": "wreck", "text": "WRECK", "color": RED, "t": 0.2},
            {"k": "route", "pts": ["wheelus", "wreck"], "dash": True, "t": 0.35}]}),
        ("21:39", {"k": "illus", "name": "planes", "kind": "search"}),
        ("21:54", {"k": "map", "cam": WRECKV, "items": [
            {"k": "area", "at": (23.5, 27.4), "r": 70, "t": 0.1, "color": GOLD}, {"k": "pin", "at": "wreck", "color": RED, "t": 0.02}],
            "notes": [("≈ 450 sq mi · 6 days", 0.2)]}),
        ("22:02", {"k": "photo", "img": "c4"}),
        ("22:16", {"k": "photo", "img": "c2"}),
        ("22:22", {"k": "title", "style": "stamp", "text": "SEARCH CALLED OFF", "sub": "SEPTEMBER 2, 1959"}),
    ],
    "S6.4": [
        ("22:29", {"k": "title", "style": "date", "text": "FEBRUARY 11, 1960", "sub": "A BRITISH PETROLEUM SURVEY TEAM"}),
        ("22:44", {"k": "cards", "show": FIVE, "slow": True}),
        ("22:54", {"k": "photo", "img": "prayer", "cap": "Service at the site, 1960"}),
        ("23:02", {"k": "map", "cam": WRECKV, "items": [
            {"k": "pin", "at": "wreck", "color": RED, "t": 0.02, "text": "WRECK"},
            {"k": "route", "pts": ["wreck", FIVE_AT], "dash": True, "t": 0.1, "text": "≈ 81 mi · " + WIKI},
            {"k": "pin", "at": FIVE_AT, "color": GOLD, "t": 0.3, "text": "THE FIVE", "off": (-16, -14), "anchor": "end"}]}),
    ],
    "S6.5": [
        ("23:13", {"k": "title", "style": "stamp", "text": "OPERATION CLIMAX", "sub": "MAY 1960"}),
        ("23:20", {"k": "illus", "name": "planes", "kind": "search"}),
        ("23:33", {"k": "map", "cam": (23.0, 28.0, 2.9), "items": [
            {"k": "pin", "at": FIVE_AT, "color": GOLD, "t": 0.02, "text": "THE FIVE", "off": (16, 30)},
            {"k": "pin", "at": SHELLEY_AT, "t": 0.2, "text": "SHELLEY · MAY 12"},
            {"k": "pin", "at": RIP_AT, "t": 0.45, "text": "RIPSLINGER · MAY 17"}],
            "notes": [("Positions schematic", 0.1)]}),
        ("23:53", {"k": "chips", "title": "HOW FAR BEYOND THE FIVE", "items": [("Shelley · 37.5 mi", ASF), ("Shelley · 21 mi", NARA), ("Ripslinger · +26 mi", ASF)],
                   "note": "The records do not agree"}),
        ("24:04", {"k": "map", "cam": WRECKV, "items": [
            {"k": "pin", "at": "wreck", "color": RED, "t": 0.02},
            {"k": "pin", "at": WORAVKA_AT, "t": 0.15, "text": "WORAVKA · AUG 1960 · ≈ 12 mi", "off": (-16, 30), "anchor": "end"}]}),
        ("24:12", {"k": "cards", "show": ["Vernon Moore"], "title": "NEVER FOUND"}),
    ],
    "S7.1": [
        ("24:21", {"k": "quote", "text": "a gross navigational error", "label": "The official verdict", "src": f"as quoted by {ASF}"}),
        ("24:41", {"k": "chain", "items": ["first mission", "dark night", "ADF not working", "330° misread", "coast unseen"], "fade_end": True}),
        ("25:06", {"k": "map", "cam": (21.2, 31.0, 1.4), "items": [
            {"k": "route", "pts": [(20.0, 33.6), "soluch", "wreck"], "t": 0.05, "d": 5.0},
            {"k": "pin", "at": "wreck", "color": RED, "t": 0.6}]}),
    ],
    "S7.2": [
        ("25:18", {"k": "photo", "img": "parts", "cap": "Parts were removed for other aircraft"}),
        ("25:33", {"k": "photo", "img": "aerial57"}),
        ("25:43", {"k": "photo", "img": "window", "cap": "Stained-glass window, Wheelus Air Base chapel"}),
        ("25:58", {"k": "map", "cam": (23.5, 29.5, 1.6), "items": [
            {"k": "pin", "at": "wreck", "color": RED, "t": 0.02},
            {"k": "route", "pts": ["wreck", "tobruk"], "t": 0.1, "d": 3.0, "color": GOLD},
            {"k": "pin", "at": "tobruk", "text": "TOBRUK · 1994", "t": 0.4}]}),
        ("26:08", {"k": "title", "style": "big", "text": "1943 → 1994", "sub": "51 YEARS IN THE DESERT"}),
        ("26:16", {"k": "map", "region": "lakes", "cam": (-87.5, 45.6, 2.3), "cam2": (-88.4, 47.0, 3.2), "items": [
            {"k": "pin", "at": "lake_linden", "text": "LAKE LINDEN, MICHIGAN", "t": 0.1}]}),
    ],
    "S7.3": [
        ("26:25", {"k": "cards"}),
        ("26:35", {"k": "cards", "groups": [["John Woravka"], FIVE, ["Guy Shelley", "Harold Ripslinger"], ["Vernon Moore"]],
                   "glabels": ["CAME DOWN ALONE", "STOPPED TOGETHER", "KEPT WALKING", "STILL OUT THERE"], "dim": ["Vernon Moore"], "compact": True}),
        ("26:55", {"k": "photo", "img": "nosewheel"}),
        ("27:03", {"k": "map", "cam": (21.6, 30.0, 1.15), "items": [
            {"k": "pin", "at": THOUGHT, "text": "WHERE THEY THOUGHT THEY WERE", "t": 0.05, "color": GOLD},
            {"k": "pin", "at": JUMP, "text": "WHERE THEY WERE", "t": 0.25, "color": RED}]}),
        ("27:12", {"k": "title", "style": "big", "text": "One question for the crew?", "sub": "TELL US IN THE COMMENTS"}),
        ("27:22", {"k": "illus", "name": "sky", "lights": True, "cap": "NEXT ON ICYFOX: FOO FIGHTERS", "mark": False}),
    ],
}
