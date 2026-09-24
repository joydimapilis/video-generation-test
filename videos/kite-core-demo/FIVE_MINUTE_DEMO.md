# Five-minute demo sequence

Open [DEMO.html](DEMO.html) in your browser. Use its numbered stages or left/right arrow keys. This is a walkthrough of the actual completed run; do not wait for new generation live. All media is local. Allow **4:40 for the walkthrough and 0:20 buffer**. Keep the browser at 100% zoom, close unrelated tabs, and test sound before presenting.

| Time | Show | Action and one speaking line |
| --- | --- | --- |
| 0:00–0:20 | Stage 1 · [BRIEF.md](BRIEF.md) | Show the one-sentence example: “I start with one sentence; the standing workflow handles the production steps.” |
| 0:20–0:55 | Stage 2 · [reference-review.json](reference-review.json) | Play the Paper 6–9s excerpt; point to the other two reviewed references. “It studies relevant examples before planning, using our general video library.” |
| 0:55–1:25 | Stage 3 · [STORYBOARD.md](STORYBOARD.md) | Show the five timed shots. “Each shot has a purpose, a plan, and a review criterion.” |
| 1:25–1:55 | Stage 4 · [shot-routing.json](shot-routing.json) | Point to Kling for the opening and HyperFrames for the UI. “The shot determines the method; accurate text is rendered deterministically.” |
| 1:55–2:40 | Stage 5 · [generation-review.json](generation-review.json), [composition-revisions.json](composition-revisions.json) | Play the five-second take, then show the rejected assembly and corrected headline. “The generated take passed, but the first assembly did not; review caught a hidden headline and a wrong font subset.” |
| 2:40–3:10 | Stage 6 · [LEARNINGS.md](LEARNINGS.md), [learning-after-run.json](learning-after-run.json) | Show Fold's visible-revision lesson, then this run's selected take in refreshed evidence. “Past results influence this run, and this reviewed result becomes evidence for the next one.” |
| 3:10–3:50 | Stage 7 · [final MP4](../../artifacts/final_outcome/kite-core-demo/kite-core-demo.mp4) | Say “Here is the finished 30-second film,” then play it in full with sound. Leave five seconds to point to the verification summary. |
| 3:50–4:40 | Stage 8 · [individual reverse-engineering document](../../artifacts/final_outcome/kite-core-demo/kite-core-demo.reverse-engineering.md) | Show sections, matching video identity and hash. Toggle the actual [missing-file failure](document-gate-before.txt) and [passed gate](document-gate-after.json). “This video stays incomplete until its own production document exists and matches the final file.” |
| 4:40–5:00 | Buffer | Return to the final frame, handle one short question, or finish early. |

## Keep the claims precise

- This example sentence was chosen for the demo by the agent; it was not a verbatim user message.
- Three general references were reviewed through chronological decoded samples and closer joins. Phase 2 movement research was excluded.
- There was **one paid video take, accepted**. The rejected version was a composition; there was no model switch or paid retry to show in this run.
- The product interaction is labelled illustrative. The film does not demonstrate a live Kite backend or publication.
- Provider cost is an estimate of **$0.56**, with **$0.65 reserved**, against one **$10 ceiling**; confirmed billing is unavailable. Local score/UI/rendering have no provider charge.
- Picture review was sampled; audio verified numerically, without independent listening. Automated motion subcheck was disabled; encoded transition samples and preview comparisons were inspected separately.
- An installed helper dependency needed local restoration; see [TOOLING_NOTE.md](TOOLING_NOTE.md). Do not present this run as having required zero intervention.

## Optional editable timeline

[HyperFrames Studio](http://localhost:3047/#project/kite-core-demo) was started and checked during this run. If it is no longer running, execute `npx hyperframes preview --background --port 3047` from `videos/kite-core-demo`. The guided demo and final MP4 do not depend on Studio.
