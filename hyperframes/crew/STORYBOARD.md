# The Sunday Problem (revised) / 44.4 seconds

Twelve cuts: six dialogue, four b-roll, two authored product screens, one close
card. All cuts hard except the close card. Dialogue audio runs CONTINUOUSLY across
picture cuts inside a line - the picture cuts away, the voice does not.

Every media-start and caption time below is derived from MEASURED Whisper segment
boundaries, listed under "Measured speech" at the bottom. Nothing here is estimated.

## Cut list

| # | in | dur | video | media-start | note |
| ---: | ---: | ---: | --- | ---: | --- |
| 1 | 0.0 | 7.3 | hero (talk_hero_v1) | 0.0 | line 1. Reused unchanged from the first cut |
| 2 | 7.3 | 2.0 | dough (broll_dough_v1) | 1.0 | breath |
| 3 | 9.3 | 3.3 | line2 (line2_schedule_v1) | 1.10 | line 2 begins on camera; media-start trims a 1.4s lead-in |
| 4 | 12.6 | 3.1 | paper (broll_rota_v1) | 0.6 | the paper staff schedule; her voice continues underneath |
| 5 | 15.7 | 5.6 | linec (line3_pain_v2) | 0.0 | line 3. Re-generated (line3_pain_v2) to remove an offensive hand gesture in the original take |
| 6 | 21.3 | 1.7 | room (broll_room_v1) | 1.2 | breath |
| 7 | 23.0 | 2.6 | line4 (line4_product_v1) | 0.0 | line 4: she names Crew, on camera |
| 8 | 25.6 | 2.6 | SCREEN A | - | availability arriving, under the rest of line 4 |
| 9 | 28.2 | 4.2 | SCREEN B | - | the schedule building, under all of line 5 |
| 10 | 32.4 | 6.0 | line6 (line6_result_v1) | 0.0 | line 6, stays on her through the pause and the smile |
| 11 | 38.4 | 2.6 | oven (broll_oven_v1) | 1.8 | the warm resolve; runs 0.6s under the close card so the card fades over the oven rather than through black |
| 12 | 40.4 | 4.0 | CLOSE CARD | - | fades up |

## Dialogue audio tracks

Each dialogue plate's audio is a separate `<audio>` pointing at the same staged
mp4; the video side is muted. Durations span the picture cuts inside each line.

| track | src | data-start | media-start | duration |
| --- | --- | ---: | ---: | ---: |
| A1 | hero.mp4 | 0.0 | 0.0 | 7.3 |
| A2 | line2.mp4 | 9.3 | 1.10 | 6.4 |
| A3 | linec.mp4 | 15.7 | 0.0 | 5.6 |
| A4 | line4.mp4 | 23.0 | 0.0 | 5.2 |
| A5 | line5.mp4 | 28.2 | 0.0 | 4.2 |
| A6 | line6.mp4 | 32.4 | 0.0 | 6.0 |

## Captions

Bottom-centre, 46px Arial Bold, white, soft drop shadow, no box, max width 1480px.
ONE caption element whose text comes from a time table read as a pure function of
the clock; empty between spans.

| in | out | text |
| ---: | ---: | --- |
| 0.00 | 3.90 | We're a bakery. Six people, two ovens, |
| 4.02 | 6.95 | and a lot of very early mornings. |
| 9.55 | 15.55 | Every Sunday night I'd sit down with a pencil and rebuild the staff schedule. |
| 15.70 | 21.15 | Someone's got an exam. Someone's kid is sick. Start again. |
| 23.00 | 28.00 | We use Crew now. Everyone puts their availability on their phone. |
| 28.20 | 32.10 | It builds the schedule around that, and everyone sees it update. |
| 32.40 | 35.00 | Now the whole schedule takes about nine minutes. |
| 36.66 | 38.20 | I got my Sundays back. |

## SCREEN A - Availability (2.6s, cut 8)

`--panel` ground. `Crew` in CrewSerif 30px `--panel-dim` top-left at 72px inset.
Heading `AVAILABILITY` 26px `--panel-dim`, letter-spacing .18em, below the mark.
Sub-heading `Week of 14 April` 24px `--panel-dim` at the right of the same line.

Four rows in a 1300px column starting 300px from the top, each 86px tall,
separated by a 1px `--panel-line` rule:

| name (34px `--panel-ink`) | what they gave (30px `--panel-dim`, right-aligned) |
| --- | --- |
| Mara | All week |
| Tomas | Mon-Thu |
| Aisha | Not Thursday |
| Joel | Evenings only |

Each row arrives with its text already set, sliding up 16px and fading in over
0.22s, staggered 0.2s apart, starting 0.15s in - so all four have landed by ~1.2s
and the last 1.4s holds. A small `--proof` dot sits 24px left of each name and
appears with its row.

## SCREEN B - The schedule (4.2s, cut 9)

`--panel` ground, same mark and inset. Heading `THIS WEEK'S SCHEDULE` 26px
`--panel-dim`, letter-spacing .18em.

A grid, 1500px wide, starting 300px from the top: five columns headed
`MON TUE WED THU FRI` (24px `--panel-dim`, 1px `--panel-line` rule beneath), and
three rows 96px tall headed at the left by `OPEN`, `MID`, `CLOSE` (24px
`--panel-dim`). Fifteen cells, each containing one first name at 30px
`--panel-ink`, centred:

| | MON | TUE | WED | THU | FRI |
| --- | --- | --- | --- | --- | --- |
| OPEN | Mara | Mara | Tomas | Mara | Mara |
| MID | Tomas | Aisha | Aisha | Tomas | Aisha |
| CLOSE | Joel | Joel | Joel | Joel | Joel |

Cells fill in reading order - left to right, top to bottom - each fading in over
0.14s, staggered 0.09s, starting 0.2s in, so the grid completes at about 1.7s.
Then at 2.3s a line appears centred beneath the grid: a `--proof` dot, then
`Updated - everyone notified` at 28px `--panel-ink`, fading in over 0.3s. It holds
to the end of the cut.

The grid must agree with SCREEN A, because a viewer who checks will check exactly
this: Aisha never appears on Thursday, Tomas never appears on Friday, Joel is on
CLOSE every day because he gave evenings only, and Mara covers the rest. An earlier
draft of this table put Aisha on Thursday and it contradicted the screen before it.

## Close card (4.0s, cut 12)

`--crumb` ground. Centred block:
- `Crew` in CrewSerif 140px `--crust`
- immediately beneath the word, a 2px `--proof` rule exactly as wide as the word
- below that, `Staff scheduling for small teams.` in CrewSans 32px `--crust`

Fades up over 0.5s. No coloured full stop.

## Lower third

Once only, 1.2s to 5.2s. Cream `--crumb` plate, bottom-left, inset 96px, sitting
above the caption line. `Mara Osman` 40px CrewSans Bold `--crust`;
`Owner, Second Shift Bakery` 27px CrewSans `--crust` at 70%. Slides up 18px over
0.3s, leaves the same way.

## Audio

One quiet score across 44.4s, score_volume 0.55. Three movements: sparse under the
problem, a small lift from 23.0 as the product arrives, a warm settle from 38.4.
It must stay well out of the way - the voice is the point.

Duck windows, merged from the measured speech spans with a 0.30s pad, duck level
0.42, 0.25s ramps: 0.00-7.25, 9.25-21.30, 22.70-32.40, 32.10-38.50 merges with the
previous into 22.70-38.50. Final merged set: **0.00-7.25, 9.25-21.30, 22.70-38.50**.

## Measured speech (source of every timing above)

| plate | clip | speech segments |
| --- | ---: | --- |
| hero (talk_hero_v1) | 8.00 | 0.00-3.78, 4.08-6.82 |
| line2 (line2_schedule_v1) | 8.00 | 1.40-7.18 |
| linec (line3_pain_v2) | 6.02 | 0.00-5.34 |
| line4 (line4_product_v1) | 6.02 | 0.00-4.80 |
| line5 (line5_how_v1) | 6.02 | 0.00-3.68 |
| line6 (line6_result_v1) | 8.00 | 0.00-2.42, 4.26-5.42 |
