# Three library-inspired samples: H3, Veo, Kling and HyperFrames

Seven new generations, three final edits, one shared $10 ledger.

Agent subjective visual review of eight chronological full-frame samples per new take, actual decoded joint frames, local Whisper base.en transcripts and full decode. No independent audio listening, audience study, exhaustive frame-by-frame anatomy review or calibrated perceptual scoring. Lip sync, accent fidelity and voice identity remain unmeasured. Pixel MAE measures closeness at a specific cut, not general visual quality. Faces are untreated.

Scores average four equally weighted criteria. Compare within use case only.
One generation per condition. The two H3 interview requests hold prompt, seed, reference, duration and resolution fixed; only provider expansion changes, but backend nondeterminism may remain. Cross-model resolution, expansion and seed semantics differ. Compare scores only within the use case and audio/reference mode.

| Run | Role | v | Score / 10 | Dimensions | Estimate | Seconds | Used |
| --- | --- | ---: | ---: | --- | ---: | ---: | :-: |
| `interview_h3_concise` | interview | 1 | 7.0 | 1344x768 | $0.36 | 58.31 | - |
| `ugc_h3_one_action` | ugc | 1 | 8.0 | 1344x768 | $0.36 | 60.21 | yes |
| `product_h3_pullback` | product_ad | 1 | 8.5 | 1344x768 | $0.36 | 341.71 | yes |
| `interview_h3_no_expansion` | interview | 2 | 6.75 | 1344x768 | $0.36 | 340.47 | - |
| `ugc_veo_one_action` | ugc | 1 | 7.62 | 1280x720 | $0.90 | 84.6 | - |
| `product_h3_paired` | product_continuation | 2 | 8.88 | 1344x768 | $0.30 | 87.31 | - |
| `product_kling_paired` | product_continuation | 2 | 9.25 | 1904x1088 | $0.56 | 181.9 | yes |

## Detailed criteria

N/T means not tested, not zero. These are subjective sampled-frame scores; a single-shot identity score does not establish consistency across shots.

| Criterion | interview_h3_concise | ugc_h3_one_action | product_h3_pullback | interview_h3_no_expansion | ugc_veo_one_action | product_h3_paired | product_kling_paired |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| human realism | 7 | 7.5 | N/T | 7 | 8 | N/T | N/T |
| face realism | 7 | 7.5 | N/T | 7 | 8 | N/T | N/T |
| hand body movement | N/T | 7.5 | N/T | N/T | 7 | N/T | N/T |
| identity consistency | 8 | 8 | N/T | 7.5 | 8.5 | N/T | N/T |
| product accuracy | N/T | N/T | 8.5 | N/T | N/T | 9 | 9 |
| text ui accuracy | N/T | N/T | N/T | N/T | N/T | N/T | N/T |
| camera movement | 8.5 | 9 | 8.5 | 8 | 9 | 9 | 9.5 |
| cinematic quality | N/T | N/T | 8 | N/T | N/T | 8 | 8.5 |
| transition quality | N/T | N/T | N/T | N/T | N/T | 9 | 9.5 |
| entry exit continuity | N/T | N/T | N/T | N/T | N/T | 9 | 9.5 |
| context clarity | N/T | 8 | N/T | N/T | 8 | N/T | N/T |
| product message clarity | N/T | N/T | N/T | N/T | N/T | N/T | N/T |
| prompt adherence | 6.5 | 7.5 | 8.5 | 6.5 | 6.5 | 9 | 9.5 |
| consistency | 8 | 8 | 8.5 | 7.5 | 8.5 | 9 | 9.5 |

## What Changed This Loop

Added H3 to actual local evidence; tested its prompt expansion, native speech, one-gesture UGC, physical product pullback and paired endpoints. Used a reviewed H3 exit frame to start both H3 and Kling continuations. Added explicit native-audio intent to plan validation, automatic speech evaluation and routing, plus a schema-checked H3 interview adapter. New final edits demonstrate scene-specific model choices and exact authored UI.

## Routing After This Loop

| Shot type | Route to | Selected run | Caution |
| --- | --- | --- | --- |
| interview | Veo 3.1 Fast image-to-video, existing reviewed take | `reused realism_line4_v2` | H3 delivered words but not restrained performance. Neither H3 take replaces the incumbent; sampled review does not establish lip sync. |
| ugc | H3 image-to-video for this casual creator sample | `ugc_h3_one_action` | Provisional single-take selection. Gesture starts earlier than requested; a long gap separates sentences. Skin remains somewhat smooth. Veo remains a candidate for higher-detail faces. |
| product reveal | H3 image-to-video from reviewed object reference | `product_h3_pullback` | Simple rigid object and slow camera motion only. No hand interaction, CAD-level fidelity or complex physics established. |
| product continuation | Kling 3.0 Pro image-to-video with paired identical endpoints | `product_kling_paired` | Best measured boundary match in this two-output trial. This is a settled product shot; it does not establish moving-character continuity. |
| exact ui | HyperFrames 0.8.35 | `-` | Authored illustrative interfaces, exact text and timing. It cannot synthesize realistic people. |

## Observations

### `interview_h3_concise` - 7.0/10
Both product sentences transcribe correctly, ending at 6.26s. Broad smiles, several closed-eye expressions and eyebrow changes conflict with restrained direction. Reference bakery, apron and recognizable face remain in sampled frames. Native output is 1344x768 at 24fps, with container duration 6.592s despite requesting 6s. A correct transcript is not proof of lip sync. Reject for this restrained interview, not all possible H3 people shots.

### `ugc_h3_one_action` - 8.0/10  **selected**
Correct new hook line, ending at 5.10s. Clear palm-up gesture and recognizable starting face; warm smile changes into a rueful expression. Gesture starts in the first sentence rather than the requested second; the 1.42s transcript gap slows the hook. Hands return by the end. Sampled visible hand shape is plausible; fast finger transitions and lip sync are unmeasured. Selected 0–5.5s for this casual concept; do not advertise it as indistinguishable from real footage.

### `product_h3_pullback` - 8.5/10  **selected**
Single button, indicator, ivory rim and cylindrical body remain coherent in sampled frames. Camera pulls back and creates left-side space. The reviewed 5.5s frame has a usable settled composition; the preceding frame differs by 0.69 RGB MAE/255. Source image comes from an earlier Kling-generated fictional object, not a real product design. Selected for the reveal and as the continuation reference.

### `interview_h3_no_expansion` - 6.75/10
Provider returned expanded_prompt=null, confirming no expanded text was returned for this setting. Same requested line transcribes through 6.28s. Broad smiles, eyes squeezed closed and visible leaning remain; the toggle did not repair the target performance in this paired trial. Do not repeat unchanged. A next human test should change observable performance direction or use the incumbent, rather than buy another expansion toggle.

### `ugc_veo_one_action` - 7.62/10
Same full prompt, reference and line as H3. Correct transcript ends at 5.14s; native 1280x720 at 24fps. More visible facial texture, but a conspicuous raised hand on screen right (her left) instead of the requested right hand, plus stronger squinting and gestures. Retain as an alternate, not the preferred restrained-action take for this sample. The modest subjective face-detail advantage does not establish a universal human-realism winner.

### `product_h3_paired` - 8.88/10
Actual previous-shot exit used for both input endpoints. Stable stationary object and low middle-frame drift in this simple case. Boundary RGB MAE 2.1308/255; mean-luma shift 1.5995/255. Cheaper continuation candidate ($0.30 estimated) than Kling; slight boundary tone change remains. Exact repeated endpoints do not imply all intermediate frames are identical.

### `product_kling_paired` - 9.25/10  **selected**
Same continuation prompt and reviewed endpoints as H3, audio disabled. Boundary RGB MAE 1.3293/255 and luma shift 0.9340/255; first-to-middle MAE 0.9039. Main geometry, shadow and composition appear stable in sampled frames. Selected for final product film because this measured joint is closer. No complex motion or human identity transfer tested.

## Findings

- H3 native audio works for the tested lines; speech evaluation and routing must not depend solely on a generate_audio flag that this endpoint lacks.
- H3 2K/4K modes upscale a 768P base according to the live schema. Requested 768P is the appropriate economical screening mode; paying more for upscaling would not test new underlying detail.
- The expansion toggle did not fix the interview performance. Keep the failed condition and its prompt in memory and stop repeating it.
- A reference role should be explicit: identity for people, geometry for objects, and the actual decoded exit frame for a continuation.
- Kling continuation's 1.33/255 boundary MAE is much lower than restarting the unrelated macro composition (39.67/255). This is a diagnostic baseline, not a randomized experiment proving all paired-frame transitions improve by that ratio.
- Every final uses local HyperFrames text and UI. Music begins after speech, and the original faces are not retouched.
- No new third-party skills were installed from the video-prompts topic. Selected planning techniques were tested in the current workflow; unproven repository marketing does not affect model scores.

## Budget

Estimated generation total: $3.20. Conservative reserved total: $3.72. Hard cap: $10.00.
7 reserved requests; 7 completed; 0 failed or uncertain. No automatic retries.
This loop has its own ledger at `artifacts/library-loop-8/budget.json`; it is the persistent cost record and deleting it defeats the cap guard. Provider invoice not queried.

