import json, re, subprocess
W_=json.load(open('transcript/words_v3.json')); CUTS=json.load(open('transcript/cutpoints_v3.json')); DUR=60.1
norm=lambda x: re.sub(r"[^a-z0-9']","",x.lower())
def W(word,n=1):
    k=0
    for w in W_:
        if norm(w[0])==word:
            k+=1
            if k==n: return w[1]
    raise SystemExit('missing '+word)
def WE(word,n=1):
    k=0
    for w in W_:
        if norm(w[0])==word:
            k+=1
            if k==n: return w[2]
c1out=W('iske')-0.05; c2out=W('iss')-0.05; c6in=W('aapko',3)-0.3; c7in=W('main',2)-0.05; c8in=W('because')-0.08; c9in=W("beginner's")-0.3; c10in=W('you',3)-0.12
SFX=[(0.0,'whoosh-short',.3),(W('one'),'impact-bass-1',.26),(W('successful'),'sparkle',.2),
(c1out,'whoosh-short',.32),(W('2'),'ping',.2),(W('3'),'ping',.2),(W('6'),'ping',.2),
(c2out,'whoosh-short',.32),(W('preparation'),'sparkle',.2),(W('proper')-0.25,'whoosh-short',.26),
(W('entry'),'click',.42),(W('exit'),'click',.42),(W('execution'),'click',.42),(W("let's"),'whoosh',.3),
(c6in,'whoosh-short',.32),(W('ek',3),'pop',.28),(W('important'),'sparkle',.18),(c7in,'whoosh',.36),(W('tak'),'pop',.28),
(W('thousands'),'impact-bass-1',.32),(c8in,'whoosh',.3),(W('aaj'),'click-soft',.38),(W('kal'),'click-soft',.38),(W('mahine',2)-0.1,'click-soft',.38),
(W('nahi',2)-0.55,'error',.2),(W('nahi',2),'pop',.26),(c9in-0.1,'whoosh-short',.3),(W("beginner's"),'sparkle',.2),(W('andar')-0.5,'pop',.26),
(c10in,'whoosh',.36),(W('successful',3),'ping',.18),(W('downfall'),'impact-bass-1',.36)]
def dur(f): return float(subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',f],capture_output=True,text=True).stdout)
tags=[];tracks={}
for i,(t,f,v) in enumerate(sorted(SFX)):
    t=round(max(0,t),2); d=min(dur(f'public/audio/{f}.mp3'),DUR-t); tr=10
    while tracks.get(tr,-1)>t: tr+=1
    tracks[tr]=t+d
    tags.append(f'      <audio id="sfx{i:02d}" src="audio/{f}.mp3" data-start="{t}" data-duration="{d:.2f}" data-volume="{v}" data-track-index="{tr}"></audio>')
s=open('transcript/index.template.html').read()
a=s.index('          // ── Zoom cuts'); b=s.index('          window.__timelines = window.__timelines')
s=s[:a]+open('transcript/timeline_v2.js').read()+'\n'+s[b:]
s=s.replace('DUR = 62.6','DUR = 60.1').replace('data-duration="62.6"','data-duration="60.1"')
s=s.replace('__WORDS__',json.dumps(W_,ensure_ascii=False,separators=(',',':'))).replace('__CUTS__',json.dumps(CUTS)).replace('__SFX__','\n'.join(tags))
s=s.replace('(Mixkit "Deep Urban", pre-levelled to ~-29 LUFS)','(Mixkit "Drawing the Sky" by Eugenio Mininni, sidechain-ducked under the voice, ~-29 LUFS)')

# card-host visibility windows derived from the same word cues as timeline_v2.js
WIN={'c1':(0,c1out),'c2':(c1out,c2out),'c34':(c2out,WE('sath')+0.25),'c5':(W("let's")-0.1,WE('guys',2)+0.15),
     'c6':(c6in,W('main',2)-0.08),'c7':(c7in,c8in+0.35),'c8':(c8in,W("beginner's")-0.4),'c9':(c9in,c10in),'c10':(c10in,DUR)}
for cid,(a,b) in WIN.items():
    s,nsub=re.subn(r'(id="%s" data-start=")[0-9.]+(" data-duration=")[0-9.]+(")'%cid, lambda m: f'{m.group(1)}{a:.3f}{m.group(2)}{b-a:.3f}{m.group(3)}', s)
    assert nsub==1, cid
    print(cid, round(a,2), round(b,2))
open('public/index.html','w').write(s)
print(len(tags),'sfx; tracks',sorted(tracks))
