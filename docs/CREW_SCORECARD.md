# The Sunday Problem, revised / a customer testimonial for Crew

A revision loop rather than a new film: four lines re-bought, six plates reused, and the product's value made explicit. $4.20 instead of a whole new production.

Every re-generated line was transcribed with local Whisper and compared word by word against the written script before being cut in. Shot durations were set arithmetically from 0.48 seconds per word - the rate measured across the four verified takes of the previous loop - rather than estimated. Identity across old and new takes was checked on stacked contact sheets. No human audience testing.

Scores average four equally weighted criteria. Compare within use case only.
One trial per model per shot, no repeat seeds, no confidence intervals.

| Run | Role | v | Score / 10 | Dimensions | Estimate | Seconds | Used |
| --- | --- | ---: | ---: | --- | ---: | ---: | :-: |
| `line2_schedule_v1` | interview | 1 | 9.0 | 1920x1080 | $1.20 | 193.67 | yes |
| `line4_product_v1` | interview | 1 | 9.0 | 1920x1080 | $0.90 | 147.35 | yes |
| `line5_how_v1` | interview | 1 | 9.0 | 1920x1080 | $0.90 | 149.28 | yes |
| `line6_result_v1` | interview | 1 | 9.0 | 1920x1080 | $1.20 | 170.04 | yes |

## What Changed This Loop

The arc is now explicit where it was previously implied: problem, what she uses, how it helps, result. Two authored product screens carry the mechanic, the product is named on screen and in speech, and 'nine minutes' finally has a stated subject. The testimonial register is unchanged - no superlatives, no statistics beyond her own estimate, and the two product lines are mechanical rather than enthusiastic.

## Controlled Comparisons

### The Length Rule Corrected

Winner: **duration_matched_to_line**

The previous loop's only failure came from over-buying time: given three spare seconds on a five-second line, the model padded by restarting the clause. Loop one's rule - buy about 1.3x the spoken length - caused it. Sizing every line here to land between 0.7 and 1.8 seconds of spare room produced four clean takes out of four, with no repair round at all. The correction is now a number, not a hunch.

## Routing After This Loop

| Shot type | Route to | Selected run | Caution |
| --- | --- | --- | --- |
| changed dialogue lines | Veo 3.1 Fast image-to-video, audio on | `line6_result_v1` | Generate from the SAME reference frame the original takes used, or the revision will not intercut with the footage it is meant to join. |
| unchanged dialogue lines | reuse | `-` | The cheapest shot is the one already bought. Two of six lines needed no new words, so they were not re-bought. |
| product mechanic on screen | HyperFrames | `-` | Six loops of evidence that no generative model spells reliably. These screens carry names, days and a filled grid, so they could not be generated at any price. |

## Observations

### `line2_schedule_v1` - 9.0/10  **selected**
The problem line, rewritten to say 'staff schedule' in plain words instead of the trade jargon 'rota'. Word-perfect, no repeats, speech 1.40-7.18s of an 8s shot. The 1.4s lead-in before she starts is trimmed with media-start rather than wasted. Selected.

### `line4_product_v1` - 9.0/10  **selected**
The line that names the product, and the one most at risk of sounding like an advert. Asking for matter-of-fact delivery - 'the way someone describes their ordinary working week rather than recommending something' - produced exactly that. Word-perfect, speech 0.00-4.80s of 6s. Selected.

### `line5_how_v1` - 9.0/10  **selected**
The mechanic line. Word-perfect and delivered faster than estimated - 3.68s against a predicted 5.3s - which left more room than intended but caused no padding. Selected.

### `line6_result_v1` - 9.0/10  **selected**
The payoff, rewritten so 'nine minutes' finally has a stated subject: the whole schedule. Both sentences once, straight through, word-perfect, with a 1.8s beat between them that the edit keeps. This is the line the previous loop had to re-buy after the model stuttered; the corrected length rule produced it right first time. Selected.

## Findings

- **Revise by delta, not by remake.** Only four of ten plates changed words, so only four were re-bought. $4.20 against the $7.88 the original cut cost. Because every new line was generated from the same reference frame as the originals, the reused and regenerated takes intercut invisibly.
- **The corrected length rule held.** Sizing each shot from the measured 0.48s-per-word rate produced four usable takes with no repair round, against the previous loop's one-in-four failure. Loop one's 1.3x guidance is now formally superseded.
- **Authored screens are how a testimonial explains a product.** The spoken lines say what she uses and roughly how; the two screens show the actual mechanic - availability in, schedule out, everyone notified. That work is free, deterministic and spells correctly, and it is the only part of the film that could not have been generated.
- **An authored screen must survive being checked.** The first build of the schedule grid put Aisha on Thursday and Tomas on Friday, contradicting the availability screen shown seconds earlier. Nothing in the render pipeline can catch that - it is internally consistent HTML - and it was caught only by reading the two screens against each other. Invented data still has to be true to itself.
- **Jargon is a clarity bug.** The product was called ROTA, which is British trade jargon for a staff schedule. Renaming it Crew and saying 'staff schedule' in the script cost nothing and removed the single biggest comprehension barrier in the film.

## Budget

Estimated generation total: $4.20. Conservative reserved total: $4.84. Hard cap: $10.00.
4 paid requests, all completed, no failures and no automatic retries.
This loop has its own ledger at `artifacts/library-loop-6/budget.json`; it is the persistent cost record and deleting it defeats the cap guard. Provider invoice not queried.

## Final Film

`/Users/joydimapilis/conductor/workspaces/video-generation-test/amarillo/artifacts/final_outcome/crew/crew-final.mp4`
Zero lint, runtime, layout and motion findings; 41/41 contrast checks pass.
No generation API cost for the assembly. Authoring time is the real cost of the
HyperFrames layer and is not comparable to a model call.

