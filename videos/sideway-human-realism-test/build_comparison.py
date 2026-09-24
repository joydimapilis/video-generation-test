"""Build the local diagnostic comparison without editing the original film."""
from pathlib import Path
import json,shutil,subprocess,html
ROOT=Path(__file__).resolve().parents[2]
P=ROOT/'videos/sideway-human-realism-test/comparison';A=P/'assets';C=P/'compositions'
A.mkdir(exist_ok=True);C.mkdir(exist_ok=True)
for role in ['phone','arrival','story']:
 shutil.copy2(ROOT/f'artifacts/library-loop-14/outputs/sideway_{role}_v2.mp4',A/f'{role}-original.mp4')
for role in ['phone','arrival']:
 shutil.copy2(ROOT/f'artifacts/library-loop-14/outputs/sideway_{role}_sample02_wan_v3.mp4',A/f'{role}-candidate.mp4')
reading=ROOT/'artifacts/library-loop-14/outputs/sideway_reading_sample02_wan_v4.mp4'
if reading.exists():shutil.copy2(reading,A/'reading-candidate.mp4')
for name,src,duration in [('phone','233390_medium',4),('cafe','216598_medium',5),('story','297986_medium',3),('hands','736-138808023_medium',4)]:
 dest=A/f'{name}-reference.mp4'
 if not dest.exists():subprocess.run(['ffmpeg','-v','error','-y','-i',str(ROOT/f'references/sample02/{src}.mp4'),'-t',str(duration),'-vf','scale=1280:1280:force_original_aspect_ratio=decrease','-an','-c:v','libx264','-crf','18','-preset','fast',str(dest)],check=True)
shutil.copy2(ROOT/'videos/sideway/assets/gsap.min.js',A/'gsap.min.js')
shutil.copy2(ROOT/'videos/kite-tomorrow-contact-test/assets/Onest.woff2',A/'Onest.woff2')
(P/'design.md').write_text('''# Sideway realism comparison\nConcept: inspect original and candidate performances at equal scale, with the observed motion reference beside them.\nWarm charcoal #20231f, cream #f3f1e6, yellow #f0d970. Onest for all diagnostic labels: one neutral voice, no ornamental typography. Full images remain uncropped and ungraded. Equal original/candidate portrait panels are the focal pair; reference and concise observations occupy the right column. No decorative movement. Hard cuts separate studies; a thin linear progress marker supports review seeking. No music or speech in this silent movement comparison. Original spoken take remains available separately.\n''')
scenes=[
 dict(id='phone-open',start=0,duration=3,title='01  Phone opening',original='phone-original.mp4',candidate='phone-candidate.mp4',reference='phone-reference.mp4',orig_start=0,orig_rate=1,cand_start=0,cand_rate=1,detail='Original window 0–3s · both at native speed',ref_label='sample02 / 233390 · 0–3s',verdict='Trial 1 · rejected',notes=['Screen attention and small hand motion.','Candidate adds unwanted mouth movement.','The full take also develops a look away.'],candidate_label='Candidate · 720p'),
 dict(id='phone-return',start=3,duration=4,title='02  Phone reading return',original='phone-original.mp4',candidate='reading-candidate.mp4',reference='phone-reference.mp4',orig_start=1,orig_rate=.5,cand_start=0,cand_rate=1,detail='Original window 6–10s · original 0.5× / candidate 1×',ref_label='sample02 / 233390 · 0–4s',verdict='Trial 2 · not selected',notes=['Hands steadier; mouth movement persists.','480p study; reduced facial detail.','Source pose and playback timing also differ.'],candidate_label='Candidate · 480p'),
 dict(id='cafe',start=7,duration=5,title='03  Café pause',original='arrival-original.mp4',candidate='arrival-candidate.mp4',reference='cafe-reference.mp4',orig_start=0,orig_rate=1,cand_start=0,cand_rate=1,detail='Original window 26–32s · first 5s compared at native speed',ref_label='sample02 / 216598 · 0–5s',verdict='Trial 1 · partial improvement',notes=['Free hand lowers onto the trousers.','Cup and holding hand stay connected.','Low eyelids and posed expression remain.'],candidate_label='Candidate · 720p')]
basecss='''@font-face{font-family:Onest;src:url("assets/Onest.woff2")}*{box-sizing:border-box}html,body{margin:0;width:100%;height:100%;overflow:hidden}body{background:#20231f;color:#f3f1e6;font-family:Onest,sans-serif}#root{position:relative;width:100%;height:100%;overflow:hidden}.clip{position:absolute}.panel{position:absolute;top:155px;width:468px;height:832px;object-fit:contain;background:#151713}.old{left:40px}.new{left:532px}.reference{position:absolute;left:1056px;top:155px;width:824px;height:510px;object-fit:contain;background:#151713}.headline{position:absolute;left:40px;top:30px;margin:0;font-size:43px;font-weight:700;line-height:1.2}.chapter{position:absolute;right:40px;top:38px;font-size:29px;color:#f0d970}.label{position:absolute;top:110px;font-size:27px;margin:0;font-weight:600}.reference-label{left:1056px}.note-box{position:absolute;left:1056px;top:697px;width:820px}.verdict{color:#f0d970;font-size:31px;margin:0 0 23px}.note{font-size:28px;line-height:1.45;margin:0 0 12px}.disclosure{position:absolute;left:1056px;top:925px;width:820px;font-size:23px;line-height:1.4;color:#e0ddcc}.footer{position:absolute;left:40px;top:1010px;font-size:24px}.progress{position:absolute;left:40px;top:1054px;width:1840px;height:4px;background:#f0d970;transform-origin:left center}'''
for s in scenes:
 sid=s['id'];D=s['duration']
 markup=f'''<!doctype html><html><body><template><style>#{sid}-root{{position:absolute;inset:0;width:100%;height:100%;background:#20231f}}</style>
 <div id="{sid}-root" data-composition-id="{sid}" data-width="1920" data-height="1080" data-duration="{D}">
 <h1 class="headline">Sideway / human realism test</h1><div class="chapter">{s['title']}</div>
 <p class="label old">Original · latest delivered take</p><p class="label new">{s['candidate_label']}</p><p class="label reference-label">{s['ref_label']}</p>
 <video id="{sid}-original" class="clip panel old" src="assets/{s['original']}" data-start="0" data-duration="{D}" data-media-start="{s['orig_start']}" data-playback-rate="{s['orig_rate']}" data-track-index="1" muted playsinline></video>
 <video id="{sid}-candidate" class="clip panel new" src="assets/{s['candidate']}" data-start="0" data-duration="{D}" data-media-start="{s['cand_start']}" data-playback-rate="{s['cand_rate']}" data-track-index="2" muted playsinline></video>
 <video id="{sid}-reference" class="clip reference" src="assets/{s['reference']}" data-start="0" data-duration="{D}" data-track-index="3" muted playsinline></video>
 <div class="note-box"><p class="verdict">{s['verdict']}</p>{''.join('<p class="note">'+html.escape(n)+'</p>' for n in s['notes'])}</div>
 <div class="disclosure">Reference observations informed the prompt.<br>Different model; no direct motion-video conditioning.</div>
 <div class="footer">{s['detail']}</div><div id="{sid}-progress" class="progress"></div>
 </div><script>window.__timelines["{sid}"]=gsap.timeline({{paused:true}}).fromTo("#{sid}-progress",{{scaleX:0}},{{scaleX:1,duration:{D},ease:"none"}},0);</script></template></body></html>'''
 # Avoid line-break markup per composition contract; separate paragraphs already styled.
 markup=markup.replace('Reference observations informed the prompt.<br>Different model; no direct motion-video conditioning.','Reference observations informed the prompt. Different model; no direct motion-video conditioning.')
 (C/f'{sid}.html').write_text(markup)
mounts=''.join(f'<div id="{s["id"]}" class="clip" data-composition-id="{s["id"]}" data-composition-src="compositions/{s["id"]}.html" data-start="{s["start"]}" data-duration="{s["duration"]}" data-track-index="0" data-width="1920" data-height="1080" style="inset:0"></div>' for s in scenes)
(P/'index.html').write_text(f'<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Sideway human realism comparison</title><script src="assets/gsap.min.js"></script><style>{basecss}</style></head><body><div id="root" data-composition-id="comparison" data-width="1920" data-height="1080" data-duration="12">{mounts}</div><script>window.__timelines["comparison"]=gsap.timeline({{paused:true}});</script></body></html>')
(P/'selection.json').write_text(json.dumps(scenes,indent=2)+'\n')
(P/'BRIEF.md').write_text('---\nworkflow: general-video\nflow: automation\nstoryboard: no\n---\nDiagnostic comparison only. Rendering authorized by user request. See ../BRIEF.md for preserved scope, cumulative budget, source review and limitations.\n')
(P/'STORYBOARD.md').write_text('\n'.join(f'## Frame {i+1}\nstatus: implemented\nsrc: compositions/{s["id"]}.html\nDuration: {s["duration"]} seconds.\n{ s["title"] }: fixed comparison panels, native media playback, hard cut, linear progress marker (GSAP adapter).\n' for i,s in enumerate(scenes)))
print('Built 12-second comparison:',P)
