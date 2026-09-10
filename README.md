# Amarillo Video Prompt Lab

Amarillo is a local-first system for turning reference video samples into reusable AI-video prompt patterns, testing those patterns across Fal-hosted models, and producing evidence-based model scoreboards.

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
