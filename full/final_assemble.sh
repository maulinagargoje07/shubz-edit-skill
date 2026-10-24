#!/bin/zsh
set -e
cd "/Users/rajakumarmishra/Desktop/One Trade Edit/C9010_HF/parts"
OUT="../C9010 - FULL EDIT 4K (ShubzTrader).mp4"
rm -f concat.txt; : > concat.txt
for k in 1 2 3 4 5 6 7 8 9; do echo "file 'out_p${k}_4k.mp4'" >> concat.txt; done
# 1) join parts losslessly
ffmpeg -v error -y -f concat -safe 0 -i concat.txt -c copy joined.mp4
TOT=$(ffprobe -v error -show_entries format=duration -of csv=p=0 joined.mp4)
echo "joined duration $TOT"
# 2) voice-only key track aligned to each rendered part (pad each part's voice to its rendered length)
rm -f keyparts.txt; : > keyparts.txt
for k in 1 2 3 4 5 6 7 8 9; do
  D=$(ffprobe -v error -show_entries format=duration -of csv=p=0 out_p${k}_4k.mp4)
  ffmpeg -v error -y -i p${k}_voice.wav -af "apad,atrim=0:$D" -ar 48000 -ac 1 key_p${k}.wav
  echo "file 'key_p${k}.wav'" >> keyparts.txt
done
ffmpeg -v error -y -f concat -safe 0 -i keyparts.txt -c pcm_s16le key_full.wav
# 3) music bed: Drawing the Sky looped x3 with 4s crossfades, levelled, ducked under the voice, faded
M=../audio/mixkit-606.mp3
ffmpeg -v error -y -i $M -i $M -i $M -filter_complex "[0][1]acrossfade=d=4:c1=tri:c2=tri[a];[a][2]acrossfade=d=4:c1=tri:c2=tri[b]" -ar 48000 bed_loop.wav
FADE=$(echo "$TOT - 3.5" | bc)
ffmpeg -v error -y -i bed_loop.wav -i key_full.wav -filter_complex "[0:a]atrim=0:$TOT,asetpts=PTS-STARTPTS,loudnorm=I=-22.6:TP=-4:LRA=7,aresample=48000[m];[1:a]aresample=48000,pan=stereo|c0=c0|c1=c0,highpass=f=120[sc];[m][sc]sidechaincompress=threshold=0.05:ratio=2.4:attack=60:release=450:makeup=1[d];[d]afade=t=in:d=0.6,afade=t=out:st=$FADE:d=3.5[out]" -map "[out]" -ar 48000 bed_final.wav
# 4) mix: parts audio (voice + SFX) + music bed; keep video stream untouched
ffmpeg -v error -y -i joined.mp4 -i bed_final.wav -filter_complex "[0:a]aresample=48000[v];[1:a]aresample=48000[m];[v][m]amix=inputs=2:duration=first:normalize=0,alimiter=limit=0.89:level=false[a]" -map 0:v -map "[a]" -c:v copy -c:a aac -b:a 320k -movflags +faststart "$OUT"
ffprobe -v error -show_entries stream=codec_type,width,height,r_frame_rate:format=duration,size -of compact "$OUT"
ffmpeg -hide_banner -i "$OUT" -af ebur128=framelog=quiet -f null - 2>&1 | grep -E "^\s+(I|LRA):"
ffmpeg -hide_banner -i "$OUT" -af volumedetect -f null - 2>&1 | grep max_volume
echo FINAL_OK
