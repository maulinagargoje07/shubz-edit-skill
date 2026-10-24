import wave,struct,math,json
w=wave.open('audio/rooster/raw16.wav');sr=w.getframerate();n=w.getnframes();s=struct.unpack('<%dh'%n,w.readframes(n))
N=1024;win=[0.5-0.5*math.cos(2*math.pi*i/(N-1)) for i in range(N)]
def mag(seg,f):
    k=2*math.cos(2*math.pi*f/sr);s1=s2=0.0
    for i,x in enumerate(seg):
        s0=x*win[i]+k*s1-s2;s2=s1;s1=s0
    return math.sqrt(max(s1*s1+s2*s2-k*s1*s2,0))
frames=[]
for a,b in [(0.7,2.8),(24.95,26.4),(37.15,38.6)]:
    t=a
    while t<b:
        i=int(t*sr);seg=s[i:i+N]
        fr=[1200+10*j for j in range(81)]
        m=[mag(seg,f) for f in fr];mx=max(m);fi=fr[m.index(mx)];med=sorted(m)[len(m)//2]+1e-9
        pk=20*math.log10(mx/med)
        # harmonic check: 3rd harmonic of f0=fi/2 should also peak
        h3=mag(seg,fi*1.5);h3n=(mag(seg,fi*1.5+70)+mag(seg,fi*1.5-70))/2+1e-9
        frames.append((round(t,3),fi,round(pk,1),round(20*math.log10(h3/h3n),1)))
        t+=0.05
crow=[f for f in frames if f[2]>=17 and f[3]>=6]
print(len(crow),'crow frames');print(' '.join(f'{t}:{f}' for t,f,p,h in crow))
# merge into segments, notch k*f0 (k=1..6) with frame-level enable windows
filt=[]
for t,f2,p,h in crow:
    f0=f2/2;a=max(0,t-0.02);b=t+N/sr+0.02
    for k in range(1,7):
        F=k*f0
        if F>7500: break
        filt.append(f"equalizer=f={F:.0f}:t=h:w={30+k*22}:g=-30:enable='between(t,{a:.3f},{b:.3f})'")
open('audio/rooster/notch.txt','w').write(','.join(filt))
json.dump(crow,open('audio/rooster/crow_frames.json','w'))
print(len(filt),'notch filters')
