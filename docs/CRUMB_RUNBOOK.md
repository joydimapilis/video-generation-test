# Crumb run / resume

One bounded run consists of the four frozen plans below. Every plan declares
`artifacts/library-loop-9` as its budget root. The ledger reserves all 12 requests
at $5.92 against the $10 cap, including rejected takes. Do not delete or reset it.
All requests are complete. Resuming these same plans is retrieval/evaluation,
with zero new submissions. This is an agent-driven test/evaluate/learn/improve
loop that stops at final review, not an unattended spending daemon.

```sh
.venv/bin/python scripts/run_library_loop.py configs/crumb_round1.json --dry-run
.venv/bin/python scripts/run_library_loop.py configs/crumb_h3max.json --dry-run
.venv/bin/python scripts/run_library_loop.py configs/crumb_round2.json --dry-run
.venv/bin/python scripts/run_library_loop.py configs/crumb_return.json --dry-run
```

Replace `--dry-run` with `--evaluate` to retrieve/evaluate persisted jobs. A fresh
run on another checkout must restore the ledger and generated artifacts first;
otherwise those commands can submit paid requests. In particular, the follow-up
plans require the actual reviewed exit images from this run, not a substitute
frame. No automatic paid retries are allowed. H3 Max promotional prices expire
September 14, 2026; re-quote before a future new request.

Source selection lives in `assembled_outputs/crumb_samples.json`, with its working
copy under the experiment root. All final MP4 source entries begin under
`artifacts/library-loop-9/outputs/`. Generic fonts and staging helpers may be reused.
Rebuild uses only existing local assets and never buys another generation:

```sh
.venv/bin/python scripts/build_crumb_samples.py
npx hyperframes check hyperframes/crumb-customer
npx hyperframes check hyperframes/crumb-baker
npx hyperframes check hyperframes/crumb-morning
npx hyperframes render hyperframes/crumb-customer -f 24 -q high -w 2 -o artifacts/final_outcome/crumb/crumb-customer.mp4
npx hyperframes render hyperframes/crumb-baker -f 24 -q high -w 2 -o artifacts/final_outcome/crumb/crumb-baker.mp4
npx hyperframes render hyperframes/crumb-morning -f 24 -q high -w 2 -o artifacts/final_outcome/crumb/crumb-morning.mp4
.venv/bin/python scripts/verify_crumb_samples.py
```

For modified compositions, refresh the JSON checks used by verification:
`npx hyperframes check hyperframes/crumb-customer --json > artifacts/library-loop-9/check-customer.json`
(and the baker/morning equivalents). Verification checks decoding, duration,
source lineage, peaks, zero-offset speech correlation and the actual product joint.

Review notes → scorecard → automatic routing and prompt memory:

```sh
.venv/bin/python scripts/evaluate_crumb_joins.py
.venv/bin/python scripts/report_loop.py --root artifacts/library-loop-9 --review review_notes/crumb.json --out docs/CRUMB_SCORECARD.md
.venv/bin/python scripts/learn_from_loops.py
```

The automatic router compares compatible use case, reference and audio modes.
`artifacts/library-loop-9/route-decisions.json` freezes the current-run recommendations.
Global learning also retains older cohorts. Rejected prompts are preserved in
`prompt_library/tested_crumb_patterns.json`; the next paid test should state the
specific failure it changes. Accuracy dimensions without measurements stay null.

Final-review entry point: `artifacts/final_outcome/crumb/review.html`. Editable
Studio previews run on local ports 3032, 3033 and 3034. The final films are not
published to an external service.
