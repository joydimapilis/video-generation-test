# Trace — a new browser bug-reporting product film

Three fresh generated hand takes, newly authored UI, script, voice and score. One 33-second film; no interview scenes.

Agent visual screening of eight chronological frames per generated take, full-resolution selected stills, full source decode, actual composition snapshots and measured cursor-target geometry. Scores are subjective screening judgments. No independent listening, calibrated hand-motion metric, exhaustive motion review, or audience test.

Scores average four equally weighted criteria. Compare within use case only.
One take per condition. Round one holds prompt text constant across models but not seed semantics or resolution. H3 Max v2 changes prompt, seed and framing together, so improvement cannot be attributed to one variable. No general model superiority established.

| Run | Role | v | Score / 10 | Dimensions | Estimate | Seconds | Used |
| --- | --- | ---: | ---: | --- | ---: | ---: | :-: |
| `trace_hands_kling_v1` | industrial_human | 1 | 7.38 | 1920x1080 | $0.56 | 164.41 | - |
| `trace_hands_h3max_v1` | industrial_human | 1 | 8.0 | 1344x768 | $0.40 | 19.74 | - |
| `trace_hands_h3max_v2` | industrial_human | 2 | 8.38 | 1344x768 | $0.40 | 103.42 | yes |

## Detailed criteria

N/T means not tested, not zero. These are subjective sampled-frame scores; a single-shot identity score does not establish consistency across shots.

| Criterion | trace_hands_kling_v1 | trace_hands_h3max_v1 | trace_hands_h3max_v2 |
| --- | ---: | ---: | ---: |
| human realism | 8 | 8 | 8 |
| face realism | N/T | N/T | N/T |
| hand body movement | N/T | N/T | N/T |
| identity consistency | N/T | N/T | N/T |
| product accuracy | N/T | N/T | N/T |
| text ui accuracy | N/T | N/T | N/T |
| camera movement | 8 | 8.5 | 8.5 |
| cinematic quality | N/T | N/T | N/T |
| transition quality | N/T | N/T | N/T |
| entry exit continuity | N/T | N/T | N/T |
| context clarity | N/T | N/T | N/T |
| product message clarity | N/T | N/T | N/T |
| prompt adherence | 7 | 7.5 | 8 |
| consistency | 8 | 8 | 8.5 |

## What Changed This Loop

Created a new software concept and exact UI workflow rather than extending Crumb. Compared two fresh hand takes, generated a targeted third take, revised UI chronology and pointer coordinates, and assembled a new 33-second edit. Voice and music are newly created locally. No previous generated video is used.

## Controlled Comparisons

### Cool Device Insert

Winner: **H3 Max v1 for this edit, then revised to v2**

Matched round-one prompt gives H3 Max a closer palette and framing fit. Kling remains credible for other hand/device work. This is a narrow creative-fit screen, not a replacement for the broader routing history.

## Routing After This Loop

| Shot type | Route to | Selected run | Caution |
| --- | --- | --- | --- |
| exact ui text | HyperFrames 0.8.40 | `-` | Deterministic authored UI. Click geometry and visible state order must still be verified. |
| cool single hand insert | H3 Max for this selected take | `trace_hands_h3max_v2` | One short sample; complex manipulation, identities and faces not tested. |
| narration | Local Kokoro af_heart | `-` | No on-camera speech or lip-sync claims. |

## Observations

### `trace_hands_kling_v1` - 7.38/10
Good visible skin texture and coherent laptop in samples. The gray environment misses the intended midnight-blue palette; curled finger poses and the visible screen edge make this less suitable for the restrained one-click insert. Rejected for this edit, not for all hand scenes.

### `trace_hands_h3max_v1` - 8.0/10
Cool palette and tighter device framing fit Trace better. Hand/device remain coherent in samples, but multiple fingers lift and the screen edge remains. Targeted overhead revision requested; source not used in final.

### `trace_hands_h3max_v2` - 8.38/10  **selected**
Selected source seconds 1–4 for a three-second insert. Tighter overhead framing supports the tap; cool desk and skin shading fit the UI palette. Several fingers still change pose slightly; do not claim perfect isolated-index adherence. The final centered crop excludes the tiny screen edge. Returned 1344x768 footage is placed in a 1060x800 region; this is not native 1080p generated footage.

## Findings

- Make the product name and category visible from the beginning; demonstrate one concrete failure and its report.
- Use one browser element across workflow states to preserve position and prevent scene-to-scene UI drift.
- First UI revision moved Record's cursor onto its real target, filled the form after recording began, and separated payment and order-button boxes.
- An onion-path diagnostic placed fitted markers away from the real button locations; measured DOM geometry and actual full-frame snapshots established all three clicks landed correctly. Do not treat marker overlays as rendered interaction proof.
- H3 Max's $0.02/s launch promotion expired September 14. This run uses the September 15 normal 768P rate of $0.08/s.
- No generated facial performance needed: 30 of 33 seconds contain authored product/UI or typography. Human insert totals three seconds; zero interview seconds.
- Encoded transition review caught one-frame hand bleed and an empty CTA boundary. Opaque demo backing, an overlapping final wipe and timed retirement of old text fixed both without new API calls.

## Budget

Estimated generation total: $1.36. Conservative reserved total: $1.57. Hard cap: $10.00.
3 reserved requests; 3 completed; 0 failed or uncertain. No automatic retries.
This loop has its own ledger at `artifacts/library-loop-10/budget.json`; it is the persistent cost record and deleting it defeats the cap guard. Provider invoice not queried.


## Delivered film

`artifacts/final_outcome/trace/trace.mp4` — 33 seconds, 1920×1080, 24fps. Full decode passes; no detected black intervals or digital clipping. Composition: zero lint/runtime/layout/contrast findings, 59/59 contrast checks pass. Separate cursor geometry and encoded transition review passed; the CLI motion sub-audit was disabled. Audio mix zero-offset correlation: 0.99949. See `artifacts/final_outcome/trace/verification.json` for the final file hash, source timing and review limitations.
