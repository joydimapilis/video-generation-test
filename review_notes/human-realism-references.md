# Human realism references — initial review

Workflow scope: this movement library and its clip-comparison procedure are
reserved for separate Phase 2 human-realism evaluation and improvement, not default
video generation. The observations below are retained as historical evidence.
Normal production continues to use source image → internal image review →
image-to-video → motion review for people scenes independently of this library.

## Decision for Kite Tomorrow

**Closest overall match: `references/human-realism/human-reference-04.mp4`,
approximately 0–4 seconds.** It combines seated solo work, a visible face,
medium three-quarter framing, forward attention toward a nearby screen, and
soft side lighting. This best addresses Kite's quiet opening without requiring
a different story or a large gesture. The comparison is a subjective judgment
about suitability, not a numerical realism score.

In the first approximately 0–2.8 seconds, her attention largely stays on the
tablet while the stylus hand makes small changes and the head/torso adjust less.
Around 2.9–3.6 seconds, gaze/head lower toward the page and the hand lowers;
around 3.6–4 seconds attention returns toward the tablet. The motions have
different amplitudes and timing. The expression stays task-focused, without a
presentational smile. Later, approximately 4–8 seconds show writing, 8–10 seconds
a hair adjustment, and 12–19 seconds page handling and brief looks to the screen.
Those later actions are additional reference evidence, not an action list to
squeeze into Kite's 3.6-second opening. Times are approximate sampled observations.

04 is not an exact setup match: it uses a tablet, stylus and book, faces screen
right rather than left, and has a cooler, simpler lighting/background treatment.
Borrow the coordination and restraint, not the person, props, framing coordinates,
action sequence or complete composition. Keep Kite's established identity,
screen-left gaze target, warm room and shot length.

## Comparison with the current generated shot

The existing Seedance take remains the selected, delivered shot; this review
does not alter that selection or regenerate anything. Its laptop-directed gaze
and supported arms are useful improvements over the earlier version, but its
hands remain grouped/resting with little task-specific behavior. The motion
therefore still reads as a posed reading hold. Reference 04 shows how a mostly
quiet torso can coexist with small independent, purposeful hand and gaze changes.
Naturalness does not require constant motion, a scheduled smile or an exactly
prescribed blink. The earlier finding of softer generated facial detail also
remains unresolved; these references do not establish a model or texture fix.

For a future test, the strongest untested hypothesis is to revise the source
pose first so one hand can plausibly rest on the laptop's trackpad/palm-rest
area while the other has stable support, then animate one small task and a pause.
Do not ask the current folded-hand still to invent complicated typing or a new
prop interaction. Preserve the four-second generation / 3.6-second editorial
window and assess behavior at normal speed. This is a hypothesis only; no model
call, prompt submission, upload or new cost was made in this review.

## Roles of all five clips

| Clip | Useful observations | Role for Kite |
| --- | --- | --- |
| 01, 20.56 s | Approximately 0–5 s: seated laptop work. Around 5–8 s: stops, shifts weight, reaches toward folder, rises; then walks away as camera follows. Broad office light, wider elevated view. Shirt/hair respond to larger body movement. | Secondary reference for whole-body mechanics; stand/walk action and busy framing do not fit this opening. |
| 02, 5.08 s | Close view of laptop typing with independent finger bends/lifts and relatively steady wrists. Hands do not rise and fall together; contact is localized to keys. Warm directional light and a small framing move. | Best close-up supplement for finger articulation if typing is needed. Face and gaze untested. |
| 03, 25.36 s | Repeated gaze between monitor and keyboard, typing/pauses, and approximately 3–6 s reach/grasp/return of a small container. Upright seated posture, restrained face, bright broad light. Glasses obscure some eye detail. | Useful alternative for gaze/hand coordination and object contact, but desktop setup/clinical scene are less close overall. |
| 04, 19.65 s | Quiet seated concentration, small unequal head/hand movement, task-motivated looks, writing/page contact; face and arms visible in a medium three-quarter view. Soft side lighting. | Primary overall motion/performance/framing reference, especially 0–4 s. |
| 05, 36.20 s | Laptop work with different roles for each hand, typing and trackpad-area motion, pauses, slight forward-posture adjustments. Around 7–9 s the farther hand lifts/repositions while the nearer remains around the keyboard. Darker directional side light. | Best contextual supplement for laptop contact and timing. Mask and rear/side view make lower-face expression unsuitable for assessment. |

No isolated external mouse grip/click sequence is clearly established by the
inspected views. Keep that dimension unverified rather than inventing mouse
evidence. Use a more specific reference if a future shot requires external-mouse
mechanics. Likewise, do not use clip 02 or masked clip 05 as facial-expression
benchmarks.

## How to use the set during Phase 2

Select a reference by the actual action and view, then record its useful time
range and observable cues in the shot plan. Establish posture, gaze target,
hand support and object contact in the source still. Evaluate the generated
motion chronologically for stable contact, plausible weight, independent hand
activity, task-related gaze and pauses, expression, and clothing/hair response.
Compare framing and light separately from motion. Mark obscured or untested
dimensions as unverified. Do not copy the subjects or reproduce the clips.

## Evidence and limits

All five files were decoded successfully and inspected through the repository's
`src/amarillo/library.py` / `scripts/inspect_library_slice.py` workflow with a
command-scoped `AMARILLO_LIBRARY_DIR=references/human-realism`. This did not replace
the general video library. Review covered 12 overview samples per clip and 213
chronological frames at 2 fps across the full set, plus 8-fps detail sequences
for 04 (0–4 s), 02 (0–2 s) and 05 (7–9 s). The current Kite source's existing
chronological full-frame sheet was also re-inspected.

This is sampled visual review, not uninterrupted real-time playback, eye tracking,
or a frame-accurate measurement of blink or keystroke durations. Audio was not
evaluated because this review concerns visible human behavior. The user identifies
the clips as real human references; source/capture provenance beyond that is not
independently established.

Evidence: `artifacts/human-realism-reference-review/overview/manifest.json`,
`dense-manifest.json`, each clip's `sheet-*.jpg`, and `detail-*/sheet-*.jpg`.
Source SHA-256 values are preserved in `references/human-realism/catalog.json`.
No generation or final-video edit took place; new provider spend is $0.
