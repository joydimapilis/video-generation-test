# The Sunday Problem (revised) design truth

Concept angle: a testimonial is believable in proportion to how little it claims.
The design stays out of the way - her words, her name, and two screens that show
the mechanic plainly rather than dressing it.

## Palette
| Token | Value | Use |
| --- | --- | --- |
| `--crumb` | `#f3ede3` | Close card ground, lower-third plate |
| `--crust` | `#3a2a1d` | Text on cream |
| `--proof` | `#1f5b3f` | The one accent: close rule, live values on the product screens |
| `--panel` | `#1a1410` | Ground of the two authored product screens |
| `--panel-ink` | `#f0e9de` | Text on the product screens |
| `--panel-dim` | `#9b8e80` | Secondary labels on the product screens |
| `--panel-line` | `#332a22` | Grid rules and hairlines on the product screens |
| `--paper` | `#ffffff` | Captions over footage |

The product screens are warm near-black, NOT cream. Two reasons: the captions run
continuously over them while she speaks, and white captions would be unreadable on
a light ground; and a dark screen cut against bright bakery footage gives the film
a rhythm it otherwise lacks. Cream is reserved for the close card, where no
caption ever sits.

## Type
- `CrewSerif` = Big Caslon, converted to WOFF2. The Crew wordmark and the close
  card only. Chromium's font sanitiser rejects the raw macOS TrueType face, so the
  .ttf must never be used directly - it silently falls back to a default serif.
- `CrewSans` = Arial / Arial Bold. Captions, lower third, product screens, footer.

## Layout
- Captions: bottom-centre, 46px Arial Bold, white, soft drop shadow, no box, max
  width 1480px, wrapping to two lines when needed. They run over footage AND over
  the product screens - the voice does not stop, so neither do they.
- Brand mark: top-left, `Crew` in CrewSerif 34px, white at 62%, on footage cuts
  only. Never on the product screens (they carry their own mark) or the close card.
- Lower third: once only, 1.2s to 5.2s, cream plate bottom-left above the caption.
- Footer: bottom-right, above everything, whole runtime.

## Motion
- Cuts between speaker, b-roll and product screens are hard. An interview does not
  dissolve.
- Product screen content arrives as rows and cells, staggered, mechanical, nothing
  eased softer than power2. The screens should feel like software updating, not
  like a graphic animating.
- Captions cut with the line; no fade longer than 0.14s.
- The close card is the only fade.

## Honesty
Mara, Second Shift Bakery and Crew are invented. The names on the product screens
are invented staff. "About nine minutes" is a story beat, not a measurement.
Footer reads `ORIGINAL CONCEPT / AI-GENERATED FILM` throughout.
