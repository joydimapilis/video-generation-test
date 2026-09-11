# ORRIN Scorecard: Second Library Loop

Concept: **ORRIN / Built to see in the dark** - a dark industrial precision-hardware launch film, chosen because it is the inverse of the first loop's Cue ad on every axis that matters: no dialogue, no interface, dark instead of light.

Subjective 0-10 scores read from eight evenly sampled frames per output plus one full-size frame for the shots that were selected. No human audience testing, no calibrated perceptual model, no repeat-seed trials. Temporal stability is sampled, not exhaustive. There is no dialogue in this loop, so no transcripts were taken.

Scores average four equally weighted criteria. Compare within use case only.
One trial per model per shot, no repeat seeds, no confidence intervals.

| Run | Role | v | Score / 10 | Dimensions | Estimate | Seconds | Used |
| --- | --- | ---: | ---: | --- | ---: | ---: | :-: |
| `weave_kling_v1` | material_macro | 1 | 7.75 | 1920x1080 | $0.45 | 239.73 | yes |
| `hero_kling_v1` | product_hero | 1 | 6.75 | 1920x1080 | $0.68 | 273.23 | - |
| `hero_veo_v1` | product_hero | 1 | 8.75 | 1920x1080 | $0.60 | 106.97 | yes |
| `hands_kling_v1` | industrial_human | 1 | 6.25 | 1920x1080 | $0.56 | 185.31 | - |
| `ridge_veo_v1` | environment | 1 | 9.25 | 1920x1080 | $0.60 | 109.45 | yes |
| `ridge_ltx_v1` | environment | 1 | 7.25 | 1920x1080 | $0.48 | 83.71 | - |
| `array_kling_v1` | product_hero | 1 | 8.0 | 1920x1080 | $0.56 | 180.05 | yes |
| `hero_kling_v2` | product_hero | 2 | 8.5 | 1920x1080 | $0.68 | 166.99 | yes |
| `hands_kling_v2` | industrial_human | 2 | 8.25 | 1920x1080 | $0.56 | 184.68 | yes |

## What Changed This Loop

Two pairs ran on byte-identical prompts, which is the only comparison in either loop where the input was genuinely controlled: Veo against Kling on the same product-hero prompt, and Veo against LTX on the same landscape prompt.

## Controlled Comparisons

### Product Hero

Winner: **split**

Kling produced the more beautiful object and Veo the more literal one. Veo also delivered 1080p at $0.10/s with audio disabled, against Kling's $0.112/s, so on this shot Veo was cheaper and more obedient while Kling was prettier. Both were used.

### Environment

Winner: **veo_3_1_fast**

Veo won clearly on light, contrast and depth for $0.12 more. LTX remains the cheapest way to see whether a landscape idea works at all.

## Routing After This Loop

| Shot type | Route to | Selected run | Caution |
| --- | --- | --- | --- |
| material macro | Kling 3.0 Pro | `-` | Expect less camera movement than requested; budget an authored push. |
| product hero beauty | Kling 3.0 Pro | `hero_kling_v2` | Fills frame; leaves little negative space for type. |
| product hero with type | Veo 3.1 Fast, audio off | `hero_veo_v1` | Pulls back further than asked, which is why the space exists. |
| industrial hands | Kling 3.0 Pro | `hands_kling_v2` | Faceless hands are far more reliable than faces, but gloves still soften. |
| landscape environment | Veo 3.1 Fast, audio off | `ridge_veo_v1` | - |
| repeated unit array | Kling 3.0 Pro | `array_kling_v1` | Worked here on one trial; do not generalize to arrays that must be countable. |
| annotation and type | HyperFrames | `-` | Unchanged from the first loop: no generated glyph is trustworthy. |

## Observations

### `weave_kling_v1` - 7.75/10  **selected**
Correct material, correct black, correct hard raking light, and rock steady. But the camera barely moves across four seconds despite an explicit continuous drift instruction, and a bright band along the sheet's near edge draws the eye. Used, with an authored push supplying the movement the model did not.

### `hero_kling_v1` - 6.75/10
The best object geometry in the whole loop - a genuinely flat hexagonal slab with a convincing multi-element coated lens - attached to the wrong product. Warm bronze instead of black, an unrequested port on the side wall, and a lamp reflection in the background. Rejected on identity, not on craft.

### `hero_veo_v1` - 8.75/10  **selected**
Black, bead-blasted, exactly one lens and one amber ring, no ports - the closest read of the written spec in the loop. Pulls back further than the requested three-quarter framing and the body is chunkier than a puck, but it ends with half the frame clean. Selected as the reveal, and the negative space is what made the wordmark placement possible.

### `hands_kling_v1` - 6.25/10
The gesture was right on the first attempt: hands lower the module, seat it, and withdraw out of frame. The module is polished silver steel, which cannot be intercut with a black one. Gloves soften slightly mid-shot. Rejected on finish alone.

### `ridge_veo_v1` - 9.25/10  **selected**
Every requested element present: dusk ridge, deep blue sky over an orange horizon, the instrument on a low tripod with its ring lit, wind in dry grass, and a steady push past it into the valley. The strongest single frame produced across both loops. Selected.

### `ridge_ltx_v1` - 7.25/10
Contains everything the prompt asked for and holds together, but the light is flat and the sky muddy next to the Veo take from the identical prompt. The instrument reads as a flat octagonal disc rather than a housing. Competent and cheap; not the shot.

### `array_kling_v1` - 8.0/10  **selected**
The result that contradicted the hypothesis. Repeated identical units were written into the plan as a likely failure, and Kling returned a deep receding grid of matching modules with matching rings. Spacing wanders in places and the model letterboxed the frame, which an authored crop removes. Selected.

### `hero_kling_v2` - 8.5/10  **selected**
The colour repair landed: matte black, no side port, no background lamp, and v1's geometry and lens survive intact. Four screw heads appeared on the top face that the prompt denied, and a metal bracket is still visible top right. Selected as the macro beauty shot; the object fills the frame, so annotations sit on its own body.

### `hands_kling_v2` - 8.25/10  **selected**
Same gesture, now in matte black. The last second leaves the object alone on the bench, which is a clean out-point into the next scene. The lens glows greenish-white rather than showing a distinct amber ring, and the gloves still soften. Selected.

## Findings

- **Veo without audio is cheap.** `generate_audio: false` drops Veo 3.1 Fast to $0.10/s and unlocks 1080p at the same rate, making it cheaper than Kling 3.0 Pro ($0.112/s) for any silent shot. The first loop only ever measured Veo with audio on at 720p, so it looked like the expensive option. It is not.
- **Faces were the problem, not people.** Every human shot in loop one was a talking head. Gloved hands with no face and no speech scored 8.25 and needed one repair, against four attempts to get one usable talking head.
- **A written hypothesis was wrong, and that is the useful part.** Repeated identical units were planned as a likely failure; the array came back usable on the first try.
- **Colour is a repairable defect; geometry is not.** Both repairs in this loop were finish corrections and both landed on one retry. Naming the wrong outcome explicitly - "absolutely not silver, not chrome, not bronze" - is what fixed them.
- **Two models beat one.** Kling produced the better object and Veo the better negative space from the same prompt, so the film uses both as two angles rather than picking a winner.

## Budget

Estimated generation total: $5.17. Conservative reserved total: $5.99. Hard cap: $10.00.
9 paid requests, all completed, no failures and no automatic retries.
This loop has its own ledger at `artifacts/library-loop-2/budget.json`; it is the persistent cost record and deleting it defeats the cap guard. Provider invoice not queried.

## Final Film

`/Users/joydimapilis/conductor/workspaces/video-generation-test/amarillo/artifacts/final_outcome/orrin/orrin-final.mp4`
Zero lint, runtime, layout and motion findings; 22/22 contrast checks pass.
No generation API cost for the assembly. Authoring time is the real cost of the
HyperFrames layer and is not comparable to a model call.

