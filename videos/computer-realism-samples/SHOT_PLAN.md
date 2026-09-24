# Three computer-use studies

Fresh batch, not another paid round of the prior Kite film. All three samples and revisions share one $10 ledger, stricter than the per-video ceiling. Six seconds each, silent, native speed, static camera, no finishing effects. Faces are fictional; separate stills are similar in demographic and wardrobe but cross-shot identity is not a requirement.

## Evidence and model decision

Read human-realism README and review, Kite purposeful-contact rejection/partial result, Serein/Portion lessons, Crew realism and Round8/topic research. Reviewed chronological 8fps detail sheets for real clips 02 (0–2s), 04 (0–2s) and 05 (7–9s), plus fresh library extraction through inspect_library_slice.py. These are sampled sequences, not continuous playback. The currently discoverable library resolves to the human-realism collection; no broader general library was available through its normal discovery.

Current learned `hands` route reports no compatible reviewed route. Kling 3 Pro is a bounded candidate based on the legacy hands route and reviewed adjacent contact tasks, not a learned winner for typing. Latest Seedance2 purposeful-trackpad test is only partially successful: hand lift and very still performance. Veo interview evidence does not establish superior keyboard interaction. Use a common Kling model/settings across this batch to limit additional variation. Actual endpoint schema saved in research, including start_image_url, duration string, cfg_scale and audio switch. API pricing $0.14/sec is conservatively used over the public $0.112 silent rate; $0.84 estimated, $0.97 reserved per six-second take. Flux2 Pro image: 1536x864, conservatively two MP at $0.03 = $0.06 estimated/$0.07 reserved. Initial total $2.70 estimated/$3.12 reserved, leaving correction headroom.

The default built-in image tool has no verifiable USD-per-call bound exposed here. Standing user instructions permit choosing a costed provider instead; source stills use Fal Flux2 Pro and share the ledger without being video routing evidence.

## 01 — Typing, medium three-quarter

Observed: clip 02 0–2s has alternating unequal finger flexion with quiet wrists; 04 0–2s shows restrained task attention, small unequal head/hand motion.
Hypothesis: existing home-row contact plus a short uneven typing burst and pause should avoid both synchronized hand bobbing and a frozen posed hold. Medium view includes face and hands. Review for finger identity, contact, eye target and independent motion.

## 02 — Trackpad, closer side three-quarter

Observed: clip 05 7–9s assigns distinct roles to hands, with one reposition and the other remaining at the keyboard. This is trackpad-area evidence, not precise mouse-click evidence. Clip 04 0–2s supports quiet attention.
Hypothesis: establish two fingertips on the trackpad in the still, ask for one short glide then a reading pause, keep palm heel supported. Do not ask for a hand transfer from keyboard, the prior failure point. Check glide stays on the pad rather than inventing a raised gesture. No external mouse is tested.

## 03 — Wider typing → reading pause

Observed: clip 03 early desk work and clip 04 0–4s exhibit task-related attention changes; 05 shows restrained forward posture and unequal hand activity.
Hypothesis: short typing followed by fingers resting and a slight eye/head refocus toward the screen will look purposeful without a theatrical pose change. Keep seated throughout, hands supported; only a small settling of upper body after typing.

## Experiment limits

References supply observed behavioral cues translated into prompts; no real reference video or identity is uploaded to the model. Source pose, framing and action vary between samples. No matched no-reference control and no fixed video seed (not exposed) mean this tests feasibility/consistency, not causality or a model ranking. UI correctness, speech/lip-sync, external mouse mechanics and cross-shot identity remain untested. Chronological face and hand reviews, not API success, decide selection.

## Round 2 revision
Both Kling samples rejected: 01 has large hooked finger lifts/hovering, 03 curls both hands away and withdraws arms, both widen framing. New route Seedance 2.0 with five-second actions, 720p and audio off. Source 01 unchanged; source 02 Nano Banana Pro establishes a real two-finger trackpad pose, with the left hand active and right resting (matching actual still over prompt hand labels); source 03 regenerated with lit screen. Reference cues and budget unchanged. Model, prompt, and one source image change, so no isolated model superiority claim. See reviewed rejected takes in the shared scorecard.

## Round 3 provider eligibility failure
All three Seedance jobs failed with 422 partner_validation_failed, rejecting possible likenesses. No image alteration or safety-setting change to overcome this gate. All three estimated charges remain reserved because usage API is forbidden (403). Move to the existing supported Veo3.1 Fast adult-person route, default safety and auto_fix false, 1080p four seconds silent at $0.10/s ($0.40 estimate/$0.46 reserve each). Overall reservations $9.21 including all failed jobs; no ledger reset. Same reviewed sources and simple motion cues.

## Final-resolution review and editorial selection
Veo typing is provisionally usable. Trackpad glide still crosses onto keyboard: final bounded retry is one stationary tap with identical still. Veo reading-pause hand curl is too pronounced in full-resolution snapshot; reject full take and use only 0–1.5s as side-view typing. This changes the third output duration and action label, preserving quality rather than claiming the intended pause succeeded. No slowdown or frozen hold extends it. Final reservations including last retry: $9.67.

Final selection: 01 typing 4s; 02 trackpad contact/tap 1.25s; 03 side typing 1.5s. Full takes 02 and 03 rejected for later curled-hand poses and retained untrimmed in comparison delivery. No matched controls and no direct reference-video conditioning: consistent reference benefit remains unproven.
