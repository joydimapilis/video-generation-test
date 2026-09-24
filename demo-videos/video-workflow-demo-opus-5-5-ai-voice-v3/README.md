# Video Workflow Demo — Opus 5.5, AI voice v3 (ElevenLabs)

Version 3 of the AI-voice demo. The narration is an **ElevenLabs** voice (Bella, Eleven
Multilingual v2) reading the script. The picture edit, pacing, captions, and mix follow
the first AI-voice version (`../video-workflow-demo-opus-5-5-ai-voice/`, with its "UI" fix).
No supplied audio recording is used. All earlier versions are unchanged.

| File | What it is |
|---|---|
| `Video-Workflow-Demo-Opus-5.5-AI-Voice-v3.mp4` | Final render: 2:56.5, 1920×1080, 30 fps, H.264 + AAC stereo, −15.3 LUFS / −2.8 dBTP |
| `Video-Workflow-Demo-Opus-5.5-AI-Voice-v3.tsrct` | Editable Tesseract project (footage, holds, 23 narration clips, font embedded) |
| `Video-Workflow-Demo-Opus-5.5-AI-Voice-v3.reverse-engineering.md` | Voice, timing, checks, and limits |
| `Captions.srt` / `Script.txt` | Caption sidecar and the script as read |
| `Assets/` | `AI-Voice/`: ElevenLabs MP3s as returned, WAV decodes, mastered WAVs, and alignment. Plus `Source/`, `Derived/`, `Holds/`, `Fonts/`. See `Assets/SOURCES.md` |
| `Previews/` | A 4-second contact sheet of the encoded MP4, and a poster frame |
| `.tesseract-work/` | `elevenlabs_tts.py`, `voice_plan.py`, `build_edit.py` + `warp.py`, `create_project.sh`, `rebuild.sh`, transcripts, and checks |

## Rebuild / re-export (from this folder)

```sh
python3 .tesseract-work/elevenlabs_tts.py      # needs ELEVENLABS_API_KEY (sk_…); skips files that exist, so no characters are used
for f in Assets/AI-Voice/sentences/*.wav; do ffmpeg -y -i "$f" -af "aresample=48000,volume=2.2dB,alimiter=limit=0.708:attack=3:release=60:level=disabled" -c:a pcm_s24le "Assets/AI-Voice/processed/$(basename "$f")"; done
.tesseract-work/create_project.sh
(cd .tesseract-work && python3 voice_plan.py)
.tesseract-work/rebuild.sh
/Users/joydimapilis/conductor/workspaces/video-generation-test/reykjavik/demo-videos/scripts/tsrct export \
  --project Video-Workflow-Demo-Opus-5.5-AI-Voice-v3.tsrct --fps 30 --resolution 1080p \
  --output Video-Workflow-Demo-Opus-5.5-AI-Voice-v3.mp4
```

To redo one sentence (for example, after a wording or pronunciation change), run
`python3 .tesseract-work/elevenlabs_tts.py --force V4c-1`.
