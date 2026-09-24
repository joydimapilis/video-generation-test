# New computer movement studies — batch 02

Three new images and new image-to-video animations. This project does not reuse source images or takes from the preceding batch. The supplied real videos were reviewed for behavioral cues only: no real clip or extracted frame was uploaded to a model or used as final media.

- `BRIEF.md`, `SHOT_PLAN.md`: direction and standing authorization.
- `reference-observations.json`: observed motion, clip/time ranges, hashes, limits and per-sample application.
- `source-image-plan.json`, `source-reviews.json`: exact new-image requests and pre-animation review.
- `pricing.json`: settings-specific quote and initial cost plan.
- `selection.json`: final reviewed selections, source hashes and durations.
- `../../review_notes/computer-movement-studies-02.json`: full attempt review, including failures.
- `../../artifacts/library-loop-computer-movement-studies-02/budget.json`: persistent shared $10 budget, reservations, provider IDs and request payloads. Never reset on resumption.

Local-only rebuild from repository root:

```sh
.venv/bin/python videos/computer-movement-studies-02/build.py
npx hyperframes check videos/computer-movement-studies-02/01-desktop-reading
npx hyperframes check videos/computer-movement-studies-02/02-mouse-work
npx hyperframes check videos/computer-movement-studies-02/03-laptop-typing
# Render each selected subproject with --fps 24 --quality delivery to its named final MP4.
.venv/bin/python videos/computer-movement-studies-02/deliver.py
```

Resume the generation runner with the same plan and IDs, never a relabeled duplicate:

```sh
PYTHONPATH=src .venv/bin/python scripts/run_library_loop.py configs/computer_movement_studies_02_round1.json --evaluate
PYTHONPATH=src .venv/bin/python scripts/run_library_loop.py configs/computer_movement_studies_02_round2_mouse.json --evaluate
PYTHONPATH=src .venv/bin/python scripts/run_library_loop.py configs/computer_movement_studies_02_round2_typing.json --evaluate
PYTHONPATH=src .venv/bin/python scripts/run_library_loop.py configs/computer_movement_studies_02_round3_typing.json --evaluate
PYTHONPATH=src .venv/bin/python scripts/run_library_loop.py configs/computer_movement_studies_02_round4_reading.json --evaluate
```

Completed jobs are retrieved without new paid submissions. Source generation similarly resumes `generate_sources.py`; source-image entries are kept separate from video-routing evidence. Final media, original generated takes and source stills are in `artifacts/final_outcome/computer-movement-studies-02/`; open `review.html` for side-by-side viewing. Generated media and runtime caches are excluded from Git, while prompts and production records remain durable text.

No causal reference-improvement claim: there are no matched no-reference controls. The external mouse action is an application hypothesis, not an action directly demonstrated by the supplied clips. No speech, exact UI or cross-shot identity test.

Desktop delivery is a 1.5-second supported reading-pause selection; sustained desktop hand realism remains unresolved. Both other samples retain full six seconds. Full untrimmed generated originals are linked alongside the selections.
