---
workflow: general-video
flow: automation
storyboard: no
---

# Seventeen: a founder origin story for TUESDAY

One original 42-second 16:9 documentary-style short, delivered as H.264/AAC MP4.
The user delegates every technical decision and reviews only the final video.
Ledger: `artifacts/library-loop-4/budget.json`, hard $10 estimated cap.

TUESDAY is a fictional company and Ada is a fictional person. No real product,
company, metric or person is depicted. A footer identifies the piece as a concept
for the whole runtime.

## Why this genre
The first three films had no characters. ORRIN and KEEL showed only hands; Cue
used one static talking head as a hook. The Clova reference in the library is a
person with an arc, narrated about in the third person over documentary b-roll
and large kinetic captions. It is the only inspected genre where a character
carries the story, and it is the only one left that this system has not tried.

## Why this routing
Character consistency across shots is the known weakness of text-to-video and was
flagged untested in both earlier loops. The fix here is structural rather than a
prompt trick: one hero character frame was generated with text-to-video, and every
other character shot was generated from that exact frame with image-to-video,
which costs the same $0.10/s at 1080p. Because image-to-video continues the scene
it is handed, the film is deliberately a chamber piece - one desk, one night,
three emotional states - and time passes through the authored screens and the
b-roll rather than by relighting the character.

Shots where identity does not read (hands, still lifes, weather, city) stayed on
plain text-to-video. Faceless hands went to Kling, its measured strength.

## The story
Ada ships an app. Nobody comes. She ships it again, sixteen times. On the
seventeenth, one person arrives. Then eleven more. It is not a triumph; it is a
start, and the film is careful not to oversell it.

## Craft targets
- The authored screens carry the plot, not just the branding. The dashboards and
  counters ARE the beats - which puts the system's single strongest measured
  capability at the centre of the story instead of at the edges.
- Light authored screens cut against dark night footage, so the film's rhythm is
  literally the rhythm of a screen in a dark room.
- Kinetic captions that move around the frame, against KEEL's fixed bottom bar.
- Over-coverage again: ten plates bought, eight used, one dropped outright.

## Audio
Narration from the local Kokoro engine, a warm female read in the third person -
deliberately a different voice and register from KEEL's male manifesto. Original
locally synthesized score. Music ducked under narration by an automation envelope
derived from the measured line lengths.

## Acceptance
Full MP4 decode; 1080p; narration audible and unclipped under the bed and
verified against the written script by local transcript; every authored number
and label spelled exactly; no overflow or overlapping text; contrast passes on
every caption and screen; per-channel peak measurement, never a mono downmix.
