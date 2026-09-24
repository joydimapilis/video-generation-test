# Sources — Video Workflow Demo (Opus 5.5, AI voice)

The supplied narration recordings (`Desktop/Experiment/Audio/*.m4a`) are **not used** in
this version and are not included here. The narration is an AI voice reading the script.

## Source/ — original user files (APFS clones, byte-identical to /Users/joydimapilis/Desktop/Experiment)
- `Script & Structure.rtf` — the script (source of truth). Plain text: `../Script.txt`.
- `Step 2.mov` … `Step 8.mov` — screen recordings.

## AI-Voice/ — the narration
- Generated locally by **Kokoro v1.0** (`kokoro-v1.0.onnx`, the voice pack in `~/.cache/hyperframes/tts`),
  voice **af_heart** (American English), speed 1.0, via `kokoro-onnx` 0.x on onnxruntime 1.30. There was no cloud service and no cost.
  Script: `.tesseract-work/tts.py`. Text: `.tesseract-work/script_lines.py`.
- `sentences/*.wav` — one file per script sentence (24 kHz mono), exactly as generated.
  The text is the script, verbatim, with one pronunciation hint: "HyperFrames" → "Hyper Frames".
  ("UI" is sent as written; an earlier "U.I." hint split the letters and was removed.)
  `manifest.json` lists each file's text and duration.
- `processed/*.wav` — the same files (48 kHz, sample-aligned, 0 ms offset) with
  `acompressor=threshold=0.1:ratio=2.5:attack=5:release=150:knee=3:makeup=1,alimiter=limit=0.22:attack=2:release=60:level=false:latency=true`,
  so the mix reaches loudness without clipping. These are packaged in the .tsrct.

## Derived/ — shared with the original-voice version (clones of ../video-workflow-demo-opus-5-5/Assets/Derived)
- `Step2-request-src0-20s.mp4`, `Step2-timelapse-src17-1017s-60x.mp4`, `Step2-complete-src1012-end.mp4` — Step 2.mov excerpts / time-lapse.
- `Kite-soundtrack-pause-removed.wav` — the Kite video's own soundtrack from Step 7.mov, with the playback pause removed.

## Holds/ — unaltered single frames from the recordings (same as the original-voice version)

## Fonts/
- `IBMPlexSans-Medium.ttf` (used), plus Regular/Bold for reference, and `IBMPlexSans-OFL.txt` (SIL OFL 1.1).
  Source: https://github.com/IBM/plex

No music, SFX, or generated footage was added.
