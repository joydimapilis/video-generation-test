"""Check final Sideway encode, native audio alignment and image-first provenance."""
from amarillo.delivery import require_reverse_engineering

import hashlib,json,subprocess
from pathlib import Path
import numpy as np
P=Path('videos/sideway');R=Path('artifacts/library-loop-14');O=Path('artifacts/final_outcome/sideway');V=O/'sideway-cafe-revised.mp4';SR=48000

def run(*args):return subprocess.check_output(args)
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def pcm(p):return np.frombuffer(run('ffmpeg','-v','error','-i',str(p),'-vn','-ac','2','-ar',str(SR),'-f','f32le','-'),dtype='<f4').reshape(-1,2)
def frame(p,t,filters='',w=540,h=960):
 f=(filters+',' if filters else '')+f'scale={w}:{h}'
 return np.frombuffer(run('ffmpeg','-v','error','-ss',str(t),'-i',str(p),'-frames:v','1','-vf',f,'-pix_fmt','rgb24','-f','rawvideo','-'),dtype=np.uint8).reshape(h,w,3).astype(float)
def main():
 require_reverse_engineering(V)
 s=(R/'check-final.json').read_text();check=json.loads(s[s.index('{'):]);assert check['ok'];assert all(check[k]['errorCount']==0 for k in ['lint','runtime','layout','motion','contrast'])
 meta=json.loads(run('ffprobe','-v','error','-show_streams','-show_format','-of','json',str(V)));v=next(x for x in meta['streams'] if x['codec_type']=='video');assert(v['width'],v['height'],v['r_frame_rate'],int(v['nb_frames']))==(1080,1920,'24/1',864);assert abs(float(meta['format']['duration'])-36)<.05
 decode=subprocess.run(['ffmpeg','-v','error','-i',str(V),'-f','null','-'],capture_output=True);assert decode.returncode==0 and not decode.stderr
 black=subprocess.run(['ffmpeg','-hide_banner','-i',str(V),'-vf','blackdetect=d=0.04:pix_th=0.08','-an','-f','null','-'],capture_output=True);intervals=[x for x in black.stderr.decode().splitlines() if 'black_start:' in x];assert not intervals
 actual=pcm(V);expected=pcm(P/'assets/speech.wav')+pcm(P/'assets/score.wav');n=min(len(actual),len(expected));corr=float(np.corrcoef(actual[:n].ravel(),expected[:n].ravel())[0,1]);peak=float(abs(actual).max());assert corr>.99 and peak<.9999,(corr,peak)
 plan=json.loads((P/'audio-plan.json').read_text());native=pcm(plan['native_source']);speech=pcm(P/'assets/speech.wav');voice=[]
 for cut in plan['cuts']:
  a=round((cut['source_start']+.05)*SR);b=round((cut['source_end']-.05)*SR);start=round((cut['timeline_start']+.05)*SR);source=native[a:b]*plan['gain'];derived=speech[start:start+len(source)];c=float(np.corrcoef(source.ravel(),derived.ravel())[0,1]);assert c>.999;voice.append({'timeline_start':cut['timeline_start'],'source_start':cut['source_start'],'zero_offset_correlation':c})
 joins=[]
 for t in [10,26]:
  err=float(abs(frame(V,t-1/24)-frame(V,t)).mean());assert err<2,(t,err);joins.append({'time':t,'mae_255':err})
 hold=float(abs(frame(V,34.4)-frame(V,35.95)).mean());assert hold<1
 preservation=json.loads((R/'cafe-preservation.json').read_text())
 for path,digest in preservation['unchanged'].items():assert sha(path)==digest,path
 previous_audio=pcm(O/'sideway-revised.mp4');n=min(len(actual),len(previous_audio));unchanged_audio=float(np.corrcoef(actual[:n].ravel(),previous_audio[:n].ravel())[0,1]);assert unchanged_audio>.99999
 sources=json.loads((P/'sources.json').read_text());ledger=json.loads((R/'budget.json').read_text());photo=[]
 for row in sources:
  review=json.loads(Path(row['review']).read_text());assert review['approved'];assert row['image_first'];assert sha(row['source'])==row['source_sha256'];assert sha(row['derived'])==row['derived_sha256'];assert sha(P/row['reference'])==row['reference_sha256']==review['source_sha256'];assert 'image-to-video' in ledger['runs'][row['run_id']]['payload']['endpoint']
  samples={'phone':[(.5,.5),(1.5,1.5),(2.5,2.5),(6.5,1.25),(7.5,1.75),(8,2)],'story':[(4,1),(5.7,2.7)],'arrival':[(27.1,1.1),(28,2),(29.5,3.5),(31,5)]}[row['role']]
  for t,st in samples:
   # Exclude editorial copy while comparing face, hands and physical phone/cup.
   f='scale=1080:1920,crop=1080:850:0:450';a=frame(V,t,f,w=540,h=425);b=frame(row['source'],st,f,w=540,h=425);err=float(abs(a-b).mean());assert err<10,(row['role'],t,err);photo.append({'role':row['role'],'timeline_time':t,'source_time':st,'mae_255':err})
 estimated=sum(r['estimate_cents'] for r in ledger['runs'].values());reserved=sum(r['reserved_cents'] for r in ledger['runs'].values());image_allowance=sum(r['estimate_cents'] for r in ledger['runs'].values() if not r['payload'].get('endpoint'));assert reserved<=ledger['limit_cents']==1200;assert ledger['cap_changes'][-1]['to_cents']==1200;assert ledger['cap_changes'][-1]['authorization'];assert all(r['status']=='completed' for r in ledger['runs'].values())
 geom=json.loads((R/'geometry.json').read_text());assert all(x['inside'] for x in geom['clicks']);assert geom['walking_minutes']+geom['linger_minutes']==60
 result={'path':str(V),'sha256':sha(V),'bytes':V.stat().st_size,'duration_seconds':36,'dimensions':[1080,1920],'fps':24,'frames':864,'full_decode':True,'black_intervals':intervals,'audio_peak':peak,'audio_correlation_with_previous_delivery':unchanged_audio,'unchanged_assets_verified':list(preservation['unchanged']),'audio_mix_correlation':corr,'audio_mix_reference':'Unprocessed speech plus authored score; output includes native dynamic carve at strength0.25','native_voice_alignment':voice,'seams':joins,'source_comparisons':photo,'final_hold_mae_255':hold,'image_first':True,'human_reference_reviews':[x['review'] for x in sources],'on_camera_speaking_seconds':3,'revision':'Café source and I2V regenerated for aligned forward-facing posture and relaxed coffee gaze; previous phone and dialogue revisions retained','checks':{k:{'errors':check[k]['errorCount'],'warnings':check[k]['warningCount']} for k in ['lint','runtime','layout','motion','contrast']},'contrast':{'passed':check['contrast']['passed'],'checked':check['contrast']['checked']},'budget':{'estimated_cents_including_image_allowance':estimated,'reserved_cents':reserved,'cap_cents':ledger['limit_cents'],'image_allowance_cents':image_allowance,'fal_estimated_cents':estimated-image_allowance},'limitations':['Fictional app and illustrative route, no live routing backend.','Sampled subjective visual review; ASR is not proof of lip sync.','Built-in image tool exposes no invoice; image costs are planning allowances.']}
 (O/'verification.json').write_text(json.dumps(result,indent=2)+'\n')
 times=[1.5,4.5,8,9.95,10,12,13.8,15,18,22,24.5,25.95,26,27.5,30,32.4,34.4,35.95];select='+'.join(f'eq(n\\,{round(t*24)})' for t in times)
 run('ffmpeg','-v','error','-y','-i',str(V),'-vf',f'select={select},scale=270:480,tile=6x3','-frames:v','1',str(O/'review-sheet.jpg'))
 print(json.dumps({k:result[k] for k in ['frames','audio_peak','audio_mix_correlation','native_voice_alignment','seams','source_comparisons','budget']},indent=2))
if __name__=='__main__':main()
