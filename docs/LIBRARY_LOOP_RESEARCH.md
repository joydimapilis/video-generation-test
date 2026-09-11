# Library-Inspired Sample, September 11, 2026

Second loop (ORRIN, a dark industrial hardware film from a different library slice):
`docs/ORRIN_SCORECARD.md`. It re-measured Veo with audio disabled and found $0.10/s
at 1080p, which changes the cost comparison recorded below for any silent shot.

Third loop (KEEL, a narrated brand manifesto from the Aurus/Beyond-Reach slice):
`docs/KEEL_SCORECARD.md`. It bought 60 seconds of footage for a 38-second film so
weak plates could be dropped rather than used, and added local Kokoro narration,
a three-act cut rhythm and three distinct transition languages.

## Scope and Cost
One original concept video, five sampled video model families plus HyperFrames.
This is a small practical workflow study, not a statistically valid model ranking.
Seven initial requests use three identical UGC prompts, two identical product
prompts, one interview test, and one exact-UI stress test. Follow-up prompts must
respond to observed problems. No automatic paid retries. Persistent reservations
include 15% headroom and unknown/failed requests. Absolute cumulative cap: $10.
Local compute, existing assistant subscription and cloud storage costs are not
API-generation charges. Provider estimates are not an account invoice.

## Reference Observations
347 MP4s discovered; six stratified examples inspected through eight sampled
frames each. Full technical probes and contact sheets are under
`artifacts/library-loop/references`. This is not a claim to have watched all 347.

| Reference | Observed pattern | Transfer to new concept |
| --- | --- | --- |
| Motion-5 | playful hook, white UI walkthrough, multi-step result | explicit task state changes |
| Content Rewards | line-led reveal, three short verbs, contrast flip, CTA | three-beat language, dark-to-light progression |
| Pocket introduction | presenter at desk, macro hardware inserts, feature text | human hook into physical recorder |
| SupersonikAI | problem title, UI closeups, benefit sequence | one focused screen, one visible result |
| Tarun Amasa announcement | two seated speakers alternating with actual spreadsheet | test two-person turn-taking; route exact data to renderer |
| Cluely customer support | dialogue-driven cross-cut ad, contrasting locations | emotional hook, but avoid complex dialogue in final |

The original Cue concept combines these structural patterns without copying
people, product logos, soundtrack, exact script or unsupported success claims.

## Current Model Research
Checked official Fal endpoint pages, schemas and pricing. Model catalog changes
quickly; “current” means verified on this date, not exhaustive latest coverage.

| Tool | Reason to test or research | Pricing basis / source |
| --- | --- | --- |
| Veo 3.1 Fast | native dialogue, short natural performance | [Fal](https://fal.ai/models/fal-ai/veo3.1): $0.15/s with audio at 720p |
| Grok Imagine 1.5 | current xAI video family, creator speech | [Fal](https://fal.ai/models/xai/grok-imagine-video/v1.5/text-to-video): $0.14/s at 720p; reserve rounding |
| LTX 2.3 Pro | inexpensive 1080p dialogue and interview baseline | [Fal](https://fal.ai/models/fal-ai/ltx-2.3/text-to-video): $0.08/s; live pricing API confirms. Marketing table also says $0.06; use higher quote. |
| Kling 3.0 Pro | camera direction, product geometry, exact-UI stress test | [Fal](https://fal.ai/learn/tools/seedance-2-0-vs-kling-3-0): $0.112/s without audio |
| Seedance 2.5 | newest verified ByteDance endpoint, native long takes | [Fal](https://fal.ai/models/bytedance/seedance-2.5/text-to-video): roughly $0.473/s at 720p; 4s only, never auto duration |
| HyperFrames 0.8.34 | exact UI/type/timing, local editing and assembly | installed CLI and skills; $0 marginal generation API cost, engineering effort excluded |
| MiniMax H3 | research-only: multimodal references, 2K, edit workflow | [Fal](https://fal.ai/minimax-h3); provider claims not measured here |
| Gemini Omni | research-only: conversation-driven video editing | [Fal](https://fal.ai/gemini-omni); reserve for a later funded edit test |

Seedance 2.5's 30-second full-generation capability would exceed this budget at
720p, so this experiment deliberately buys short reusable shots. HyperFrames is
a deterministic renderer, not a photorealistic generative model; compare roles,
not a single blended “winner” across incompatible workloads.

## Measurement Rules
Local review dependencies: `pip install -e '.[video-review]'`, FFmpeg/FFprobe,
Node/npm, Chrome, and HyperFrames 0.8.34. Whisper downloads its base.en weights
once, then transcribes locally without a paid API call.

Preserve prompt, endpoint, settings, request ID, latency, output, technical probe,
sampled frames and local speech transcript. Agent aesthetic scores are subjective
and explicitly labelled. Do not equate resolution with fidelity, transcription
with lip-sync, or a valid decode with good video. Untested categories remain N/T.

## Ideas
1. **Cue / Make room for the idea:** human problem, pocket recorder, exact task
   transformation, calm close. Selected and produced: covers three tested roles
   naturally. Final render: `artifacts/final_outcome/cue/cue-final.mp4`.
2. **Launchroom / From brief to launch:** whiteboard or voice becomes a scene plan.
   Mostly HyperFrames; optional short presenter. Lowest generation dependency.
3. **After the call:** two founders explain how decisions become actions, cut to
   real software. Requires stronger turn-taking evidence and a real product brief.
4. **Pocket / Ship it before you forget it** and **Signal / Three verbs, one flip**
   were written after the loop, once the routing evidence existed.

Ideas 2-4 are specified scene by scene, with the routed model and the exact prompt
for each shot, in `docs/LIBRARY_LOOP_CONCEPTS.md` (generated by
`scripts/build_concept_slate.py` from `prompt_library/concept_slate.json`). None of
them has been generated: $0.34 remains under the $10 cap and the cheapest concept
estimates at $0.75.
