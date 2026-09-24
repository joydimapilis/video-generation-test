# Video Workflow Demo — Opus 5.5, AI voice

This version of the demo uses an **AI voice reading the script**. It does not use
the supplied audio recordings. The picture edit, captions style, highlights, and
Kite video are the same as the original-voice version in
`../video-workflow-demo-opus-5-5/`. That version was not modified.

| File | What it is |
|---|---|
| `Video-Workflow-Demo-Opus-5.5-AI-Voice.mp4` | Final render: 2:56.2, 1920×1080, 30 fps, H.264 + AAC stereo, −15.2 LUFS / −3.3 dBTP ("UI" pronunciation fixed) |
| `Video-Workflow-Demo-Opus-5.5-AI-Voice.tsrct` | Editable Tesseract project (footage, holds, one AI-narration clip per sentence, and the font are embedded) |
| `Video-Workflow-Demo-Opus-5.5-AI-Voice.reverse-engineering.md` | How it was made: voice, timing warp, checks, and limits |
| `Captions.srt` | Caption sidecar (captions are also burned in) |
| `Script.txt` | The script, as read by the AI voice |
| `Assets/` | `Source/`: original recordings. `AI-Voice/`: generated narration. `Derived/`, `Holds/`, `Fonts/`. See `Assets/SOURCES.md` |
| `Previews/` | A 4-second contact sheet of the encoded MP4, and a poster frame |
| `Versions/` | The render and project from before the "UI" pronunciation fix |
| `.tesseract-work/` | `tts.py`, `voice_plan.py`, `build_edit.py` + `warp.py`, `create_project.sh`, `rebuild.sh`, transcripts, and checks |

## Rebuild / re-export (from this folder)

```sh
/Users/joydimapilis/conductor/workspaces/video-generation-test/reykjavik/.context/tts-venv/bin/python .tesseract-work/tts.py   # regenerate the voice (optional)
# re-run the processing command in Assets/SOURCES.md if the voice was regenerated
.tesseract-work/create_project.sh          # recreate the .tsrct and package assets
(cd .tesseract-work && python3 voice_plan.py)
.tesseract-work/rebuild.sh                 # build the edit, re-time it to the AI voice, commit
/Users/joydimapilis/conductor/workspaces/video-generation-test/reykjavik/demo-videos/scripts/tsrct export \
  --project Video-Workflow-Demo-Opus-5.5-AI-Voice.tsrct --fps 30 --resolution 1080p \
  --output Video-Workflow-Demo-Opus-5.5-AI-Voice.mp4
```
