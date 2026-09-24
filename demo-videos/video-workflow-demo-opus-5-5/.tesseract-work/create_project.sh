#!/bin/bash
# Create the .tsrct from scratch and package every asset the edit uses (run from the project root).
# Then run .tesseract-work/rebuild.sh to place the timeline.
set -euo pipefail
T=/Users/joydimapilis/conductor/workspaces/video-generation-test/reykjavik/demo-videos/scripts/tsrct
P=${1:-Video-Workflow-Demo-Opus-5.5.tsrct}
R=$PWD
$T project create --project "$P"
iv(){ $T project import-video --project "$P" --file "$R/$1" --asset-id "$2"; echo; }
ia(){ $T project import-asset --project "$P" --file "$R/$1" --asset-id "$2" --kind "$3"; echo; }
# Footage (Step 2 is packaged as three derived excerpts; see Assets/SOURCES.md)
iv Assets/Derived/Step2-request-src0-20s.mp4 s2-request
iv Assets/Derived/Step2-timelapse-src17-1017s-60x.mp4 s2-timelapse
iv Assets/Derived/Step2-complete-src1012-end.mp4 s2-complete
iv "Assets/Source/Step 3.mov" s3
iv "Assets/Source/Step 4.mov" s4
iv "Assets/Source/Step 4_Part 2.mov" s4p2
iv "Assets/Source/Step 4_Part 3.mov" s4p3
iv "Assets/Source/Step 5.mov" s5
iv "Assets/Source/Step 6.mov" s6
iv "Assets/Source/Step 7.mov" s7
iv "Assets/Source/Step 8.mov" s8
# Original-frame holds
ia Assets/Holds/Hold-Storyboard-Frame1-src5.00s.png hold-f1 image
ia Assets/Holds/Hold-Storyboard-Frame2-src10.20s.png hold-f2 image
ia Assets/Holds/Hold-Storyboard-Frame3-src13.00s.png hold-f3 image
ia Assets/Holds/Hold-fal-top-src0.50s.png hold-fal image
ia Assets/Holds/Hold-Verification-top-src0.80s.png hold-ver-top image
ia Assets/Holds/Hold-Verification-review-src14.00s.png hold-ver-review image
# Narration: full-length, sample-aligned compressed derivatives of each original take file
N=Assets/Derived/Narration
ia $N/Step_1-comp.wav vo1 audio
ia $N/Step_2-comp.wav vo2 audio
ia $N/Step_3-comp.wav vo3 audio
ia $N/Step_4_and_part_2-comp.wav vo4 audio
ia $N/Step_4_Part_3-comp.wav vo4p3 audio
ia $N/Step_5-comp.wav vo5 audio
ia $N/Step_6-comp.wav vo6 audio
ia $N/Step_7-comp.wav vo7 audio
ia $N/Step_8-comp.wav vo8 audio
# Kite video soundtrack from Step 7.mov with the playback pause removed (continuous, 4 ms crossfade)
ia Assets/Derived/Kite-soundtrack-pause-removed.wav kite-audio audio
# Font: IBM Plex Sans Medium (captions and chapter chips)
$T project import-font --project "$P" --file "$R/Assets/Fonts/IBMPlexSans-Medium.ttf"; echo
$T project checkout --project "$P" --output .tesseract-work/editable-v0.json
