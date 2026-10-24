#!/usr/bin/env python3
"""$hubzTrader part generator: storyboard (python dict) -> HyperFrames composition HTML.
Same look as the approved C9010 first minute: black + gold cards, tasteful 3D, gold-box karaoke
captions, face-safe framing engine with zoom cuts, word-anchored SFX. Music is mixed globally later."""
import json, re, subprocess, os, sys, html

ROOT = os.path.dirname(os.path.abspath(__file__))
BASE_CSS = open(os.path.join(ROOT, 'base.css')).read()

EXTRA_CSS = r"""
.card-host { color: var(--fg); }
.g-card { position:absolute; color:var(--fg); background:linear-gradient(180deg,#16171b,#0a0a0a); border:1px solid var(--line); border-radius:18px; box-shadow:var(--shadow); overflow:hidden; padding:40px 44px; }
.g-card::before { content:""; position:absolute; left:0; right:0; top:0; height:2px; background:linear-gradient(90deg,rgba(212,175,55,0),#d4af37 35%,#f3d675 72%,rgba(255,247,220,0)); }
.g-L { left:48px; top:260px; width:660px; transform-origin:left center; }
.g-R { left:1212px; top:200px; width:660px; transform-origin:right center; }
.g-S { left:80px; top:170px; width:800px; }
.g-h2 { margin:18px 0 0; font-size:52px; line-height:1.03; }
.g-h2.sm { font-size:44px; }
.g-line { display:block; }
.g-sub { margin-top:20px; font-size:25px; color:var(--cream); line-height:1.3; }
.g-sub b { color:var(--gold-hi); }
.g-row { position:relative; display:flex; align-items:center; gap:18px; padding:16px 20px; border-radius:14px; background:#0b0b0b; border:1px solid #23242a; margin-top:12px; font-size:25px; font-weight:700; color:var(--cream); transform-origin:50% 0%; }
.g-row .ic { width:42px; height:42px; border-radius:11px; display:grid; place-items:center; background:rgba(212,175,55,.12); color:var(--gold-hi); font-family:"Plus Jakarta Sans",sans-serif; font-weight:800; font-size:19px; flex:none; }
.g-row .mk { margin-left:auto; width:40px; height:40px; border-radius:50%; display:grid; place-items:center; font-size:21px; font-weight:800; flex:none; }
.g-row .mk.x { background:rgba(239,68,68,.14); color:var(--red); }
.g-row .mk.ok { background:rgba(212,175,55,.16); color:var(--gold-hi); }
.g-row .strike { position:absolute; left:80px; top:50%; height:3px; width:0; background:var(--red); border-radius:2px; }
.g-verdict { margin-top:20px; display:inline-flex; padding:14px 26px; border-radius:999px; background:var(--gold-grad); color:#050505; font-family:"Plus Jakarta Sans",sans-serif; font-size:22px; font-weight:800; letter-spacing:.04em; text-transform:uppercase; }
.g-brow { margin-top:24px; }
.g-brow .top { display:flex; justify-content:space-between; align-items:baseline; font-family:"Plus Jakarta Sans",sans-serif; font-size:28px; font-weight:800; margin-bottom:10px; }
.g-brow .top span:last-child { font-family:"Inter",sans-serif; font-size:16px; font-weight:400; color:var(--muted); }
.g-track { height:14px; border-radius:7px; background:#1b1c24; overflow:hidden; }
.g-bar { height:100%; width:0; border-radius:7px; background:var(--gold-grad); box-shadow:0 0 18px rgba(212,175,55,.35); }
.g-flow { position:relative; margin-top:34px; height:190px; perspective:900px; }
.g-flow .lbg { position:absolute; left:60px; right:60px; top:56px; height:3px; background:#24252c; border-radius:2px; }
.g-flow .ln { position:absolute; left:60px; top:56px; height:3px; width:0; background:var(--gold-grad); border-radius:2px; }
.g-step { position:absolute; top:0; width:140px; text-align:center; }
.g-step .n { margin:0 auto; width:112px; height:112px; border-radius:22px; background:#0b0b0b; border:1px solid #2a2b31; display:grid; place-items:center; color:#5d5f68; font-family:"Plus Jakarta Sans",sans-serif; font-weight:800; font-size:38px; }
.g-step .lbl { margin-top:14px; font-family:"Plus Jakarta Sans",sans-serif; font-size:17px; font-weight:800; letter-spacing:.04em; text-transform:uppercase; color:var(--cream); line-height:1.15; }
.g-step.on .n { border-color:transparent; background:var(--gold-grad); color:#050505; box-shadow:0 14px 36px rgba(212,175,55,.35); }
.g-chips { margin-top:22px; display:flex; flex-wrap:wrap; gap:12px; }
.g-chip { display:inline-flex; align-items:center; gap:10px; padding:12px 20px; border-radius:999px; background:rgba(212,175,55,.08); border:1px solid var(--line); font-size:22px; font-weight:700; color:var(--cream); }
.g-chip i { width:9px; height:9px; border-radius:50%; background:var(--gold); display:inline-block; }
.g-chip.hot { background:var(--gold-grad); color:#050505; border-color:transparent; }
.g-chip.hot i { background:#050505; }
.g-sec { width:100%; margin-top:18px; font-family:"Plus Jakarta Sans",sans-serif; font-size:15px; font-weight:700; letter-spacing:.2em; text-transform:uppercase; color:var(--muted); }
.g-pill { position:absolute; left:50%; top:780px; transform:translateX(-50%); display:flex; align-items:center; gap:14px; padding:16px 30px; background:var(--gold-grad); color:#050505; border-radius:999px; box-shadow:var(--shadow); font-family:"Plus Jakarta Sans",sans-serif; font-size:24px; font-weight:800; letter-spacing:.06em; text-transform:uppercase; white-space:nowrap; }
.g-full { position:absolute; inset:0; }
.g-center { position:absolute; left:160px; right:160px; top:0; bottom:200px; display:flex; flex-direction:column; align-items:center; justify-content:center; text-align:center; }
.g-big { font-size:96px; line-height:0.98; margin-top:22px; }
.g-big.md { font-size:78px; }
.g-bsub { margin-top:26px; font-size:34px; color:var(--cream); font-weight:700; }
.g-num3d { position:relative; font-family:"Plus Jakarta Sans",sans-serif; font-weight:800; line-height:0.85; font-size:220px; margin-bottom:6px; }
.g-num3d .back { position:absolute; left:0; top:0; color:#4a3810; text-shadow:1px 1px 0 #5a4314,2px 2px 0 #5a4314,3px 3px 0 #4f3b11,4px 4px 0 #4f3b11,5px 5px 0 #45330f,6px 6px 0 #45330f,7px 7px 0 #3b2c0d,8px 8px 0 #3b2c0d,9px 9px 0 #30240a,10px 10px 0 #30240a,14px 18px 30px rgba(0,0,0,.7); }
.g-num3d .front { position:relative; }
.g-cmp { position:absolute; left:120px; right:120px; top:250px; height:560px; perspective:1600px; }
.g-col { position:absolute; top:0; width:760px; height:540px; background:linear-gradient(180deg,#121318,#0a0a0a); border:1px solid var(--line); border-radius:20px; box-shadow:0 50px 100px rgba(0,0,0,.75); padding:38px 40px; }
.g-col.l { left:0; transform-origin:right center; } .g-col.r { right:0; transform-origin:left center; }
.g-col h3 { margin:14px 0 6px; font-size:46px; }
.g-col.r h3 { background:var(--gold-grad); -webkit-background-clip:text; background-clip:text; color:transparent; }
.g-vs { position:absolute; left:50%; top:230px; width:96px; height:96px; margin-left:-48px; border-radius:50%; background:var(--gold-grad); color:#050505; display:grid; place-items:center; font-family:"Plus Jakarta Sans",sans-serif; font-weight:800; font-size:30px; box-shadow:0 0 50px rgba(212,175,55,.45); }
.g-ftitle { position:absolute; left:120px; right:120px; top:110px; text-align:center; }
.g-ftitle h2 { margin:14px 0 0; font-size:50px; }
.g-tl { position:absolute; left:160px; right:160px; top:470px; height:300px; }
.g-tl .axis { position:absolute; left:0; right:0; top:120px; height:10px; border-radius:5px; background:#1b1c24; }
.g-tl .rng { position:absolute; top:116px; height:18px; border-radius:9px; background:var(--gold-grad); box-shadow:0 0 30px rgba(212,175,55,.45); transform-origin:left center; }
.g-tl .tick { position:absolute; top:150px; width:80px; margin-left:-40px; text-align:center; font-family:"Plus Jakarta Sans",sans-serif; font-weight:800; font-size:20px; color:var(--muted); }
.g-tl .pin { position:absolute; top:40px; width:150px; margin-left:-75px; text-align:center; }
.g-tl .pin .dot { width:22px; height:22px; border-radius:50%; margin:44px auto 0; background:#5d5f68; border:4px solid #050505; box-shadow:0 0 0 2px #5d5f68; }
.g-tl .pin.you .dot { background:var(--gold); box-shadow:0 0 0 2px var(--gold), 0 0 24px rgba(243,214,117,.7); }
.g-tl .pin .t { font-family:"Plus Jakarta Sans",sans-serif; font-weight:800; font-size:20px; color:var(--muted); text-transform:uppercase; letter-spacing:.06em; }
.g-tl .pin.you .t { color:var(--gold-hi); }
.g-tl .rl { position:absolute; top:186px; transform:translateX(-50%); padding:10px 18px; border-radius:999px; background:rgba(212,175,55,.12); border:1px solid var(--gold); color:var(--gold-hi); font-family:"Plus Jakarta Sans",sans-serif; font-size:22px; font-weight:800; white-space:nowrap; }
.g-grid { margin-top:26px; display:grid; grid-template-columns:repeat(30,22px); gap:6px; transform-style:preserve-3d; }
.g-grid i { width:22px; height:22px; border-radius:5px; background:#2c2d35; border:1px solid rgba(212,175,55,.12); display:block; }
.g-grid i.hero { background:var(--gold-grad); border:0; box-shadow:0 0 0 5px rgba(212,175,55,.22),0 0 40px rgba(243,214,117,.75); }
.g-gpanel { position:absolute; left:40px; top:40px; width:920px; height:720px; background:linear-gradient(180deg,#121318,#0a0a0a); border-radius:20px; box-shadow:0 60px 120px rgba(0,0,0,.8); border:1px solid var(--line); padding:36px 40px; transform-style:preserve-3d; transform-origin:50% 60%; }
.g-gpanel .hd { display:flex; justify-content:space-between; font-family:"Plus Jakarta Sans",sans-serif; font-size:15px; font-weight:700; color:var(--gold); letter-spacing:.2em; text-transform:uppercase; }
.g-copy { position:absolute; left:130px; top:250px; width:640px; }
.g-copy .a { margin-top:22px; font-size:38px; font-weight:700; color:var(--muted); line-height:1.15; }
.g-copy .b { margin-top:18px; font-size:84px; line-height:0.96; color:var(--fg); }
.g-copy .b .gold-text { display:block; }
/* broker screenshot recreation */
.g-brk { position:absolute; left:860px; top:170px; width:900px; height:600px; perspective:1800px; }
.g-brk .pn { position:absolute; inset:0; background:linear-gradient(180deg,#121318,#0a0a0a); border:1px solid var(--line); border-radius:22px; box-shadow:0 60px 120px rgba(0,0,0,.8); overflow:hidden; transform-origin:50% 60%; }
.g-brk .bar { height:70px; border-bottom:1px solid #1f2026; display:flex; align-items:center; padding:0 30px; gap:10px; }
.g-brk .bar .d { width:11px; height:11px; border-radius:50%; background:#2a2b31; }
.g-brk .bar .ttl { margin-left:14px; font-family:"Plus Jakarta Sans",sans-serif; font-size:15px; font-weight:700; letter-spacing:.2em; text-transform:uppercase; color:var(--gold); }
.g-brk .bar .tag { margin-left:auto; padding:7px 14px; border-radius:8px; font-size:15px; font-weight:700; background:rgba(212,175,55,.12); color:var(--gold-hi); }
.g-brk table { width:100%; border-collapse:collapse; margin-top:10px; }
.g-brk th { text-align:left; padding:26px 40px 18px; font-family:"Inter",sans-serif; font-weight:400; font-size:26px; color:#8b93a3; }
.g-brk th span { font-size:18px; margin-left:10px; color:#5d6676; }
.g-brk td { padding:34px 40px; border-top:1px solid #1f2026; font-family:"Plus Jakarta Sans",sans-serif; font-weight:800; font-size:54px; color:var(--fg); }
.g-brk td.vol { background:var(--gold-grad); -webkit-background-clip:text; background-clip:text; color:transparent; }
.g-brk .red { display:inline-block; width:300px; height:44px; border-radius:10px; background:repeating-linear-gradient(90deg,#2a2b33 0 18px,#22232a 18px 36px); filter:blur(5px); vertical-align:middle; }
.g-brk .lock { display:inline-flex; margin-left:14px; padding:6px 12px; border-radius:999px; background:rgba(255,255,255,.06); color:var(--muted); font-family:"Inter",sans-serif; font-weight:700; font-size:14px; letter-spacing:.08em; text-transform:uppercase; vertical-align:middle; }
.g-endcard { position:absolute; inset:0; display:flex; flex-direction:column; align-items:center; justify-content:center; }
.g-endcard img { width:150px; height:150px; border-radius:50%; box-shadow:0 0 60px rgba(212,175,55,.35); }
.g-endcard .nm { margin-top:26px; font-family:"Plus Jakarta Sans",sans-serif; font-weight:800; font-size:64px; }
.g-endcard .tg { margin-top:10px; font-family:"Plus Jakarta Sans",sans-serif; font-weight:700; font-size:22px; letter-spacing:.3em; text-transform:uppercase; color:var(--muted); }
"""

def gold(s):
    """'*word*' -> gold gradient span; escape the rest."""
    out = []
    for i, part in enumerate(re.split(r'\*([^*]+)\*', s)):
        out.append(f'<span class="gold-text">{html.escape(part)}</span>' if i % 2 else html.escape(part))
    return ''.join(out).replace('&lt;b&gt;','<b>').replace('&lt;/b&gt;','</b>')

norm = lambda x: re.sub(r"[^a-z0-9':]", "", x.lower())

class Words:
    def __init__(self, words): self.w = words
    def at(self, a):
        """a = number (seconds) | 'word@approx' -> start time of nearest matching word (±4 s), else approx."""
        if isinstance(a, (int, float)): return float(a)
        word, approx = a.rsplit('@', 1); approx = float(approx); word = norm(word)
        best = None
        for t, s, e in self.w:
            if norm(t) == word and abs(s - approx) <= 4 and (best is None or abs(s - approx) < abs(best - approx)): best = s
        if best is None:
            for t, s, e in self.w:
                if norm(t).startswith(word) and abs(s - approx) <= 4 and (best is None or abs(s - approx) < abs(best - approx)): best = s
        if best is None:
            print(f'   ! anchor "{a}" not found, using {approx}', file=sys.stderr); return approx
        return best

ICONS = {
 'arrow': '<path d="M5 12h14M13 6l6 6-6 6"/>', 'exit': '<path d="M10 4H5v16h5M14 8l4 4-4 4M18 12H9"/>',
 'check': '<path d="M5 12.5l4.5 4.5L19 7"/>', 'chart': '<path d="M4 19V5M4 19h16M8 15l4-4 3 3 5-6"/>',
 'zone': '<path d="M4 7h16M4 17h16M7 7v10M17 7v10"/>', 'target': '<circle cx="12" cy="12" r="8"/><circle cx="12" cy="12" r="3"/>',
 'brain': '<path d="M9 5a3 3 0 0 0-3 3v1a3 3 0 0 0 0 6v1a3 3 0 0 0 6 0V5a3 3 0 0 0-3 0zM15 5a3 3 0 0 1 3 3v1a3 3 0 0 1 0 6v1a3 3 0 0 1-6 0"/>',
 'heart': '<path d="M12 20s-7-4.5-7-10a4 4 0 0 1 7-2.5A4 4 0 0 1 19 10c0 5.5-7 10-7 10z"/>',
 'clock': '<circle cx="12" cy="12" r="8"/><path d="M12 8v4l3 2"/>', 'star': '<path d="M12 4l2.4 5 5.6.6-4.2 3.8 1.2 5.6L12 16.3 7 19l1.2-5.6L4 9.6 9.6 9z"/>',
}
def icon(name, size=44, color='currentColor'):
    return f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">{ICONS.get(name, ICONS["arrow"])}</svg>'

def build(part):
    P = part; W = Words(P['words']); DUR = P['dur']; cards = P['cards']
    html_cards = []; js = []; sfx = []; sides = []
    T = W.at
    def q(t): return f'{round(t*30)/30:.4f}'
    def S(t, f, v): sfx.append((max(0, t), f, v))

    for c in cards:
        cid = c['id']; typ = c['type']; side = c.get('side', 'L'); t0 = T(c['t0']); t1 = T(c['t1'])
        sides.append((t0, t1, {'L': 'L', 'R': 'R', 'S': 'S', 'F': 'F', 'N': 'N'}[side]))
        host_open = f'<div class="card-host clip" id="{cid}" data-start="{t0:.3f}" data-duration="{t1 - t0 + (0.35 if side in "FS" else 0):.3f}" data-track-index="{4 if side in "FS" else 2}" style="left:0;top:0;width:1920px;height:1080px;">'
        sel = f'#{cid}'
        inner = ''
        if side == 'F' or typ in ('big', 'compare', 'timeline', 'grid', 'broker', 'chart', 'end'):
            inner += '<div class="gridbg"></div>'
        if side == 'S':
            inner += '<div style="position:absolute;left:0;top:0;width:960px;height:1080px;overflow:hidden"><div class="gridbg"></div></div>'

        # ---- entry/exit for side cards ----
        def card_in(cls_extra=''):
            ry = -32 if side in 'LS' else 32
            js.append(f'tl.fromTo("{sel} .g-card",{{opacity:0,rotationY:{ry},x:{-40 if side in "LS" else 40},z:-120}},{{opacity:1,rotationY:{-10 if side=="R" else 0},x:0,z:0,duration:0.7,ease:"power3.out"}},{q(t0)});')
            js.append(f'tl.to("{sel} .g-card",{{opacity:0,y:-10,duration:0.35,ease:"power2.in"}},{q(t1-0.35)});')
            S(t0, 'whoosh-short', .3)
        def full_in():
            js.append(f'tl.fromTo("{sel}",{{opacity:0}},{{opacity:1,duration:0.3,ease:"power2.out"}},{q(t0)});')
            js.append(f'tl.to("#video-wrap",{{opacity:0,duration:0.01}},{q(t0+0.3)});')
            js.append(f'tl.to("#video-wrap",{{opacity:1,duration:0.01}},{q(t1)});')
            js.append(f'tl.to("{sel}",{{opacity:0,duration:0.3,ease:"power2.in"}},{q(t1)});')
            js.append(f'tl.to("#brand",{{opacity:0,duration:0.3}},{q(t0)});tl.to("#brand",{{opacity:1,duration:0.3}},{q(t1)});')
            S(t0, 'whoosh', .34)
        def rise(s_, t, d=0.45, extra=''):
            js.append(f'tl.fromTo("{s_}",{{opacity:0,y:18{extra}}},{{opacity:1,y:0,duration:{d},ease:"power3.out"}},{q(t)});')

        kick = f'<div class="kicker"><span class="dot"></span>{html.escape(c.get("kicker",""))}</div>' if c.get('kicker') else ''

        if typ in ('title', 'quote'):
            lines = ''.join(f'<span class="g-line" id="{cid}-l{i}">{gold(l["text"])}</span>' for i, l in enumerate(c['lines']))
            sub = f'<div class="g-sub" id="{cid}-sub">{gold(c["sub"]["text"])}</div>' if c.get('sub') else ''
            inner += f'<div class="g-card g-{side}">{kick}<h2 class="h g-h2{" sm" if c.get("small") else ""}">{lines}</h2>{sub}</div>'
            card_in()
            for i, l in enumerate(c['lines']):
                rise(f'#{cid}-l{i}', T(l['at']), 0.45); S(T(l['at']), l.get('sfx', 'pop' if i else 'whoosh-short'), .22 if i else 0)
            if c.get('sub'): rise(f'#{cid}-sub', T(c['sub']['at'])); S(T(c['sub']['at']), 'sparkle', .18)
        elif typ == 'list':
            rows = ''
            for i, r in enumerate(c['rows']):
                mk = {'x': '<span class="mk x">✕</span>', 'ok': '<span class="mk ok">✓</span>'}.get(r.get('mark'), '')
                st = '<span class="strike"></span>' if r.get('strike') else ''
                rows += f'<div class="g-row" id="{cid}-r{i}"><span class="ic">{r.get("ic", i + 1)}</span>{gold(r["text"])}{mk}{st}</div>'
            ver = f'<div class="g-verdict" id="{cid}-v">{html.escape(c["verdict"]["text"])}</div>' if c.get('verdict') else ''
            title = f'<h2 class="h g-h2 sm">{gold(c["title"])}</h2>' if c.get('title') else ''
            inner += f'<div class="g-card g-{side}">{kick}{title}{rows}{ver}</div>'
            card_in()
            for i, r in enumerate(c['rows']):
                t = T(r['at'])
                js.append(f'tl.fromTo("#{cid}-r{i}",{{opacity:0,rotationX:-90}},{{opacity:1,rotationX:0,duration:0.55,ease:"back.out(1.4)"}},{q(t)});')
                S(t, 'click-soft', .36)
                if r.get('mark'):
                    tm = T(r.get('mark_at', r['at'])) + (0 if r.get('mark_at') else 0.35)
                    js.append(f'tl.fromTo("#{cid}-r{i} .mk",{{opacity:0,scale:0.4}},{{opacity:1,scale:1,duration:0.35,ease:"back.out(2)"}},{q(tm)});')
                    S(tm, 'error' if r['mark'] == 'x' else 'pop', .18 if r['mark'] == 'x' else .24)
                if r.get('strike'):
                    js.append(f'tl.to("#{cid}-r{i} .strike",{{width:{r.get("strike_w", 380)},duration:0.4,ease:"power2.inOut"}},{q(T(r["strike"]))});')
            if c.get('verdict'):
                tv = T(c['verdict']['at'])
                js.append(f'tl.fromTo("#{cid}-v",{{opacity:0,y:14,scale:0.9}},{{opacity:1,y:0,scale:1,duration:0.45,ease:"back.out(1.8)"}},{q(tv)});'); S(tv, 'pop', .26)
        elif typ == 'bars':
            rows = ''.join(f'<div class="g-brow" id="{cid}-b{i}"><div class="top"><span>{html.escape(r["label"])}</span><span>{html.escape(r.get("right",""))}</span></div><div class="g-track"><div class="g-bar" id="{cid}-bb{i}"></div></div></div>' for i, r in enumerate(c['rows']))
            foot = f'<div class="g-sub" id="{cid}-sub">{gold(c["sub"]["text"])}</div>' if c.get('sub') else ''
            inner += f'<div class="g-card g-{side}">{kick}<h2 class="h g-h2 sm">{gold(c["title"])}</h2>{rows}{foot}</div>'
            card_in()
            for i, r in enumerate(c['rows']):
                t = T(r['at']); rise(f'#{cid}-b{i}', t, 0.4)
                js.append(f'tl.fromTo("#{cid}-bb{i}",{{width:"0%"}},{{width:"{r["pct"]}%",duration:0.9,ease:"power2.inOut"}},{q(t+0.02)});'); S(t, 'ping', .2)
            if c.get('sub'): rise(f'#{cid}-sub', T(c['sub']['at'])); S(T(c['sub']['at']), 'pop', .22)
        elif typ == 'flow':
            n = len(c['steps']); gap = 440 / max(1, n - 1) if n > 1 else 0
            steps = ''.join(f'<div class="g-step" id="{cid}-s{i}" style="left:{-10 + i * gap:.0f}px"><div class="n">{icon(s_.get("icon","arrow")) if s_.get("icon") else i + 1}</div><div class="lbl">{html.escape(s_["label"])}</div></div>' for i, s_ in enumerate(c['steps']))
            foot = f'<div class="g-chips" id="{cid}-ch">' + ''.join(f'<span class="g-chip" id="{cid}-c{i}"><i></i>{html.escape(x["text"])}</span>' for i, x in enumerate(c.get('chips', []))) + '</div>' if c.get('chips') else ''
            title = f'<h2 class="h g-h2 sm">{gold(c["title"])}</h2>' if c.get('title') else ''
            inner += f'<div class="g-card g-{side}">{kick}{title}<div class="g-flow"><div class="lbg"></div><div class="ln" id="{cid}-ln"></div>{steps}</div>{foot}</div>'
            card_in()
            js.append(f'gsap.set("#{cid} .g-step",{{opacity:0.35,rotationY:70}});')
            for i, s_ in enumerate(c['steps']):
                t = T(s_['at'])
                js.append(f'tl.to("#{cid}-s{i}",{{opacity:1,rotationY:0,duration:0.55,ease:"back.out(1.6)"}},{q(t)});tl.set("#{cid}-s{i}",{{className:"g-step on"}},{q(t)});')
                if i: js.append(f'tl.to("#{cid}-ln",{{width:{gap * i:.0f},duration:0.5,ease:"power2.inOut"}},{q(t - 0.1)});')
                S(t, 'click', .4)
            for i, x in enumerate(c.get('chips', [])):
                t = T(x['at']); js.append(f'tl.fromTo("#{cid}-c{i}",{{opacity:0,scale:0.7}},{{opacity:1,scale:1,duration:0.4,ease:"back.out(1.8)"}},{q(t)});'); S(t, 'pop', .24)
        elif typ == 'chips':
            body = ''
            for i, x in enumerate(c['chips']):
                if x.get('sec'): body += f'<div class="g-sec" id="{cid}-c{i}">{html.escape(x["text"])}</div>'
                else: body += f'<span class="g-chip{" hot" if x.get("hot") else ""}" id="{cid}-c{i}"><i></i>{html.escape(x["text"])}</span>'
            title = f'<h2 class="h g-h2 sm">{gold(c["title"])}</h2>' if c.get('title') else ''
            foot = f'<div class="g-sub" id="{cid}-sub">{gold(c["sub"]["text"])}</div>' if c.get('sub') else ''
            inner += f'<div class="g-card g-{side}">{kick}{title}<div class="g-chips">{body}</div>{foot}</div>'
            card_in()
            for i, x in enumerate(c['chips']):
                t = T(x['at']); js.append(f'tl.fromTo("#{cid}-c{i}",{{opacity:0,scale:0.7,y:10}},{{opacity:1,scale:1,y:0,duration:0.4,ease:"back.out(1.8)"}},{q(t)});'); S(t, 'pop', .22)
            if c.get('sub'): rise(f'#{cid}-sub', T(c['sub']['at'])); S(T(c['sub']['at']), 'sparkle', .18)
        elif typ == 'pill':
            inner += f'<div class="g-pill" id="{cid}-p">{gold(c["text"])}</div>'
            ta = T(c['at'])
            js.append(f'tl.fromTo("#{cid}-p",{{opacity:0,y:30,rotationX:-60}},{{opacity:1,y:0,rotationX:0,duration:0.55,ease:"power3.out"}},{q(ta)});')
            js.append(f'tl.to("#{cid}-p",{{opacity:0,y:12,duration:0.3,ease:"power2.in"}},{q(t1 - 0.3)});'); S(ta, 'whoosh', .28)
        elif typ == 'big':
            num = ''
            if c.get('num'):
                num = f'<div class="g-num3d" id="{cid}-n"><span class="back">{html.escape(c["num"]["text"])}</span><span class="front gold-text">{html.escape(c["num"]["text"])}</span></div>'
            lines = ''.join(f'<span class="g-line" id="{cid}-l{i}">{gold(l["text"])}</span>' for i, l in enumerate(c['lines']))
            subs = ''.join(f'<div class="g-bsub" id="{cid}-s{i}">{gold(s_["text"])}</div>' for i, s_ in enumerate(c.get('subs', [])))
            chips = ''
            if c.get('chips'):
                chips = '<div class="g-chips" style="justify-content:center;margin-top:30px">' + ''.join(f'<span class="g-chip" id="{cid}-c{i}" style="font-size:26px;padding:14px 24px"><i></i>{html.escape(x["text"])}</span>' for i, x in enumerate(c['chips'])) + '</div>'
            inner += f'<div class="g-center">{kick}{num}<div class="h g-big{" md" if c.get("md") else ""}">{lines}</div>{subs}{chips}</div>'
            full_in()
            if c.get('num'):
                tn = T(c['num']['at'])
                js.append(f'tl.fromTo("#{cid}-n",{{rotationY:-80,opacity:0}},{{rotationY:-14,opacity:1,duration:0.9,ease:"back.out(1.4)"}},{q(tn)});tl.to("#{cid}-n",{{rotationY:10,duration:{max(1, t1 - tn - 1):.2f},ease:"sine.inOut"}},{q(tn + 0.9)});')
                S(tn, 'impact-bass-1', .3)
            for i, l in enumerate(c['lines']):
                t = T(l['at']); js.append(f'tl.fromTo("#{cid}-l{i}",{{opacity:0,y:30,scale:0.94}},{{opacity:1,y:0,scale:1,duration:0.55,ease:"power3.out"}},{q(t)});')
                if l.get('hit'): S(t, 'impact-bass-1', .3)
            for i, s_ in enumerate(c.get('subs', [])): rise(f'#{cid}-s{i}', T(s_['at'])); S(T(s_['at']), 'sparkle', .18)
            for i, x in enumerate(c.get('chips', [])):
                t = T(x['at']); js.append(f'tl.fromTo("#{cid}-c{i}",{{opacity:0,scale:0.7,y:12}},{{opacity:1,scale:1,y:0,duration:0.4,ease:"back.out(1.8)"}},{q(t)});'); S(t, 'pop', .22)
        elif typ == 'compare':
            def col(k, d):
                items = ''.join(f'<div class="g-row" id="{cid}-{k}{i}"><span class="ic">{html.escape(str(x.get("ic", i + 1)))}</span>{gold(x["text"])}</div>' for i, x in enumerate(d['items']))
                return f'<div class="g-col {k}" id="{cid}-{k}"><div class="kicker"><span class="dot"></span>{html.escape(d.get("kicker",""))}</div><h3 class="h">{html.escape(d["title"])}</h3>{items}</div>'
            inner += f'<div class="g-ftitle">{kick}<h2 class="h" id="{cid}-t">{gold(c["title"])}</h2></div><div class="g-cmp">{col("l", c["left"])}{col("r", c["right"])}<div class="g-vs" id="{cid}-vs">VS</div></div>'
            full_in()
            rise(f'#{cid}-t', t0 + 0.15)
            tl_ = T(c['left']['at']); tr_ = T(c['right']['at'])
            js.append(f'tl.fromTo("#{cid}-l",{{opacity:0,rotationY:40,x:-60}},{{opacity:1,rotationY:10,x:0,duration:0.8,ease:"power3.out"}},{q(tl_)});')
            js.append(f'tl.fromTo("#{cid}-r",{{opacity:0,rotationY:-40,x:60}},{{opacity:1,rotationY:-10,x:0,duration:0.8,ease:"power3.out"}},{q(tr_)});')
            js.append(f'tl.fromTo("#{cid}-vs",{{opacity:0,scale:0.3}},{{opacity:1,scale:1,duration:0.5,ease:"back.out(2)"}},{q(tr_ + 0.2)});'); S(tr_ + 0.2, 'impact-bass-1', .26); S(tl_, 'whoosh-short', .26)
            for k in ('l', 'r'):
                for i, x in enumerate(c['left' if k == 'l' else 'right']['items']):
                    t = T(x['at']); js.append(f'tl.fromTo("#{cid}-{k}{i}",{{opacity:0,rotationX:-90}},{{opacity:1,rotationX:0,duration:0.55,ease:"back.out(1.4)"}},{q(t)});'); S(t, 'click-soft', .34)
        elif typ == 'timeline':
            hrs = c['hours']; h0, h1 = hrs[0], hrs[-1]
            X = lambda h: (h - h0) / (h1 - h0) * 100
            ticks = ''.join(f'<div class="tick" style="left:{X(h):.2f}%">{int(h) if h<=12 else int(h)-12} AM</div>' for h in hrs)
            pins = ''.join(f'<div class="pin{" you" if p.get("you") else ""}" id="{cid}-p{i}" style="left:{X(p["h"]):.2f}%"><div class="t">{html.escape(p["label"])}</div><div class="dot"></div></div>' for i, p in enumerate(c['pins']))
            r = c['range']
            rng = f'<div class="rng" id="{cid}-rg" style="left:{X(r["from"]):.2f}%;width:{X(r["to"]) - X(r["from"]):.2f}%"></div><div class="rl" id="{cid}-rl" style="left:{(X(r["from"]) + X(r["to"])) / 2:.2f}%">{html.escape(r["label"])}</div>'
            subs = ''.join(f'<div class="g-bsub" id="{cid}-s{i}" style="position:absolute;left:0;right:0;top:{830 + i * 52}px;text-align:center;font-size:30px">{gold(s_["text"])}</div>' for i, s_ in enumerate(c.get('subs', [])))
            inner += f'<div class="g-ftitle">{kick}<h2 class="h" id="{cid}-t">{gold(c["title"])}</h2></div><div class="g-tl"><div class="axis"></div>{rng}{ticks}{pins}</div>{subs}'
            full_in(); rise(f'#{cid}-t', t0 + 0.15)
            js.append(f'gsap.set("#{cid} .tick",{{opacity:0}});tl.to("#{cid} .tick",{{opacity:1,duration:0.3,stagger:0.05}},{q(t0 + 0.3)});')
            for i, p in enumerate(c['pins']):
                t = T(p['at']); js.append(f'tl.fromTo("#{cid}-p{i}",{{opacity:0,y:-30}},{{opacity:1,y:0,duration:0.45,ease:"back.out(1.8)"}},{q(t)});'); S(t, 'pop' if p.get('you') else 'click-soft', .26)
            tr = T(r['at'])
            js.append(f'tl.fromTo("#{cid}-rg",{{scaleX:0,opacity:1}},{{scaleX:1,duration:0.8,ease:"power2.inOut"}},{q(tr)});tl.fromTo("#{cid}-rl",{{opacity:0,y:10}},{{opacity:1,y:0,duration:0.4,ease:"back.out(1.8)"}},{q(tr + 0.5)});')
            js.append(f'gsap.set("#{cid}-rg",{{scaleX:0}});'); S(tr, 'impact-bass-1', .28)
            for i, s_ in enumerate(c.get('subs', [])): rise(f'#{cid}-s{i}', T(s_['at'])); S(T(s_['at']), 'sparkle', .18)
        elif typ == 'grid':
            inner += f'<div class="g-copy"><div class="kicker" id="{cid}-k"><span class="dot"></span>{html.escape(c.get("kicker",""))}</div><div class="a" id="{cid}-a">{gold(c["a"]["text"])}</div><div class="b h" id="{cid}-b">{gold(c["b"]["text"])}</div></div><div style="position:absolute;left:820px;top:90px;width:1000px;height:800px;perspective:1800px"><div class="g-gpanel" id="{cid}-p"><div class="hd"><span>Trade log</span><span style="letter-spacing:0;text-transform:none;font-family:Inter;font-weight:400;color:var(--muted)">■ The one trade · ■ Practice trades</span></div><div class="g-grid" id="{cid}-g"></div></div></div>'
            full_in(); rise(f'#{cid}-k', t0 + 0.15); rise(f'#{cid}-a', T(c['a']['at']))
            ta = T(c['fill_at']); tb = T(c['b']['at']); th = T(c['hero_at'])
            js.append(f'(function(){{const g=document.getElementById("{cid}-g");for(let i=0;i<660;i++){{const e=document.createElement("i");if(i===344)e.className="hero";g.appendChild(e);}}}})();')
            js.append(f'tl.fromTo("#{cid}-p",{{opacity:0,rotationX:62,rotationY:-38,rotationZ:8,z:-300}},{{opacity:1,rotationX:32,rotationY:-24,rotationZ:4,z:0,duration:1.0,ease:"power3.out"}},{q(t0 + 0.1)});tl.to("#{cid}-p",{{rotationX:16,rotationY:-10,rotationZ:1,duration:{max(1, t1 - t0 - 1.1):.2f},ease:"sine.inOut"}},{q(t0 + 1.1)});')
            js.append(f'gsap.set("#{cid}-g i",{{opacity:0}});tl.to("#{cid}-g i:not(.hero)",{{opacity:1,duration:0.25,stagger:{{each:0.0028,from:344,grid:[22,30]}}}},{q(ta)});')
            js.append(f'tl.fromTo("#{cid}-g i.hero",{{opacity:0,scale:0.4,z:0}},{{opacity:1,scale:1.25,z:60,duration:0.6,ease:"back.out(2)"}},{q(th)});')
            rise(f'#{cid}-b', tb, 0.55); S(ta, 'impact-bass-1', .3); S(th, 'sparkle', .22)
        elif typ == 'broker':
            rows = ''.join(f'<tr id="{cid}-r{i}"><td><span class="red"></span><span class="lock">hidden</span></td><td class="vol" id="{cid}-v{i}">0.00</td></tr>' for i, r in enumerate(c['volumes']))
            inner += (f'<div class="g-copy" style="width:660px"><div class="kicker" id="{cid}-k"><span class="dot"></span>{html.escape(c["kicker"])}</div><div class="b h" id="{cid}-b" style="font-size:66px">{gold(c["title"]["text"])}</div>'
                      f'<div class="a" id="{cid}-a" style="font-size:30px">{gold(c["meta"]["text"])}</div><div class="g-verdict" id="{cid}-f" style="margin-top:28px">{html.escape(c["foot"]["text"])}</div></div>'
                      f'<div class="g-brk"><div class="pn" id="{cid}-pn"><div class="bar"><span class="d"></span><span class="d"></span><span class="d"></span><span class="ttl">Broker · account history</span><span class="tag">1 of 3 brokers</span></div>'
                      f'<table><tr><th>Withdrawals<span>⇅</span></th><th>Volume<span>⇅</span></th></tr>{rows}</table></div></div>')
            full_in(); rise(f'#{cid}-k', t0 + 0.15); rise(f'#{cid}-b', T(c['title']['at'])); rise(f'#{cid}-a', T(c['meta']['at'])); S(T(c['meta']['at']), 'pop', .24)
            tf = T(c['foot']['at']); js.append(f'tl.fromTo("#{cid}-f",{{opacity:0,scale:0.85}},{{opacity:1,scale:1,duration:0.45,ease:"back.out(1.8)"}},{q(tf)});'); S(tf, 'pop', .26)
            tp = T(c['panel_at'])
            js.append(f'tl.fromTo("#{cid}-pn",{{opacity:0,rotationX:40,rotationY:-30,z:-260}},{{opacity:1,rotationX:12,rotationY:-14,z:0,duration:1.0,ease:"power3.out"}},{q(tp)});tl.to("#{cid}-pn",{{rotationX:4,rotationY:-6,duration:{max(1, t1 - tp - 1):.2f},ease:"sine.inOut"}},{q(tp + 1)});'); S(tp, 'whoosh-short', .3)
            for i, r in enumerate(c['volumes']):
                t = T(r['at'])
                js.append(f'tl.fromTo("#{cid}-r{i}",{{opacity:0,y:20}},{{opacity:1,y:0,duration:0.45,ease:"power3.out"}},{q(t)});')
                js.append(f'(function(){{const o={{v:0}};tl.to(o,{{v:{r["value"]},duration:1.6,ease:"power2.out",onUpdate:function(){{const e=document.getElementById("{cid}-v{i}");if(e)e.textContent=o.v.toLocaleString("en-US",{{minimumFractionDigits:2,maximumFractionDigits:2}});}}}},{q(t + 0.15)});}})();')
                S(t + 0.15, 'ping', .22)
            js.append(f'gsap.set("#{cid} tr[id]",{{opacity:0}});')
        elif typ == 'chart':
            inner += (f'<div style="position:absolute;inset:0;perspective:1800px"><div class="dash" id="{cid}-d" style="position:absolute;left:160px;top:70px;width:1600px;height:790px;background:linear-gradient(180deg,#121318,#0a0a0a);border-radius:20px;box-shadow:0 60px 120px rgba(0,0,0,.8);border:1px solid var(--line);overflow:hidden;transform-origin:50% 100%">'
                      f'<div style="position:absolute;left:56px;top:56px">{kick}<h2 class="h" id="{cid}-h" style="margin:12px 0 0;font-size:50px">{gold(c["title"]["text"])}</h2><div id="{cid}-f" style="margin-top:12px;font-size:24px;font-weight:700;color:var(--muted)">{gold(c["foot"]["text"])}</div></div>'
                      f'<svg style="position:absolute;left:60px;top:250px;width:1480px;height:520px" viewBox="0 0 1480 520" fill="none"><defs><linearGradient id="{cid}gU" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#8a681f"/><stop offset=".6" stop-color="#d4af37"/><stop offset="1" stop-color="#f3d675"/></linearGradient></defs>'
                      f'<g stroke="#1c1d23" stroke-width="2"><line x1="0" y1="80" x2="1480" y2="80"/><line x1="0" y1="200" x2="1480" y2="200"/><line x1="0" y1="320" x2="1480" y2="320"/><line x1="0" y1="440" x2="1480" y2="440"/></g>'
                      f'<path id="{cid}-up" d="M0 420 C 140 400, 260 330, 380 280 S 600 150, 760 90" stroke="url(#{cid}gU)" stroke-width="7" stroke-linecap="round"/>'
                      f'<path id="{cid}-dn" d="M760 90 C 820 100, 880 200, 940 300 S 1080 470, 1180 480" stroke="#ef4444" stroke-width="7" stroke-linecap="round"/>'
                      f'<path id="{cid}-rec" d="M1180 480 C 1240 470, 1300 420, 1350 380 S 1440 330, 1470 310" stroke="#f3d675" stroke-width="7" stroke-dasharray="2 16" stroke-linecap="round"/></svg>'
                      f'<div class="tag" id="{cid}-t1" style="position:absolute;left:640px;top:250px;padding:10px 18px;border-radius:10px;background:var(--gold-grad);color:#050505;font-family:Plus Jakarta Sans;font-weight:800;font-size:18px;letter-spacing:.06em;text-transform:uppercase">{html.escape(c["up"]["text"])}</div>'
                      f'<div class="tag" id="{cid}-t2" style="position:absolute;left:1120px;top:640px;padding:10px 18px;border-radius:10px;background:rgba(239,68,68,.12);border:1px solid rgba(239,68,68,.45);color:#ef4444;font-family:Plus Jakarta Sans;font-weight:800;font-size:18px;letter-spacing:.06em;text-transform:uppercase">{html.escape(c["down"]["text"])}</div>'
                      f'<div class="tag" id="{cid}-t3" style="position:absolute;left:1330px;top:500px;padding:10px 18px;border-radius:10px;background:rgba(212,175,55,.12);border:1px solid var(--gold);color:var(--gold-hi);font-family:Plus Jakarta Sans;font-weight:800;font-size:18px;letter-spacing:.06em;text-transform:uppercase">{html.escape(c["rec"]["text"]) if c.get("rec") else ""}</div></div></div>')
            full_in()
            js.append(f'tl.fromTo("#{cid}-d",{{rotationX:34,y:60,z:-200}},{{rotationX:12,y:0,z:0,duration:0.9,ease:"power3.out"}},{q(t0)});tl.to("#{cid}-d",{{rotationX:4,duration:{max(1, t1 - t0 - 1):.2f},ease:"sine.inOut"}},{q(t0 + 0.9)});')
            rise(f'#{cid}-h', T(c['title']['at'])); rise(f'#{cid}-f', T(c['foot']['at']))
            for p_, k in ((f'{cid}-up', 'up'), (f'{cid}-dn', 'down')):
                js.append(f'(function(){{const e=document.getElementById("{p_}");const L=e.getTotalLength();gsap.set(e,{{strokeDasharray:L,strokeDashoffset:L,opacity:0}});tl.set(e,{{opacity:1}},{q(T(c[k]["at"]) + 0.05)});tl.to(e,{{strokeDashoffset:0,duration:1.0,ease:"power1.inOut"}},{q(T(c[k]["at"]))});}})();')
            js.append(f'gsap.set(["#{cid}-t1","#{cid}-t2","#{cid}-t3","#{cid}-rec"],{{opacity:0}});')
            rise(f'#{cid}-t1', T(c['up']['at']) + 0.6); rise(f'#{cid}-t2', T(c['down']['at']) + 0.6)
            S(T(c['up']['at']), 'ping', .2); S(T(c['down']['at']), 'impact-bass-1', .34)
            js.append(f'tl.fromTo("#{cid}-d",{{x:0}},{{x:6,duration:0.05,yoyo:true,repeat:5,ease:"none"}},{q(T(c["down"]["at"]) + 0.05)});')
            if c.get('rec'):
                tr = T(c['rec']['at']); js.append(f'tl.to("#{cid}-rec",{{opacity:1,duration:0.6}},{q(tr)});'); rise(f'#{cid}-t3', tr + 0.3); S(tr, 'sparkle', .2)
        elif typ == 'end':
            inner += f'<div class="g-endcard"><img src="img/emblem.png" id="{cid}-i"/><div class="nm gold-text" id="{cid}-n">$hubzTrader</div><div class="tg" id="{cid}-g">{html.escape(c.get("tag","One trade away"))}</div></div>'
            full_in()
            js.append(f'tl.fromTo("#{cid}-i",{{opacity:0,scale:0.6,rotationY:-60}},{{opacity:1,scale:1,rotationY:0,duration:0.9,ease:"back.out(1.6)"}},{q(t0 + 0.2)});')
            rise(f'#{cid}-n', t0 + 0.5); rise(f'#{cid}-g', t0 + 0.8); S(t0 + 0.2, 'impact-bass-1', .3)
        else:
            raise SystemExit('unknown type ' + typ)
        html_cards.append(host_open + inner + '</div>')

    # ---- SFX tags ----
    tags = []; tracks = {}
    for i, (t, f, v) in enumerate(sorted(sfx)):
        if v <= 0: continue
        d = min(SFX_DUR[f], DUR - t)
        if d <= 0.05: continue
        tr = 10
        while tracks.get(tr, -1) > t: tr += 1
        tracks[tr] = t + d
        tags.append(f'<audio id="sfx{i:03d}" src="audio/{f}.mp3" data-start="{t:.2f}" data-duration="{d:.2f}" data-volume="{v}" data-track-index="{tr}"></audio>')

    side_js = json.dumps([[round(a, 3), round(b, 3), s] for a, b, s in sides if s != 'N'])
    words_js = json.dumps(P['words'], ensure_ascii=False, separators=(',', ':'))
    cuts_js = json.dumps(P['cuts'])
    key_re = P.get('key_re', "trade|successful|trader|backtesting|forward|testing|emotions|psychology|losing|loss|profitable|profit|fear|dar|lot|size|confident|session|london|york|tokyo|sydney|asian|demo|hard|mehnat|life|family|happy|happiness|beautiful|important|hormones|winning|thousands|hazaar|setup|strategies|broker|brokers|journey|fight|duniya|zindagi")
    brand_anim = 'tl.fromTo("#brand .pill",{opacity:0,x:-16},{opacity:1,x:0,duration:0.5,ease:"power3.out"},0.1);' if P.get('brand_anim') else ''
    out = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8" /><style>{BASE_CSS}
{EXTRA_CSS}</style></head>
<body>
<div id="stage" data-composition-id="shubz-{P['name']}" data-start="0" data-duration="{DUR:.3f}" data-fps="30" data-width="1920" data-height="1080">
  <div class="video-wrapper" id="video-wrap"><div id="zoom"><video id="bg-video" src="input-video.mp4" playsinline data-has-audio="true" data-start="0" data-duration="{min(DUR, P['video_dur']):.3f}" data-track-index="1"></video></div><div class="vignette"></div></div>
  {''.join(html_cards)}
  <div class="card-host clip" id="brand" data-start="0" data-duration="{DUR:.3f}" data-track-index="5" style="left:0;top:0;width:1920px;height:140px;"><div class="pill"><img src="img/emblem.png" alt="" /><span class="nm gold-text">$hubzTrader</span><span class="sep"></span><span class="ep">One Trade Away</span></div></div>
  <div class="card-host clip" id="captions" data-start="0" data-duration="{DUR:.3f}" data-track-index="6" style="left:0;top:0;width:1920px;height:1080px;"></div>
  {''.join(tags)}
  <script src="vendor/gsap.min.js"></script>
  <script>
  (function(){{
    const FPS=30, DUR={DUR:.3f}; const q=(t)=>Math.round(t*FPS)/FPS;
    const tl=gsap.timeline({{paused:true}}); const E="power3.out", EI="power2.inOut";
    const WORDS={words_js}; const CUTS={cuts_js}; const SIDE={side_js};
    // framing engine: zoom cuts + face-safe reframes
    const sideAt=(t)=>{{for(const [a,b,s] of SIDE) if(t>=a-0.001&&t<b) return s; return "N";}};
    const FR={{L:[[1.12,110],[1.2,125]],R:[[1.12,-110],[1.2,-125]],N:[[1.0,0],[1.24,0]],S:[[1.0,0],[1.0,0]],F:[[1.0,0],[1.0,0]]}};
    const Z="#zoom"; let alt=0,last=sideAt(0); gsap.set(Z,{{scale:FR[last][0][0],x:FR[last][0][1]}});
    const ev=[...CUTS.map(t=>[t,"cut"]),...SIDE.map(s=>[s[0],"side"]),...SIDE.map(s=>[s[1],"side"])].filter(e=>e[0]>0.05&&e[0]<DUR-0.1).sort((a,b)=>a[0]-b[0]);
    for(const [t,k] of ev){{const s=sideAt(t+0.01);
      if(k==="cut"){{alt^=1;const [sc,x]=FR[s][alt];tl.set(Z,{{scale:sc,x:x}},q(t));}}
      else if(s!==last){{alt=0;const [sc,x]=FR[s][0];tl.to(Z,{{scale:sc,x:x,duration:0.55,ease:EI}},q(Math.max(0,t-0.35)));}}
      last=s;}}
    // split-screen: shift video right while an S card is up
    for(const [a,b,s] of SIDE) if(s==="S"){{tl.set("#video-wrap",{{x:480}},q(a));tl.set(Z,{{scale:1,x:0}},q(a));tl.to("#video-wrap",{{x:0,duration:0.55,ease:EI}},q(b-0.3));}}
    // captions v2
    const KEY=/^({key_re})$/i; const host=document.getElementById("captions"); const chunks=[]; let cur=[];
    WORDS.forEach(w=>{{const p=cur[cur.length-1];const len=cur.reduce((a,x)=>a+x[0].length+1,0)+w[0].length;
      if(cur.length&&(cur.length>=4||len>22||(p&&w[1]-p[2]>0.45))){{chunks.push(cur);cur=[];}} cur.push(w);
      if(/[.,?!]$/.test(w[0])&&cur.length>=2){{chunks.push(cur);cur=[];}}}});
    if(cur.length) chunks.push(cur);
    chunks.forEach((c,ci)=>{{const el=document.createElement("div");el.className="chunk";
      c.forEach(w=>{{const s=document.createElement("span");const tx=w[0].replace(/[.,]$/,"");s.className="cw"+(KEY.test(tx.replace(/[^A-Za-z']/g,""))?" key":"");s.textContent=tx;el.appendChild(s);}});
      host.appendChild(el); const st=c[0][1], nx=chunks[ci+1]; const en=Math.min(nx?nx[0][1]:DUR,c[c.length-1][2]+0.6,DUR);
      tl.set(el,{{visibility:"visible"}},q(st)); tl.fromTo(el,{{opacity:0,y:14,scale:0.97}},{{opacity:1,y:0,scale:1,duration:0.16,ease:"power2.out"}},q(st)); tl.set(el,{{visibility:"hidden",opacity:0}},q(en));
      const sp=el.querySelectorAll(".cw"); c.forEach((w,wi)=>{{const base=sp[wi].className.replace(/ ?(on|done)/g,"");
        tl.set(sp[wi],{{className:base+" on"}},q(w[1])); tl.fromTo(sp[wi],{{scale:1.12}},{{scale:1,duration:0.18,ease:"power2.out"}},q(w[1]));
        tl.set(sp[wi],{{className:base+" done"}},q(wi<c.length-1?c[wi+1][1]:en-0.01));}});}});
    {brand_anim}
    {chr(10).join(js)}
    window.__timelines=window.__timelines||{{}}; window.__timelines["shubz-{P['name']}"]=tl;
  }})();
  </script>
</div></body></html>"""
    return out

SFX_DUR = {}
def load_sfx_durations(audio_dir):
    for f in os.listdir(audio_dir):
        if f.endswith('.mp3'):
            d = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', os.path.join(audio_dir, f)], capture_output=True, text=True).stdout)
            SFX_DUR[f[:-4]] = d
