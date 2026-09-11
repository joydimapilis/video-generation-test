# Seventeen design truth

Concept angle: the film is lit by one screen in one dark room, so the cut rhythm
is a dark frame, a bright frame, a dark frame - and the bright frames are the
ones carrying the plot.

## Palette
| Token | Value | Use |
| --- | --- | --- |
| `--night` | `#0a0c0f` | Film background, between-shot black |
| `--paper` | `#f4f2ed` | Authored product screens |
| `--ink` | `#14181d` | Text on paper |
| `--muted` | `#5f686f` | Secondary labels, units |
| `--accent` | `#2f6df0` | One product blue: live values and the close only |
| `--flat` | `#848c94` | The zero state - deliberately not red, nothing is broken |
| footer text | `#c9ced3` | Footer only - sits on a dark chip, so it takes its own light value rather than `--muted` |

The zero state is grey, not red. Nothing failed; nobody came. That distinction is
the whole film and the palette has to hold it.

## Type
- `SeventeenSans` = Arial / Arial Bold, bundled. Everything.
- Numbers are tabular so a counter does not jitter as it climbs.
- Captions: 64px bold, white, soft drop shadow, no box - they sit on the footage
  and move from beat to beat rather than living in a fixed bar.
- Screen UI: 26-34px, real product proportions, not "designed for camera".

## Layout
- Captions: three positions only - lower-left, lower-centre, upper-left - chosen
  per line so the words never sit on her face or on a live number.
- Authored screens: full-bleed paper, a 1px `--muted` chrome bar at the top, the
  content block optically centred slightly above middle.
- Footer: bottom-right, small, holds the whole runtime.

## Motion
- Footage cuts are hard. No dissolves anywhere; this is a documentary, not a
  montage, and KEEL already owns the crossfade language.
- Authored screens arrive by a 0.18s paper wipe from the left, which reads as a
  screen repainting rather than a graphic animating.
- Numbers tick from a table read as a pure function of time, never incremented.
- The one exception to the hard-cut rule is the final card, which fades up.

## Honesty
Ada and TUESDAY are invented. Every number on screen is a story beat, not a
measurement. Footer reads `ORIGINAL CONCEPT / AI-GENERATED FILM` throughout.
