import json, os, sys, shutil, subprocess, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gen, importlib; from storyboards import SB
ROOT = os.path.dirname(os.path.abspath(__file__)); PROJ = os.path.dirname(ROOT)
FIX = {'bohot':'bahut','boht':'bahut','bot':'bahut','bhoot':'bahut','sika':'sikhaya','sika,':'sikhaya,','treads':'trades','treads.':'trades.','Ujha':'Mujhe','Uskele':'Uske liye','Khudkele':'Khud ke liye','koro.':'karo.','Dehko':'Dekho','fayta':'fayda','taunga':'bataunga','zaadi':'zyada','wada':'bada','mai':'main','Mai':'Main','pochoge,':'pahunchoge,','loko,':'logo,'}
parts = json.load(open(os.path.join(ROOT, 'parts_keep.json')))
def dur(p): return float(subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',p],capture_output=True,text=True).stdout)
which = [int(a) for a in sys.argv[1:]] or list(range(2, 10))
for k in which:
    keep = parts[k-2]
    words = json.load(open(os.path.join(ROOT, f'p{k}_words_raw.json')))
    for x in words:
        if x[0] in FIX: x[0] = FIX[x[0]]
        if x[0].lower() in ('maine','maine,') and k == 2 and x[1] < 6: x[0] = 'mahine'
    if k == 8: words = [x for x in words if not (x[1] > 29.5 and x[0].lower().startswith(('thank','you')))]
    vdur = dur(os.path.join(ROOT, f'p{k}_voice.wav'))
    D = vdur + (3.0 if k == 9 else 0)
    acc = 0; cuts = []
    for a, b in keep: acc += b - a; cuts.append(round(acc, 2))
    cards = json.loads(json.dumps(SB[k]))
    for c in cards:
        for key in ('t0', 't1'):
            if c.get(key) == 'END': c[key] = round(vdur, 3)
            if c.get(key) == 'END+': c[key] = round(D, 3)
    pub = os.path.join(ROOT, f'p{k}', 'public'); os.makedirs(pub, exist_ok=True)
    for d in ('fonts', 'img', 'vendor'):
        if not os.path.exists(os.path.join(pub, d)): shutil.copytree(os.path.join(PROJ, 'public', d), os.path.join(pub, d))
    os.makedirs(os.path.join(pub, 'audio'), exist_ok=True)
    for f in os.listdir(os.path.join(PROJ, 'public', 'audio')):
        if f.endswith('.mp3'): shutil.copy(os.path.join(PROJ, 'public', 'audio', f), os.path.join(pub, 'audio', f))
    gen.SFX_DUR.clear(); gen.load_sfx_durations(os.path.join(pub, 'audio'))
    P = dict(name=f'p{k}', words=words, cuts=cuts[:-1], dur=D, video_dur=vdur, cards=cards)
    open(os.path.join(pub, 'index.html'), 'w').write(gen.build(P))
    print(f'p{k}: {len(cards)} cards, dur {D:.2f}s')
