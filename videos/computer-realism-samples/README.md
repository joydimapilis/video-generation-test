# Computer realism samples

Three independent silent image-to-video studies: 4-second typing, 1.25-second trackpad contact/tap and 1.5-second side-view typing. User-supplied movement references are translated into observed behavioral cues in prompts; they are not direct video conditioning or identity inputs. No causal improvement claim without matched no-reference controls.

Read BRIEF.md, SHOT_PLAN.md, source-reviews.json, the source-image plan and exact per-shot prompts. Selection and review findings are in selection.json and ../../review_notes/computer-realism-samples.json. All attempts share ../../artifacts/library-loop-computer-realism/budget.json; keep that ledger when resuming.

From repository root:

```sh
# Local rebuild from retained reviewed takes (no paid generation)
.venv/bin/python videos/computer-realism-samples/build.py
npx hyperframes check videos/computer-realism-samples/01-typing
npx hyperframes check videos/computer-realism-samples/02-trackpad
npx hyperframes check videos/computer-realism-samples/03-side-typing
# Render each named project at 24 fps, delivery quality, to artifacts/final_outcome/computer-realism-samples/<name>.mp4.
.venv/bin/python videos/computer-realism-samples/deliver.py
```

Generation resumption uses `PYTHONPATH=src .venv/bin/python scripts/run_library_loop.py configs/computer_realism_round3.json --evaluate`. These plans reuse persisted queue IDs. Source-image resumption uses generate_sources.py from repository root. Do not delete or reset budget records; uncertain calls require reconciliation, not resubmission.

All generated video/stills, asset copies and runtime caches are excluded from Git. Prompts, code, brief, selection, cost and review manifests are durable text records. No synthetic music, captions, color grade, skin filter, speed change or interpolation is added.

The third sample is deliberately trimmed to 0–1.5s because the full take develops an unnatural curled-hand pose. Rejected full takes remain in artifacts/library-loop-computer-realism/outputs. The final trackpad attempt resumes via configs/computer_realism_round4_trackpad.json.

The trackpad full take also fails after approximately 1.3s; selected duration is 1.25s. The comparison player links all three untrimmed four-second generated takes so trimming cannot conceal failures.
