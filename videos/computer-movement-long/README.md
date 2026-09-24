# Longer computer movement studies

Three single-take image-to-video sequences from the previously generated source stills. No real movement video, extracted real frame, or motion-control input enters generation. Reference observations inform text only. See BRIEF.md, SHOT_PLAN.md, source-reviews.json and reference-observations.json.

Delivered durations are 15s desktop, 15s mouse, and 9s laptop. Each has varied task activity. Laptop is a continuous selection from its third 15-second take, excluding later sustained hand hovering. No loops or time stretching. Desktop uses keyboard navigation because there is no mouse in its source scene. Mouse/keyboard transfer was retained. Laptop trackpad-transfer attempts failed; the final prompt uses simpler nearby-key editing. All are provisional realism studies with documented limits.

Budget continuity: budget-continuity.json carries every prior sample charge into its matching cumulative $10-per-video ledger. Historical runs mirrored from the earlier shared batch must not be counted twice. All failed/uncertain/revised charges remain reserved. Do not resume the old batch for new requests; use these cumulative per-video roots. Do not delete a ledger or change its cap.

Generation is complete. The following commands resume the same first-round IDs without duplicate paid submissions; later rounds are in configs/computer_long_01_round2.json, computer_long_03_round2.json and computer_long_03_round3.json:

```sh
PYTHONPATH=src .venv/bin/python scripts/run_library_loop.py configs/computer_long_01_round1.json --evaluate
PYTHONPATH=src .venv/bin/python scripts/run_library_loop.py configs/computer_long_02_round1.json --evaluate
PYTHONPATH=src .venv/bin/python scripts/run_library_loop.py configs/computer_long_03_round1.json --evaluate
```

Local build (no paid calls): `.venv/bin/python videos/computer-movement-long/build.py`. Check and render each named subproject at its native frame rate, then run deliver.py. The final comparison page links the source still, selected MP4 and full generated original. Exact requests, upload URLs, IDs and costs remain in the persistent ledgers.

These are qualitative tests without matched no-reference controls. They cannot isolate a causal effect of movement-reference observations.

Final files: `artifacts/final_outcome/computer-movement-long/` with `review.html` comparison. Audit: `review_notes/computer-movement-long-generation-audit.md` and JSON. Run `update_reviews.py`, then `PYTHONPATH=src .venv/bin/python videos/computer-movement-long/refresh_learning.py` to refresh evidence without double-counting mirrored historical queue IDs.
