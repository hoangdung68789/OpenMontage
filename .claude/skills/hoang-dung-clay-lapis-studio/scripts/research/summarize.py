import json, sys, statistics as st
D = sys.argv[1]
S = json.load(open(f"{D}/search.json")); C = json.load(open(f"{D}/channels.json"))
def f(n):
    if n is None: return "-"
    n=float(n)
    return f"{n/1e6:.1f}M" if n>=1e6 else (f"{n/1e3:.0f}K" if n>=1e3 else f"{n:.0f}")
rows=[]
for niche, chans in S.items():
    cs=[(cid,C.get(cid)) for cid in chans if C.get(cid)]
    young=[c for _,c in cs if c["age_months"] is not None and c["age_months"]<=24]
    med10=[c["med10"] for _,c in cs if c["med10"] is not None]
    viral=[c for _,c in cs if c["viral_last30"]>0]
    active=[c for _,c in cs if c["uploads_365d"]>0]
    print(f"\n=== {niche}: {len(cs)} kênh | trung vị med10 {f(st.median(med10) if med10 else None)} | kênh trẻ ≤24 tháng: {len(young)} | kênh có video ≥5x TB10 (30 video gần nhất): {len(viral)} | kênh có đăng trong 365 ngày: {len(active)} | thời lượng TV {st.median([c['med_dur_min'] for _,c in cs if c['med_dur_min']]) if cs else '-'} phút")
    for cid,c in sorted(cs,key=lambda x:-(x[1]['subs'] or 0)):
        print(f"  {c['channel'][:28]:28} subs {f(c['subs']):>6} | tuổi {('>'+str(c['n_listed'])+'vid') if c['capped'] else str(c['age_months'])+'th':>8} | med10 {f(c['med10']):>6} | avg10 {f(c['avg10']):>6} | 365d: {c['uploads_365d']:>3} vid, TV {f(c['med_views_365d']):>6} | viral30 {c['viral_last30']} | dur {c['med_dur_min']}p | {cid}")
