# The Sunday Problem / a customer testimonial for ROTA

Fifth library loop - the interview use case, which had measured plates since loop one and no delivered film. It closes the open caution written down back then: speaker identity across a longer exchange.

Subjective 0-10 scores read from eight evenly sampled frames per output, plus a full-size frame for every selected plate. Every dialogue take was additionally transcribed with local Whisper and compared word by word against the written line. No human audience testing, no calibrated perceptual model, no repeat-seed trials. A transcript is not proof of lip-sync; lip-sync was judged visually from sampled frames.

Scores average four equally weighted criteria. Compare within use case only.
One trial per model per shot, no repeat seeds, no confidence intervals.

| Run | Role | v | Score / 10 | Dimensions | Estimate | Seconds | Used |
| --- | --- | ---: | ---: | --- | ---: | ---: | :-: |
| `talk_hero_v1` | interview | 1 | 9.25 | 1920x1080 | $1.20 | 141.5 | yes |
| `broll_room_v1` | environment | 1 | 7.75 | 1920x1080 | $0.60 | 118.19 | yes |
| `broll_dough_v1` | industrial_human | 1 | 8.5 | 1920x1080 | $0.68 | 175.42 | yes |
| `broll_rota_v1` | environment | 1 | 8.75 | 1920x1080 | $0.60 | 96.41 | yes |
| `broll_oven_v1` | environment | 1 | 9.0 | 1920x1080 | $0.60 | 135.51 | yes |
| `talk_b_v1` | interview | 1 | 8.75 | 1920x1080 | $1.20 | 190.67 | yes |
| `talk_c_v1` | interview | 1 | 9.0 | 1920x1080 | $0.90 | 144.67 | yes |
| `talk_d_v1` | interview | 1 | 5.25 | 1920x1080 | $1.20 | 162.14 | - |
| `talk_d_v2` | interview | 2 | 9.25 | 1920x1080 | $0.90 | 256.25 | yes |

## What Changed This Loop

The first film in the series where the voice is a generated performance rather than authored narration - the previous two used local TTS over silent footage, and this one is carried by the model's own speech. The first to use J-cuts, with dialogue audio spanning picture cuts. And the first to close on a light card; the four before it all ended on near-black, which had stopped being a choice and started being a habit.

## Controlled Comparisons

### Dialogue Identity Across An Exchange

Winner: **reference_conditioned_image_to_video_with_audio**

Loop one measured a good interview plate and wrote down an open caution - longer exchanges and speaker identity remain untested - which stayed open through three more films. Tested here it is settled: four separate takes, four different lines, one continuous person. Identity, wardrobe, set, lighting and even an unrequested lavalier mic carry across, and the speech is lip-synced rather than dubbed. Loop four proved reference conditioning holds a face in silence; this proves it holds a face that is talking.

## Routing After This Loop

| Shot type | Route to | Selected run | Caution |
| --- | --- | --- | --- |
| interview first line | Veo 3.1 Fast, audio on, 1080p | `talk_hero_v1` | With audio, 1080p bills the same as 720p - a free upgrade loop one did not know about. This plate also supplies the reference frame, so choose it for a mouth-closed, hands-at-rest moment, not just for the best read. |
| interview later lines | Veo 3.1 Fast image-to-video, audio on | `talk_d_v2` | Match the shot duration to the line. Over-buying time is how the one failure happened. |
| faceless hands | Kling 3.0 Pro | `broll_dough_v1` | Unchanged across four loops. |
| warm interior b roll | Veo 3.1 Fast, audio off | `broll_oven_v1` | Atmospheric detail like dust in a light beam is requested far more often than it is delivered. |
| deliberately illegible handwriting | Veo 3.1 Fast, audio off | `broll_rota_v1` | Ask for text-shaped marks that must not resolve into words, and deny readable letters in the negative prompt. Do not use this where the words must be read - that is still HyperFrames. |
| captions lower third brand mark close | HyperFrames | `-` | Unchanged across five loops. Here the captions are a transcript of generated speech, so they must be timed from the measured segments rather than from the written script. |

## Observations

### `talk_hero_v1` - 9.25/10  **selected**
The speaker arrived exactly as written on the first attempt and the line transcribed word-perfect, filling 6.82s of the 8s bought. The model added a lavalier mic clipped to her apron strap that nothing asked for - precisely the detail that sells a documentary interview. Selected, and the most valuable plate of the loop because it also supplies the reference frame for every later line.

### `broll_room_v1` - 7.75/10  **selected**
Warm backlit bakery interior with racks of cooling loaves. The flour dust hanging in a light beam, which was the point of the shot, never really reads, and a large dark counter makes the lower third heavy. Weakest plate of the loop; used briefly mid-film where it costs least. Selected.

### `broll_dough_v1` - 8.5/10  **selected**
Kling on faceless hands for the fourth loop running and still the most literal read in its category: flour-dusted hands turning and tucking a round of dough, no face, warm side light. Selected.

### `broll_rota_v1` - 8.75/10  **selected**
The story's problem object, and a small first: the prompt asked for a grid covered in pencil marks that are NOT readable words, and the model delivered exactly that - text-shaped scribble that never resolves into letters. Four loops of denying legible text, and this is the first time the ask was inverted and it worked first try. Reads a little more like parchment than paper. Selected.

### `broll_oven_v1` - 9.0/10  **selected**
Dark-crusted loaves on a wooden peel at a glowing stone oven mouth, steam lifting. The strongest b-roll image of the loop, and the right one to carry the warm resolve before the close. Selected.

### `talk_b_v1` - 8.75/10  **selected**
The probe that answered the loop's open question. Image-to-video from one frame, audio on: word-perfect transcript, and unmistakably the same woman in the same bakery in the same wardrobe, down to the mic on the apron strap. She picks up a pencil unprompted, matching the line she is speaking. Framing drifts slightly wider than the reference. Selected.

### `talk_c_v1` - 9.0/10  **selected**
Word-perfect, and the performance carries the beat the line needs - the tired, amused familiarity of someone who has listed these interruptions many times. Ten words in a 6s shot, speech ending at 5.16s. Selected.

### `talk_d_v1` - 5.25/10
The only genuine failure of the loop, and it landed on the most important line. Transcribed as 'Now it takes about nine minutes, now it takes about, I've got my thundays' - the model restarted the clause mid-line, dropped the word 'back' and slurred 'Sundays'. Speech ended at 4.58s of an 8s shot. Rejected.

### `talk_d_v2` - 9.25/10  **selected**
Repaired by buying LESS time, not more: 6s instead of 8s, plus an explicit instruction against repeating, plus a new seed. Both sentences delivered once, straight through, word-perfect - and with a natural 1.5 second beat between them that the edit uses as a breath. Selected.

## Findings

- **Image-to-video with audio holds a talking face.** Four takes, four lines, one continuous person, lip-synced. This closes the caution loop one wrote down and left open through three films, and it makes multi-shot interview films practical at $0.15/s.
- **The length trap inverts.** Loop one measured delivery running SHORT of the requested duration and concluded: buy about 1.3x the spoken length. That rule produced this loop's only failure - given three spare seconds on a five-second line, the model padded by restarting the clause. The corrected rule is to match the duration to the line: 6s for a ten-to-eleven word line, 8s for fourteen.
- **A font on disk is not a font that embeds.** BigCaslon.ttf was silently rejected by Chromium's OTS sanitizer - an invalid platform/encoding pairing on a format-12 cmap subtable - so the wordmark rendered in whatever serif the renderer defaulted to. Off-design, and different on another machine. Converting to WOFF2 with the cmap re-tagged fixed it. Check the Runtime stage for font-decode warnings; do not assume.
- **Asking for illegible text works.** Five loops have been spent denying generated text because it never spells correctly. This loop inverted the ask - text-shaped pencil scribble that must NOT resolve into words - and got it first try. The failure mode is also a capability when the design wants the look of writing rather than the content of it.
- **J-cuts are what make an interview read as edited.** The dialogue audio runs continuously across the picture cuts inside a line, so the b-roll lands under her voice rather than interrupting it. It costs nothing - it is purely how the audio elements are placed against the video elements - and it is the single largest difference between this film and a set of clips laid end to end.

## Budget

Estimated generation total: $7.88. Conservative reserved total: $9.08. Hard cap: $10.00.
9 paid requests, all completed, no failures and no automatic retries.
This loop has its own ledger at `artifacts/library-loop-5/budget.json`; it is the persistent cost record and deleting it defeats the cap guard. Provider invoice not queried.

## Final Film

`/Users/joydimapilis/conductor/workspaces/video-generation-test/amarillo/artifacts/final_outcome/rota/rota-final.mp4`
Zero lint, runtime, layout and motion findings; 17/17 contrast checks pass.
No generation API cost for the assembly. Authoring time is the real cost of the
HyperFrames layer and is not comparable to a model call.

