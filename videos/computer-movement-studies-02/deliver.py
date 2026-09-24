"""Verify final native-speed exports and create a local comparison page."""
from pathlib import Path
import json,subprocess,hashlib,shutil,re,html
from fractions import Fraction
p=Path(__file__).resolve().parent;root=p.parents[1]
out=root/'artifacts/final_outcome/computer-movement-studies-02';out.mkdir(parents=True,exist_ok=True)
selection=json.loads((p/'selection.json').read_text());assert len(selection['samples'])==3 and not selection.get('pending');report={'samples':[],'editable_project':str(p.relative_to(root))}
for row in selection['samples']:
 name=row['name'];video=out/(name+'.mp4')
 probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-count_frames','-show_streams','-show_format','-of','json',str(video)]))
 v=next(s for s in probe['streams'] if s['codec_type']=='video');duration=float(probe['format']['duration'])
 assert abs(duration-row['duration'])<.06,(name,duration)
 assert int(v['nb_read_frames'])==round(row['duration']*24)
 assert Fraction(v['avg_frame_rate'])==24
 assert (v['width'],v['height'])==(1920,1080)
 assert not any(s['codec_type']=='audio' for s in probe['streams'])
 subprocess.run(['ffmpeg','-v','error','-i',str(video),'-f','null','-'],check=True)
 still=out/(name+'-source.png');shutil.copy2(root/row['source_image'],still)
 raw=out/(name+'-generated.mp4');shutil.copy2(root/row['source'],raw)
 subprocess.run(['ffmpeg','-v','error','-y','-i',str(video),'-vf',f'fps=12/{duration},scale=480:270,tile=4x3','-frames:v','1',str(out/(name+'-review.jpg'))],check=True)
 subprocess.run(['ffmpeg','-v','error','-y','-sseof','-0.042','-i',str(video),'-frames:v','1',str(out/(name+'-last.jpg'))],check=True)
 comparison=subprocess.run(['ffmpeg','-v','info','-i',str(root/row['source']),'-i',str(video),'-filter_complex',f'[0:v]trim=start={row.get("source_start",0)}:duration={row["duration"]},setpts=PTS-STARTPTS[ref];[ref][1:v]ssim','-an','-f','null','-'],capture_output=True,text=True,check=True)
 ssim=float(re.findall(r'All:([0-9.]+)',comparison.stderr)[-1]);assert ssim>.98,(name,ssim)
 report['samples'].append({**row,'file':str(video.relative_to(root)),'source_image_delivery':str(still.relative_to(root)),'unmodified_generated_take':str(raw.relative_to(root)),'decoded_frames':int(v['nb_read_frames']),'full_decode_ok':True,'source_to_final_ssim':ssim,'sha256':hashlib.sha256(video.read_bytes()).hexdigest(),'source_image_sha256':hashlib.sha256(still.read_bytes()).hexdigest(),'audio':'intentionally silent','playback_rate':1})
ledger=json.loads((root/'artifacts/library-loop-computer-movement-studies-02/budget.json').read_text())
report['cost']={'estimated_usd':sum(r['estimate_cents'] for r in ledger['runs'].values())/100,'reserved_usd':sum(r['reserved_cents'] for r in ledger['runs'].values())/100,'shared_cap_usd':ledger['limit_cents']/100,'confirmed_spend_usd':None,'note':'Estimated from current endpoint quotes/settings; 15 percent reservation buffer, rounded per call. All attempts included; invoice not verified.'}
report['reference_use']={'source':'references/human-realism','behavioral_observations':'videos/computer-movement-studies-02/reference-observations.json','real_videos_or_frames_sent_to_provider':False,'real_video_content_in_final':False,'matched_no_reference_controls':False,'causal_improvement':None}
report['verification_method']='Full decode, frame count/duration/fps, source hash and SSIM, encoded chronological overview/last-frame review; subjective motion review separately. Technical checks do not establish human realism.'
for f in [root/'assembled_outputs/computer-movement-studies-02.json',root/'review_notes/computer-movement-studies-02-final-verification.json']:f.write_text(json.dumps(report,indent=2)+'\n')
cards=[]
for row in selection['samples']:
 n=row['name'];cards.append(f'<article><h2>{html.escape(row["title"])} · {row["duration"]:g}s</h2><video controls muted playsinline preload="metadata" src="{n}.mp4" poster="{n}-source.png"></video><p><a href="{n}.mp4">Final MP4</a> · <a href="{n}-source.png">New source image</a> · <a href="{n}-generated.mp4">Unmodified generated take</a></p><p>{html.escape(row["review_note"])}</p></article>')
page='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>New computer movement studies</title><style>body{max-width:1540px;margin:36px auto;padding:0 24px;background:#f4f2ed;color:#242826;font:16px system-ui;line-height:1.55}h1{font-size:32px}h2{font-size:19px}main{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:24px}video{width:100%;background:#16191a}button,select{font:inherit;padding:8px 12px;margin:0 8px 18px 0}a{color:#285d52}@media(max-width:900px){main{grid-template-columns:1fr}}</style><h1>New computer movement studies</h1><p>Three newly generated people and scenes. Real movement clips informed written motion directions only; no reference footage or extracted reference frames were used in generation or delivery.</p><p>Silent · 1080p · 24fps · native speed. Use full screen to inspect hands and eyes.</p><button id="play">Play all from start</button><button id="pause">Pause all</button><label>Review speed <select id="speed"><option value="1">1× normal</option><option value=".5">0.5× inspection</option></select></label><main>'''+''.join(cards)+'''</main><p>These are qualitative tests without matched no-reference controls. They cannot isolate a causal benefit from movement-reference observations. External mouse grip is an application hypothesis; the supplied clips mainly show keyboard/trackpad and screen-attention behavior.</p><script>const vs=[...document.querySelectorAll('video')];document.querySelector('#play').onclick=()=>vs.forEach(v=>{v.currentTime=0;v.playbackRate=+document.querySelector('#speed').value;v.play().catch(console.error)});document.querySelector('#pause').onclick=()=>vs.forEach(v=>v.pause());document.querySelector('#speed').onchange=e=>vs.forEach(v=>v.playbackRate=+e.target.value);</script></html>'''
(out/'review.html').write_text(page)
for rel in re.findall(r'(?:src|href|poster)="([^"]+)"',page):assert (out/rel).is_file(),rel
print(json.dumps(report,indent=2))
