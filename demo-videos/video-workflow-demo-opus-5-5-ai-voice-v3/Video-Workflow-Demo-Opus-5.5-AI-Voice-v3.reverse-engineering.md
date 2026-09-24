# Reverse engineering — Video Workflow Demo (Opus 5.5, AI voice v3, ElevenLabs)

## Request

Create version 3, narrated with ElevenLabs using `ELEVENLABS_API_KEY` from the environment.

The first two attempts failed: the variable held the key's ID, not the `sk_…` secret.
Nothing was generated then. After the key was updated, authentication succeeded
(free plan, 49 of 10,000 characters used at the start).

## Base

Version 3 starts from the version the user preferred: the first AI-voice version, including
its "UI" fix. It keeps the same edit (`build_edit.py`), the same re-timing method
(`warp.py`), and the same pacing: 0.45 s between sentences (0.25 s after "Hi everyone."),
the original chapter gaps, and the Kite video in full. Only the voice source changes.

## Voice

- ElevenLabs **Bella — Professional, Bright, Warm** (American), model
  **eleven_multilingual_v2**, stability 0.5 / similarity 0.75 / style 0 / speaker boost /
  speed 1.0. Chosen from the account's 21 premade voices as the closest match to the warm,
  bright American voice of the preferred version, and it is tagged for explainer narration.
- One request per sentence (23), with the chapter's other sentences as `previous_text` /
  `next_text`, so each sentence keeps the intonation it would have in context.
- The text is the script, verbatim. The alignment shows "Fal" said as one word (0.35 s, not
  spelled out), "UI" as one "you-eye" (0.50 s), and "HyperFrames" and "Conductor" as single words.
- Mastering: +2.2 dB and a −3 dBFS peak limiter, no compression. ElevenLabs' read is
  already even (−20.0 LUFS raw).

## Timing

Word timings come from **ElevenLabs' own character alignment**, not the transcriber. The
first and last words are clamped to the measured audio, because the final period's timing
runs into the trailing silence. This makes cue timing tighter than in the Kokoro versions:
every highlight lands on its cue word or up to 0.15 s before it. The one exception is
"status: complete", which lands 0.29 s before "complete", on "considering… complete",
as in the original edit. Two word-form aliases were
added to the warp: ElevenLabs keeps "reverse-engineering" as one word, and "HyperFrames"
and "UI" are no longer split.

## Result and checks

- `Video-Workflow-Demo-Opus-5.5-AI-Voice-v3.mp4`: H.264 1920×1080, 30 fps, 5294 frames,
  176.5 s, AAC 48 kHz stereo. The full decode passed. **−15.26 LUFS, −2.84 dBTP.**
- Every sentence was transcribed on its own, and the delivered MP4 per chapter
  (`transcripts/final-render-transcript.txt`). Both match the script. The transcriber's
  spellings "FAL" and "hyperframes" refer to the correct words.
- Audio layers: 23 ElevenLabs sentences plus the Kite soundtrack. Footage is muted, and
  no supplied narration is packaged.
- The API key is not in any project file or log (text scan: 0 matches).
- The original-voice MP4, AI voice v1, and AI voice v2 deliverables were verified
  unchanged (SHA-256).
- Visual: a 4-second contact sheet of the encoded MP4.

## Limits

- The agent cannot listen. Voice choice and naturalness were judged from ElevenLabs
  metadata, transcripts, alignment, and levels. Please listen, and ask if you'd prefer
  another voice. The script uses about 1,900 characters per full re-voice, and the free
  plan has 10,000.
- Free-plan ElevenLabs audio carries attribution and no commercial license. Upgrade
  or check the terms before publishing commercially.
- As in version 1, the Step 2 "send" click comes slightly before "short request".
