# shubz-edit

Claude Code skill for editing $hubzTrader talking-head videos in the house style. See `SKILL.md` for the full style and workflow.

## Install on a new Mac

```bash
git clone https://github.com/maulinagargoje07/shubz-edit-skill ~/.claude/skills/shubz-edit
zsh ~/.claude/skills/shubz-edit/setup.sh
```

`setup.sh` installs ffmpeg, whisper-cpp, the Claude Code CLI, the HyperFrames plugin and the Whisper large-v3 model (~3 GB).

## Update

```bash
git -C ~/.claude/skills/shubz-edit pull
```

Music in `assets/audio` is from Mixkit / Pixabay — keep this repo private.
