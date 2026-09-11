---
workflow: general-video
flow: automation
storyboard: no
---

# KEEL: Built below the waterline

One original 38-second 16:9 narrated brand manifesto, delivered as H.264/AAC MP4.
The user delegates every technical decision and reviews only the final video.
This run has its own ledger at `artifacts/library-loop-3/budget.json` and its own
hard $10 estimated cap.

KEEL is a fictional company. The film makes no product claim, shows no product,
and a footer identifies it as a concept throughout.

## Why this genre
Neither previous film was carried by voice. Cue was a product ad with a spoken
hook; ORRIN was a silent hardware film. The Aurus reference in the library is a
third thing: a narrated manifesto that never shows a product, cuts unrelated
worlds against a spoken argument, and resolves on a logo. Voice and rhythm carry
it, so it exercises the two things the previous films did least - pacing and
transitions.

## Direction
Three acts with a visible turn. Acceleration (cold cyan city, machines, hands
typing) -> descent (open sea, light shafts, deep dark water) -> the work (a boat
shed at dawn, a hand plane, a keel timber). The metaphor is literal by the end:
a keel is the backbone of a ship, built below the waterline, where nobody sees it.

## Craft targets
- **Pacing.** Act one accelerates from 1.6s cuts to 0.35s. Act two slows to ~4s.
  Act three holds. Both previous films ran one flat 4-6s cadence end to end.
- **Transitions.** Three languages, one per act: whip-slide entries with a short
  flash in act one, a dip through black at the turn, and slow opposing-opacity
  crossfades in acts two and three. Both previous films were hard cuts only.
- **Coverage.** 60 seconds of footage bought for a 38-second film, so a weak
  plate can simply be dropped instead of used.
- **Match cut.** Hands typing fast under cold light in act one and hands planing
  timber under warm light in act three share framing and camera move, so the
  film's argument is made once in pictures before the voice makes it.

## Routing
From the two measured loops: Veo 3.1 Fast with `generate_audio: false` for every
environment and landscape plate ($0.10/s at 1080p), Kling 3.0 Pro for the two
faceless-hands plates. No generated plate carries a legible glyph; every readable
character is authored in HyperFrames.

## Audio
Narration from the local Kokoro engine (not signed in to HeyGen; offline voice is
the stated fallback). Original locally synthesized three-act score, ducked under
the narration by an automation envelope derived from the measured line lengths.

## Acceptance
Full MP4 decode; 1080p delivery; narration audible and unclipped under the bed;
captions match the spoken words exactly; no overflow or overlapping text;
contrast passes on every caption; agent review of every plate before selection.
