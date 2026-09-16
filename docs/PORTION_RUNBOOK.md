# Rebuild Portion

This is a new film; no existing video was used as an edit base. Keep all selected source images and videos in videos/portion/assets. The selected before clip is portion_before_v2; before_v1 was rejected for raised gaze.

```sh
.venv/bin/python scripts/build_portion_composition.py
.venv/bin/python scripts/prepare_portion_audio.py
node scripts/verify_portion_geometry.cjs
npx hyperframes check videos/portion --samples 18 --json
```

From videos/portion:

```sh
npx hyperframes render --quality delivery --fps 24 --workers 2 --output ../../artifacts/final_outcome/portion/portion.mp4
```

From repository root:

```sh
.venv/bin/python scripts/verify_portion_video.py
```

Verification requires numpy and Pillow in the local Python environment, ffmpeg/ffprobe, and the HyperFrames CLI's Puppeteer dependency plus Google Chrome for geometry checks. It checks decode, frames, audio correlation/headroom, source selection, image approvals, budget, final hold and source-region pixel comparisons; chronological encoded contact sheets still require visual review.

Generation plans: configs/portion_round1.json and configs/portion_round2_gaze.json. Shared crash-safe $10 ledger: artifacts/library-loop-15/budget.json. Never submit a completed request again. Image-first approval records bind hashes to each still; retries count against the same budget.

The builder copies only reusable font/runtime binaries from existing projects. Layout, story, imagery, footage, data, animations and sound are newly authored for Portion. Registry cursor provenance is kept in videos/portion/compositions/components/simulated-cursor.html.
