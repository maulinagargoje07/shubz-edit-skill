import wave,struct,math,json
w=wave.open('audio/voice/enh_v3.wav');sr=w.getframerate();n=w.getnframes();s=struct.unpack('<%dh'%n,w.readframes(n))
hop=sr//100
db=[20*math.log10(math.sqrt(sum(v*v for v in s[i:i+hop])/hop)/32768+1e-12) for i in range(0,int(72*sr),hop)]
TH=-36; MIN=0.18; PAD=0.06
# first speech onset
start=2.62  # first real word (0.85-2.65 is a rooster crow, no speech)
END=71.14
runs=[];st=None
for i,v in enumerate(db):
    if v<TH:
        st=i if st is None else st
    else:
        if st is not None and (i-st)/100>=MIN: runs.append((st/100,i/100))
        st=None
cuts=[(31.40,36.88),(37.24,38.07)]  # off-script aside; rooster crow before 'jab'
for a,b in runs:
    if a>start and b<END and (b-PAD)-(a+PAD)>0.06: cuts.append((a+PAD,b-PAD))
cuts.sort()
keep=[];t=start
for a,b in cuts:
    if b<=t: continue
    if a>t: keep.append((round(t,3),round(a,3)))
    t=max(t,b)
keep.append((round(t,3),END))
keep=[k for k in keep if k[1]-k[0]>0.05]
print('start %.2f, %d segments, duration %.2f'%(start,len(keep),sum(b-a for a,b in keep)))
json.dump({'keep':keep},open('transcript/cuts_v3.json','w'))
fc=[]
for i,(a,b) in enumerate(keep):
    d=b-a
    fc.append(f"[0:v]trim={a}:{b},setpts=PTS-STARTPTS,fps=30,scale=1920:1080:flags=lanczos,split[s{i}][t{i}];[t{i}]lut3d=dl/luts/Honey_LUT.cube[g{i}];[g{i}][s{i}]blend=all_mode=normal:all_opacity=0.65,curves=master='0/0.06 0.25/0.35 0.5/0.61 0.75/0.83 1/1',eq=saturation=1.06[v{i}]")
    fc.append(f"[1:a]atrim={a}:{b},asetpts=PTS-STARTPTS,afade=t=in:d=0.006,afade=t=out:st={d-0.006:.3f}:d=0.006[a{i}]")
fc.append(''.join(f'[v{i}][a{i}]' for i in range(len(keep)))+f'concat=n={len(keep)}:v=1:a=1[v][ac];[ac]loudnorm=I=-15:TP=-1.5:LRA=7[a]')
open('transcript/cut_filter_v3.txt','w').write(';\n'.join(fc))
