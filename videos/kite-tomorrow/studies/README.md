# Kite Tomorrow — isolated revision studies

These studies preserve the main 38-second film and its source files. No full-film regeneration was performed in this pass.

- `ui-before/`: the original handoff scene copied from the tracked composition. It reproduces the original 7.2–16.5-second segment, without sound. It is not extracted from the missing original final MP4.
- `ui-after/`: an isolated 9.3-second revision with the same story copy and reveal/click times. Uses the official Kite Slack icon, a screenshot of the existing Relay draft, more consistent typography/spacing, retained request context, and a hover/press response on Preview.
- `draft-before/`: original draft composition copied for inspection and thumbnail capture; no revised product-page design.
- `comparison/`: synchronized, labelled before/after video comparison. Its two MP4 inputs are copied from the standalone study renders and excluded from Git.
- `CHARACTER_TEST.md`: the prepared image-first character test; not submitted because cumulative USD spend is unresolved.

The UI remains a labelled illustrative reconstruction, with a fictional Relay company. It is not a signed-in recording or a claim of pixel-identical Kite/Slack UI. Preview/Review and thread revision behavior are grounded in [Kite's approvals documentation](https://docs.kite.ai/slack/approvals). The app icon comes from [Kite's own website](https://kite.ai/ai-marketer/kite-slack-app-icon.png). Colors/wordmark context: [Kite newsroom](https://kite.ai/newsroom).

The study projects use HyperFrames 0.8.46; the main film remains pinned to 0.8.45. Both study versions use the same renderer for comparison. Run from either `ui-before/` or `ui-after/`:

```sh
npm run check
npm run render -- --quality looks --fps 30 --output ../../../../artifacts/kite-tomorrow-revision/ui-after.mp4
```

Use `ui-before.mp4` for the before project's output. The rendered studies are intentionally silent; original narration/music are not being revised.

Recovered source files, hashes and original provider-job URLs are in `artifacts/kite-tomorrow-revision/recovered/`. They were downloaded from archived completed jobs, with no new paid generation. Keep this media locally; Git does not preserve the original large artifacts.

New generation spend: $0. Historical spend: 31.38 quoted credits plus one image, USD unknown. Do not interpret the $0 revision spend as a reset of the video's $10 ceiling.

The draft thumbnail is a local generated asset: reproduce with `hyperframes snapshot` in `draft-before/` at 5.5 seconds, zooming `#page-surface` at scale 1, then copy the frame to `ui-after/assets/relay-draft-thumbnail.png`.
