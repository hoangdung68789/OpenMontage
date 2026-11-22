import json,sys,re,time,statistics as st
D=json.load(open(sys.argv[1])); NOW=time.time()
def f(n):
    if n is None: return "-"
    return f"{n/1e6:.1f}M" if n>=1e6 else (f"{n/1e3:.0f}K" if n>=1e3 else f"{n:.0f}")
allv=[]; rows=[]
for cid,c in D["channels"].items():
    if not c: continue
    vs=[v for v in c["videos"] if v["views"] is not None and (v["dur"] or 0)>=480]
    if len(vs)<8: continue
    base=st.median([v["views"] for v in vs[:30]]) or 1
    avg10=sum(v["views"] for v in vs[:10])/min(10,len(vs))
    ts=[v["ts"] for v in c["videos"] if v["ts"]]
    age=None if len(c["videos"])>=60 or not ts else round((NOW-min(ts))/86400/365,1)
    yr=[v for v in vs if v["ts"] and NOW-v["ts"]<=365*86400]
    out=[v for v in vs[:30] if avg10 and v["views"]>=5*avg10]
    rows.append((c["channel"],c["subs"],age,len(yr),f(base),len(out),round(st.median([v['dur'] for v in vs[:30]])/60),"https://www.youtube.com/channel/"+cid))
    for v in vs: allv.append({**v,"ch":c["channel"],"score":v["views"]/base,"subs":c["subs"]})
print("=== KÊNH (sắp theo sub)")
for r in sorted(rows,key=lambda r:-(r[1] or 0)):
    print(f"{r[0][:26]:26} sub {f(r[1]):>6} | tuổi {('>60vid' if r[2] is None else str(r[2])+'n'):>7} | video/365d {r[3]:>3} | TV30 {r[4]:>6} | ≥5xTB10 {r[5]} | dur {r[6]}p | {r[7]}")
print("\n=== THỜI LƯỢNG vs điểm (views / trung vị 30 video của chính kênh)")
for lo,hi,lab in [(480,1200,"8-20p"),(1200,3600,"20-60p"),(3600,7200,"60-120p"),(7200,99999,"120p+")]:
    s=[v["score"] for v in allv if lo<=(v["dur"] or 0)<hi]
    if s: print(f"{lab:8} n={len(s):4} | điểm trung vị {st.median(s):.2f} | tỉ lệ video ≥3x: {sum(x>=3 for x in s)/len(s):.0%}")
print("\n=== CHỦ ĐỀ / MẪU TIÊU ĐỀ (n, điểm trung vị, tỉ lệ ≥3x)")
pats={"Egypt":r"egypt|pharaoh|pyramid","Rome/Roman":r"\brom(e|an)","Greek myth/Greece":r"greek|greece|zeus|odyss|troy|sparta|athen","Norse/Viking":r"norse|viking|odin|thor\b","Mesopotamia/Sumer/Babylon":r"mesopotam|sumer|babylon|akkad|assyri","Persia":r"persia","Aztec/Maya/Inca":r"aztec|maya|inca","China":r"china|chinese","Bible/biblical":r"bible|biblical|jesus|israel","Mystery/unexplained":r"myster|unexplain|nobody|can't explain|secret|hidden|lost",
"'ENTIRE/Complete/Full'":r"entire|complete|full story|whole","'Explained'":r"explained","'Sleep'":r"sleep","Số trong tiêu đề":r"\d","'No AI'":r"no a-?i|no a-eye"}
for k,p in pats.items():
    s=[v["score"] for v in allv if re.search(p,v["title"] or "",re.I)]
    if len(s)>=5: print(f"{k:28} n={len(s):4} | {st.median(s):.2f} | {sum(x>=3 for x in s)/len(s):.0%}")
print("\n=== TOP 15 VIDEO VƯỢT TRỘI (điểm cao nhất, views ≥100K)")
for v in sorted([v for v in allv if v["views"]>=100000],key=lambda v:-v["score"])[:15]:
    print(f"{v['score']:5.1f}x | {f(v['views']):>6} | {round(v['dur']/60):>3}p | {v['ch'][:18]:18} | {v['title'][:85]} | {v['id']}")
json.dump(sorted([v for v in allv if v["views"]>=100000],key=lambda v:-v["score"])[:15],open(sys.argv[1].replace('deep.json','top.json'),'w'))
