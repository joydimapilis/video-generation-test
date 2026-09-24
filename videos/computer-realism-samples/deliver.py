"""Verify final encodes, copy reviewed source stills and write local comparison player."""
from pathlib import Path
import subprocess,json,hashlib,shutil,re
p=Path(__file__).resolve().parent;root=p.parents[1]
out=root/'artifacts/final_outcome/computer-realism-samples';out.mkdir(parents=True,exist_ok=True)
sel=json.loads((p/'selection.json').read_text());report={'samples':[],'method':'Full decode, metadata, source hashes, sampled encoded frames; subjective motion review recorded separately.'}
for row in sel['samples']:
 name=row['name'];video=out/(name+'.mp4');assert video.is_file()
 probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-count_frames','-show_streams','-show_format','-of','json',str(video)]))
 v=next(s for s in probe['streams'] if s['codec_type']=='video');duration=float(probe['format']['duration'])
 assert abs(duration-row['duration'])<.06,(name,duration)
 assert int(v['nb_read_frames'])==round(row['duration']*24)
 assert not any(s['codec_type']=='audio' for s in probe['streams'])
 subprocess.run(['ffmpeg','-v','error','-i',str(video),'-f','null','-'],check=True)
 target=out/(name+'-source.png');shutil.copy2(root/row['source_image'],target)
 full_take=out/(name+'-full-take.mp4');shutil.copy2(root/row['source'],full_take)
 sheet=out/(name+'-review.jpg')
 subprocess.run(['ffmpeg','-v','error','-y','-i',str(video),'-vf',f'fps=8/{duration},scale=480:270,tile=4x2','-frames:v','1',str(sheet)],check=True)
 comparison=subprocess.run(['ffmpeg','-v','info','-i',str(root/row['source']),'-i',str(video),'-filter_complex',f'[0:v]trim=start={row.get("source_start",0)}:duration={row["duration"]},setpts=PTS-STARTPTS[ref];[ref][1:v]ssim','-an','-f','null','-'],capture_output=True,text=True,check=True)
 match=re.findall(r'All:([0-9.]+)',comparison.stderr);ssim=float(match[-1]);assert ssim>.98,(name,ssim)
 report['samples'].append({'source_to_final_ssim':ssim,'name':name,'file':str(video.relative_to(root)),'source_image':str(target.relative_to(root)),'duration':duration,'width':v['width'],'height':v['height'],'fps':v['r_frame_rate'],'decoded_frames':int(v['nb_read_frames']),'full_decode_ok':True,'audio':'intentionally silent','sha256':hashlib.sha256(video.read_bytes()).hexdigest(),'source_sha256':row['source_sha256'],'source_image_sha256':hashlib.sha256(target.read_bytes()).hexdigest(),'source_range':[row.get('source_start',0),row.get('source_start',0)+row['duration']],'playback_rate':1})
 report['samples'][-1].update({'full_generated_take':str(full_take.relative_to(root)), 'selection_decision':row['decision'], 'review_limit':row.get('review_limit','Provisional naturalness judgment; minor regular finger cadence and softened facial detail remain.')})
ledger=json.loads((root/'artifacts/library-loop-computer-realism/budget.json').read_text())
report['cost']={'estimate_usd':sum(v['estimate_cents'] for v in ledger['runs'].values())/100,'reserved_usd':sum(v['reserved_cents'] for v in ledger['runs'].values())/100,'cap_usd':10,'confirmed_charge_usd':None,'invoice_limitation':'Fal usage endpoint returns 403 for this key; no verified invoice. All source-image and rejected video attempts included.'}
report['limitations']=['Behavioral reference cues translated into prompts; real movement videos were not model inputs.','No matched no-reference control; causal improvement untested.','Independent source-image identities; no cross-shot identity test.','Second and third samples retain only 0–1.25s and 0–1.5s respectively; later curled-hand poses were rejected. Untrimmed takes are included for diagnosis.','Exact UI, speech/lip sync and external mouse use not tested.']
(root/'assembled_outputs/computer-realism-samples.json').write_text(json.dumps(report,indent=2)+'\n')
(root/'review_notes/computer-realism-final-verification.json').write_text(json.dumps(report,indent=2)+'\n')
cards='\n'.join(f'<article><h2>{r["name"]} · {r["duration"]:g}s</h2><video controls preload="metadata" muted playsinline src="{r["name"]}.mp4" poster="{r["name"]}-source.png"></video><p><a href="{r["name"]}.mp4">Selected MP4</a> · <a href="{r["name"]}-source.png">Source image</a> · <a href="{r["name"]}-full-take.mp4">Full 4s generated take</a></p><p>{r.get("review_limit", "Provisional selection: minor regular finger cadence and softened facial detail remain.")}</p></article>' for r in sel['samples'])
html='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Computer realism samples</title><style>body{margin:32px auto;padding:0 24px;max-width:1500px;background:#f4f1eb;color:#242725;font:16px system-ui;line-height:1.5}h1{font-size:32px}h2{font-size:18px}main{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:20px}video{width:100%;background:#242725}button,select{padding:10px 14px;margin:0 8px 16px 0;font:inherit}a{color:#27584e}@media(max-width:900px){main{grid-template-columns:1fr}}</style><h1>Computer realism · three studies</h1><p>Silent · native playback speed · duration shown per sample. Separate source stills and reviewed image-to-video takes.</p><button id="play">Play all from start</button><button id="pause">Pause all</button><label>Review speed <select id="speed"><option value="1">1× normal</option><option value="0.5">0.5× inspection</option></select></label><main>'''+cards+'''</main><p>Movement references informed the prompts; they were not supplied directly to the model. No matched no-reference controls: these samples cannot establish a causal improvement. Exact screen text is not a tested dimension.</p><script>const vs=[...document.querySelectorAll('video')];document.querySelector('#play').onclick=()=>{vs.forEach(v=>{v.currentTime=0;v.playbackRate=+document.querySelector('#speed').value;v.play().catch(console.error)})};document.querySelector('#pause').onclick=()=>vs.forEach(v=>v.pause());document.querySelector('#speed').onchange=e=>vs.forEach(v=>v.playbackRate=+e.target.value);</script></html>'''
(out/'review.html').write_text(html)
print(json.dumps(report,indent=2))
