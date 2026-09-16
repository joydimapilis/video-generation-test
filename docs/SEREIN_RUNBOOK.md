# Serein — image-first product film

Fresh fictional AI focus-planner concept,32 seconds,1920×1080 at24fps. Initial character still followed by a corrected mouse-interaction still, each internally reviewed before animation. Nine I2V attempts retained. No prior generated image, video or audio reused. Source fonts and existing tooling are reusable infrastructure.

## Source chain

- New GPT Image2 still via the built-in image tool: `videos/serein/assets/designer-mouse-v2.png`.
- Still approval, anatomy/texture observations and SHA: `artifacts/library-loop-13/reviews/character-mouse-v2.json`.
- Opening: Kling3Pro mouse v5, settled source1.5–6s retimed0.75× to six seconds.
- Return: Kling3Pro mouse v5, source0–6s from a separate take.
- Both requests condition on the exact same approved PNG. Crop/offset/source hashes are in `videos/serein/sources.json`.
- Main people footage is exclusively image-to-video. No text-to-video people shots, interviews or generated screen text.

## Budget

Shared persistent ledger: `artifacts/library-loop-13/budget.json`. Do not delete it to retry. Nine Fal I2V requests estimate $5.92 total. Two $1 allowances cover planning for the built-in image calls; that tool exposes no invoice. Total planning estimate $7.92, reserved $9.14 including15%, $10 cap. Estimates are not settled provider invoices. The mouse jobs first encountered a local missing-module error before upload or API submission when launched outside the project venv. They were submitted once from the venv with the original reservations retained; the ledger records that recovery.

Pricing checked16Sep2026: [Veo3.1Fast silent1080p](https://fal.ai/models/fal-ai/veo3.1/fast/image-to-video), [Kling3Pro silent](https://fal.ai/models/fal-ai/kling-video/v3/pro/image-to-video).

## Rebuild locally

Project CLI pinned to HyperFrames0.8.41. SourceSerif4 comes from Google Fonts (`ofl/sourceserif4/SourceSerif4[opsz,wght].ttf`); Inter is staged locally. Generated media and font binaries remain local under the project ignore file.

1. Keep the approved image and original generated outputs in place. Saved plans `configs/serein_round1.json` through `serein_round3.json`, plus `serein_round4_mouse.json` and `serein_round5_mouse.json`, can resume request IDs without a new paid submission using `scripts/run_library_loop.py`.
2. Run `.venv/bin/python scripts/stage_serein_video.py`.
3. Fresh local Kokoro af_bella narration was generated through product-launch-video's `audio.mjs`; raw takes are preserved in `assets/voice/*-raw.wav`. Run `.venv/bin/python scripts/prepare_serein_assets.py` to rebuild the paced voice files and original84BPM score.
4. Run `.venv/bin/python scripts/build_serein_composition.py`.
5. Run `node scripts/verify_serein_geometry.cjs`, then `npx hyperframes check videos/serein --samples 18 --json`. Inspect midpoint and boundary snapshots.
6. Render from `videos/serein` with `npx hyperframes render --quality delivery --fps 24 --workers 2 --output ../../artifacts/final_outcome/serein/serein-mouse-revision.mp4`.
7. Save final check JSON as `artifacts/library-loop-13/check-final.json`; run `.venv/bin/python scripts/verify_serein_video.py` and inspect the actual encoded review sheet.

The UI is an authored concept, not a working calendar backend. Narration transcription is an automated completeness check, not an independent listening test. Skin/daylight were left untreated after the media-polish scan; no smoothing or cosmetic grading. The films are reviewed through chronological source samples and encoded output; subjective scores are not audience metrics.

## Mouse revision
User review found the original person shots too passive. The new still establishes the mouse, finger placement, neutral wrist and screen-directed gaze before animation. Both clips use the exact approved revised PNG. Inspect face and hand contact sheets before staging. The original final and its provenance remain in `artifacts/final_outcome/serein/original/`.

The first mouse animations (Veo v4) retained the mouse but looked down repeatedly and rotated it too much; both were rejected. V5 uses the same approved still, a shorter screen-fixation prompt and Kling3Pro. This is a confounded prompt/model change, not proof of universal model superiority.
