#!/bin/bash
# Rebuild the editable document from build_edit.py (run from the project root).
set -euo pipefail
T=/Users/joydimapilis/conductor/workspaces/video-generation-test/reykjavik/demo-videos/scripts/tsrct
P=Save-the-Learnings-Opus-5.5-AI-Voice.tsrct
python3 .tesseract-work/build_edit.py
$T project commit --project $P --file .tesseract-work/editable.json
$T project apply --project $P --actions .tesseract-work/keyframes.json
