# Kite — From feedback to a better message

36 seconds, 1920×1080, 30fps. Editable HyperFrames project. Read BRIEF.md and PRODUCTION_REVIEW.md for source, assumptions, review and cost record.

Render exact checked index:

```sh
npx hyperframes@0.8.60 check
npx hyperframes@0.8.60 render --skill=product-launch-video --quality high --fps 30 --output renders/kite-feedback.mp4
```

Final source is index.html plus compositions/frames and local assets. tools/assemble-index.mjs is retained as assembly provenance; rerunning it overwrites the root human-video placement and audio automation, so render the checked index directly. Assets remain local under existing media-exclusion rules. No paid generation is required to re-render.
