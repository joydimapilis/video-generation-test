# Tuck production and rebuild

Tuck is a fictional AI expense-report tool. A hand slides a receipt, the physical paper becomes a software surface, and three receipt images become a reviewed $178.40 report. The report stays visible while the same hand leaves the desk. All footage, narration, script, UI, music and editing were made for this run. No interview, face close-up, testimonial or direct-to-camera speech appears.

## Direction and references

The user requested a fresh product launch with a subtle human opening, short walkthrough, human callback ending and a $10 maximum estimated generation budget. The selected concept provides a physical object that can continue into the interface.

This run reuses established model-routing lessons, not earlier footage. Trace informed simple hand framing and exact cursor verification; Fold informed paper-surface continuity and a result that remains visible in the ending. Three local library references were inspected: Wispr Flow's rapid real-use/input-to-result demonstrations, Bloom's clear input/output transformation, and Notion's task fragments. Wispr's interview and presenter framing was deliberately excluded. No reference video is copied into Tuck. Source filenames and contact sheets are in `artifacts/library-loop-12/references/`.

The product-launch workflow used a fictional no-capture brief and a Blue Professional preset remixed into cream #F5F0E8, charcoal #171A18 and amber #965B16. Fonts are local Space Grotesk and Inter. The frame workers ran serially inline; the user's autonomous production request covered storyboard, iteration and final rendering.

Registry `modal-morph` informed measured paper-plane transforms; `simulated-cursor` supplied the pointer/pulse primitive. Root-mounted video sits behind the authored scene layers. The photographic media received a framing/polish review and retains the generated natural light without additional grading or effects.

## Generation and revision

H3 Max was selected from the previous constrained hand-shot screen. The first take exposed prominent invented receipt print and a pinch/lift movement. A targeted second prompt requested blank receipt backs, a flatter hand, a short slide and a simple withdrawal. It improved these issues; the paper remains wider than the requested narrow strip. This is a two-take creative revision, not a controlled cross-model benchmark.

Only `tuck_receipt_h3max_v2` is used. It returned 1344×768 at 24fps. New source ranges:

| Role | Source time | Placement | Processing |
| --- | --- | --- | --- |
| Opening | 0.5–6.0s | x830 y0, 1090×1080 | Scale to 1080 high, crop x550; the paper transition covers it before the range ends. |
| Human return | 6.0–10.0s | x1050 y0, 870×1080 | Same source, crop x700 after scaling; freeze its final frame for four seconds. |

The return is a later part of one continuous take. It does not claim independent multi-shot identity generation. The human is visible for approximately seven seconds overall, in a supporting role. `videos/tuck/sources.json` stores source hashes and exact derivations.

HyperFrames owns every meaningful merchant, date, amount and interface state. Example rows are Kindred Cafe $6.40, City Cab $24.00 and North Hotel $148.00, totaling $178.40. This is illustrative expense preparation; no tax, reimbursement or approval result is implied.

New local Kokoro `af_heart` narration uses speed 1.01, measured pauses and real silence padding to 8/14/8-second scenes. Raw takes remain beside the padded files. A new deterministic 96 BPM electric-piano score, seed 91512, adds gentle percussion, paper movements and exact click accents. Raw engine timestamps remain in `audio_engine_meta.json`; captions are intentionally skipped.

## Finished-film revisions

- Tightened the hand direction and removed meaningful print from generated paper.
- Matched settled app and report geometry across both modular scene boundaries.
- Moved the review pointer beside the amounts and added immediate “Preparing…” feedback.
- Encoded review exposed a short empty table-to-report beat. The final revision reveals the report earlier while the underlying paper settles.
- Preserved the same completed report through the hand's withdrawal and the closing CTA.

## Budget

H3 Max normal 768P pricing after September 14 is $0.08 per generated second. Two requested ten-second takes total **$1.60 estimated**, with **$1.84 reserved** under a **$10 cap**. The expired $0.02/s promotional rate is not used. [Fal's H3 Max pricing](https://fal.ai/models/minimax/h3-max/text-to-video).

Both requests completed; no failed or uncertain requests. Local narration, score and HyperFrames render incur no generation API charge. The provider invoice was not queried. The persistent run-specific ledger is `artifacts/library-loop-12/budget.json`; do not delete or reset it.

## Rebuild

From the repository root, with the staged raw narration and generated source available:

```sh
.venv/bin/python scripts/prepare_tuck_assets.py
.venv/bin/python scripts/prepare_tuck_audio.py
.venv/bin/python scripts/build_tuck_composition.py
npx hyperframes@0.8.40 check videos/tuck --timeout 30000 --json > artifacts/library-loop-12/check-final.json
node scripts/verify_tuck_geometry.cjs
npx hyperframes@0.8.40 render videos/tuck --fps 24 --quality delivery --strict --no-best-effort --skill product-launch-video --output artifacts/final_outcome/tuck/tuck.mp4
.venv/bin/python scripts/verify_tuck_video.py
```

The builder runs the workflow root assembler and installs local GSAP/media wiring. `prepare_tuck_assets.py` only restages existing media; it does not make a paid call. If a download is missing, resume the persisted queue job without submitting a duplicate:

```sh
.venv/bin/python scripts/run_library_loop.py configs/tuck_round2.json --evaluate
```

To regenerate missing narration, use the product-launch `audio.mjs` adapter with the project's SCRIPT and STORYBOARD, `--provider kokoro --voice af_heart --speed 1.01`, and `HYPERFRAMES_PYTHON` pointing to the workspace virtualenv. Then run the audio preparation script. Keep `*-raw.wav` source files separate from scene tracks.

Preview:

```sh
npx hyperframes@0.8.40 preview videos/tuck --background --port 3037
npx hyperframes@0.8.40 preview videos/tuck --status
```

Final files: `artifacts/final_outcome/tuck/` — MP4, review player, poster, encoded frame/transition sheets and verification JSON. Studio: `http://localhost:3037/#project/tuck`.

## Review limits

The full file is decoded numerically; visual review samples chronological encoded frames and targeted transition sequences. Audio alignment and clipping are checked against the intended mix. No independent listening or audience test was performed. The CLI motion sub-audit was disabled; separate timeline inspection, seek-state regression, cursor geometry and source-frame comparisons provide motion evidence. The output is 1080p, while the generated plate is cropped/enlarged from 768p.
