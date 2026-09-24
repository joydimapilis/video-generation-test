# Save the Learnings — Opus 5.5 version (AI voice)

**This is the Opus 5.5 edit narrated by an AI voice.** The supplied voice
recording is not used. The picture design matches
`../save-the-learnings-opus-5-5/`, re-timed to the new read. That project and its
MP4 were not modified.

| File | What it is |
|---|---|
| `Save-the-Learnings-Opus-5.5-AI-Voice.mp4` | Final render: 20.2 s, 1920×1080, 30 fps, H.264 + AAC stereo, −15.6 LUFS / −4.0 dBTP |
| `Save-the-Learnings-Opus-5.5-AI-Voice.tsrct` | Editable Tesseract project, with the screen recording, AI-voice WAVs, holds, and font embedded |
| `Save-the-Learnings-Opus-5.5-AI-Voice.reverse-engineering.md` | Voice choice, processing, timing map, checks, and limits |
| `Captions.srt` / `Script.txt` | Caption sidecar and the supplied script |
| `Assets/` | Screen recording, raw and level-matched AI-voice WAVs, holds, font and license, and `SOURCES.md` |
| `Previews/` | Encoded filmstrip, heading match-cut strip, and poster |
| `.tesseract-work/` | `build_edit.py`, `rebuild.sh`, `tts/synth.py` plus voice auditions, JSON, and check reports |

The voice is Kokoro-82M `af_heart` at 0.92×, synthesized locally and offline,
one sentence per file with 0.50 s and 0.55 s pauses between sentences.

Re-export from the Reykjavik workspace root:

```sh
./scripts/tsrct export --project save-the-learnings-opus-5-5-ai-voice/Save-the-Learnings-Opus-5.5-AI-Voice.tsrct --fps 30 --resolution 1080p --output save-the-learnings-opus-5-5-ai-voice/Save-the-Learnings-Opus-5.5-AI-Voice.mp4
```

The delivered MP4 is this export, remuxed losslessly (`-c copy`) to add the title
tag "Save the Learnings — Opus 5.5 version (AI voice)".
