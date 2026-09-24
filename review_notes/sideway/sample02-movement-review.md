# Sideway × sample02 — reference review and test preparation

2026-09-19. **Initial reference review below; recovery and generation subsequently completed.** See `sample02-test-results.json` and `sample02-test-results.md` for current findings. The initial missing-media and no-spend statements below describe the pre-recovery stage only. Original full-film selection remains unchanged.

## Evidence actually inspected

All six supplied sample02 clips passed full FFmpeg decoding. The repository
library resolver and `scripts/inspect_library_slice.py` were used with a
command-scoped `AMARILLO_LIBRARY_DIR=references/sample02`. All six 12-frame
overview sheets were visually inspected. Additional chronological 2-fps sheets
were inspected for phone 233390 (0–7.5s), interview 297986 (0–7.5s), café 216598
(0–15.5s), and hands 736 (0–7.5s). This is sampled chronological inspection,
not uninterrupted real-time playback or precise blink/keystroke measurement.
Dense frames for the remaining ranges are extracted but not claimed as inspected.

Hashes, durations, dimensions, decode results and sheet paths are retained in
`artifacts/sideway-human-realism-test/reference-review/dense-manifest.json`.
Overview manifest: the adjacent `overview/manifest.json`.

The existing human-realism README and review were consulted for method. Sideway
scorecards and source manifests provide historical findings only: its MP4s,
stills, takes and original budget ledger are absent locally. Therefore no claim
is made to have watched Sideway or ranked its current shots from fresh evidence.

## Provisional movement matches for every human window

| Sideway window | Closest sample02 reference | Observed cues and applicable range | Transfer limits |
| --- | --- | --- | --- |
| Phone opening, 0–3s | `233390_medium.mp4`, approximately 0–3s; supplement `736-138808023_medium.mp4`, 0–3s | Seated phone attention with chin naturally inclined; small hand changes while torso stays comparatively quiet. Hand close-up shows stable support around device with localized thumb movement. | Different person, lighting and setting. Original uses a tapping index, while the close-up uses thumbs: borrow support/contact, not a new grip or finger choreography. |
| Speaking portrait, 3–6s | `297986_medium.mp4`, approximately 0–2s | Low joined hands, forward conversational posture, mouth movement with small head changes and a fairly consistent attention direction. | Brows are expressive; after about 2s posture shifts and a broad smile develops. Do not import the later smile/laugh. Different speech cannot supply Sideway's lip movement. |
| Phone return, 6–10s | `233390_medium.mp4`, approximately 0–4s | Sustained phone-directed attention with small unequal hand/head movements; phone stays below the face. | Original stretches source 1–3s to four seconds at 0.5×. Compare that editorial baseline and native-speed motion separately. Exact eye fixation is not measurable at these sampled sizes. |
| Café, 26–32s | `216598_medium.mp4`, approximately 0–1s for downward attention; 1–7.5s for grip mechanics only | Head/shoulder relationship remains coherent as a cup rises; fingers stay around the handle; cup and hand travel together. | A sip follows, then eyes remain closed for a long interval around 8–13s. No suitable six-second quiet coffee-gaze performance was established. Use grip/posture observations to inform I2V, not wholesale motion transfer. Elbow/counter contact is outside this reference's crop. |

Other references: `258057_medium.mp4` is a useful secondary hand/phone close-up
with small finger actions and a stable supporting grip, but it gives no face,
neck or eye-direction evidence. `6590-193729460_medium.mp4` supplies outdoor
phone use, but sunglasses hide the eyes, the person walks, and a hand comes to
the face mid-clip. Those actions do not match Sideway's seated phone shot.
No sample02 actor is an identity source.

## Historical failure leads — not a new ranking

The user previously rejected phone v1 for a missed screen eye line and café v1
for staged sideways posture. Those failures were already addressed in v2.
The selected phone v2 still had early repeated taps and a later head lift/long
blink; that later range was excluded from the film. Café v2 retained a slight
cup lift and parted lips despite instructions. Story v2 was previously accepted
for restrained delivery. These records suggest examining phone and café first,
but the current actual footage must decide which shots need regeneration.

The half-speed phone return may magnify sluggishness. That is an untested
editorial hypothesis, not an observed defect in the missing encode.

## Conditioning route and cost check

Fal's current [Kling v3 Pro motion-control schema](https://fal.ai/models/fal-ai/kling-video/v3/pro/motion-control/api)
accepts a character image plus a movement video. Its reference-video guidance
requires a visible head and upper/full body, so the hands-only clips are not
suitable direct motion-control inputs. Image orientation can help retain the
source pose; it does not guarantee framing or prop contact. The speaking
reference does not carry Sideway's words, so direct motion transfer alone would
not preserve dialogue synchronization.

The [motion-control price page](https://fal.ai/models/fal-ai/kling-video/v3/pro/motion-control)
displayed $0.168 per second when checked on 2026-09-19. A four-second phone
pilot would estimate $0.672, rounded conservatively to $0.68, with $0.79 reserved
after the repository's 15% buffer. This is a planning quote, not a submitted
request, complete multi-shot budget or verified invoice. Endpoint minimums and
the runner adapter still need preflight before a live request.

The latest delivery manifest reports $11.67 reserved under the previously
approved $12 cumulative cap, leaving $0.33. Even that pilot would exceed the
documented available reservation capacity. The original budget ledger is
missing and must not be recreated as an empty ledger. No budget increase has
been requested for a speculative multi-shot batch; first recover originals,
rank actual defects, and finalize the smallest useful costed test.

## Resume requirements

Recover `artifacts/final_outcome/sideway/sideway-cafe-revised.mp4`,
`videos/sideway/assets/` and `artifacts/library-loop-14/` from the original
production folder. Verify hashes against `videos/sideway/sources.json` and
`assembled_outputs/sideway.json`. If only the encoded film survives, it supports
visual review and baseline extraction, but source-image recovery and historical
budget reconciliation still need an explicit documented resolution.

Inspect actual footage and source images; prepare exact candidate payloads and
current cost quotes; retain all earlier reservations; resolve any required
cumulative-cap increase before generation. Then run the bounded I2V test,
review every candidate chronologically and render the comparison only. Keep the
full Sideway film and its selected-takes manifest unchanged.
