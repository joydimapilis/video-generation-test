# Model review and reusable techniques — 12 September 2026

This run extends the earlier [model review](MODEL_REVIEW_2026-09-12.md),
[topic repository review](VIDEO_PROMPTS_TOPIC_REVIEW.md), and actual local tests.
It adds **seven paid requests across H3, Veo and Kling**, then three HyperFrames
samples. It is a bounded screening run, not an exhaustive benchmark of every
currently advertised video model.

## Current model evidence

| Model / tool | Evidence available | Strength in this workspace | Weakness / preferred use | Cost basis |
|---|---|---|---|---|
| MiniMax H3 I2V | Five new successful requests: two interviews, one creator, one reveal, one continuation | Correct short speech, anchored rigid object, inexpensive screening | Interview overacting persisted with and without expansion; occasional long speech gaps; no tested multi-shot human identity or voice consistency | Native 768P: $0.06/s; $0.30–$0.36 per requested shot |
| Veo 3.1 Fast I2V | One new UGC comparison plus prior interview tests | Provisional interview incumbent; more visible facial texture in the new creator comparison | Wrong requested hand and stronger squint/gesture in this UGC take; reference alone does not enforce acting | New six-second audio-on test: $0.90 |
| Kling 3.0 Pro I2V | One new paired-endpoint continuation plus two earlier interviews | Closest measured product join here; reference-guided geometry | Earlier interview speech was correct but gaze and expression were imperfect; no cross-shot voice result here | New five-second silent shot: $0.56 |
| HyperFrames 0.8.35 | Three newly authored and checked compositions | Exact task fields, scheduling state, captions and reproducible scene timing | Depends on authored content and supplied footage; cannot repair source facial performance | $0 new generation API fees; local compute and engineering effort excluded |
| Grok Imagine 1.5 | Existing first-loop UGC take | Keep prior creator screening evidence | No new run or current-price comparison in this pass | Historical ledger only |
| LTX 2.3 | Existing UGC, interview and landscape takes | Useful historical low-cost baseline | Prior two-person/speech limitations remain; no new result for newer LTX families | Historical ledger only |
| Seedance 2.5 | Existing product T2V result; prior rejected interview I2V | Product evidence is distinct from face-input eligibility | Do not repeat the rejected face request; no new quality result | Historical ledger; no new charge |
| Hailuo 2.3, Gemini Omni and other new catalog entries | Provider documentation only in this pass | Candidates for targeted future tests | Not routed as winners without local output evidence | No paid tests in this run |

The provider's H3 overview emphasizes 2K, but the **live endpoint schema** says
480P and 768P are native and 2K/4K upscale a 768P base. We chose 768P accordingly.
The API returned 1344×768, 24fps. Six requested seconds produced a 6.592s container;
five requested seconds produced 5.184s. Use probed duration and word timings in
edits, not the request duration. Reservations retain 15% headroom, including
rounding. Actual account invoicing was not queried.

Sources checked for this run: [H3 pricing](https://fal.ai/models/minimax/h3/image-to-video),
[H3 live schema](https://fal.ai/api/openapi/queue/openapi.json?endpoint_id=minimax/h3/image-to-video),
[H3 overview](https://fal.ai/minimax-h3),
[Veo Fast endpoint](https://fal.ai/models/fal-ai/veo3.1/fast/image-to-video),
[Kling Pro endpoint](https://fal.ai/models/fal-ai/kling-video/v3/pro/image-to-video),
[Hailuo 2.3 endpoint](https://fal.ai/models/fal-ai/minimax/hailuo-2.3/standard/image-to-video),
[Google Veo](https://deepmind.google/models/veo/).
Exact H3 schemas and provider-expanded prompts are frozen in
`artifacts/library-loop-8/research/`.

## What transferred from the prompt repositories

The requested [video-prompts topic](https://github.com/topics/video-prompts) was
revisited. The existing detailed repository review remains the shortlist;
no repository was installed merely because it appeared there.

- **Small action contract and controlled change:** [Reviral's advanced guide](https://github.com/Reviral-ai/awesome-kling-prompts/blob/main/PROMPTS-ADVANCED.md) motivates separating action, camera, protected properties and endpoint. We tested one gesture for the creator and a single pullback for the product. The product worked; neither creator model followed the gesture timing perfectly. This validates a useful planning constraint, not the repository's superiority.
- **Observable performance cues:** [ai-visual-skills' performance module](https://github.com/sundny8/ai-visual-skills/blob/main/skills/seedance-director/references/physics-microexpression.md) is relevant to skin, gaze and movement. Our restrained interview contract still produced overacting on H3. More facial instructions or removing expansion did not earn a new default. Keep this technique conditional and review the actual output.
- **Persistent scene state:** [the short-film project planner](https://github.com/jnMetaCode/ai-shortfilm-prompts/blob/main/templates/project-planner.md) supports recording identity, props, camera and handoff state. Here a decoded exit, not a verbal promise, became both endpoint images for the continuation. Our own reusable implementation saves source hashes, timestamp, selected image, requested state and measured joint.

These are independently authored adaptations of general techniques. Existing
third-party attribution remains in `docs/third-party/`. No repository's tests
of prompt text are counted as evidence of rendered realism.

## Human realism rules after the tests

Use a reviewed, naturally lit identity reference before recurring human shots.
Preserve existing skin variation, age and asymmetry rather than requesting an
ideal face or adding arbitrary imperfections. Pick one gaze target and one
motivated action. Review shoulders, hand direction, blink samples, sleeve folds,
and the return to a settled pose. Preserve hair and clothing in the reference;
these still-air takes do not establish realistic wind or walking motion.

For interviews, use the reviewed Veo route for now. H3 is a provisional casual
creator alternative, not a demonstrated general winner for people. Both H3
interview variants stay rejected for this restrained-use-case cohort. Native
speech availability is not a reason to assume natural lip sync or stable voices.
The reusable memory records successful and failed prompts with those limits.

## Continuity result and limits

The actual 5.5s frame of the H3 product reveal was reviewed, hashed, and supplied
as the starting and ending image for two continuations. The edit ends the first
shot at 5.5416667s, so that reviewed frame is its last displayed frame at 24fps.
The first decoded continuation frame differs from the outgoing frame by:

| Continuation | RGB MAE / 255 | Mean-luma shift / 255 | First → middle MAE / 255 |
|---|---:|---:|---:|
| H3, paired images | 2.1308 | 1.5995 | 1.1997 |
| Kling, paired images | 1.3293 | 0.9340 | 0.9039 |
| Restarting the earlier macro composition (diagnostic mismatch) | 39.6676 | 7.5741 | — |

Kling is selected for the product film. The low scores indicate close pixels in
this simple settled shot, not a population-level quality improvement. Uniform
960×540 analysis resizing normalizes dimensions; final render uses a consistent
1920×1080 viewport. Geometry, shadow, light direction and subject position were
also reviewed in the actual frames. No skin treatment, color correction,
interpolation or dissolve hides this source join. The text change at the cut is
intentional. Human cross-shot continuity and complex camera handoffs remain
separate questions.

## Next useful tests

Stop this batch at final-video review. Reusing the current plans submits zero
new requests. Future paid attempts must keep this ledger if they continue this
experiment and be priced before submission; do not reset it to gain budget.

The most informative next human experiment is a simpler positive performance
cue with a quieter starting expression, tested against the same Veo reference.
Do not repeat the failed expansion toggle. For moving subjects, use a real exit
frame plus velocity/direction review; the settled product result is not evidence
that those harder joins will work. Continue exact UI and text in HyperFrames.

## HyperFrames audio finding

The first creator render advanced the source speech by 32 ms when using the
32 kHz AAC MP4 directly as the audio source. FFT alignment recovered a 0.9991
source correlation at a -512-sample offset (16 kHz analysis). The first mono analysis also appeared
over full scale because the float downmix added gain; the actual stereo source
was within range. The final builder decodes the source once
into a 48 kHz WAV, applies only linear gain to leave 0.8 peak headroom, and keeps
the original picture timing. Source and derived hashes and the gain are saved.
Final verification requires zero-offset speech correlation above 0.98 and decoded
stereo audio below full scale. This repairs transport alignment and level; it does
not claim to repair the model's lip sync.
