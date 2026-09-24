# New computer movement studies — batch 02

This is a new production with newly generated people, scenes and source images. Real videos informed written movement directions only. No supplied clip or extracted reference frame was uploaded, directly transformed, included in a composition or used as a character reference.

## Selected outputs

| Sample | Range | Finding |
| --- | --- | --- |
| Desktop reading pause | v3, 2.167–3.667s (1.5s) | Short supported-hand reading pause only. All full desktop takes rejected; sustained hand realism remains unresolved. |
| Mouse pointer movement | v2, 0–6s | Grip and contact retained; brief head dip. |
| Laptop typing | v1, 0–6s | Low localized typing and screen gaze; brief mouth opening and some regular cadence. |

The desktop reading-only attempt also introduced typing and hand lifting, so it was rejected. The short selected section does not turn the full take into a successful action. Original untrimmed takes are supplied alongside selected videos. This batch does **not** establish consistent improvement from movement observations.

## Reference observations

The user's movement collection is stored at `references/human-realism/`; no separate `human-movements` folder was found. Its README and existing review notes were consulted. `scripts/inspect_library_slice.py`, using the repository library resolver, inspected the local collection. The normal library discovery did not expose additional relevant general-library footage.

Before generation, chronological reference frames were inspected: clip 02 at 0–2s (8fps hand detail), clip 03 at 0–2.5s and 5–7s (2fps context), clip 04 at 0–2.8s (2fps context), clip 05 at 0–3s and 7–9s (8fps hand detail). Exact paths, hashes, applied sample IDs and limitations are in `videos/computer-movement-studies-02/reference-observations.json`.

Useful observations were uneven finger timing, unequal hand roles, supported forearms, small gaze checks and much less head/body movement than hand movement. Clip 02 does not show gaze. Clip 04 uses a stylus; external mouse operation is a proposed application of restrained posture and attention, not behavior directly established by these references. Visible large curls/reaches in references were deliberately not requested. Identities, attire and scenes were newly conceived.

## Models and experiment limits

New source images used Nano Banana Pro, followed by image-to-video with standard Veo 3.1 at 1080p and without audio. Prior local Veo Fast results made Veo a reasonable candidate; standard Veo quality was a hypothesis, not a verified best-model ranking. Fresh endpoint schemas and setting-specific costs were checked before submission. Every new still was reviewed before animation.

No matched no-reference control exists. Seeds, prompts and sometimes source images changed during revisions. These results cannot establish that references consistently improve realism or distinguish reference effects from source pose, prompt simplification or model choice. Prompt guidance is not video motion conditioning, training or fine-tuning.

## Review and revisions

All complete generated takes were reviewed chronologically with hand crops at 12fps and full/face crops at 4fps, supplemented by full-resolution composition snapshots. Review is sampled visual inspection, not continuous real-time playback. Subjective scores are provisional and uncalibrated; exact key depression/cursor response, cross-shot identity, UI accuracy and lip sync remain untested.

The first desktop take over-articulated fingers. A brand-new still added a visible padded wrist rest; that improved nearer-hand support but did not prevent far-hand lifting. A third desktop prompt requested two key presses followed by reading, but repeated typing and downward glances persisted. The final bounded revision removed typing altogether and requested four seconds of attentive reading with hands resting on keys. Rejected takes and exact revision hypotheses remain in the production records.

The initial mouse click produced repeated high index-finger lifts. A new animation of the same new still, requesting mouse movement alone, retained the grip across six seconds; a brief downward head inclination remains. The six-second laptop take retained localized finger movement and supported arms, with a brief mouth opening and some regular cadence.

## Budget and delivery records

One conservative shared $10 ceiling covers the entire new batch. Four new source-image calls at $0.15 each, six six-second video calls at $1.20 each, and one four-second video call at $0.80 total **$8.60 estimated**. The **$9.92 reservation** includes the 15% buffer, rounded per request. All quality-rejected attempts remain counted. Actual charges are unconfirmed; estimates are not an invoice. The previous batch's separate cumulative ledger is unchanged.

Veo's settings-specific silent 1080p quote was $0.20/second, distinct from its generic audio-enabled API price: [official endpoint](https://fal.ai/models/fal-ai/veo3.1/image-to-video). The source quote was $0.15 per 2K image: [Nano Banana Pro endpoint](https://fal.ai/models/fal-ai/nano-banana-pro). Quote/schema snapshots and the persistent queue/budget ledger are in `artifacts/library-loop-computer-movement-studies-02/`.

Editable projects and exact prompts: `videos/computer-movement-studies-02/`. Delivery: `artifacts/final_outcome/computer-movement-studies-02/review.html`, with separate final videos, new source stills and original generated takes. Final metadata/hashes: `assembled_outputs/computer-movement-studies-02.json`. Attempt reviews: `review_notes/computer-movement-studies-02.json`. Generated media remains excluded from Git.

## Final verification

All three HyperFrames checks passed without findings. The silent 1920×1080 24fps exports decoded in full: 36, 144 and 144 frames. Source-to-final SSIM was 0.989950, 0.985309 and 0.986345 respectively. Encoded overview sheets and native final frames were inspected; no added camera treatment, speed changes or output corruption were seen. There are no scene joins, captions or audio to align. Technical success does not establish realism. Detailed checks and encoded visual findings are in `review_notes/computer-movement-studies-02-*`.
