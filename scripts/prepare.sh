#!/bin/zsh
# Prepare a talking-head clip for a $hubzTrader-style HyperFrames edit.
# Usage: prepare.sh <input-video> <project-dir> [start-sec] [duration-sec]
# Produces: <project>/public/{input-video.mp4,fonts,img,vendor}, transcript/words.json,
#           transcript/words_compact.json, transcript/sheet.jpg (1 frame/sec contact sheet)
set -e
IN="$1"; PROJ="$2"; SS="${3:-0}"; DUR="${4:-}"
SKILL="${0:A:h:h}"
MODEL="$HOME/.cache/claude-shorts/ggml-large-v3.bin"
[[ -z "$IN" || -z "$PROJ" ]] && { echo "usage: prepare.sh <video> <project-dir> [start] [duration]"; exit 1; }
mkdir -p "$PROJ/public" "$PROJ/transcript"
cp -R "$SKILL/assets/fonts" "$SKILL/assets/img" "$SKILL/assets/vendor" "$PROJ/public/"
T=(); [[ -n "$DUR" ]] && T=(-t "$DUR")
# 1080p30 with a keyframe every second (renderer seeks per frame)
ffmpeg -v error -y -ss "$SS" "${T[@]}" -i "$IN" -vf "scale=1920:1080:flags=lanczos,fps=30" \
  -c:v libx264 -crf 18 -preset fast -g 30 -keyint_min 30 -pix_fmt yuv420p -movflags +faststart \
  -c:a aac -b:a 256k "$PROJ/public/input-video.mp4"
ffmpeg -v error -y -i "$PROJ/public/input-video.mp4" -ar 16000 -ac 1 "$PROJ/transcript/audio16k.wav"
whisper-cli -m "$MODEL" -f "$PROJ/transcript/audio16k.wav" -l en -ml 1 -sow -ojf -t 8 \
  -of "$PROJ/transcript/whisper" \
  --prompt "Hinglish in Roman script. Dekho guys, main aapko bataunga, ek trade, successful trader, beginner's luck, entry, exit, execution, stop loss, risk." >/dev/null 2>&1
/usr/bin/python3 - "$PROJ/transcript" <<'PY'
import json, sys
d = sys.argv[1]
j = json.load(open(f"{d}/whisper.json"))
w = [{"text": s["text"].strip(), "start": round(s["offsets"]["from"]/1000, 2), "end": round(s["offsets"]["to"]/1000, 2)}
     for s in j["transcription"] if s["text"].strip()]
json.dump(w, open(f"{d}/words.json", "w"), indent=1, ensure_ascii=False)
json.dump([[x["text"], x["start"], x["end"]] for x in w], open(f"{d}/words_compact.json", "w"), ensure_ascii=False, separators=(",", ":"))
print(f"{len(w)} words")
PY
DURS=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$PROJ/public/input-video.mp4")
ROWS=$(( (${DURS%.*} + 5) / 6 + 1 ))
ffmpeg -v error -y -i "$PROJ/public/input-video.mp4" -vf "fps=1,scale=320:-1,tile=6x${ROWS}" -frames:v 1 "$PROJ/transcript/sheet.jpg"
echo "duration=$DURS  -> $PROJ"
