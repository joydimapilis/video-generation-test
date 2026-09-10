# Long-Term Plan

## North Star

Build a mostly automated system that studies reference videos, extracts reusable creative patterns, tests those patterns across video-generation models, and learns which model/tool is best for each shot type and use case.

The project should eventually let an AI model inspect the prompt library, prior outputs, costs, and scoreboards, then select, adapt, or combine the strongest approaches for a new brief.

## Default Product Decisions

- Primary use case: short-form product, marketing, and social video clips.
- Prompt strategy: prioritize reusable pattern extraction over exact recreation.
- Interface: local CLI first; lightweight review dashboard later.
- Evaluation: combine automated technical checks, structured model notes, and human review.
- Budget: dry-run by default, live generation only with explicit command flags and cost caps.
- Safety: capture style/structure/motion patterns without cloning protected characters, exact copyrighted ads, private brands, or identifiable people.

## Phases

### Phase 1: Foundation

- Create a repo structure for samples, prompt patterns, run plans, outputs, and reports.
- Build video ingestion with `ffprobe` metadata and keyframe extraction.
- Define a prompt-pattern schema that separates reusable attributes from sample-specific facts.
- Seed a current Fal model catalog with known strengths, limitations, costs, and required inputs.
- Add run planning, spend estimation, dry-run logging, and Markdown reporting.

### Phase 2: Better Reverse Engineering

- Add AI vision analysis for frames and clips when an API key is available.
- Extract structured dimensions: subject, action, camera motion, shot scale, lighting, art direction, transitions, pacing, overlay/text behavior, audio intent, and negative constraints.
- Generate multiple prompt variants per pattern: faithful recreation, reusable template, cross-domain adaptation, and model-specific prompt.
- Add embedding/search over the prompt library so new briefs can retrieve related patterns.

### Phase 3: Model Benchmarks

- Run small batches across cheap/fast models first.
- Escalate winning prompts to premium models only when the expected value is clear.
- Track latency, estimated cost, errors, prompt adherence, temporal coherence, subject stability, artifact level, and commercial usefulness.
- Build model-selection rules from evidence, not assumptions.

### Phase 4: Review System

- Produce compact review packs and broader galleries grouped by prompt pattern and model.
- Compare outputs to reference samples with automated visual-signature metrics.
- Let reviewers mark “usable,” “needs iteration,” or “reject,” with short reason codes.
- Feed review labels back into the scoreboard and selector.
- Add generated summary reports at each milestone.

### Phase 5: Adaptive Prompt Selection

- Given a new use case, retrieve similar prompt patterns and prior winning runs.
- Select a model/tool by shot type: text-to-video, image-to-video, effect preset, lip-sync, HyperFrames composition, or hybrid.
- Compose a run plan that balances quality, speed, budget, licensing, and controllability.
- Generate final prompt packets for the selected model/tool.

## Model And Tool Roles

- Text-to-video models: ideation, scene generation from briefs, broad style exploration.
- Image-to-video models: product, character, or brand consistency from a source frame.
- Preset effect models: repeatable social effects and transformations.
- Lip-sync/audio-to-video models: dialogue-driven clips and localization.
- HyperFrames: deterministic layout, typography, overlays, captions, compositing, edit structure, and repeatable rendered packages.

## Milestones

1. Foundation CLI and schemas are in place.
2. First real sample batch is ingested and prompt patterns are generated.
3. First dry-run model matrix produces a costed run plan.
4. First live Fal batch generates videos under a small cap.
5. First scoreboard identifies model strengths by shot type.
6. Prompt selector recommends a model and prompt for a new brief.
7. Review pack and reference comparison reduce manual file inspection.
8. Review dashboard adds persistent labels and finalist side-by-side comparison.

## Evidence Standard

Every milestone should leave behind artifacts:

- Input sample manifest.
- Prompt patterns and variants.
- Model run plan with cost estimate.
- Raw model result logs.
- Downloaded output videos when live runs are used.
- Scoreboard with reasoning.
- Technical evaluation and reference comparison.
- Compact review pack for nontechnical judgment.
- Markdown report suitable for nontechnical review.
