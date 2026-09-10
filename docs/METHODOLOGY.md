# Methodology

## Prompt Reverse Engineering

Each reference video is analyzed into two layers:

- Sample-specific facts: visible subject, exact props, brand marks, setting, or text.
- Reusable pattern: shot structure, camera grammar, pacing, lighting, transition design, motion technique, prompt constraints, and failure modes.

The prompt library should preserve the reusable pattern and treat sample-specific facts as replaceable slots.

## Scoring Dimensions

- Prompt adherence: did the output follow the requested action, camera move, and style?
- Temporal coherence: do objects remain stable over time?
- Motion quality: is movement intentional rather than smeared or random?
- Subject fidelity: does the subject remain recognizable when using references?
- Artifact level: anatomy, text, faces, edges, physics, compression, or warping issues.
- Commercial usefulness: would this be usable in a real draft or campaign?
- Cost efficiency: useful quality per dollar.
- Latency: time to result.
- Reusability: does the prompt pattern transfer to different subjects/use cases?
- Reference similarity: automated visual-signature closeness to the sample using luminance, contrast, motion, aspect, resolution, and duration alignment.

## Model Selection Heuristics

- Use low-cost models for wide prompt exploration and failure discovery.
- Use premium cinematic models for finalist prompts, native audio, or complex motion.
- Use image-to-video when subject consistency matters.
- Use text-to-video when generating scenes from scratch.
- Use preset-effect endpoints when repeatability matters more than open-ended control.
- Use HyperFrames for deterministic edits, titles, captions, overlays, compositing, and any output that must be exactly repeatable.

## Review Artifacts

- Use `artifacts/review_pack/latest.html` for the human shortlist.
- Use `artifacts/reference_comparisons/latest.md` for automated source-vs-output triage.
- Use `artifacts/evaluations/latest.md` for technical health checks such as resolution, blank-frame risk, and motion.
- Use `artifacts/knowledge/latest.json` as the AI-readable evidence bundle for future prompt selection.

## Safety Rules

- Do not build prompts that copy a specific copyrighted ad shot-for-shot.
- Do not clone identifiable people without permission.
- Avoid brand names unless the supplied source is owned or explicitly allowed.
- Record uncertainty in analysis instead of inventing details.
