# Crew: human realism and shot continuity

A four-clip controlled revision of an existing film, not a new production. Three
plates of the ten-plate Crew testimonial were re-generated and re-cut; the other
seven were left untouched. $3.38 of new generation against the same $10 cap.

The question was narrow enough to answer with the money left: **does a structured
shot contract make generated people look more real, and does feeding one clip's
exit frame into the next clip close the seam between them?** Both were tested
against the footage they replace, with the model, seed, duration, resolution and
audio settings held fixed.

Deliverables:

- The revised film — `artifacts/final_outcome/crew-improved/crew-improved-final.mp4`
- A silent A/B reel — `artifacts/final_outcome/crew-improved/crew-before-after.mp4`
- The previous cut, unchanged — `artifacts/final_outcome/crew/crew-final.mp4`

## What changed

### 1. A shot contract instead of a prose prompt

`src/amarillo/shot_plan.py` introduces `ShotState`: ten fields that describe a
shot's boundary conditions — identity, wardrobe, environment, lighting, framing,
camera, screen position, travel direction, pose, prop state. Every shot now
declares the state it enters on and the state it exits on, and `validate_join`
refuses a join labelled `continuous` if any field differs across it.

Screen position and travel direction are deliberately separate fields. The
planner in `ai-shortfilm-prompts` conflates them and contradicts itself as a
result (its right-exit example asks for right-entry while its narrative template
asks for left-entry); keeping them apart removes the ambiguity.

`interview_prompt` compiles a `ShotState` pair plus a line of dialogue into the
request text. The realism direction it adds over the baseline prompt is:

- **Identity, stated as preservation rather than description.** "Preserve the
  visible face, age, hairline, nose, asymmetry and skin texture of the reference;
  do not beautify or add new facial marks."
- **Behaviour instead of adjectives.** "Eyes attend to the same interviewer just
  camera-right, with tiny refocusing movements and unforced irregular blinking.
  Quiet breath moves the shoulders; one slight head inclination accompanies the
  thought, then settles."
- **Hands given a resting state.** "Hands rest low in her lap, not rigid; no
  finger-counting or presenting objects." The previous cut had to re-generate a
  take because the model produced an offensive hand gesture unprompted.
- **Secondary motion tied to a cause.** "Sleeve folds respond only to body
  movement; stray hairs remain settled in still air."
- **An explicit exit.** Pose, screen position, travel and props are restated at
  the end of the prompt, so the take is asked to finish somewhere specific.
- **A negative list aimed at the AI-face signature**: `beauty retouching, waxy
  skin, exaggerated eyebrows, finger counting, floating hair`, appended to the
  baseline negatives.

### 2. Routing that refuses under-specified work

`route_shot` is a function, not a table, because two of the routes have
preconditions that were previously honoured by memory:

| Use case | Route | Refuses when |
| --- | --- | --- |
| `interview`, `ugc_dialogue` | Veo 3.1 Fast image-to-video, audio on | no reviewed identity reference exists |
| `hands` | Kling 3 Pro (image-to-video if a reference exists, else text-to-video) | continuous action is requested without a real entry frame |
| `exact_ui` | HyperFrames | never — generated text is not a candidate at any price |

Veo 3.1 Fast keeps the dialogue route because it is the only endpoint in this
project's catalogue that returns lip-synced spoken audio in the take; six loops
of evidence say no model in the catalogue spells reliably, so on-screen product
text stays in HyperFrames.

### 3. Real exit-frame conditioning

Continuity was previously *asserted* in prompt text ("the same woman continues").
It is now *conditioned*: the outgoing clip's chosen exit frame is uploaded as the
incoming clip's input image.

- `scripts/review_exit_frame.py` extracts candidate frames around the intended
  cut and records the approved one with the source SHA-256, the frame SHA-256 and
  a written reason. It refuses to approve more than one candidate at a time.
- `src/amarillo/references.py` resolves `local:` paths anywhere in a request —
  including `start_image_url`/`end_image_url` pairs and `reference_image_urls`
  lists, which the previous three-field helper could not reach. It validates
  every path before uploading anything, uploads each distinct file once, and
  returns a copy so the saved request still shows the local path.
- `build_crew_improved.py` will not build if `selection.json` is not marked
  reviewed, and `plan_crew_realism.py` will not compile a continuation config if
  the named frame does not exist on disk.

Nine candidates were pulled from `realism_line4_v2` between 4.80s and 5.90s. The
frame at 5.125s was chosen because the lips have just closed after speech ends at
5.06s, the eyes are open and the face and apron are intact; the 5.4–5.9s
open-mouth tail was rejected. That timestamp then became the cut point in the
edit, so the frame the next clip starts from is the frame the previous clip ends
on.

### 4. A hands prompt built as one causal chain

The dough insert was re-prompted from `awesome-kling-prompts`' action-chain
shape: preparation, contact, release, settle, with the forces named. "Palms
settle on the near half of the dough, lean weight gently forward, compressing it
against the bench; fingers remain curved together as the palms release; the
elastic dough partly rebounds and stays on the bench," plus "wrists and forearms
carry the force, no floating contact" and "no second kneading cycle." The
baseline prompt asked for kneading and got a loop of turning and tucking.

### 5. Three fixes found on the way

- `prepare_crew_assets.predict_mix_peak` summed dialogue tracks without applying
  each track's volume, so the pre-render clipping prediction ignored the two
  tracks that carry one. Fixed; the revision predicts a 0.906 per-channel peak
  and measures below 1.0 in every window.
- White captions and the corner brand mark sat on generated footage of
  uncontrolled luminance. Over the near-white pencil-schedule cutaway they
  measured 2.59:1 and 2.96:1 against a 3:1 requirement. Each now carries its own
  local scrim — a bottom gradient that appears only while a caption is on screen,
  and a small radial falloff behind the mark. 41/41 contrast checks pass.
- Re-timing the cut opened a 4.25s hole between line 5 and line 6 that the
  original did not have, and the score's loudest movement plays underneath it.
  Swelling the music to full there put it at 0.63× the quietest spoken line — the
  delivery gate requires the loudest music to sit below half the quietest speech,
  and refused the render. That one lift now stops at 0.65; the measured ratio is
  2.45×.

## What the tests show

Four new clips, one trial each. Everything else held fixed.

| Comparison | Held fixed | Varied |
| --- | --- | --- |
| `line4_product_v1` → `realism_line4_v2` | Veo 3.1 Fast, seed 92, anchor frame `f5.8.jpg`, 6s, 1080p | prompt and negatives |
| `realism_line5_control` → `realism_line5_chained` | Veo 3.1 Fast, seed 93, revised prompt, outgoing shot, 6s, 1080p | input reference image only |
| `broll_dough_v1` → `realism_dough_v2` | Kling 3 Pro text-to-video, 6s, unseeded | prompt |

The second row is the one that matters most. Without it, wording and visual
conditioning change together and nothing can be attributed to either; with it,
the only difference between two clips is which image the model started from.

### Shot continuity — the clearest result

Mean absolute pixel change at the cut, against the median change between adjacent
frames on either side. A ratio near 1 means the cut moves the picture about as
much as one ordinary frame of motion does; a high ratio means the picture jumps.

| Join | Full frame | Head region |
| --- | ---: | ---: |
| Original, both shots from the shared anchor | 6.76× | 5.27× |
| Revised prompt, both shots from the shared anchor (control) | 11.00× | 7.35× |
| **Revised prompt, incoming shot from the outgoing exit frame** | **2.38×** | **1.19×** |

In the head region the seam drops from 5.27× to 1.19× — the cut becomes roughly
indistinguishable from one frame of her ordinary movement. The control is the
load-bearing row: with the same improved prompt and the same seed but the shared
anchor as input, the seam got *worse* (7.35×), because the revised prompt pulls
the framing tighter and a tighter shot cut against the original wide framing
jumps more than the original pair did. Prompt text alone did not close the seam
and would have widened it. The exit frame closed it.

This is a pixel diagnostic, and it is easy to fool: a frozen face also scores
low. It locates seams; it does not measure naturalness. Chapters 03 and 04 of the
comparison reel show the same four joins in motion for that reason.

### Human realism — better on hands, mixed on faces

Hands are the unambiguous win. Side by side at the moment of contact, the revised
dough take shows tendons, veins, knuckle creases and short nails, and the palm
visibly compresses the dough against the bench before releasing. The baseline
take's fingers partly merge into one another and the dough deforms without a
clear line of force.

The action chain did not, however, get obeyed as written. "No second kneading
cycle" was ignored: the take completes its press and release and then starts
another press at about 4.5s. It cost nothing only because the shot was bought
long enough to trim — the film uses 2.5–4.5s. Negative instructions about
repetition should be treated as preferences the edit may have to enforce, not as
constraints the model will honour.

On the face, the revised take reads as older and more textured — a deeper
nasolabial fold, more visible skin structure under the side light, a mid-thought
expression rather than a held pleasant one. That is the direction asked for and
it is less obviously AI-generated. It is also a small identity drift from the
reused plates it sits beside, and one reviewer's judgement on one take, which is
not the same as an audience preferring it.

### Speech

Automatic Whisper transcription, ordered word by word against the script:

| Clip | Ordered words match |
| --- | --- |
| `realism_line4_v2` | yes |
| `realism_line5_control` | yes |
| `realism_line5_chained` | **no** — "everyone sees **an** update" for "everyone sees **it** update" |

The exit-frame-conditioned take substituted one word. The caption in the film was
changed to match what she actually says rather than what the script asked for,
which is the honest fix but does record a cost: conditioning on a video frame
appears to have cost a little prompt adherence on this take. One clip is not
enough to call that a property of the method.

## What did not improve, and what is still wrong

- **Identity drifts slightly across the revision boundary.** The revised
  interview takes are marginally tighter and more textured than the seven reused
  plates. Every shot they touch is a deliberate cutaway, so the drift is not
  exposed at a continuous join, but a full re-generation would be more coherent
  than a partial one.
- **The revised dough insert is lighter and cooler** than the warm bakery grade
  around it. It is better anatomy in a slightly wrong colour; no grade was
  applied, and it should be.
- **Conditioning on a decoded video frame carries that frame's artifacts
  forward.** The chained take is visibly crunchier around the hair and background
  than the control, which started from a clean reference JPEG.
- **One clip per condition.** The review that motivated this work recommended
  three repetitions per method across three scenes — 24 clips. The ledger had
  room for four. Every number here is a single trial with no confidence interval,
  and seeds do not guarantee comparability across models.
- **Only one continuous join exists in the film.** Nine of the ten remaining
  handoffs are cutaways or intentional cuts, where continuity is not asserted.
  The method is demonstrated, not exercised at scale.
- **No human audience testing.** All quality judgements here are mine.

## Where the techniques came from

MIT-licensed material only, adapted rather than installed; attribution in
`docs/third-party/cinematic-techniques-LICENSE.txt`. Full source review in
[VIDEO_PROMPTS_TOPIC_REVIEW.md](VIDEO_PROMPTS_TOPIC_REVIEW.md).

| Source | What was taken | What was rejected |
| --- | --- | --- |
| [ai-shortfilm-prompts](https://github.com/jnMetaCode/ai-shortfilm-prompts) (MIT templates only) | The project planner's entry/exit-state record, reworked into `ShotState` | Mandatory camera/lens names and camera "breathing"; its conflated position/direction field |
| [ai-visual-skills](https://github.com/sundny8/ai-visual-skills) (MIT) | Preparation → contact → reaction as the shape of a physical action; observable facial behaviour instead of emotion words; carrying changed state into later shots | Fixed 30s/vertical/8K defaults and mandatory dramatic structure |
| [awesome-kling-prompts](https://github.com/Reviral-ai/awesome-kling-prompts) (MIT) | Single action chain, named forces, a stated final pose, and what must stay fixed | Nothing needed for this pass |
| [awesome-ad-video-prompts](https://github.com/LichAmnesia/awesome-ad-video-prompts) | Not used this round | — |
| [awesome-ai-video-transition-prompts](https://github.com/yinxiaowai/awesome-ai-video-transition-prompts) | Studied only — the idea of designing both sides of a join together | Not imported: all-rights-reserved licence |
| [super-director](https://github.com/fanchengchen1-collab/super-director) | Studied only | Not imported: CC BY-NC-ND |

Nothing was borrowed for its own sake. Of the five shortlisted repositories,
three contributed and two did not.

## Cost

| | |
| --- | ---: |
| This realism round, estimated (4 clips, one bought as a control and discarded) | $3.38 |
| Loop 6 total, estimated | $8.48 |
| Loop 6 total, conservatively reserved | $9.79 |
| Hard cap | $10.00 |

Nine paid requests across the loop, all completed, no failures and no automatic
retries. **$0.21 of reserved headroom remains, so no further generation is
possible under this cap.** The ledger at `artifacts/library-loop-6/budget.json`
is the persistent cost record and deleting it defeats the cap guard. Provider
invoice not queried. The HyperFrames assembly, the comparison reel and every
diagnostic in this report cost nothing.

## Verification

Every gate below is an assertion in `scripts/finalize_crew_improved.py`; the film
is not written to `artifacts/final_outcome/` unless all of them hold. Full record
in `artifacts/final_outcome/crew-improved/verification.json`.

| Gate | Result |
| --- | --- |
| Container | H.264 1920×1080, 24fps, AAC stereo, 49.000s |
| Full decode, film and reel | no errors |
| Comparison reel | 1920×1080, no audio stream (silent by design) |
| Audio overload | peak below 1.0 in all 12 measured windows, per channel |
| Music duck | quietest spoken line 2.45× the loudest music bed (gate: 2.0×) |
| Whisper transcript vs. caption script | 0 missing words |
| Previous deliverable | SHA-256 unchanged across the run |
| Exit-frame provenance | recorded SHA-256 matches the file on disk |
| Ledger | 9 requests, all completed, $9.79 reserved against the $10 cap |
| HyperFrames check, both projects | 0 lint / runtime / layout / motion findings; 41/41 and 25/25 contrast |
| Python tests | 38 passed |

## Reproducing this

```bash
.venv/bin/python scripts/plan_crew_realism.py                     # baseline-prompt retakes
.venv/bin/python scripts/run_library_loop.py configs/crew_realism_round1.json
.venv/bin/python scripts/review_exit_frame.py \
    artifacts/library-loop-6/outputs/realism_line4_v2.mp4 \
    --at 5.125 --output artifacts/library-loop-6/realism/selected \
    --approve-reason "..."                                        # human review gate
.venv/bin/python scripts/plan_crew_realism.py \
    --continuation-frame artifacts/library-loop-6/realism/selected/exit-5.125.png
.venv/bin/python scripts/plan_crew_realism.py --control           # isolates the reference
.venv/bin/python scripts/evaluate_crew_realism.py                 # seams, speech, provenance
.venv/bin/python scripts/build_crew_improved.py
.venv/bin/python scripts/build_crew_comparison.py
.venv/bin/python scripts/finalize_crew_improved.py
```

`run_library_loop.py` will refuse any request that would push the reserved total
past the cap, so the first three commands are no-ops now.
