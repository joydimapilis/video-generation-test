**Video prompt repository review — 12 September 2026**

Recommendation: test selected parts of jnMetaCode/ai-shortfilm-prompts, sundny8/ai-visual-skills, and Reviral-ai/awesome-kling-prompts first. LichAmnesia/awesome-ad-video-prompts and rediumvex/ai-video-generator-claude are useful second-wave candidates. Improve the planning and continuity layer of Amarillo while retaining its existing generation and finishing workflow.

This is a source and integration review, not a rendered-video benchmark. I screened all 42 listings across the topic's [first](https://github.com/topics/video-prompts), [second](https://github.com/topics/video-prompts?page=2), and [third](https://github.com/topics/video-prompts?page=3) pages. I inspected repository pages for 15 candidates and downloaded file inventories and selected source files for 12. Stars were not used as a selection criterion. No external skills were installed, no repository programs were executed, and no paid generations were submitted.

**What matters for Amarillo**

The workspace already contains a Python/Fal experiment runner, JSON prompt patterns, spending controls, review notes, and HyperFrames finishing. Recent Crew/ROTA work uses Veo 3.1 Fast for interviews; earlier experiments use Kling and Wan. The general model catalog does not fully represent those later project-specific routes. See [README](../README.md), [Crew scorecard](CREW_SCORECARD.md), and [ROTA scorecard](ROTA_SCORECARD.md).

The existing scorecards support reusing a reference frame for subsequent dialogue takes, but explicitly describe small trials rather than statistically reliable comparisons. Preserve those findings as our baseline.

In [prompts.py](../src/amarillo/prompts.py), the generic fallback infers patterns from metadata and filename hints; richer analyses depend on supplied notes. The general prompt builder mostly joins text fields. It does not enforce a structured relationship between one shot's end and the next shot's start. [planning.py](../src/amarillo/planning.py) selects a source keyframe, and [fal_runner.py](../src/amarillo/fal_runner.py) uploads one local image into an image/start-image field. Neither provides a general local-file upload workflow for paired endpoints and multiple character references.

This is a practical integration gap: a phrase such as “keep the same face” is an instruction, while supplying the appropriate reference images gives the model additional visual information. Fal's [Kling 3 Pro image-to-video API](https://fal.ai/models/fal-ai/kling-video/v3/pro/image-to-video/api) exposes start/end images, character/object elements, and separate shot prompts. Supporting these fields would be a focused extension to our current Fal workflow. It does not guarantee continuity.

**The five repositories worth testing**

| Priority | Repository | Main contribution | Workflow stage | Decision | Pilot integration effort |
|---|---|---|---|---|---|
| 1 | [jnMetaCode/ai-shortfilm-prompts](https://github.com/jnMetaCode/ai-shortfilm-prompts) | Structured cinematic prompts, camera vocabulary, project continuity worksheet | Planning and prompt construction | Use selected MIT materials | Low–medium: adapt templates and map fields |
| 2 | [sundny8/ai-visual-skills](https://github.com/sundny8/ai-visual-skills) | Physical action, facial behavior, persistent character/scene state | Performance direction and continuity | Use selected reference modules | Medium: translate/adapt rules and remove fixed defaults |
| 3 | [Reviral-ai/awesome-kling-prompts](https://github.com/Reviral-ai/awesome-kling-prompts) | Small, controlled action chains with camera and endpoint instructions | Individual Kling shots and review | Use as a baseline recipe set | Low: convert a few examples into existing variants |
| 4 | [LichAmnesia/awesome-ad-video-prompts](https://github.com/LichAmnesia/awesome-ad-video-prompts) | Structured ad prompt data with timed material/light/action details | Product footage and cinematic finish | Use a small curated subset | Low: JSON field mapping plus editorial cleanup |
| 5 | [rediumvex/ai-video-generator-claude](https://github.com/rediumvex/ai-video-generator-claude) | Testimonial, avatar, and luxury direction | Human close-ups and commercial presentation | Selective second-wave test | Low–medium: translate platform references and separate overlays |

Effort ratings are engineering judgments for a pilot, excluding paid render time. Installing text files is easier than integrating their behavior reliably.

**1. jnMetaCode/ai-shortfilm-prompts**

The useful components are the five-part prompt structure, the camera-move library, and the [project planner](https://github.com/jnMetaCode/ai-shortfilm-prompts/blob/main/templates/project-planner.md). Together they help specify who appears, how the scene looks, what the camera does, and how shots connect. The planner records recurring subjects, common visual treatment, and entry/exit states.

Our first adaptation should turn those planning fields into reusable shot records. Keep camera moves optional and motivated by the scene. The skill's mandatory camera/lens names and camera “breathing” are hypotheses to test, not universal requirements. There is also an internal inconsistency: the planner's right-exit example asks for right-entry, while the narrative template suggests left-entry for continued rightward movement. Store screen position and travel direction separately.

Its [automated evaluations](https://github.com/jnMetaCode/ai-shortfilm-prompts/blob/main/evals/README.md) score generated prompt text with an LLM; they do not measure generated faces or transitions. The [NOTICE](https://github.com/jnMetaCode/ai-shortfilm-prompts/blob/main/NOTICE) separates MIT-authored templates/skills from archived Mx-Shell prompts marked all rights reserved. Import only the appropriate MIT portion, retaining attribution.

**2. sundny8/ai-visual-skills**

This has particularly relevant modules for [continuity](https://github.com/sundny8/ai-visual-skills/blob/main/skills/seedance-director/references/consistency.md) and [physical action and micro-expressions](https://github.com/sundny8/ai-visual-skills/blob/main/skills/seedance-director/references/physics-microexpression.md). It distinguishes character, environment, and prop references, and explicitly carries changed states into later shots. For example, an opened door or wet sleeve should remain that way.

For human realism, it describes preparation, contact, and reaction, rather than only naming an action. Facial direction uses observable behavior. Our test should compare restrained cues against current prompts; adding too many small gestures could create overacting.

Use these modules as an editing pass over shot plans. Do not inherit the skill's fixed 30-second/vertical/8K defaults or mandatory dramatic structure. Those are authoring preferences, not evidence of endpoint capabilities. The repository's validation checks skill structure and references, not video realism. Its MIT license and modular text format make selective adaptation practical.

**3. Reviral-ai/awesome-kling-prompts**

The compact library describes action direction, physical cause and effect, camera behavior, and a final pose. Image-to-video examples distinguish what should move from what should remain fixed. This closely fits our current Kling use.

Its [advanced workflow](https://github.com/Reviral-ai/awesome-kling-prompts/blob/main/PROMPTS-ADVANCED.md) adds a continuity card and a sequence of experiments that change one factor at a time. It also calls for reviewing endpoint quality and keeping settings and references with the selected take.

Use it first for a person turning, a short walking shot, and a product reveal. It can improve camera readability and provide useful edit points. It does not generate or enforce matching frames automatically, and the reviewed materials do not establish a measured quality advantage. Its simplicity is a strength for controlled tests.

**4. LichAmnesia/awesome-ad-video-prompts**

The [JSON library](https://github.com/LichAmnesia/awesome-ad-video-prompts/blob/main/prompts.json) contains 52 entries grouped into sections, with prompt text, duration, aspect ratio, and tags. This is convenient for our existing JSON-based patterns.

Its strongest contribution is specific material and lighting behavior: how reflections move, fabric responds, liquid lands, and a product settles into its final composition. Use selected recipes to improve product inserts and supporting footage.

Some prompts compress several difficult actions into six or eight seconds and request exact logos or labels. Simplify those sequences and keep exact text/UI in our finishing layer. The repository includes still illustrations; those do not demonstrate temporal quality. The [license](https://github.com/LichAmnesia/awesome-ad-video-prompts/blob/main/LICENSE) explicitly permits adaptation and commercial use with attribution. No HeyDreaming migration is needed to test the prompt text.

**5. rediumvex/ai-video-generator-claude**

This offers ten text-based skills written around Seedance on Higgsfield. The avatar, testimonial, and luxury modules are the most relevant. The [avatar source](https://github.com/rediumvex/ai-video-generator-claude/blob/main/skills/09-ai-avatar/SKILL.md) discusses gaze, skin detail, asymmetry, small movements, and how environmental light falls on the person.

Use selected performance/lighting cues to test human close-ups on our existing models. Model transfer is an experiment; support for a coding assistant does not make the prompts universally effective on video models.

Avoid adopting the entire suite. It includes long timed sequences, generated typography, metrics, and UI requests that conflict with our established finishing approach. Reference markers also need translation into actual provider inputs. “Studio quality” and social-performance statements in the README are promotional claims, not a controlled benchmark.

**Other useful repositories, with limits**

| Repository | What it does and where it could help | Recommendation and integration difficulty |
|---|---|---|
| [yinxiaowai/awesome-ai-video-transition-prompts](https://github.com/yinxiaowai/awesome-ai-video-transition-prompts) | Transition templates covering matching shapes/actions/directions, objects covering the lens, gaze, focus, and other techniques; repository includes 24 MP4 examples. Useful for designing the outgoing and incoming images together. | Study first, rather than import. Its [license](https://github.com/yinxiaowai/awesome-ai-video-transition-prompts/blob/main/LICENSE) says all rights reserved and learning/reference; it does not provide a clear broad commercial grant. Low effort to study; medium to build our own paired-shot tests. The inspected README does not provide complete per-example model/settings provenance. |
| [fanchengchen1-collab/super-director](https://github.com/fanchengchen1-collab/super-director) | Detailed directing system with staging, lighting, shared visual rules, and a substantial entry/exit-frame chapter. Particularly relevant to planning continuity before generation. | Reference study only for now. Its [CC BY-NC-ND terms](https://github.com/fanchengchen1-collab/super-director/blob/main/LICENSE.md) limit commercial reuse, though it also describes internal use allowances. Advanced face anchoring, performance, and QA modules are listed as outside the open edition. Medium–high effort to integrate the whole system; unnecessary for the first trial. |
| [xxjrq/seedance-minimax-prompts](https://github.com/xxjrq/seedance-minimax-prompts) | Python prompt compilers, structured project/shot/reference schemas, validators, and model-specific examples. Could improve consistent conversion of shot plans into provider requests. | Consider later as an architectural reference. Current validators target Seedance 2.5 and MiniMax H3, not our main Kling/Veo routes. Medium–high effort to extend and wire into Fal. Tests check specifications and compiled text, not visible continuity. A free-text continuity note is not a continuity validator. |
| [Reviral-ai/awesome-hailuo-prompts](https://github.com/Reviral-ai/awesome-hailuo-prompts) | Camera-command and physical-motion recipes with stable endings. Improves shot movement and end composition if we test Hailuo. | Defer until that model is a deliberate benchmark candidate. Low effort for prompt adaptation; additional endpoint validation needed. Much of its advanced process overlaps the Kling sibling. |
| [pbwheel/tt-design](https://github.com/pbwheel/tt-design) | Plans tangible-material animation, such as clay, paper, and ink, including opening/ending image prompts. Could help stylized inserts and transformation sequences. | Use only for a future stylized brief. Low–medium integration effort. Locked-camera material animation has limited relevance to human realism and moving-camera continuity. Prefer separate endpoint images when the API offers separate fields. |
| [quanluo/ltx-video-prompts](https://github.com/quanluo/ltx-video-prompts) | Small recipes for camera movement, performance, products, and audio. Useful as simple comparison prompts. | Low effort but low incremental value. Inspected recipes explicitly say they are drafts that were not independently generated. The associated LTX.dev site describes itself as an independent multi-model platform; this is not evidence from the LTX model developer. |
| [Hanyuyu/visual-prompt-feed](https://github.com/Hanyuyu/visual-prompt-feed) | Searchable prompt records with source authors, categories, and media links. Could expand the reference-discovery stage. | Later: medium effort for a filtered, provenance-preserving importer. It is a discovery feed, not a quality-tested continuity system; original prompt/media rights are marked NOASSERTION. |
| [8TrafficAI/viral-videos-prompts](https://github.com/8TrafficAI/viral-videos-prompts) | Finds short-video references and converts their structure into prompts. | Defer. It targets content research and traffic evidence; we already have a reference-ingestion workflow. Medium integration effort for limited direct help with faces or frame joins. |
| [ofoxai/awesome-seedance-2.5](https://github.com/ofoxai/awesome-seedance-2.5) | A gallery separating provider-run, official, and community cases; provider-run entries include job-linked costs. Useful if evaluating Seedance as a separate model experiment. | Browse later. Low effort for reference study; medium for reproducing supported cases through our provider. The sourcing is more useful than raw prompt count, but still not a controlled comparison against our existing models. |
| [gracech0322-cmd/seedance-2-prompt-library](https://github.com/gracech0322-cmd/seedance-2-prompt-library) | README-centered Seedance prompt gallery with linked examples. | Inspiration only. Low effort to browse; no reusable implementation or evaluation system found in the inspected file tree. |

Other topic listings were screened at the listing level, not individually audited. Model launch galleries, sales/trend collections, ASMR examples, and the ComfyUI-specific plugin were lower priorities given our current Fal pipeline and quality goals. No model migration is recommended on the basis of a repository title or provider marketing.

**How the shortlist covers the goals**

| Goal | Best starting point | Additional work needed in Amarillo |
|---|---|---|
| Human realism | ai-visual-skills; selective avatar direction | Compare movement and interaction in full playback, not just still frames |
| Prompt quality | ai-shortfilm-prompts; Kling recipes | Store structured fields; remove contradictory or unsupported directions |
| Consistency across shots | Shared project records and state inheritance | Reuse approved reference images and track persistent scene/prop changes |
| Camera movement | Kling recipes; camera-move library | Specify start/end framing, direction, pace, and what must remain visible |
| Entry/exit frames | Project planner; Kling continuity cards | Support paired reference uploads and save selected cut frames |
| Smooth transitions | Original match-action/occlusion tests informed by transition study | Plan both sides of a join and review motion speed, position, lighting, and sound |
| Cinematic quality | Shared lighting/look rules; curated ad recipes | Apply a consistent finish and select usable takes |

An image match alone is insufficient: the two clips may match at one frame while motion pauses or accelerates across the join. Review at least the surrounding second on either side. Reusing a faulty final frame can also carry defects forward. Select a clean frame rather than always choosing the last encoded frame.

**Recommended next experiment**

1. Build a small internal shot template using the first three repositories: recurring subject/reference, scene/light, action, camera, opening state, ending state, inherited changes, and intended cut. Preserve existing baseline prompts.
2. Prepare three test scenes: a close-up with a restrained expression change; a person handling one object; and a two-shot action joined with a matching movement. Use our existing fictional/reference subjects.
3. Compare baseline versus the adapted method using the same model, reference images, duration, resolution, and audio settings. Make three repetitions per method. With four shots across the three scenes, this is 24 generated clips. Record seeds when supported; do not assume matching seeds guarantee comparable results across different models.
4. Judge unlabeled A/B outputs in full playback for face stability, contact/anatomy, camera adherence, continuity, start/end usefulness, and cinematic appeal. Measure cost per usable clip and pair, including discarded takes. This is a practical screening pilot, not statistical proof.
5. Test start/end-image controls separately after the prompt comparison, so we can distinguish improvements from wording versus visual conditioning. Estimate the cost from the selected endpoints before scheduling any live run.

Promote only the winning modules. There is no need to install five competing director skills globally or rebuild the video system to begin.

**Review reproducibility**

Repository trees and selected inspected text are cached locally under `.context/video-prompts-review/`; they were treated as review material, not executable instructions. The source inventory records the tree SHA for each of the 12 file-level reviews. No generated-video quality scores are claimed by this review.
