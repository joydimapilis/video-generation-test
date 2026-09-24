#!/bin/bash
# Regenerate the AI-voice timeline and save it into the .tsrct (run from the project root).
# build_edit.py lays out the original edit on its original clock; warp.py re-times it
# onto the AI narration (voice_timeline.json from voice_plan.py) and swaps in AI voice + captions.
set -euo pipefail
T=/Users/joydimapilis/conductor/workspaces/video-generation-test/reykjavik/demo-videos/scripts/tsrct
P=Video-Workflow-Demo-Opus-5.5-AI-Voice.tsrct
cd .tesseract-work && python3 build_edit.py && python3 warp.py && cd ..
$T project commit --project $P --file .tesseract-work/editable.json
$T project apply --project $P --actions .tesseract-work/keyframes.json
