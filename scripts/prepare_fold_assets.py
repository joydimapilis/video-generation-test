"""Time new local Fold narration and compose its original 120 BPM paper-pop score."""
import json, shutil, subprocess
from pathlib import Path
import numpy as np
from prepare_seventeen_assets import write_wav
ROOT=Path(__file__).resolve().parents[1]; P=ROOT/'videos/fold'; SR=48000; D=31

def main():
 meta=json.loads((P/'audio_meta.json').read_text()); plan=[]
 for v,d in zip(meta['voices'],[9,12,10]):
  src=P/'assets/voice'/f"{v['frame']:02d}.wav"; raw=src.with_name(src.stem+'-raw.wav')
  if not raw.exists(): shutil.copyfile(src,raw)
  pcm=subprocess.check_output(['ffmpeg','-v','error','-i',str(raw),'-f','f32le','-ar',str(SR),'-ac','1','-'])
  x=np.frombuffer(pcm,dtype=np.float32).astype(float); out=np.zeros((d*SR,2)); a=int(.3*SR)
  x*=.64/max(np.max(np.abs(x)),.01); out[a:a+len(x)]=x[:,None];write_wav(src,out)
  # Captions are skipped; original engine timestamps remain in separate metadata.
  v['duration_s']=d; v['words']=[] # captions intentionally skipped; alignment retained in engine metadata
  plan.append({'frame':v['frame'],'raw_duration':len(x)/SR,'lead_s':.3,'slot_s':d,'source':str(raw.relative_to(P))})
 music=np.zeros((D*SR,2));rng=np.random.default_rng(91511)
 def add(at,x,gain=1,pan=0):
  pos=round(at*SR); n=min(len(x),len(music)-pos)
  if n>0:music[pos:pos+n]+=x[:n,None]*gain*np.array([1-pan*.25,1+pan*.25])
 # Sparse major-sixth wood tones, brushed ticks and dry bass. Arrangement opens at product reveal.
 melody=[67,74,79,76,74,71,69,74,67,74,81,79,76,74,71,69]
 for i,at in enumerate(np.arange(0,29.5,.25)):
  t=np.arange(int(.38*SR))/SR; f=440*2**((melody[i%16]-69)/12)
  note=(np.sin(2*np.pi*f*t)+.22*np.sin(2*np.pi*f*3.01*t))*np.exp(-t*15)*np.minimum(t/.004,1)
  if i%2==0 or at>4: add(at,note,.032,(-1)**i*.6)
  if i%4==0:
   t=np.arange(int(.24*SR))/SR;add(at,np.sin(2*np.pi*(54*t+1.7*(1-np.exp(-30*t))))*np.exp(-t*20),.075)
  if i%4==2:
   t=np.arange(int(.06*SR))/SR;add(at,rng.normal(0,1,len(t))*np.exp(-t*65),.015)
 # Paper moves and exact interface clicks are part of this score, independently authored.
 for at in [1.25,3.6,6.5,19.0,21.4,24.5]:
  t=np.arange(int(.34*SR))/SR;noise=rng.normal(0,1,len(t));noise=np.convolve(noise,np.ones(8)/8,mode='same')
  add(at,noise*np.sin(np.pi*t/.34)**2,.075,.4)
 for at in [10.7,16.4]:
  t=np.arange(int(.07*SR))/SR;add(at,np.sin(2*np.pi*1250*t)*np.exp(-t*90),.055)
 # Closing chord resolves and decays through the final hold.
 t=np.arange(int(2.5*SR))/SR
 for midi in [55,62,67,71]:add(28.4,np.sin(2*np.pi*440*2**((midi-69)/12)*t)*np.exp(-t*2)*np.minimum(t/.015,1),.03)
 t=np.arange(D*SR)/SR; music*= (np.minimum(t/.1,1)*np.minimum((D-t)/.5,1))[:,None]
 write_wav(P/'assets/score.wav',music)
 meta['bgm']={'path':'assets/score.wav','volume':1};(P/'audio_meta.json').write_text(json.dumps(meta,indent=2)+'\n')
 (P/'audio-plan.json').write_text(json.dumps({'duration':D,'voice':'Kokoro am_michael, speed 1.02, local','schedule':plan,'score':'Original 120 BPM major-sixth wood-tone score; seed 91511','generation_cost_usd':0},indent=2)+'\n')
 (ROOT/'artifacts/library-loop-11/budget.json').write_text(json.dumps({'limit_cents':1000,'runs':{},'estimated_generation_cost_cents':0,'note':'Local Kokoro voice, original procedural score and HyperFrames; no paid generation calls.'},indent=2)+'\n')
if __name__=='__main__':main()
