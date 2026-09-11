# The Sunday Problem design truth

Concept angle: a testimonial is believable in proportion to how little it claims,
so the design stays out of the way - the only things on screen are her words, her
name, and the mark of the thing she is talking about.

## Palette
| Token | Value | Use |
| --- | --- | --- |
| `--crumb` | `#f3ede3` | Close card ground, lower-third plate |
| `--crust` | `#3a2a1d` | Text on cream |
| `--proof` | `#1f5b3f` | The one accent: the wordmark's mark and the close rule |
| `--paper` | `#ffffff` | Captions and the brand mark over footage |
| `--shadow` | `rgba(24,16,10,.55)` | Caption drop shadow so white holds over warm footage |

No accent appears over footage at all. The green exists only on the cream card and
in the small brand mark, so the interview itself is never dressed.

## Type
- `RotaSerif` = Big Caslon, bundled. The ROTA wordmark and the close card only.
  A warm old-style serif because the brand lives among bread and wood, and because
  no previous film used it.
- `RotaSans` = Arial / Arial Bold, bundled. Captions, the lower third, the footer.

## Layout
- Captions: bottom-centre, 46px, white with a soft shadow and no box, max width
  1480px, one line of speech at a time. They sit where the Chowdeck reference puts
  them because that is where the format's audience expects to read them.
- Brand mark: top-left, small, white, present on every footage shot - the
  watermark convention of the case-study genre.
- Lower third: appears once, early, on a cream plate - her name and what she runs.
  It never returns; a testimonial only has to introduce its speaker once.
- Footer: bottom-right, small, holds the whole runtime.

## Motion
- Cuts between speaker and b-roll are hard. An interview does not dissolve.
- Captions cut with the line, no fade longer than 0.14s - a caption that eases in
  lags the voice and reads as a subtitle track rather than as speech.
- The lower third slides up 18px over 0.3s and leaves the same way.
- The close card is the only fade.

## Honesty
Mara, Second Shift Bakery and ROTA are invented. "About nine minutes" is a story
beat, not a measurement. Footer reads `ORIGINAL CONCEPT / AI-GENERATED FILM`
throughout.
