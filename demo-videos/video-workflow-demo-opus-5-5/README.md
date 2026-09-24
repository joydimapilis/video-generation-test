# Video Workflow Demo — Opus 5.5

A Tesseract recreation of the CapCut product demo, edited by Claude Opus 5.5 from
`/Users/joydimapilis/Desktop/Experiment`. It is a new project; no earlier Astra or
Opus project was modified.

| File | What it is |
|---|---|
| `Video-Workflow-Demo-Opus-5.5.mp4` | Final render: 2:56.7, 1920×1080, 30 fps, H.264 + AAC stereo, −15.6 LUFS / −1.5 dBTP |
| `Video-Workflow-Demo-Opus-5.5.tsrct` | Editable Tesseract project (all footage, holds, narration, and the font are embedded) |
| `Video-Workflow-Demo-Opus-5.5.reverse-engineering.md` | Cut map, take choices, audio/caption decisions, revisions, checks, and limits |
| `Captions.srt` | Caption sidecar (captions are also burned in as editable text layers) |
| `Script.txt` | The supplied script (plain text) |
| `Assets/` | `Source/`: byte-identical originals. `Derived/`: Step 2 excerpts/time-lapse, compressed narration, Kite soundtrack. `Holds/`: original frames. `Fonts/`: IBM Plex Sans + OFL. See `Assets/SOURCES.md` |
| `Previews/` | A 4-second contact sheet of the encoded MP4, and a poster frame |
| `.tesseract-work/` | `plan.py` (take list + timeline), `build_edit.py` (whole timeline), `create_project.sh`, `rebuild.sh`, transcripts, and check reports |

## Rebuild / re-export

From this folder:

```sh
.tesseract-work/create_project.sh      # only if recreating the .tsrct from scratch
.tesseract-work/rebuild.sh             # regenerate the timeline from build_edit.py
/Users/joydimapilis/conductor/workspaces/video-generation-test/reykjavik/demo-videos/scripts/tsrct export \
  --project Video-Workflow-Demo-Opus-5.5.tsrct --fps 30 --resolution 1080p \
  --output Video-Workflow-Demo-Opus-5.5.mp4
```
