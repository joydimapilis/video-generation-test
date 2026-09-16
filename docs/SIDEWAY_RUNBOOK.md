# Sideway — Less saving. More going.

Original 36-second portrait customer-experience film for a fictional mobile walking planner. A person who saves places but never visits them chooses an hour, builds a three-stop walk, and arrives at a café. Three seconds of on-camera speech support the story; lifestyle footage and authored app UI carry the rest.

## Production

The user brief, storyboard, script, design, audio plan, and source hashes are in `videos/sideway/`. Source prompts are `prompt_library/sideway_*_still.txt`; generation configuration is `configs/sideway_round1.json`. Reviews are preserved in `review_notes/sideway/` and `artifacts/library-loop-14/reviews/`.

Three new still images establish the same character, clothing, lighting, and natural interaction before animation. Each image was inspected and approved before its I2V request. The phone reference establishes a visible device, supporting hand, poised tapping finger, and phone-directed gaze. Story and café references derive from the same approved character.

Kling 3 Pro animates the phone and café stills with restrained motion. Veo 3.1 Fast animates the story still with native dialogue. Both spoken excerpts use that single voice take. Source 0–3 seconds supplies the speaking shot; the later reflection is voiceover. Phone and café clips are silent. Important readable UI is authored in HyperFrames, with a local original music bed and interface sounds.

Existing Pocket, Supersonik AI, Motion5, Tuck, and Serein learnings informed pacing, product clarity, UI transitions, and source-image interaction checks. No previous human footage, source image, narration, or music was reused. Shared fonts and runtime dependencies are infrastructure.

## Rebuild

From the repository root, with generated media available locally:

```sh
.venv/bin/python scripts/prepare_sideway_assets.py
.venv/bin/python scripts/build_sideway_composition.py
node scripts/verify_sideway_geometry.cjs
npx hyperframes check videos/sideway --samples 18 --json > artifacts/library-loop-14/check-final.json
```

Render from `videos/sideway`:

```sh
npx hyperframes render --quality delivery --fps 24 --workers 2 --output ../../artifacts/final_outcome/sideway/sideway.mp4
```

Then verify from the repository root:

```sh
.venv/bin/python scripts/verify_sideway_video.py
```

Generated media and tool caches are gitignored. The source manifest records local media hashes; rebuilding requires those files. Generation requires provider access and incurs cost; assembly does not submit generation requests.

## Delivery

`artifacts/final_outcome/sideway/sideway.mp4`: 1080×1920, 24 fps, 36 seconds, 864 frames, 32,069,579 bytes. SHA-256: `2e1e63c1fd8621d07eede9e985191d8e3113d2b910feb79e63ce746b57a7ec66`.

The final encode passes full decode, black-frame detection, audio alignment, source comparisons, modular seam checks, and the ending hold. HyperFrames reports zero errors or warnings across lint, runtime, layout, motion, and contrast, with 50/50 contrast checks passing. Evidence: `artifacts/final_outcome/sideway/verification.json`.

Separate $10 run ledger: $2.56 estimated Fal video plus $3 in image planning allowances = $5.56 total; $6.41 reserved with margin. The built-in image tool exposes no invoice, so allowances are estimates rather than measured charges.

## Current gaze/dialogue revision

Use `configs/sideway_round2_gaze_dialogue.json` for the two replacement I2V requests. They are already complete; running the existing runner with the same IDs resumes without a new paid request. The original $10 ledger is shared and must not be reset. The corrected phone source and pre-animation review are version2; the speaking reference remains version1.

`selected-takes.json` is required by staging and records the chosen versions and native speech cuts. Root playback retimes the quiet phone return at0.5× from source1–3s. The original delivery and original build/provenance files remain under `artifacts/final_outcome/sideway/original`. Render the current version to `artifacts/final_outcome/sideway/sideway-revised.mp4`; the verifier targets that filename.

After staging and rebuilding, refresh the voice/music carve before checking or rendering. Install `@hyperframes/core@0.8.41` under `.context/sideway-audio`, then run the installed `hyperframes-audio/scripts/carve.mjs` with `--comp videos/sideway/index.html --core .context/sideway-audio --bed sideway-score --voice sideway-speech --strength 0.25`. The resulting dynamic carve removes a small amount of score energy in speech bands; source audio remains intact. `audio-mix.json` records the selected settings.

Current estimate including the revision:$8.44; reserved$9.73. The image tool does not expose actual invoices. See current `verification.json` for final dimensions, hashes and encoded checks rather than the historical first-delivery metrics above.

## Approved café-only revision

User explicitly approved a $12 total cap. The same ledger retains all earlier attempts and records the authorization and previous $10 limit. The runner still defaults to a $10 ceiling; a larger approved budget is passed explicitly, not read from a generation plan. Twelve budget/planning tests pass, covering default refusal, the approved ceiling, cumulative reservations, and prevention of ledger-cap changes through the runner.

The already-submitted café request can be resumed without resubmission:

```sh
PYTHONPATH=src .venv/bin/python scripts/run_library_loop.py configs/sideway_round3_cafe.json --cap-cents 1200 --approved-cap-cents 1200 --evaluate
```

The new forward-facing still is `assets/arrival-reference-v2.png`, reviewed before animation. The café output is selected in `selected-takes.json`; the final filename is `artifacts/final_outcome/sideway/sideway-cafe-revised.mp4`. The previous dialogue/gaze MP4 remains `sideway-revised.mp4`, and its verification/provenance is archived under `dialogue-gaze-revision/`. No dialogue or composition rebuild is needed for this media-only replacement. The preservation record is `artifacts/library-loop-14/cafe-preservation.json`.
