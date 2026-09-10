# Operating Runbook

## Default Policy

- Do not spend Fal credits unless a run plan has an explicit budget cap and the command uses `--live`.
- Prefer variant-level tests over one-off full-prompt tests.
- Treat generated video text and app UI as temporary unless HyperFrames replaces it deterministically.
- After any new run or review-note edit, run `.venv/bin/python -m amarillo.cli refresh-artifacts`.

## New Sample Workflow

```bash
.venv/bin/python -m amarillo.cli ingest --samples data/samples
.venv/bin/python -m amarillo.cli analyze
.venv/bin/python -m amarillo.cli build-prompts
.venv/bin/python -m amarillo.cli plan-runs --include-variants --max-estimated-cost 2.00
.venv/bin/python -m amarillo.cli run-fal --run-plan artifacts/run_plans/latest.json --live --max-estimated-cost 2.00
.venv/bin/python -m amarillo.cli refresh-artifacts
```

## Current Decision Rules

- Use `kling_2_6_pro_i2v` for source-anchored launch hooks and checkout proof shots.
- Use `kling_3_pro_t2v` for full reward-app montage candidates.
- Use `wan_2_1_t2v` for cheap alternate-direction exploration.
- Use `krea_wan_14b_t2v` for cheap static product/app scene exploration.
- Use HyperFrames for deterministic UI, text, counters, claims, captions, end cards, and final assembly.

## Review Order

1. Open `artifacts/review_pack/latest.html` for the compact human review set.
2. Watch `artifacts/outputs/cero_overlay_hyperframes.mp4` first because it is the best assembled review artifact.
3. Use the review pack's suggested decision as the default label unless the video clearly feels wrong.
4. Use `artifacts/reference_comparisons/latest.md` to see automated reference-similarity triage.
5. Use `artifacts/reports/latest.html` for a broad all-output visual pass.
6. Use `artifacts/knowledge/latest.json` when an AI model needs the full evidence base.

## Quality Thresholds

- Strong candidate: final score >= 75 and technical score >= 90.
- Useful exploration: final score >= 60.
- Reject or isolate failure mode: final score < 60, high blank risk, severe subject drift, unreadable generated UI, or confusing action.
- Reference similarity >= 80 is a strong automated match, but manual semantic notes override it when a model copies the visual signature while missing the actual story.

## Next Technical Milestones

1. Add more reference samples from different shot families.
2. Add AI vision analysis for frames/clips when a vision API key is available.
3. Add reviewer labels to the review pack HTML.
4. Add retrieval over prompt patterns for better brief matching.
5. Add automated side-by-side video grids for finalist comparison.
