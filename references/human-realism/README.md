# Human realism reference set

Five user-supplied clips, described by the user as real human footage. This is a
dedicated **Phase 2** reference set for evaluating and improving human realism: natural posture,
eye/gaze behavior, hand movement, mouse/keyboard interaction, body movement,
facial expressions, framing, lighting and gesture timing.

This set is excluded from the default video-generation workflow. Consult these
clips during separate Phase 2 work. Normal production still uses a reviewed source
image → image-to-video workflow for people scenes and reviews the resulting motion;
neither step requires this movement library. Preserve the clips and existing
observations below as Phase 2 evidence.

Use the observable behavior and physical relationships. Do not recreate these
videos directly or substitute their subjects' identities, settings, wardrobe or
stories into a production. A clip's presence here does not mean it was supplied
to a generation API. No clips were uploaded or used for new generation during
the initial review.

| Clip | Main reference use | Important limit |
| --- | --- | --- |
| human-reference-01.mp4 | Laptop work, seated-to-standing weight transfer, reaching and walking; approximately 0–5 s for desk work, 5–11 s for standing/exiting | Wide, elevated, moving office framing; face small/partly obscured |
| human-reference-02.mp4 | Laptop typing: independent finger motion, contact, wrist stability and irregular cadence across approximately 0–5 s | Face excluded; no gaze/expression evidence |
| human-reference-03.mp4 | Screen-to-keyboard gaze, typing pauses, reaching/grasping/returning an object; approximately 0–7 s is a compact example | Desktop monitor, glasses and clinical setting differ from Kite |
| human-reference-04.mp4 | Quiet attention, small posture changes, screen/page gaze, restrained expression, soft side lighting and medium three-quarter framing | Tablet/stylus/book rather than laptop; screen direction opposite Kite |
| human-reference-05.mp4 | Laptop keyboard/trackpad-area interaction, unequal hand roles, pauses and forward working posture | Mask obscures lower face; darker side/rear view limits eye/expression analysis |

**Historical Kite Tomorrow review:** 04 is the closest overall match, especially approximately
0–4 s. Use 02 and 05 as supplemental device-contact references if the action
is changed to include typing or trackpad use. External mouse grip/click motion
is not clearly established in this review; do not label trackpad motion as mouse
evidence.

Read the [detailed review](../../review_notes/human-realism-references.md) and
`catalog.json` for provenance, observation limits and the Kite comparison.
Full-decode results, contact sheets and chronological review samples live in
`artifacts/human-realism-reference-review/`. Source media stays local and unchanged.
