import json, subprocess, sys, time, statistics as st
from concurrent.futures import ThreadPoolExecutor
OUT = sys.argv[1]
NICHES = {
 "history_doc": ["history documentary full", "entire history explained documentary"],
 "mythology_ancient": ["mythology explained documentary", "ancient civilizations documentary"],
 "geography": ["geography explained why country", "why is this country so map explained"],
 "space_science": ["space documentary universe explained", "science explained documentary"],
 "business_stories": ["rise and fall of company documentary", "business case study documentary how company"],
 "megaprojects": ["megaprojects engineering how was built", "how was it built engineering documentary"],
 "history_mysteries": ["unsolved history mysteries documentary", "historical mysteries explained"],
}
def ytdlp(args, timeout=180):
    try:
        r = subprocess.run(["yt-dlp","-J","--flat-playlist","--no-warnings"]+args, capture_output=True, text=True, timeout=timeout)
        return json.loads(r.stdout) if r.stdout.strip() else None
    except Exception as e:
        return None
search = {}
for niche, qs in NICHES.items():
    chans = {}
    for q in qs:
        d = ytdlp([f"ytsearch40:{q}"])
        for e in (d or {}).get("entries", []) or []:
            if not e or not e.get("channel_id") or (e.get("duration") or 0) < 480: continue
            c = chans.setdefault(e["channel_id"], {"channel": e.get("channel"), "hits":0, "max_views":0})
            c["hits"] += 1; c["max_views"] = max(c["max_views"], e.get("view_count") or 0)
    top = sorted(chans.items(), key=lambda kv: -kv[1]["max_views"])[:10]
    search[niche] = dict(top)
    print(niche, "channels:", len(chans), "kept:", len(top), flush=True)
json.dump(search, open(f"{OUT}/search.json","w"), indent=1)
NOW = time.time()
def chan_stats(cid):
    d = ytdlp(["--playlist-end","120","--extractor-args","youtubetab:approximate_date", f"https://www.youtube.com/channel/{cid}/videos"], timeout=240)
    if not d: return cid, None
    ents = [e for e in d.get("entries") or [] if e]
    v = [e.get("view_count") for e in ents if e.get("view_count") is not None]
    ts = [e.get("timestamp") for e in ents if e.get("timestamp")]
    last10 = [e.get("view_count") or 0 for e in ents[:10]]
    last30 = ents[:30]
    avg10 = sum(last10)/len(last10) if last10 else 0
    viral30 = [e for e in last30 if avg10 and (e.get("view_count") or 0) >= 5*avg10]
    yr = [e for e in ents if e.get("timestamp") and NOW - e["timestamp"] <= 365*86400]
    capped = len(ents) >= 120
    return cid, {
        "channel": d.get("channel"), "subs": d.get("channel_follower_count"),
        "n_listed": len(ents), "capped": capped,
        "age_months": None if capped or not ts else round((NOW-min(ts))/86400/30.4,1),
        "med10": st.median(last10) if last10 else None, "avg10": round(avg10),
        "med30": st.median([e.get("view_count") or 0 for e in last30]) if last30 else None,
        "uploads_365d": len(yr), "med_views_365d": st.median([e.get("view_count") or 0 for e in yr]) if yr else None,
        "viral_last30": len(viral30), "max_last30": max([e.get("view_count") or 0 for e in last30] or [0]),
        "med_dur_min": round(st.median([e.get("duration") or 0 for e in last30])/60,1) if last30 else None,
    }
ids = sorted({cid for n in search.values() for cid in n})
print("total channels:", len(ids), flush=True)
with ThreadPoolExecutor(4) as ex:
    stats = dict(ex.map(chan_stats, ids))
json.dump(stats, open(f"{OUT}/channels.json","w"), indent=1)
print("done", sum(1 for s in stats.values() if s), "ok of", len(stats))
