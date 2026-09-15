---
format: 1920x1080
duration: 31s
message: "Turn scattered campaign notes into one clear creative brief."
arc: Before → transformation → product → quick glimpse → complete the transformation
audience: creative teams and marketers
mode: autonomous
music: none
captions: skipped (short on-screen product copy carries the message; avoid duplicate caption rails)
---

## Video direction
Bright coral/cream/ink from frame.md, condensed bold poster typography. Three frames, each containing multiple developing scenes. A note avalanche becomes one surface; the surface hosts a brief-making glimpse; the resulting brief folds out into an ordered campaign board. Shared exact geometry across seams. No generated people or cinematic filler. Original local percussion score is added after narration generation; music:none suppresses provider lookup only. User authorizes all production and final render. Inline serial frame-worker fallback, no delegated agents.

## Frame 1 — The idea is everywhere
- scene: Campaign notes invade a cream field, snap into order, and become Fold.
- duration: 9s
- poster: 5.5s
- transition_in: cut
- status: animated
- type: hook
- blueprint: compose
- asset_candidates: fold-mark.svg
- src: compositions/frames/01-everywhere.html
- voiceover: "The idea is good. It's just everywhere. In a message. In a note. In your head. Fold turns it into a creative brief."
- sfx: none

Scene 1 (0–1.3s): Giant central condensed "GOOD IDEA." A single cream note at x120 y590 w520 h180 says "Refillable bottle." Coral right region 40% width. Signature movement: `waterfall-entry`.
Scene 2 (1.3–3.5s): The headline changes to "EVERYWHERE." Six note surfaces rush into a deliberately scattered arrangement around the headline. Main notes "Refillable bottle.", "For everyday commuters.", "Make it feel less preachy." Remain readable for a beat. Compose `depth-scatter-assemble`, preserving flat paper style and no shadows; controlled rotation, perspective only during movement, then flat.
Scene 3 (3.5–6.5s): Notes rotate flat and gather as one stack to the right; left half reveals large FOLD and "AI CREATIVE BRIEFS". "From scattered to started." One accent plane travels with the gathering motion; no simple full-frame fade.
Scene 4 (6.5–9s): The stack enlarges into a cream product surface with black header. `card-morph-anchor` plus fixed header, mask-reveal. Finish on shared blank Fold surface, so the next frame's UI grows from it.
handoff_out: paper surface x=180 y=210 width=1560 height=720 scale=1 opacity=1 rotation=0; cream #F5F0E8; black #1A1A1A header height=78; header text FOLD left x=220 y=227 font Bebas Neue 48; speed=0 direction=none; coral #E85D5D full background.

## Frame 2 — Give it a direction
- scene: Three notes become an organized brief; one tone control refines the central message.
- duration: 12s
- poster: 6s
- transition_in: cut
- status: animated
- type: feature_showcase
- blueprint: compose
- asset_candidates: fold-mark.svg
- src: compositions/frames/02-direction.html
- voiceover: "Drop in your notes. Fold finds the audience, the message, and what to make. Want a different feel? Change the tone. The brief changes with it."
- sfx: none

handoff_in: exact same blank paper surface/header as Frame 1; same geometry, scale, opacity, rotation, colors, speed=0 direction=none.
Scene 1 (0–2.4s): Keep shared window x180 y210 w1560 h720. Original notes enter left column; an ORGANIZE action at x440 y800 w280 h70. Cursor lands and presses at 1.7s. Exact-note content from opening.
Scene 2 (2.4–6.5s): Audience, core message, deliverables arrive sequentially in right panel. Audience "Everyday commuters"; message "Refill. Reuse. Keep moving."; deliverables "Launch page · Social posts · Email". Header reads FOLD / FIELD CAMPAIGN. `waterfall-entry` and `cursor-click-ripple`. Flat held UI after each arrival, not a full tutorial.
Scene 3 (6.5–9.8s): Cursor touches tone choice HUMAN at x1280 y800 w250 h70 (default FORMAL). Click 7.4s. Core message changes from "Refill. Reuse. Keep moving." to "Your everyday refill." The UI must visibly respond to the control, `control-target-sync`.
Scene 4 (9.8–12s): Cursor exits. Side panels withdraw. Hero brief shrinks to a centered cream sheet x560 y190 w800 h700 on coral. Black top band height78, title FIELD / CREATIVE BRIEF. One short line "Your everyday refill." remains. Deterministic `card-morph-anchor`; exact handoff to final frame.
handoff_out: brief sheet x=560 y=190 width=800 height=700 scale=1 rotation=0 opacity=1; cream #F5F0E8; black header height=78; title FIELD / CREATIVE BRIEF at x600 y215 Inter 24 white; body line Your everyday refill. at x600 y350 Bebas Neue 62 uppercase; speed=0 direction=none; coral background.

## Frame 3 — A place to start
- scene: The finished brief opens into an ordered board made from the original notes; a bold closing statement completes the hook.
- duration: 10s
- poster: 7.8s
- transition_in: cut
- status: animated
- type: cta
- blueprint: compose
- asset_candidates: fold-mark.svg
- src: compositions/frames/03-started.html
- voiceover: "Now those scattered thoughts have a direction. One brief your team can build from. Fold. Shape your next idea."
- sfx: none

handoff_in: exact same centered cream brief sheet/header/body as Frame 2. Identical geometry and colors; speed=0 direction=none.
Scene 1 (0–3.5s): The sheet opens horizontally into three ordered panels, `center-outward-expansion`, like an unfolded paper board. AUDIENCE / MESSAGE / MAKE. Same opening facts now in purpose-labeled columns. The original bottle idea remains as text in the message panel; the result is explicitly a creative brief.
Scene 2 (3.5–6.4s): Panels compress to an ordered row in lower half. Oversized "LESS SCATTERED." then "MORE STARTED." arrives in the upper half in two passes, `waterfall-entry`. This returns to the hook's exact visual objects in an organized state.
Scene 3 (6.4–10s): CTA "SHAPE YOUR NEXT IDEA ↗" becomes an ink strip with Fold wordmark at left. The three organized note panels remain visible, so the ending holds a finished result as well as a brand. Hold final layout for at least 2 seconds; no black tail, no reset, no stock logo/tagline screen. Tiny footer "FICTIONAL PRODUCT CONCEPT".
