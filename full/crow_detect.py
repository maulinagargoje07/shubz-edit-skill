import os,json
W,H=6000,700; F0,F1=600,4100; hz=(F1-F0)/(H-1)   # 5 Hz/row
def row(f): return int(round((F1-f)/hz))
res=[]
for i in range(11):
    p=f'full/det/c{i}.gray'
    if not os.path.exists(p): continue
    px=open(p,'rb').read(); dur=min(60,618.62-i*60)
    rows=range(row(2100),row(1450)+1)   # 1550-2050 Hz (2nd harmonic band)
    hits=[]
    for x in range(W):
        best=None
        for r in rows:
            v=px[r*W+x]
            if v<100: continue
            nb=max(px[(r-14)*W+x],px[(r+14)*W+x],px[(r-24)*W+x],px[(r+24)*W+x])  # +-70/120 Hz
            if v-nb>=20 and (best is None or v>best[1]): best=(r,v)
        hits.append(best)
    # runs: consecutive cols with hit rows within +-6 rows (30 Hz), allowing 3-col gaps
    x=0
    while x<W:
        if hits[x] is None: x+=1; continue
        start=x; last=x; r0=hits[x][0]; fs=[hits[x][0]]
        y=x+1
        while y<W and y-last<=4:
            if hits[y] and abs(hits[y][0]-r0)<=6: last=y; r0=hits[y][0]; fs.append(r0)
            y+=1
        if (last-start)>=18:
            t0=i*60+start*dur/W; t1=i*60+(last+1)*dur/W
            f=sorted(fs)[len(fs)//2]; res.append((round(t0,2),round(t1,2),round(F1-f*hz)))
        x=last+1
for r in res: print(r)
json.dump(res,open('full/det/crows_auto.json','w'))
