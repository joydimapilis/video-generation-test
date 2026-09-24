#!/bin/bash
# Create the AI-voice .tsrct from scratch and package every asset it uses (run from the project root).
set -euo pipefail
T=/Users/joydimapilis/conductor/workspaces/video-generation-test/reykjavik/demo-videos/scripts/tsrct
P=${1:-Video-Workflow-Demo-Opus-5.5-AI-Voice-v3.tsrct}
R=$PWD
$T project create --project "$P"
iv(){ $T project import-video --project "$P" --file "$R/$1" --asset-id "$2"; echo; }
ia(){ $T project import-asset --project "$P" --file "$R/$1" --asset-id "$2" --kind "$3"; echo; }
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
ia Assets/Holds/Hold-Storyboard-Frame1-src5.00s.png hold-f1 image
ia Assets/Holds/Hold-Storyboard-Frame2-src10.20s.png hold-f2 image
ia Assets/Holds/Hold-Storyboard-Frame3-src13.00s.png hold-f3 image
ia Assets/Holds/Hold-fal-top-src0.50s.png hold-fal image
ia Assets/Holds/Hold-Verification-top-src0.80s.png hold-ver-top image
ia Assets/Holds/Hold-Verification-review-src14.00s.png hold-ver-review image
ia Assets/Derived/Kite-soundtrack-pause-removed.wav kite-audio audio
# AI narration: one ElevenLabs file per script sentence (see Assets/SOURCES.md)
for f in Assets/AI-Voice/processed/*.wav; do b=$(basename "$f" .wav); ia "$f" "tts-$b" audio; done
$T project import-font --project "$P" --file "$R/Assets/Fonts/IBMPlexSans-Medium.ttf"; echo
$T project checkout --project "$P" --output .tesseract-work/editable-v0.json
