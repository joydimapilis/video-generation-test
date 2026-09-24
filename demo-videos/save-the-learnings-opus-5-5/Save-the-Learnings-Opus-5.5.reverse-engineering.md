# Reverse engineering — Save the Learnings (Opus 5.5 version)

Built from scratch by Claude Opus 5.5 with Tesseract 0.2.0. It is a separate
project from the earlier Astra edit in `../save-the-learnings/`. That folder was
not opened for writing, and none of its editorial decisions were reused.

## Brief (same as the Astra version)

Recreate a CapCut-style manual edit in Tesseract: a polished 20–30 s demo from the
supplied screen recording, narration, and script. Trim unnecessary pauses; sync
the screen to the narration; cut or reposition where needed. Add clean captions,
and use subtle zooms or highlights only where they help. Keep transitions simple,
pacing natural, and motion graphics to a minimum. Review for awkward timing. Add
no AI-generated footage and do not change the original content. Keep the
project, sources, and MP4 together.

## Inputs

- Screen recording: 3164×1930, H.264, variable frame rate (60 fps nominal),
  29.76 s, no audio. The camera is static before 2.8 s, then scrolls the Kite
  reverse-engineering doc from 2.8 to 8.0 s, then stays static.
- Narration: 48 kHz stereo AAC, 23.25 s, −18.3 LUFS, −3.5 dBFS peak. Speech runs
  from 2.28 s to about 20.7 s.
- Script: `Script.txt`. A local whisper.cpp (small.en) transcript matched it
  word for word.

## Editorial idea

The narration lists five things: prompts, structure, methods, revisions, and
learnings. The document has a real heading for each one. So the edit's structure
is a **heading match-cut**: every spoken item cuts to an original frame where its
heading lands in the same screen position. An amber highlighter swipes across the
heading, using the same motion every time. The final sentence moves from the
document to the file itself in the sidebar tree.

## Cut and source map (edit seconds)

| Edit | Picture (source) | Narration | Treatment |
|---|---|---|---|
| 0–5.00 | Screen 0–2.8 s, slowed to 0.56× (static page) | "For every finished video … document." | Wide app view. Slow 2.5 s push-in (0.65→3.15 s) to the doc title and file path at 1:1 pixels. The highlighter lands on `kite-campaign.reverse-engineering.md` on "reverse". |
| 5.00–8.42 | Screen 2.8–7.1 s at 1.26× (real scroll) | "This records how the video was made, including the" | The camera drifts down with the scroll, which lands on "Prompts" |
| 8.42–9.19 | Hold of source 7.10 s | "prompts," | "Prompts" heading highlighted |
| 9.19–10.26 | Hold of source 1.00 s | "structure," | "Structure" heading highlighted |
| 10.26–11.10 | Hold of source 7.25 s | "methods used," | "Models and methods" highlighted |
| 11.10–11.87 | Hold of source 7.45 s | "revisions," | "Revisions" highlighted |
| 11.87–20.50 | Screen from 9.0 s (live, static page) | "and key learnings. The workflow also checks … marked complete." | "Final learnings" is highlighted. On "The workflow also checks" (13.15–14.45 s) the camera pans and zooms to 1.4× on the file tree. The file row highlights on "this file". On "before the video" the box grows to include its `artifacts / final_outcome` folder. It holds, then fades to black over 20.0–20.5 s. |

Each cut lands about 60 ms before its word. Every heading sits at canvas (149, 210)
at 1:1 source pixels, so the list reads as one stable flip rather than as jumps.
The speed changes apply only to a static page or a scroll, with no speech on screen.

## Narration edit

The edit is one voice take at its original speed, split into four Audio layers
with 15 ms edge ramps:

| Kept source range | Edit range | Removed |
|---|---|---|
| 1.78–6.92 s | 0–5.14 s | 1.78 s of leading silence; 0.50 s of lead-in kept |
| 7.12–12.25 s | 5.14–10.27 s | 0.20 s of the 0.55 s sentence pause (cut at −69 and −59 dB) |
| 12.37–15.12 s | 10.27–13.02 s | 0.12 s of the 0.46 s "structure, / methods" pause (−54 and −72 dB) |
| 15.36–22.84 s | 13.02–20.50 s | 0.24 s of the 0.58 s pause before the last sentence (−70 dB). The room-tone tail fades over the last 0.7 s. |

Each shortened pause still leaves about 0.25–0.35 s of breathing room. No word
was touched. The only processing is +2.4 dB of clip gain. There is no
compression, EQ, or noise reduction.

## Captions and design

Eleven editable phrase captions from the supplied script. They use IBM Plex Sans
Regular at 48 px on opaque dark rounded pills, over a soft bottom gradient. They
are also supplied as `Captions.srt`. Caption changes coincide with the list cuts.
Highlights are one amber rounded box (16% fill, 3 px stroke) with a 260 ms
left-to-right swipe. There are no other graphics, transitions, SFX, or music.
The voice-only mix keeps the original content unchanged.

## Revisions during the build

1. Font: the IBM Plex Sans SemiBold, IBM Plex Sans Bold, Poppins SemiBold, and
   Poppins Medium static faces all imported. Each failed to render with
   `missing_fonts` in CLI 0.2.0. Lato Bold, Poppins Bold, and Plex Regular
   rendered. Chose Plex Regular and rebuilt the project so no unusable font is
   embedded.
2. Framing: the first draft assumed cover-fit layer space. A calibration render
   showed Video/Image layer-local space is source pixels. Corrected the mapping.
3. Highlights sat half a box off because `rect.position` is the top-left, not
   the center. Corrected.
4. The caption pill at 78% alpha still showed document text through it.
   Changed to an opaque pill plus a bottom gradient.
5. The file-tree highlight appeared fully drawn because its swipe time was
   passed in the wrong clock (group-local). Corrected, then re-checked at 14.85–15.2 s.
6. Gain went from +2.0 dB (−16.42 LUFS) to +2.4 dB to sit inside the −16…−14 LUFS target.

## Checks actually performed

- Source copies match the attachments (SHA-256).
- Rendered narration versus an FFmpeg splice of the intended source ranges:
  correlation 0.999 in every sampled window, with a constant gain. The export is
  about 21 ms early, which is under one frame (AAC priming).
- Joins sit in −57 to −81 dB room tone, with no sample-step discontinuities above −35 dBFS.
- The rendered audio was re-transcribed locally: the word sequence equals `Script.txt`.
- Final MP4: H.264 1920×1080, 30 fps, 615 frames, 20.5 s. AAC 48 kHz stereo.
  A full decode passed. −16.03 LUFS integrated, −1.23 dBTP.
- Visual review: native filmstrips of every cut and camera move, full-resolution
  stills of the captions and highlights, and a one-second strip of the encoded MP4.

## Limits

The agent cannot listen or watch in real time. Pacing and voice feel were judged
from waveforms, levels, transcription, and frames. Please listen to the MP4. The
recording does not show the completion check executing, so that sentence is
narration over the real file in the sidebar. No completion UI was invented. In the
list, "methods" is shown with the document's real "Models and methods" heading.
