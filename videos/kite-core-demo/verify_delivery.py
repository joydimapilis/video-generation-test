"""Verify this individual film before writing its completed delivery manifest."""
from pathlib import Path
import sys
import json
import hashlib
import subprocess
import numpy as np
from PIL import Image

PROJECT = Path(__file__).resolve().parent
REPO = PROJECT.parents[1]
sys.path.insert(0, str(REPO/'src'))
from amarillo.delivery import require_reverse_engineering

OUT = REPO/'artifacts/final_outcome/kite-core-demo'
VIDEO = OUT/'kite-core-demo.mp4'
def command(*args):
    return subprocess.check_output([str(x) for x in args])
def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()
def pcm(path):
    return np.frombuffer(command('ffmpeg','-v','error','-i',path,'-vn','-ac','2','-ar','48000','-f','f32le','-'),dtype='<f4')
def video_frame(t):
    return np.frombuffer(command('ffmpeg','-v','error','-ss',t,'-i',VIDEO,'-frames:v','1','-f','rawvideo','-pix_fmt','rgb24','-'),dtype='uint8').reshape(1080,1920,3)

def main():
    # Fail before writing any completed/successful delivery artifact.
    document = require_reverse_engineering(VIDEO)
    check = json.loads((PROJECT/'check-03.json').read_text())
    assert check['ok']
    for key in ['lint','runtime','layout','contrast']:
        assert check[key]['errorCount']==0 and check[key]['warningCount']==0
    review=json.loads((PROJECT/'encoded-review.json').read_text())
    assert review['decision']=='accept' and review['video_sha256']==digest(VIDEO)
    meta=json.loads(command('ffprobe','-v','error','-show_format','-show_streams','-of','json',VIDEO))
    v=next(s for s in meta['streams'] if s['codec_type']=='video')
    a=next(s for s in meta['streams'] if s['codec_type']=='audio')
    assert (v['width'],v['height'],v['r_frame_rate'])==(1920,1080,'30/1')
    assert int(v['nb_frames'])==900
    assert abs(float(meta['format']['duration'])-30)<.06
    decode=subprocess.run(['ffmpeg','-v','error','-i',str(VIDEO),'-f','null','-'],capture_output=True)
    assert decode.returncode==0 and not decode.stderr
    black=subprocess.run(['ffmpeg','-hide_banner','-i',str(VIDEO),'-vf','blackdetect=d=0.1:pix_th=0.08','-an','-f','null','-'],capture_output=True)
    black_intervals=[x for x in black.stderr.decode().splitlines() if 'black_start:' in x]
    assert not black_intervals
    actual,expected=pcm(VIDEO),pcm(PROJECT/'assets/score.wav')
    n=min(len(actual),len(expected)); correlation=float(np.corrcoef(actual[:n],expected[:n])[0,1])
    peak=float(np.abs(actual).max())
    assert correlation>.98 and peak<.999
    comparisons=[]
    for t,filename in [(1.5,'frame-00-at-1.5s.png'),(7.8,'frame-01-at-7.8s.png'),(17,'frame-04-at-17s.png'),(24.5,'frame-07-at-24.5s.png'),(29.8,'frame-08-at-29.8s.png')]:
        expected_frame=np.asarray(Image.open(REPO/'.context/kite-core-demo/snapshots-final'/filename).convert('RGB'))
        mae=float(np.abs(video_frame(t).astype(float)-expected_frame.astype(float)).mean())
        assert mae<5,(t,mae)
        comparisons.append({'seconds':t,'encoded_vs_preview_mae_255':round(mae,3)})
    ledger=json.loads((REPO/'artifacts/library-loop-kite-core-demo/budget.json').read_text())
    estimated=sum(x['estimate_cents'] for x in ledger['runs'].values())
    reserved=sum(x['reserved_cents'] for x in ledger['runs'].values())
    assert reserved<=1000 and ledger['limit_cents']==1000
    result={'video':str(VIDEO),'sha256':digest(VIDEO),'duration_seconds':30,'dimensions':[1920,1080],'fps':30,'frames':900,'full_decode':True,'black_intervals':black_intervals,'audio':{'codec':a['codec_name'],'sample_rate':a['sample_rate'],'channels':a['channels'],'score_correlation':correlation,'peak':peak},'encoded_preview_comparisons':comparisons,'composition':{'errors':0,'warnings':0,'contrast_passed':check['contrast']['passed'],'contrast_checked':check['contrast']['checked'],'automated_motion_subcheck_enabled':check['motion']['enabled']},'visual_review':review,'budget':{'cap_cents':1000,'estimated_cents':estimated,'reserved_cents':reserved,'confirmed_charge_cents':None,'paid_attempts':len(ledger['runs']),'local_audio_cost_cents':0},'source_hashes':{str(p.relative_to(REPO)):digest(p) for p in [PROJECT/'index.html',*sorted((PROJECT/'compositions/frames').glob('*.html')),PROJECT/'assets/score.wav',PROJECT/'assets/Onest.woff2']},'limitations':['Illustrative UI, not an authenticated backend capture.','Sampled chronological visual review and numerical audio checks; no audience test or independent listening.','Automated motion subcheck disabled; actual encoded frame sequences and preview equivalence checked.'],**document}
    (OUT/'verification.json').write_text(json.dumps(result,indent=2))
    (REPO/'review_notes/kite-core-demo-final-verification.json').write_text(json.dumps(result,indent=2))
    manifest={'status':'complete','project':'kite-core-demo','final_video':str(VIDEO),'editable_project':str(PROJECT),'demo_page':str(PROJECT/'DEMO.html'),'verification':str(OUT/'verification.json'),'phase2_used':False,'reference_library':json.loads((PROJECT/'reference-review.json').read_text())['library'],'budget':result['budget'],'limitations':result['limitations'],**document}
    (REPO/'assembled_outputs/kite-core-demo.json').write_text(json.dumps(manifest,indent=2))
    print(json.dumps({'status':'complete','duration_seconds':30,'frames':900,'audio_correlation':correlation,'comparisons':comparisons,**document},indent=2))

if __name__=='__main__':main()
