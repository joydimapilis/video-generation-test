"""Verify the delivered Serein encode and the image-first source chain."""
import hashlib,json,subprocess
from pathlib import Path
import numpy as np
P=Path('videos/serein');R=Path('artifacts/library-loop-13');O=Path('artifacts/final_outcome/serein');V=O/'serein-mouse-revision.mp4'
def run(*args):return subprocess.check_output(args)
def pcm(p):return np.frombuffer(run('ffmpeg','-v','error','-i',str(p),'-vn','-ac','2','-ar','48000','-f','f32le','-'),dtype='<f4').reshape(-1,2)
def frame(p,t,w=960,h=540,filters=''):
 f=(filters+',' if filters else '')+f'scale={w}:{h}'
 return np.frombuffer(run('ffmpeg','-v','error','-ss',str(t),'-i',str(p),'-frames:v','1','-vf',f,'-pix_fmt','rgb24','-f','rawvideo','-'),dtype=np.uint8).reshape(h,w,3).astype(float)
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def main():
 raw=(R/'check-final.json').read_text();check=json.loads(raw[raw.index('{'):]);assert check['ok'];assert not any(check[k]['errorCount'] for k in ['lint','runtime','layout','contrast','motion'])
 meta=json.loads(run('ffprobe','-v','error','-show_format','-show_streams','-of','json',str(V)));v=next(s for s in meta['streams'] if s['codec_type']=='video')
 assert (v['width'],v['height'],v['r_frame_rate'],int(v['nb_frames']))==(1920,1080,'24/1',768);assert abs(float(meta['format']['duration'])-32)<.05
 decode=subprocess.run(['ffmpeg','-v','error','-i',str(V),'-f','null','-'],capture_output=True);assert decode.returncode==0 and not decode.stderr
 b=subprocess.run(['ffmpeg','-hide_banner','-i',str(V),'-vf','blackdetect=d=0.04:pix_th=0.08','-an','-f','null','-'],capture_output=True);black=[x for x in b.stderr.decode().splitlines() if 'black_start:' in x];assert not black
 actual=pcm(V);expected=np.concatenate([pcm(P/f'assets/voice/{i:02d}.wav') for i in [1,2,3]])+pcm(P/'assets/score.wav');n=min(len(actual),len(expected));corr=float(np.corrcoef(actual[:n].ravel(),expected[:n].ravel())[0,1]);peak=float(abs(actual).max());assert corr>.99;assert peak<.9999
 joins=[]
 for t in [8,24]:
  err=float(abs(frame(V,t-1/24)-frame(V,t)).mean());assert err<2,(t,err);joins.append({'time':t,'mae_255':err})
 hold=float(abs(frame(V,30.8)-frame(V,31.95)).mean());assert hold<1
 provenance=json.loads((P/'sources.json').read_text());reference=json.loads((R/'reviews/character-mouse-v2.json').read_text());assert reference['approved'];photo=[]
 for row in provenance:
  assert row['image_first'] and sha(row['source'])==row['source_sha256'];assert sha(P/row['reference'])==reference['source_sha256']==row['reference_sha256']
  for local in ([.8,2.4,4] if row['role']=='focus' else [1.5,2.5,4]):
   t=row['timeline_start']+local;width=row['crop']['width'];a=frame(V,t,width//2,540,f"crop={width}:1080:{row['display_x']}:0")
   b=frame(row['source'],row['source_start']+local*row.get('playback_rate',1),width//2,540,f'scale=1920:1080,crop={width}:1080:350:0');err=float(abs(a-b).mean());assert err<9,(t,err)
   photo.append({'timeline_time':t,'source_time':row['source_start']+local*row.get('playback_rate',1),'role':row['role'],'mae_255':err})
 budget=json.loads((R/'budget.json').read_text());estimated=sum(r['estimate_cents'] for r in budget['runs'].values());reserved=sum(r['reserved_cents'] for r in budget['runs'].values());assert reserved<=budget['limit_cents']==1000;assert all(r['status']=='completed' for r in budget['runs'].values())
 image_allowance=sum(r['estimate_cents'] for r in budget['runs'].values() if not r['payload'].get('endpoint'))
 geom=json.loads((R/'geometry.json').read_text());assert all(r['inside'] for r in geom['clicks']);assert geom['geometry']['end_minutes']-geom['geometry']['start_minutes']==90
 result={'path':str(V),'sha256':sha(V),'bytes':V.stat().st_size,'duration_seconds':32,'fps':24,'dimensions':[1920,1080],'frames':768,'full_decode':True,'black_intervals':black,'audio_peak':peak,'audio_mix_correlation':corr,'seams':joins,'source_comparisons':photo,'image_first':True,'reference_review':reference,'final_hold_mae_255':hold,'checks':{k:{'errors':check[k]['errorCount'],'warnings':check[k]['warningCount']} for k in ['lint','runtime','layout','motion','contrast']},'motion_enabled':check['motion'].get('enabled'),'contrast':{'passed':check['contrast']['passed'],'checked':check['contrast']['checked']},'budget':{'estimated_cents_including_image_allowance':estimated,'reserved_cents':reserved,'cap_cents':1000,'image_allowance_cents':image_allowance,'image_invoice':'not exposed by built-in tool; allowance is planning estimate','fal_estimated_cents':estimated-image_allowance},'source_hashes':{str(p):sha(p) for p in [P/'index.html',*sorted((P/'compositions/frames').glob('*.html'))]},'limitations':['Subjective sampled visual review; no independent audience test.','Image tool invoice not exposed; Per-image planning allowances included.','Product UI is a fictional authored demonstration.']}
 (O/'verification.json').write_text(json.dumps(result,indent=2)+'\n')
 times=[0,1,3,5,5.5,5.9,6,7.95833,8,10,13.4,14.8,17,20.5,21.4,22,23.95833,24,24.6,26,28,29,29.7,30.5,31.95]
 select='+'.join(f'eq(n\\,{round(t*24)})' for t in times)
 run('ffmpeg','-v','error','-y','-i',str(V),'-vf',f'select={select},scale=480:270,tile=5x5','-frames:v','1',str(O/'review-sheet.jpg'))
 print(json.dumps({k:result[k] for k in ['frames','audio_peak','audio_mix_correlation','seams','source_comparisons','contrast','budget']},indent=2))
if __name__=='__main__':main()
