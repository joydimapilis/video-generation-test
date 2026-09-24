"""Full encoded decode, expected identity, preview match and audio correlation.
Does not replace agent visual review; refuses completion without that review and the per-video document.
"""
from pathlib import Path
import subprocess,json,hashlib
import numpy as np
from PIL import Image
from amarillo.delivery import require_reverse_engineering
ROOT=Path(__file__).resolve().parents[2]; P=Path(__file__).resolve().parent
F=ROOT/'artifacts/final_outcome/kite-campaign/kite-campaign.mp4'
OUT=ROOT/'.context/kite-campaign-encoded';OUT.mkdir(parents=True,exist_ok=True)
def run(args):return subprocess.check_output(args)
def probe(path):return json.loads(run(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(path)]))
meta=probe(F);v=next(x for x in meta['streams'] if x['codec_type']=='video');a=next(x for x in meta['streams'] if x['codec_type']=='audio')
assert (v['width'],v['height'],v['r_frame_rate'])==(1920,1080,'30/1')
assert abs(float(meta['format']['duration'])-36)<.05
subprocess.run(['ffmpeg','-v','error','-i',str(F),'-f','null','-'],check=True)
count=run(['ffprobe','-v','error','-select_streams','v:0','-count_frames','-show_entries','stream=nb_read_frames','-of','csv=p=0',str(F)]).decode().strip();assert int(count)==1080
# Sample encoded visual motion at2fps across every scene, not just midpoints.
for i,start in enumerate([0,6,12,18,24,30]):
 subprocess.run(['ffmpeg','-v','error','-y','-ss',str(start),'-i',str(F),'-t','6','-vf','fps=2,scale=480:270,tile=4x3','-frames:v','1',str(OUT/f'motion-{i}.jpg')],check=True)
# Encoder vs inspected preview at held states plus end frame.
comparisons=[]
for t,fn in [(7.9,'frame-02-at-7.9s.png'),(15.9,'frame-06-at-15.9s.png'),(19.9,'frame-08-at-19.9s.png'),(27.9,'frame-12-at-27.9s.png'),(35.9,'frame-16-at-35.9s.png')]:
 target=OUT/f'held-{t}.png'
 subprocess.run(['ffmpeg','-v','error','-y','-ss',str(t),'-i',str(F),'-frames:v','1',str(target)],check=True)
 actual=np.asarray(Image.open(target).convert('RGB'),dtype=float)
 expected=np.asarray(Image.open(ROOT/'.context/kite-campaign-final-joins'/fn).convert('RGB'),dtype=float)
 mae=float(np.mean(np.abs(actual-expected)));assert mae<5,(t,mae)
 comparisons.append({'time':t,'rgb_mae_255':round(mae,4)})
# Decode encoded stereo PCM and compare with intended source.
raw=run(['ffmpeg','-v','error','-i',str(F),'-vn','-f','f32le','-ac','2','-ar','48000','-'])
x=np.frombuffer(raw,dtype='<f4').reshape(-1,2)
raw=run(['ffmpeg','-v','error','-i',str(P/'assets/score.wav'),'-f','f32le','-ac','2','-ar','48000','-']);y=np.frombuffer(raw,dtype='<f4').reshape(-1,2)
n=min(len(x),len(y));corr=float(np.corrcoef(x[:n].ravel(),y[:n].ravel())[0,1]);assert corr>.98
peak=float(np.max(np.abs(x)));assert peak<.99
report={'video':str(F.relative_to(ROOT)),'width':1920,'height':1080,'fps':30,'duration_seconds':float(meta['format']['duration']),'frames_decoded':int(count),'full_decode_pass':True,'preview_encoded_comparisons':comparisons,'audio':{'codec':a['codec_name'],'sample_rate':a['sample_rate'],'channels':a['channels'],'source_correlation':corr,'peak_dbfs':float(20*np.log10(peak)),'clipped_samples':int((np.abs(x)>=1).sum()),'review_method':'Numerical waveform, exact intended-score correlation and synthesis inspection. No independent listening claim.'},'status':'technical_checks_passed_pending_visual_review'}
(P/'encoded-technical-checks.json').write_text(json.dumps(report,indent=2))
print(json.dumps(report,indent=2))
