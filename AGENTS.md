# Amarillo video production defaults

These are the user's standing instructions for every new video-generation request
in this repository. Apply them without requiring the user to repeat them. An
explicit current user request wins wherever it conflicts with these defaults.
An inspection, plan-only request, or targeted edit does not authorize an unrelated
new production.

## Ownership and authorization

- Own the creative and technical decisions. Choose the concept treatment, script,
  shot plan, models, tools, and implementation; state useful assumptions briefly.
  Ask only for a genuine blocker, such as an essential missing fact or asset,
  inaccessible required service, or an unavoidable budget conflict. Do not ask
  the user to select models, tools, technical approaches, or intermediate options.
- A request for a finished video authorizes generation, revisions, assembly, and
  final rendering within the budget below. Continue through final MP4 delivery.
  Do not require storyboard, stage, or final-render approval unless the user
  explicitly requests approval checkpoints. Internal reviews remain mandatory.
- Start with the installed `hyperframes` skill and its selected workflow, usually
  `product-launch-video` or `general-video`. For a new production, record
  `flow: automation`, `storyboard: no`, and this standing authorization in
  `BRIEF.md`, unless the user requests otherwise. A requested storyboard deliverable
  or approval checkpoint must still be honored.
- This standing user preference supplies the autonomy and render authorization
  sought by generic skill intake/review gates, including the final
  "preview first, or render?" question. Follow the skills' technical contracts
  and quality checks without reopening those permission questions. Existing
  subproject instructions still govern composition mechanics.

## Research and planning

- Before planning, review relevant videos from the existing reference library.
  Use `src/amarillo/library.py` and `scripts/inspect_library_slice.py`; library
  discovery uses `AMARILLO_LIBRARY_DIR`, `data/library`, or prior manifests as
  documented in `README.md`. Inspect the actual relevant footage and pacing;
  contact sheets and existing analyses support this review. If media is missing,
  report the limitation and use available evidence rather than claiming a review.
- Apply relevant `analysis_notes/`, `review_notes/`, `docs/*SCORECARD.md`, production
  runbooks, and `prompt_library/tested_*_patterns.json`. Consult
  `artifacts/learning/latest.json` and refresh cross-loop evidence with
  `scripts/learn_from_loops.py` when needed. Use `docs/AUTOMATED_VIDEO_LAB.md` for
  the evidence and review workflow. Recent relevant failures and user corrections
  take precedence over older successful examples or static model recommendations.
- Consider the relevant techniques already reviewed in
  `docs/VIDEO_PROMPTS_TOPIC_REVIEW.md`, `docs/ROUND8_RESEARCH_AND_LEARNINGS.md`, and
  `docs/CREW_REALISM_REPORT.md` from https://github.com/topics/video-prompts.
  Apply useful prompting, physical-action, and continuity techniques selectively;
  respect their recorded provenance and licenses. A new scrape or wholesale
  installation of external skills is not required for each video.
- Treat supplied concepts, scripts, dialogue, and shot plans as inspiration unless
  explicitly locked/verbatim. Preserve required facts, product claims, and stated
  constraints; improve wording, pacing, visuals, and structure where useful.
  Do not invent product capabilities or unsupported claims. Record the adapted
  direction and any locked material in the brief/script.

## Shot routing and people

- Choose tools and models per shot. Consider Fal.ai and other available providers
  appropriate to the shot, using `src/amarillo/shot_plan.py`,
  `src/amarillo/learning.py`, and compatible reviewed evidence where applicable.
  Verify current endpoint capabilities and inputs before use. A catalog entry or
  provider's default model is a candidate, not a mandate. An unsupported route
  calls for a bounded test or a supported alternative.
- Use HyperFrames or deterministic rendering for accurate UI, typography,
  captions, product screens, and text-heavy scenes. Follow the installed
  composition skills instead of asking generative footage to render exact text.
- For generated scenes involving people, generate a source image first and
  internally review it before image-to-video. An exception needs a strong reason
  documented in the shot plan, such as an already suitable supplied reference.
  Establish identity, pose, gaze target, hands, and object contact in the still;
  retain the reviewed reference and its provenance for subsequent shots.
- Review every generated shot, including chronological motion and useful close-ups,
  not only a representative still or successful API response. For people, check
  hands, gaze, posture, object interaction, anatomy, facial realism, identity
  consistency across shots, and obvious AI artifacts; check speech/lip sync when
  applicable. Carry forward Serein/Sideway/Portion lessons: attractive faces do
  not compensate for failed gaze, staged posture, or implausible interaction.
- Reject weak takes. Revise the source image or prompt, regenerate, reroute,
  simplify the action, or select a genuinely usable segment within the remaining
  budget. Record the failure and revision hypothesis. Do not accept a take merely
  because generation succeeded, or regenerate an already good take reflexively.
  Prioritize final quality over the number of shots, attempts, or models used.

## One $10 budget per video

- The total ceiling is **USD $10 per video**, across all providers, source images,
  video, voice/audio, retries, failed or uncertain paid attempts, and revisions.
  Continue the same video's cumulative ledger across rounds and sessions; never
  reset it or split providers into independent $10 budgets. Only an explicit user
  instruction may change the ceiling.
- Verify expected cost before paid generation whenever possible, using current
  provider quotes and the actual duration, resolution, and audio settings. Record
  the quote, USD estimate, and reservation before submission. Provider credits
  require a documented USD conversion; do not treat unknown cost as zero. If cost
  cannot be bounded conservatively, use a costed/local alternative or report the
  blocker before spending. This project explicitly requests cost estimation even
  when a provider skill normally omits it.
- Use `scripts/run_library_loop.py` and its shared `budget_root` for Fal rounds;
  reuse `src/amarillo/budget.py` reservations, including its 15% buffer. Reserve
  non-Fal image/audio/tool allowances in the same ledger before those calls, without
  presenting them as Fal video evidence. Reconcile actual charges when available;
  distinguish estimates, reservations, and confirmed spend in the delivery report.
- Follow `docs/AUTOMATED_VIDEO_LAB.md` for preflight, persisted queue IDs, resumption,
  and duplicate-request protection. Use `--evaluate` for generated outputs. The
  legacy `amarillo` CLI still needs `--live`; this standing authorization permits
  the agent to pass it within the cap, without another user approval. Dry runs are
  useful validation, not the finished deliverable. Never bypass budget checks or
  raise the cap automatically. Preserve enough budget for useful correction rounds;
  if funds run short, simplify or reroute without silently lowering quality gates.

## Finish, verify, and deliver

- Use the installed workflow's assembly, captions, transitions, audio, and finishing
  procedures. Load `hyperframes-core`, `hyperframes-animation`, `media-use`,
  `hyperframes-audio`, and `hyperframes-cli` as required by that workflow; their
  detailed implementation instructions remain the source of truth.
- Run required composition checks, inspect timing and scene joins, and fix failures.
  Review the encoded final MP4 for picture, readable text, caption/audio alignment,
  sound quality, continuity, and the ending. Use relevant existing verification
  scripts and decode/metadata checks; technical success does not prove realism.
- Save prompts, selected/rejected takes, review findings, costs, and limitations in
  the existing production records. Update applicable scorecards, reusable prompt
  learnings, and routing evidence; refresh the legacy artifacts when that pipeline
  was used. Keep untested dimensions null and subjective judgments labeled.
- Follow the existing layout: editable projects in `videos/<name>/` (or an existing
  `hyperframes/<name>/` project), final media in `artifacts/final_outcome/<name>/`,
  delivery manifests in `assembled_outputs/`, and durable reviews in `review_notes/`
  and `docs/`. Preserve source media and the repository's media-exclusion policy.
  Deliver a clickable final MP4 path, editable project path, cost summary, and any
  material limitations. Do not stop at a plan, storyboard, preview, or loose shots
  when the user requested a finished video.

## Demo Videos workspace

`demo-videos/` is a separate Tesseract editing workspace for the product demo
videos. For any work inside it, follow `demo-videos/AGENTS.md` instead of the
Amarillo production defaults above.
