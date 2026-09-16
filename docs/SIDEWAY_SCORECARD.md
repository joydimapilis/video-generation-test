# Sideway evaluation

Original delivery (superseded): `artifacts/final_outcome/sideway/original/sideway.mp4`. The current revision is `sideway-revised.mp4`; see the revision review below. Scores are subjective production judgments supported by sampled frames and mechanical verification, not audience research.

| Take | Route | Decision | Observations |
| --- | --- | --- | --- |
| sideway_phone_v1 | Approved still → Kling 3 Pro, silent, 6s | Superseded after user gaze feedback | Visible phone, stable supporting grip, phone-directed gaze. Several tiny taps rather than the requested single tap; still reads as plausible browsing. |
| sideway_story_v1 | Approved still → Veo 3.1 Fast, native audio, 8s | Superseded after user dialogue feedback | Consistent identity, skin texture, intelligible requested speech. Some eyebrow emphasis; only four seconds of on-camera speech retained. |
| sideway_arrival_v1 | Approved still → Kling 3 Pro, silent, 6s | Selected; 8.5/10 | Natural cup grip, relaxed posture, stable face and clothing. Mouth remains closed beneath the reflection voiceover. |

All three source images passed visual review before I2V. No source regeneration was needed. Phone interaction was established in the still. The café still uses a handled cup despite the requested handleless cup; its natural handle grip was accepted.

## Assembly improvements

- Corrected an overlapping brand identifier at the phone-to-app expansion.
- Hid inactive UI states and retired outgoing controls before incoming panels covered them.
- Increased headline line spacing to eliminate detected overlap.
- Kept the expanding app surface opaque for legibility during the transition.
- Verified touch centers against controls and the selected 60-minute total against 22 minutes walking plus 38 minutes lingering.
- Reviewed portrait source sheets at their actual aspect ratio; the generic landscape evaluator sheet distorts portrait media.

## Final evidence

Full decode succeeds with no detected black intervals. Audio peaks at 0.717; correlation against the intended speech/music mix is 0.99808. Both speech excerpts retain source alignment with zero-offset correlation above 0.9999999. This verifies timing, not perceptual lip sync by itself.

The 10s and 26s composition joins have mean pixel differences below 0.003/255. The ending holds steadily, with mean difference 0.00283/255. Six decoded source-region comparisons fall between 2.13 and 2.23/255. The rendered portrait review sheet confirms the product workflow, café result, visible phone interaction, and final callback.

HyperFrames lint, runtime, layout, motion, and contrast checks report zero errors and zero warnings. Contrast passes 50/50 checks. Geometry verifies touch targets, deterministic forward/backward seeking, route markers, and duration arithmetic.

## Reusable learnings

One native dialogue take can supply a brief visible speaking moment and a later reflection with consistent voice identity. Keep the latter over a closed-mouth reaction. Stable start-frame interaction permits tiny movements without asking the video model to create a grip. Modular UI seams need distinct element IDs and decoded boundary checks; isolated snapshots can be misleading. Treat hidden states explicitly so text and touch feedback do not overlap during transitions.

Budget: $5.56 estimated including three $1 image allowances; $6.41 reserved against a new $10 cap. All three video requests completed. Image charges are not exposed by the built-in tool. Sideway and its route are fictional; there is no live routing backend.

## Dialogue and gaze revision

User feedback overrides the original sampled gaze approval: the original phone take missed the screen in some moments. It is now rejected in the machine scorecard and learning records. The original dialogue was also judged too scripted and omitted a spoken app name.

The phone still was regenerated with a lowered chin and a raised phone closer to the body midline. Both eyes visibly target the display; hand/device geometry and identity were checked before I2V. The revised prompt holds that screen target and discourages eye darting or head lifting. Source review: `review_notes/sideway/phone-image-v2.json`.

Selected phone v2: opening source0–3s; return source1–3s at0.5×. The return is a quiet reading stretch. The longer blink and head lift around3.3–4.6s are excluded. Taps occurred earlier than requested, and exact one-tap choreography was not achieved. Review used24 chronological enlarged eye/phone frames plus full portrait samples.

Selected story v2: “I’d save all these places, then forget about them.” / “Sideway maps them out for me. Way easier.” The exact wording is confirmed by local ASR. Three seconds remain on camera; the reflection uses the same voice take over the café reaction. ASR and audio alignment do not independently prove natural delivery or lip sync.

Both new takes are accepted for the selected ranges, with subjective edit-readiness8.5/10. The café take remains unchanged. Revised source selections and speech cut points live in `videos/sideway/selected-takes.json`. All requests remain in the original ledger: estimated$8.44, reserved$9.73 of$10, including four$1 image allowances; image invoices are not exposed.

Revision encode verified: 29,114,805bytes; SHA-256 `8d1b817834ce3404a87adaf848b81a92bcb702e3be28c9d87ced2a983bfcca02`. Audio peak0.7224; correlation against the authored pre-carve mix0.99864. Native speech cut alignment exceeds0.9999999. Ten source-region checks are below2.20/255, including the retimed return. The final encoded transcript retains both exact sentences. Final eye/phone crops were inspected. No black intervals or decode errors.

## Candid café revision

The user found the sideways café pose staged. Arrival v1 is now superseded. A new image aligns his head with his forward-facing shoulders, lowers his gaze toward the coffee, removes the hand-in-pocket pose and supports his elbow on the counter. Both hand anatomy and gaze were reviewed before animation. The free hand rests near his waist rather than on the counter; this is recorded in the still review.

Arrival v2 is selected (subjective edit-readiness8.5/10). A24-frame enlarged chronological review shows stable head/shoulder orientation, coffee-directed gaze and handle grip. The cup lifts slightly and his lips part briefly early despite stricter prompt instructions; the motion reads as a quiet breath near coffee. There is no sideways street glance or camera-facing smile. Full decode passes.

The same6-second slot and native reflection remain in place. Hash checks verify the existing phone and speaking clips, speech/music files, composition index, and all scene HTML are unchanged. User approved a total$12 cap. Cumulative estimate$10.12 includes five$1 image planning allowances; total reserved$11.67. Tool image invoices remain unavailable.

Café revision final verification: 29,590,967bytes; SHA-256 `178493db8b740913365f28de478eab483f44c658860fd4782daae4f17c300a4e`. Twelve decoded source-region comparisons pass (all below2.20/255). Exported audio correlation with the prior delivery:1.00000000. Nine final café frames inspected. No detected black intervals or decode errors. All five HyperFrames audit groups report zero errors and warnings.

Tracked evidence: [machine scorecard](../review_notes/sideway/scorecard.json) and [final verification](../review_notes/sideway/final-verification.json). Generated frame sheets and full media remain local under `artifacts/`.
