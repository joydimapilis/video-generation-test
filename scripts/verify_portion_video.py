"""Verify delivered Portion media, source selection, exact data and budget.
Perceptual scores remain subjective in scorecard.json; these are technical checks.
"""
from pathlib import Path
import hashlib,io,json,subprocess,wave
import numpy as np
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[1]
PROJECT=ROOT/'videos/portion'; RUN=ROOT/'artifacts/library-loop-15'
FINAL=ROOT/'artifacts/final_outcome/portion/portion.mp4'
QA=FINAL.parent/'verification';QA.mkdir(parents=True,exist_ok=True)
def cmd(args):return subprocess.check_output(args)
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def frame(path,t,filter='scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080'):
    return Image.open(io.BytesIO(cmd(['ffmpeg','-v','error','-ss',f'{t:.6f}','-i',str(path),'-vf',filter,'-frames:v','1','-f','image2pipe','-vcodec','png','-']))).convert('RGB')
probe=json.loads(cmd(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(FINAL)]))
v=next(x for x in probe['streams'] if x['codec_type']=='video');a=next(x for x in probe['streams'] if x['codec_type']=='audio')
assert(v['width'],v['height'],v['r_frame_rate'],int(v['nb_frames']))==(1920,1080,'24/1',864)
assert abs(float(probe['format']['duration'])-36)<.06
p=subprocess.run(['ffmpeg','-v','error','-i',str(FINAL),'-f','null','-'],capture_output=True)
assert p.returncode==0 and not p.stderr,p.stderr
b=subprocess.run(['ffmpeg','-hide_banner','-i',str(FINAL),'-vf','blackdetect=d=0.08:pix_th=0.08','-an','-f','null','-'],capture_output=True)
assert b.returncode==0 and b'black_start:' not in b.stderr
# AAC output versus original sum, allowing codec delay only if correlation requires it.
audio=np.frombuffer(cmd(['ffmpeg','-v','error','-i',str(FINAL),'-vn','-ar','48000','-ac','2','-f','f32le','-']),dtype='<f4').reshape(-1,2)
expected=np.zeros((36*48000,2),np.float64)
for name in ['score.wav','ui-sfx.wav']:
    with wave.open(str(PROJECT/'assets'/name),'rb') as w:expected+=np.frombuffer(w.readframes(w.getnframes()),dtype='<i2').reshape(-1,2)/32768
n=min(len(audio),len(expected));corr=float(np.corrcoef(audio[:n].flatten(),expected[:n].flatten())[0,1]);peak=float(np.max(np.abs(audio)))
assert corr>.97,corr
assert 0.02<peak<.99,peak
# Comparison over unobscured person/prop area. Small resizing/AAC differences are expected.
source_checks=[]
for role,times,offset in [('before',[.5,1.5,3,4.3],.3),('after',[26.6,27.7,29.2,30.7],-25.6)]:
    for t in times:
        out=np.asarray(frame(FINAL,t).crop((750,40,1880,1010))).astype(float)
        expected_t=t+offset
        scores=[]
        for delta in [-1/24,0,1/24]:
            src=np.asarray(frame(PROJECT/'assets'/f'{role}.mp4',max(0,expected_t+delta)).crop((750,40,1880,1010))).astype(float)
            scores.append(float(np.mean(np.abs(out-src))))
        best=min(scores);source_checks.append({'role':role,'timeline_time':t,'source_time':expected_t,'mean_abs_error_255':best})
        assert best<6.5,(role,t,best)
# Final text holds for a deliberate finish.
hold=float(np.mean(np.abs(np.asarray(frame(FINAL,34)).astype(float)-np.asarray(frame(FINAL,35.875)).astype(float))))
assert hold<.75,hold
ledger=json.loads((RUN/'budget.json').read_text());est=sum(x['estimate_cents'] for x in ledger['runs'].values());res=sum(x['reserved_cents'] for x in ledger['runs'].values())
assert est==404 and res==467 and res<=ledger['limit_cents']==1000
for role in ['before','after']:
    review=json.loads((RUN/'reviews'/f'{role}-image-v1.json').read_text())
    assert review['approved'] and review['source_sha256']==sha(PROJECT/'assets'/f'{role}-reference-v1.png')
assert sha(PROJECT/'assets/before.mp4')==sha(RUN/'outputs/portion_before_v2.mp4')
assert sha(PROJECT/'assets/after.mp4')==sha(RUN/'outputs/portion_after_v1.mp4')
assert json.loads((RUN/'check-final.json').read_text())['ok']
assert json.loads((RUN/'geometry.json').read_text())['passed']
# Encoded final review sheets, including transitions and actual used human ranges.
times=[.5,3,4.7,5.35,8.4,10.3,11.7,14.15,15.7,17.2,20.2,23.2,24.8,25.8,27.5,30.5,31.4,32,34,35.875]
sheet=Image.new('RGB',(4*480,5*292),'#17291F');draw=ImageDraw.Draw(sheet)
for i,t in enumerate(times):
    im=frame(FINAL,t).resize((480,270));x=(i%4)*480;y=(i//4)*292
    sheet.paste(im,(x,y+22));draw.text((x+10,y+4),f'{t:.3f}s',fill='white')
sheet.save(QA/'final-contact-sheet.jpg',quality=93)
for role,times in [('before',[.3+i*.38 for i in range(12)]),('after',[26.2+i*.41 for i in range(12)])]:
    sheet=Image.new('RGB',(6*330,2*380),'#17291F');draw=ImageDraw.Draw(sheet)
    for i,t in enumerate(times):
        im=frame(FINAL,t).crop((1000,0,1880,950)).resize((330,356));x=(i%6)*330;y=(i//6)*380
        sheet.paste(im,(x,y+24));draw.text((x+8,y+5),f'{t:.2f}s',fill='white')
    sheet.save(QA/f'final-{role}-interaction.jpg',quality=94)
result={'passed':True,'path':str(FINAL.relative_to(ROOT)),'sha256':sha(FINAL),'bytes':FINAL.stat().st_size,'duration':float(probe['format']['duration']),'width':1920,'height':1080,'fps':24,'frames':864,'full_decode':True,'black_gaps':False,'audio_peak_dbfs':float(20*np.log10(peak)),'audio_source_correlation':corr,'source_comparisons':source_checks,'final_hold_pixel_error':hold,'budget_estimated_cents':est,'budget_reserved_cents':res,'budget_cap_cents':1000,'human_review':'See scorecard and encoded chronological sheets; source matches are technical evidence, not aesthetic scores.'}
(QA/'verification.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
