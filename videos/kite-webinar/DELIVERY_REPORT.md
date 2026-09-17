# Kite — The webinar request

39-second screen-led marketing film. 1920×1080 at 30fps. A single request in Slack becomes a short plan, webinar signup-page draft and invitation, followed by a human revision. The final output remains drafts in the thread. No public send or publication is depicted.

## Production

Completely new script and task, produced autonomously under the latest brief. HyperFrames 0.8.46, GSAP and deterministic SVG for accurate screen text. Local Kokoro af_heart narration. Newly composed local score and restrained UI cues, with music carved around voice. Official Kite wordmark and Onest font. No human footage or generative video was needed. Total generation cost: $0 of the $10 limit.

## Library references

- Remotion Agent Skills: action-first opening and a short, legible product result.
- Lovable Introducing a smarter Lovable: focused product views and cursor-led attention.
- Notion Introducing Custom Agents: concrete work outputs grouped around a conversation.

The referenced files and review sheets are recorded in artifacts/kite-webinar/references/manifest.json. No library footage or audio was reused.

## Product fidelity

The workflow uses the current public [Kite approvals documentation](https://docs.kite.ai/slack/approvals) and [what Kite posts](https://docs.kite.ai/slack/what-kite-posts): website draft Preview/Review controls, copy returned in thread, and revisions requested through thread feedback. Screens are explicitly labelled Illustrative workflow and Sample company. Their signed-in geometry has not been verified. No customer data, invented performance claims, native approval badges or public-action confirmation is shown.

The end card uses a text-only Add Kite to Slack CTA. No campaign tracking URL was supplied or invented.

## Verification

HyperFrames runtime, layout, contrast and motion assertions pass. The sole lint warning concerns five sequential caption clips on one track, not a visual defect. All principal scene snapshots were inspected. The delivered MP4 has 1,170 frames, 39 seconds, 1920×1080 at 30fps, with video and audio streams. Full FFmpeg decoding passes. Verification and audio levels are alongside the video.

## Rebuild

Editable project: videos/kite-webinar. Run scripts/prepare_kite_webinar_audio.py to prepare local audio and scripts/build_kite_webinar.py to rebuild the composition. Rebuilding HTML removes the audio-carve attributes; rerun the HyperFrames audio carve for music-bed against narration, then npm run check and npm run render from the project directory.
