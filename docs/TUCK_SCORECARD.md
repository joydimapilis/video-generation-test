# Tuck — Receipts to ready

A new 30-second AI expense-product launch: minimal hand footage, exact UI walkthrough, human callback and finished report. Two fresh hand takes; one selected.

Agent review of eight chronological source frames per take, selected full-resolution stills, source decode, composition snapshots, encoded frame sequences, cursor geometry and source-timing comparisons. Scores are subjective screening judgments. No calibrated hand-motion or lip-sync metric, independent listening or audience test.

Scores average four equally weighted criteria. Compare within use case only.
One take per condition. The revision changes prompt and seed together, so improvement cannot be attributed to one variable. No new cross-model benchmark or general model-superiority claim.

| Run | Role | v | Score / 10 | Dimensions | Estimate | Seconds | Used |
| --- | --- | ---: | ---: | --- | ---: | ---: | :-: |
| `tuck_receipt_h3max_v1` | industrial_human | 1 | 7.0 | 1344x768 | $0.80 | 18.96 | - |
| `tuck_receipt_h3max_v2` | industrial_human | 2 | 8.25 | 1344x768 | $0.80 | 18.58 | yes |

## Detailed criteria

N/T means not tested, not zero. These are subjective sampled-frame scores; a single-shot identity score does not establish consistency across shots.

| Criterion | tuck_receipt_h3max_v1 | tuck_receipt_h3max_v2 |
| --- | ---: | ---: |
| human realism | 8 | 8.5 |
| face realism | N/T | N/T |
| hand body movement | N/T | N/T |
| identity consistency | N/T | N/T |
| product accuracy | N/T | N/T |
| text ui accuracy | N/T | N/T |
| camera movement | 8.5 | 8.5 |
| cinematic quality | N/T | N/T |
| transition quality | N/T | N/T |
| entry exit continuity | N/T | N/T |
| context clarity | N/T | N/T |
| product message clarity | N/T | N/T |
| prompt adherence | 6.5 | 8 |
| consistency | 8 | 8.5 |

## What Changed This Loop

New Tuck concept, script, original hand source, specific hand/text revision, exact expense walkthrough, fresh local narration and96 BPM score. Source frames and actual encode are evaluated; no prior generated footage is reused.

## Routing After This Loop

| Shot type | Route to | Selected run | Caution |
| --- | --- | --- | --- |
| minimal hand and paper | H3 Max for this selected take | `tuck_receipt_h3max_v2` | Only simple paper contact and withdrawal screened. Do not generalize to precise multi-step handling. |
| exact ui and text | HyperFrames 0.8.40 | `-` | Fictional authored UI; clicks, math, readable states and boundary frames independently checked. |
| voice | Local Kokoro af_heart | `-` | No on-camera speech; source narration includes measured pause insertion. |

## Observations

### `tuck_receipt_h3max_v1` - 7.0/10
Plausible hand and warm desk, but the prominent invented receipt print reads as gibberish in the full-resolution close-up. The hand lifts and pinches despite the planned simple slide. Replaced for this edit.

### `tuck_receipt_h3max_v2` - 8.25/10  **selected**
Blank receipt backs remove the fake-text distraction; the flatter hand and slow withdrawal support the story. Receipts are wider than the requested slender strips, and several fingers move together. Selected source0.5–6s for the opening and6–10s for the return, with framing and a final-frame hold; no old footage or second identity is used.

## Findings

- A receipt backside can supply the physical shape while all readable business details are authored in the UI.
- Keep a hand flat and its motion simple; remove instructions that invite pinching, lifting or complex manipulation.
- Use distinct ranges of the same fresh continuous take for the opening and return when identity and lighting should match. This is source-range continuity, not a separately generated matching identity.
- Keep paper opaque as its plane expands; retire type before nonuniform aspect changes.
- Show immediate Preparing feedback after the report action; move the review cursor beside numbers so it does not cover them.
- The final report keeps the same $178.40 sum and three attached receipts visible while the hand leaves.
- Source footage is1344x768 and is cropped/enlarged into1080p panels; exact UI is authored at1920x1080.

## Budget

Estimated generation total: $1.60. Conservative reserved total: $1.84. Hard cap: $10.00.
2 reserved requests; 2 completed; 0 failed or uncertain. No automatic retries.
This loop has its own ledger at `artifacts/library-loop-12/budget.json`; it is the persistent cost record and deleting it defeats the cap guard. Provider invoice not queried.


## Finished-film review

Subjective screening of the actual encoded film, not audience metrics. Opening 8/10; product clarity 9; walkthrough 9; UI quality 9; natural human presence 8.5; visual consistency 8.5; transitions 8.5; ending 8.5; overall watchability 8. The person remains secondary, and the report stays visible in the human callback. The brief empty table-to-report interval was shortened after encoded review.

Delivered MP4: `artifacts/final_outcome/tuck/tuck.mp4` — 30 seconds, 1920×1080, 24fps, 7.84 MiB. All 720 frames decode; no detected black intervals or digital clipping. Zero lint/runtime/layout/contrast findings; 69/69 contrast checks pass. Both click tips land inside their controls. Source-frame comparisons at six opening/return times have mean error below 1.9/255. Both scene boundaries have mean error below 0.004/255. Audio correlation with the intended mix is 0.99973, peak 0.601. The report/CTA holds through the last frame.

The CLI motion sub-audit was disabled; separate timeline inspection, cursor geometry, seek-state regression and encoded source comparisons were used. No independent listening or audience test was performed. [Exact verification and file hashes](../artifacts/final_outcome/tuck/verification.json).
