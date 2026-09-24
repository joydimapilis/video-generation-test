# Kite Tomorrow — character revision

The final 38-second film uses the selected Seedance 2.0 take for the existing 0–3.6-second human opening. The shot now plays at native speed. All subsequent visuals are the already improved deterministic UI pass 2; copy, timing, narration, music and ending remain unchanged.

## Human review and selection

One four-second, 1080p, silent image-to-video test used the reviewed original reference. No new source image was purchased. The same identity, supported hand positions, room and wardrobe were retained. The old Veo Fast prompt suppressed facial changes and the edit ran at half speed; the new prompt allows a quiet breath, blink, small reading gaze changes and slight supported finger relaxation.

Review used 32 chronological samples at 8 fps, full-frame/face/hand close-ups and matching editorial-time comparisons. The selected take maintains laptop-directed gaze, a shorter unstretched blink and subtle brow/lip relaxation. Visible hands remain supported without obvious merging; the laptop and desk stay stable. The encoded side-by-side comparison preserves the old 0.5× edit beside the new 1× segment.

The performance improves, but the new face is **softer and less finely detailed** than the old take. An initial impression of improved skin texture did not hold up in the matched close-ups. No sharpening or beauty processing was applied. The pose is still restrained; occluded fingers cannot be fully audited. This is a usable incremental improvement, not a complete elimination of the generated look. There is one human shot, so cross-shot identity is untested. No speech, typing or complex object interaction was tested. Model, prompt and speed changed together: this is not proof of general model superiority.

## Media and evidence

- Final: `artifacts/final_outcome/kite-tomorrow-character-pass/kite-tomorrow-final.mp4`
- Comparison: `artifacts/final_outcome/kite-tomorrow-character-pass/character-comparison.mp4`
- Original and rejected source takes remain under `artifacts/kite-tomorrow-revision/recovered/`.
- Candidate, exact prompt, queue ID, quote and immutable reservation: `artifacts/library-loop-kite-tomorrow/`.
- Qualitative review: `review_notes/kite-tomorrow-character.json`.
- Scorecard: `docs/KITE_TOMORROW_CHARACTER_SCORECARD.md`.

## Cost and authorization

The user's “Now please go ahead and continue with the character and the $3.14” authorized the previously blocked single paid test. One request was submitted, with a $2.73 estimate and $3.14 reservation including the 15% buffer. No paid retries, new images or audio were generated.

Pricing was checked before submission: Fal Seedance 2.0 image-to-video 1080p, four seconds, no audio, standard bitrate. Pricing API returned $0.014 per 1,000 tokens; the more conservative published per-second estimate was rounded up to $2.73. Actual invoice reconciliation was attempted but the API key returned 403 for billing access, so confirmed charge remains null.

Earlier spend remains 31.38 Higgsfield credits plus an unknown-cost source image. No USD conversion or historical upper bound has been invented. The same-video record retains that history and the ordinary cumulative $10 ceiling, alongside this explicit single-test incremental exception. The cumulative USD total is unknown; this report does not claim it is below $10.

## Rendering and validation

HyperFrames CLI upgraded from 0.8.46 to 0.8.47 for the new revision projects. The original projects and renders remain intact. Full composition checks passed with no errors; 109/109 contrast checks passed and 300 motion samples had no findings. One lint warning is reviewed and accepted: the Kite icon is intentionally reused as the app/header icon and message avatar in the handoff scene, not a duplicated video/audio track. Runtime and layout checks passed. The comparison passed its checks, including 10/10 contrast checks.

Final encoded review and decode/audio verification are recorded in `artifacts/final_outcome/kite-tomorrow-character-pass/verification.json`. UI remains an illustrative reconstruction informed by official Kite references, not an authenticated recording of a real launch. No additional UI features or claims were introduced in this character revision.

Final verification completed: 1920×1080, 30 fps, 38 seconds; full video/audio decode passed. Encoded UI text, opening, scene joins, caption and ending were visually inspected. Decoded audio SHA-256 matches UI pass 2 exactly. Final SHA-256: `4894d53755694501447041c93ed1c38f0b4aeeaafb7f777aa859dabe9f0a85d2`. No new listening review is claimed.
