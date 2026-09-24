# Save the Learnings — Opus 5.5 version

**This is the Claude Opus 5.5 edit.** It uses the same brief, footage, narration,
and script as the Astra edit in `../save-the-learnings/`, but was built from
scratch as a separate project. The Astra project was not modified.

| File | What it is |
|---|---|
| `Save-the-Learnings-Opus-5.5.mp4` | Final render: 20.5 s, 1920×1080, 30 fps, H.264 + AAC stereo, −16.0 LUFS / −1.2 dBTP |
| `Save-the-Learnings-Opus-5.5.tsrct` | Editable Tesseract project, with all media and the font embedded |
| `Save-the-Learnings-Opus-5.5.reverse-engineering.md` | How it was made: cut map, audio trims, revisions, checks, and limits |
| `Captions.srt` | Optional subtitle sidecar (captions are already burned in) |
| `Script.txt` | Supplied script |
| `Assets/` | Original MOV and M4A (byte-identical), original-frame holds, the font and its license, and `SOURCES.md` |
| `Previews/` | Encoded one-second filmstrip, project filmstrip, heading match-cut strip, and poster |
| `.tesseract-work/` | `build_edit.py` (generates the whole timeline), `rebuild.sh`, editable JSON, keyframes, transcripts, and check reports |

## Edit summary

- **Pauses:** removes 1.8 s of leading silence and shortens three internal pauses
  by 0.12–0.24 s each. Speed and words are untouched.
- **Opening:** a slow push-in from the whole app to the document. An amber
  highlight lands on the `…reverse-engineering.md` file path on "reverse".
- **Middle:** the real scroll plays at 1.26× and lands on "Prompts". Then each
  spoken item (prompts, structure, methods, revisions, learnings) cuts to its
  actual heading. Every heading sits in the same screen position with the same
  highlighter swipe (a match cut).
- **Ending:** on "the workflow also checks" the camera pans to the file tree. It
  highlights the reverse-engineering file on "this file", then extends the box to
  its `final_outcome` folder, and ends with a short fade.
- **Captions:** 11 phrase captions in IBM Plex Sans on dark pills.
- **Sound and footage:** no music, SFX, or generated footage.

## Re-export

From the Reykjavik workspace root:

```sh
./scripts/tsrct export --project save-the-learnings-opus-5-5/Save-the-Learnings-Opus-5.5.tsrct --fps 30 --resolution 1080p --output save-the-learnings-opus-5-5/Save-the-Learnings-Opus-5.5.mp4
```

The delivered MP4 is this export, remuxed losslessly (`-c copy`) to add the title
tag "Save the Learnings — Opus 5.5 version".
To regenerate the timeline after editing `build_edit.py`, run
`.tesseract-work/rebuild.sh` from this folder.
