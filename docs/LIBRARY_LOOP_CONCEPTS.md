# Concept Slate: New Video Ideas and Per-Scene Routing

Concepts written after the measured loop. Prompts instantiate tested templates and apply the repairs learned in round 2. No scene here has been generated; every cost is an estimate from published per-second pricing, not an invoice.

Every concept below is derived from the inspected library references and routed
scene by scene to whichever tool measurably handled that role best in the loop.
Scene prompts instantiate the templates in `prompt_library/library_loop_patterns.json`
and already carry the round-2 repairs: explicit feature counts for product shots,
raw-camera wording to suppress burned-in subtitles, and a speech budget longer than
the line actually needs.

Remaining headroom under the $10 cap is **$0.34**. No concept in this
slate fits that, so none has been generated. Running one requires a new,
explicitly approved budget.

## Routing Rules

| Shot type | Route to | Fallback | Evidence | Caution |
| --- | --- | --- | --- | --- |
| Human speaks one short line to camera | `veo_3_1_fast` | `grok_imagine_1_5` | ugc_veo_v2 scored 8.75/10, the highest measured run; ugc_grok_v1 8.0 at $0.85; ugc_ltx_v1 7.38 at $0.48. | Measured delivery ran short of the requested length in every trial. Budget roughly 1.3x the spoken duration and re-check the transcript. |
| Two people alternating short questions and answers | `veo_3_1_fast` | `ltx_2_3_pro` | interview_veo_v1 8.5/10 with no burned-in subtitles; interview_ltx_v1 5.25 failed on garbled subtitles until the round-2 rewrite reached 7.88. | Two lines only were tested. Longer exchanges, named speakers and precise lip-sync remain untested. |
| Product beauty move on invented hardware | `kling_3_0_pro` | `seedance_2_5` | hero_kling_v2 8.38/10 at $0.45; hero_seedance25_v1 8.0 at $1.90 for a 4s cap. | Text-to-video does not hold identity between shots. Use reference-conditioned generation for a real product; untested here. |
| Exact interface, spelling, cursor or state change | `hyperframes` | `--` | ui_kling_v1 scored 3.75/10 with misspelled labels, invented sidebars and the wrong row clicked. The HyperFrames demo passed 0 lint/runtime/layout findings and all 40 contrast checks. | An authored concept UI is a design, not proof that software works. Screen-record real software for real claims. |
| Typography, counters, captions, contrast flip, final edit | `hyperframes` | `--` | Deterministic and seek-safe; $0 generation cost; used for the Cue demo and close. | Authoring time is the real cost. Zero API spend is not zero effort. |
| Cheap exploration before committing spend | `ltx_2_3_pro` | `--` | $0.08/s at 1080p, the lowest measured rate of the tested generative set. | Sampled detail was softer than the 720p Veo output despite the higher resolution. |
| Cinematic landscape or environment, no people | `veo_3_1_fast_silent` | `ltx_2_3_pro` | ridge_veo_v1 9.25/10 against ridge_ltx_v1 7.0/10 on byte-identical prompts; Veo cost $0.12 more. | One trial per model. LTX held the composition, it just lit it badly. |
| Human presence without a face - hands, gestures, tools | `kling_3_0_pro` | `veo_3_1_fast_silent` | hands_kling_v2 8.25/10 after one colour repair, against four attempts to get one usable talking head in the first loop. | Gloves and fingers still soften mid-shot. Cut before the softening, and end on the object rather than the hand. |
| Pure material or texture macro | `kling_3_0_pro` | `--` | weave_kling_v1 7.75/10; nothing for the model to miscount. | Delivered far less camera movement than requested. Budget an authored push. |
| Narration or voiceover, no on-camera speaker | `kokoro_local_tts` | `--` | Seven KEEL lines synthesized offline at zero cost with measured durations of 1.5-3.2s each, which then drove every cut, caption and music duck in the film. | No direction over emphasis or pause. Write lines short enough that the read cannot go wrong, and time the edit from the measured output rather than an estimate. |
| Any montage where shot quality varies | `veo_3_1_fast_silent` | `--` | KEEL bought 60s of plates for a 38s film for about $1.80 more than a minimal buy, and dropped rush_hands_v1 outright rather than defending it. | Only worth it at the silent rate. At $0.15/s with audio the same over-coverage costs nearly three dollars more. |

## Slate at a Glance

| Concept | Use case | Length | Paid shots | Estimated generation cost |
| --- | --- | ---: | ---: | ---: |
| Launchroom / From brief to launch | product_demo | 30s | 1 | $0.75 |
| Signal / Three verbs, one flip | video_ad | 20s | 2 | $0.90 |
| Pocket / Ship it before you forget it | ugc_ad | 25s | 2 | $1.20 |
| After the call / Decisions become work | interview | 35s | 2 | $2.70 |

Whole slate if every concept were produced once: **$5.54** estimated, excluding retries.
Measured retry rate in the loop was 4 repairs across 11 requests, so plan for more.

## Launchroom / From brief to launch

- Use case: `product_demo`
- Length: 30s
- Library references: Motion-5, SupersonikAI
- Estimated generation cost: $0.75

A one-line brief becomes a scene-by-scene plan, then a finished page. The interface carries the whole argument; a single human line opens it.

**Why this routing.** The observed references are almost entirely screen work. Generative UI failed the exact-text test at 3.75/10, so everything legible is authored and only the hook is bought.

| # | Time | Role | Tool | Pattern | Est. |
| ---: | --- | --- | --- | --- | ---: |
| 1 | 0-5s | ugc | `veo_3_1_fast` | `human_problem_hook` | $0.75 |
| 2 | 5-12s | product_demo | `hyperframes` | `voice_to_action_ui` | $0.00 |
| 3 | 12-22s | product_demo | `hyperframes` | `voice_to_action_ui` | $0.00 |
| 4 | 22-30s | motion_typography | `hyperframes` | `three_beat_close` | $0.00 |

### Scene 1 — 0-5s, `veo_3_1_fast`

```text
One uninterrupted creator-led ad. A woman in her early thirties with short dark hair at a plain studio desk, wearing a charcoal crewneck. Eye-level medium close-up and natural daylight. Says in measured English: "I can describe the video I want. Building it is the part that takes all week." Allow 4 seconds for the line. One subtle gesture, relaxed expression, quiet room tone, no baked-in text or music.
```

Accept when: Local transcript matches the line; delivery reaches at least 3.5s; no burned-in captions.

### Scene 2 — 5-12s, `hyperframes`

```text
Author the exact Launchroom interface. A single typed brief line lands in the composer, then stagger-reveal four scene cards with exact titles: Hook, Problem, Product, Close. Each card shows its own duration. Use dynamic-content-sequencing so the cards resolve in semantic order, not all at once.
```

Accept when: Zero layout and contrast findings; every card label spelled exactly; card durations sum to the stated total.

### Scene 3 — 12-22s, `hyperframes`

```text
Cursor drags the Problem card above Hook; the timeline re-flows and the durations recompute visibly. Then click Build once. A progress bar fills and resolves to a finished frame preview. One visible action only, one deterministic state change, readable hold on the result.
```

Accept when: Exactly one click; the recomputed durations are arithmetically correct on screen; result holds at least 1.5s.

### Scene 4 — 22-30s, `hyperframes`

```text
Three-beat headline cadence in the brand face: Plan it. Build it. Ship it. Then a contrast flip to the dark brand card and a logo-brand-close. Footer identifies the piece as an original concept.
```

Accept when: No text overflow or overlap; contrast checks pass on both the light and dark states.

## After the call / Decisions become work

- Use case: `interview`
- Length: 35s
- Library references: Tarun Amasa announcement, Cluely customer support
- Estimated generation cost: $2.70

Two founders, seated, trade one short question and one short answer about what happens to decisions after a meeting. Cuts to the artifact that proves the point.

**Why this routing.** The reference cuts between talking heads and an actual spreadsheet. Veo held a clean two-shot without subtitle corruption; any legible data is routed away from the generator.

| # | Time | Role | Tool | Pattern | Est. |
| ---: | --- | --- | --- | --- | ---: |
| 1 | 0-8s | interview | `veo_3_1_fast` | `two_person_question_answer` | $1.20 |
| 2 | 8-16s | product_demo | `hyperframes` | `voice_to_action_ui` | $0.00 |
| 3 | 16-26s | interview | `veo_3_1_fast` | `two_person_question_answer` | $1.50 |
| 4 | 26-35s | motion_typography | `hyperframes` | `three_beat_close` | $0.00 |

### Scene 1 — 0-8s, `veo_3_1_fast`

```text
Raw unedited two-shot camera footage of an interviewer on the left and a guest on the right in a plain office with a window behind them. Clean photographic frame with no graphic overlays and no subtitles. AUDIO: the left speaker asks "So what actually happens after the call ends?"; the right speaker listens, then answers "Everyone agrees, and then nobody writes it down." One speaker at a time. Natural mouth movement; quiet room tone.
```

Accept when: Both lines transcribe correctly; no burned-in subtitles; one speaker moves at a time.

### Scene 2 — 8-16s, `hyperframes`

```text
Authored cutaway: a meeting transcript pane on the left, an empty action list on the right. Three decisions highlight in the transcript and travel across as exact task rows with owners and dates. Hold the filled list.
```

Accept when: Transcript text and task text match exactly; no orphaned or clipped rows.

### Scene 3 — 16-26s, `veo_3_1_fast`

```text
Raw unedited two-shot camera footage, same plain office and same seating, continuing the conversation. No graphic overlays and no subtitles. AUDIO: the left speaker asks "And when it is written down?"; the right speaker answers "Then the week starts on Monday instead of Thursday." One speaker at a time; natural pause before the answer.
```

Accept when: Identity drift between scene 1 and 3 is checked on sampled frames and disclosed; re-shoot as one longer take if drift is visible.

### Scene 4 — 26-35s, `hyperframes`

```text
Pull the answer forward as a typographic card, then a three-beat close: Decide. Capture. Start. Contrast flip to the brand card with the concept footer.
```

Accept when: Quoted line matches the generated audio word for word.

**Known risk.** Two seated generations cannot be assumed to depict the same two people. Either accept one continuous take or treat the second exchange as a separate scene with different framing.

## Pocket / Ship it before you forget it

- Use case: `ugc_ad`
- Length: 25s
- Library references: Pocket introduction, Cluely customer support
- Estimated generation cost: $1.20

A creator admits the idea-to-nothing problem, the hardware appears, one capture happens, and the close lands on a single benefit.

**Why this routing.** This is the hybrid shape that already rendered successfully as Cue, reused with a different hook, a different device and a shorter run. Each role goes to its measured best performer.

| # | Time | Role | Tool | Pattern | Est. |
| ---: | --- | --- | --- | --- | ---: |
| 1 | 0-5s | ugc | `veo_3_1_fast` | `human_problem_hook` | $0.75 |
| 2 | 5-9s | product_hero | `kling_3_0_pro` | `macro_to_product_reveal` | $0.45 |
| 3 | 9-19s | product_demo | `hyperframes` | `voice_to_action_ui` | $0.00 |
| 4 | 19-25s | motion_typography | `hyperframes` | `three_beat_close` | $0.00 |

### Scene 1 — 0-5s, `veo_3_1_fast`

```text
One uninterrupted creator-led ad. A man in his late twenties walking slowly on a quiet residential street at golden hour, wearing a plain oatmeal sweater. Eye-level medium close-up, handheld but steady. Says in measured English: "My best ideas happen on this walk. None of them survive it." Allow 4 seconds for the line. One subtle gesture, quiet outdoor room tone, no baked-in text or music.
```

Accept when: Transcript matches; face stable across sampled frames; walking motion does not smear the background.

### Scene 2 — 5-9s, `kling_3_0_pro`

```text
One camera pullback on a small matte aluminium recorder the size of a poker chip, featuring exactly one recessed black button on its top face and no other markings. Start on this button, pull back to a full three-quarter product view. Object remains stationary on a dark slate surface. End with the right third of the frame entirely clear for typography. Hold the final composition. Plain unbranded surfaces, no extra parts, no writing.
```

Accept when: Exactly one button, no extra lights or seams, right third clear, object does not tilt.

### Scene 3 — 9-19s, `hyperframes`

```text
Authored phone-shaped panel. A press indicator, a waveform, then the transcript resolves to one exact line: "Pitch the walking app to Dana." Stagger-reveal a single reminder row with a time. One cursor tap sets it. Hold the confirmed state.
```

Accept when: Exact sentence spelled correctly; exactly one tap; confirmed state holds.

### Scene 4 — 19-25s, `hyperframes`

```text
Benefit line in the brand face, then the contrast flip and logo-brand-close: Say it once. Keep it forever. Concept footer stays legible over the dark card.
```

Accept when: Benefit line clears the frame before the closing transition covers it; contrast passes.

## Signal / Three verbs, one flip

- Use case: `video_ad`
- Length: 20s
- Library references: Content Rewards reveal
- Estimated generation cost: $0.90

No dialogue. A product move, three verbs, a dark-to-light flip, and a call to action. The cheapest shape in the slate.

**Why this routing.** Removing speech removes the model's weakest measured axis. All copy is authored, so the only paid shot is the beauty move Kling already handled at 8.38/10.

| # | Time | Role | Tool | Pattern | Est. |
| ---: | --- | --- | --- | --- | ---: |
| 1 | 0-4s | product_hero | `kling_3_0_pro` | `macro_to_product_reveal` | $0.45 |
| 2 | 4-8s | product_hero | `kling_3_0_pro` | `macro_to_product_reveal` | $0.45 |
| 3 | 8-16s | motion_typography | `hyperframes` | `three_beat_close` | $0.00 |
| 4 | 16-20s | motion_typography | `hyperframes` | `three_beat_close` | $0.00 |

### Scene 1 — 0-4s, `kling_3_0_pro`

```text
One slow orbit around a matte ceramic desk object shaped like a shallow cylinder, featuring exactly one thin brass ring around its base and no other detail. Start tight on the ring, orbit to a three-quarter view. Object remains stationary against a deep charcoal seamless background. End with the left half of the frame entirely clear for typography. Hold the final composition. Plain unbranded surfaces, no extra parts, no writing.
```

Accept when: One ring only, no invented logos, left half clear, no tilt or drift.

### Scene 2 — 4-8s, `kling_3_0_pro`

```text
One camera push from a wide desk view toward the same shallow ceramic cylinder with exactly one thin brass ring, on the same deep charcoal seamless background. Object remains stationary. End centred with the lower third entirely clear for typography. Hold the final composition. Plain unbranded surfaces, no extra parts, no writing.
```

Accept when: Shape and ring read as the same object as scene 1 on sampled frames; disclose any drift.

### Scene 3 — 8-16s, `hyperframes`

```text
Waterfall-entry three-beat cadence over the held product frames: Capture. Clarify. Commit. Each verb holds long enough to read, then hands off before the next enters.
```

Accept when: Each verb holds at least 1.2s; no two verbs on screen at once.

### Scene 4 — 16-20s, `hyperframes`

```text
Contrast flip from dark to the bright brand card, single call to action, logo-brand-close, concept footer.
```

Accept when: Contrast passes on the bright card; footer legible at 1080p.

**Known risk.** Two separately generated shots of the same invented object will not match exactly. Treat scene 2 as a different angle of a similar object or generate one longer take and cut it.

## How to Produce One

1. Copy the concept into a run plan shaped like `configs/library_loop_round2.json`,
   one entry per paid scene, with `estimate_cents` computed from the rate table above.
2. Raise the cap deliberately. `BudgetLedger` refuses to change the limit on an existing
   ledger, so a larger run needs its own ledger file and its own approval.
3. `python scripts/run_library_loop.py <plan>` submits once per reserved run and resumes
   persisted queue IDs instead of resubmitting.
4. `python scripts/evaluate_library_loop.py --speech` freezes frames, probes and transcripts.
5. Check each scene against its stated acceptance line before assembling anything.
6. Author every legible element in HyperFrames, then render and verify the full decode.

## Limits

The routing rules come from one trial per model per role, without repeat seeds or
confidence intervals. They describe what happened here, not a general model ranking.
Untested pairings stay untested: nothing below claims a model cannot do a job it was
never asked to do. All four concepts are fictional products; none is a customer claim.

