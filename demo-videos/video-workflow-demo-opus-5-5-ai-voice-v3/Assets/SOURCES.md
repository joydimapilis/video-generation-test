# Sources — Video Workflow Demo (Opus 5.5, AI voice v3)

The supplied narration recordings are **not used** and not included.

## AI-Voice/ — ElevenLabs narration
- Service: ElevenLabs text-to-speech API (`/v1/text-to-speech/{voice}/with-timestamps`), using the account
  in `ELEVENLABS_API_KEY` (free plan). The key is read from the environment and is not stored in this project.
- Voice: **Bella — Professional, Bright, Warm** (`hpp4J3VqNfWAUOO0d1Us`, ElevenLabs premade, American).
  Model **eleven_multilingual_v2**; settings: stability 0.5, similarity 0.75, style 0, speaker boost on, speed 1.0.
  Output: `mp3_44100_128`.
- Text: the script, verbatim, one request per sentence (23). Each request passed the chapter's other
  sentences as `previous_text` / `next_text`, so the intonation flows across sentences.
  There are no pronunciation hints: "HyperFrames", "UI", "Fal", and "Conductor" read correctly as written.
- `elevenlabs-mp3/*.mp3` — the audio exactly as returned. `alignment/*.json` — ElevenLabs' character
  timings and request IDs. `sentences/*.wav` — mono decodes. `manifest.json` — text, files, and durations.
- `processed/*.wav` (packaged in the .tsrct): `aresample=48000,volume=2.2dB,alimiter=limit=0.708:attack=3:release=60:level=disabled`.
  The raw read is −20.0 LUFS, so this is a small lift with peak control only. There is no compression.
- Usage: 1,873 characters for this synthesis (the account showed 1,922 of 10,000 used afterwards).
- Licensing note: check your ElevenLabs plan terms before commercial use. On the free plan,
  ElevenLabs requires attribution and does not grant a commercial license.

## Source/, Derived/, Holds/, Fonts/
APFS clones of the files used by the earlier versions: the screen recordings (byte-identical to
Desktop/Experiment), the Step 2 excerpts/time-lapse, the Kite soundtrack with its pause removed,
original-frame holds, and IBM Plex Sans Medium (+ SIL OFL 1.1). No music, SFX, or generated footage was added.
