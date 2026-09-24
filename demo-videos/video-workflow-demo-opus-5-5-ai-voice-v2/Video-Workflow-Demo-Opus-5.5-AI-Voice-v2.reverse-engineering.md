# Reverse engineering — Video Workflow Demo (Opus 5.5, AI voice v2)

## Request

Re-voice the AI-voice demo so it copies the pacing, intonation, and word delivery of
`save-the-learnings-opus-5-5-ai-voice/Save-the-Learnings-Opus-5.5-AI-Voice.mp4`.

## What the reference does (read from its project notes, synth script, and timing file)

| Aspect | Reference | AI voice v1 (previous) | This version |
|---|---|---|---|
| Voice | Kokoro v1.0 `af_heart` | `af_heart` | `af_heart` |
| Speed | **0.92×** | 1.0× | **0.92×** |
| Text sent to the model | script verbatim, one file per sentence | script with hints ("Hyper Frames", "U.I.", and "fal," in one draft) | **script verbatim**, one file per sentence |
| Pause between sentences (speech to speech) | 0.50 s, then 0.55 s | 0.45 s | **0.50 s after a chapter's first sentence, 0.55 s after later ones** |
| Mastering | +6.5 dB, peak limiter at −1.9 dBFS, no compression | 2.5:1 compressor + limiter | **+6.5 dB, same limiter, no compression** |
| Layer gain in the mix | −2.2 dB (mono on both channels) | +8.1 dB (after compression) | **−2.2 dB** |

The intonation and word delivery come from the model, voice, speed, and the exact text
(punctuation drives Kokoro's phrasing). This version uses the same settings and the
script text as written. The pronunciation hints were dropped after checking the
phonemes: the plain script already reads "HyperFrames" as /haɪpɚ freɪmz/, "UI" as
/juː aɪ/, "Fal" as /fæl/, and "Conductor" correctly. The v1 compressor was also
removed, because it flattened the natural rise and fall of the read.

Chapter-to-chapter pauses still follow the original edit (0.6–1.4 s), because the
reference has only one chapter. The Kite video plays in full between Steps 7 and 8.

## Proof of match

- Step 6 of this video reads the same three sentences as the reference. The raw WAVs
  are **byte-identical**, and the mastered WAVs are **sample-identical** (max difference 0).
- Their placement (file starts 0 / 5.42 / 12.65 s) is identical to the reference.
- The Step 6 section of the rendered MP4 matches the reference MP4's narration with
  an energy-envelope correlation of **0.982**.

## Timing

`voice_plan.py` places the sentences. `build_edit.py` lays out the original edit, and
`warp.py` re-times it onto the new read. The warp uses word-matched anchors spaced
≥ 0.9 s apart, plus 22 pinned cue words (the Fal pin accepts whisper's spellings
"fall"/"file"). Real-time footage stays real time, and the Kite section is a pure
shift. Step 8's list beats are keyed to "human realism / especially… / hands /
eye direction / and longer scenes". The slower read makes the video 7 s longer
(3:03.7). Every highlight lands on its cue word or up to 0.4 s before it.

## Checks

- MP4: H.264 1920×1080, 30 fps, 5511 frames, 183.7 s, AAC 48 kHz stereo. The full
  decode passed. −15.54 LUFS, −3.32 dBTP.
- The per-chapter re-transcription of the MP4 matches the script
  (`transcripts/final-render-transcript.txt`). Whisper spells the /fæl/ as "fowl"
  and "moved" as "move"; these are transcriber spellings.
- No supplied narration asset is packaged. The earlier Opus MP4, the AI-voice v1
  MP4/.tsrct, and the reference project were verified unchanged (SHA-256).

## Limits

- The agent cannot listen. The match was established by identical synthesis settings,
  identical bytes on the shared sentences, and envelope correlation, not by ear.
- Kokoro's pronunciation of "Fal" (/fæl/, as in "pal") may sound like "fall" to some listeners.
  Changing it would mean departing from the verbatim text.
