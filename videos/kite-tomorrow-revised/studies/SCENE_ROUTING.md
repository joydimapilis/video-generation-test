# Kite Tomorrow — independent scene routes, round 2

Current master: `artifacts/final_outcome/kite-tomorrow-revised/kite-tomorrow-revised.mp4` (38 s).
Do not force one model to handle both people and product graphics. The routes below
were selected before any new generation. No paid requests have been submitted.

| Film time | Scene | Route and decision |
| --- | --- | --- |
| 0–3.6 s | Person at laptop | Reference-conditioned I2V; first candidate Seedance 2.0 standard, 1080p, 4 s, audio off, normal-speed 3.6 s editorial selection. Candidate, not a proven winner. |
| 3.6–7.2 s | Calendar and missing page | Retain existing deterministic composition; no reason to regenerate. |
| 7.2–16.5 s | Request and returned draft | HyperFrames HTML/CSS, Lato inside Slack, Onest for film titles, actual Kite app icon, source-backed interface hierarchy. Independent UI test. |
| 16.5–35 s | Draft and revision | HyperFrames HTML/SVG. Relay is the fictional deliverable, not Kite's product dashboard. Match feedback UI to the selected handoff treatment; retain exact page copy and editing beat. |
| 35–38 s | Brand ending | Retain official wordmark, existing CTA and timing. |

## Person: actual failures and changed hypothesis

Current source is Higgsfield Google Veo 3.1, params `model=veo-3-1-fast`,
`enhance_prompt=true`, `quality=high`, 4 s. The film selects the initial 1.8 s
and plays at 0.5×. Two prior Kling 3 Pro takes were rejected for gaze.

Reviewed the current encoded shot and 0.25-second source face/hand samples.
The still has more useful natural texture than the animated cheeks/eye region.
The largely static hand pose reads as staged, gaze rises late, and hair/cloth
barely move. Exact finger count is partly occluded; do not score unseen anatomy.
Only one human shot exists, so cross-shot identity consistency is untested.

The enhanced prompt explicitly asks for perfect stillness and forbids facial
expression changes. This conflicts with the user's desired micro-expressions.
The second prompt also confuses looking at the screen with the keyboard/hinge.
Half-speed playback makes the already small performance slower. These are
workflow problems as well as a possible model-quality problem; a model switch
alone is not a demonstrated fix.

First use the recovered original reference as the identity/lighting anchor. It
already contains ordinary skin texture and coherent object placement. A still
edit is desirable if it can establish a less posed wrist/hand setup without
changing identity; it is not permission to invent freckles or beauty-retouch the
face. Do not request a task the selected still cannot physically support.

Test Seedance 2.0 with one restrained action, normal speed and no automatic
prompt expansion: a reading refocus on the actual screen, unforced blink, quiet
breath and tiny supported finger relaxation. Keep props and camera fixed, with
hair/cloth movement caused by the body. No task-switch, head lift or performed
smile. The prepared prompt is in `human-motion-round2.txt`.

Reject a candidate if gaze leaves the screen, cheek texture boils, digits fuse,
wrist contact slides, or the face becomes a polished mask. Skin, gaze, expression,
hands, posture, object contact, secondary motion and identity each need review.
No success score until real output is inspected chronologically and at close range.

Seedance's first-party provider documentation supports reference frames and
character/fabric motion, but does not establish superiority on this woman's
shot. Full Veo 3.1 is a second candidate if the first take fails. Do not repeat
Kling 3 unchanged after two failures. Static model defaults do not override
shot-specific results. Crew's useful lesson is observable action and explicit
entry/exit state, not a blanket endorsement of Veo Fast.

## UI: source-backed improvement

The current UI is already deterministic; it looks generic because of its
simplified chrome, uniform typography, oversized fictional draft card, sparse
composer and weak message hierarchy. It is not evidence of generated glyphs.

Reviewed Kite's current public Slack demonstration at https://kite.ai/ and its
workflow documentation at https://docs.kite.ai/slack/approvals. The site uses
Lato in Slack UI, distinct from Onest brand typography, channel tabs, compact
APP/time metadata and a formatted composer. Capture and measured tokens are in
`artifacts/kite-tomorrow-round2/`. This is public marketing UI, not authenticated
product evidence. Opaque blue chrome is an adapted film treatment; do not claim
pixel-perfect reproduction of a signed-in account.

`ui-product/` tests this treatment with the original request/notes/draft content
and 9.3 s timing. Preview and Review are supported by Kite's documentation.
The thumbnail is the actual existing fictional Relay page. Illustrative times
and company content remain visibly covered by the fictional-workflow label.
No new capabilities, publication state or performance claims are introduced.

## Cost boundary, not an invented historical estimate

The standing $10 cumulative cap is a real constraint. Current Fal listed rates:
Seedance 2.0 1080p $0.682/s → four seconds $2.728, proposed buffered allowance
$3.14 (15%, rounded up). Standard bitrate, audio off. This is a planning estimate,
not a reservation or confirmed charge. Recheck the provider quote before submit.
Full Veo 3.1 1080p without audio lists $0.20/s; four seconds would be $0.80
before buffer, subject to current schema acceptance. A new still edit would be
an additional cost, not included in these video-only allowances.

Historical confirmed spend remains 31.38 Higgsfield credits plus a source image
with unknown dollar cost. No valid historical USD bound was provided or found.
The answer “Add a bound when it serves a real constraint” does not supply a
number or change the ceiling. Therefore a paid model test remains pending;
unknown cost is not zero and the budget has not been reset. Reusing the original
reference adds no new image charge. This pass's paid generation spend is $0.

Sources checked during this pass:
- https://fal.ai/models/bytedance/seedance-2.0/image-to-video
- https://fal.ai/models/bytedance/seedance-2.0/image-to-video/api
- https://fal.ai/models/fal-ai/veo3.1/image-to-video
- Current authenticated Higgsfield `model list` and `model get seedance_2_0`.

The existing aggregate learning artifact is absent in this checkout. Historical
Crew/Serein/Portion reports and source prompts inform the hypothesis, not a
fabricated cross-loop ranking. Prior actual Cero/GrokBot library samples support
keeping context visible as a result arrives; neither proves human-model quality.


## Completed independent tests

UI product shot: local render, 9.3 s at 30 fps; check passes 201/201 text
contrast checks. Side-by-side compares the previously delivered encoded handoff
against the new treatment at identical duration. Reviewed encoded chronological
samples and full scene states; accepted the typography, chrome, message hierarchy
and card treatment as a visible, subjective improvement. Extended that treatment
to the feedback panel in the separate `videos/kite-tomorrow-ui-pass2` master.

Person timing diagnostic: rendered the same existing source at 0.5× and 1×
side by side for 3.6 s. This is not a new model test. The normal-speed version
still exhibits gaze lift and persistent posed hands, so it is rejected as a
replacement. Original source skin texture is not restored by a speed change.
Model comparison and new-reference realism scores remain null.


## Explicit authorization received

The user subsequently instructed: “Now please go ahead and continue with the
character and the $3.14.” This authorizes the single previously blocked test.
One request was submitted using the unchanged reviewed reference. The immutable
$3.14 reservation, quote and queue ID are in
`artifacts/library-loop-kite-tomorrow/budget.json`. Historical credits and unknown
source-image USD are retained there; the cumulative prior spend is not set to
zero or represented as verified below $10. No broader retry allowance is inferred.


## Authorized character test completed — 2026-09-18

One Seedance 2.0 reference-conditioned test was completed under the explicit $3.14 incremental authorization. Selected 0–3.6 seconds at native speed for more natural gaze/blink/expression timing. Matched close-ups show **softer**, not better, fine facial detail; the pose remains restrained. No new source image, paid retry or audio generation. Latest editable project: `videos/kite-tomorrow-character-pass/`. Final: `artifacts/final_outcome/kite-tomorrow-character-pass/kite-tomorrow-final.mp4`. Review and cost limitations: `videos/kite-tomorrow-character-pass/DELIVERY_REPORT.md`. Estimate $2.73, reserved $3.14, actual charge unverified; historical USD still unknown. Prior pending-test notes above describe earlier states.
