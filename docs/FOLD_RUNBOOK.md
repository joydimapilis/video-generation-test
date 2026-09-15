# Fold production and rebuild

The brief requested a new product launch with a creative hook, short walkthrough, connected ending, no interview dependency, an autonomous improvement loop, and a maximum $10 estimated generation cost. Fold is an invented AI tool that turns scattered campaign notes into a creative brief. FIELD, the refillable-bottle campaign inside its UI, is also fictional.

## Sources and routing

The existing library contains 347 videos. Three new reference contact sheets informed this run: Bloom's on-brand input-to-output transformations; Gamma's quick creation glimpses; Notion's moving task fragments. Their source filenames and selection are recorded in `artifacts/library-loop-11/references/manifest.json`. No reference footage was copied into the film. This was a targeted creative reference pass, not repeated model research.

Prior Trace/Crumb/H3 model scorecards and exact-UI/continuity lessons informed routing. HyperFrames 0.8.40 owns every visual frame because exact notes, message changes and paper geometry are the story. No generated human or cinematic insert is needed. Local Kokoro `am_michael` at 1.02 supplies new narration; a newly authored deterministic 120 BPM wood-tone score supplies music and synchronized paper/click sounds. No paid API calls were made.

The product-launch workflow used the no-capture fictional-script route and coral preset. Registry `modal-morph` supplied the measured-surface/counter-scale approach; `simulated-cursor` supplied the pointer/pulse primitive, adapted without shadows. Frames were authored serially using the workflow's inline worker fallback. The user's autonomous production request superseded storyboard/render checkpoints.

## Project

- `videos/fold/BRIEF.md`, `SCRIPT.md`, `STORYBOARD.md`: intent, narration and timed scenes.
- `videos/fold/frame.md`: local design contract.
- `videos/fold/compositions/frames/`: three seekable, modular scenes.
- `videos/fold/audio-plan.json`: measured raw narration, leading silence and intentional scene holds.
- `videos/fold/audio_engine_meta.json`: original speech engine metadata; captions are deliberately skipped.
- `scripts/build_fold_composition.py`: shared geometry and original animation source.
- `scripts/prepare_fold_assets.py`: padded narration and fresh score, deterministic seed 91511.
- `artifacts/library-loop-11/`: this run's budget, diagnostics and reference evidence.

Voice tracks are 9, 12 and 10 seconds, including real silence padding; these durations are not fabricated metadata. Raw takes remain alongside the padded files. Fonts are locally staged Google Fonts Bebas Neue and Inter. GSAP is locally staged and shared as tooling, not recycled video content.

## Rebuild with the staged assets

Run from the repository root. The existing project already contains its root assembly and local GSAP reference.

```sh
.venv/bin/python scripts/prepare_fold_assets.py
.venv/bin/python scripts/build_fold_composition.py
npx hyperframes@0.8.40 check videos/fold --json > artifacts/library-loop-11/check-final.json
node scripts/verify_fold_geometry.cjs
npx hyperframes@0.8.40 render videos/fold --fps 24 --quality delivery --strict --no-best-effort --skill product-launch-video --output artifacts/final_outcome/fold/fold.mp4
.venv/bin/python scripts/verify_fold_video.py
```

To regenerate missing raw narration, use the installed product-launch workflow audio adapter with `SCRIPT.md`, `STORYBOARD.md`, provider `kokoro`, voice `am_michael`, speed `1.02`, and `HYPERFRAMES_PYTHON` pointing to the workspace `.venv/bin/python`. Then run `prepare_fold_assets.py`; keep its `*-raw.wav` originals separate from the padded scene tracks. Preparing the existing assets does not call a generation API.

The root was created with the workflow's `assemble-index.mjs` and checked with `transitions.mjs verify`. If rebuilding the root, replace its default remote GSAP script tag with `assets/gsap.min.js`, and give the scene mounts `class="scene clip"`. Modular transitions are nominal cuts between identical settled states; the creative morphs occur within the frames. Do not inject a crossfade over those matched seams.

For preview:

```sh
npx hyperframes@0.8.40 preview videos/fold --background --port 3036
npx hyperframes@0.8.40 preview videos/fold --status
```

Studio: `http://localhost:3036/#project/fold`. Final player: `artifacts/final_outcome/fold/review.html`.

## Cost and limits

`artifacts/library-loop-11/budget.json` records a $10 cap, zero paid requests and $0 estimated generation cost. This is separate from previous loops. Local compute is not a billed generation API expense. No real AI backend or measured software capability was built; this deliverable is a fictional product launch film.

Final MP4, poster, encoded frame and seam sheets, review player and verification JSON live in `artifacts/final_outcome/fold/`. See [the scorecard](FOLD_SCORECARD.md) for revisions and review limitations.
