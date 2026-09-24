# Kite purposeful-contact test review

Result: **partial improvement; diagnostic only, not integrated into the film**. One new source still passed a still-frame review, then one Seedance 2.0 image-to-video request produced the new shot. The revised hands are purposeful; sustained trackpad contact and facial naturalness remain imperfect.

## Hands

Clearer purpose than the current joined resting hands: separate roles and visible device contact are established in the still and retained at the end. No obvious fused visible digits in sampled frames; hidden digits cannot be audited. From approximately 0.25–1.1 s the active hand lifts and repositions before returning, rather than maintaining the requested gentle trackpad glide. Continuous contact instruction therefore only partly followed.

## Gaze

The new still establishes a laptop-directed gaze, and the video maintains it with restrained eyelid/eye changes. No camera-facing glance. A full blink is not clearly evident in sampled frames, while the baseline has a clearer blink near 0.75 s. Do not claim improved gaze dynamics or that every requested micro-action occurred.

## Posture

Separated supported forearms and a modest forward lean read as task engagement. Small body changes stay restrained; no large gestures. More purposeful pose, but the performance remains very still.

## Purposeful movement

One small active-hand reposition and a long pause give clearer intent than the baseline resting finger curl. The second hand stays quiet. Action is more legible, but the brief lift weakens the requested sustained trackpad contact.

## Overall naturalness

Partial improvement driven chiefly by pose and task context. Face shape, hair and wardrobe remain recognizably consistent with the edited reference. Skin remains softly rendered and facial performance restrained; no convincing independent gain in skin realism is established. Hair and shirt motion are slight and do not imply wind. Treat as a useful diagnostic candidate, not a fully solved photoreal person.

## Device geometry

Contact is judged against the generated laptop surface. This is not a verified physical laptop layout or an accurate product UI. Complex typing, screen responses and real hardware correctness were not tested.

## Method and controls

Subjective chronological visual review: 48 sampled frames at 12 fps across 0–3.917 s, full-frame/face/hand contact sheets, plus final frame at 4.0 s; baseline face/hand sequences at 8 fps. Encoded comparison frames inspected at 0.2, 1.2, 2.5 and 3.5 s. Full decode checks passed. This is sampled frame review, not a claim of continuous real-time playback.

Both videos use Seedance 2.0, 1080p, 4-second request, 16:9, standard bitrate, no audio, native playback speed. The comparison uses the matching 0–3.6 s window. Source pose and matching action prompt changed together. The current API does not accept a seed input; the candidate returned seed 2020143156. This is one workflow test, not a still-only causal result. Clip 04 guided quiet posture/gaze, 02 finger contact, 03 task-related gaze, and 05 pauses/repositioning. Reference clips were not uploaded or recreated.

## Audit and cost

Exact still and motion prompts: `../kite-tomorrow-character-pass/studies/purposeful-contact-test/`. Request `01a0b443-bb89-7bf3-b53b-26b0d4b20a80` and resolved image input: repository `artifacts/library-loop-kite-tomorrow/budget.json`, run `kite_person_seedance2_purposeful_contact_v2`. Generation and resume log: `purposeful-contact-generation.log`. Source provenance/review: `source-images/purposeful-contact-v2.json` and `purposeful-contact-v2-review.json`.

New video estimate $2.73; buffered reservation $3.14. Built-in image-generation cost and final invoice charge were not reported, and are not zero. Previous Fal estimate $2.73/reservation $3.14 remains in the same ledger. Original 31.38 Higgsfield credits and original source-image USD remain unknown. The user explicitly waived the budget for this single test. Full film and existing selected opening were preserved.
