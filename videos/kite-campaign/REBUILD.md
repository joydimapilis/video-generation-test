# Rebuild

From repository root:

```
.venv/bin/python videos/kite-campaign/build.py
.venv/bin/python videos/kite-campaign/make_score.py
```

The saved `index.html` is the reviewed host. Render from `videos/kite-campaign` with `npm run check`, then `npx hyperframes render --quality high --fps 30 --output ../../artifacts/final_outcome/kite-campaign/kite-campaign.mp4`. Regenerate the per-MP4 reverse-engineering document from the individual production JSON and run final verification before marking any new render complete.

To rebuild the host with the installed assembler, use `node --import ./tooling/restore-import.mjs /Users/joydimapilis/.agents/skills/product-launch-video/scripts/assemble-index.mjs --storyboard ./STORYBOARD.md --hyperframes .`. The loader restores a missing packaged media-fetch import using the official module retained with provenance in `tooling/source.json`. After assembly, replace the remote GSAP tag (including its integrity attribute) with `<script src="assets/gsap.min.js"></script>` and preserve the white host ground. Validate transitions and rerun composition checks. Do not patch global skills.

Local rendering and synthesis have no provider charges. No credentials are required. The production's single persistent budget ledger is `budget.json` with USD10 cap and no paid requests.
