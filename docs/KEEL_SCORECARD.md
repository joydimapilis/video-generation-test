# KEEL / Built below the waterline

Third library loop - a narrated brand manifesto, the first film in the series carried by voice and rhythm rather than by a product.

Subjective 0-10 scores read from eight evenly sampled frames per output, plus a full-size frame for every plate that was selected. No human audience testing, no calibrated perceptual model, no repeat-seed trials. Temporal stability is sampled, not exhaustive. No plate contains dialogue, so no transcripts were taken; the narration is a separate local TTS track.

Scores average four equally weighted criteria. Compare within use case only.
One trial per model per shot, no repeat seeds, no confidence intervals.

| Run | Role | v | Score / 10 | Dimensions | Estimate | Seconds | Used |
| --- | --- | ---: | ---: | --- | ---: | ---: | :-: |
| `rush_street_v1` | environment | 1 | 7.75 | 1920x1080 | $0.60 | 125.83 | yes |
| `rush_transit_v1` | environment | 1 | 8.5 | 1920x1080 | $0.60 | 127.93 | yes |
| `rush_servers_v1` | environment | 1 | 9.0 | 1920x1080 | $0.60 | 120.79 | yes |
| `rush_hands_v1` | industrial_human | 1 | 5.25 | 1920x1080 | $0.68 | 201.47 | - |
| `water_surface_v1` | environment | 1 | 8.75 | 1920x1080 | $0.60 | 99.91 | yes |
| `water_descend_v1` | environment | 1 | 9.25 | 1920x1080 | $0.60 | 154.95 | yes |
| `water_deep_v1` | environment | 1 | 8.5 | 1920x1080 | $0.60 | 94.49 | yes |
| `shop_wide_v1` | environment | 1 | 8.25 | 1920x1080 | $0.60 | 150.57 | yes |
| `shop_hands_v1` | industrial_human | 1 | 8.75 | 1920x1080 | $0.68 | 127.19 | yes |
| `shop_keel_v1` | environment | 1 | 8.75 | 1920x1080 | $0.60 | 130.0 | yes |
| `rush_hands_v2` | industrial_human | 2 | 8.25 | 1920x1080 | $0.68 | 113.07 | yes |

## What Changed This Loop

Pacing and transitions were the stated targets. Act one accelerates from 1.60s cuts to 0.45s across eight cuts, act two slows to roughly 4.1s, act three holds; the previous two films each ran one flat 4-6s cadence end to end. Three transition languages replace the hard-cut-only approach: whip-slide entries with a two-frame flash, a full dip through black at the turn, and opposing-opacity crossfades in the two slow acts.

## Controlled Comparisons

### Over Coverage

Winner: **over-coverage**

60 seconds of footage were bought for a 38-second film. That converted editing from 'use what arrived' into 'drop what is weak', and rush_hands_v1 was dropped outright rather than defended. The first two loops bought close to exactly what they needed and had to use every frame. At Veo's silent rate this cost about $1.80 more than a minimal buy.

## Routing After This Loop

| Shot type | Route to | Selected run | Caution |
| --- | --- | --- | --- |
| cold urban environment | Veo 3.1 Fast, audio off | `rush_servers_v1` | Street scenes with plausible real-world signage resist text suppression; interiors comply. |
| crowd with motion | Veo 3.1 Fast, audio off | `rush_transit_v1` | Asking for indistinct faces did not produce them. Cut short or frame past the crowd. |
| water and depth | Veo 3.1 Fast, audio off | `water_descend_v1` | Very low-key water needs narration or motion over it; four seconds of near-black will not hold alone. |
| warm interior craft | Veo 3.1 Fast, audio off | `shop_wide_v1` | Check for baked-in letterbox before designing the frame around the plate. |
| hands with a tool | Kling 3.0 Pro | `shop_hands_v1` | Specify the camera move, not just the action, if the shot has to match-cut with another. |
| narration | Kokoro-82M local | `bm_george at 0.92` | Free and offline, but no direction over emphasis or pause; write lines short enough that the read cannot go wrong. |
| captions type transitions | HyperFrames | `-` | Unchanged across three loops: no generated glyph is trustworthy. |

## Observations

### `rush_street_v1` - 7.75/10  **selected**
Wet asphalt, depth and vehicle light streaks all present, and the lateral pan is there. Readable background shop signage appeared despite being denied three ways in the negative prompt, and the red signs push warmth into a shot specified as cold. Used, cut short, in two pieces.

### `rush_transit_v1` - 8.5/10  **selected**
A convincing crowded concourse under cold fluorescent light with the requested lateral track and real motion blur on the figures. Faces are more distinct than the brief asked for and one or two commuters glance toward the lens. Used in two pieces.

### `rush_servers_v1` - 9.0/10  **selected**
The most literal read of any prompt in the loop: narrow aisle, hundreds of cyan status lights, fast forward dolly, nothing else in frame. Used in two pieces and the strongest act-one plate.

### `rush_hands_v1` - 5.25/10
A laptop lid carrying a readable browser window sits across the top of frame, despite the prompt stating no screen content and no monitor. The room reads flat grey instead of unlit-with-cyan, and the head-on framing cannot match-cut against the act-three plane shot. Rejected.

### `water_surface_v1` - 8.75/10  **selected**
Grey-green chop under a flat overcast horizon with a slow forward drift and nothing else in frame - no boats, no land, no birds. Deliberately the least interesting image in the film, which is its job at the turn. Selected.

### `water_descend_v1` - 9.25/10  **selected**
Light shafts cutting down through teal into deep blue with suspended particles drifting through the beams. The best single frame produced in this loop and the shot the whole middle act rests on. Selected.

### `water_deep_v1` - 8.5/10  **selected**
Near-black with one faint shaft far above and slow particle drift, exactly as specified. So empty that it barely sustains four seconds on its own; it works because the narration is carrying that stretch. Selected.

### `shop_wide_v1` - 8.25/10  **selected**
Bare hull ribs against a doorway full of low golden light with sawdust hanging in the beams - the shot that makes the metaphor land. Undercut by 92 pixels of baked-in letterbox top and bottom that nothing in the prompt asked for, removed with a 1.21 scale crop that costs some sharpness. Selected.

### `shop_hands_v1` - 8.75/10  **selected**
A hand plane riding a curved timber with a single continuous curl of shaving peeling off the blade, warm side light, lateral track. One hand is visible rather than the two requested. Selected, and it carries the film's only match cut.

### `shop_keel_v1` - 8.75/10  **selected**
A long warm curve against near-black with one work lamp, tracking along its length. Reads as a finished hull rather than the bare keel timber on trestles that was specified, which is a better image than the one asked for. Selected as the final plate.

### `rush_hands_v2` - 8.25/10  **selected**
Screen gone, keys blank, background near-black, and the camera now tracks laterally so it pairs with shop_hands_v1 across the film's turn. The key light reads neutral rather than the specified cyan, which the surrounding cold plates absorb. Selected.

## Findings

- **Over-coverage is the cheapest quality lever found so far.** Veo at $0.10/s silent made it affordable to buy 60 seconds for a 38-second film. Being able to delete a bad plate instead of defending it improved the result more than any prompt change in three loops.
- **Negative prompts suppress text unevenly.** The same denial that produced blank keyboard keys and an unmarked workshop failed to stop shop signage in a night-street plate. Where the model expects text in the world, it puts text in the world.
- **Baked-in letterbox is a recurring unrequested behaviour.** ORRIN's array plate and KEEL's boat shed both arrived with bars nothing asked for. It is now detected programmatically from a single column of pixels rather than by eye.
- **Naming the wrong outcome worked a third time.** Denying the screen by every name it could take - screen, monitor, display, laptop lid, browser, window - removed it in one retry, as the colour denials did in the second loop.
- **Craft is free; footage is not.** The three transition languages, the accelerating cut rate, the music duck and the match cut cost nothing and did more for the film than the last two plates bought.

## Budget

Estimated generation total: $6.84. Conservative reserved total: $7.89. Hard cap: $10.00.
11 paid requests, all completed, no failures and no automatic retries.
This loop has its own ledger at `artifacts/library-loop-3/budget.json`; it is the persistent cost record and deleting it defeats the cap guard. Provider invoice not queried.

## Final Film

`/Users/joydimapilis/conductor/workspaces/video-generation-test/amarillo/artifacts/final_outcome/keel/keel-final.mp4`
Zero lint, runtime, layout and motion findings; 12/12 contrast checks pass.
No generation API cost for the assembly. Authoring time is the real cost of the
HyperFrames layer and is not comparable to a model call.

