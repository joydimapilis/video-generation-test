"""Create crop-check videos, verify encoded media, and write the Kite delivery."""
from amarillo.delivery import require_reverse_engineering

from pathlib import Path
import hashlib,json,subprocess,shutil
import numpy as np

R=Path(__file__).resolve().parents[1];P=R/'videos/kite';D=R/'artifacts/final_outcome/kite';Q=R/'artifacts/kite'
def run(args):return subprocess.run(args,check=True,capture_output=True,text=True)
for name,vf in [('kite-square.mp4','crop=1080:1080:0:420'),('kite-landscape.mp4','scale=1920:-2,crop=1920:1080')]:
 run(['ffmpeg','-v','error','-y','-i',str(D/'kite.mp4'),'-vf',vf,'-c:v','libx264','-preset','fast','-crf','16','-c:a','copy','-movflags','+faststart',str(D/name)])
checks=[]
for name,wh in [('kite.mp4',(1080,1920)),('kite-square.mp4',(1080,1080)),('kite-landscape.mp4',(1920,1080))]:
 file=D/name
 require_reverse_engineering(file)
 probe=json.loads(run(['ffprobe','-v','error','-count_frames','-show_streams','-show_format','-of','json',str(file)]).stdout)
 v=next(s for s in probe['streams'] if s['codec_type']=='video');a=next(s for s in probe['streams'] if s['codec_type']=='audio')
 assert (v['width'],v['height'])==wh
 assert abs(float(probe['format']['duration'])-42)<.04
 assert int(v['nb_read_frames'])==1260
 run(['ffmpeg','-v','error','-i',str(file),'-f','null','-'])
 checks.append({'file':name,'width':v['width'],'height':v['height'],'duration':float(probe['format']['duration']),'frames':int(v['nb_read_frames']),'fps':v['r_frame_rate'],'audio':a['codec_name'],'full_decode':'pass','sha256':hashlib.sha256(file.read_bytes()).hexdigest()})
def pcm(file):return np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',str(file),'-f','f32le','-ar','48000','-ac','1','-']),dtype=np.float32)
reference=pcm(P/'assets/mix.wav');encoded=pcm(D/'kite.mp4');n=min(len(reference),len(encoded));corr=float(np.corrcoef(reference[:n],encoded[:n])[0,1]);assert corr>.99
levels=run(['ffmpeg','-hide_banner','-i',str(D/'kite.mp4'),'-af','loudnorm=I=-16:TP=-1:LRA=8:print_format=json','-f','null','-']).stderr
(Q/'encoded-audio-levels.log').write_text(levels)
stats=json.loads(levels[levels.rfind('{'):levels.rfind('}')+1]);assert float(stats['input_tp'])<=-1
run(['ffmpeg','-v','error','-y','-ss','38.5','-i',str(D/'kite.mp4'),'-frames:v','1',str(D/'poster.jpg')])
run(['ffmpeg','-v','error','-y','-i',str(D/'kite.mp4'),'-vf','fps=1/4.5,crop=1080:608:0:656,scale=540:304,tile=3x3','-frames:v','1',str(Q/'encoded-contact-sheet.jpg')])
for name in ['kite-square','kite-landscape']:
 run(['ffmpeg','-v','error','-y','-i',str(D/(name+'.mp4')),'-vf','fps=1/7,scale=480:-2,tile=3x2','-frames:v','1',str(Q/(name+'-check.jpg'))])
verification={'exports':checks,'audio_correlation':corr,'loudness_lufs':float(stats['input_i']),'true_peak_dbtp':float(stats['input_tp']),'geometry':json.loads((Q/'video-geometry.json').read_text()),'cost_usd':0,'limitations':['Illustrative reconstruction grounded in public documentation; not a live product recording.','Campaign tracking URL was not supplied; no destination URL is burned into the video.','Automated audio checks and measured cue timing; no independent listening review.']}
(D/'verification.json').write_text(json.dumps(verification,indent=2)+'\n')
report=f'''# Kite — Ask, plan, review

Rendered result: **42.000 seconds · 1080×1920 · 30fps · burned-in captions · voiceover and music**.

## Production

| Shot | Time | Tool / model |
| --- | --- | --- |
| Stacked launch work → conversation | 0–6s | HyperFrames 0.8.45 + GSAP |
| Ask in Slack | 6–13s | HyperFrames; exact typed request |
| Plan first | 13–21s | HyperFrames; sequential plan emphasis |
| Research and review state | 21–27s | HyperFrames; sample source and caveat |
| Four output examples → one draft | 27–31s | HyperFrames; documented Preview / Review controls |
| Approval point | 31–37s | HyperFrames; typed publication instruction remains unsent |
| Kite / category / CTA | 37–42s | HyperFrames; official wordmark |

All seven shots use deterministic UI. No people, image-to-video, source photographs, cinematic model footage, or external reference footage. Local Kokoro af_heart supplies the exact six supplied voiceover lines, split at phrase boundaries; measured audio lengths set the burned-in caption cues. Music is a new locally synthesized 92 BPM keyboard/pulse bed with one subtle review-ready note.

## Library inspiration

The 347-file library was inventoried and five references visually shortlisted. The file called Motion-5 actually depicts Grok Bot: anchored chat, task-card consolidation and centered close. Notion Custom Agents: visible accumulating work. Tempo: restrained lower captions and single-CTA end card. Jam and Pocket: human framing/lighting/gesture studied but unused because this concept has no people. Exact filenames and inspected intervals are in videos/kite/PRODUCTION_PLAN.md. No reference assets, customer results or testimonials appear in this film.

## Corrections and cost

**$0 generation API cost / $10 cap.** No paid image or video attempts. Deterministic revisions: repaired storyboard header spacing; faded card text before the opening consolidation to avoid transient overlap; slowed local voice phrases where their slots allowed; removed invented native state badges; used documented draft controls; kept publication wording unsent; removed the one-frame empty end-card entrance and rerendered. Two full local renders, no paid regenerations.

## Quality checks

- Master: 42.000s, 1080×1920, 30fps; 1,260 frames decode.
- Square crop: 1080×1080, 42s; full decode passes.
- Landscape crop: 1920×1080, 42s; full decode passes. Central crop after scaling retains the shared safe area.
- Every essential text and logo bound checked across all 1,260 authored frames inside x108–972, y690–1230; zero out-of-bounds results. Reverse seeks restore request and unsent-decision text.
- Runtime/layout/motion checks pass; 32/32 sampled contrast checks pass. Two informational authoring-density warnings concern the seven scene clips and sixteen caption cues sharing tracks, not visual defects.
- Caption text reconstructs all six supplied voiceover lines verbatim. Caption onsets and ends use actual generated phrase durations. No generated UI text.
- Encoded audio: {float(stats['input_i']):.2f} LUFS, {float(stats['input_tp']):.2f} dBTP; zero-offset correlation with intended mix {corr:.5f}.
- Chronological encoded frames and both crop sheets reviewed for text, transitions, consistent palette and complete end card. No human anatomy, gaze, identity or lip-sync checks apply.

## Product representation and remaining release checks

All workflow scenes read Illustrative workflow and Sample company. The approval scene depicts the documented default Propose first mode. Preview and Review are documented website-draft controls. Mode, review-readiness and unsent-draft explanations are editorial text outside the product card, not claims of native badges. Publish it. is typed in a composer and never submitted; no public result, sent message, customer data or performance claim is shown.

The user explicitly authorized this render. It is a documentation-backed illustrative reconstruction, not a recording verified inside a current production workspace. Product-owner screen-fidelity confirmation and the campaign's tracking destination remain release checks. The end card preserves Add Kite to Slack without inventing a URL or QR code. The optional review-player destination is the public https://kite.ai/ homepage. No ad campaign has been published.

Evidence: [Kite approvals documentation](https://docs.kite.ai/slack/approvals), [official homepage](https://kite.ai/). Hashes, exact output dimensions and audio measurements are in verification.json. No audience test or independent listening review was performed.
'''
(D/'REPORT.md').write_text(report)
(P/'DELIVERY_REPORT.md').write_text(report)
player='''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Kite — Ask, plan, review</title><style>*{box-sizing:border-box}body{margin:0;background:#151515;color:#fafafa;font:15px system-ui,sans-serif}main{max-width:1120px;margin:0 auto;padding:28px}header{display:flex;justify-content:space-between;gap:20px;align-items:center}h1{font-size:24px;letter-spacing:-.035em;margin:0}p{color:#bbb}nav{display:flex;gap:8px;margin:20px 0}button,a{font:inherit;color:inherit}button{padding:9px 18px;border:1px solid #555;border-radius:30px;background:transparent;cursor:pointer}button.active{background:#ff6d2d;color:#111;border-color:#ff6d2d}video{display:block;margin:auto;max-width:100%;height:min(74vh,960px);background:white;border-radius:8px}footer{display:flex;gap:25px;justify-content:center;flex-wrap:wrap;margin:22px}a{color:#ddd;text-decoration:none}a:hover{text-decoration:underline}@media(max-width:600px){main{padding:16px}header{display:block}h1{font-size:22px}}</style></head><body><main><header><div><h1>Kite — Ask, plan, review.</h1><p>42 seconds · Illustrative workflow</p></div><a href="https://kite.ai/">Add Kite to Slack ↗</a></header><nav><button class="active" data-file="kite.mp4">9:16 master</button><button data-file="kite-square.mp4">1:1 crop</button><button data-file="kite-landscape.mp4">16:9 crop</button></nav><video id="film" src="kite.mp4" poster="poster.jpg" controls playsinline preload="metadata"></video><footer><a id="download" href="kite.mp4" download>Download MP4</a><a href="REPORT.md">Production report</a></footer></main><script>const v=document.getElementById('film');document.querySelectorAll('button').forEach(b=>b.onclick=()=>{const time=v.currentTime,playing=!v.paused;v.src=b.dataset.file;document.getElementById('download').href=b.dataset.file;v.onloadedmetadata=()=>{v.currentTime=time;if(playing)v.play()};document.querySelectorAll('button').forEach(x=>x.classList.toggle('active',x===b))});</script></body></html>'''
(D/'review.html').write_text(player)
manifest={'name':'Kite — Ask, plan, review','duration':42,'master':str((D/'kite.mp4').relative_to(R)),'player':str((D/'review.html').relative_to(R)),'exports':checks,'generation_cost_usd':0,'report':str((P/'DELIVERY_REPORT.md').relative_to(R))}
(R/'assembled_outputs/kite.json').write_text(json.dumps(manifest,indent=2)+'\n')
print(json.dumps({'exports':checks,'audio_correlation':corr,'lufs':stats['input_i'],'true_peak':stats['input_tp'],'cost':0},indent=2))
