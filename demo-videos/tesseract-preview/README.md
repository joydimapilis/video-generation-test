# Setup preview

- `Preview.mp4`: three-second silent 1080p30 H.264 render.
- `Preview.tsrct`: matching portable editable project, including font bytes.
- `Assets/`: original font and redistribution license.
- `Previews/`: poster and ten-frame animation filmstrip.
- `.tesseract-work/`: source actions, editable JSON, build helper, schemas, and probe results.

Reviewed the saved revision's title at 1.5s and filmstrip at
0, 150, 350, 600, 1000, 1500, 2300, 2600, 2800, 2967 ms.
Title fades/moves in, holds, and fades out; the mint marker traverses and returns.
No clipping or missing glyphs observed. The exported MP4 decodes all 90 frames.
Real-time playback and listening were not performed; this test is intentionally silent.

To render again from the workspace root:
`./scripts/tsrct export --project tesseract-preview/Preview.tsrct --output tesseract-preview/Preview.mp4`
