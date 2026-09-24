# Reverse engineering — Video Workflow Demo (Opus 5.5, AI voice)

## Request

Make another version that does **not** use the supplied audio recordings: an AI voice
reads the script. Save it as a separate output, and do not edit or rewrite
`../video-workflow-demo-opus-5-5/Video-Workflow-Demo-Opus-5.5.mp4`.

The original MP4's SHA-256 was recorded before this work began. It was re-verified
afterwards and is unchanged (`b0cceb0c…a524`). The original project folder was only
read: this version cloned assets from it and copied its build script.

## Voice

- **Model:** Kokoro v1.0 (ONNX), voice `af_heart`, speed 1.0. The model files were
  already in the HyperFrames cache. Its Python runtime was installed into a
  workspace-local venv (`.context/tts-venv`). Everything ran locally: no cloud
  service, no uploads, no cost.
- **Text:** the script, verbatim, one file per sentence (23 sentences). `[PLAY VIDEO]`
  is a stage direction and is not read. One pronunciation hint is sent to the
  model: "Hyper Frames". Kokoro reads "Fal" as one word (/fæl/, rhymes
  with "pal"), checked from its phonemes. A first try used "fal," with a comma, which
  added an unnatural stop. That sentence was regenerated exactly as scripted.
- **Because the AI reads the script**, Step 8 now uses the script's wording ("…is human
  realism, especially improving natural movement, hands, eye direction, and longer
  scenes with people"), and Step 4 says "I'm". The original-voice version differs from
  the script in both places.
- **Processing:** the same gentle compressor and limiter as the original version,
  plus +8.1 dB clip gain.

## Timing

1. **Placement** (`voice_plan.py`): sentences inside a chapter have 0.45 s between
   them. Between chapters, the original edit's pauses are reused (0.6–1.4 s). The
   Kite video starts 0.5 s after "…that workflow." and plays its full 36 s. Step 8
   starts 1.02 s after it, as before. Result: 2:56.2 (2:56.7 before the UI fix).
2. **Word timing:** whisper.cpp tokens for each sentence were fitted to the measured
   speech extent. Pauses were snapped to measured silences, preferring punctuation.
3. **Re-timing the picture** (`warp.py`): the original edit is built on its own
   clock (`build_edit.py`, unchanged). It is then mapped onto the new clock with a
   piecewise-linear warp. The warp's anchors are words that match between the
   original and AI narration, spaced ≥ 0.9 s apart to avoid jitter. 22 cue words that
   trigger highlights or cuts are pinned exactly: simple, short, examples, pacing,
   initial, campaign, expands, precise, instead, Fal, cinematic, idea, final,
   timing, transitions, audio, output, considering, reverse, key, file, marked. The
   Kite section is a pure shift. Step 8's list beats are re-keyed by hand to the new
   wording: breadcrumb on "human realism", generated take on "especially…", hands on
   "hands", eyes on "eye direction", page on "and longer scenes".
4. Footage that played in real time stays real time (source ranges re-derived).
   Slowed/sped shots, holds, camera moves, highlights, and chips follow the warp.
   Captions are rebuilt from the AI word timings, with the same phrase splits (69).

## Result and checks

- `Video-Workflow-Demo-Opus-5.5-AI-Voice.mp4`: H.264 1920×1080, 30 fps, 5285 frames,
  176.2 s, AAC 48 kHz stereo. The full decode passed.
- Loudness: −15.18 LUFS integrated, −3.3 dBTP (`checks/final-loudness.json`). The
  first export measured −13.3 LUFS because the mono voice plays on both channels
  (+3 LU); voice gain was lowered accordingly.
- The project contains 24 audio layers: 23 AI-narration sentences plus the Kite
  soundtrack. All footage layers are muted. No original narration asset is packaged
  (checked in `project inspect`).
- The delivered MP4 was re-transcribed per chapter
  (`transcripts/final-render-transcript.txt`). It matches the script word for word.
  The transcriber's spellings ("hyper frames", "FAL", "move") are its own
  rendering of the correct words; the isolated sentence transcribes as "moved".
- Highlight times against the AI words: every highlight is within about 0.25 s
  of its word, and most are within 0.1 s.
- Visual: a 4-second contact sheet of the encoded MP4, plus stills of the Step 8
  beats (breadcrumb highlight, hands, eyes, page).

## Limits

- The agent cannot listen. Voice naturalness, pronunciation of "Conductor" / "Fal" /
  "HyperFrames", and pacing were judged from transcripts, phonemes, and levels.
  Please listen.
- Kokoro is a small open model. It sounds clearly synthetic next to a human take.
  The hands (0.9 s) and eyes (1.0 s) close-ups in Step 8 are brief, because the
  script lists those words quickly.
- The Step 2 "send" click now happens about 0.7 s before "short request", because
  that shot plays in real time from the first frame of the recording and the AI
  narration reaches that line later than the original take did.

## Revision: "UI" pronunciation fix

The first delivery sent "U.I." to the voice. The periods made Kokoro read the letters
separately, with a 0.57 s break ("U… I"); the transcriber heard "U, I". The sentence is
now sent with plain "UI" (phonemes /juː ˈaɪ/, one smooth "you-eye"). Three variants
were compared ("U.I.", "UI", "U I"). Plain "UI" has no internal gap and
re-transcribes as "UI".

- Only `V4b-2` was regenerated; the other 22 sentence files are byte-identical to before.
  The sentence is 0.46 s shorter, so everything after it moves 0.46 s earlier.
- The project was rebuilt from `create_project.sh`, re-timed through the same warp, and
  re-exported. The highlights on this line still land on their words: "HyperFrames"
  69.1 s (word 69.27), "precise" 71.29 (71.30), "instead" 74.03 (74.02).
- The render re-transcribes as "…precise text, UI, and layout instead of generative
  footage." Loudness: −15.18 LUFS, −3.3 dBTP.
- The previous render and project are kept in `Versions/` (`*-before-UI-fix.*`).
- The original-voice MP4 and the AI voice v2 deliverables were re-verified unchanged (SHA-256).
