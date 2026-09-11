# Seventeen / 42 seconds

Fifteen cuts. Six are authored screens and nine are generated plates. All cuts
are hard except the final card, which fades up. Total runtime exactly 42.0s.

## Cut list

| # | in | dur | source | media-start | note |
| ---: | ---: | ---: | --- | ---: | --- |
| 1 | 0.0 | 3.4 | hero_night_v1 | 0.3 | she types, presses a key |
| 2 | 3.4 | 2.6 | AUTHORED A | - | SHIPPED |
| 3 | 6.0 | 3.6 | AUTHORED B | - | ACTIVE USERS 0 |
| 4 | 9.6 | 1.6 | hands_laptop_v1 | 3.0 | the lid closes, light goes out |
| 5 | 11.2 | 2.8 | char_lookup_v1 | 2.2 | she sits back, looks away |
| 6 | 14.0 | 2.0 | window_rain_v1 | 1.0 | rain, city bokeh |
| 7 | 16.0 | 1.8 | coffee_dawn_v1 | 1.2 | cold coffee, last steam |
| 8 | 17.8 | 1.8 | desk_empty_v1 | 1.0 | nobody at the desk |
| 9 | 19.6 | 4.4 | AUTHORED C | - | SHIP LOG, v1.1 to v1.16 |
| 10 | 24.0 | 3.2 | AUTHORED D | - | 0 flips to 1 |
| 11 | 27.2 | 4.2 | char_react_v1 | 1.4 | the smile |
| 12 | 31.4 | 3.4 | AUTHORED E | - | 1 climbs to 12 |
| 13 | 34.8 | 3.4 | char_exhale_v1 | 1.8 | she sits back, settles |
| 14 | 38.2 | 1.8 | city_dawn_v1 | 1.6 | first light. scale 1.36 to crop 140px letterbox |
| 15 | 40.0 | 2.0 | AUTHORED F | - | close card, fades up |

`street_walk_v1` is bought but deliberately unused: the figure reads as a man in
dark clothing rather than the character, and it carries 131px of baked-in bars.

## Narration

Warm female read, third person, Kokoro `bf_emma` at speed 0.94. Starts are fixed;
durations are whatever the engine measures, and the build reads the measured
values rather than an estimate.

| line | start | text |
| --- | ---: | --- |
| l01 | 0.80 | Ada shipped her first app on a Tuesday. |
| l02 | 6.60 | Nobody came. |
| l03 | 11.50 | So she shipped another one. And another. |
| l04 | 20.00 | Sixteen times, nobody came. |
| l05 | 24.40 | On the seventeenth, someone did. |
| l06 | 31.80 | Then eleven more. |
| l07 | 35.40 | It isn't a rocket ship. It's a start. |

## Captions

Captions appear ONLY over generated footage, never over an authored screen - the
screens already carry their own words and doubling them is noise. So only l01,
l03 and l07 are captioned. 64px Arial Bold, white, soft drop shadow, no box.

| line | position |
| --- | --- |
| l01 | lower-left |
| l03 | lower-left |
| l07 | lower-centre |

## Authored screens

All six sit on `--paper` except F. Each enters with a 0.18s wipe from the left
that reveals the paper, reading as a screen repainting. A 1px `--muted` chrome
bar runs across the top of every product screen with `tuesday.app` at its left in
22px `--muted`.

**A - SHIPPED (2.6s).** Centred block: `SHIPPED` at 128px bold `--ink`; below it
`v1.0 · 2:14 AM` at 28px `--muted`; below that a 10px `--accent` dot with `live`
at 26px `--muted` beside it. The dot pulses once, 0.5s in.

**B - ACTIVE USERS 0 (3.6s).** Label `ACTIVE USERS` at 30px `--muted`, letter
spacing .16em. Beneath it `0` at 240px bold in `--flat` grey, tabular. Beneath
that `LAST 7 DAYS` at 26px `--muted`. Across the lower third a perfectly flat
1px `--flat` sparkline, 1100px wide, that draws left to right over 1.6s and never
rises. The grey is deliberate: nothing is broken, nobody came.

**C - SHIP LOG (4.4s).** A left-aligned list of 16 rows in a 1200px column,
starting at the top under the chrome bar. Each row is 44px tall: version at 30px
`--ink` (`v1.1` through `v1.16`), the word `shipped` at 26px `--muted` in the
middle, and a right-aligned `0` at 30px in `--flat`. Rows stagger in over 2.6s -
fast, mechanical, no easing softer than power2. Top right, a running count
`16 RELEASES` at 28px `--muted` that ticks up with the rows from a time table.

**D - ONE (3.2s).** Identical layout to B. The number holds at `0` in `--flat`
for 0.7s, then swaps to `1` in `--accent` with a small 1.0 to 1.08 to 1.0 scale
pop over 0.22s. The sparkline redraws flat and makes a single step up at its
right end as the number changes.

**E - TWELVE (3.4s).** Identical layout again. The number ticks `1` to `12` in
`--accent` over 1.6s, read from a table as a pure function of time, never
incremented. The sparkline rises across its last third. A line appears beneath
`LAST 7 DAYS` reading `+11 THIS WEEK` at 26px `--accent`, 0.4s after the tick
settles.

**F - CLOSE (2.0s).** `--night` background, no chrome bar. Centred: `tuesday.`
at 132px bold white with the final period in `--accent`; a 1px `--accent` rule
280px wide beneath it; `Ship it anyway.` at 40px white below the rule. The whole
card fades up over 0.5s - the only non-hard transition in the film.

## Audio

Original synthesized score, three movements matching the acts: sparse and small
under act one, a little motion under act two, a warm resolve from 24.0. One soft
key-press accent on cut 2 at 3.4, one on cut 10 at 24.0. Music ducked under every
narration line by an automation envelope derived from the measured line lengths.
