# Reverse engineering — Save the Learnings (Opus 5.5, AI voice)

A second Opus 5.5 deliverable. It keeps the same brief, screen recording, script,
and picture design as `../save-the-learnings-opus-5-5/`, but the supplied voice
recording is replaced by an AI voice reading the script. It is a separate
project; the earlier Opus 5.5 MP4 and project were not modified (SHA-256 re-checked).

## Voice

- Engine: Kokoro-82M v1.0 (ONNX, Apache-2.0), run locally from the cached model
  in a workspace-local venv. No cloud service, upload, or voice cloning.
- Auditions: `af_heart` at 1.0× (15.8 s of speech), `af_heart` at 0.92× (16.7 s),
  and `am_michael` at 1.0× (17.9 s). All three re-transcribed word-for-word with local whisper.
- Chosen: `af_heart` at 0.92×. It is Kokoro's highest-rated English voice, and
  the slightly slower pace gives each listed item enough time for its heading cut.
- Each sentence was synthesized separately, so the pauses between sentences are
  editorial choices (0.50 s and 0.55 s, speech to speech) rather than model timing.
  Commas inside sentences keep the model's natural phrasing.
- Level: +6.5 dB with a transparent peak limiter (−1.9 dBFS), 48 kHz. The raw TTS
  was −22.3 LUFS, and sentence 1 had two clipped samples on "every". In Tesseract
  the three mono files sit at −2.2 dB, because mono plays on both stereo channels.

## Timing (edit seconds)

| Edit | Picture | Voice |
|---|---|---|
| 0–5.40 | Screen 0–2.8 s at 0.52× (static page), push-in 0.65–3.15 s; path highlight at 3.46 s | Sentence 1 at 0.45 s ("reverse" ≈3.51) |
| 5.40–8.61 | Real scroll, screen 2.8–7.1 s at 1.34×, lands on "Prompts" | Sentence 2 at 5.87 s |
| 8.61 / 9.21 / 9.93 / 10.89 | Heading match cuts: Prompts, Structure, Models and methods, Revisions | "prompts" 8.67, "structure" 9.27, "methods" 9.99, "revisions" 10.95 |
| 11.79–20.20 | Final learnings, then a 13.05–14.35 s camera move to the file tree; file highlight at 14.86 s, grows to `final_outcome` at 15.68 s; fade 19.6–20.2 s | Sentence 3 at 13.10 s; speech ends 17.86 s |

Word onsets came from the waveform energy profile, cross-checked with local
whisper. Cuts sit about 60 ms before each word, as in the recorded-voice edit.

## Checks actually performed

- The rendered audio equals the three mastered WAVs at their planned offsets:
  0.9993–0.9994 correlation in every sampled window, with a constant 21.3 ms
  AAC offset (under one frame).
- A local re-transcription of the final MP4 matches `Script.txt` word for word.
- MP4: H.264 1920×1080, 30 fps, 606 frames, 20.2 s. AAC 48 kHz stereo. A full
  decode passed. −15.63 LUFS integrated, −3.98 dBTP. The first export measured
  −13.4 LUFS; that was corrected with the −2.2 dB layer gain.
- The project package contains no copy of the supplied narration.
- The encoded one-second filmstrip and the heading-cut strip were visually inspected.

## Limits

The agent cannot listen, so the voice quality, prosody, and pause feel of the
synthetic read are unauditioned. Please listen before sharing. Kokoro may stress
words differently from the original speaker. Because this is AI speech, it
should not be presented as a recording of a real person.
