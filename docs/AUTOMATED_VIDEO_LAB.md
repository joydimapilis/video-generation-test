# Automated video lab

The existing library analyses and finished films remain the foundation. This
extension joins the previously separate experiment ledgers and reviews into one
evidence library, adds compatible-shot routing, and closes a budget resume bug.

The mandatory new-request research gate and per-video completion gate are in
[CORE_VIDEO_WORKFLOW.md](CORE_VIDEO_WORKFLOW.md). Review the configured general
library before shot planning. Each final MP4 needs a separate adjacent
`<mp4-stem>.reverse-engineering.md`; finalizers reject missing or stale documents.

## People scenes and Phase 2 movement references

Normal production follows **source image → internal image review → image-to-video
→ motion review** for generated scenes involving people. Establish identity, pose,
gaze, hands and object contact in the still before animating it; retain the reviewed
image and provenance. Document any justified exception in the shot plan, as required
by `AGENTS.md`. Review every generated take and revise weak images or motion within
the same video's budget.

The human-movement library in `references/human-realism/` is reserved for separate
Phase 2 evaluation and improvement of human realism. Studying those clips, selecting
movement ranges, comparing against them or using them for conditioning is not a
default generation step. Keep the clips and historical reviews available for that
phase. General video reference research, prior production learnings and normal
realism checks still apply; source-image generation does not depend on this library.

## Run and resume

```sh
.venv/bin/python scripts/run_library_loop.py configs/interview_models_round1.json --dry-run
.venv/bin/python scripts/run_library_loop.py configs/interview_models_round1.json --evaluate
.venv/bin/python scripts/learn_from_loops.py --route interview --reference --audio
```

The live command is authorized by the attached task's request to run experiments.
It uses the plan's `budget_root`, refuses a conflicting `--root`, refuses caps above
$10, preflights the whole batch, and keeps failed/uncertain charges reserved.
The 15% reserve is an estimation buffer, not a verified invoice or provider-side
spending limit. Keep the ledger: deleting it destroys the spend history.
The same endpoint/input cannot be resubmitted under a new ID in the same loop;
a changed prompt or reference is a new experiment and must have a recorded hypothesis.
Concurrent reservations still enforce the cap under a filesystem lock.

`--evaluate` decodes completed outputs, extracts frames, transcribes dialogue
locally, and refreshes learning. A saved qualitative review is required before
new footage affects routing. Metadata, transcription and sampled images cannot
prove natural blinking, lip sync, hand movement, or audience response.
When polling reaches its deadline, rerun the same command; persisted queue IDs
resume without another paid submission. No cron or unattended unlimited spend
loop is installed.

## Evidence and routing

`artifacts/learning/latest.json` combines all `library-loop*/budget.json` records
with their evidence and scorecards. It carries every requested visual dimension,
with `null` for untested dimensions, and preserves prompts, settings, costs,
latency, successes, rejections and provider failures.

Use `artifacts/learning/core.json` for normal production decisions. It excludes
Phase 2 research from both routing and prompt memory. The complete `latest.json`
history is retained and archived before refresh. Previously recorded rows with
unavailable ledgers remain historical-only rather than disappearing.
Whole-take `selected`, `accepted`, and `approved` decisions are compatible with
`accept` and `provisional`, without rewriting original labels. Rejected,
superseded and segment-only takes stay available as lessons, not whole-take
endorsements. Recommendations include compatible success/failure findings under
`lessons`; unavailable or unverified media never acquires a verified score.

The router compares only the same use case, image-conditioning mode, and requested
audio mode. It averages the same four historical criteria, excludes rejected or
unverified footage, deduplicates identical attempts, and records supporting run
IDs. These provisional averages are not calibrated human-realism scores; scene
difficulty, resolution, and prompt revision still vary. An unsupported category
returns `needs_test`. Exact UI, typography and captions route to HyperFrames.

`route_shot` can read the resulting evidence file; absent an evidence file, its
legacy routes remain available for old projects. `adapt_interview_input` explicitly
handles different image fields and duration formats. A new endpoint requires its
own validated adapter and a fresh cost quote before live use. A route is a quality
candidate, not authorization to reuse another model's price.

The older `amarillo` CLI still supports reference ingestion and its initial smoke
test workflow. Its live path now also caps at $10, recomputes line-item costs,
imports historical failed and completed attempts into a persistent reservation
ledger, and refuses implicit retries. Use the bounded runner above for new
multi-round experiments because it also persists queue IDs and resumes downloads.

## Review procedure

For each new output, inspect the source, early/middle/late frames, motion and
speech where possible. Record a decision, scored dimensions, method, limits and
concrete findings in the loop scorecard. Refresh learning afterward. Keep
unsupported scores null and distinguish a single-shot identity observation from
identity continuity across multiple shots. Reject unclear product explanations
or use an explicit explanatory UI insert; never infer context from the filename.

The prompt memory retains each tested prompt with its finding and evidence.
Successful prompts are provisional templates; rejected versions are retained so
future revisions target a known failure. Nothing scraped from GitHub is installed
automatically. See `VIDEO_PROMPTS_TOPIC_REVIEW.md` for source and license decisions.

The current reusable templates are in `prompt_library/tested_interview_patterns.json`.
Each includes the tested endpoint, evidence, observed failure, and limitations.

## Round 8: H3 and three new sample edits

H3 native audio has no `generate_audio` input switch. Plans may now declare
`audio_requested: true` outside `input`; validation, speech evaluation and learning
preserve that intent without sending an unsupported parameter to the provider.
This describes requested sound, not proof that the output contains good speech.
Older plans retain their existing behavior. The H3 interview adapter validates
5–15-second duration and selects native `768P`.

```sh
# Resume existing jobs without resubmitting or charging again.
.venv/bin/python scripts/run_library_loop.py configs/h3_samples_round1.json --evaluate
.venv/bin/python scripts/run_library_loop.py configs/h3_samples_round2.json --evaluate
.venv/bin/python scripts/run_library_loop.py configs/h3_samples_continuity.json --evaluate

# Local evaluation → stored review → learned routing; no paid calls here.
.venv/bin/python scripts/evaluate_round8_joins.py
.venv/bin/python scripts/report_loop.py --root artifacts/library-loop-8 --review review_notes/h3_samples.json --out docs/H3_SAMPLES_SCORECARD.md
.venv/bin/python scripts/learn_from_loops.py --route ugc --reference --audio
.venv/bin/python scripts/build_round8_samples.py
```

All three plans share `artifacts/library-loop-8/budget.json`: **$3.20 estimated,
$3.72 reserved**, maximum $10. The review file rejects both H3 interview takes for
overacting, so the router retains Veo for that use case. The new H3 UGC result and
Kling continuation are provisionally selected in their compatible cohorts.

The local selection manifest chooses exact source ranges for the three samples.
Building never makes paid requests. Run HyperFrames checks after rebuilding and
render the three named projects only within the user's authorized task. Then run
`verify_round8_samples.py`; it checks source hashes, decoded video, expected
frames, isolated speech audio and live preview URLs.

The current batch stops at final-video review. This is a resumable agent-driven
loop with automated accounting, generation retrieval, technical evaluation and
routing; it is not a scheduled daemon claiming it can judge all human realism
without review. Future changes should respond to recorded failures, remain in the
same ledger for this experiment, and never relabel identical failed requests.
