# Model Selection Rules

## Current Evidence

The first benchmark used the `Reward Pack To App Proof Montage` pattern from `Cero.mp4`.

| Model | Best Use | Evidence |
| --- | --- | --- |
| `kling_3_pro_t2v` | Default for cinematic multi-beat reward/product montage prompts | Highest final score in first benchmark; cleanest city launch, product/app transformation, and checkout proof sequence. |
| `kling_2_6_pro_i2v` | Single-shot continuation from a real keyframe or supplied product image | Preserved the source keyframe and neon reward motion best, but did not cover the full montage structure as well. |
| `wan_2_1_t2v` | Cheap exploration and rough animatics | Captured several broad motifs at low cost, but produced weaker layout, UI, and text consistency. |
| `krea_wan_14b_t2v` | Cheap static product/app concept exploration | Coherent low-cost lime app scene, but ignored the multi-beat montage structure in the first smoke test. |
| HyperFrames | Controlled overlays, UI text, score cards, captions, end cards, and final assembly | Generated models invent UI/text. Deterministic rendered overlays are needed before production use. |

## Draft Rule

For reward-app/product proof ads:

1. Use `wan_2_1_t2v` to explore broad visual directions cheaply.
2. Use `kling_3_pro_t2v` for the main generated montage candidate.
3. Use `kling_2_6_pro_i2v` when a specific product/keyframe must remain visually anchored.
4. Use HyperFrames to replace generated app screens, claims, counters, typography, and final end-card structure.

## Variant-Level Rules

- `full_montage`: use `kling_3_pro_t2v` for commercial coherence, but keep the longer reverse-engineered prompt when close reference structure matters. Shortened prompts drift more.
- `single_shot_launch`: use `kling_2_6_pro_i2v` from the city-launch keyframe. This is the strongest current result and should become the opening-hook generator.
- `checkout_proof`: use `kling_2_6_pro_i2v` from a checkout keyframe. It produces the strongest grounded proof shot, then HyperFrames should replace the phone UI.
- `wan_2_1_t2v`: use as a cheap style exploration tool. It is useful for discovering alternate moods, but should not be trusted for final UI, exact product identity, or close reconstruction.
- `krea_wan_14b_t2v`: keep in the cheap exploration tier for simple product/app tabletop scenes. Do not use it as the primary montage reconstruction model yet.
