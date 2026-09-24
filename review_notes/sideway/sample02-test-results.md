# Sideway human-realism comparison — 19 September 2026

The experiment produced three image-to-video takes. **None passes all replacement criteria.** The café trial improves the resting free hand, but its face and eyes remain posed. Both phone trials introduce unwanted mouth movement. The full Sideway film and its selected takes remain unchanged.

## Review output

- `artifacts/final_outcome/sideway-human-realism-test/sideway-human-realism-comparison.mp4`: 12-second silent comparison, originals left, candidates center, movement references right.
- `artifacts/final_outcome/sideway-human-realism-test/review.html`: comparison plus full native-speed originals, all candidates, references and the unchanged speaking take with original audio.
- Editable HyperFrames project: `videos/sideway-human-realism-test/comparison/`.

| Original film window | Closest sample02 reference | Test and finding |
|---|---|---|
| Phone opening, 0–3s | `233390_medium.mp4`, 0–4s: downward screen attention, supported posture; supplemental `736-138808023_medium.mp4`, 0–3s: hand/device contact | Reused original reviewed still. Wan 2.2 Turbo 720p trial adds unwanted mouth motion, hovering finger and later gaze departure. Rejected. |
| Speaking, 3–6s | `297986_medium.mp4`, 0–2s: restrained head/neck movement and conversational gaze | Original visible segment comparatively usable; retained with original speech. No regeneration or new lip-sync assessment. |
| Phone return, 6–10s | `233390_medium.mp4`, 0–4s | Original source segment 1–3s plays at 0.5×. Correction uses a reviewed frame at source 2.4s, with open eyes and a supported hand. 480p trial steadies hands but retains mouth movement and loses facial detail. Rejected. |
| Café pause, 26–32s | `216598_medium.mp4`, 0–1s for downward attention, 1–7.5s for cup grip only | Reused original reviewed still. Free hand settles onto trousers; cup contact stable. Low eyelids, facial softening and posed expression remain. Partial movement improvement; rejected as a replacement. |

The café reference contains a sip and later prolonged eye closure; it is not a matched six-second quiet pause. These actions were not requested in the new take. The walking/sunglasses clip is unsuitable for these seated scenes. References supply behavior, not actor identity or wardrobe.

## What this comparison can establish

Reference observations informed the generation prompts. **No reference video was uploaded for direct motion conditioning.** The alternative model, source pose, resolution and playback timing also change, so causal benefit from sample02 is unproven. This is a bounded diagnostic, not a controlled motion-transfer benchmark.

Original footage was recovered from Fal history: all six historical human videos and five source images. Selected video/still hashes match the original delivery manifests. The original full film encode remains missing; the comparison uses recovered human footage and documented editorial ranges, not a reconstructed full film.

The first two comparison sections retain the original 3s and 4s windows. The phone return labels original 0.5× versus candidate 1×. Café shows the shared first 5s at native speed: its original slot is 6s, while the new endpoint produced 5.03125s. There is no padded or slowed candidate. Full native-speed clips are available separately to inspect these differences. Comparison audio is intentionally absent; the original speaking clip remains separately available with audio.

## Review and cost

Human reviews used chronological 4fps portrait sheets over each full take and 8fps enlarged face/hand/prop sheets for the original phone/café and first candidates. Reference review used 146 sampled chronological frames plus overview sheets. Source stills were inspected before generation; clips passed full FFmpeg decode. These are subjective sampled visual reviews, not uninterrupted playback or calibrated measurements. Detailed scores and untested fields are in `sample02-test-results.json`.

Three trials: **$0.25 estimated, $0.30 reserved including buffer**. Sideway cumulative: **$10.37 estimated, $11.97 reserved against the previously approved $12 cap**. Historical accounting was reconstructed from matched provider requests and five retained $1 image allowances; the original ledger bytes were not recovered. Confirmed invoice charges are unavailable. Remaining reservation capacity is $0.03, insufficient for another paid trial. No budget reset or increase was used.

The evidence supports retaining the original footage and carrying forward the café hand-support observation. It does not support calling any candidate an overall realism improvement.
