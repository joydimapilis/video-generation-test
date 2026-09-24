# Demo Videos workspace (Reykjavik)

Use Tesseract by Mirage for video edits and motion graphics requested here.
Read `demo-videos/.agents/skills/tesseract-video/SKILL.md` for footage editing or
`demo-videos/.agents/skills/tesseract-motion/SKILL.md` for focused motion graphics.
Both official skills are installed locally and pin CLI 0.2.0.

Always invoke the absolute workspace path to `demo-videos/scripts/tsrct`; it
selects the verified workspace runtime and confines CLI file writes to this
workspace. Do not use or update a global Tesseract installation. The local
runtime is `.context/tesseract/runtime/bin/tsrct` at the workspace root. Do not
change shell profiles or global agent skills. Keep all demo-video work inside
`demo-videos/`; do not modify the Amarillo video-generation system at the
repository root, Brasilia, or existing video-generation projects.

Keep each deliverable's `.tsrct`, final render, original source assets, licenses,
useful previews, and retained authoring files together in its project folder
under `demo-videos/`. Create a fresh project directory for a new video; preserve
existing projects. `tesseract-preview/` is the setup smoke test, not a user
footage project.

`.mov`, `.mp4`, and `.tsrct` files are too large for Git and stay local (see
`.gitignore`). When adding or replacing them, regenerate `MEDIA_MANIFEST.md`.
