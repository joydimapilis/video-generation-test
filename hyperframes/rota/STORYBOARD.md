# The Sunday Problem / 36.6 seconds

Nine cuts. Four are dialogue takes, four are b-roll, one is the close card. All
cuts are hard except the close card, which fades up. The dialogue audio runs
CONTINUOUSLY across the b-roll cuts inside a line - the picture cuts away, the
voice does not. That J-cut is what makes an interview read as edited rather than
as clips laid end to end.

## Cut list

| # | in | dur | video | media-start | note |
| ---: | ---: | ---: | --- | ---: | --- |
| 1 | 0.0 | 7.4 | talk_hero_v1 | 0.0 | line 1, stays on her to establish the speaker |
| 2 | 7.4 | 2.2 | broll_dough_v1 | 1.0 | breath between lines |
| 3 | 9.6 | 3.8 | talk_b_v1 | 0.0 | line 2 begins on camera |
| 4 | 13.4 | 3.2 | broll_rota_v1 | 0.6 | cut to the paper rota while she describes rebuilding it; her voice continues |
| 5 | 16.6 | 5.8 | talk_c_v1 | 0.0 | line 3, stays on her - the list is a performance beat |
| 6 | 22.4 | 2.2 | broll_room_v1 | 1.2 | breath |
| 7 | 24.6 | 6.0 | talk_d_v2 | 0.0 | line 4, stays on her through the pause and the smile |
| 8 | 30.6 | 2.0 | broll_oven_v1 | 1.8 | the warm resolve |
| 9 | 32.6 | 4.0 | CLOSE CARD | - | fades up, the only non-hard transition |

`talk_d_v1` is bought and deliberately unused: the model restarted the clause,
dropped the word "back" and slurred "Sundays". `talk_d_v2` replaces it.

## Dialogue audio tracks

Each dialogue plate's audio is a separate `<audio>` element pointing at the same
mp4, muted on the video side. Durations are chosen so the voice spans the b-roll
cut inside its line.

| track | src | data-start | media-start | duration |
| --- | --- | ---: | ---: | ---: |
| A1 | talk_hero_v1.mp4 | 0.0 | 0.0 | 7.4 |
| A2 | talk_b_v1.mp4 | 9.6 | 0.0 | 7.0 |
| A3 | talk_c_v1.mp4 | 16.6 | 0.0 | 5.8 |
| A4 | talk_d_v2.mp4 | 24.6 | 0.0 | 6.0 |

## Captions

Burned-in transcript captions, Chowdeck-style: bottom-centre, 46px Arial Bold,
white, soft drop shadow, no box, max width 1480px, wrapping to two lines when it
must. Timings below are film time, derived from each take's MEASURED Whisper
segment boundaries plus a small tail - not estimated.

| in | out | text |
| ---: | ---: | --- |
| 0.00 | 3.90 | We're a bakery. Six people, two ovens, |
| 4.02 | 6.95 | and a lot of very early mornings. |
| 9.60 | 15.98 | Every Sunday night, I'd sit down with a pencil and rebuild the whole week. |
| 16.60 | 21.90 | Someone's got an exam. Someone's kid is sick. Start again. |
| 24.60 | 26.55 | Now it takes about nine minutes. |
| 27.92 | 29.80 | I got my Sundays back. |

Use ONE caption element whose text comes from a time table read as a pure
function of the clock. Between spans the text is empty.

## Persistent overlays

- **Brand mark**: top-left, `rota` in RotaSerif 34px, white, 62% opacity, on
  cuts 1-8 only, never on the close card.
- **Lower third**: appears once, 1.2s to 5.2s. A cream `--crumb` plate, bottom
  left, inset 96px from the left and sitting above the caption line. Two lines:
  `Mara Osman` at 40px RotaSans Bold `--crust`, and `Owner, Second Shift Bakery`
  at 27px RotaSans `--crust` at 70% opacity. It slides up 18px over 0.3s and
  leaves the same way. It never returns.
- **Footer**: bottom-right, 19px RotaSans, light text on a dark chip, above
  everything including the close card, whole runtime,
  `ORIGINAL CONCEPT / AI-GENERATED FILM`.

## Close card

`--crumb` ground. Centred block:
- `rota` in RotaSerif 140px `--crust`
- immediately beneath the word, a 2px `--proof` rule exactly as wide as the word
- below that, `Shift scheduling for small teams.` in RotaSans 32px `--crust`

No coloured full stop - three previous films closed on a wordmark plus an accent
period and it has become a tic. Fades up over 0.5s.

## Audio

One quiet score across 36.6s, three movements: sparse under the problem, a small
lift from 24.6 as the answer arrives, and a warm settle under the close. It must
stay well out of the way - the voice is the whole point of an interview, and this
is the first film in the series where the dialogue is generated performance rather
than authored narration.

Music ducks during speech. Duck windows, merged from the measured spans with a
0.30s pad: 0.00-7.25, 9.30-22.20, 24.30-30.10. Duck level 0.42, which is deeper
than the previous films because a bed competing with a real voice is worse than a
bed competing with a clean TTS read.
