#!/bin/zsh
# One-time setup for the shubz-edit skill on macOS, Linux, or Windows (inside WSL).
# Run after the skill is in ~/.claude/skills/shubz-edit:
#   zsh ~/.claude/skills/shubz-edit/setup.sh
set -e

# Homebrew works on macOS and Linux and ships ffmpeg 8 + whisper-cpp on both
if ! command -v brew >/dev/null; then
  for b in /opt/homebrew/bin/brew /usr/local/bin/brew /home/linuxbrew/.linuxbrew/bin/brew; do
    [[ -x $b ]] && eval "$($b shellenv)" && break
  done
fi
command -v brew >/dev/null || { echo "Install Homebrew first: https://brew.sh"; exit 1; }

command -v node >/dev/null || brew install node
command -v python3 >/dev/null || brew install python
command -v ffmpeg >/dev/null || brew install ffmpeg
command -v whisper-cli >/dev/null || brew install whisper-cpp
command -v claude >/dev/null || npm install -g @anthropic-ai/claude-code

# HyperFrames plugin (renderer used by the skill)
claude plugin marketplace add heygen-com/hyperframes || true
claude plugin install hyperframes@hyperframes

# Whisper large-v3 model (~3 GB)
MODEL="$HOME/.cache/claude-shorts/ggml-large-v3.bin"
if [[ ! -f "$MODEL" ]]; then
  mkdir -p "${MODEL:h}"
  curl -L --fail -o "$MODEL.part" https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-large-v3.bin
  mv "$MODEL.part" "$MODEL"
fi

chmod +x "${0:A:h}"/scripts/*.sh "${0:A:h}"/full/*.sh
echo "shubz-edit is ready. Restart Claude and say: shubz edit <video>"
