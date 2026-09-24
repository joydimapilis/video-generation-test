# Kite — Tomorrow, revised

Full 38-second restoration and targeted UI revision of `../kite-tomorrow`.
Original project files and recovered source takes are preserved.

Run `npm install`, then `npm run dev`, `npm run check`, or
`npm run render -- --quality delivery --fps 30 --output <absolute-path.mp4>`.

Local media is excluded from Git. Source recovery provenance is recorded in
`../../artifacts/kite-tomorrow-revision/recovered/manifest.json`. The selected
Veo clip is copied into `assets/marketer.mp4`; music is decoded from the
recovered Sonilo file. Narration and cut cues can be recreated with
`../../scripts/prepare_kite_tomorrow_revised_audio.py` using the original cached
Kokoro model and voices. After restoring audio, run the installed
`hyperframes-audio/scripts/carve.mjs --comp index.html`.

The handoff UI comes from `../kite-tomorrow/studies/ui-after`; the feedback
panel carries the same thread context and official app icon. Both are
illustrative HTML/SVG reconstructions. Product workflow source:
https://docs.kite.ai/slack/approvals.

Character footage is retained, not newly improved. Prior generation costs are
carried forward in `budget.json`; this revision adds no paid generations.
