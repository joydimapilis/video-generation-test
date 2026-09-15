# Crew: interview model and prompt screening

Two new Kling takes, one failed Seedance request, and a reused Veo baseline.

Agent subjective scores from 12 chronological face crops and eight full-frame samples per take, plus local Whisper base.en transcripts and full decode. No independent audio listening, calibrated perceptual model, audience test, or exhaustive motion review. Hand anatomy and lip sync are unmeasured. Context score refers to a six-second insert, not the complete Crew film.

Scores average four equally weighted criteria. Compare within use case only.
One new take per condition. Different models do not share seed semantics; Kling has no exposed seed. Prompt revision effects are confounded with stochastic variation.

| Run | Role | v | Score / 10 | Dimensions | Estimate | Seconds | Used |
| --- | --- | ---: | ---: | --- | ---: | ---: | :-: |
| `interview_kling3_contract` | interview | 1 | 8.25 | 1920x1080 | $1.01 | 185.18 | yes |
| `interview_seedance25_contract` | interview | 1 | N/T | N/T | $2.84 | N/T | - |
| `interview_kling3_restrained` | interview | 2 | 8.5 | 1920x1080 | $1.01 | 144.1 | yes |

## Detailed criteria

N/T means not tested, not zero. These are subjective sampled-frame scores; a single-shot identity score does not establish consistency across shots.

| Criterion | interview_kling3_contract | interview_seedance25_contract | interview_kling3_restrained |
| --- | ---: | ---: | ---: |
| human realism | 7.5 | N/T | 7.5 |
| face realism | 7.5 | N/T | 7.5 |
| hand body movement | N/T | N/T | N/T |
| identity consistency | 8 | N/T | 8.5 |
| product accuracy | N/T | N/T | N/T |
| text ui accuracy | N/T | N/T | N/T |
| camera movement | 9 | N/T | 9 |
| cinematic quality | 8 | N/T | 8 |
| transition quality | N/T | N/T | N/T |
| entry exit continuity | N/T | N/T | N/T |
| context clarity | 6 | N/T | 6 |
| product message clarity | 8 | N/T | 8 |
| prompt adherence | 8 | N/T | 8.5 |
| consistency | 8 | N/T | 8.5 |
## Routing After This Loop

| Shot type | Route to | Selected run | Caution |
| --- | --- | --- | --- |
| interview with identity | Veo 3.1 Fast image-to-video remains provisional incumbent | `reused realism_line4_v2` | Native speech is also available in Kling. Retention is based on current reviewed evidence, not a unique audio capability. |
| concise alternative | Kling 3.0 Pro image-to-video, concise observable blocking | `interview_kling3_restrained` | Trim listening tail. No cross-shot voice or identity consistency tested. |
| exact ui | HyperFrames | `-` | Product names, schedules and mechanics remain deterministic. |
| seedance face reference | Do not repeat this rejected request | `-` | Provider rejected reference; visual quality is N/T. |

## Observations

### `interview_kling3_contract` - 8.25/10  **selected**
Native speech transcribes the full product sentence correctly. Stable bakery, apron and recognizable face in sampled frames; the face is smoother than the Veo baseline. The gaze travels sideways and a shoulder lift conflicts with the restrained-performance instruction. Speech begins at 1.26s and ends at 5.32s. Product named, availability mechanism stated, but this isolated line does not establish the pain or final benefit. Useful comparison take, not enough evidence to replace Veo.

### `interview_seedance25_contract` - None/10
Provider returned HTTP 422 content_policy_violation for the supplied generated face reference; no output, no visual quality scores. No retry or workaround attempted. Full estimated reservation retained; charge settlement unknown.

### `interview_kling3_restrained` - 8.5/10  **selected**
The shorter prompt produces the correct product sentence from 0.00 to 3.48s, followed by a long closed-mouth listening tail. The sampled shoulders and gaze are more settled; raised eyebrows remain early in the sentence. Skin remains smooth and the 2.5-second tail is too long for a six-second ad beat. Prefer trimming around 3.75s for an insert; retain full output in the comparison. This is a promising blocking repair, not proof of better human realism.

## Findings

- Speech onset improved from 1.26s to 0.00s in the revised Kling take, but delivery shortened to 3.48s and leaves a long listening tail.
- Both Kling takes deliver the complete product line. Transcript correctness does not prove lip sync or accent fidelity.
- Detailed human/face scores are subjective single-shot observations; hands, UI accuracy and join continuity remain null.
- HyperFrames comparison keeps original audio isolated by take and leaves colors, framing and skin untreated.

## Budget

Estimated generation total: $4.86. Conservative reserved total: $5.61. Hard cap: $10.00.
3 reserved requests; 2 completed; 1 failed or uncertain. No automatic retries.
This loop has its own ledger at `artifacts/library-loop-7/budget.json`; it is the persistent cost record and deleting it defeats the cap guard. Provider invoice not queried.

