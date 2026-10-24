import wave,struct,math
w=wave.open('full/raw16_full.wav');sr=w.getframerate();n=w.getnframes();s=struct.unpack('<%dh'%n,w.readframes(n))
N=1024;win=[0.5-0.5*math.cos(2*math.pi*i/(N-1)) for i in range(N)]
def mag(seg,f):
    k=2*math.cos(2*math.pi*f/sr);s1=s2=0.0
    for i,x in enumerate(seg):
        s0=x*win[i]+k*s1-s2;s2=s1;s1=s0
    return math.sqrt(max(s1*s1+s2*s2-k*s1*s2,0))
WINS=[(72.65,73.2),(102.3,104.2),(270.7,272.35),(294.3,295.0),(310.9,311.9),(337.55,339.4),(424.1,425.7)]
filt=[];step=0.04;log=[]
for a,b in WINS:
    t=a;last=None
    while t<b:
        i=int(t*sr);seg=s[i:i+N]
        fr=[1550+10*j for j in range(46)]
        m=[mag(seg,f) for f in fr];mx=max(m);fi=fr[m.index(mx)]
        nb=(mag(seg,fi+70)+mag(seg,fi-70))/2+1e-9
        iso=20*math.log10(mx/nb)
        if iso>=9: last=fi
        f2=last if last else fi
        log.append((round(t,2),fi,round(iso,1)))
        if last:
            e=f"enable='between(t,{t-0.01:.3f},{t+step+0.01:.3f})'"
            for F,wd in ((f2/2,50),(f2,100),(f2*1.5,130),(f2*2,160),(f2*2.5,180),(f2*3,200)):
                filt.append(f"equalizer=f={F:.0f}:t=h:w={wd}:g=-28:{e}")
        t+=step
open('full/notch_full.txt','w').write(','.join(filt))
print(len(filt),'notch filters')
