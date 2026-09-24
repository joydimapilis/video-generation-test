"""Verify encoded selections, retain source/input provenance and build comparison."""
from pathlib import Path
from fractions import Fraction
import hashlib,html,json,re,shutil,subprocess
p=Path(__file__).resolve().parent;root=p.parents[1];out=root/'artifacts/final_outcome/computer-movement-long';out.mkdir(parents=True,exist_ok=True)
sel=json.loads((p/'selection.json').read_text());assert len(sel['samples'])==3 and sel['reviewed']
report={'project':str(p.relative_to(root)),'samples':[],'costs':[],'reference_media_used_as_model_inputs':False,'reference_guidance':'written observations only','matched_controls':False}
cards=[]
for s in sel['samples']:
 n=s['name'];num=n[:2];f=out/(n+'.mp4');src=root/s['source']
 probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-count_frames','-show_format','-show_streams','-of','json',str(f)]));v=next(x for x in probe['streams'] if x['codec_type']=='video');fps=Fraction(s['fps'])
 assert Fraction(v['avg_frame_rate'])==fps
 assert abs(float(probe['format']['duration'])-s['duration'])<=1/float(fps)+.001
 assert int(v['nb_read_frames'])==round(s['duration']*float(fps))
 assert not any(x['codec_type']=='audio' for x in probe['streams'])
 subprocess.run(['ffmpeg','-v','error','-i',str(f),'-f','null','-'],check=True)
 for srcpath,dst in [(root/s['source_image'],out/(n+'-source.png')),(src,out/(n+'-generated.mp4'))]:shutil.copy2(srcpath,dst)
 subprocess.run(['ffmpeg','-v','error','-y','-i',str(f),'-vf',f'fps=16/{s["duration"]},scale=480:270,tile=4x4','-frames:v','1',str(out/(n+'-review.jpg'))],check=True)
 subprocess.run(['ffmpeg','-v','error','-y','-sseof',str(-1/float(fps)-.002),'-i',str(f),'-frames:v','1',str(out/(n+'-last.jpg'))],check=True)
 comp=subprocess.run(['ffmpeg','-v','info','-i',str(src),'-i',str(f),'-filter_complex',f'[0:v]trim=start={s.get("source_start",0)}:duration={s["duration"]},setpts=PTS-STARTPTS[ref];[ref][1:v]ssim','-an','-f','null','-'],check=True,capture_output=True,text=True)
 similarity=float(re.findall(r'All:([0-9.]+)',comp.stderr)[-1]);assert similarity>.98,(n,similarity)
 report['samples'].append({**s,'file':str(f.relative_to(root)),'decoded_frames':int(v['nb_read_frames']),'source_to_final_ssim':similarity,'full_decode_ok':True,'sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'audio':'silent','playback_speed':1})
 ledger=json.loads((root/f'artifacts/library-loop-computer-long-{num}/budget.json').read_text());hist=json.loads((p/'budget-continuity.json').read_text());prior=next(x for x in hist['videos'] if x['video']==num)
 est=sum(x['estimate_cents'] for x in ledger['runs'].values());res=sum(x['reserved_cents'] for x in ledger['runs'].values());assert res<=1000
 report['costs'].append({'sample':num,'cumulative_estimated_usd':est/100,'cumulative_reserved_usd':res/100,'incremental_estimated_usd':(est-prior['prior_estimated_cents'])/100,'incremental_reserved_usd':(res-prior['prior_reserved_cents'])/100,'per_video_cap_usd':10,'confirmed_spend_usd':None})
 cards.append(f'<article><h2>{html.escape(s["title"])}</h2><p>{s["duration"]:g}s · {float(fps):g}fps</p><video controls muted playsinline preload="metadata" src="{n}.mp4" poster="{n}-source.png"></video><p><a href="{n}.mp4">Final MP4</a> · <a href="{n}-source.png">Source image</a> · <a href="{n}-generated.mp4">Original generated take</a></p><p>{html.escape(s["review_note"])}</p></article>')
report['cost_note']='All corresponding historical attempts remain included, including rejected/uncertain calls. Mirrored prior batch records counted once per video. Reservations include 15% buffer rounded per call. Invoice not verified.'
for path in [root/'assembled_outputs/computer-movement-long.json',root/'review_notes/computer-movement-long-final-verification.json']:path.write_text(json.dumps(report,indent=2)+'\n')
page='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Longer computer interaction studies</title><style>body{max-width:1540px;margin:36px auto;padding:0 24px;background:#f4f2ed;color:#242826;font:16px system-ui;line-height:1.55}h1{font-size:32px}h2{font-size:19px}main{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:24px}video{width:100%;background:#16191a}button,select{font:inherit;padding:8px 12px;margin:0 8px 18px 0}a{color:#285d52}@media(max-width:900px){main{grid-template-columns:1fr}}</style><h1>Longer computer interaction studies</h1><p>Existing generated source images animated into varied work sequences. Real movement clips informed written directions only; no real clip, extracted real frame, pose map or motion-control input was sent to generation.</p><p>Silent · native speed · separate files. Full-screen and half-speed controls help inspect hands and gaze.</p><button id="play">Play all from start</button><button id="pause">Pause all</button><label>Review speed <select id="speed"><option value="1">1× normal</option><option value=".5">0.5× inspection</option></select></label><main>'''+''.join(cards)+'''</main><p>Qualitative tests without matched controls; do not infer a causal benefit from reference observation. Requested beat timings and actual achieved actions are distinguished in the production review.</p><script>const vs=[...document.querySelectorAll('video')];document.querySelector('#play').onclick=()=>vs.forEach(v=>{v.currentTime=0;v.playbackRate=+document.querySelector('#speed').value;v.play().catch(console.error)});document.querySelector('#pause').onclick=()=>vs.forEach(v=>v.pause());document.querySelector('#speed').onchange=e=>vs.forEach(v=>v.playbackRate=+e.target.value);</script></html>'''
(out/'review.html').write_text(page)
for rel in re.findall(r'(?:src|href|poster)="([^"]+)"',page):assert (out/rel).is_file(),rel
print(json.dumps({'samples':[(s['name'],s['duration'],s['source_to_final_ssim']) for s in report['samples']],'costs':report['costs']},indent=2))
