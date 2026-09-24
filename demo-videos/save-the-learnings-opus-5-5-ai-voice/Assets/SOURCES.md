# Sources — Opus 5.5 AI-voice version

- Screen-Recording.mov: original user screen recording, a byte-identical copy of the attachment (SHA-256 018b26c8…b6aa).
- Hold-*.png: unaltered frames of that recording at 1.00, 7.10, 7.25, and 7.45 s
  (copied from the Opus 5.5 project's Assets).
- AI-Voice-af_heart-sentence-{1,2,3}-raw.wav: synthesized locally from `Script.txt`,
  one sentence per file. Model: Kokoro-82M v1.0 ONNX (Apache-2.0), voice
  `af_heart`, speed 0.92, lang en-us. Runtime: `kokoro-onnx` 0.4.7 with onnxruntime
  1.30.0 in a workspace-local venv (`.context/tts-venv`). Synthesis ran offline
  and nothing was uploaded. The script is `.tesseract-work/tts/synth.py`.
- AI-Voice-af_heart-sentence-{1,2,3}.wav: the files used in the edit. FFmpeg
  recipe: `aresample=48000,volume=6.5dB,alimiter=limit=0.8:attack=3:release=60:level=disabled`, 24-bit PCM mono.
- IBMPlexSans-Regular.ttf and IBMPlexSans-OFL.txt: caption font (SIL OFL 1.1).

The supplied narration recording (`Save the Learnings.m4a`) is **not** used or
embedded in this project. Alternate voice auditions (`af_heart` at 1.0× and
`am_michael` at 1.0×) remain in `.tesseract-work/tts/` for reference.
