# Serein — image-first interaction revision

The user found the original resting-hand shots too passive: they did not clearly communicate computer use. The replacement still establishes a visible mouse, natural grip, aligned wrist and forearm, and gaze directed at the laptop before animation. Full-frame and enlarged hand review passed before submission. Both revised shots share this exact source image.

Scores are historical agent judgments from sampled frames, not calibrated realism measurements or audience tests. Model, prompt and seed changes confound causal comparisons. Product interaction is now an explicit selection requirement; a high face-quality score does not override failed gaze or mouse interaction.

| Take | Decision | Observation |
| --- | --- | --- |
| Original Veo focus/relief v1 | Rejected | Early mouth opening or exaggerated reaction. |
| Original Kling focus v2 | Rejected | Mouth opening and softer facial texture. |
| Original Kling relief v2 | Superseded | Previously selected for restrained reaction; resting hands did not show active use. |
| Original Veo focus v3 | Superseded | Previously selected for face texture and quiet expression; passive hand pose and downward gaze failed user intent. |
| Mouse Veo focus v4 | Rejected | Visible mouse and recognizable grip, but repeated downward gaze and excess mouse rotation. |
| Mouse Veo relief v4 | Rejected | Same gaze failure despite improved mouse interaction. |
| Mouse Kling focus v5 | Selected, source1.5–6s at0.75× | Settled screen attention, visible grip and mouse navigation; early downward eye movement omitted. |
| Mouse Kling relief v5 | Selected, source0–6s | Screen attention and a stable mouse grip with subtle finger movement; softer face than the still. |

## Workflow learning

- Review both anatomy and the intended action in the source still. A realistic idle hand is not evidence of computer use.
- Establish mouse grip before I2V; do not ask the video model to invent it.
- Check the face and hand together through time. A stable hand does not compensate for looking away from the screen.
- Keep all original attempts, rejected takes, requests and costs in the same cumulative ledger.
- Preserve original delivery and provenance separately when replacing shots.

## Spend and evidence

Nine Fal I2V attempts estimate $5.92. Two $1 image planning allowances bring the cumulative estimate to $7.92; $9.14 reserved with margin under the $10 cap. The image tool exposes no invoice, so allowances are not confirmed charges.

Evidence: `artifacts/library-loop-13/scorecard.json`, `reviews/character-mouse-v2.json`, chronological full-frame/face/hand sheets, `videos/serein/sources.json`, and final encoded verification. The original final and verification are retained in `artifacts/final_outcome/serein/original/`.

## Revised encode
32s,1920×1080,24fps;768frames fully decode. Zero composition findings,43/43contrast checks,300motion samples. Six source comparisons below2.40/255 verify the selected crop/timing including0.75× opening playback. Audio correlation0.99989, peak0.815. Encoded opening/return inspection confirms the mouse remains visible beside the laptop and the hand stays seated on it.

Tracked evidence: [machine scorecard](../review_notes/serein/scorecard.json) and [final verification](../review_notes/serein/final-verification.json). Generated frame sheets and full media remain local under `artifacts/`.
