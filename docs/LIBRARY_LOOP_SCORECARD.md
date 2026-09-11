# Capability and Results Scorecard

Subjective 0-10 scores from eight evenly sampled frames per output and local Whisper transcripts; no human audience testing, calibrated perceptual model, or independent audio listening. Temporal stability is sampled, not exhaustive.

Scores average four equally weighted criteria. Compare within use case only.
Resolution, clip duration, seed availability and stochastic variation confound cross-model comparisons.
Latency includes queue polling and download, not just inference. No repeat-seed confidence intervals.

| Run | Role | Score / 10 | Dimensions | Estimate | Seconds elapsed |
| --- | --- | ---: | --- | ---: | ---: |
| ugc_veo_v1 | ugc | 8.5 | 1280x720 | $0.90 | 90.46 |
| ugc_grok_v1 | ugc | 8.0 | 1280x720 | $0.85 | 83.49 |
| ugc_ltx_v1 | ugc | 7.38 | 1920x1080 | $0.48 | 86.24 |
| hero_kling_v1 | product_ad | 6.75 | 1920x1080 | $0.45 | 107.09 |
| hero_seedance25_v1 | product_ad | 8.0 | 1280x720 | $1.90 | 222.37 |
| interview_ltx_v1 | interview | 5.25 | 1920x1080 | $0.48 | 78.03 |
| ui_kling_v1 | product_demo | 3.75 | 1920x1080 | $0.56 | 125.33 |
| ugc_veo_v2 | ugc | 8.75 | 1280x720 | $0.90 | 69.85 |
| hero_kling_v2 | product_ad | 8.38 | 1920x1080 | $0.45 | 148.27 |
| interview_ltx_v2 | interview | 7.88 | 1920x1080 | $0.48 | 129.43 |
| interview_veo_v1 | interview | 8.5 | 1280x720 | $0.90 | 63.22 |

## Capability Coverage

| Model / tool | UGC | Product beauty | Exact UI | Interview | Motion type |
| --- | --- | --- | --- | --- | --- |
| Veo 3.1 Fast | Tested, selected | N/T | N/T | Tested, preferred | N/T |
| Grok Imagine 1.5 | Tested alternative | N/T | N/T | N/T | N/T |
| LTX 2.3 Pro | Tested, economical draft | N/T | N/T | Tested, improved with prompt repair | N/T |
| Kling 3.0 Pro | N/T | Tested, selected v2 | Tested, rejected | N/T | N/T |
| Seedance 2.5 | N/T | Tested, premium alternative | N/T | N/T | N/T |
| HyperFrames | Assembly only | Assembly only | Authored and rendered | Assembly only | Authored and rendered |

N/T means not tested, not incapable. There is no defensible universal winner.

## Observations

### ugc_veo_v1
Clean face, hand and framing. Correct transcript; line ends at 2.8s, leaving a posed smile for roughly half the clip. Useful short hook but not the intended six-second performance.

### ugc_grok_v1
Correct transcript, restrained clean scene. Line finishes at 2.72s; gaze shifts off lens and hand movement is more expansive than requested. Good economical alternative to Veo in this one sample.

### ugc_ltx_v1
Correct spoken line, finishes at 4.24s. More cluttered bookshelves and larger gestures; slightly softer sampled detail despite 1080p. Low-cost UGC roughs remain useful.

### hero_kling_v1
Convincing camera pullback but pale button instead of dark, several side LEDs instead of one, centered final composition. Inaccurate hardware specification, not selected.

### hero_seedance25_v1
Attractive fine material and coherent macro pullback, dark button and one top light. Device tilts slightly instead of remaining planted, with softer rounded shape. Strong appearance but much higher cost on this small shot; not proof of overall model inferiority.

### interview_ltx_v1
Both requested spoken lines transcribe correctly, but garbled yellow subtitles are burned in despite no-subtitles instruction. Reject as a clean interview plate.

### ui_kling_v1
Captures broad waveform-to-tasks idea but heading and task labels are misspelled, adds unsolicited sidebars and checks the third rather than first row. Reject for exact product demos. Route text and interactions to HyperFrames.

### ugc_veo_v2
Correct transcript extends to 3.9s vs 2.8s. More reflective expression, stable frame and skin detail. Timing still not exact and uses more than one hand gesture. Selected for final human hook.

### hero_kling_v2
Black button, one visible top LED, clean plain side and improved right-side negative space. Starts wider than the requested macro and retains small markings on button. Selected; original concept geometry, not faithful to a real manufactured device.

### interview_ltx_v2
Rewording as raw camera footage removes burned-in subtitles. Correct transcript with both lines, plausible speaker staging. More subdued exposure and stiff interaction than Veo. Successful repair in one trial, not guaranteed reproducibility.

### interview_veo_v1
Both lines transcribe correctly, no visible subtitle insertion, clean brighter presentation and plausible turns. Tiny sample: long exchanges, speaker identity and precise lip-sync remain untested.

## Loop Outcome

- Veo UGC v1 -> v2: same line extends from 2.8 to 3.9 seconds in the local transcript. Better pacing; not the exact 4.8s target.
- Kling hero v1 -> v2: pale button/multiple LEDs/central framing repaired to black button, one top light and usable right-side placement.
- LTX interview v1 -> v2: corrupted burned-in subtitles removed by clean-camera wording. Both versions transcribe the requested lines.
- Kling UI -> HyperFrames: switch tools when exact symbols, spelling and interactions fail; do not keep spending on the wrong role.
- HyperFrames first check -> revision: hide outgoing benefit text once covered by the closing transition; rerun layout and contrast checks.
- Final mix -> revision: strip embedded audio from video plates and keep the separately mastered dialogue track; prevent duplicate speech and clipping.

## Budget

Estimated generation total: $8.35. Conservative reserved total: $9.66. Hard cap: $10.00.
All 11 paid requests completed. No paid retries, new paid image/audio calls, or further submissions. Provider invoice not queried.

## Reproduce

Run plans are in configs/library_loop_round1.json and configs/library_loop_round2.json. The runner resumes stored IDs and never intentionally resubmits the same run ID.
Keep artifacts/library-loop/budget.json: it is the persistent cost and request ledger. Deleting it defeats the guard.
Run scripts/evaluate_library_loop.py --speech for local evidence, scripts/report_library_loop.py for this report, and npm run render in hyperframes/cue for the final edit.
Research and primary source links: docs/LIBRARY_LOOP_RESEARCH.md. Reusable patterns: prompt_library/library_loop_patterns.json.
Next concepts, routed scene by scene from this evidence: docs/LIBRARY_LOOP_CONCEPTS.md, rebuilt by scripts/build_concept_slate.py.

## HyperFrames Result

30-second 1080p H.264/AAC final. Exact labels and first-row click confirmed visually. Zero lint/runtime/layout/motion findings, 24 layout samples, 300 motion samples, all 40 contrast checks pass.
No generation API cost. Local rendering and code authoring are not free labor and are not equivalent inputs to a generative model. Final verification includes full decode and audio measurements.
