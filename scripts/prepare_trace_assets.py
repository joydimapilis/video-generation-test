"""Generate fresh local narration and an original score for the Trace film."""
import json, os, shutil, subprocess, wave
from pathlib import Path
import numpy as np
from prepare_seventeen_assets import read_wav, write_wav
ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT / 'hyperframes/trace'
SR, DURATION = 48000, 33
LINES = [
 ('01.wav', .3, "A bug report shouldn't start a guessing game."),
 ('02.wav', 3.5, 'Meet Trace. Browser bug reports, with the context.'),
 ('03.wav', 9.55, 'Record the problem once.'),
 ('04.wav', 13.1, 'Trace keeps the steps, the screenshot, and the browser details together.'),
 ('05.wav', 19.4, 'Share one report your developer can reproduce.'),
 ('06.wav', 24.0, 'Fewer follow-up questions. A clearer place to start.'),
 ('07.wav', 29.0, 'Trace. Capture your next bug.'),
]
def main():
 assets=PROJECT/'assets'; vo=assets/'vo'; vo.mkdir(parents=True, exist_ok=True)
 shutil.copyfile(ROOT/'hyperframes/motion5/assets/gsap.min.js',assets/'gsap.min.js')
 for name,source in [('TraceSans.ttf','Arial.ttf'),('TraceSans-Bold.ttf','Arial Bold.ttf')]:
  shutil.copyfile(Path('/System/Library/Fonts/Supplemental')/source, assets/name)
 env=os.environ.copy(); env['HYPERFRAMES_PYTHON']=str(ROOT/'.venv/bin/python')
 schedule=[]; voice=np.zeros((SR*DURATION,2))
 for i,(name,at,text) in enumerate(LINES):
  dst=vo/name
  if not dst.exists():
   r=subprocess.run(['npx','hyperframes@0.8.40','tts',text,'-v','af_heart','-s','1.03','-o',str(dst),'--json'],env=env,capture_output=True,text=True,cwd=PROJECT)
   if r.returncode: raise RuntimeError(r.stdout+r.stderr)
  data=read_wav(dst); duration=len(data)/SR
  next_start=LINES[i+1][1] if i+1<len(LINES) else DURATION
  if at+duration>next_start-.08: raise ValueError(f'VO overlaps: {name} ends {at+duration:.2f}, next {next_start}')
  edge=int(SR*.012); data[:edge]*=np.linspace(0,1,edge);data[-edge:]*=np.linspace(1,0,edge)
  start=round(at*SR);voice[start:start+len(data)]+=data[:,None]
  schedule.append(dict(file=name,start=at,duration=duration,text=text));print(name,duration,flush=True)
 voice*=.67/np.max(np.abs(voice));write_wav(assets/'voice.wav',voice)
 # New deterministic 108 BPM score: plucked A minor ostinato, sub pulse and soft hats.
 music=np.zeros((SR*DURATION,2));rng=np.random.default_rng(915);beat=60/108
 def add(at,data,gain=1,pan=0):
  start=round(at*SR);n=min(len(data),len(music)-start)
  if n>0 and start>=0: music[start:start+n]+=data[:n,None]*np.array([1-pan*.35,1+pan*.35])*gain
 for n,at in enumerate(np.arange(0,DURATION,beat/2)):
  tt=np.arange(int(SR*.55))/SR;freq=440*2**(([57,64,69,72,64,69,67,64][n%8]-69)/12)
  pluck=(np.sin(2*np.pi*freq*tt)+.18*np.sin(2*np.pi*freq*2*tt))*np.exp(-tt*11)*np.minimum(tt/.008,1)
  add(at,pluck,.03,(-1)**n*.7)
  if n%2==0:
   t=np.arange(int(SR*.3))/SR
   add(at,np.sin(2*np.pi*(48*t+2*(1-np.exp(-25*t))))*np.exp(-t*18)*np.minimum(t/.006,1),.045)
  if n%2:
   t=np.arange(int(SR*.04))/SR;add(at,rng.normal(0,1,len(t))*np.exp(-t*85),.009)
 t=np.arange(len(music))/SR;envv=np.minimum(t/.8,1)*np.minimum((DURATION-t)/1.4,1)
 for line in schedule:
  inside=(t>line['start']-.12)&(t<line['start']+line['duration']+.15)
  envv[inside]*=.55
 music*=envv[:,None];write_wav(assets/'score.wav',music)
 effects=np.zeros_like(music)
 for at in [10.5,12.45,17.0,23.2]:
  tt=np.arange(int(SR*.09))/SR;click=np.sin(2*np.pi*1700*tt)*np.exp(-tt*80)*np.minimum(tt/.002,1)*.055
  pos=round(at*SR);effects[pos:pos+len(click)]+=click[:,None]
 write_wav(assets/'clicks.wav',effects)
 (PROJECT/'audio-plan.json').write_text(json.dumps({'duration':DURATION,'voice':'Kokoro-82M af_heart speed 1.03, local','schedule':schedule,'score':'Original deterministic 108 BPM synth, seed915','predicted_peak':float(np.max(np.abs(voice+music+effects)))},indent=2)+'\n')
if __name__=='__main__':main()
