# Demo Videos workspace

This folder is the Demo Videos workspace. It is separate from the Amarillo video-generation system at the repository root and does not depend on it.

| Project | What it is |
| --- | --- |
| `video-workflow-demo-opus-5-5/` | Video Workflow Demo, Opus 5.5 edit with the recorded narration |
| `video-workflow-demo-opus-5-5-ai-voice/` | Same demo narrated by an AI voice (includes the pre-UI-fix version) |
| `video-workflow-demo-opus-5-5-ai-voice-v2/` | AI voice v2, re-voiced to match the reference read |
| `video-workflow-demo-opus-5-5-ai-voice-v3/` | AI voice v3, ElevenLabs narration |
| `save-the-learnings/` | Save the Learnings, first Tesseract editing test |
| `save-the-learnings-opus-5-5/` | Save the Learnings, Opus 5.5 edit |
| `save-the-learnings-opus-5-5-ai-voice/` | Save the Learnings, Opus 5.5 edit with AI voice |
| `tesseract-preview/` | Three-second setup smoke test |
| `scripts/tsrct`, `.agents/skills/` | Workspace Tesseract launcher and the pinned official skills |

Each project folder keeps its script, source assets and licenses, audio, previews, notes (`README.md`, `*.reverse-engineering.md`), and authoring files (`.tesseract-work/`) together.

## Large media

Screen recordings (`.mov`), renders (`.mp4`), and editable Tesseract projects (`.tsrct`) are about 10 GB, and many exceed GitHub's 100 MB file limit. They are excluded by `.gitignore` and stay in the local workspace. [`MEDIA_MANIFEST.md`](MEDIA_MANIFEST.md) lists every excluded file with its size and SHA-256, so a local copy can be verified.

# Tesseract setup

Workspace-local installation of [Tesseract by Mirage](https://github.com/mirage-hq/Tesseract), following its [official installation guide](https://github.com/mirage-hq/Tesseract/blob/main/skills/tesseract-video/references/installation.md).

- Host: macOS 26.5.1, Apple Silicon (`Darwin arm64`). The bundle requires macOS 14.0.0 or later.
- Official skills: `demo-videos/.agents/skills/tesseract-video` and `demo-videos/.agents/skills/tesseract-motion`, from commit `7c0e3a0243355c7d3eb0057d619ba1055219ec4e`.
- Required and installed CLI: **0.2.0**, build `91214aa14b4e2bd9c48622ab0419cb7f288b3e48`.
- Runtime: `.context/tesseract/runtime` at the workspace root; installed with the official `install.sh` custom prefix. No global installation or shell profile edits.
- Use `./scripts/tsrct` from this `demo-videos/` directory (project READMEs assume it), or its absolute path from elsewhere. It sets a workspace temp directory and uses macOS sandbox-exec to restrict CLI file writes to this workspace (plus `/dev/null`). This also prevents changes to global telemetry settings/state. It does not change existing telemetry preferences or block all network access.

```sh
./scripts/tsrct --version
./scripts/tsrct export --project tesseract-preview/Preview.tsrct --output tesseract-preview/Preview.mp4
```

Both local skills are available for subsequent turns. `demo-videos/AGENTS.md` records the local launcher and project conventions.

## Verification

Downloaded the pinned `tesseract-0.2.0-darwin-arm64.zip` and matching `.sha256` from the official v0.2.0 release. `shasum -a 256 -c` passed:

```text
c5a0ab2d7840a3bfee60270d8f9b365f4e5ce8833142bbf9a42beea3d5419ca0
```

The official installer also verified all bundle checksums and launched the versioned executable. Archive, checksum, extracted installer, and install log remain under `.context/tesseract/` (gitignored). The native runtime needs no Node installation.

`tesseract-preview/` contains the three-second smoke test: editable text, shapes, opacity and position keyframes, embedded font, source font/license, authoring JSON, filmstrip, and MP4. The MP4 is H.264, 1920×1080, 30 fps, 90 decoded frames, exactly 3 seconds. Full FFmpeg decode passed. Poster and ten sampled animation poses were visually inspected; real-time playback was not available to the agent. This intentional silent test does not validate footage codecs or an audio mix.

A Space Grotesk variable-font import failed with `face 0 selection names do not match its semantic family/styles`. The test uses static Abel Regular, which imports, embeds, and renders successfully. This is a font-specific limitation, not a runtime installation failure.

Keep each future video's editable project, original footage and other source assets, licenses, previews, and finished render in the same project folder. Do not store user deliverables only in `.context/`.
