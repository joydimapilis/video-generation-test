---
format: 1920x1080
duration: 30s
message: Receipts become a ready-to-send expense report.
arc: Physical paperwork → digital review → finished report → back to your day
audience: independent professionals and small teams
mode: autonomous
music: none
captions: skipped (short on-screen statements and exact product UI carry the message)
---

## Video direction
Warm charcoal photography becomes a cream and dark-amber product world. Space Grotesk display, Inter body, generous spacing, softly rounded UI surfaces, no drop shadows. One tight hand/receipt source supplies distinct opening and withdrawal segments; approximately seven seconds of human presence total. No faces, speech to camera or interviews. Product facts stay explicit. Original local rhythm score will be added after narration; music:none suppresses catalog generation only. No site capture: fictional Tuck and example expenses. Inline serial worker fallback. Root assembly owns video and audio; frame compositions own exact text and UI. Media remains photographically natural after source review, without an extra color effect.

## Frame 1 — One small receipt
- scene: A small physical receipt creates a large administrative detour; its paper shape becomes Tuck.
- duration: 8s
- poster: 2.5s
- transition_in: cut
- status: animated
- type: hook
- blueprint: compose
- asset_candidates: tuck-mark.svg
- src: compositions/frames/01-receipt.html
- voiceover: "One small receipt. One more thing to do. Tuck turns receipts into ready-to-send expense reports."
- sfx: none

Scene 1 (0–2s): Warm hand/receipt macro video in the right panel x830 y0 w1090 h1080. A charcoal left region holds "One small receipt." in cream, 102px Space Grotesk. Small TUCK mark/name at x100 y95; source action is slow and natural.
Scene 2 (2–4.4s): The short line "One more thing to do." replaces the first while the hand rests by the paper. The authored paper plane starts at the transition target at x1225 y120 w480 h670 rotation-24deg. No text is composited onto a moving real screen.
Scene 3 (4.4–6.3s): Opaque paper plane rotates flat and expands into a full cream surface, `card-morph-anchor`. Hand footage is covered by the surface; the cream becomes the product world. Large TUCK / AI EXPENSE REPORTS is revealed, using `waterfall-entry`. Keep body text separate from nonuniform surface scaling.
Scene 4 (6.3–8s): Brand settles into the fixed app header; blank app body appears and is held before the next frame.
handoff_out: full background #F5F0E8; app x120 y190 width1680 height770; header height90; app opacity1 scale1 rotation0; header brand TUCK at x164 y216 Space Grotesk40 weight700; speed0 directionnone; header/body split y280; no other content visible.

## Frame 2 — Extract, check, report
- scene: Three receipt files become reviewed rows and one report.
- duration: 14s
- poster: 7s
- transition_in: cut
- status: animated
- type: feature_showcase
- blueprint: compose
- asset_candidates: tuck-mark.svg
- src: compositions/frames/02-report.html
- voiceover: "Drop in your receipts. Extract the details. Merchant, date, amount—ready to review. Check it once. Create your report. The receipts stay attached."
- sfx: none

handoff_in: identical full cream ground and blank app/header from Frame 1. Exact x120 y190 w1680 h770, opacity1 scale1 rotation0, speed0 directionnone.
Scene 1 (0–2.5s): Three sample receipt file surfaces arrive in the left intake: cafe.jpg, cab.jpg, hotel.jpg. Their face-up digital examples have exact authored merchant/date/amount matching the result; physical footage showed only receipt backs. Cursor presses EXTRACT DETAILS at x400 y825 width330 height72. This is a concise input step, not an elaborate tutorial.
Scene 2 (2.5–6.6s): Rows arrive sequentially in the right review panel: Kindred Cafe / Sep 15 / $6.40; City Cab / Sep 15 / $24.00; North Hotel / Sep 15 / $148.00. Show total $178.40 and "3 receipts · ready to review". `waterfall-entry`, `control-target-sync`.
Scene 3 (6.6–10.5s): Cursor briefly hovers the amounts, then presses CREATE REPORT at x1300 y825 w360 h72. Rows collect into one report with a small attachment strip, not an implied approval or reimbursement claim.
Scene 4 (10.55–14s): Finished report centers at x530 y160 w860 h800. It is titled CLIENT VISIT, carries all three rows, total $178.40, and "3 original receipts attached". Read hold. Full surrounding cream ground remains.
handoff_out: centered report x530 y160 w860 h800 opacity1 scale1 rotation0; cream #F5F0E8 background; report surface #F5F0E8 border rgba(150,91,22,.2), 14px radius; exact shared header/rows/total generated from same helper; speed0 directionnone.

## Frame 3 — Receipts to ready
- scene: The report remains in view while the same hand quietly leaves the desk, then a concise invitation closes the task.
- duration: 8s
- poster: 6.5s
- transition_in: cut
- status: animated
- type: cta
- blueprint: compose
- asset_candidates: tuck-mark.svg
- src: compositions/frames/03-ready.html
- voiceover: "That's the paperwork, done. Now, back to your day. Tuck. Receipts to ready."
- sfx: none

handoff_in: exact centered report from Frame 2, same shared helper, x530 y160 w860 h800 scale1 rotation0 opacity1, speed0 directionnone.
Scene 1 (0–2s): Report moves left and slightly reduces uniformly to x120 y250 scale.72. The cream right cover retracts to reveal fresh later seconds from the same hand take at x1050 y0 w870 h1080. Same camera, wrist and light; simple withdrawal, no new action or facial performance. `card-morph-anchor` plus horizontal mask reveal.
Scene 2 (2–4.5s): "Paperwork done." appears above the report. The hand leaves; the final relaxed desk holds. The report remains readable, especially $178.40 and its attachment count.
Scene 3 (4.5–8s): Product TUCK and CTA "RECEIPTS TO READY ↗" appear along the lower left. Closing frame is a finished report beside the real desk, completing the original receipt-to-report transformation. Hold final state for at least two seconds. Tiny "FICTIONAL PRODUCT · EXAMPLE DATA" footer.
