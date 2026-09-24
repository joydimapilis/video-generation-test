from pathlib import Path
import numpy as np,soundfile as sf,subprocess,json
from kokoro_onnx import Kokoro
P=Path(__file__).resolve().parents[1]/'videos/kite-tomorrow-revised'; A=P/'assets';sr=48000;D=38
cache=Path.home()/'.cache/hyperframes/tts'
k=Kokoro(str(cache/'models/kokoro-v1.0.onnx'),str(cache/'voices/voices-v1.0.bin'))
voice=np.zeros(D*sr);takes=[]
for i,(line,at) in enumerate([('The product’s ready.',.45),('The page isn’t.',4.0),('Now we have something to work with.',32.25)]):
 raw=A/f'vo-{i}.wav'
 if not raw.exists():
  x,rate=k.create(line,voice='af_heart',speed=.94,lang='en-us')
  nz=np.flatnonzero(abs(x)>.005);x=x[max(0,nz[0]-int(.045*rate)):nz[-1]+int(.12*rate)]
  sf.write(raw,x,rate)
 subprocess.run(['ffmpeg','-v','error','-y','-i',str(raw),'-ar',str(sr),str(A/f'vo-{i}-48k.wav')],check=True)
 x,_=sf.read(A/f'vo-{i}-48k.wav');x*=.60/max(abs(x));p=round(at*sr);voice[p:p+len(x)]+=x
 takes.append({'text':line,'start':at,'end':at+len(x)/sr})
 print(takes[-1],flush=True)
sf.write(A/'voice.wav',voice,sr)
sfx=np.zeros(D*sr);rng=np.random.default_rng(91738)
for at in [3.6,7.2,13.8,15.8,24.6,30.4,35]:
 t=np.arange(int(.10*sr))/sr
 x=(rng.normal(0,1,len(t))*.20+np.sin(2*np.pi*170*t))*.065*np.exp(-t*75)
 pos=round(at*sr);sfx[pos:pos+len(x)]+=x
sf.write(A/'sfx.wav',sfx,sr)
(P/'narration.json').write_text(json.dumps(takes,indent=2,ensure_ascii=False))
print('Voice and tactile cut cues ready.')
