"""Create paced local narration and an original warm 96 BPM Tuck score."""
import json,shutil,subprocess,hashlib
from pathlib import Path
import numpy as np
from prepare_seventeen_assets import write_wav
ROOT=Path(__file__).resolve().parents[1];P=ROOT/'videos/tuck';SR=48000;D=30

def pcm(p):return np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',str(p),'-f','f32le','-ar',str(SR),'-ac','1','-']),dtype=np.float32).astype(float)
def main():
 meta=json.loads((P/'audio_meta.json').read_text());plan=[]
 for v,d,pauses in zip(meta['voices'],[8,14,8],[[(3.055,.8)],[(5.55,1.5),(6.34,.55)],[(2.71,.9)]]):
  src=P/f"assets/voice/{v['frame']:02d}.wav";raw=src.with_name(src.stem+'-raw.wav')
  if not raw.exists():shutil.copyfile(src,raw)
  x=pcm(raw);x*=.60/max(.01,abs(x).max());pieces=[];last=0;actualpauses=[]
  for target,length in pauses:
   center=round(target*SR);candidates=range(max(last,center-1920),min(len(x)-240,center+1920),48)
   index=min(candidates,key=lambda k:float(np.mean(x[k:k+240]**2)))+120
   pieces.extend([x[last:index],np.zeros(round(length*SR))]);last=index;actualpauses.append({'raw_time':index/SR,'pause_s':length})
  pieces.append(x[last:]);voice=np.concatenate(pieces);out=np.zeros((d*SR,2));at=round(.3*SR);assert at+len(voice)<=len(out);out[at:at+len(voice)]=voice[:,None]
  write_wav(src,out);v.update(duration_s=d,words=[])
  plan.append({'frame':v['frame'],'source':str(raw.relative_to(P)),'raw_duration':len(x)/SR,'lead_s':.3,'inserted_pauses':actualpauses,'duration_s':d})
 music=np.zeros((SR*D,2));rng=np.random.default_rng(91512);beat=.625
 def add(at,x,gain=1,pan=0):
  pos=round(at*SR);n=min(len(x),len(music)-pos)
  if n>0:music[pos:pos+n]+=x[:n,None]*gain*np.array([1-pan*.3,1+pan*.3])
 # Electric-piano harmonics and a dry, quiet heartbeat; no reused melody or sample.
 chords=[[53,60,64,69],[55,62,65,69],[57,64,67,72],[48,55,62,64]]
 for bar,start in enumerate(np.arange(0,27.5,beat*4)):
  for n,midi in enumerate(chords[bar%4]):
   t=np.arange(int(SR*2.1))/SR;f=440*2**((midi-69)/12)
   x=(np.sin(2*np.pi*f*t)+.22*np.sin(2*np.pi*f*2*t)+.08*np.sin(2*np.pi*f*4*t))*np.exp(-t*2.5)*np.minimum(t/.012,1)
   add(start+n*.045,x,.014,(-1)**n*.5)
 for i,start in enumerate(np.arange(0,28,beat)):
  t=np.arange(int(SR*.23))/SR;add(start,np.sin(2*np.pi*(45*t+1.8*(1-np.exp(-t*28))))*np.exp(-t*19),.046)
  if i%2:
   t=np.arange(int(SR*.07))/SR;noise=rng.normal(0,1,len(t));noise=np.concatenate([[0],np.diff(noise)]);add(start,noise*np.exp(-t*80),.006,.25)
 for at in [2.0,4.4,6.8,18.4,22.4]:
  t=np.arange(int(.3*SR))/SR;noise=rng.normal(0,1,len(t));noise=np.convolve(noise,np.ones(11)/11,mode='same');add(at,noise*np.sin(np.pi*t/.3)**2,.055,.45)
 for at in [10.2,17.2]:
  t=np.arange(int(.07*SR))/SR;add(at,np.sin(2*np.pi*950*t)*np.exp(-t*90),.05)
 t=np.arange(int(2.7*SR))/SR
 for m in [53,60,64,69]:add(27.1,np.sin(2*np.pi*440*2**((m-69)/12)*t)*np.exp(-t*1.6)*np.minimum(t/.02,1),.019)
 t=np.arange(D*SR)/SR;music*=(np.minimum(t/.2,1)*np.minimum((D-t)/.8,1))[:,None]
 write_wav(P/'assets/score.wav',music);meta['bgm']={'path':'assets/score.wav','volume':1};(P/'audio_meta.json').write_text(json.dumps(meta,indent=2)+'\n');(P/'audio-plan.json').write_text(json.dumps({'duration':D,'voice':'Kokoro af_heart, 1.01; new local take','schedule':plan,'score':'Original 96 BPM warm electric-piano synthesis, seed91512; click/paper accents','generation_api_cost':0},indent=2)+'\n')
if __name__=='__main__':main()
