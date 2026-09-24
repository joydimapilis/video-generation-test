#!/bin/bash
# Regenerate the timeline from build_edit.py and save it into the .tsrct (run from the project root).
set -euo pipefail
T=/Users/joydimapilis/conductor/workspaces/video-generation-test/reykjavik/demo-videos/scripts/tsrct
P=Video-Workflow-Demo-Opus-5.5.tsrct
cd .tesseract-work && python3 build_edit.py && cd ..
$T project commit --project $P --file .tesseract-work/editable.json
$T project apply --project $P --actions .tesseract-work/keyframes.json
