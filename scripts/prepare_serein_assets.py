"""Stage newly generated Serein media, paced narration and a new original score."""
from pathlib import Path
import json,shutil,subprocess,hashlib
import numpy as np
from prepare_seventeen_assets import write_wav
R=Path(__file__).resolve().parents[1];P=R/'videos/serein';SR=48000;D=32

def pcm(p):return np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',str(p),'-f','f32le','-ar',str(SR),'-ac','1','-']),dtype=np.float32).astype(float)
def main():
 meta=json.loads((P/'audio_meta.json').read_text());schedule=[]
 # Fresh TTS normalized and slowed modestly; phrase gaps paced to picture cues.
 settings=[(8,[(.92,.2),(2.46,.85),(3.35,.45)],.25),(16,[(1.65,.15),(4.5,.25),(8.42,.3),(9.62,.2)],.3),(8,[(1.17,.4),(2.8,1.4),(3.27,.25)],.3)]
 for v,(dur,pauses,lead) in zip(meta['voices'],settings):
  src=P/v['path'];raw=src.with_name(src.stem+'-raw.wav')
  if not raw.exists():shutil.copyfile(src,raw)
  x=pcm(raw);x*=.58/max(.01,abs(x).max());pieces=[];last=0;actual=[]
  # Forced word times can exceed actual PCM; seek quiet gaps near the phrase boundary.
  for target,length in pauses:
   center=round(target*SR);lo=max(last,center-3500);hi=min(len(x)-240,center+2500)
   if hi<=lo:continue
   index=min(range(lo,hi,48),key=lambda k:float(np.mean(x[k:k+240]**2)))+120
   pieces.extend([x[last:index],np.zeros(round(length*SR))]);last=index;actual.append({'raw_time':index/SR,'pause_s':length})
  pieces.append(x[last:]);voice=np.concatenate(pieces)
  # Middle line uses a measured 0.87 rate, giving review time without changing pitch.
  if v['frame']==2:
   tmp=P/'assets/voice/middle-paced.wav';write_wav(tmp,voice[:,None].repeat(2,axis=1));voice=np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',str(tmp),'-af','atempo=0.87','-f','f32le','-ar',str(SR),'-ac','1','-']),dtype='<f4').astype(float)
  out=np.zeros((dur*SR,2));at=round(lead*SR);assert at+len(voice)<=len(out),(v['frame'],len(voice)/SR)
  out[at:at+len(voice)]=voice[:,None];write_wav(src,out);v.update(duration_s=dur,words=[])
  schedule.append({'frame':v['frame'],'raw_duration':len(x)/SR,'spoken_with_pauses_s':len(voice)/SR,'lead':lead,'pauses':actual,'rate':.87 if v['frame']==2 else 1})
 music=np.zeros((D*SR,2));rng=np.random.default_rng(91613);beat=60/84
 def add(at,x,gain=1,pan=0):
  pos=round(at*SR);n=min(len(x),len(music)-pos)
  if n>0:music[pos:pos+n]+=x[:n,None]*gain*np.array([1-pan*.3,1+pan*.3])
 # Original sparse felt-piano progression, airy pluck response and soft pulse.
 chords=[[50,57,62,65,69],[46,53,58,62,65],[53,60,65,69,72],[48,55,60,64,67]]
 for bar,start in enumerate(np.arange(0,29,4*beat)):
  for k,m in enumerate(chords[bar%4]):
   t=np.arange(int(2.7*SR))/SR;f=440*2**((m-69)/12)
   x=(np.sin(2*np.pi*f*t)+.18*np.sin(2*np.pi*2*f*t)+.05*np.sin(2*np.pi*3*f*t))*np.exp(-t*1.7)*np.minimum(t/.025,1)
   add(start+k*.035,x,.015,(-1)**k*.5)
 for i,start in enumerate(np.arange(0,29,beat)):
  t=np.arange(int(.22*SR))/SR
  if i%2==0:add(start,np.sin(2*np.pi*(43*t+.9*(1-np.exp(-t*20))))*np.exp(-t*25),.03)
  if i%4==3:add(start,rng.normal(0,1,len(t))*np.exp(-t*55),.003,.5)
 for at in [13.4,19.5]:
  t=np.arange(int(.09*SR))/SR;add(at,np.sin(2*np.pi*850*t)*np.exp(-t*75),.035)
 for at in [5.45,21.35,24.2,28.85]:
  t=np.arange(int(.6*SR))/SR;n=rng.normal(0,1,len(t));n=np.convolve(n,np.ones(23)/23,mode='same');add(at,n*np.sin(np.pi*t/.6)**2,.035)
 for k,m in enumerate([50,57,62,65,69]):
  t=np.arange(int(2.7*SR))/SR;add(29+k*.04,np.sin(2*np.pi*440*2**((m-69)/12)*t)*np.exp(-t*1.4)*np.minimum(t/.025,1),.017)
 t=np.arange(D*SR)/SR;music*=(np.minimum(t/.4,1)*np.minimum((D-t)/1.1,1))[:,None]
 write_wav(P/'assets/score.wav',music);meta['bgm']={'path':'assets/score.wav','volume':1};(P/'audio_meta.json').write_text(json.dumps(meta,indent=2)+'\n')
 (P/'audio-plan.json').write_text(json.dumps({'duration':D,'voice':'Fresh local Kokoro af_bella','schedule':schedule,'score':'Original84BPM felt-piano, seed91613; no previous audio reused','api_cost':0},indent=2)+'\n')
 print(json.dumps(schedule,indent=2))
if __name__=='__main__':main()
