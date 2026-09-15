# Model and prompt review: September 12, 2026

This pass rechecked the live Fal endpoint documentation and the requested
[video-prompts topic](https://github.com/topics/video-prompts), then extended the
existing tests. It is a current candidate review, not an exhaustive claim to have
benchmarked every model on the market.

| Candidate | Documented capability and price checked this pass | Actual local evidence |
| --- | --- | --- |
| Kling 3.0 Pro I2V | Native English/Chinese audio, start/end images, optional character elements. $0.168/s with audio, $0.112/s without. | Two new 6s, 1080p, 24fps interview takes. Both transcribe correctly; performance control remains imperfect. |
| Seedance 2.5 I2V | Fixed 4–30s duration, optional ending image, audio and resolution controls. Approximately $0.473/s at 720p; token-based billing. | This reference rejected with HTTP 422; no new quality evidence. Earlier T2V product test remains separate evidence. |
| Veo 3.1 Fast I2V | Current Fal image-conditioned endpoint with audio options. | Reused existing 6s, 1080p interview baseline and prior scorecards; no new charge. |
| HyperFrames 0.8.35 | Installed renderer, confirmed current pin; exact authored text and media placement. | New 24s comparison, zero check findings, 30/30 contrast checks, verified source audio order. |

Sources: [Kling schema](https://fal.ai/models/fal-ai/kling-video/v3/pro/image-to-video/api),
[Kling pricing](https://fal.ai/models/fal-ai/kling-video/v3/pro/image-to-video),
[Seedance schema](https://fal.ai/models/bytedance/seedance-2.5/image-to-video/api),
[Seedance pricing](https://fal.ai/models/bytedance/seedance-2.5/image-to-video),
[Veo endpoint](https://fal.ai/models/fal-ai/veo3.1/fast/image-to-video).

The historical notes' claim that Veo is the only catalog model with lip-synced
speech is incorrect as a capability rationale: Kling also supports native audio.
This pass demonstrates correct spoken text with Kling. It does not establish
lip-sync quality from transcription. Veo remains the provisional route because
of the saved reviewed evidence, not a unique speech feature.

The other families already tested in this workspace include Grok Imagine 1.5,
LTX 2.3, Seedance 2.5 T2V, and older Kling/Wan baselines. Preserve their actual
use-case results; do not retroactively claim new tests or updated prices for them.
MiniMax H3 and Gemini Omni remain untested candidates from the earlier research.
See [earlier model research](LIBRARY_LOOP_RESEARCH.md) and
[the new scorecard](INTERVIEW_MODEL_SCORECARD.md).

The repository shortlist and selective technique imports are already documented
in [the repository review](VIDEO_PROMPTS_TOPIC_REVIEW.md). This pass rechecked
[Reviral's Kling recipes](https://github.com/Reviral-ai/awesome-kling-prompts) and
[the short-film planner](https://github.com/jnMetaCode/ai-shortfilm-prompts).
The useful principle is to specify the action, protected appearance, camera and
settled ending. Our next test shortened the inherited contract to observable
performance instructions after the first take overacted. It improved speech
onset and sampled pose control, but shortened delivery and left a long tail.
This finding is specific to these unseeded takes; it is not evidence that a
shorter prompt universally improves realism. No additional repository or skill
was installed from the topic.
