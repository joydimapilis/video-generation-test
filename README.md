# Amarillo Video Prompt Lab

Amarillo is a local-first system for turning reference video samples into reusable AI-video prompt patterns, testing those patterns across Fal-hosted models, and producing evidence-based model scoreboards.

## Repository structure

- **Repository root: the video-generation system (Amarillo).** `src/`, `scripts/`, `configs/`, `prompt_library/`, `catalog/`, `hyperframes/`, `videos/`, `docs/`, `analysis_notes/`, `review_notes/`, `assembled_outputs/`, and `tests/` are the core workflow and its production records. See [Main Folders](#main-folders) below.
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

## Latest session deliveries

The current delivery is **Portion**, a new 36-second before/after catering workflow
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

If unset, it uses `data/library`, then a single accessible library recorded in prior reference manifests. Missing or ambiguous libraries fail clearly.
