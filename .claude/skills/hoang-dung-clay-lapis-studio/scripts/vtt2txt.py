import re,sys
# Gộp phụ đề tự động (lặp dòng) thành đoạn theo mốc 30s
for f in sys.argv[1:]:
    t=open(f,encoding='utf-8').read()
    out=[];seen=set();cur=None
    for blk in t.split('\n\n'):
        m=re.search(r'(\d+):(\d+):(\d+)\.\d+ -->',blk)
        if not m: continue
        s=int(m[1])*3600+int(m[2])*60+int(m[3])
        for ln in blk.split('\n')[1:]:
            ln=re.sub(r'<[^>]+>','',ln).strip()
            if ln and ln not in seen and '-->' not in ln:
                seen.add(ln); b=s//30
                if b!=cur: out.append(f"\n[{s//60}:{s%60:02d}] "); cur=b
                out.append(ln+' ')
    open(f.replace('.en.vtt','.txt'),'w',encoding='utf-8').write(''.join(out))
    print(f, len(''.join(out).split()),'words')
