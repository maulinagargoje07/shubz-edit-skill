#!/bin/zsh
cd "/Users/rajakumarmishra/Desktop/One Trade Edit/C9010_HF/parts"
L=~/.claude/plugins/cache/hyperframes/hyperframes/0.8.181/skills/hyperframes/scripts/plugin-cli.mjs
for k in 1 2 3 4 5 6 7 8 9; do
  until grep -q "part $k done" render_inputs.log; do sleep 10; done
  ffmpeg -v error -y -i p${k}_video4k.mp4 -i p${k}_voice.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 320k -ar 48000 -shortest -movflags +faststart p${k}/public/input-video.mp4
  echo "render p$k start $(date +%T)"
  PRODUCER_BROWSER_GPU_MODE=hardware node $L render p${k}/public --skill=talking-head-recut --resolution 4k --quality delivery --fps 30 -o out_p${k}_4k.mp4 2>&1 | grep -E "MB|rror|Error"
  echo "render p$k done $(date +%T)"
done
echo ALLDONE
