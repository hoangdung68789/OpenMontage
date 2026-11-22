import json, subprocess, sys, time, statistics as st
from concurrent.futures import ThreadPoolExecutor
OUT=sys.argv[1]
QUERIES=["ancient civilizations documentary","greek mythology explained full story","norse mythology full story",
"ancient egypt documentary","fall of rome documentary","mesopotamia sumer history documentary",
"ancient history for sleep","the entire history of ancient","ancient mythology documentary","bronze age collapse documentary",
"persian empire documentary","aztec maya history documentary"]
def ytdlp(args,timeout=240):
    try:
        r=subprocess.run(["yt-dlp","-J","--flat-playlist","--no-warnings"]+args,capture_output=True,text=True,timeout=timeout)
        return json.loads(r.stdout) if r.stdout.strip() else None
    except Exception: return None
def search(q):
    d=ytdlp([f"ytsearch40:{q}"]); return q,[e for e in (d or {}).get("entries",[]) or [] if e]
with ThreadPoolExecutor(4) as ex: res=dict(ex.map(search,QUERIES))
chans={}
for q,ents in res.items():
    for e in ents:
        if not e.get("channel_id") or (e.get("duration") or 0)<480: continue
        c=chans.setdefault(e["channel_id"],{"channel":e.get("channel"),"hits":0,"max_views":0,"queries":set()})
        c["hits"]+=1; c["max_views"]=max(c["max_views"],e.get("view_count") or 0); c["queries"].add(q)
# rank: appear in >=2 queries or big views
ranked=sorted(chans.items(),key=lambda kv:(-len(kv[1]["queries"]),-kv[1]["max_views"]))[:30]
print("channels found",len(chans),"analysed",len(ranked),flush=True)
def chan(cid):
    d=ytdlp(["--playlist-end","60","--extractor-args","youtubetab:approximate_date",f"https://www.youtube.com/channel/{cid}/videos"])
    if not d: return cid,None
    ents=[e for e in d.get("entries") or [] if e]
    return cid,{"channel":d.get("channel"),"subs":d.get("channel_follower_count"),
      "videos":[{"id":e.get("id"),"title":e.get("title"),"views":e.get("view_count"),"dur":e.get("duration"),"ts":e.get("timestamp")} for e in ents]}
with ThreadPoolExecutor(4) as ex: data=dict(ex.map(chan,[c for c,_ in ranked]))
json.dump({"queries":QUERIES,"channels":data,"search_meta":{k:{**v,"queries":sorted(v["queries"])} for k,v in ranked}},open(f"{OUT}/deep.json","w"),indent=1)
print("done",sum(1 for v in data.values() if v))
