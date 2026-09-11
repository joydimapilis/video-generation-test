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

## Delivered Films

Six finished concept films, each produced inside its own `$10` estimated-cost
ledger. Rendered MP4s live under `artifacts/final_outcome/<name>/` and are not in
Git; the compositions that produce them are.

| Film | Use case | Length | Est. cost | Scorecard |
| --- | --- | ---: | ---: | --- |
| Cue | Product ad with UI demo | 30s | $8.35 | `docs/LIBRARY_LOOP_SCORECARD.md` |
| ORRIN | Industrial hardware film, silent | 30s | $5.17 | `docs/ORRIN_SCORECARD.md` |
| KEEL | Narrated brand manifesto | 38s | $6.84 | `docs/KEEL_SCORECARD.md` |
| Seventeen | Founder origin story | 42s | $6.08 | `docs/SEVENTEEN_SCORECARD.md` |
| The Sunday Problem | Customer testimonial | 36s | $7.88 | `docs/ROTA_SCORECARD.md` |
| The Sunday Problem (revised) | Customer testimonial, clarified | 44s | $5.10 | `docs/CREW_SCORECARD.md` |

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

It defaults to `data/library` if unset.
