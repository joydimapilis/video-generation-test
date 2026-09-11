# ORRIN design truth

Concept angle: precision photographed the way a machine shop lights its own work
— one hard source, deep black, and the measurement written beside the object.

## Palette
| Token | Value | Use |
| --- | --- | --- |
| `--void` | `#07080a` | Background behind every plate and card |
| `--panel` | `#0d1013` | Annotation plates, spec rules |
| `--line` | `#23282c` | Hairlines, leader lines, grid |
| `--ink` | `#e9ecea` | Headline and primary readout |
| `--muted` | `#79817f` | Units, secondary labels, footer |
| `--amber` | `#ff9b2f` | The instrument's ring; one accent only |

The amber appears in generated footage as the module's ring. Authored amber is
reserved for the single live value on screen, never for decoration.

## Type
- `OrrinSans` = Arial / Arial Bold, bundled. Headlines only, tracking `-0.02em`,
  weight 700. Used at 96-132px.
- `OrrinMono` = Andale Mono, bundled. Every annotation, spec row, unit, index and
  footer. 22-32px, tracking `0.08em`, uppercase for labels only.

Two families, no third. Monospace carries all technical voice; the grotesk only
ever speaks the four headline beats.

## Layout
- Focal element: the instrument, always off-centre, always with one clear third.
- Edge anchors: a monospace frame index top-left (`01 / MATERIAL`), a running
  timecode-style readout bottom-right.
- Supporting detail: annotation labels attached to the object by a 1px leader
  line with a 5px terminal dot. Labels sit in negative space the generated plate
  left clear, never over the object.
- Background treatment: full-bleed video plate, a `--void` vignette at the edges,
  and a 1px `--line` safe-area rule inset 64px that never animates.

## Motion
Everything is mechanical. Labels do not fade in softly; they arrive by leader
line drawing to its terminal dot, then the text types or steps in. No easing
softer than `power2`. No bounce, no elastic, no drift.

## Honesty
Every number on screen is a property of the fictional concept, not a measured
result. The footer carries `ORIGINAL CONCEPT / AI-GENERATED FILM` for the whole
runtime.
