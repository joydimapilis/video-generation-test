# Computer interaction realism — three image-to-video studies

The experiment produced one provisionally usable full typing take and two short usable selections. It did **not** establish that movement references consistently improve realism. Later hand curls remain in both the trackpad and side-view takes. All three original four-second Veo takes are delivered alongside selected segments, so the failure tails remain inspectable.

| Study | Selected range | Finding |
| --- | --- | --- |
| 01 — three-quarter typing | 0–4s | Lower, alternating finger movement; supported arms and screen/key gaze. Minor regular cadence and softened facial detail remain. |
| 02 — elevated trackpad view | 0–1.25s | Brief index contact/tap near pad edge. Full take fails: fingers curl/lift around 1.3s, then hold. Sustained trackpad operation is not solved. |
| 03 — side-view typing | 0–1.5s | Small typing movements and supported arms. Full-resolution review exposed a pronounced curled-hand pose after about 1.7s. Requested reading pause was not achieved. |

All are silent, 1920×1080, 24 fps, at native speed, with mostly static camera. Each starts from a generated still reviewed before animation. No skin filtering, interpolation or speed adjustment was added. These are independent source identities, not a character continuity test.

## Reference use and inference limits

The repository's supplied collection is `references/human-realism/`; no separate `human-movements` directory was found. Consulted its README and `review_notes/human-realism-references.md`, inspected the footage through chronological frames and the library inspection script, and retained hashes and selected ranges in `videos/computer-realism-samples/reference-provenance.json`.

Observed cues: reference 02 at 0–2s — unequal finger timing and supported wrists; reference 04 at 0–2s — restrained head/gaze/body movement; reference 05 at 7–9s — unequal hand roles and repositioning. Reference 03 also informed desktop-work posture. Those observations became prompt instructions. The clips were **not uploaded as motion conditioning**, nor used as identity sources. The normal library discovery exposed this collection; additional general-library footage was unavailable through that path.

No paired no-reference control was generated. Source poses, prompts and models changed between rounds, so relative quality cannot be attributed to references alone, and this is not a general model ranking. A matched, preregistered comparison with identical source, model/settings and action would be needed to measure a reference effect. Exact key depression, UI correctness, speech/lip sync, external mouse use and cross-shot identity are untested.

## Attempts and review

Six source-image generations: Flux 2 Pro established the first typing still; Nano Banana Pro supplied the selected trackpad and side-view stills after poor contact/screen poses were rejected. Every source and decision is recorded in `source-reviews.json`.

Two Kling 3 Pro takes failed on high hooked fingers, lost contact and camera widening. Three Seedance 2 requests were declined by the provider's likeness validation and yielded no video; no realism conclusion follows. Four Veo 3.1 Fast takes yielded the final choices: one provisional full-take selection, two rejected full takes with usable short segments, and one rejected trackpad glide. Routing evidence retains full-take failures as failures rather than counting trims as successful four-second actions.

Review used chronological full-frame, hand and face crops (8 fps for Kling, 12 fps for Veo), plus full-resolution composition snapshots. This was sampled visual inspection, not continuous playback. Scores are subjective and provisional. All final encodes underwent full decoding, metadata/frame-count checks, source-to-encode similarity checks and encoded-frame visual inspection. The individual files have no scene joins, captions or audio to align. Composition checks passed with no findings; technical checks alone do not establish realistic movement.

## Cost and records

One conservative shared $10 ceiling covered this entire batch. Estimated allowance: **$8.38**; buffered reservation: **$9.67**. Completed requests account for $3.82 of estimates. The remaining $4.56 estimate / $5.25 reservation belongs to the three provider-rejected requests and remains reserved until billing is reconciled. Confirmed charges are unknown because the usage API returned 403. No failed allowance was silently released.

Detailed group totals: `review_notes/computer-realism-costs.json`. Persistent queue IDs, payloads and the shared budget remain in `artifacts/library-loop-computer-realism/budget.json`. Do not reset that ledger on resumption.

Delivery: `artifacts/final_outcome/computer-realism-samples/review.html`, including all source stills, selected MP4s and untrimmed four-second takes. Editable compositions and exact prompts: `videos/computer-realism-samples/`. Final hashes and verification: `assembled_outputs/computer-realism-samples.json`. Durable attempt reviews: `review_notes/computer-realism-samples.json`; reusable findings: `prompt_library/tested_computer_realism_patterns.json`. Generated media and runtime caches remain excluded from Git.
