from pathlib import Path
import numpy as np,soundfile as sf,subprocess,json
from kokoro_onnx import Kokoro
R=Path(__file__).resolve().parents[1];P=R/'videos/kite-webinar';A=P/'assets';sr=48000;D=39
cache=Path.home()/'.cache/hyperframes/tts';k=Kokoro(str(cache/'models/kokoro-v1.0.onnx'),str(cache/'voices/voices-v1.0.bin'))
voice=np.zeros(D*sr);caps=[]
lines=[('You’ve got a webinar to run.',.45),('The page and the invitation',8.0),('shouldn’t take you away from it.',10.1),('You give the feedback.',27.8),('You decide what goes out.',31.6)]
for i,(line,at) in enumerate(lines):
 raw=A/f'vo-{i}.wav'
 if not raw.exists():
  x,rate=k.create(line,voice='af_heart',speed=.93,lang='en-us');nz=np.flatnonzero(abs(x)>.005);x=x[max(0,nz[0]-int(.04*rate)):nz[-1]+int(.12*rate)];sf.write(raw,x,rate)
 out=A/f'vo-{i}-48k.wav';subprocess.run(['ffmpeg','-v','error','-y','-i',str(raw),'-ar',str(sr),str(out)],check=True)
 x,_=sf.read(out);x*=.61/max(abs(x));pos=round(at*sr);voice[pos:pos+len(x)]+=x;caps.append({'text':line,'start':at,'end':at+len(x)/sr+.12});print(caps[-1],flush=True)
sf.write(A/'voice.wav',voice,sr)
# Original 100 BPM minimal score: mellow keys, rounded bass, restrained dry percussion.
N=sr*D;music=np.zeros((N,2));rng=np.random.default_rng(2026091714)
def add(at,x,g=.1,pan=0):
 pos=round(at*sr);n=min(len(x),N-pos)
 if n>0:music[pos:pos+n]+=x[:n,None]*g*np.array([1-pan*.2,1+pan*.2])
def note(m,d=1.8):
 t=np.arange(int(d*sr))/sr;f=440*2**((m-69)/12)
 return (np.sin(2*np.pi*f*t)+.19*np.sin(2*np.pi*2*f*t)+.045*np.sin(2*np.pi*3*f*t))*np.exp(-t*2.1)*np.minimum(t/.012,1)
beat=.6;chords=[[50,57,60,64],[48,55,59,62],[45,52,55,60],[43,50,54,57]]
for bar,at in enumerate(np.arange(.1,37,beat*4)):
 chord=chords[bar%4]
 for j,m in enumerate(chord):add(at+j*.035,note(m+12,2.5),.016,(-1)**j*.55)
 for off in [0,1.8]:
  t=np.arange(int(.58*sr))/sr;f=440*2**((chord[0]-12-69)/12);add(at+off,np.sin(2*np.pi*f*t)*np.minimum(t/.018,1)*np.exp(-t*4),.036)
 if bar>=2:
  for off,m in [(0.9,chord[2]+24),(1.5,chord[1]+24)]:add(at+off,note(m,.7),.008,(-1)**bar*.6)
for i,at in enumerate(np.arange(3.7,36.7,beat)):
 t=np.arange(int(.18*sr))/sr
 add(at,np.sin(2*np.pi*(49*t+.75*(1-np.exp(-28*t))))*np.exp(-30*t),.03)
 if i%2:
  t=np.arange(int(.10*sr))/sr;n=rng.normal(0,1,len(t));n=np.r_[0,np.diff(n)]
  add(at,n*np.exp(-t*48),.0038,.25)
 if i>6:
  t=np.arange(int(.035*sr))/sr;add(at+.3,rng.normal(0,1,len(t))*np.exp(-t*125),.0018,-.35)
t=np.arange(N)/sr;music*=np.minimum(t/.5,1)[:,None]*np.minimum((D-t)/2.0,1)[:,None]
sf.write(A/'score-raw.wav',music,sr)
subprocess.run(['ffmpeg','-v','error','-y','-i',str(A/'score-raw.wav'),'-af','loudnorm=I=-23:TP=-3:LRA=7','-ar',str(sr),str(A/'music.wav')],check=True)
sfx=np.zeros(N)
for at in [3.9,4.5,10,14,15.8,21,27,30.4,35]:
 t=np.arange(int(.08*sr))/sr;x=(np.sin(2*np.pi*190*t)+rng.normal(0,.1,len(t)))*.055*np.exp(-t*80);pos=round(at*sr);sfx[pos:pos+len(x)]+=x
sf.write(A/'sfx.wav',sfx,sr)
(P/'captions.json').write_text(json.dumps(caps,indent=2,ensure_ascii=False))
(P/'SCRIPT.md').write_text('# Original narration\n\nYou’ve got a webinar to run.\n\nThe page and the invitation shouldn’t take you away from it.\n\nYou give the feedback. You decide what goes out.\n\nLocal Kokoro af_heart, five measured caption phrases; original deterministic instrumental and soft action cues. Generation charge: $0.\n')
print('Created new voice, score, cues, measured captions. $0 generation charge.')
