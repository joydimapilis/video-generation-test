"""Verify the final webinar film and write its self-contained local handoff."""
from pathlib import Path
import json, subprocess, hashlib, shutil
from PIL import Image, ImageDraw
R=Path(__file__).resolve().parents[1]
P=R/'videos/kite-webinar'; D=R/'artifacts/final_outcome/kite-webinar'
movie=D/'kite-webinar.mp4'
meta=json.loads(subprocess.check_output(['ffprobe','-v','error','-count_frames','-show_format','-show_streams','-of','json',str(movie)]))
v=next(s for s in meta['streams'] if s['codec_type']=='video')
a=next(s for s in meta['streams'] if s['codec_type']=='audio')
assert (v['width'],v['height'])==(1920,1080)
assert v['avg_frame_rate']=='30/1'
assert int(v['nb_read_frames'])==1170
assert abs(float(meta['format']['duration'])-39)<.06
subprocess.run(['ffmpeg','-v','error','-i',str(movie),'-f','null','-'],check=True)
times=[2.8,8.6,12,15.5,19,24,28.6,30.8,33.7,37]
sheet=Image.new('RGB',(1278,1040),'#171717'); draw=ImageDraw.Draw(sheet)
for i,t in enumerate(times):
 frame=D/f'frame-{t}.jpg'
 subprocess.run(['ffmpeg','-v','error','-y','-ss',str(t),'-i',str(movie),'-frames:v','1',str(frame)],check=True)
 im=Image.open(frame).resize((426,240)); x=i%3*426; y=i//3*260
 sheet.paste(im,(x,y+20)); draw.text((x+8,y+3),f'{t}s',fill='white')
sheet.save(D/'contact-sheet.jpg',quality=92)
shutil.copy(D/'frame-19.jpg',D/'poster.jpg')
checks=json.loads((R/'artifacts/kite-webinar/check-final.json').read_text())
assert checks['ok']
levels=subprocess.run(['ffmpeg','-hide_banner','-i',str(movie),'-af','volumedetect','-vn','-sn','-dn','-f','null','-'],capture_output=True,text=True,check=True)
(D/'audio-levels.txt').write_text(levels.stderr)
result={'verified':True,'duration':float(meta['format']['duration']),'width':v['width'],'height':v['height'],'fps':30,'frames':int(v['nb_read_frames']),'video_codec':v['codec_name'],'audio_codec':a['codec_name'],'bytes':movie.stat().st_size,'sha256':hashlib.sha256(movie.read_bytes()).hexdigest(),'full_decode':'passed','checks':checks['ok'],'generation_cost_usd':0,'ui':'Labelled illustrative reconstruction; signed-in UI not verified.'}
(D/'verification.json').write_text(json.dumps(result,indent=2))
(D/'budget.json').write_text(json.dumps({'limit_usd':10,'total_generation_cost_usd':0,'paid_generation_calls':0,'narration':'Local cached Kokoro af_heart','music':'New deterministic local score','visuals':'Deterministic SVG, HTML and GSAP'},indent=2))
report='''# Kite — The webinar request

39-second screen-led marketing film. 1920×1080 at 30fps. A single request in Slack becomes a short plan, webinar signup-page draft and invitation, followed by a human revision. The final output remains drafts in the thread. No public send or publication is depicted.

## Production

Completely new script and task, produced autonomously under the latest brief. HyperFrames 0.8.46, GSAP and deterministic SVG for accurate screen text. Local Kokoro af_heart narration. Newly composed local score and restrained UI cues, with music carved around voice. Official Kite wordmark and Onest font. No human footage or generative video was needed. Total generation cost: $0 of the $10 limit.

## Library references

- Remotion Agent Skills: action-first opening and a short, legible product result.
- Lovable Introducing a smarter Lovable: focused product views and cursor-led attention.
- Notion Introducing Custom Agents: concrete work outputs grouped around a conversation.

The referenced files and review sheets are recorded in artifacts/kite-webinar/references/manifest.json. No library footage or audio was reused.

## Product fidelity

The workflow uses the current public [Kite approvals documentation](https://docs.kite.ai/slack/approvals) and [what Kite posts](https://docs.kite.ai/slack/what-kite-posts): website draft Preview/Review controls, copy returned in thread, and revisions requested through thread feedback. Screens are explicitly labelled Illustrative workflow and Sample company. Their signed-in geometry has not been verified. No customer data, invented performance claims, native approval badges or public-action confirmation is shown.

The end card uses a text-only Add Kite to Slack CTA. No campaign tracking URL was supplied or invented.

## Verification

HyperFrames runtime, layout, contrast and motion assertions pass. The sole lint warning concerns five sequential caption clips on one track, not a visual defect. All principal scene snapshots were inspected. The delivered MP4 has 1,170 frames, 39 seconds, 1920×1080 at 30fps, with video and audio streams. Full FFmpeg decoding passes. Verification and audio levels are alongside the video.

## Rebuild

Editable project: videos/kite-webinar. Run scripts/prepare_kite_webinar_audio.py to prepare local audio and scripts/build_kite_webinar.py to rebuild the composition. Rebuilding HTML removes the audio-carve attributes; rerun the HyperFrames audio carve for music-bed against narration, then npm run check and npm run render from the project directory.
'''
(D/'REPORT.md').write_text(report); (P/'DELIVERY_REPORT.md').write_text(report)
(P/'README.md').write_text('# Kite — The webinar request\n\n39-second screen-led product film. See DELIVERY_REPORT.md for sources, verification and rebuild instructions.\n\nFinal movie: ../../artifacts/final_outcome/kite-webinar/kite-webinar.mp4\n')
(P/'BRIEF.md').write_text((P/'BRIEF.md').read_text().replace('status: production','status: rendered'))
(D/'review.html').write_text('''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Kite — The webinar request</title><style>body{margin:0;background:#171717;color:#f6f3ed;font:16px system-ui}main{max-width:1200px;margin:32px auto;padding:0 20px}video{width:100%;display:block;background:#000;border-radius:12px}a{color:#ff9563}p{line-height:1.6}</style><main><video controls playsinline preload="metadata" poster="poster.jpg" src="kite-webinar.mp4"></video><p>Kite — The webinar request · 39 seconds · 1080p<br><a href="kite-webinar.mp4" download>Download MP4</a> · <a href="REPORT.md">Production notes</a></p></main></html>''')
(R/'assembled_outputs/kite-webinar.json').write_text(json.dumps({'name':'Kite — The webinar request','video':str(movie.relative_to(R)),'player':str((D/'review.html').relative_to(R)),'duration_seconds':39,'generation_cost_usd':0,'resolution':[1920,1080],'verification':str((D/'verification.json').relative_to(R))},indent=2))
print(json.dumps(result,indent=2))
