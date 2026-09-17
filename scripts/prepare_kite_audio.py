"""Local, exact-script Kite voice, caption timings and restrained original score."""
from pathlib import Path
import json, subprocess
import numpy as np
import soundfile as sf
from kokoro_onnx import Kokoro

ROOT=Path(__file__).resolve().parents[1]
P=ROOT/'videos/kite'; A=P/'assets'; V=A/'voice'; V.mkdir(exist_ok=True)
SR=48000; D=42
data=json.loads((P/'storyboard.json').read_text())
cache=Path.home()/'.cache/hyperframes/tts'
model=Kokoro(str(cache/'models/kokoro-v1.0.onnx'),str(cache/'voices/voices-v1.0.bin'))
voice=np.zeros((SR*D,2)); captions=[]; takes=[]
for i,c in enumerate(data['captions']):
 raw=V/f'{i+1:02}-raw.wav'; fitted=V/f'{i+1:02}.wav'
 if not raw.exists():
  x,sr=model.create(c['text'],voice='af_heart',speed=1.0,lang='en-us')
  # Remove engine padding only, preserving small breaths.
  idx=np.flatnonzero(np.abs(x)>.008)
  if len(idx):x=x[max(0,idx[0]-int(.04*sr)):min(len(x),idx[-1]+int(.09*sr))]
  sf.write(raw,x,sr)
 x,sr=sf.read(raw); duration=len(x)/sr
 slot=c['end']-c['start']; speed=max(.88,duration/(slot-.18))
 subprocess.run(['ffmpeg','-v','error','-y','-i',str(raw),'-af',f'atempo={speed}', '-ar',str(SR),'-ac','1',str(fitted)],check=True)
 x,sr=sf.read(fitted); x*=.64/max(.01,np.max(np.abs(x)))
 start=c['start']+.08; pos=round(start*SR)
 assert pos+len(x)<round(c['end']*SR)
 voice[pos:pos+len(x)]+=x[:,None]
 captions.append({'start':start,'end':min(c['end']-.03,start+len(x)/SR+.10),'text':c['text']})
 takes.append({'text':c['text'],'start':start,'duration':len(x)/SR,'rate':speed,'file':str(fitted.relative_to(P))})
 print(i+1,round(len(x)/SR,2),round(speed,3),c['text'],flush=True)
sf.write(A/'voice.wav',voice,SR)
music=np.zeros((SR*D,2));rng=np.random.default_rng(91742)
def add(at,x,gain=1,pan=0):
 pos=round(at*SR);n=min(len(x),len(music)-pos)
 if n>0:music[pos:pos+n]+=x[:n,None]*gain*np.array([1-pan*.2,1+pan*.2])
# Airy, slow-moving keyboard harmony and a soft 92 BPM pulse, no hype rises.
beat=60/92
for i,at in enumerate(np.arange(.2,40,beat*4)):
 chord=[[50,57,62,65],[48,55,60,64],[46,53,58,62],[48,55,60,67]][i%4]
 for j,m in enumerate(chord):
  t=np.arange(int(SR*2.8))/SR;f=440*2**((m-69)/12)
  x=(np.sin(2*np.pi*f*t)+.13*np.sin(2*np.pi*f*2*t))*np.exp(-t*1.65)*np.minimum(t/.045,1)
  add(at+j*.025,x,.010,(-1)**j*.5)
for i,at in enumerate(np.arange(.2,40,beat)):
 t=np.arange(int(SR*.2))/SR
 add(at,np.sin(2*np.pi*(48*t+.65*(1-np.exp(-t*30))))*np.exp(-t*24),.026)
 if i%2:
  t=np.arange(int(SR*.065))/SR
  add(at,rng.normal(0,1,len(t))*np.exp(-t*75),.003,.3)
# One low-key review-ready note. No sound on the approval or publish controls.
t=np.arange(int(.45*SR))/SR
add(26.2,(np.sin(2*np.pi*660*t)+.2*np.sin(2*np.pi*990*t))*np.exp(-t*12)*np.minimum(t/.01,1),.016)
t=np.arange(D*SR)/SR;music*=(np.minimum(t/.4,1)*np.minimum((D-t)/1.3,1))[:,None]
sf.write(A/'score.wav',music,SR)
sf.write(A/'mix-raw.wav',voice+music,SR)
subprocess.run(['ffmpeg','-v','error','-y','-i',str(A/'mix-raw.wav'),'-af','loudnorm=I=-16:TP=-1:LRA=8','-ar',str(SR),str(A/'mix.wav')],check=True)
(P/'captions.json').write_text(json.dumps(captions,indent=2,ensure_ascii=False)+'\n')
(P/'audio-plan.json').write_text(json.dumps({'duration':D,'voice':'Kokoro af_heart local','source':'six supplied lines split at caption phrase boundaries','takes':takes,'score':'original 92 BPM restrained keyboard/pulse, fixed seed91742','cost_usd':0},indent=2,ensure_ascii=False)+'\n')
print('Completed exact 42s mix and measured caption schedule.',flush=True)
