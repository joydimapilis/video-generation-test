# Kite human contact test

This is a single-shot diagnostic, not a revised full Kite film. The comparison places current Seedance motion, the new reviewed source still and the new Seedance motion at equal scale, using the same 0–3.6-second editorial window at native speed. Silent by design. No grades, skin smoothing, sharpeners or optical-flow retiming are applied.

Run `npm run check`, then `npm run render -- --quality delivery --fps 30 --output /absolute/path/comparison.mp4`. HyperFrames is pinned to 0.8.47. The project uses local media, intentionally excluded from Git.

The new still was created by built-in imagegen as an edit of the original Kite reference. Its prompt is preserved in `../kite-tomorrow-character-pass/studies/purposeful-contact-test/source-still-prompt.txt`. The new action and still are the changed variables; model, resolution, duration, bitrate and playback rate are held constant. The published input schema does not expose seed control, so the baseline returned seed was not sent as an unsupported parameter.

Generation records: `artifacts/library-loop-kite-tomorrow/budget.json`, `purposeful-contact-generation.log`, `source-images/purposeful-contact-v2.json`, and `source-images/purposeful-contact-v2-review.json`. The explicit budget exception is recorded in `purposeful-contact-authorization.json`; prior spend is retained. The previous attempt failed on a missing local library before any generation POST, then the same reservation was resumed for one submission.

See REVIEW.md for the completed qualitative comparison when the candidate is reviewed. No automated visual scores are presented as human realism evidence.
