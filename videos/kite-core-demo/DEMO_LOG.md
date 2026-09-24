# Kite core workflow demo — production log

This is a new 30-second production from a simple request. The example request below was chosen by the agent for this run; it is not a verbatim quotation from the user. No Phase 2 movement reference or Phase 2-conditioned footage is used.

| Stage | What happened | Open during the demo | Say this |
| --- | --- | --- | --- |
| 1. Request | The short request was expanded using standing core instructions. | `BRIEF.md` | “I start with one sentence; the production workflow is already installed.” |
| 2. References | Resolved 11 general-library videos; selected Motion-5, Cero and Paper. Reviewed complete chronological frame samples plus closer joins, then passed the reference gate. | `references/manifest.json`, `reference-review.json`, reference clips through `DEMO.html` | “It studies relevant examples before deciding how to tell this story.” |
| 3. Shot plan | Defined five shots across three ten-second compositions, each with a purpose, timing and acceptance criteria. | `STORYBOARD.md` | “The idea becomes individual shots with a job to do.” |
| 4. Routing | Exact UI and text go to HyperFrames; the paper opening is a bounded Kling test through Fal. | `shot-routing.json`, `generation-plan.json` | “The method follows the shot: generated texture where useful, exact rendering where accuracy matters.” |
| 5. Generate/review | One new Kling take accepted; first assembly rejected for hidden headline, wrong font subset and overlap; corrected and rechecked. | `generation-review.json`, `composition-revisions.json`, `assets/paper-opening.mp4` | “An API result is a candidate until it passes review.” |
| 6. Prior learning | Applied Fold's same-object story and visible-revision lessons. Crumb's stationary-object result suggests a small test, without treating it as a universal route. | `LEARNINGS.md` | “Past successes and failures change the next production decisions.” |
| 7. Assemble/verify | Rendered 30s/1080p/30fps; decode, 42 contrast samples, audio correlation and five encoded-preview comparisons passed. | `../../artifacts/final_outcome/kite-core-demo/kite-core-demo.mp4`, adjacent `verification.json` | “Approved pieces are assembled and the encoded video gets checked.” |
| 8. Reverse engineering | Created one individual MD beside the MP4; missing-file gate failed before writing, passed afterward; matching hash verified. | `../../artifacts/final_outcome/kite-core-demo/kite-core-demo.reverse-engineering.md`, `document-gate-before.txt`, `document-gate-after.json` | “This film cannot be marked complete without its own production record.” |

## Short request used

“Make a short Kite.ai launch video showing release notes becoming a draft launch page, then improving through feedback.”

## Research receipt

Actual library: `/Users/joydimapilis/Desktop/untitled folder/Startup Launch Videos` via `data/library`. Selected filenames and absolute source paths are in `references/manifest.json`. Motion-5's filename describes Motion, but its actual content shows a Grok Bot software story; decisions use the observed footage, not the filename. Sampling is documented honestly in `reference-review.json`: this is not a claim of uninterrupted audiovisual playback.

## Budget receipt

One shared $10 ledger: `artifacts/library-loop-kite-core-demo/budget.json`. Initial generated shot estimated $0.56; $0.65 reserved with buffer. Local UI, assembly and original score incur no provider charges. Confirmed billing unavailable; total remains estimated $0.56 and reserved $0.65. No paid retries.


## Delivery

Open [guided demo](DEMO.html) and [five-minute sequence](FIVE_MINUTE_DEMO.md). Full production record: [individual JSON](kite-core-demo.production.json). Final verification: [verification.json](../../artifacts/final_outcome/kite-core-demo/verification.json). Actual technical repairs: [TOOLING_NOTE.md](TOOLING_NOTE.md).
