import wave,struct,math,json
w=wave.open('full/enh16_full.wav');sr=w.getframerate();n=w.getnframes();s=struct.unpack('<%dh'%n,w.readframes(n))
hop=sr//100
db=[20*math.log10(math.sqrt(sum(v*v for v in s[i:i+hop])/hop)/32768+1e-12) for i in range(0,n-hop,hop)]
TH=-36;MIN=0.18;PAD=0.06;START=71.14;END=614.62
runs=[];st=None
for i,v in enumerate(db):
    if v<TH: st=i if st is None else st
    else:
        if st is not None and (i-st)/100>=MIN: runs.append((st/100,i/100))
        st=None
manual=[(228.62,235.72)]
cuts=sorted(manual+[(a+PAD,b-PAD) for a,b in runs if a>START and b<END and (b-PAD)-(a+PAD)>0.06])
keep=[];t=START
for a,b in cuts:
    if b<=t: continue
    if a>t: keep.append((round(t,3),round(a,3)))
    t=max(t,b)
keep.append((round(t,3),END)); keep=[k for k in keep if k[1]-k[0]>0.05]
# part boundaries: nearest cut gap to each target raw time
targets=[133.6,201.0,265.6,354.0,437.5,499.0,547.7]
bounds=[]
for T in targets:
    best=min(range(len(keep)-1),key=lambda i:abs(keep[i][1]-T)); bounds.append(best)
parts=[];prev=0
for bi in bounds+[len(keep)-1]:
    parts.append(keep[prev:bi+1]); prev=bi+1
tot=0
for i,p in enumerate(parts):
    d=sum(b-a for a,b in p); tot+=d
    print(f'P{i+2}: raw {p[0][0]:.2f}-{p[-1][1]:.2f}  {len(p)} segs  {d:.1f}s')
print('total after part1: %.1f s'%tot)
json.dump(parts,open('parts/parts_keep.json','w'))

# --- v2: split at sentence starts (seamless, contiguous raw) ---
B=[133.65,200.95,265.65,354.05,437.55,499.05,534.25]
def quiet(T):
    lo=int((T-0.3)*100);hi=int((T+0.3)*100)
    return min(range(lo,hi),key=lambda i:db[i])/100
Bq=[quiet(T) for T in B]
flat=[]
for a,b in keep:
    pieces=[(a,b)]
    for q in Bq:
        nxt=[]
        for x,y in pieces:
            if x<q<y: nxt+= [(x,q),(q,y)]
            else: nxt.append((x,y))
        pieces=nxt
    flat+=pieces
parts=[[] for _ in range(len(Bq)+1)]
for a,b in flat:
    k=sum(1 for q in Bq if a>=q-1e-6)
    parts[k].append((round(a,3),round(b,3)))
tot=0
for i,p in enumerate(parts):
    d=sum(b-a for a,b in p); tot+=d
    print(f'P{i+2}: raw {p[0][0]:.2f}-{p[-1][1]:.2f}  {len(p)} segs  {d:.1f}s')
print('total %.1f'%tot)
json.dump(parts,open('parts/parts_keep.json','w'))
