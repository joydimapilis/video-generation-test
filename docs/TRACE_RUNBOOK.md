# Trace — product-led software film

The new finished film is `artifacts/final_outcome/trace/trace.mp4`: 33 seconds, 1920×1080, 24fps. Trace is a fictional browser bug-reporting product. It records a checkout problem and produces reproduction steps, a screenshot and browser context for a developer. The closing CTA is “Capture your next bug.”

The final video contains three seconds of newly generated hand/device footage, 17.5 seconds of continuous authored UI, and original typography/brand scenes. No interview or prior generated video is used. New narration uses local Kokoro af_heart, and the sparse electronic score is newly synthesized at 108 BPM.

## Library patterns used

The existing library resolver found 347 files in the connected Google Drive folder. Three local references were sampled; paths, lengths and sheets are in `artifacts/library-loop-10/references/manifest.json`.

- The Jam reference combines interviews with actual software surfaces. Only the concrete screen demonstration pattern transfers to Trace.
- Lucent shows a user-session problem, then a visible report. Trace borrows that problem-to-evidence structure and removes the interview emphasis.
- The file named Motion-5 actually shows a Grok Bot UI film. Its sparse stage, readable product states and explicit final lockup informed pacing. The filename was not treated as evidence of its contents.

These are structural inspirations. No library video or earlier generated scene appears in Trace.

## New tests and changes

The existing scorecards favor deterministic UI/text and often route faceless hand/device footage to Kling. This run compared one identical five-second prompt in Kling 3 Pro and H3 Max. H3 Max better matched the intended blue palette, while both showed some finger-pose ambiguity. A tighter overhead H3 Max revision improved framing. Source seconds 1–4 of v2 are used. The final crop omits the small screen edge; generated keyboard glyphs are incidental photography, never the software demo.

The first authored UI draft had a cursor above Record, a payment-field/button overlap, and a prefilled form before recording started. The revision fixed the pointer coordinates and spacing and showed form values filling after Record. All three action targets were checked against measured cursor positions. UI scene states share one browser element, preserving position across the transition into the report.

The keyframes onion diagnostic applies a fitted marker view that did not match the visible button geometry in this project. Actual snapshots and DOM measurements, saved in `cursor-targets.json`, were used to verify clicks. All three land inside their target rectangles.

An intentional full-frame blue entrance is marked for overflow because its panel moves through the scene clipping boundary. Old hook text fades before the product name arrives. Encoded transition review caught one-frame hand bleed behind the entering browser and an empty CTA boundary; an opaque demo background plus a brief overlapping final wipe corrected both. The report fades under the advancing wipe, before the final headline arrives. The first check hit a browser navigation timeout; a 30-second initialization allowance completed successfully. Final checks have zero findings and 59/59 contrast checks pass. The CLI's motion sub-audit was disabled; a separate keyframes export, full-frame snapshots, cursor checks and encoded transition strips were reviewed instead.

## Budget and sources

One persistent ledger, `artifacts/library-loop-10/budget.json`, protects this run's **$10** cap. Three requests completed: **$1.36 estimated**, **$1.57 reserved** including the runner's 15% buffer. No failed, pending or automatically retried jobs. Provider invoice not queried.

Pricing checked September 15, 2026:

- [Kling 3 Pro](https://fal.ai/models/fal-ai/kling-video/v3/pro/text-to-video): silent generation $0.112/s; five seconds estimated at $0.56.
- [H3 Max](https://fal.ai/models/minimax/h3-max/text-to-video): normal native 768P rate from September 15 is $0.08/s; two five-second requests estimated at $0.40 each. The $0.02/s launch promotion ended September 14 and is not used in this budget.

Narration, score, authored UI and rendering added no generation API charge. Selected generated footage is 1344×768, cropped into a 1060×800 region. The finished composition is 1080p; the generated plate is not natively 1080p. Sampled visual review and numerical audio checks are not an independent listening or audience test.

## Rebuild locally

```sh
.venv/bin/python scripts/prepare_trace_assets.py
.venv/bin/python scripts/build_trace_composition.py
node scripts/verify_trace_geometry.cjs
npx hyperframes@0.8.40 check hyperframes/trace --timeout 30000 --json
npx hyperframes@0.8.40 render hyperframes/trace -f 24 -q high -w 2 -o artifacts/final_outcome/trace/trace.mp4 --skill general-video
.venv/bin/python scripts/verify_trace_video.py
```

Run from the repository root. Existing narration files are reused on rebuild; remove only an intentionally replaced line to regenerate it locally. The selected plate is preserved at `hyperframes/trace/assets/hands.mp4`; its source path, source range and hash are in `hyperframes/trace/sources.json`. The editable project pins HyperFrames 0.8.40.

Resume a generation download using the existing ledger, without submitting the same paid job again:

```sh
.venv/bin/python scripts/run_library_loop.py configs/trace_round1.json --evaluate
.venv/bin/python scripts/run_library_loop.py configs/trace_round2.json --evaluate
```

Do not delete or reset the ledger. New paid requests require a new ID and cost estimate within its remaining cap.

Review UI: `http://localhost:3035/#project/trace`. Start or verify it with `npx hyperframes preview hyperframes/trace --background --port 3035` and `npx hyperframes preview hyperframes/trace --status`.

Reusable patterns: `prompt_library/tested_trace_patterns.json`. Reviewed model results: `review_notes/trace.json` and `docs/TRACE_SCORECARD.md`. Cross-loop learning was refreshed after scoring all three takes.
