# Amarillo Video Prompt Lab

Amarillo is a local-first system for turning reference video samples into reusable AI-video prompt patterns, testing those patterns across Fal-hosted models, and producing evidence-based model scoreboards.

## Repository structure

- **Repository root: the video-generation system (Amarillo).** `src/`, `scripts/`, `configs/`, `prompt_library/`, `catalog/`, `hyperframes/`, `videos/`, `docs/`, `analysis_notes/`, `review_notes/`, `assembled_outputs/`, `references/`, and `tests/` are the automated video-generation workflow and its production records. See [Main Folders](#main-folders) and [Latest automated video-generation work](#latest-automated-video-generation-work) below. Rendered media stays local under the ignored `artifacts/` tree.
- **[`demo-videos/`](demo-videos/README.md): the Demo Videos workspace.** Self-contained Tesseract (by Mirage) editing workspace for the product demo videos: demo scripts, screen recordings, audio and AI voice, edited outputs, notes, and the Tesseract launcher and skills they use. It does not depend on, or change, the system at the root.

## Workflow

The near-term workflow is intentionally conservative:

1. Put reference videos in `data/samples/`.
2. Run ingestion to extract metadata and keyframes.
3. Generate reusable prompt patterns from each sample.
4. Plan model runs under a spend cap.
5. Run selected experiments through Fal only when `--live` is passed.
6. Score outputs, compare them to the reference sample, and write a compact review pack.

```bash
python3 -m amarillo.cli init
python3 -m amarillo.cli ingest --samples data/samples
python3 -m amarillo.cli analyze
python3 -m amarillo.cli build-prompts
python3 -m amarillo.cli plan-runs --max-estimated-cost 2.00
python3 -m amarillo.cli run-fal --run-plan artifacts/run_plans/latest.json
python3 -m amarillo.cli refresh-artifacts
```

Live Fal calls are disabled by default. To spend credits, use:

```bash
python3 -m amarillo.cli run-fal --run-plan artifacts/run_plans/latest.json --live --max-estimated-cost 2.00
```

To benchmark reusable prompt variants:

```bash
python3 -m amarillo.cli plan-runs --include-variants --max-estimated-cost 2.00
python3 -m amarillo.cli run-fal --run-plan artifacts/run_plans/latest.json --live --max-estimated-cost 2.00
python3 -m amarillo.cli score
python3 -m amarillo.cli recommend
python3 -m amarillo.cli catalog-outputs
python3 -m amarillo.cli evaluate-outputs
python3 -m amarillo.cli compare-reference
python3 -m amarillo.cli build-review-pack
python3 -m amarillo.cli build-knowledge
python3 -m amarillo.cli report
```

After any new run or review-note edit, refresh the evidence artifacts with:

```bash
python3 -m amarillo.cli refresh-artifacts
```

The first HyperFrames finishing prototype lives in `hyperframes/cero-overlay/`.

```bash
cd hyperframes/cero-overlay
npx hyperframes check --snapshots
npx hyperframes preview --background --port 3017
```


## Latest automated test run

**Tuck — Receipts to ready** is a new **30-second product launch film** with a subtle hand-and-receipt opening, exact AI expense walkthrough, and human callback beside the finished report. New footage, script, UI, narration and music; no interviews or earlier generated scenes.

[Watch the MP4](artifacts/final_outcome/tuck/tuck.mp4) · [Review player](artifacts/final_outcome/tuck/review.html) · [Delivery checks](docs/LATEST_RUN.md) · [Scorecard](docs/TUCK_SCORECARD.md) · [Rebuild and learnings](docs/TUCK_RUNBOOK.md)

**$1.60 estimated generation cost; $1.84 reserved under a $10 cap.** 1920×1080, 24fps. All 720 frames decode; UI interactions, expense totals, source timing, audio alignment and scene continuity pass verification.

## Previous run: Fold

**Fold — From scattered to started** is a new **31-second product launch film** for a fictional AI creative-brief builder. Scattered notes become a brief, two concise interactions show how it works, and the completed campaign board remains visible at the ending. Bright coral/cream graphics, new local narration and original music; no interviews.

[Watch the MP4](artifacts/final_outcome/fold/fold.mp4) · [Review player](artifacts/final_outcome/fold/review.html) · [Delivery checks](docs/LATEST_RUN.md) · [Creative scorecard](docs/FOLD_SCORECARD.md) · [Rebuild and learnings](docs/FOLD_RUNBOOK.md)

**$0 estimated generation API cost under a $10 cap.** 1920×1080, 24fps; all 744 frames decode. Exact UI, cursor targets, scene seams and audio alignment verified. No new video-model benchmark was necessary for this graphic concept.

## Previous run: Trace

**Trace — Keep the context** is a completely new **33-second software product film** with exact UI, a short newly generated hand/device insert, local narration and an original electronic score. No interviews or earlier generated footage.

[Watch the MP4](artifacts/final_outcome/trace/trace.mp4) · [Review player](artifacts/final_outcome/trace/review.html) · [Delivery checks](docs/LATEST_RUN.md) · [Scorecard](docs/TRACE_SCORECARD.md) · [Rebuild and learnings](docs/TRACE_RUNBOOK.md)

Three new test clips: **$1.36 estimated**, **$1.57 reserved** under one $10 cap. Finished output: 1920×1080, 24fps. Full decode, source timing, audio alignment and UI checks pass.

## Previous run: Crumb

Three completely fresh **Crumb** sample films are ready in
`artifacts/final_outcome/crumb/`: customer UGC (19.75s), baker interview with
order-list demo (21.25s), and pastry-led preorder ad (17s).

This run generated **12 new test clips for $5.10 estimated**, with **$5.92
reserved** under one $10 cap. Final media uses only footage generated in this
run. Veo supplies the customer, revised H3 Max supplies the baker and a new
identity-conditioned return, Kling supplies pastry/continuity, and HyperFrames
supplies exact text, interfaces and final edits.

[Watch all three](artifacts/final_outcome/crumb/review.html) ·
[Delivery and validation](docs/LATEST_RUN.md) ·
[Scorecard](docs/CRUMB_SCORECARD.md) ·
[Research](docs/CRUMB_RESEARCH.md) · [Resume/rebuild](docs/CRUMB_RUNBOOK.md)

## Previous run: H3 samples

Three new samples from the September 12 H3 screening run are ready in
`artifacts/final_outcome/round8/`:

- **Cue / Follow-through** — 18s creator ad: new H3 presenter and product footage, exact HyperFrames task demo.
- **Cue / Object study** — 13.54s product film: new H3 reveal → Kling continuation from the reviewed exit frame.
- **Crew / Availability** — 18s interview-led demo: reviewed Veo presenter plus a new HyperFrames schedule sequence.

Seven new generations cost **$3.20 estimated**, with **$3.72 reserved** in one
persistent **$10** ledger. H3's speech worked, but its interview performance stayed
too expressive with and without prompt expansion. Veo remains the interview
route. Kling produced the closer measured product handoff in this small trial.

See [the sample scorecard](docs/H3_SAMPLES_SCORECARD.md),
[research and reusable techniques](docs/ROUND8_RESEARCH_AND_LEARNINGS.md),
[latest delivery](docs/LATEST_RUN.md), and
[automation instructions](docs/AUTOMATED_VIDEO_LAB.md).

```sh
.venv/bin/python scripts/run_library_loop.py configs/h3_samples_round1.json --evaluate
.venv/bin/python scripts/run_library_loop.py configs/h3_samples_round2.json --evaluate
.venv/bin/python scripts/run_library_loop.py configs/h3_samples_continuity.json --evaluate
.venv/bin/python scripts/learn_from_loops.py --route interview --reference --audio
```

Resuming these exact plans reuses persisted jobs. All three plans share
`artifacts/library-loop-8/budget.json`; no automatic paid retries or cap resets.
Routing learns from compatible decoded and reviewed outputs; missing realism,
lip-sync or continuity dimensions remain untested. Earlier interview comparison:
`artifacts/library-loop-7/interview-comparison.mp4` and
[its scorecard](docs/INTERVIEW_MODEL_SCORECARD.md).

## Current Defaults

- People scenes: source image → internal image review → image-to-video → motion
  review, following [the production defaults](AGENTS.md). This remains part of
  normal video generation.
- The human-movement clips in `references/human-realism/` are reserved for separate
  Phase 2 human-realism evaluation and improvement. They are not a default
  production dependency. General video reference review and normal generated-shot
  realism checks remain in place.
- First use case: reusable short-form marketing/social clips.
- Review format: Markdown milestone report plus machine-readable JSON.
- Output formats: MP4 videos, JSON prompt library, JSONL experiment logs, Markdown reports.
- Budget posture: cheap planning and dry runs by default; explicit live flag required.
- Safety posture: abstract style, structure, motion, and editing patterns; avoid copying protected characters, identifiable people, private brands, or exact ad executions.

## Main Folders

- `data/samples/`: reference videos to analyze.
- `artifacts/`: generated metadata, keyframes, run plans, results, and reports.
- `artifacts/review_pack/`: compact human review page and shortlist.
- `artifacts/reference_comparisons/`: automated source-vs-output visual signature comparisons.
- `prompt_library/`: reusable prompt patterns derived from references.
- `catalog/`: model catalog and model-selection evidence.
- `docs/`: roadmap, methodology, and operating notes.
- `demo-videos/`: the separate Demo Videos workspace (not part of the Amarillo pipeline).

## Latest automated video-generation work

Added on 2026-09-24. Everything here lives at the repository root, separate from
`demo-videos/`.

**Workflow changes** (see [core workflow gates](docs/CORE_VIDEO_WORKFLOW.md)):

- Every final MP4 needs its own `<mp4-stem>.reverse-engineering.md`, written and
  checked by `scripts/reverse_engineering.py`. Finalizers call
  `amarillo.delivery.require_reverse_engineering` before recording completion.
- Every new request reviews general-library footage first and validates
  `videos/<name>/reference-review.json` with `scripts/verify_reference_review.py`.
- The library resolver rejects the Phase 2 `references/human-realism/` collection;
  core learning accepts whole-take `selected`/`accepted`/`approved` decisions.

**Sample outputs.** MP4s are local under `artifacts/final_outcome/<name>/`. Hashes,
costs and limitations are in `assembled_outputs/<name>.json`.

| Production | Output | Estimated / reserved provider USD | Scorecard |
| --- | --- | ---: | --- |
| Kite campaign | 36s deterministic HyperFrames film, no paid generation | $0 / $0 | [Scorecard](docs/KITE_CAMPAIGN_SCORECARD.md) |
| Kite core demo | 30s film with one Kling 3.0 Pro paper take and a demo page | $0.56 / $0.65 | [Scorecard](docs/KITE_CORE_DEMO_SCORECARD.md) |
| Kite feedback | 36s Slack-to-Kite feedback film; I2V bookend revision reusing existing takes | $0 new; inherited cost unresolved | [Scorecard](docs/KITE_FEEDBACK_SCORECARD.md) |
| Kite Tomorrow series | 38s film revisions (Slack, UI pass 2, character pass, final) plus a contact test | Character pass $2.73 / $3.14; historical Higgsfield USD unresolved | [Scorecard](docs/KITE_TOMORROW_CHARACTER_SCORECARD.md) · [Notes](review_notes/kite-tomorrow.md) |
| Computer realism samples | Three short I2V computer-interaction studies | $8.38 / $9.67 | [Scorecard](docs/COMPUTER_REALISM_SAMPLES_SCORECARD.md) |
| Computer movement studies 02 | Reading pause, mouse movement, laptop typing | $8.60 / $9.92 | [Scorecard](docs/COMPUTER_MOVEMENT_STUDIES_02_SCORECARD.md) |
| Computer movement long | 15s, 15s and 9s desktop, mouse and laptop sequences, each with its own ledger | $20.39 / $23.51 cumulative across the three videos | [Scorecard](docs/COMPUTER_MOVEMENT_LONG_SCORECARD.md) |
| Sideway human-realism tests | Café left-hand correction and a reference comparison (diagnostic only) | $10.57 / $12.21 cumulative, user-approved $12.25 cap | [Left hand](review_notes/sideway/left-hand-correction.md) · [Comparison](review_notes/sideway/sample02-test-results.md) |

No invoices were confirmed. These figures are published-quote estimates with the
15% reservation buffer, and unknown historical costs are not counted as zero.

**Learnings** (details in the scorecards and `prompt_library/tested_*_patterns.json`):

- Selecting a usable segment is valid, but it does not make the full take a success.
  Long takes still drift into hovering hands, finger splay and downward keyboard gaze.
- Written movement observations from reference clips did not reliably improve
  realism. Model, prompt and seed changes confound every comparison.
- Seedance improved gaze and expression timing in the Kite character pass, but its
  faces are softer than Veo's. One comparison does not rank the models.
- Deterministic UI films need checks for font glyph coverage, media stacking and
  contrast before layout findings can be trusted. Keep the result visible through
  the CTA.

## Previous session deliveries

The previous delivery was **Portion**, a new 36-second before/after catering workflow
film. Serein and Sideway also include the latest mouse, gaze, dialogue and café
revisions. Each project includes editable compositions, source-image and motion
prompts, generation plans, review decisions and rebuild instructions.

| Film | Latest work | Estimated generation cost | Rebuild and review |
| --- | --- | ---: | --- |
| Portion | New image-first human scenes and exact order-to-prep UI | $4.04 / $10 cap | [Runbook](docs/PORTION_RUNBOOK.md) · [Scorecard](docs/PORTION_SCORECARD.md) |
| Serein | Visible mouse interaction and screen-aligned gaze | $7.92 / $10 cap | [Runbook](docs/SEREIN_RUNBOOK.md) · [Scorecard](docs/SEREIN_SCORECARD.md) |
| Sideway | Conversational dialogue, phone gaze and candid café pose | $10.12 / user-approved $12 cap | [Runbook](docs/SIDEWAY_RUNBOOK.md) · [Scorecard](docs/SIDEWAY_SCORECARD.md) |

Costs include image planning allowances, not confirmed image invoices. The default
generation ceiling remains $10; a larger cap requires explicit caller approval and
preserves every earlier reservation. Image allowances share the budget but are
excluded from video-model scoring. The latest snapshot covers 104 recorded video
attempts; review scores remain subjective and provisional.

Delivery manifests and hashes are in `assembled_outputs/`. Machine scorecards,
source-image reviews and final verification summaries are tracked in `review_notes/`.
Generated MP4s, stills, audio, fonts and render caches remain local under the existing
media-exclusion policy. Regenerating model footage can incur cost and does not
reproduce identical bytes; retain the approved local media to reproduce an edit.

## Earlier delivered films

The earlier concept films below were produced inside `$10` estimated-cost
ledgers. Rendered MP4s live under `artifacts/final_outcome/<name>/` and are not in
Git; the compositions that produce them are.

| Film | Use case | Length | Est. cost | Scorecard |
| --- | --- | ---: | ---: | --- |
| Cue | Product ad with UI demo | 30s | $8.35 | `docs/LIBRARY_LOOP_SCORECARD.md` |
| ORRIN | Industrial hardware film, silent | 30s | $5.17 | `docs/ORRIN_SCORECARD.md` |
| KEEL | Narrated brand manifesto | 38s | $6.84 | `docs/KEEL_SCORECARD.md` |
| Seventeen | Founder origin story | 42s | $6.08 | `docs/SEVENTEEN_SCORECARD.md` |
| The Sunday Problem | Customer testimonial | 36s | $7.88 | `docs/ROTA_SCORECARD.md` |
| The Sunday Problem (revised) | Customer testimonial, clarified | 44s | $5.10 | `docs/CREW_SCORECARD.md` |
| The Sunday Problem (realism cut) | Testimonial, human realism and shot continuity | 49s | $8.48 cumulative | `docs/CREW_REALISM_REPORT.md` |

The realism cut supersedes the revised cut and shares its ledger. It ships with a
silent before/after reel at
`artifacts/final_outcome/crew-improved/crew-before-after.mp4`; the earlier cut
stays at `artifacts/final_outcome/crew/` unchanged.

Routing rules accumulated across those loops are in
`prompt_library/concept_slate.json`; reusable prompt patterns are in
`prompt_library/library_loop_patterns.json`.

## Reproducing a Film

Generated media is deliberately not committed - it is large and fully
regenerable. To rebuild a film from source:

```bash
pip install -e '.[video-review]'            # numpy, faster-whisper, fonttools, brotli
export FAL_KEY=...                          # only needed to re-generate plates
python scripts/prepare_crew_assets.py       # stages plates, synthesizes score
cd hyperframes/crew && npm run check && npm run render
```

The realism cut restages from the first cut's assets rather than from scratch,
and its plates are 24fps, so the render has to be told:

```bash
python scripts/build_crew_improved.py       # restages, re-times, rebuilds the composition
python scripts/build_crew_comparison.py     # silent before/after reel
cd hyperframes/crew-improved && npx hyperframes check && npx hyperframes render -f 24 -q high
python scripts/finalize_crew_improved.py    # delivery gates, then artifacts/final_outcome/
```

Each `scripts/prepare_*_assets.py` restages its plates and regenerates its audio
deterministically from a fixed seed, so `hyperframes/*/assets/` is reproducible
and stays out of Git.

### Reference library path

The source video library lives outside this repository. Point the inspectors at
it with an environment variable rather than editing them:

```bash
export AMARILLO_LIBRARY_DIR="/path/to/your/video library"
python scripts/inspect_library_slice.py --out artifacts/slice --terms configs/library_slice_round5.json
```

If unset, it uses `data/library`, then a single accessible general library recorded
in prior reference manifests. Missing or ambiguous libraries fail clearly.
The core resolver rejects `references/human-realism` and symlink aliases, including
when explicitly configured. This workspace's gitignored `data/library` points to
`/Users/joydimapilis/Desktop/untitled folder/Startup Launch Videos` (11 accessible
MP4s verified on 2026-09-23; older records describe a larger collection).

Every new request automatically includes agent review of relevant general-library
footage before shot planning. The agent records and validates
`videos/<name>/reference-review.json`; a generated contact sheet is not itself a
completed review. Core learning uses `artifacts/learning/core.json`, supports
historical `selected` approvals, and retains both success and failure findings.

Every final MP4 requires its own adjacent `<mp4-stem>.reverse-engineering.md`.
The completion gate checks the individual document, required content and current
MP4 hash; missing/stale documents block completion. Multi-video projects require
one document per video. See [core workflow gates](docs/CORE_VIDEO_WORKFLOW.md)
for the reference-review schema, production-record fields and write/check commands.
