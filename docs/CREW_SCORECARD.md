# The Sunday Problem, revised / a customer testimonial for Crew

A revision loop rather than a new film. Four lines re-bought for their words, one for an offensive gesture, and four more clips spent on a controlled test of whether a shot contract and a real exit frame make generated people and generated cuts better. $8.48 of the $10 cap, no new production.

Every re-generated line was transcribed with local Whisper and compared word by word against the written script before being cut in. Shot durations were set arithmetically from 0.48 seconds per word - the rate measured across the four verified takes of the previous loop - rather than estimated. Identity across old and new takes was checked on stacked contact sheets. The realism and continuity runs hold model, seed, reference, duration, resolution and audio settings fixed and vary exactly one factor each; cut seams are measured as mean absolute pixel change at the boundary against the median change between adjacent frames on either side, on the full frame and on a head crop. That diagnostic locates seams and cannot measure naturalness - a frozen face scores low too - so every join was also watched in motion. No human audience testing.

Scores average four equally weighted criteria. Compare within use case only.
One trial per condition. Seeds are repeated deliberately inside the controlled pairs and never across models. No confidence intervals.

| Run | Role | v | Score / 10 | Dimensions | Estimate | Seconds | Used |
| --- | --- | ---: | ---: | --- | ---: | ---: | :-: |
| `line2_schedule_v1` | interview | 1 | 9.0 | 1920x1080 | $1.20 | 193.67 | yes |
| `line4_product_v1` | interview | 1 | 9.0 | 1920x1080 | $0.90 | 147.35 | - |
| `line5_how_v1` | interview | 1 | 9.0 | 1920x1080 | $0.90 | 149.28 | - |
| `line6_result_v1` | interview | 1 | 9.0 | 1920x1080 | $1.20 | 170.04 | yes |
| `line3_pain_v2` | interview | 2 | 9.0 | 1920x1080 | $0.90 | 128.04 | yes |
| `realism_line4_v2` | interview | 2 | 8.25 | 1920x1080 | $0.90 | 101.61 | yes |
| `realism_dough_v2` | industrial_human | 2 | 8.25 | 1920x1080 | $0.68 | 118.93 | yes |
| `realism_line5_chained` | interview | 2 | 8.5 | 1920x1080 | $0.90 | 143.52 | yes |
| `realism_line5_control` | interview | 2 | 8.0 | 1920x1080 | $0.90 | 112.8 | - |

## What Changed This Loop

The arc is explicit where it was previously implied: problem, what she uses, how it helps, result. Two authored product screens carry the mechanic, the product is named on screen and in speech, and 'nine minutes' finally has a stated subject.

The second half of the loop rebuilt how shots are asked for. A shot now declares the state it enters on and the state it exits on across ten fields, and a join marked continuous is rejected if any of them differ. Dialogue prompts direct observable behaviour - refocusing eyes, irregular blinking, breath in the shoulders, hands resting low - instead of naming emotions, and the negative list now names the AI-face signature directly. Most importantly, continuity stopped being asserted in prose and started being conditioned: the reviewed exit frame of one clip is uploaded as the input image of the next. Full write-up in docs/CREW_REALISM_REPORT.md.

## Controlled Comparisons

### The Length Rule Corrected

Winner: **duration_matched_to_line**

The previous loop's only failure came from over-buying time: given three spare seconds on a five-second line, the model padded by restarting the clause. Loop one's rule - buy about 1.3x the spoken length - caused it. Sizing every line here to land between 0.7 and 1.8 seconds of spare room produced four clean takes out of four, with no repair round at all. The correction is now a number, not a hunch.

### Shot Contract Versus Prose Prompt

Winner: **shot_contract**

Compiling the prompt from a ten-field shot contract - identity stated as preservation, behaviour described instead of emotion named, hands given a resting state, secondary motion tied to a cause, and the AI-face signature listed in the negatives - produced a face with more skin structure and a less posed expression than the baseline prompt at the same seed. It is one take judged by one reviewer, not an audience preference. It also reframed tighter than the anchor it was given, which is a continuity cost the contract was supposed to prevent: 'the original headroom and lens perspective' is a phrase, and the model treated it as one.

### Exit Frame Versus Shared Anchor

Winner: **previous_exit_frame**

This is the loop's real result, and the control is what makes it one. Three joins, measured as boundary pixel change over the median adjacent-frame change: the two original takes cut together at 6.76x on the full frame and 5.27x on the head; the same improved prompt from the shared anchor got worse, 11.00x and 7.35x; the improved prompt started from the outgoing clip's reviewed exit frame closed to 2.38x and 1.19x. In the head region the cut becomes about as disruptive as one ordinary frame of her own movement. Prompt wording alone did not close the seam and would have widened it - only the image did. The cost is one substituted word and the input frame's compression artifacts carried into the new take.

## Routing After This Loop

| Shot type | Route to | Selected run | Caution |
| --- | --- | --- | --- |
| changed dialogue lines | Veo 3.1 Fast image-to-video, audio on | `line6_result_v1` | Generate from the SAME reference frame the original takes used, or the revision will not intercut with the footage it is meant to join - unless the shot is deliberately joined to its predecessor's exit frame instead, in which case everything it cuts against must move with it. |
| unchanged dialogue lines | reuse | `-` | The cheapest shot is the one already bought. Two of six lines needed no new words, so they were not re-bought. |
| product mechanic on screen | HyperFrames | `-` | Six loops of evidence that no generative model spells reliably. These screens carry names, days and a filled grid, so they could not be generated at any price. |
| recurring person any shot | Veo 3.1 Fast image-to-video, compiled shot contract, audio on | `realism_line4_v2` | Route refuses to compile without a reviewed identity reference. Expect the model to reframe: ask for framing in the contract, then check the take against the plates it must sit beside, because a phrase about headroom is not a lens. |
| a cut that must feel continuous | Veo 3.1 Fast image-to-video, conditioned on the previous clip exit frame | `realism_line5_chained` | Choose the frame by eye, not by taking the last encoded one - pick a settled pose after speech ends and reject open-mouth tails - and cut the outgoing clip at exactly the timestamp the frame came from. The frame is a decoded video frame, so its artifacts propagate; budget a little prompt adherence for it. |
| hands and physical contact | Kling 3 Pro text-to-video, single preparation-contact-release chain | `realism_dough_v2` | Name the forces and the body parts carrying them. Negative instructions about repetition are unreliable - this take started a second cycle anyway - so buy enough length to trim, and grade the result to the surrounding footage. |

## Observations

### `line2_schedule_v1` - 9.0/10  **selected**
The problem line, rewritten to say 'staff schedule' in plain words instead of the trade jargon 'rota'. Word-perfect, no repeats, speech 1.40-7.18s of an 8s shot. The 1.4s lead-in before she starts is trimmed with media-start rather than wasted. Selected.

### `line4_product_v1` - 9.0/10
The line that names the product, and the one most at risk of sounding like an advert. Asking for matter-of-fact delivery - 'the way someone describes their ordinary working week rather than recommending something' - produced exactly that. Word-perfect, speech 0.00-4.80s of 6s. Carried the first cut of the film; superseded in the revision by `realism_line4_v2`, which is the same line at the same seed with the compiled shot contract instead of this prose prompt.

### `line5_how_v1` - 9.0/10
The mechanic line. Word-perfect and delivered faster than estimated - 3.68s against a predicted 5.3s - which left more room than intended but caused no padding. Carried the first cut; superseded in the revision by `realism_line5_chained`, which is the same line generated from the previous shot's exit frame rather than the shared anchor.

### `line6_result_v1` - 9.0/10  **selected**
The payoff, rewritten so 'nine minutes' finally has a stated subject: the whole schedule. Both sentences once, straight through, word-perfect, with a 1.8s beat between them that the edit keeps. This is the line the previous loop had to re-buy after the model stuttered; the corrected length rule produced it right first time. Selected.

### `line3_pain_v2` - 9.0/10  **selected**
The complaint line, re-bought because the original take answered an unprompted instruction with an offensive hand gesture. Word-perfect, speech 0.00-5.34s of 6s, and the hands stay out of it. A reminder that a clean transcript is not a clean take: nothing in the speech gate would have caught the gesture, and only watching it did. Selected.

### `realism_line4_v2` - 8.25/10  **selected**
The same line as `line4_product_v1`, same model, same seed 92, same anchor frame - only the prompt changed, to the compiled shot contract with its identity-preservation, micro-behaviour and anti-retouching direction. Word-perfect, speech 0.00-5.06s of 6s. The face reads older and more textured than the baseline take: a deeper nasolabial fold, visible skin structure under the side light, and a mid-thought expression instead of a held pleasant one. That is the direction asked for and it is less obviously generated. It also came at a cost the prompt did not intend - the model reframed tighter than the anchor, so this take no longer matches the wide framing of the seven reused plates. Selected, but every shot next to it is a cutaway.

### `realism_dough_v2` - 8.25/10  **selected**
The hands insert, re-prompted from a repeated kneading instruction into one causal chain - palms settle, weight leans forward, dough compresses, fingers stay curved as the palms release, dough partly rebounds - with the forces named and floating contact ruled out. The clearest realism win of the loop: tendons, veins, knuckle creases and short nails are all present, and the dough visibly takes the weight instead of deforming on its own. Two reservations. The take ignores 'no second kneading cycle' and starts another press at about 4.5s, so the edit uses only 2.5-4.5s. And it is lighter and cooler than the warm bakery grade around it - better anatomy in slightly the wrong colour, ungraded. Selected.

### `realism_line5_chained` - 8.5/10  **selected**
The continuity test. Identical to `realism_line5_control` in model, seed 93, prompt, duration and resolution; the only difference is that its input image is the reviewed 5.125s exit frame of `realism_line4_v2` rather than the shared anchor. It inherits the outgoing shot's tighter framing, and the head region at the cut moves 1.19x a normal frame of motion against the original pair's 5.27x. It is the only join in the film that is genuinely continuous. Two costs, both real: it substituted one word - 'everyone sees an update' for 'everyone sees it update', so the caption was changed to match what she actually says - and conditioning on a decoded video frame carried that frame's encoding artifacts forward, leaving it visibly crunchier around the hair and background than the control. Selected.

### `realism_line5_control` - 8.0/10
The control, and the run that makes the result mean anything. Same improved prompt, same seed, same outgoing shot as the chained take; only the input reference differs. Word-perfect where the chained take was not. But cut against `realism_line4_v2` it reverts to the wide anchor framing, and the seam measures 7.35x in the head region - worse than the 5.27x of the two original takes it was meant to improve on. Better wording made the cut worse. Not used in the film; bought to be discarded, and worth the $0.90.

## Findings

- **Revise by delta, not by remake.** Only four of ten plates changed words, so only four were re-bought. $4.20 against the $7.88 the original cut cost. Because every new line was generated from the same reference frame as the originals, the reused and regenerated takes intercut invisibly.
- **The corrected length rule held.** Sizing each shot from the measured 0.48s-per-word rate produced four usable takes with no repair round, against the previous loop's one-in-four failure. Loop one's 1.3x guidance is now formally superseded.
- **Authored screens are how a testimonial explains a product.** The spoken lines say what she uses and roughly how; the two screens show the actual mechanic - availability in, schedule out, everyone notified. That work is free, deterministic and spells correctly, and it is the only part of the film that could not have been generated.
- **An authored screen must survive being checked.** The first build of the schedule grid put Aisha on Thursday and Tomas on Friday, contradicting the availability screen shown seconds earlier. Nothing in the render pipeline can catch that - it is internally consistent HTML - and it was caught only by reading the two screens against each other. Invented data still has to be true to itself.
- **Jargon is a clarity bug.** The product was called ROTA, which is British trade jargon for a staff schedule. Renaming it Crew and saying 'staff schedule' in the script cost nothing and removed the single biggest comprehension barrier in the film.
- **Continuity is conditioned, not described.** The same improved prompt from the shared anchor made the cut worse than the baseline; the same prompt from the outgoing clip's exit frame dropped the head-region seam from 5.27x to 1.19x a normal frame of motion. The control cost $0.90 and is the only reason that sentence can be said at all. Prompt text asking two shots to match is a hope; handing the second shot the first one's last frame is a mechanism.
- **Choose the handoff frame by eye.** Nine candidates were pulled between 4.80s and 5.90s and the last encoded frame was not the right one. 5.125s was taken because the lips had just closed after speech and the eyes were open; the 5.4-5.9s open-mouth tail would have started the next shot mid-vowel. The tooling now refuses to build unless a human approved a single named frame and recorded why.
- **Better prompts can make an edit worse.** The shot contract improved the face and the hands, and simultaneously reframed the interview tighter than the seven plates it has to live beside. A realism gain measured on one shot is not a gain on the film. Judge a prompt change at the cut, not in the clip.
- **Negative instructions are not constraints.** 'No second kneading cycle' was ignored; the take starts another press at 4.5s. It cost nothing because the shot was bought long enough to trim. Buy the length that lets the edit fix what the prompt cannot.
- **A clean transcript is not a clean take.** The line re-bought as `line3_pain_v2` was word-perfect the first time and still unusable, because the model volunteered an offensive hand gesture. Every automatic gate in this system reads pixels or words. Somebody still has to watch it.

## Budget

Estimated generation total: $8.48. Conservative reserved total: $9.79. Hard cap: $10.00.
9 paid requests, all completed, no failures and no automatic retries.
This loop has its own ledger at `artifacts/library-loop-6/budget.json`; it is the persistent cost record and deleting it defeats the cap guard. Provider invoice not queried.

## Final Film

`/Users/joydimapilis/conductor/workspaces/video-generation-test/amarillo/artifacts/final_outcome/crew-improved/crew-improved-final.mp4`
Zero lint, runtime, layout and motion findings; 41/41 contrast checks pass.
No generation API cost for the assembly. Authoring time is the real cost of the
HyperFrames layer and is not comparable to a model call.

