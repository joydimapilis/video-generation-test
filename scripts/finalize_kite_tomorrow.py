"""Verify a completed render and write the local handoff artifacts."""
from amarillo.delivery import require_reverse_engineering

from pathlib import Path
import json,subprocess,hashlib,shutil
from PIL import Image,ImageDraw
R=Path(__file__).resolve().parents[1];P=R/'videos/kite-tomorrow';D=R/'artifacts/final_outcome/kite-tomorrow';movie=D/'kite-tomorrow.mp4'
require_reverse_engineering(movie)
meta=json.loads(subprocess.check_output(['ffprobe','-v','error','-count_frames','-show_format','-show_streams','-of','json',str(movie)]))
v=next(s for s in meta['streams'] if s['codec_type']=='video');a=next(s for s in meta['streams'] if s['codec_type']=='audio')
assert (v['width'],v['height'])==(1920,1080)
assert v['avg_frame_rate']=='30/1'
assert int(v['nb_read_frames'])==1140
assert abs(float(meta['format']['duration'])-38)<.06
subprocess.run(['ffmpeg','-v','error','-i',str(movie),'-f','null','-'],check=True)
for t in [1.5,5.2,10,15.5,23,27,31.5,33.5,37]:
 subprocess.run(['ffmpeg','-v','error','-y','-ss',str(t),'-i',str(movie),'-frames:v','1',str(D/f'frame-{t}.jpg')],check=True)
sheet=Image.new('RGB',(1440,870),'#171717');draw=ImageDraw.Draw(sheet)
for i,t in enumerate([1.5,5.2,10,15.5,23,27,31.5,33.5,37]):
 im=Image.open(D/f'frame-{t}.jpg').resize((480,270));x=i%3*480;y=i//3*290;sheet.paste(im,(x,y+20));draw.text((x+8,y+3),f'{t}s',fill='white')
sheet.save(D/'contact-sheet.jpg',quality=90)
shutil.copy(D/'frame-1.5.jpg',D/'poster.jpg')
result={'verified':True,'duration':float(meta['format']['duration']),'width':v['width'],'height':v['height'],'fps':30,'frames':int(v['nb_read_frames']),'video_codec':v['codec_name'],'audio_codec':a['codec_name'],'bytes':movie.stat().st_size,'sha256':hashlib.sha256(movie.read_bytes()).hexdigest(),'full_decode':'passed','checks':json.loads((R/'artifacts/kite-tomorrow/check-final.json').read_text())['ok'],'human':'Veo 3.1 Fast I2V after two rejected Kling takes','generation_credits_quoted':31.38}
(D/'verification.json').write_text(json.dumps(result,indent=2))
report='''# Kite — Tomorrow

38-second 1920×1080, 30fps launch film. The recommended new concept was produced following the user's request to continue and provide the output. The previous film remains intact.

A marketer has an approaching launch and an empty page. Kite develops a launch-page draft from release notes, the marketer redirects the headline, and the revised draft becomes the payoff. No public send or publication is shown.

## Production

- One newly generated source photograph, inspected before animation.
- Two Kling 3 Pro I2V takes rejected for gaze drift; the first 1.8 seconds of a Veo 3.1 Fast I2V take selected after review and played at half speed for the 3.6-second opening. Later gaze drift is excluded.
- Precise, editable HyperFrames UI and typography in four sub-compositions.
- Short local Kokoro narration; new 38-second Sonilo instrumental; tactile edit cues. Music dynamically carved around the voice.
- Official Kite wordmark and Onest font; fictional Relay company and sample names.
- Library influence: Pocket's natural human framing, Notion's concrete work pressure, Bloom's input-to-output presentation. No library footage reused.

## Fidelity and CTA

Product behavior is based on [Kite's current approvals documentation](https://docs.kite.ai/slack/approvals): website drafts have Preview/Review controls, and thread feedback requests revisions. The UI is a labelled illustrative reconstruction, not verified signed-in footage. No native approval-state badges or publication instructions were invented. The CTA is text-only; a campaign tracking destination has not been supplied.

## Verification

HyperFrames lint, runtime, layout, motion assertions and contrast checks pass. Midpoint and transition samples were inspected. Final MP4: 1,140 frames, 38.000 seconds, 1920×1080 at 30fps, video and audio streams present; complete FFmpeg decode passed. See verification.json for codec details and SHA-256.

## Usage

Paid generation quotes: 31.38 Higgsfield credits total, including both rejected takes and music. One built-in source-image generation; no USD invoice supplied. Local narration, composition and rendering incur no generation API charge. Credits are not represented as a verified dollar amount.

Editable project: videos/kite-tomorrow. Build script: scripts/build_kite_tomorrow.py. Audio script: scripts/prepare_kite_tomorrow_audio.py. Restoring HTML from the builder requires rerunning the audio carve before export.
'''
(D/'REPORT.md').write_text(report);(P/'DELIVERY_REPORT.md').write_text(report)
(R/'assembled_outputs/kite-tomorrow.json').write_text(json.dumps({'name':'Kite — Tomorrow','video':str(movie.relative_to(R)),'player':str((D/'review.html').relative_to(R)),'duration_seconds':38,'resolution':[1920,1080],'verification':str((D/'verification.json').relative_to(R))},indent=2))
print(json.dumps(result,indent=2))
