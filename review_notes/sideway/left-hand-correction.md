# Sideway coffee: left-hand revision

The revised five-second shot changes the free left hand from a spread-finger pose across the trousers to a purposeful move into the outer hip pocket. The fingers finish entering the pocket and stay there. The right hand keeps its coffee-cup grip and supported elbow. The full film remains unchanged.

The first new take (V4) achieves the pocket movement but starts looking toward the camera after about two seconds. Its later footage was rejected. The correction (V5) continues from a reviewed V4 frame at 1.9375s, retaining lowered attention as the hand settles. The delivered sequence uses V4 0–1.9375s (62 frames) followed by V5 0–3.0625s (98 frames), both at native 32fps. No slow motion, freezing, frame interpolation or crossfade is used. The source frame and exact selection are retained in the editable project.

This is a targeted hand improvement for user review. The head bows slightly farther during the continuation; low eyelids and small mouth changes remain. It is not approval of every facial-realism dimension. Original identity, wardrobe, background and framing are retained as closely as generation permits. The pocket movement is a new prompt hypothesis; it was not copied from sample02 or supplied through video motion control.

Outputs: `sideway-coffee-left-hand-revised.mp4` (720×1280, 5s, 32fps) and `sideway-coffee-left-hand-comparison.mp4` (1920×1080, 5s, 24fps). Both are intentionally silent. The comparison shows the original film take, previous rejected hand trial, and revised sequence at native speed. The full six-second original slot has not been replaced. Full source takes remain in `takes/`.

Two new calls cost $0.20 estimated / $0.24 reserved. Cumulative Sideway: $10.57 estimated / $12.21 reserved against the explicitly approved $12.25 cap. Confirmed invoice charges remain unavailable; original image allowances remain reserved. No additional image generation was charged.

Review used complete FFmpeg decoding, chronological 4fps full-body frames, 8fps face/cup detail frames, and consecutive encoded frames across the join. At the join, pose and prop placement align with a slight texture change; no large spatial jump appears in the reviewed frames. These are sampled visual judgments, not uninterrupted playback or calibrated realism scores. HyperFrames 0.8.50 checks passed without errors or warnings. The earlier comparison remains on 0.8.49 and was not changed.

Editable project: `videos/sideway-human-realism-test/coffee-left-hand/`. Local rebuild scripts: `assemble_coffee_revision.py` then `build_coffee_comparison.py` in its parent directory. Neither submits paid generation. Run `npm run render -- --quality delivery --fps 24 --workers 2 --output <output.mp4>` inside the editable project for the comparison.
