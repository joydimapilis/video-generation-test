"""Verify final Tuck encode, source plate timing, exact seams, UI and authored audio."""
from amarillo.delivery import require_reverse_engineering

import hashlib,json,subprocess
from pathlib import Path
import numpy as np
P=Path('videos/tuck');R=Path('artifacts/library-loop-12');O=Path('artifacts/final_outcome/tuck');V=O/'tuck.mp4'
def run(*args):return subprocess.check_output(args)
def pcm(p):return np.frombuffer(run('ffmpeg','-v','error','-i',str(p),'-vn','-ac','2','-ar','48000','-f','f32le','-'),dtype='<f4').reshape(-1,2)
def frame(p,t,w=960,h=540,filters=''):
 f=(filters+',' if filters else '')+f'scale={w}:{h}'
 return np.frombuffer(run('ffmpeg','-v','error','-ss',str(t),'-i',str(p),'-frames:v','1','-vf',f,'-pix_fmt','rgb24','-f','rawvideo','-'),dtype=np.uint8).reshape(h,w,3).astype(float)
def digest(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def main():
 require_reverse_engineering(V)
 raw=(R/'check-final.json').read_text();check=json.loads(raw[raw.index('{'):]);assert check['ok'];assert not any(check[k]['findings'] for k in ['lint','runtime','layout','contrast'])
 meta=json.loads(run('ffprobe','-v','error','-show_format','-show_streams','-of','json',str(V)));v=next(s for s in meta['streams'] if s['codec_type']=='video')
 assert(v['width'],v['height'],v['r_frame_rate'],int(v['nb_frames']))==(1920,1080,'24/1',720);assert abs(float(meta['format']['duration'])-30)<.05
 decode=subprocess.run(['ffmpeg','-v','error','-i',str(V),'-f','null','-'],capture_output=True);assert decode.returncode==0 and not decode.stderr
 b=subprocess.run(['ffmpeg','-hide_banner','-i',str(V),'-vf','blackdetect=d=0.04:pix_th=0.08','-an','-f','null','-'],capture_output=True);black=[x for x in b.stderr.decode().splitlines() if'black_start:'in x];assert not black
 actual=pcm(V);expected=np.concatenate([pcm(P/f'assets/voice/{i:02d}.wav') for i in [1,2,3]])+pcm(P/'assets/score.wav');n=min(len(actual),len(expected));corr=float(np.corrcoef(actual[:n].ravel(),expected[:n].ravel())[0,1]);assert corr>.99
 peak=float(abs(actual).max());assert peak<.9999
 joins=[]
 for t in [8,22]:
  error=float(abs(frame(V,t-1/24)-frame(V,t)).mean());assert error<2,(t,error);joins.append({'time':t,'adjacent_encoded_frames_mae_255':error})
 hold=float(abs(frame(V,28)-frame(V,29.95)).mean());assert hold<1
 # The new generated source and both derived source ranges must match actual encoded photo pixels.
 source=P/'assets/receipt-source.mp4';provenance=json.loads((P/'sources.json').read_text());assert digest(source)==digest(provenance[0]['source'])==provenance[0]['sha256']
 photo=[]
 for t in [1.0,2.5,3.75]:
  a=frame(V,t,545,540,'crop=1090:1080:830:0');b=frame(source,t+.5,545,540,'scale=1890:1080,crop=1090:1080:550:0');e=float(abs(a-b).mean());assert e<9,(t,e);photo.append({'timeline_time':t,'source_time':t+.5,'mae_255':e,'role':'opening'})
 for t in [23.5,24.5,25.5]:
  a=frame(V,t,435,540,'crop=870:1080:1050:0');b=frame(source,t-22+6,435,540,'scale=1890:1080,crop=870:1080:700:0');e=float(abs(a-b).mean());assert e<9,(t,e);photo.append({'timeline_time':t,'source_time':t-16,'mae_255':e,'role':'return'})
 budget=json.loads((R/'budget.json').read_text());estimated=sum(x['estimate_cents'] for x in budget['runs'].values());reserved=sum(x['reserved_cents'] for x in budget['runs'].values());assert reserved<=budget['limit_cents']==1000;assert all(x['status']=='completed' for x in budget['runs'].values())
 geom=json.loads((R/'cursor-targets.json').read_text());assert all(x['inside'] for x in geom['clicks']);assert geom['example_total_cents']==17840
 result={'path':str(V),'duration_seconds':30,'dimensions':[1920,1080],'fps':24,'frames':720,'sha256':digest(V),'bytes':V.stat().st_size,'full_decode':True,'black_intervals':black,'audio_mix_correlation_at_zero_offset':corr,'audio_peak':peak,'seam_checks':joins,'source_timing':photo,'final_hold_mae_255':hold,'cursor_targets':geom['clicks'],'example_total_cents':17840,'composition_checks':{k:{'errors':check[k]['errorCount'],'warnings':check[k]['warningCount']} for k in ['lint','runtime','layout','contrast']},'contrast_checks':{'passed':check['contrast']['passed'],'total':check['contrast']['checked']},'budget':{'estimated_generation_cost_cents':estimated,'reserved_cents':reserved,'cap_cents':1000,'paid_requests':len(budget['runs'])},'source_hashes':{str(p):digest(p) for p in [P/'index.html',*sorted((P/'compositions/frames').glob('*.html')),P/'assets/score.wav',P/'assets/opening.mp4',P/'assets/return.mp4']},'limitations':['Agent review of chronological and targeted encoded frame sequences; no audience study or independent listening test.','Audio alignment and clipping checked numerically.','CLI motion sub-audit disabled; separate timeline inspection, seek-state regression and cursor geometry used.','Fictional product UI and example data; no actual expense backend, reimbursement or tax claim.','Generated source is 1344x768, cropped and enlarged into 1080p photographic panels; authored UI is native1920x1080.','Returning footage uses source6–10s then a four-second final-frame hold; no new identity-conditioned take is implied.']}
 for p in [O/'verification.json',R/'delivery-verification.json']:p.write_text(json.dumps(result,indent=2)+'\n')
 run('ffmpeg','-v','error','-y','-i',str(V),'-vf','fps=16/30,scale=480:270,tile=4x4','-frames:v','1',str(O/'tuck-frames.jpg'))
 run('ffmpeg','-v','error','-y','-ss','1.3','-i',str(V),'-frames:v','1',str(O/'tuck-poster.jpg'))
 times=[0,.5,1.5,3.5,4.3,4.6,5,5.4,7.958333,8,8.25,8.75,17.2,17.5,18.7,19.5,21.958333,22,22.5,23.5,24,24.5,25,25.5,26,27,28,29.958333]
 indices=[round(t*24) for t in times];selection='+'.join(f'eq(n\\,{n})' for n in indices)
 run('ffmpeg','-v','error','-y','-i',str(V),'-vf',f'select={selection},scale=480:270,tile=4x7','-frames:v','1',str(O/'tuck-transitions.jpg'))
 (O/'transition-times.json').write_text(json.dumps({'order':'left-to-right, top-to-bottom','times':[n/24 for n in indices]},indent=2)+'\n')
 print(json.dumps({k:result[k] for k in ['frames','audio_mix_correlation_at_zero_offset','audio_peak','seam_checks','source_timing','final_hold_mae_255','contrast_checks','budget']},indent=2))
if __name__=='__main__':main()
