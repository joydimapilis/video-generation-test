# Sources — Video Workflow Demo (Opus 5.5)

## Source/ — original user files (byte-identical copies of /Users/joydimapilis/Desktop/Experiment)
SHA-256 list: `.tesseract-work/checks/source-sha256.txt`.

- `Script & Structure.rtf` — the final script (source of truth). Plain-text copy: `../Script.txt`.
- `Step 2.mov` … `Step 8.mov` — screen recordings.
- `Audio/Step 1.m4a` … `Audio/Step 8.m4a` — narration recordings, including retakes.

## Derived/ — made locally with FFmpeg from the originals (nothing generated)
- `Step2-request-src0-20s.mp4` — Step 2.mov 0–20 s, re-encoded (x264 CRF 12). The 789 MB recording is 17 min; only these parts are used.
- `Step2-timelapse-src17-1017s-60x.mp4` — Step 2.mov 17–1017 s, sampled at 60× (all-intra, CRF 14). The edit speeds it up further to ~530×. It is labeled "Sped up" on screen.
- `Step2-complete-src1012-end.mp4` — Step 2.mov 1012 s to the end (the real "83 tool calls · 16m 46s" completion), CRF 12.
- `Narration/*-comp.wav` — one per original narration file, full length and sample-aligned (0 ms offset measured). Recipe:
  `acompressor=threshold=0.1:ratio=2.5:attack=5:release=150:knee=3:makeup=1,alimiter=limit=0.33:attack=2:release=60:level=false:latency=true`, 48 kHz 24-bit.
  This lowers speech peaks so the mix can reach −15.6 LUFS under −1 dBTP. There is no EQ, noise reduction, or timing change.
- `Kite-soundtrack-pause-removed.wav` — the Kite video's soundtrack as recorded in Step 7.mov (9.000–9.726 s + 11.6655–46.90 s, 4 ms crossfade). This removes the moment when playback was paused and resumed.

## Holds/ — unaltered single frames extracted from the recordings
- `Hold-Storyboard-Frame1-src5.00s.png`, `…Frame2-src10.20s.png`, `…Frame3-src13.00s.png` — Step 4.mov (STORYBOARD.md frame headings)
- `Hold-fal-top-src0.50s.png` — Step 4_Part 3.mov (fal.ai model catalogue)
- `Hold-Verification-top-src0.80s.png`, `Hold-Verification-review-src14.00s.png` — Step 5.mov (kite-campaign-final-verification.json)

## Fonts/
- `IBMPlexSans-Medium.ttf` (used; embedded in the .tsrct), plus Regular and Bold for reference.
  Source: https://github.com/IBM/plex (packages/plex-sans/fonts/complete/ttf).
- `IBMPlexSans-OFL.txt` — SIL Open Font License 1.1 (https://github.com/google/fonts/blob/main/ofl/ibmplexsans/OFL.txt).

No music, sound effects, generated footage, generated speech, or stock media were added.
