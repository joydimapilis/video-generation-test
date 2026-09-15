"""Verify delivered Crumb MP4s against checked compositions and source audio."""
import hashlib,json,subprocess,wave
from pathlib import Path
import numpy as np
ROOT=Path('artifacts/library-loop-9');OUT=Path('artifacts/final_outcome/crumb')
def probe(path):return json.loads(subprocess.check_output(['ffprobe','-v','error','-show_format','-show_streams','-of','json',str(path)]))
def pcm(path):return np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',str(path),'-vn','-ac','2','-ar','48000','-f','f32le','-']),dtype='<f4').reshape(-1,2)
def rgb(path,t):return np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-ss',str(t),'-i',str(path),'-frames:v','1','-vf','scale=960:540','-pix_fmt','rgb24','-f','rawvideo','-']),dtype=np.uint8).reshape(540,960,3).astype(float)
def digest(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def main():
 result={'films':[],'limitations':['Sampled visual review; no independent listening or audience test.','Automatic transcript is not proof of lip sync or voice identity.'],'generation_budget':json.loads((ROOT/'budget.json').read_text())}
 budget=result['generation_budget'];result['generation_budget']={'estimate_cents':sum(r['estimate_cents'] for r in budget['runs'].values()),'reserved_cents':sum(r['reserved_cents'] for r in budget['runs'].values()),'cap_cents':budget['limit_cents'],'completed':sum(r['status']=='completed' for r in budget['runs'].values()),'pending':sum(r['status'] in ['submitted','running','generated'] for r in budget['runs'].values())}
 assert result['generation_budget']['reserved_cents']<=1000
 for build in json.loads((ROOT/'build.json').read_text()):
  name=build['name'];short=name.removeprefix('crumb-');p=OUT/f'{name}.mp4';project=Path(build['project']);check=json.loads((ROOT/f'check-{short}.json').read_text());assert check['ok']
  meta=probe(p);video=next(s for s in meta['streams'] if s['codec_type']=='video');assert (video['width'],video['height'],video['r_frame_rate'])==(1920,1080,'24/1');duration=float(meta['format']['duration']);assert abs(duration-build['duration'])<.05
  decode=subprocess.run(['ffmpeg','-v','error','-i',str(p),'-f','null','-'],capture_output=True);assert decode.returncode==0 and not decode.stderr
  black=subprocess.run(['ffmpeg','-hide_banner','-i',str(p),'-vf','blackdetect=d=0.08:pix_th=0.08','-an','-f','null','-'],capture_output=True);intervals=[l for l in black.stderr.decode().splitlines() if 'black_start:' in l];assert not intervals
  audio=pcm(p);peak=float(abs(audio).max());assert peak<.9999
  row={'name':name,'path':str(p),'duration':duration,'dimensions':[1920,1080],'fps':24,'sha256':digest(p),'full_decode':True,'black_intervals':intervals,'audio_peak':peak,'composition_check':{'ok':check['ok'],'contrast_passed':check['contrast']['passed'],'contrast_checked':check['contrast']['checked']},'speech':[]}
  sources=json.loads((project/'sources.json').read_text())
  for asset in sources:
   if asset.get('source','').endswith('.mp4'):
    assert asset['source'].startswith('artifacts/library-loop-9/outputs/')
    assert digest(asset['source'])==asset.get('sha256',asset.get('source_sha256'))
  if short!='morning':
   n=round((build['scenes'][0]['duration']-.12)*48000);ref=pcm(project/'assets/voice.wav')[:n];actual=audio[:n];corr=float(np.corrcoef(ref.reshape(-1),actual.reshape(-1))[0,1]);assert corr>.99
   row['speech'].append({'file':'voice.wav','at':0,'correlation_at_zero_offset':corr})
   if short=='baker':
    start=build['scenes'][2]['start'];n=round(2.85*48000);ref=pcm(project/'assets/return.wav')[:n];actual=audio[round(start*48000):round(start*48000)+n];corr=float(np.corrcoef(ref.reshape(-1),actual.reshape(-1))[0,1]);assert corr>.99
    row['speech'].append({'file':'return.wav','at':start,'correlation_at_zero_offset':corr})
   a=rgb(p,.5)[62:430,55:905];b=rgb(p,2)[62:430,55:905];row['human_frame_change_mae']=float(abs(a-b).mean());assert row['human_frame_change_mae']>1
  else:
   a=rgb(p,4.5-1/24)[62:,325:];b=rgb(p,4.5)[62:,325:];row['actual_product_joint_mae_255']=float(abs(a-b).mean());assert row['actual_product_joint_mae_255']<7
  sheet=OUT/f'{name}-frames.jpg';subprocess.run(['ffmpeg','-v','error','-y','-i',str(p),'-vf',f'fps=8/{duration},scale=480:270,tile=4x2','-frames:v','1',str(sheet)],check=True)
  poster=OUT/f'{name}-poster.jpg';subprocess.run(['ffmpeg','-v','error','-y','-ss','0.25','-i',str(p),'-frames:v','1',str(poster)],check=True)
  row['contact_sheet']=str(sheet);result['films'].append(row);print(name,duration,'decode OK, audio OK, source lineage OK')
 (ROOT/'delivery-verification.json').write_text(json.dumps(result,indent=2)+'\n')
 (OUT/'verification.json').write_text(json.dumps(result,indent=2)+'\n')
 names={'crumb-customer':('Breakfast, already sorted.','Customer UGC + a clear preorder walkthrough.'),'crumb-baker':('A list before the oven.','Baker interview + a preparation list + a newly generated return shot.'),'crumb-morning':('Save the good part.','Fresh pastry photography + a matched continuation + a reservation demo.')}
 cards=''
 for r in result['films']:
  n=r['name'];title,desc=names[n];cards+=f'<article><h2>{title}</h2><p>{desc} {r["duration"]:.2f}s.</p><video controls preload="metadata" poster="{n}-poster.jpg" src="{n}.mp4"></video><p><a href="{n}.mp4" download>Download MP4</a></p></article>'
 (OUT/'review.html').write_text('<!DOCTYPE html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Crumb / Three new sample films</title><style>body{background:#f5ebdd;color:#30221d;font:18px system-ui;margin:40px auto;max-width:1100px;padding:0 25px}h1,h2{font-family:Georgia,serif}h1{font-size:48px}h2{font-size:32px}article{padding:25px 0;border-top:1px solid #943d2b;margin:35px 0}video{width:100%;background:#30221d}a{color:#943d2b}p{line-height:1.5}</style><h1>crumb. / three new films</h1><p>A fictional bakery preorder service. New concepts, scripts, footage and edits, inspired by patterns in your reference library.</p>'+cards+'<p>1920 × 1080 · 24fps · $5.10 estimated generation cost across all 12 tests; $5.92 reserved under one $10 cap.</p><p><a href="../../../docs/CRUMB_SCORECARD.md">Model scorecard</a> · <a href="../../../docs/CRUMB_RESEARCH.md">Research and learnings</a></p></html>')
if __name__=='__main__':main()
