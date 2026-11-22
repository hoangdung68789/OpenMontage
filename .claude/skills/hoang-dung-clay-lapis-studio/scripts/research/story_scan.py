"""Quét nhiều nhóm chủ đề kể chuyện, so sánh hiệu quả (dùng yt-dlp chế độ flat).
python3 story_scan.py <thư_mục_kết_quả>   (sửa NICHES bên dưới)
Đầu ra: <dir>/story_scan.json + bảng tóm tắt in ra màn hình.
"""
import json, subprocess, sys, time, statistics as st
from concurrent.futures import ThreadPoolExecutor
OUT = sys.argv[1]
NICHES = {
 "ancient_myth": ["ancient civilizations documentary", "mythology full story documentary"],
 "war_history": ["the untold story war history documentary", "battle history documentary story"],
 "medieval_empires": ["medieval history documentary story", "rise and fall of empire documentary"],
 "exploration_survival": ["survival story documentary expedition", "lost expedition documentary"],
 "heists_scams": ["greatest heist true story documentary", "con artist scam true story documentary"],
 "espionage_coldwar": ["spy true story documentary", "cold war story documentary"],
 "disasters_engineering": ["engineering disaster documentary", "shipwreck disaster story documentary"],
 "business_stories": ["rise and fall of company documentary", "how a company failed story"],
 "biographies": ["biography documentary life story", "the man who changed history documentary"],
 "history_mysteries": ["unsolved mystery history documentary", "strange disappearance documentary"],
 "space_missions": ["space mission story documentary apollo", "space disaster story documentary"],
 "true_crime": ["true crime documentary case story", "infamous criminal story documentary"],
}
def ytdlp(args, timeout=240):
    try:
        r = subprocess.run(["yt-dlp", "-J", "--flat-playlist", "--no-warnings"] + args, capture_output=True, text=True, timeout=timeout)
        return json.loads(r.stdout) if r.stdout.strip() else None
    except Exception:
        return None
def search(q):
    d = ytdlp([f"ytsearch40:{q}"]); return q, [e for e in (d or {}).get("entries", []) or [] if e]
allq = [q for qs in NICHES.values() for q in qs]
with ThreadPoolExecutor(4) as ex: res = dict(ex.map(search, allq))
niche_ch = {}
for n, qs in NICHES.items():
    ch = {}
    for q in qs:
        for e in res.get(q, []):
            if not e.get("channel_id") or (e.get("duration") or 0) < 480: continue
            c = ch.setdefault(e["channel_id"], {"channel": e.get("channel"), "max": 0})
            c["max"] = max(c["max"], e.get("view_count") or 0)
    niche_ch[n] = [cid for cid, _ in sorted(ch.items(), key=lambda kv: -kv[1]["max"])[:10]]
NOW = time.time()
def chan(cid):
    d = ytdlp(["--playlist-end", "60", "--extractor-args", "youtubetab:approximate_date", f"https://www.youtube.com/channel/{cid}/videos"])
    if not d: return cid, None
    ents = [e for e in d.get("entries") or [] if e]
    return cid, {"channel": d.get("channel"), "subs": d.get("channel_follower_count"),
                 "videos": [{"id": e.get("id"), "title": e.get("title"), "views": e.get("view_count"), "dur": e.get("duration"), "ts": e.get("timestamp")} for e in ents]}
ids = sorted({c for v in niche_ch.values() for c in v})
with ThreadPoolExecutor(4) as ex: data = dict(ex.map(chan, ids))
json.dump({"niches": NICHES, "niche_channels": niche_ch, "channels": data, "scanned_at": time.strftime("%Y-%m-%d")}, open(f"{OUT}/story_scan.json", "w"), indent=1)
def f(n): return "-" if n is None else (f"{n/1e6:.1f}M" if n >= 1e6 else f"{n/1e3:.0f}K" if n >= 1e3 else f"{n:.0f}")
rows = []
for n, cids in niche_ch.items():
    meds, scores, young, viral_ch, durs, upy = [], [], [], 0, [], []
    for cid in cids:
        c = data.get(cid)
        if not c: continue
        vs = [v for v in c["videos"] if v["views"] is not None and (v["dur"] or 0) >= 480]
        if len(vs) < 8: continue
        base = st.median([v["views"] for v in vs[:30]]) or 1
        avg10 = sum(v["views"] for v in vs[:10]) / min(10, len(vs))
        meds.append(st.median([v["views"] for v in vs[:10]]))
        scores += [v["views"] / base for v in vs[:30]]
        viral_ch += any(v["views"] >= 5 * avg10 for v in vs[:30])
        durs += [v["dur"] / 60 for v in vs[:30]]
        ts = [v["ts"] for v in c["videos"] if v["ts"]]
        upy.append(sum(1 for t in ts if NOW - t <= 365 * 86400))
        if len(c["videos"]) < 60 and ts and (NOW - min(ts)) / 86400 / 30.4 <= 24:
            young.append(f'{c["channel"][:18]}({f(c["subs"])} sub, TV {f(meds[-1])})')
    if not meds: continue
    rows.append((n, len(meds), st.median(meds), sum(s >= 3 for s in scores) / len(scores), viral_ch, st.median(durs), st.median(upy), young))
print(f'{"nhóm":22} kênh  TV-view10  %vid>=3x  kênh-viral  phút  vid/năm  kênh trẻ (<=24 tháng)')
for r in sorted(rows, key=lambda r: -r[2]):
    print(f'{r[0]:22} {r[1]:>4}  {f(r[2]):>9}  {r[3]*100:7.0f}%  {r[4]:>5}/{r[1]:<4} {r[5]:5.0f}  {r[6]:7.0f}  {"; ".join(r[7]) or "-"}')
