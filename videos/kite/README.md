# Kite — Ask, plan, review

**Rendered result: 42 seconds, 1080×1920, 30fps, narration, music and burned-in captions.**

[Watch the video](../../artifacts/final_outcome/kite/kite.mp4) · [Player and crop versions](../../artifacts/final_outcome/kite/review.html) · [Delivery report](DELIVERY_REPORT.md)

The user explicitly authorized rendering. The result is a labelled illustrative reconstruction based on public product documentation; current signed-in UI fidelity and campaign tracking remain release checks. The material below records the earlier storyboard review.

Open [review.html](review.html) for the nine sketches and exact 9:16 / 1:1 / 16:9 crop toggles. The HTML embeds its font and official logo, so the static review remains portable. [COPY.md](COPY.md) lists every spoken, caption and screen string. [PRODUCTION_PLAN.md](PRODUCTION_PLAN.md) covers seven shots, library evidence, routing, assets and acceptance criteria. The supplied brief is preserved in user_script.txt.

HyperFrames Studio: `http://localhost:3026/?view=storyboard#project/kite`. Restart with `npx hyperframes preview --background --port 3026` from this folder if necessary. Static composition sources are under compositions/frames; their status remains outline because approval is pending. The live index.html now contains the animated film. The individual sketch files and review.html preserve the preproduction board.

Review exports: `../../artifacts/kite/storyboard.pdf`, `storyboard-wide.png`, `storyboard-square.png`, `storyboard-portrait.png`. These are storyboard artifacts, not final video crop checks.

Validation on 2026-09-17: HyperFrames 0.8.45 check passes with zero lint/runtime/layout/motion findings; 40/40 sampled text contrast checks pass. Separate browser bounds check places all required text and logo boxes inside x108–972, y690–1230 for all nine static frames. Six spoken lines match the user brief exactly; caption groups reconstruct them word for word. Initial header overlap was repaired and rechecked. UI, audio and moving transitions are not production-validated yet.

Budget: $0 generation cost under the same persistent $10 cap in budget.json. Planned S1–S7: HyperFrames; planned voice/music: local generation. No I2V, people or source photographs. No reference-library footage is used.

Creative approval covers the nine-frame direction and verbatim voiceover/headline copy. Before final rendering, complete the five requirements in COPY.md: CTA destination, current UI verification, confirmed or replaced labels, no implication of completed publication, and accurate reconstruction of product behavior. The scenario explicitly uses Propose first because current documentation also offers Act first. Public-source inspection does not substitute for signed-in product verification or campaign approval.

The user's exact-copy correction is preserved in [COPY_REVIEW_POLICY.md](COPY_REVIEW_POLICY.md). All supplemental approval-state labels and behaviors remain proposals until verified. [PRODUCT_VERIFICATION.md](PRODUCT_VERIFICATION.md) separates documented terminology from unverified screen text and interactions. Final rendering requires that verification; the correction itself is not storyboard approval.

Archive-only storyboard rebuild (overwrites the film index; run build_kite_video.py afterward to restore it): `.venv/bin/python scripts/prepare_kite_storyboard.py`. This uses already captured local fonts and the official logo, and the existing lab's GSAP asset. Captured assets and runtime outputs are ignored in Git; retain them locally. The portable review.html already contains what it needs for visual review.


## Rebuild the rendered film

From the repo root, run `.venv/bin/python scripts/prepare_kite_audio.py`, then `.venv/bin/python scripts/build_kite_video.py`, `npm --prefix videos/kite run check`, and `npx hyperframes@0.8.45 render videos/kite -f 30 -q delivery -o <absolute-output-path>/kite.mp4`. Run `node scripts/verify_kite_geometry.cjs` and `.venv/bin/python scripts/finalize_kite_video.py` to recreate the crop versions and delivery checks. No paid API requests are made.
