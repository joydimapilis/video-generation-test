# Kite Tomorrow — targeted realism and UI revision

Status: a second, explicitly UI-only master is delivered in `artifacts/final_outcome/kite-tomorrow-ui-pass2/`. Person and UI routes were reviewed independently; the paid human-model test is unsubmitted because historical USD spend remains unbounded. Earlier masters are preserved. No new paid generation. Earlier audit stages below are chronological records.

## Locked scope

Preserve the existing 38-second concept, story, narration, scene boundaries and pacing. Improve one character shot and one product shot first. Compare each against its original before extending the method to other affected material. Preserve the original delivery.

## Evidence available

Read the project's brief, storyboard, source review, delivery report, budget, composition HTML and builder, plus Kite's creative restart, Serein's interaction scorecard, Portion's scorecard and Crew's realism report. These are historical records and source code, not a fresh visual review of the current MP4.

At the initial audit, the checkout lacked `artifacts/final_outcome/kite-tomorrow/kite-tomorrow.mp4`, `assets/marketer.mp4`, the character reference still, and the voice/music/SFX files. Searches of the Conductor directories and likely local project/media directories did not locate the missing Kite Tomorrow media. The library resolver also failed: no configured or accessible saved reference library. A smaller startup-video folder exists on Desktop, but its footage has not been reviewed in this pass; the specific Pocket/Bloom/Notion references cited by the prior production were not recovered.

## Character candidate: 0–3.6 seconds

This is the only character shot in the tracked composition. Historical notes report two Kling 3 Pro takes rejected for upward gaze, followed by Veo 3.1 Fast high. The selected source range is 0–1.8 seconds, played at 0.5×. This identifies the revision target structurally; current facial, hand and motion quality remain untested without the media.

Hypotheses to test after recovery:

- An overly polished still may limit natural skin texture in every downstream take. Inspect the actual reference before deciding whether to replace it.
- Half-speed playback may make blinks, small expressions and body movement feel unnatural. Inspect real-time playback before treating this as a proven cause.
- A better still must establish screen-directed pupils, supported posture, plausible hands and actual object contact together. Preserve framing, wardrobe and lighting where usable.
- Specify small observable actions and physically caused secondary movement: quiet reading refocus, an unforced blink, subtle breath, cloth following body motion, hair settled in still air. Avoid adding a performance or complex gestures.
- Compare an improved reference through a costed I2V route at normal playback speed. Do not automatically retry Kling or declare another model superior: prior results are shot-specific, and current capabilities/prices still require verification.

## UI candidate: handoff and returned draft, 7.2–16.5 seconds

The product sequences are deterministic SVG/HTML animated by HyperFrames already. Switching to HyperFrames alone will not address the user's complaint.

Source-level concerns to verify visually:

- The Slack reconstruction uses a sparse sidebar, large message text and generic initial avatars. The Kite avatar is a letter K, while the official wordmark is used in the ending.
- At approximately 13.55 seconds the request fades out; the returned draft replaces it in the same position from 13.8 seconds. This can lose conversational context rather than showing a credible reply/thread progression.
- The draft card and later feedback panel are simplified editorial constructions. Their exact resemblance to signed-in Kite is explicitly unverified in the original records.
- The Relay page is a fictional deliverable, not Kite's own interface. Keep that distinction and do not introduce unsupported controls, state badges, publication or product claims.

The handoff is a provisional first UI candidate, not a visually confirmed weakest shot. Recover and inspect the MP4, then choose between this and the 16.5–35-second draft/review sequence. Use verified product assets where available; otherwise refine the existing deterministic reconstruction against current first-party evidence. Preserve text, beat times and narrative transitions while improving typography, spacing, alignment, branding and interaction continuity.

## Budget blocker

The existing ledger records 31.38 quoted Higgsfield credits across two rejected Kling takes, one Veo take and music, plus one source-image generation with unknown USD cost. The project's cumulative $10 ceiling applies to all of these and this revision. No USD conversion or conservative source-image cost bound is recorded. Do not reset the ledger, assume earlier spend was zero, or submit paid tests until cumulative spend can be bounded.

## Required inputs and next gates

1. Recover the existing MP4 and preferably the original character still/clips and audio from a supplied path or download link.
2. Establish a documented USD bound for prior generation so the same video's remaining budget is known.
3. Review chronological motion and close-ups; identify the weakest UI shot from the actual output. Preserve hashes and original copies.
4. Produce and internally review a stronger still if needed; test only the character insert and selected deterministic UI scene.
5. Compare old/new at identical duration, scale and timing. Character criteria: skin, eyes, expression, hands, posture, contact, hair/clothing and natural movement. UI criteria: fidelity, legibility, typography, spacing, alignment and interaction continuity.
6. Extend only demonstrated improvements, run required composition checks, and inspect the encoded comparison/final output before delivery.

The initial source audit above preceded asset recovery. Current findings and their limits follow; no numerical realism rating or confirmed historical USD amount is claimed.


## Recovery and visual findings

The user supplied the former Amarillo workspace path. That directory now contains only earlier Kite thumbnail cache files, not Tomorrow media. Archived Conductor context retained completed provider-job records. Downloaded the original source still, selected Veo clip, both rejected Kling clips and Sonilo music from their original job URLs without generation charges. File hashes and provenance are in `artifacts/kite-tomorrow-revision/recovered/manifest.json`.

The original final 38-second MP4 and local narration/SFX were not recovered. Visual comparison uses the recovered character sources and freshly rendered copies of the tracked UI scene. Do not describe this as watching the original final encode or verifying its audio.

Character review used chronological 0.25-second samples, full-frame views, enlarged face sheets and a hand sheet. Findings are subjective visual judgments from those samples, not full real-time playback or calibrated model scores:

- The original still has useful forehead/cheek texture, natural shirt folds and coherent desk/device geometry. It also establishes an idle, closely held hand pose that can read as staged when animated too little.
- Veo's cheek/eye region becomes smoother and more uniform than the source. The selected early range holds its gaze low for most sampled frames, then gaze starts rising around the end of the selected 1.8 seconds. The source goes noticeably upward in the later portion.
- Hands remain supported without obvious gross deformation in the inspected samples, but their near-static relationship to the desk adds little evidence of real computer use. Hidden fingers cannot be scored from this angle.
- Both Kling versions retain the historical failures: gaze rises and lips open; neither provides a clear full-length replacement for the 3.6-second slot. No previously rejected take was promoted merely to deliver a change.
- The archived expanded Veo prompt explicitly demands perfect stillness and forbids expression changes. This is a plausible contributor to stiffness; it is not a controlled causal finding. Half-speed playback is another plausible contributor to unnatural blink/body timing.

A replacement-image direction and bounded I2V comparison contract are prepared in `videos/kite-tomorrow/studies/CHARACTER_TEST.md`. No new reference image, model benchmark or replacement character shot has been generated. Current model capabilities/prices have not been verified for a paid route because historical budget headroom is still unknown.

## UI study and comparison

Reviewed the original handoff frames and the original draft/review frames at scene-local 4, 10 and 16.5 seconds. The handoff/returned-card sequence is the chosen first target: its oversized sparse layout, generic letter-K avatar and disappearance of the original request make the interaction feel diagrammatic. The later draft/review sequence also remains simplified; it is deferred under the user's two-shot-first process.

The isolated `ui-after` study changes only the 9.3-second handoff scene:

- Replaces the invented letter-K avatar with the official Kite Slack app icon.
- Uses a more coherent application shell, compact supporting navigation, consistent text hierarchy and aligned message/attachment/card controls.
- Keeps Maya's request and the release-notes attachment visible when Kite returns the draft.
- Uses an actual captured frame of the existing fictional Relay page for the preview thumbnail, rather than generating or inventing another miniature interface.
- Adds a visible hover/press response on Preview while preserving the original click timing.
- Retains the original message, notes, draft headline, action labels, 9.3-second duration and reveal timing. The main film's concept, narration, other scenes and pacing are not edited.

The subjective improvement is clearer product identity and conversation continuity, with a less diagrammatic layout. This is still an illustrative reconstruction, not a pixel-verified signed-in Kite recording. Official product evidence rechecked: https://docs.kite.ai/slack/approvals (Preview/Review and in-thread revisions), https://kite.ai/ai-marketer/kite-slack-app-icon.png (app icon), https://kite.ai/newsroom (brand assets).

Full checks pass for both studies. The candidate has zero runtime/layout/motion/contrast errors, 187 motion samples and 164/164 passing text contrast checks. A duplicate-media warning is expected because the same official app icon is intentionally shown in the sidebar and reply; both placements were visually inspected. An initial composer/button overlap was found visually and corrected despite the earlier automated layout pass. The new studies use HyperFrames 0.8.46 consistently on both sides; the main film's 0.8.45 pin is unchanged.

## Available reference-library review

The full saved Pocket/Bloom/Notion library is still unavailable. A smaller existing startup-video folder was resolved explicitly through `AMARILLO_LIBRARY_DIR` and inspected with `scripts/inspect_library_slice.py`. Chronological contact sheets reviewed for Cero (34.8s) and Motion-5/Grok Bot (32.5s):

- Cero maintains recognizable screen content across physical-product and enlarged UI shots. Use continuity of the same deliverable; do not copy its neon treatment or dramatic product motion.
- Motion-5 keeps a recognizable conversation while replies and supporting work appear. Use preserved request context; do not import its bot cast, claims or multi-panel structure.

These are sampled visual/pacing observations; audio and frame-by-frame motion were not reviewed. No reference footage was reused. Manifest: `artifacts/kite-tomorrow-revision/references/manifest.json`.

## Remaining gate

New spend is $0. Existing spend remains 31.38 quoted Higgsfield credits plus an unpriced source image. The supplied media location did not resolve the USD cost. The same cumulative $10 cap remains in force. A conservative documented USD bound for earlier generation is required before reserving and submitting a new character test. The UI study is not installed into the main film and no full-film revision is claimed complete.

## Encoded study delivery

Delivered `artifacts/final_outcome/kite-tomorrow-revision/ui-comparison.mp4` (labelled side-by-side) and `ui-revised-shot.mp4` (full-frame candidate). Both are 9.3 seconds at 30fps, intentionally silent. The comparison is 1920×640; the standalone study is 1920×1080. Each of the before, after and comparison files fully decodes to 279 frames. Chronological encoded UI frames were inspected at 0.5-second intervals, plus a full-size final-state frame and the labelled comparison frame. Scene joins outside the isolated handoff and the original final audio remain unverified.

The final candidate retains the request while the reply arrives, the two official app-icon placements are intact, and the cursor lands on Preview without the composer overlap. The page thumbnail now comes from the existing draft composition. No change is applied to the main film until the character test and two-shot comparison can be completed.

Machine verification, output hashes and cost status: `artifacts/final_outcome/kite-tomorrow-revision/verification.json`. Delivery manifest: `assembled_outputs/kite-tomorrow-revision.json`.


## Complete final delivery after user continuation

The user requested the finished video after the isolated comparison. Delivered
`artifacts/final_outcome/kite-tomorrow-revised/kite-tomorrow-revised.mp4` from
`videos/kite-tomorrow-revised/`, preserving the original project. The tested
handoff treatment is integrated and extended to the later feedback panel;
original timings and story remain 38 seconds. The feedback now retains the
draft context and the exact user instruction in one readable thread.

Restored all three original narration lines locally using the original Kokoro
cache, af_heart voice and speed 0.94. Reused recovered Sonilo music, reconstructed
seeded cut cues, recalculated the voice carve, and faded the music at the ending.
Final encoded mix transcription recovers every scripted sentence; measured
integrated loudness is -16.0 LUFS and true peak -3.8 dBFS. This is objective
measurement/ASR, not a claim of real-time listening.

Reviewed 24 chronological encoded samples spanning human footage, UI actions,
scene joins, revised hero, and ending, plus full-size product frames. Check
passes runtime/layout/motion/contrast, and all 1,140 frames decode. Intentional
icon repetition and a 0.03-second near-invisible notes/reply overlap were reviewed.
Final verification, hashes and limits are in the delivery folder.

Reusable learning from this revision (subjective): improving a deterministic
UI requires actual interface hierarchy, persistent conversational context and
consistent brand assets; the choice of renderer alone does not improve fidelity.
Extending the same thread treatment to feedback improves continuity without
changing the storyboard. Keep fictional deliverable UI distinct from product UI.
No new model-routing or character-realism score is recorded: source alternatives
were reviewed, but no new reference/I2V test was submitted. Original character
limitations persist. Account transactions corroborate 31.38 prior credits; the
USD conversion and source image cost remain unresolved. New paid spend is $0.


## Independent person/UI review — second pass

Reviewed the delivered full cut, existing source and actual expanded Veo prompt.
The explicit ban on expression changes and perfectly still hands/body contradicts
the realism brief. Half-speed playback also slows an already limited performance.
A local 0.5×/1× diagnostic preserves the visible gaze defect at normal speed, so
it is rejected as a replacement. There is one person shot; cross-shot identity
consistency remains untested. Skin/motion scores for new models remain null.

Recommended first new person candidate: Seedance 2.0 standard, original reviewed
reference, 1080p, four seconds, audio off, one coherent reading action at 1×.
This is a test hypothesis, not evidence of superiority over Veo. Current public
provider schema/rates and the authenticated Higgsfield model catalog were checked.
The proposed video-only $3.14 allowance includes a 15% buffer; no reservation or
submission occurred. The earlier 31.38 credits and unknown source-image USD cost
still prevent a defensible remaining budget under the same $10 ceiling.

UI remains HyperFrames. Inspected and captured Kite's public Slack demo, including
actual Lato font assets and computed UI tokens; distinguished it from a signed-in
product capture. Added source-backed channel tabs, compact message metadata,
formatted composer and a restrained link preview; preserved scenario copy and
Preview/Review semantics verified in Kite docs. Opaque blue chrome adapts the
site's translucent demo treatment to legible video contrast. Illustrative times
and fictional Relay content are not represented as real customer activity.

UI study check passes, including 201/201 contrast checks. Encoded chronological
review shows a subjective improvement in hierarchy and product plausibility.
Carried the Lato/card treatment into the feedback panel and rendered a separate
38-second UI-only master; existing person and audio retained. Full check passes
109/109 text contrast checks and all runtime/layout/motion gates. Encoded full
file and study files decode without errors. Reviewed new encoded midpoint/join
samples and ending. Audio PCM matches the prior master exactly. Intentional
repeated app icon warning was reviewed. No claim of newly realistic human output.

See `videos/kite-tomorrow-revised/studies/SCENE_ROUTING.md`, its prepared prompt,
`artifacts/kite-tomorrow-round2/human-test-proposal.json`, the before/after UI reel,
and the person-speed diagnostic. New paid generation in this pass: $0.


## Authorized character test completed — 2026-09-18

One Seedance 2.0 reference-conditioned test was completed under the explicit $3.14 incremental authorization. Selected 0–3.6 seconds at native speed for more natural gaze/blink/expression timing. Matched close-ups show **softer**, not better, fine facial detail; the pose remains restrained. No new source image, paid retry or audio generation. Latest editable project: `videos/kite-tomorrow-character-pass/`. Final: `artifacts/final_outcome/kite-tomorrow-character-pass/kite-tomorrow-final.mp4`. Review and cost limitations: `videos/kite-tomorrow-character-pass/DELIVERY_REPORT.md`. Estimate $2.73, reserved $3.14, actual charge unverified; historical USD still unknown. Prior pending-test notes above describe earlier states.


## Dedicated human realism references reviewed

The five user-supplied clips in `references/human-realism/` were reviewed as behavioral references. Closest overall match to the current quiet desk opening: `human-reference-04.mp4`, approximately 0–4 s. Use 02 for finger/key contact and 05 for laptop/trackpad-area coordination as secondary references. See `review_notes/human-realism-references.md` for observations, limits and an untested source-pose hypothesis. No generation, provider upload or change to the delivered film occurred in this review.


## Purposeful-contact human test

One new still and one Seedance 2.0 image-to-video result were completed under the explicit budget exception. Partial pose/purpose improvement; brief hand lift and restrained facial behavior remain. No full-film change. Detailed findings: `kite-tomorrow-purposeful-contact.json`; editable comparison/review: `videos/kite-tomorrow-contact-test/`.


## Full-film delivery after purposeful-contact test

User requested the whole video. The 38-second final now uses purposeful-contact v2 at native speed, with existing UI/audio/timing preserved. The early reposition is editorially usable as a work pause; exact continuous-contact and facial-realism limitations remain. No new paid calls. Original test review is preserved as historical evidence. Delivery: `assembled_outputs/kite-tomorrow-final.json`; full review: `videos/kite-tomorrow-final/DELIVERY_REPORT.md`.


## Slack reference edition

The subsequent full-video revision uses the user-supplied dark Slack screenshot for deterministic UI and thread styling, with the same purposeful-contact human asset. No new human generation or realism score. See `review_notes/kite-tomorrow-slack.json` and `assembled_outputs/kite-tomorrow-slack.json`. Earlier human limitations and generation costs remain unchanged.
