# Crumb: three newly generated bakery-preorder samples

12 new generations, three fresh edits, one shared $10 ledger. No earlier generated video enters these edits.

Agent subjective visual review of eight chronological frames per take, selected full-resolution stills, actual decoded product joint measurements, local Whisper base.en transcripts and full video decode. No independent audio listening, exhaustive motion review, lip-sync measurement or audience test. Hand dynamics, subtle eye movement and voice identity remain unmeasured. Scores are screening judgments, not calibrated quality metrics.

Scores average four equally weighted criteria. Compare within use case only.
One take per condition. Same prompts across models, different sampled identities, resolution and seed semantics. Revisions hold endpoint seed and speech fixed but change prompt and scene/identity. Paired product tests share exact references. Compare within use case only.

| Run | Role | v | Score / 10 | Dimensions | Estimate | Seconds | Used |
| --- | --- | ---: | ---: | --- | ---: | ---: | :-: |
| `crumb_ugc_h3_v1` | ugc | 1 | 7.88 | 1344x768 | $0.36 | 370.08 | - |
| `crumb_ugc_veo_v1` | ugc | 1 | 8.38 | 1920x1080 | $0.90 | 116.3 | yes |
| `crumb_interview_h3_v1` | interview | 1 | 5.0 | 1344x768 | $0.36 | 388.03 | - |
| `crumb_interview_veo_v1` | interview | 1 | 7.0 | 1920x1080 | $0.90 | 134.26 | - |
| `crumb_pastry_kling_v1` | product_ad | 1 | 8.88 | 1920x1080 | $0.56 | 170.68 | yes |
| `crumb_ugc_h3max_v1` | ugc | 1 | 8.0 | 1344x768 | $0.12 | 23.5 | - |
| `crumb_interview_h3max_v1` | interview | 1 | 6.5 | 1344x768 | $0.12 | 19.62 | - |
| `crumb_interview_h3max_v2` | interview | 2 | 8.38 | 1344x768 | $0.12 | 83.02 | yes |
| `crumb_interview_veo_v2` | interview | 2 | 8.12 | 1920x1080 | $0.90 | 138.31 | - |
| `crumb_continuation_h3max` | product_continuation | 2 | 8.5 | 1344x768 | $0.10 | 98.34 | - |
| `crumb_continuation_kling` | product_continuation | 2 | 9.12 | 1920x1080 | $0.56 | 208.66 | yes |
| `crumb_baker_return_h3max` | interview | 3 | 8.5 | 1344x768 | $0.10 | 28.91 | yes |

## Detailed criteria

N/T means not tested, not zero. These are subjective sampled-frame scores; a single-shot identity score does not establish consistency across shots.

| Criterion | crumb_ugc_h3_v1 | crumb_ugc_veo_v1 | crumb_interview_h3_v1 | crumb_interview_veo_v1 | crumb_pastry_kling_v1 | crumb_ugc_h3max_v1 | crumb_interview_h3max_v1 | crumb_interview_h3max_v2 | crumb_interview_veo_v2 | crumb_continuation_h3max | crumb_continuation_kling | crumb_baker_return_h3max |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| human realism | 7.5 | 8.5 | 6.5 | 6.5 | N/T | 7.5 | 6 | 8 | 8.5 | N/T | N/T | 8 |
| face realism | 7.5 | 8.5 | 6.5 | 6.5 | N/T | 7.5 | 6 | 8 | 8.5 | N/T | N/T | 8 |
| hand body movement | N/T | N/T | N/T | N/T | N/T | N/T | N/T | N/T | N/T | N/T | N/T | N/T |
| identity consistency | 8 | 8 | 8 | 8 | N/T | 8 | 8 | 8 | 8 | N/T | N/T | 8.5 |
| product accuracy | N/T | N/T | N/T | N/T | 9 | N/T | N/T | N/T | N/T | 9 | 9 | N/T |
| text ui accuracy | N/T | N/T | N/T | N/T | N/T | N/T | N/T | N/T | N/T | N/T | N/T | N/T |
| camera movement | 8.5 | 8.5 | 8.5 | 8.5 | 8.5 | 8.5 | 8.5 | 8.5 | 8.5 | 8.5 | 8.5 | 8.5 |
| cinematic quality | N/T | N/T | N/T | N/T | 8.5 | N/T | N/T | N/T | N/T | 8.5 | 8.5 | N/T |
| transition quality | N/T | N/T | N/T | N/T | N/T | N/T | N/T | N/T | N/T | 8 | 9.5 | N/T |
| entry exit continuity | N/T | N/T | N/T | N/T | N/T | N/T | N/T | N/T | N/T | 8 | 9.5 | N/T |
| context clarity | 9 | 9 | 9 | 9 | N/T | 9 | 9 | 9 | 9 | N/T | N/T | 9 |
| product message clarity | N/T | N/T | N/T | N/T | N/T | N/T | N/T | N/T | N/T | N/T | N/T | N/T |
| prompt adherence | 8 | 8 | 3 | 6.5 | 8.5 | 8 | 6 | 8 | 7.5 | 8.5 | 9 | 8.5 |
| consistency | 8 | 8.5 | 7.5 | 8 | 9 | 8 | 7.5 | 8.5 | 8.5 | 9 | 9 | 8.5 |

## What Changed This Loop

New fictional Crumb concept and original scripts; current H3 Max screening; simpler human performance prompt revision; actual pastry exit-frame continuation comparison; new identity-conditioned baker return; three exact authored UI films.

## Routing After This Loop

| Shot type | Route to | Selected run | Caution |
| --- | --- | --- | --- |
| ugc | Veo 3.1 Fast T2V | `crumb_ugc_veo_v1` | Selected for this shot; long spoken pause remains. |
| interview | H3 Max simplified T2V + fresh-reference I2V return | `crumb_interview_h3max_v2 + crumb_baker_return_h3max` | Visual continuity sampled; voice identity and lip sync not measured. |
| product | Kling 3.0 Pro | `crumb_pastry_kling_v1` | Simple stationary food and one camera direction. |
| product continuation | Kling 3.0 Pro paired endpoints | `crumb_continuation_kling` | Near-static test only. |
| exact ui | HyperFrames 0.8.35 | `-` | Authored illustrative UI, not a recording of a deployed Crumb service. |

## Observations

### `crumb_ugc_h3_v1` - 7.88/10
Correct two-sentence script, stable kitchen/bag and resting hands in samples. Broad eyebrow and head-angle changes; 1.44s transcript gap slows pacing. Face is comparatively smooth. New T2V identity; no cross-shot test.

### `crumb_ugc_veo_v1` - 8.38/10  **selected**
Selected for stronger visible facial texture and credible domestic lighting in samples. Correct script; forearms mostly rest. Bag glance becomes a larger head turn and starts before final words; 1.8s transcript gap remains. Do not equate selected take with perfect micro-expression or lip-sync accuracy.

### `crumb_interview_h3_v1` - 5.0/10
Local transcript contains extra instruction-like speech after the intended line: delivery is steady and unmodulated. Sampled performance is expressive. Reject rather than cut around a prompt-leak failure without listening. The returned expanded prompt is retained in the ledger.

### `crumb_interview_veo_v1` - 7.0/10
Correct intended line transcribes; skin lines look exaggerated, eyebrow and mouth expressions conspicuous. Unrequested partial interviewer visible on frame right. New revision removes texture list and changes to broad low-contrast daylight.

### `crumb_pastry_kling_v1` - 8.88/10  **selected**
Fresh coherent croissant, parchment and plate. Push-in is stronger than the requested few centimeters, but remains one camera direction with stable food. Reviewed 4.5s exit supplies both continuation conditions. Natural food texture; not a real product fidelity benchmark.

### `crumb_ugc_h3max_v1` - 8.0/10
Correct script; coherent overlapping forearms and visible fingers in sampled frames. Comfortable close phone framing; roughly 1.42s gap between clauses. Face still quite smooth and bright-eyed. No clear realism improvement over Veo established.

### `crumb_interview_h3max_v1` - 6.5/10
Correct intended words but exaggerated cheek texture and repeated closed-eye expressions conflict with restrained interview direction. No hands visible, so hand motion untested. Prompt mentions pores/lines; revised condition removes that emphasis.

### `crumb_interview_h3max_v2` - 8.38/10  **selected**
Revised prompt yields a much more ordinary face than its first condition, preserved apron and stable bench/window in samples. Speech completes at 5.84s, lips settle by reviewed 6.2s. Eyebrow activity and smooth skin remain. Selected as an affordable calm interview candidate and source of the new return reference; this is a new identity, not proof of causal improvement.

### `crumb_interview_veo_v2` - 8.12/10
More ordinary skin and a coherent bakery after simplified prompt; intended line completes at 5.16s. An unrequested rising hand appears late, despite hands-below-frame direction. Strong alternative for face detail, but retained as comparison rather than chosen for this settled pose.

### `crumb_continuation_h3max` - 8.5/10
Stable pastry and tile layout in samples. Actual previous-frame to entry RGB MAE 4.59/255, with a slight crop/appearance change. Cheap alternative, but Kling gives the closer boundary in this run. Static hold only; not moving-object continuity.

### `crumb_continuation_kling` - 9.12/10  **selected**
Selected new continuation. Shared first/last references preserve pastry geometry, plate, parchment, light and framing. Actual boundary MAE 1.34/255; first-to-middle 1.43/255. Same prompt as H3 Max, but resolution and model internals differ. No claim that all transitions improve this much.

### `crumb_baker_return_h3max` - 8.5/10  **selected**
New short closing line transcribes correctly (0.90–2.02s). Sampled face, hairstyle, apron, counter and window remain recognizable against the fresh 6.2s reference. Lips settle into a slight smile. Selected first 3s after the UI cutaway. Voice identity and lip sync remain unmeasured.

## Findings

- Texture adjectives can be overinterpreted: removing them improved ordinary appearance in both revised baker takes in this small screen.
- Base H3 interview leaked instruction-like speech into the local transcript; retain rejection and do not repeat unchanged.
- H3 Max costs less in the current launch promotion; both price and faster return are separate from realism.
- A shared exit frame gave Kling a closer product boundary than H3 Max here.
- Exact text, numeric list totals and preorder states are authored and checked in HyperFrames.
- Faces remain untreated; sampled similarity is not proof that viewers cannot detect generated people.

## Budget

Estimated generation total: $5.10. Conservative reserved total: $5.92. Hard cap: $10.00.
12 reserved requests; 12 completed; 0 failed or uncertain. No automatic retries.
This loop has its own ledger at `artifacts/library-loop-9/budget.json`; it is the persistent cost record and deleting it defeats the cap guard. Provider invoice not queried.

