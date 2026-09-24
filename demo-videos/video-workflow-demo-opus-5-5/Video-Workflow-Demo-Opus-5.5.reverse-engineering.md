# Reverse engineering — Video Workflow Demo (Opus 5.5)

Claude Opus 5.5 built this with Tesseract 0.2.0, from the files in
`/Users/joydimapilis/Desktop/Experiment`. It is a new project. No earlier Astra or
Opus project was opened for writing.

## Brief

Recreate the CapCut product demo. Treat the script as the source of truth.
Choose the best narration takes and remove retakes, mistakes, repeats, long pauses,
and dead air. Match the screen recordings to the narration. Add clean captions,
simple transitions, and subtle zooms/highlights only where they help. The video
must be 5 minutes or shorter. Keep the editable project, sources, and MP4 together.

## Result

2:56.7 (176.7 s), 1920×1080, 30 fps, H.264 + AAC 48 kHz stereo.
−15.6 LUFS integrated, −1.5 dBTP.

| Edit time | Chapter (on-screen chip) | Picture | Narration take |
|---|---|---|---|
| 0:00–0:13 | Intro | Preview montage: the prompt (Step 2) → STORYBOARD.md (Step 4) → verification JSON (Step 5) → the finished Kite video (Step 7, muted) | Step 1 (only take) |
| 0:13–0:28 | 01 The request | The prompt is typed and sent in real time. The camera pushes in to the prompt, and "simple request" is highlighted. The whole 16 m 46 s agent run follows as a ~530× time-lapse ("Sped up" chip). It lands on the real completion ("83 tool calls · 16m 46s"), which is highlighted | Step 2 (only take); the tail is extended in room tone to hold the completion |
| 0:28–0:45 | 02 Reference library | Finder "Startup Launch Videos" library → two reference films previewing (AI/VC, retro computer) on "different video styles… pacing, transitions" → library again | Step 3 (only take) |
| 0:45–1:05 | 03 Shot planning | STORYBOARD.md top (slowed), then the real scroll through all four frames (2.1×). Then, on "the initial brief / the campaign idea / how that idea expands", three original-frame holds put the Frame 1/2/3 headings in the same screen spot (match cut). Each heading is highlighted on its word | Step 4 "and part 2" file: sentences 1–2, plus the **second** "Here, I am showing…" take |
| 1:05–1:29 | 04 Choosing the method | shot-routing.json. `method: HyperFrames HTML + GSAP` is highlighted on "HyperFrames", `reason` on "precise text, UI, and layout", and `paid_generation: false` on "instead of generative footage" → the fal.ai catalogue (logo highlighted on "Fal") → the real model-grid scroll | Step 4 "and part 2": the HyperFrames line. Step 4_Part 3: "For other videos…" + "The idea is…" |
| 1:29–1:42 | 05 Assembly and checks | Final verification JSON: the `video` line on "final video" → quick scroll → the visual-review entries, with timing / transitions (the "short fades… clear cuts" line) / audio / ending highlighted one by one as they are spoken → `status: "complete"` on "complete" | Step 5, **third** (last) take |
| 1:42–2:01 | 06 Reverse-engineering doc | kite-campaign.reverse-engineering.md: the file name is highlighted on "reverse-engineering document", then the real scroll lands on "Final learnings" (highlighted). Then back to the verification JSON: the `reverse_engineering` path on "this file exists", `documentation_complete: true` on "marked complete" | Step 6 (only take) |
| 2:01–2:42 | 07 Final video | Conductor preview (push-in) → the full 36 s Kite video fullscreen with its own soundtrack. The source recording's mid-play pause is cut out | Step 7, **first** take ("produced through that workflow") |
| 2:42–2:57 | Next · Human realism | Notion "Human-realism / Longer Sample" (breadcrumb highlighted) → generated woman-at-laptop take → hands close-up on "hands" → eyes close-up on "eye movement" → the page for the last sentence, then a fade to black | Step 8, **second** take (after "Okay.") |

Chapter boundaries use a 0.25 s crossfade (0.5 s from the Kite video into Step 8).
Inside a chapter every change is a straight cut, placed just before the matching word.

## Narration: take selection and cleanup

| File | Takes found | Used | Removed |
|---|---|---|---|
| Step 1 | 1 | all | 1.8 s lead silence, 3 s tail |
| Step 2 | 1 | all | lead/tail silence |
| Step 3 | 1 | all | lead/tail silence |
| Step 4 and part 2 | 2 × "Here I am showing…" | 2nd (31.8–39.8 s): fluent, 8.0 s | 1st take (14.3–23.6 s): 0.85 s and 0.52 s hesitations; 8 s of silence between the takes |
| Step 4_Part 3 | an earlier HyperFrames wording ("Next, the system decides… instead of a generated video model") | only "For other videos…" + "The idea is…" | the earlier wording. The script's HyperFrames sentence is the later re-record in the "and part 2" file (recorded 21:40 vs 21:37) |
| Step 5 | 3 starts: take 1 breaks off ("before they can…"), a false start ("Once the video…"), takes 2 and 3 complete | take 3 (41.4–53.9 s) | take 1, the false start, take 2 (runs sentence 1 into 2, then pauses mid-sentence) |
| Step 6 | 1 | all | lead/tail silence |
| Step 7 | 3 | take 1 (one continuous phrase, matches the script's "produced through") | take 2 (duplicate), take 3 (says "created using") |
| Step 8 | "…is human realism." / "Okay." / full re-take | the full re-take + final sentence | first attempt and "Okay." |

Inside the kept takes, all pauses are natural (≤ 0.8 s). No word was cut. Every
join sits in the speaker's own room tone (about −80 dB in the render). Pauses
between chapters are 0.8–1.4 s.

### Where the spoken words differ from the script
- **Step 8** (the only real wording change). The best complete take says: "The next
  phase I'm working on is *making people look and move more naturally, especially
  their hands, eye movement, and longer scenes*." The script's wording ("human
  realism, especially improving natural movement, hands, eye direction, and longer
  scenes with people") exists only as an abandoned first attempt that stops after
  "human realism". "Human realism" still appears as the chapter chip and the
  highlighted page breadcrumb. Captions follow the actual audio.
- Step 4: the audio says "Here, **I am** showing…". The caption follows the audio.
- Small ambiguities are captioned with the script wording, because the local
  transcriber is unreliable on them: "idea, plans", "the process **and** the final
  output", "I **moved**", "visual direction", "generative footage", "Fal". Please
  confirm them by ear.

## Audio

- The narration uses full-length compressed derivatives of each file. There is
  2.5:1 gentle compression plus a peak limiter, with timing unchanged (0 ms offset
  measured). The originals were at −19 LUFS with peaks near −3.7 dBFS. Clip gain
  is +8.0 dB. See `Assets/SOURCES.md`.
- The Kite video plays with its own recorded soundtrack as one continuous audio
  layer (+0.6 dB). Tesseract fades each clip's embedded audio in over ~40 ms, so
  splicing across the paused moment left a dip. A pre-joined soundtrack fixes that;
  the two picture clips stay muted.
- All other recording audio is muted (the library previews, the Kite preview click).
- No music bed or SFX was added. This is a voice-led demo, and the Kite video brings its own music.

## Captions and design

- 69 phrase captions in IBM Plex Sans Medium, 44 px, on dark rounded pills at the
  bottom. While the prompt box is the subject, the captions move up above it
  (0:00–0:04, 0:13–0:24). A sidecar copy is in `Captions.srt`.
- Chapter chips appear top-left for ~3.5 s at each section start.
- There is one highlight style: an amber rounded box with a 280 ms left-to-right
  swipe. Highlights live inside each shot's camera group, in source-pixel space,
  so they stay locked to the text through zooms.
- Framing: Conductor document shots show the sidebar and document at 0.87×, with
  the file tree trimmed at its divider. Browser pages show the full window at 0.67×.
  The 1280×720 recordings are shown full-frame. Zooms are slow and eased.

## Revisions during the build

1. Font: CLI 0.2.0 reports IBM Plex Sans Bold as missing, or silently falls back
   to Regular. Plex Medium renders correctly only as family `IBM Plex Sans Medm`,
   style `Medium` (checked in a weight-comparison render). Used Medium for everything.
2. Framing: the first doc framing cut through sidebar text. Changed to the whole
   sidebar plus the document at 0.87×.
3. Step 8: the first woman-at-laptop range showed a paused player ("0:00 / 0:09").
   Moved to a range where the clip is playing. Fixed the hands close-up
   coordinates (misread from a scaled contact sheet).
4. Audio: the first mix peaked at −0.1 dBTP. Added the compressed narration
   derivatives. Result: −15.6 LUFS / −1.5 dBTP.
5. Kite splice: a 40–60 ms dropout at the pause cut. Replaced it with a continuous
   soundtrack layer.
6. Rebuilt the .tsrct from `create_project.sh` so it packages only the assets in use.

## Checks actually performed

- Source copies are byte-identical to the Desktop originals (SHA-256).
- Transcription of every narration file (whisper.cpp small.en, local), plus
  per-take transcription of every retake to choose between them.
- The delivered MP4 was re-transcribed chapter by chapter
  (`.tesseract-work/transcripts/final-render-transcript.txt`). Every script step
  is present once, in order. There are no repeated lines, false starts, or "Okay."
  (the Step 8 wording note above applies).
- Join levels at all 11 narration/soundtrack boundaries (room tone, no dropouts). The Kite splice is continuous at 5 ms resolution.
- Loudness of the delivered MP4: −15.64 LUFS, −1.54 dBTP, LRA 2.7 LU (`checks/final-loudness.json`).
- ffprobe: H.264 High 1920×1080 30 fps, 5301 frames, 176.7 s, AAC 48 kHz stereo. The full decode passed.
- Visual: native filmstrips of every beat and cut during the build, full-resolution
  stills of captions/chips/highlights, and a 4-second contact sheet of the encoded
  MP4 (`Previews/Filmstrip-final-every-4s.png`). Two frames that looked blank in a
  native filmstrip were confirmed correct in the encoded MP4 (a filmstrip seek artifact).

## Limits

- The agent cannot watch or listen in real time. Pacing, voice quality, and the
  compression were judged from waveforms, levels, transcripts, and frames. Please
  play it once with sound.
- The QuickTime play bar is part of the Kite recording and the library previews.
  It is visible over parts of the Kite video.
- The time-lapse is sampled at 60× and then sped up further. It flickers by
  design, and is labeled "Sped up".
- The Step 3 recording has no clean, still library moment long enough for the
  first sentence, so the real Finder scroll is used.
