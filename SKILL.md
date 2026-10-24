---
name: shubz-edit
description: Edit a $hubzTrader talking-head trading video in the house style — tightened cut (silences/asides removed), studio LUT, zoom cuts, black + gold brand theme from shubztrader.com, word-synced motion-graphic cards with tasteful 3D, karaoke gold-box Hinglish captions, royalty-free music bed and synced SFX — rendered with HyperFrames at 1920x1080 30fps. Use when the user says "shubz edit", "edit this in my style", "ShubzTrader style", "same style as One Trade Away / C9010", or hands over a new trading video to edit like the last one.
---

# $hubzTrader edit style (v3 — build: C9010 preview v2)

Reference build: `~/Desktop/One Trade Edit/C9010_HF/` (raw camera file → tightened, graded, zoom cuts, 3D cards, captions v2, music + SFX).
`assets/reference-composition.html` is that composition as a template (`__WORDS__` and `__SFX__` placeholders).
**Start every new edit from it**: keep `<style>` tokens, helpers (`swingIn`, `rise`, `shine`, `exitCard`), zoom engine, caption engine, brand chip and audio block; replace only the cards, zoom list and SFX list.
`scripts/make_cut_v2.py` (pause detection on the ENHANCED voice, start on first syllable, Honey grade, ffmpeg graph), `scripts/build_v2.py` (word-anchored SFX + splices `assets/timeline_v2.js` into the template) are the exact scripts used — copy and adapt. `timeline_v2.js` anchors every cue to spoken words via `W("word", n)` (n-th occurrence) so timing survives any re-cut; update the word/occurrence keys for new scripts.

## Inputs to confirm (ask only what's missing)
1. Video file path (required).
2. Range: default = first ~60 s (after cuts) as a preview; after approval, the rest in ~60 s sections with the same look.
3. Episode title for the brand chip (default: topic from the transcript; else file name).
Everything else is fixed — don't re-ask about colors, fonts, captions, music, ratio or fps. Downloading NEW music still needs the user's OK (the two approved Mixkit tracks are already in `assets/audio/`).

## House style (locked)
- **Tokens** (shubztrader.com CSS): bg `#050505`, cards `#16171b→#0a0a0a` (OPAQUE), gold `#D4AF37`, gold-hi `#F3D675`, gold-lo `#8A681F`, gradient `135deg #8a681f, #d4af37 30%, #f3d675 50%, #c79a2b 70%, #8a681f`, text `#F7F7F5`, cream `#F5F1E8`, muted `#9A9A9A`, border `rgba(212,175,55,.22)`, green `#10b981`, red `#ef4444`.
- **Type**: Plus Jakarta Sans 800 UPPERCASE headlines with gold-gradient keywords; Inter body; gold uppercase kicker with glowing dot.
- **Cards**: radius 18, gold border + top hairline, deep shadow, shine sweep on emphasis. Full-screen graphics: radial black + faint 64px gold grid. Light vignette on the footage.
- **3D (tasteful)**: perspective on every card host; cards swing in on rotationY / flip down on rotationX; step tiles and list rows flip in; extruded gold numerals (layered back copy + gradient front); full-screen panels are tilted planes (rotateX/Y) that slowly dolly flatter; hero element lifts on z. No cartoon/bouncy 3D, no spinning logos.
- **Captions v2**: bottom centre (top 902px), Plus Jakarta 800 54px uppercase, 2–4 words/chunk (≤22 chars, break on punctuation or >0.45 s gap). Upcoming words 42% white → active word in a gold-gradient box with black text (pop 1.12→1) → spoken words white, keywords stay `#F3D675`. Words exactly as spoken (Hinglish, Roman script).
- **Zoom cuts**: inner `#zoom` (origin 50% 30%) — hard punch-in 1.12–1.28 alternating with 1.0 at each jump cut, slow push-ins (1.06–1.1) on emphasis lines, never zoom during split-screen. Split-screen = `#video-wrap` `x: 480`.
- **Audio**: voice cleaned + enhanced (see v3); music bed sidechain-ducked ~10 dB under the voice (see v3); SFX from `assets/audio` (Pixabay licence, no credit needed) at 0.2–0.45 volume: whoosh-short on card entries, whoosh on full-screen/split transitions, click on step activations, click-soft on list rows, ping on bars/data points, pop on chips/key words, sparkle on highlights, impact-bass-1 on big reveals, error on strike-throughs. Final mix ≈ -14 LUFS, peaks < -1 dB.
- Canvas 1920×1080, 30 fps.

## v3 upgrades (user feedback 2026-10-21 — always apply)
- **Start on the first word**: edit begins at the first voiced syllable (drop clicks/breaths before it); the hook card is on screen from frame 1.
- **Graphics never on the face**: side cards ≤ 670 px wide (left x 48–718, right x 1260–1860). Framing engine on `#zoom`: while a LEFT card shows → scale 1.12/1.2 with x +110/+125 (face pushed right); RIGHT card → x −110/−125; no card → 1.0 ↔ 1.24 punch-ins at cuts; split/full-screen → 1.0. Smooth 0.55 s reframe when a card enters/leaves, hard cuts on jump cuts. Always verify with snapshots at card + punch-in moments.
- **Voice clean-up + enhancement** (removes birds/chickens/room noise): ffmpeg chain in `assets/voice-chain.txt` — highpass 80 → `arnndn` with `assets/models/cb.rnnn` (conjoined-burgers; NOT sh.rnnn, it eats soft words) → light afftdn → gentle agate → EQ (−2.5 dB @220 Hz, +3 dB @3.2 kHz, +2 dB @9.5 kHz) → deesser → acompressor 3.2:1 + 5 dB makeup → limiter; cut audio loudnorm I=−15. Process the whole raw range BEFORE cutting.
- **Cinematic grade**: `assets/luts/Honey_LUT.cube` (FreeVisuals free 10 Cinematic LUTs pack, Rec.709, commercial use OK) blended at 85% over the original (`split → lut3d → blend all_opacity=0.85`). The old ShubzTrader_Studio_Grade LUT was rejected.
- **Music**: "Drawing the Sky" — Eugenio Mininni (Mixkit, YouTube OK, no credit) in `assets/audio/music-drawing-the-sky-mixkit.mp3`; loudnorm I=−21, sidechain-ducked under the voice (threshold 0.07, ratio 2.4, attack 60, release 450) → bed ≈ −26 LUFS vs voice −15 (≈10 dB under; v1's 18 dB under was inaudible). Fade in 0.6 s, out 2.2 s. Final mix ≈ −15 LUFS, peaks < −1.5 dB.
- **GRADE — CURRENT (user-approved direction 2026-10-21): educational, NOT cinematic.** No creative/cinematic LUT. Use `assets/grade-educational.txt`: correction-first — partial white balance from a neutral wall (C9010 room: colorchannelmixer gg=1.064 bb=1.19 ≈70% toward neutral, keeps skin warm), exposure lift via curves (skin ≈ 54–60% luma, shadows not crushed, highlights ≤ ~85%), `vibrance=0.18`, saturation 1.03, light unsharp. Re-measure each new shoot (wall RGB, skin luma) and adjust the mixer gains/curve; vignette barely visible (0.14). Workflow: grade the video-only re-render and mux the already-cleaned audio.
- ~~Grade v3~~ (superseded): Honey at 65% + `curves=master='0/0.06 0.25/0.35 0.5/0.61 0.75/0.83 1/1',eq=saturation=1.06` — brighter, lifted shadows for educational content (85% Honey was too dark).
- **Music v3 (approved)**: loudnorm I=−22.6 before ducking (threshold 0.05) → bed ≈ −29 LUFS, ~13.5 dB under the voice. (−26 was "a little loud".)
- **Rooster / tonal animal noise**: RNNoise does NOT remove crows (they're harmonic like voice). Make a 0–5 kHz spectrogram of the raw audio and look for stacks of flat horizontal harmonics (~850–900 Hz fundamental). Crows in gaps → CUT them out (a crow at the very start reads as dead air). Crows over speech → pitch-track them (`scripts/detect_tonal_noise.py`, Goertzel on the 2nd harmonic) and apply time-gated `equalizer` notches at k·f0 (k=1..7, −32 dB) before the voice chain. Whisper may "hear" words inside a crow — trust the spectrogram/energy for the first-word onset.
- **Crow sweep is mandatory before delivery**: after the cut, scan the FINAL voice track (no music) in 7.5 s spectrogram strips (400–4000 Hz, gain 1, intensity map) and zoom on every flat horizontal bar / 2:1 harmonic pair. Crows in pauses → remove them from the existing cut list (don't re-detect pauses; remap word times instead of re-transcribing). Faint crow fragments under SPEECH → NEVER broad dips (a −20 dB 800–3300 Hz cut over 1.5 s made the voice audibly muffled — user complaint). Read the exact bar frequencies from a zoomed spectrogram and notch each harmonic surgically (H1 w≈50, H2 w≈90, H3 w≈120 Hz, −24…−28 dB) only for the bar's duration. Verify the 1–4 kHz level in that window didn't drop vs. neighbouring speech. Tiny tonal blips in pauses → duck volume to 0.06.
- **Card-host windows**: `data-start`/`data-duration` of every card host must be derived from the same word cues as the timeline (`build_v3.py` WIN table) — stale hard-coded windows show black screens/missing cards after a re-cut.
- Whisper can duplicate a block of words at one timestamp — drop entries sharing an identical start time.
- Re-transcribing cleaned audio can garble the last line — re-run Whisper on just that tail with a prompt of the expected words.

## Workflow
1. **Transcribe raw** (whole file, background): extract 16 kHz mono → `whisper-cli -m ~/.cache/claude-shorts/ggml-large-v3.bin -l en -ml 1 -sow -ojf --prompt "Hinglish in Roman script…"`. Show the user the transcript.
2. **Find cuts**: Whisper smears word timings across pauses, so measure pauses from audio energy (10 ms RMS, threshold = 20th percentile + 6 dB, runs ≥ 0.22 s). Remove each pause leaving 0.07 s each side. Remove off-script asides, false starts, retakes (re-transcribe a suspicious span alone to get exact boundaries). End the preview on a sentence end near 60 s.
3. **Render the cut** with one ffmpeg filter graph (trim/atrim per segment, 8 ms audio fades, `fps=30,scale=1920:1080,educational grade (see GRADE — CURRENT)`, x264 crf 17 `-g 30`). ffmpeg 8 syntax: `-/filter_complex file.txt`.
4. **Re-transcribe the cut** for exact caption/graphic timing; fix spellings (mahine, liye, kiya, bahut, pahunchne, Dekho, hoon; not `maine`="I"). Compute cut points on the edited timeline for zoom cuts.
5. **Plan ≥10 moments/min** on exact word timestamps; content only from what's said. Vary: extruded-numeral hook, tilted bar card, agenda w/ highlight, 3D step-flow, CTA pill, quote card, full-screen 3D data plane, split-screen flip list w/ strike-through, 3D dashboard line chart. Keep y ≥ 880 clear for captions; side cards ≤ 750px wide on the left (x 48–750) or right (x 1250–1860) so punch-ins don't hit the face.
6. **Build**: fill template (words + SFX tags; SFX auto-assigned to tracks 10+ so none overlap). Keep the template OUTSIDE `public/` (two composition files there = `multiple_root_compositions` error).
7. **Validate**: `node $L check public` → 0 errors; `node $L snapshot public --at …` → review contact sheets (face overlaps, empty card space, premature reveals).
   `L=~/.claude/plugins/cache/hyperframes/hyperframes/<ver>/skills/hyperframes/scripts/plugin-cli.mjs`
8. **Render**: `PRODUCER_BROWSER_GPU_MODE=hardware node $L render public --skill=talking-head-recut -o versions/raw_render.mp4 --fps 30`; check ebur128 loudness, music-bed level in an SFX-free span, sample frames; copy to `<Title> (ShubzTrader edit).mp4`; deliver with SendUserFile.

## Lessons
- Card backgrounds opaque; animate `#video-wrap` only with transforms; zoom on inner `#zoom`.
- SVG dash-drawn paths: `opacity:0` until the draw starts; chart area fills must not pre-reveal a later segment.
- No negative z-index; dark grids need visible cells (`#2c2d35` + faint gold border).
- Keep every delivered version in `versions/`.


## Full-length 4K edit (approved workflow, C9010 full video 2026-10-21)
Files in `full/` (copies of the C9010 build — adapt paths):
- **Audio first, whole file**: `raw_full.wav` → crow sweep (30 s spectrogram strips 500–3500 Hz, 4 per image + `crow_detect.py` row-continuity detector, thresholds v≥100, isolation≥20, ≥0.18 s; verify every hit with a zoomed crop; the detector misses some and over-flags speech) → `notch_full.py` (Goertzel-tracked surgical notches, 6 harmonics, narrow) → voice chain → `enh_full.wav`.
- **Cut**: pause detection on the enhanced audio + manual cuts for stumbles/retakes (e.g. "nahi nahi ruk") + end right after the last word. Split into ~60 s parts at sentence starts (`make_parts.py`; split inside a segment at the quietest 10 ms within ±0.3 s — seamless).
- **4K**: render graded footage per part at 3840×2160 30 fps (crf 13) straight from the raw; HyperFrames compositions stay 1920×1080 and render with `--resolution 4k --quality delivery` (DPR 2 → crisp 4K graphics, full 4K footage).
- **Graphics**: `gen.py` card library (title, quote, list, bars, flow, chips, pill, big, compare, timeline, grid, broker, chart, end) + `storyboards.py` (anchors `"word@approx_s"`, content only from what's said) + `build_parts.py` (spelling fixes, drop Whisper hallucinations like trailing "Thank you", Whisper duplicate blocks). Check every part on 960×540 proxies (`check` + snapshots at each card's peak) BEFORE the 4K render.
- **Music once, globally**: parts render without music; `final_assemble.sh` concatenates parts (-c copy), loops the bed with 4 s crossfades, ducks it with a voice-only key track padded to each part's rendered length, mixes, limiter.
- Real data from the user (e.g. broker screenshot volumes) → rebuild as a themed 3D panel with count-up; keep private columns blurred/"hidden". Never invent numbers.
- Last part gets a 3 s brand end card (emblem + $hubzTrader + episode tag).
