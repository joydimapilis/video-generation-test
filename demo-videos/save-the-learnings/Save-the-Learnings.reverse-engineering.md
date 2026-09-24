# Reverse engineering — Save the Learnings

## Intent and inputs

Reproduce a restrained CapCut-style screen-recording edit using Tesseract 0.2.0:
20–30 seconds, original content and narration, tighter pauses, clean captions,
helpful reframing, simple transitions, editable project delivered with sources.
The exact supplied script is in Script.txt. No AI-generated imagery or speech.

Original screen recording: 3164×1930, variable frame rate, 29.763333 seconds,
H.264, no audio. Narration: 23.253333 seconds, 48 kHz stereo AAC.
Copies in Assets are byte-identical to the user attachments.

## Cut and source map

Times below are seconds. Screen cut points were chosen from inspected source frames.

| Edit interval | Picture source | Purpose |
|---|---|---|
| 0–0.7 | Screen 0–0.7 | Establish the original document |
| 0.7–5.0 | Held original screen frame 0.7 | Let the first sentence identify the document |
| 5.0–7.87 | Screen 1.4–4.27 | Show the recorded structure scroll |
| 7.87–11.14 | Held original screen frame 7.0 | Show prompts and production context |
| 11.14–13.55 | Held original screen frame 7.65 | Show revisions; pan down to learnings |
| 13.55–20.0 | Screen 8.0–14.45 | Show the saved document and verification filenames |

Narration: source 2.05–22.05 mapped to edit 0–20, no internal cuts or speed changes.
The approximately 0.43–0.59-second internal pauses were retained for breathing.
The 2.05-second leading and 1.203-second trailing excess were removed, leaving
about 0.23 seconds before the first spoken word and 1.39 seconds after the last.
A +2.2 dB native gain adjustment and short fades only in silent handles preserve
the original performance. No other sound processing was applied.

## Methods and editability

Tesseract owns project editing, native media layers, text, pan keyframes, audio
placement/gain, preview, and final export. Local FFmpeg/ffprobe handled source
inspection, extracting original frames for holds, waveform diagnostics, and
encoded-output checks. Original MOV and M4A are embedded in the portable project.
Static Lato Regular is embedded with its SIL license retained in Assets.

Whisper.cpp small.en, already available locally, transcribed the voice for
phrase timing; no audio was uploaded. The transcription matches the supplied
script. Eleven phrase captions remain native Text layers and are also supplied
as SRT. No word-by-word bouncing or added motion graphics. The caption area
occupies y=934–1080 to avoid competing with the document.

## Revision and actual review

The first filmstrip showed “Final learnings” falling below the caption shelf
at the corresponding spoken phrase. Added a 650 ms vertical pan during
11.59–12.24 seconds; inspected eight targeted native samples across that move
and its next cut. The heading is now visible during “and key learnings.”

Reviewed a 14-frame native overview, the targeted pan strip, 20 chronological
encoded frames, a full-size encoded poster, and source/final waveforms.
The waveform helper could not render labels because the installed FFmpeg lacks
drawtext; FFmpeg showwavespic supplied the inspected waveform view instead.
All 600 encoded frames decode. Final encoded audio is -16.42 LUFS, -1.33 dBTP,
with zero clipped 16-bit decoded samples. Source-to-export audio correlation
is 0.9966 at -21.31 ms, supporting intact original narration and sync to within
one output frame. Caption words were checked against the script programmatically.
Original source copies were verified with SHA-256. Exact reports and artifact
hashes are in `.tesseract-work/checks/`.

## Limits and learnings

Independent audio audition and real-time playback were unavailable. Waveforms,
transcription, and correlation cannot fully verify perceived pacing, voice
quality, or a subtle click. The result is ready for user playback review, not a
claim of a completed listening pass.

The capture demonstrates a real saved reverse-engineering document; it does
not show the completion gate executing. No fabricated completion UI was added.
Dense document paragraphs are context, not all intended to be read in 20 seconds.
The visible headings and caption phrases carry the explanation.

The title, captions, cuts, freeze holds, crop/pan, and voice gain are practical
editable equivalents of the requested manual editing workflow. Freeze-frame
assets preserve source pixels; retaining their source timestamps and original
MOV makes alternate cuts possible. No other video project was modified.
