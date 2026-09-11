# Seventeen / a founder origin story for TUESDAY

Fourth library loop - the first film in the series with a character, and the first to use reference-conditioned image-to-video to hold that character across shots.

Subjective 0-10 scores read from eight evenly sampled frames per output, plus a full-size frame for every plate that was selected. No human audience testing, no calibrated perceptual model, no repeat-seed trials. Temporal stability is sampled, not exhaustive. No plate contains dialogue; the narration is a separate local TTS track.

Scores average four equally weighted criteria. Compare within use case only.
One trial per model per shot, no repeat seeds, no confidence intervals.

| Run | Role | v | Score / 10 | Dimensions | Estimate | Seconds | Used |
| --- | --- | ---: | ---: | --- | ---: | ---: | :-: |
| `hero_night_v1` | character | 1 | 9.0 | 1920x1080 | $0.60 | 110.34 | yes |
| `hands_laptop_v1` | industrial_human | 1 | 8.0 | 1920x1080 | $0.68 | 153.88 | yes |
| `window_rain_v1` | environment | 1 | 8.75 | 1920x1080 | $0.60 | 113.69 | yes |
| `desk_empty_v1` | environment | 1 | 8.0 | 1920x1080 | $0.60 | 146.49 | yes |
| `coffee_dawn_v1` | environment | 1 | 9.0 | 1920x1080 | $0.60 | 101.51 | yes |
| `street_walk_v1` | environment | 1 | 5.5 | 1920x1080 | $0.60 | 159.33 | - |
| `city_dawn_v1` | environment | 1 | 7.75 | 1920x1080 | $0.60 | 141.28 | yes |
| `char_lookup_v1` | character | 1 | 8.75 | 1920x1080 | $0.60 | 110.23 | yes |
| `char_react_v1` | character | 1 | 8.5 | 1920x1080 | $0.60 | 111.15 | yes |
| `char_exhale_v1` | character | 1 | 8.75 | 1920x1080 | $0.60 | 128.07 | yes |

## What Changed This Loop

The first film in the series with a person in it, and the first where the authored screens carry the plot rather than the branding - the dashboards showing 0, then 1, then 12 ARE the three acts. Cuts are hard throughout, deliberately ceding the crossfade language to KEEL, and the rhythm is a dark frame against a bright screen, which is also what the story is about.

## Controlled Comparisons

### Character Consistency

Winner: **reference_conditioned_image_to_video**

The second loop recorded that text-to-video cannot hold identity between shots and left reference conditioning untested. Tested here, it is decisive: all three image-to-video beats are unmistakably the same person, in the same room, wearing the same clothes, lit by the same lamp - not approximately, exactly. And at $0.10/s silent at 1080p it costs the same as text-to-video, so for any recurring subject there is no reason to prefer plain text-to-video.

## Routing After This Loop

| Shot type | Route to | Selected run | Caution |
| --- | --- | --- | --- |
| character first appearance | Veo 3.1 Fast, audio off | `hero_night_v1` | This plate is also the reference frame for every later character shot, so choose it for framing as much as for beauty. A strict profile limits what the later performances can show. |
| character later beats | Veo 3.1 Fast image-to-video | `char_react_v1` | Identity is guaranteed, the scene is not negotiable. Image-to-video continues the frame it is handed, so write the film as a chamber piece or buy a new hero frame per location. |
| faceless hands | Kling 3.0 Pro | `hands_laptop_v1` | Asking for near-black gets near-black. Budget it as punctuation, not as a shot. |
| weather still life city | Veo 3.1 Fast, audio off | `coffee_dawn_v1` | Check every returned plate for baked-in letterbox before designing the frame around it. |
| legible number label or ui | HyperFrames | `-` | Unchanged across four loops. Here the authored screens carry the plot rather than the branding, which is the best use found for the capability so far. |
| narration | Kokoro local, bf_emma at 0.94 | `-` | Free and offline. Time the edit from measured durations, never estimates. |

## Observations

### `hero_night_v1` - 9.0/10  **selected**
The character arrived exactly as written on the first attempt - skin, closely cropped hair, the single silver stud, the olive sweatshirt, screen light in a dark room. Two misses: she sits in strict profile rather than the requested three-quarter, and faint document-like content is visible on the laptop screen the prompt denied. Selected, and the most valuable plate of the loop because it also supplies the reference frame that three more shots are generated from.

### `hands_laptop_v1` - 8.0/10  **selected**
Kling on faceless hands again, and again the most literal read in its category: the lid comes down, the screen light narrows to a line and goes out, keys blank, no face. Extremely dark by the end - which is what was asked for, but it leaves very little to look at, so it earns only a 1.6s punctuation. Selected.

### `window_rain_v1` - 8.75/10  **selected**
Rain tracking down glass with the city thrown into soft bokeh behind it. Warmer and more golden than the cold blue-grey specified, which the surrounding night footage absorbs happily. The prettiest b-roll plate of the loop. Selected.

### `desk_empty_v1` - 8.0/10  **selected**
Empty desk, closed laptop, mug, cold morning light, slow push. Correct but plain: the dust turning in the light shaft never really reads, so the shot carries mood rather than an image. Selected for 1.8s.

### `coffee_dawn_v1` - 9.0/10  **selected**
A mug, the edge of a keyboard, one last thread of steam in cold light, drifting sideways. Everything asked for and nothing else in frame. Selected.

### `street_walk_v1` - 5.5/10
A lone figure walking into golden light down an empty street - lovely on its own terms, and useless here. The figure reads as a man in dark clothing rather than a woman in an olive sweatshirt, and the plate carries 131px of letterbox. Dropped rather than repaired: the film did not need an outdoor character beat, and dropping is cheaper than fixing.

### `city_dawn_v1` - 7.75/10  **selected**
Skyline at first light with mist still in the streets, drifting up. Undercut by 140px of baked-in letterbox nothing asked for, removed with a 1.36x crop - the heaviest crop used across four loops, and it costs visible sharpness. Selected.

### `char_lookup_v1` - 8.75/10  **selected**
Image-to-video from the hero frame. Hands come to rest, she sits back, her eyes leave the screen. Identical person, room, lamp and wardrobe by construction. The performance is very restrained - arguably a shade too restrained to read inside a 2.8s cut. Selected.

### `char_react_v1` - 8.5/10  **selected**
The payoff. The smile is exactly the right size - small, disbelieving, not a celebration - which was the hardest thing to ask for. She does not stop and lean in to re-read as written; she keeps typing through it. The smile is the beat and the beat lands, so the deviation costs nothing. Selected.

### `char_exhale_v1` - 8.75/10  **selected**
She sits back, her shoulders drop, a settled smile stays. The brief eye-close does not really read at this framing. Reads as relief rather than triumph, which is the tone the whole film depends on. Selected.

## Findings

- **Reference-conditioned image-to-video is the answer to character consistency.** Three shots generated from one frame produced the same person exactly, where two earlier loops of prompt engineering could not hold a simple object's colour. It costs the same as text-to-video, so for any recurring subject it should be the default.
- **Its constraint is scenic, not visual.** Image-to-video continues the scene it is given, so it cannot move the character to a new place or time of day. That is a screenplay constraint, and the honest response is to write for it - this film became a chamber piece on purpose.
- **A hero plate that doubles as a reference frame has two jobs.** This one is beautiful and is a strict profile, which quietly capped how much the three later performances could show. Next time, specify the reference framing as a requirement of the first shot.
- **Baked-in letterbox appeared for the third loop running.** city_dawn needed a 1.36x crop, the heaviest yet. It is now detected programmatically, but it should be assumed rather than discovered.
- **Three delivery gates in two loops have now failed on measurement artifacts rather than real defects.** KEEL's peak gate measured a mono downmix and inflated a clean 0.767 to 1.083. This loop's loudness gate used a fixed 1.4s window that straddled the end of a 1.2s line and reported 1.88x where the true speech-span ratio is 2.48x. Then its transcript gate failed on 'sixteen', 'seventeenth' and 'eleven' because Whisper writes numbers as digits and the script spells them out. Every one of the three was the instrument, not the film. The lesson is specific: a gate must derive its measurement from the same source that drives the thing it measures, and must compare in a normalised space rather than a raw one.

## Budget

Estimated generation total: $6.08. Conservative reserved total: $7.00. Hard cap: $10.00.
10 paid requests, all completed, no failures and no automatic retries.
This loop has its own ledger at `artifacts/library-loop-4/budget.json`; it is the persistent cost record and deleting it defeats the cap guard. Provider invoice not queried.

## Final Film

`/Users/joydimapilis/conductor/workspaces/video-generation-test/amarillo/artifacts/final_outcome/seventeen/seventeen-final.mp4`
Zero lint, runtime, layout and motion findings; 36/36 contrast checks pass.
No generation API cost for the assembly. Authoring time is the real cost of the
HyperFrames layer and is not comparable to a model call.

