"""Verify the final Fold encode, exact seam states and newly authored audio mix."""
from amarillo.delivery import require_reverse_engineering

import hashlib,json,subprocess
from pathlib import Path
import numpy as np
P=Path('videos/fold');R=Path('artifacts/library-loop-11');O=Path('artifacts/final_outcome/fold');V=O/'fold.mp4'
def run(*args):return subprocess.check_output(args)
def pcm(p):return np.frombuffer(run('ffmpeg','-v','error','-i',str(p),'-vn','-ac','2','-ar','48000','-f','f32le','-'),dtype='<f4').reshape(-1,2)
def frame(t):return np.frombuffer(run('ffmpeg','-v','error','-ss',str(t),'-i',str(V),'-frames:v','1','-vf','scale=960:540','-pix_fmt','rgb24','-f','rawvideo','-'),dtype=np.uint8).astype(float)
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 require_reverse_engineering(V)
 raw=(R/'check-final.json').read_text();check=json.loads(raw[raw.index('{'):]);assert check['ok']
 assert not any(check[k]['findings'] for k in ['lint','runtime','layout','contrast'])
 meta=json.loads(run('ffprobe','-v','error','-show_format','-show_streams','-of','json',str(V)))
 v=next(s for s in meta['streams'] if s['codec_type']=='video');assert (v['width'],v['height'],v['r_frame_rate'])==(1920,1080,'24/1');assert int(v['nb_frames'])==744
 assert abs(float(meta['format']['duration'])-31)<.05
 decode=subprocess.run(['ffmpeg','-v','error','-i',str(V),'-f','null','-'],capture_output=True);assert decode.returncode==0 and not decode.stderr
 b=subprocess.run(['ffmpeg','-hide_banner','-i',str(V),'-vf','blackdetect=d=0.04:pix_th=0.08','-an','-f','null','-'],capture_output=True)
 black=[x for x in b.stderr.decode().splitlines() if 'black_start:'in x];assert not black
 actual=pcm(V);expected=np.concatenate([pcm(P/f'assets/voice/{i:02d}.wav') for i in [1,2,3]])+pcm(P/'assets/score.wav');n=min(len(actual),len(expected));corr=float(np.corrcoef(actual[:n].ravel(),expected[:n].ravel())[0,1]);assert corr>.99
 peak=float(abs(actual).max());assert peak<.9999
 joins=[]
 for t in [9,21]:
  error=float(abs(frame(t-1/24)-frame(t)).mean());assert error<2,(t,error);joins.append({'time':t,'adjacent_encoded_frames_mae_255':error})
 hold=float(abs(frame(29)-frame(30.95)).mean());assert hold<1
 budget=json.loads((R/'budget.json').read_text());assert budget['runs']=={} and budget['limit_cents']==1000
 geom=json.loads((R/'cursor-targets.json').read_text());assert all(x['inside'] for x in geom['clicks'])
 result={'path':str(V),'duration_seconds':31,'dimensions':[1920,1080],'fps':24,'frames':744,'sha256':digest(V),'bytes':V.stat().st_size,'full_decode':True,'black_intervals':black,'audio_mix_correlation_at_zero_offset':corr,'audio_peak':peak,'seam_checks':joins,'final_hold_mae_255':hold,'cursor_targets':geom['clicks'],'composition_checks':{k:{'errors':check[k]['errorCount'],'warnings':check[k]['warningCount']} for k in ['lint','runtime','layout','contrast']},'contrast_checks':{'passed':check['contrast']['passed'],'total':check['contrast']['checked']},'budget':{'estimated_generation_cost_cents':0,'cap_cents':1000,'paid_requests':0},'source_hashes':{str(p):digest(p) for p in [P/'index.html',*sorted((P/'compositions/frames').glob('*.html')),P/'assets/score.wav',*sorted((P/'assets/voice').glob('[0-9][0-9].wav'))]},'limitations':['Agent visual review of sampled encoded frames and transition sequences; no audience test or independent listening test.','Audio alignment and clipping checked numerically.','CLI motion sub-audit disabled; separate timeline inspection, seek-state regression and cursor geometry checks used.','Fictional product demonstration; no working backend or measured AI performance claimed.']}
 for p in [O/'verification.json',R/'delivery-verification.json']:p.write_text(json.dumps(result,indent=2)+'\n')
 run('ffmpeg','-v','error','-y','-i',str(V),'-vf','fps=16/31,scale=480:270,tile=4x4','-frames:v','1',str(O/'fold-frames.jpg'))
 run('ffmpeg','-v','error','-y','-ss','17.8','-i',str(V),'-frames:v','1',str(O/'fold-poster.jpg'))
 times=[0,.125,.5,.8,6.5,6.8,7.3,7.9,8.958333,9,9.125,9.5,20.958333,21,21.5,22,24.75,25.1,25.5,26,27,27.4,29,30.958333]
 indices=[round(t*24) for t in times];selection='+'.join(f'eq(n\\,{n})' for n in indices)
 run('ffmpeg','-v','error','-y','-i',str(V),'-vf',f'select={selection},scale=480:270,tile=4x6','-frames:v','1',str(O/'fold-transitions.jpg'))
 (O/'transition-times.json').write_text(json.dumps({'order':'left-to-right, top-to-bottom','times':[n/24 for n in indices]},indent=2)+'\n')
 print(json.dumps({k:result[k] for k in ['frames','audio_mix_correlation_at_zero_offset','audio_peak','seam_checks','final_hold_mae_255','contrast_checks']},indent=2))
if __name__=='__main__':main()
