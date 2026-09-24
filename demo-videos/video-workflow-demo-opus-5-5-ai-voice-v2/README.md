# Video Workflow Demo — Opus 5.5, AI voice v2 (reference-matched)

The AI-voice demo re-voiced to match the read in
`../save-the-learnings-opus-5-5-ai-voice/Save-the-Learnings-Opus-5.5-AI-Voice.mp4`:
same voice, speed, sentence-by-sentence delivery, pauses, and mastering. No supplied
audio recording is used. The earlier versions (`../video-workflow-demo-opus-5-5/` and
`../video-workflow-demo-opus-5-5-ai-voice/`) were not modified.

| File | What it is |
|---|---|
| `Video-Workflow-Demo-Opus-5.5-AI-Voice-v2.mp4` | Final render: 3:03.7, 1920×1080, 30 fps, H.264 + AAC stereo, −15.5 LUFS / −3.3 dBTP |
| `Video-Workflow-Demo-Opus-5.5-AI-Voice-v2.tsrct` | Editable Tesseract project (footage, holds, 23 AI-narration clips, font embedded) |
| `Video-Workflow-Demo-Opus-5.5-AI-Voice-v2.reverse-engineering.md` | How the reference was matched, timing, checks, and limits |
| `Captions.srt` / `Script.txt` | Caption sidecar and the script as read |
| `Assets/` | `Source/` recordings, `AI-Voice/` (raw + mastered sentences), `Derived/`, `Holds/`, `Fonts/`. See `Assets/SOURCES.md` |
| `Previews/` | A 4-second contact sheet of the encoded MP4, and a poster frame |
| `.tesseract-work/` | `tts.py`, `script_lines.py`, `voice_plan.py`, `build_edit.py` + `warp.py`, `create_project.sh`, `rebuild.sh`, transcripts, and checks |

## Rebuild / re-export (from this folder)

```sh
/Users/joydimapilis/conductor/workspaces/video-generation-test/reykjavik/.context/tts-venv/bin/python .tesseract-work/tts.py
for f in Assets/AI-Voice/sentences/*.wav; do ffmpeg -y -i "$f" -af "aresample=48000,volume=6.5dB,alimiter=limit=0.8:attack=3:release=60:level=disabled" -c:a pcm_s24le "Assets/AI-Voice/processed/$(basename "$f")"; done
.tesseract-work/create_project.sh
(cd .tesseract-work && python3 voice_plan.py)
.tesseract-work/rebuild.sh
/Users/joydimapilis/conductor/workspaces/video-generation-test/reykjavik/demo-videos/scripts/tsrct export \
  --project Video-Workflow-Demo-Opus-5.5-AI-Voice-v2.tsrct --fps 30 --resolution 1080p \
  --output Video-Workflow-Demo-Opus-5.5-AI-Voice-v2.mp4
```
