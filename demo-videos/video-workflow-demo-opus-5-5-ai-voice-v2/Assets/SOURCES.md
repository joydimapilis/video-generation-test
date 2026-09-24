# Sources — Video Workflow Demo (Opus 5.5, AI voice v2)

The supplied narration recordings are **not used** and not included.

## AI-Voice/
- `sentences/*.wav` — the script, verbatim, one file per sentence, read by **Kokoro v1.0**
  (`~/.cache/hyperframes/tts`), voice **af_heart**, **speed 0.92**, lang en-us, via
  `kokoro-onnx` + onnxruntime 1.30 in `.context/tts-venv`. Synthesis ran locally and offline.
  The settings are identical to the Save-the-Learnings AI-voice reference. For the three
  sentences both scripts share (Step 6), the files are byte-identical to that project's
  `AI-Voice-af_heart-sentence-{1,2,3}-raw.wav`.
- `processed/*.wav` — the reference's mastering recipe:
  `aresample=48000,volume=6.5dB,alimiter=limit=0.8:attack=3:release=60:level=disabled` (24-bit, mono).
  Step 6 outputs are sample-identical to the reference's `AI-Voice-af_heart-sentence-{1,2,3}.wav`.
- `manifest.json` — the text and duration of each file.

## Source/, Derived/, Holds/, Fonts/
These are APFS clones of the same files used by the earlier versions: the screen recordings
(byte-identical to Desktop/Experiment), the Step 2 excerpts/time-lapse, the Kite soundtrack
with its pause removed, original-frame holds, and IBM Plex Sans Medium (+ SIL OFL 1.1).
No music, SFX, or generated footage was added.
