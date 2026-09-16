"""Stage reviewed I2V takes and original audio for Sideway."""
from pathlib import Path
import hashlib,json,subprocess
import numpy as np
from prepare_seventeen_assets import write_wav
P=Path('videos/sideway');R=Path('artifacts/library-loop-14');SR=48000;D=36

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def pcm(p):return np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',str(p),'-vn','-ar',str(SR),'-ac','2','-f','f32le','-']),dtype='<f4').reshape(-1,2).astype(float)
def main():
 selection=json.loads((P/'selected-takes.json').read_text())
 rows=[]
 for role in ['phone','story','arrival']:
  take=selection['takes'][role];version=take['reference_version'];run_id=take['run_id']
  src=R/f'outputs/{run_id}.mp4';dst=P/f'assets/{role}.mp4'
  subprocess.run(['ffmpeg','-v','error','-i',str(src),'-vf','fps=24,scale=1080:1920','-t','8' if role=='story' else '6','-an','-c:v','libx264','-crf','16','-preset','slow','-pix_fmt','yuv420p','-y',str(dst)],check=True)
  rows.append({'role':role,'run_id':run_id,'source':str(src),'source_sha256':sha(src),'derived':str(dst),'derived_sha256':sha(dst),'image_first':True,'reference':f'assets/{role}-reference-v{version}.png','reference_sha256':sha(P/f'assets/{role}-reference-v{version}.png'),'review':f'artifacts/library-loop-14/reviews/{role}-image-v{version}.json','ranges':({'timeline':[0,3],'source':[0,3]}, {'timeline':[6,10],'source':[1,3],'playback_rate':.5}) if role=='phone' else [{'timeline':[3,6],'source':[0,3]}] if role=='story' else [{'timeline':[26,32],'source':[0,6]}]})
 (P/'sources.json').write_text(json.dumps(rows,indent=2)+'\n')
 story_source=R/f"outputs/{selection['takes']['story']['run_id']}.mp4"
 x=pcm(story_source);gain=.72/max(abs(x).max(),.01);x*=gain;write_wav(P/'assets/native-story.wav',x)
 speech=np.zeros((D*SR,2));cuts=selection['speech_cuts']
 for a,b,start in cuts:
  segment=x[round(a*SR):round(b*SR)].copy();n=len(segment);fade=min(480,n//2);segment[:fade]*=np.linspace(0,1,fade)[:,None];segment[-fade:]*=np.linspace(1,0,fade)[:,None];at=round(start*SR);speech[at:at+n]=segment
 write_wav(P/'assets/speech.wav',speech)
 music=np.zeros((D*SR,2));rng=np.random.default_rng(91614);beat=.6
 def add(at,x,gain,pan=0):
  pos=round(at*SR);n=min(len(x),len(music)-pos)
  if n>0:music[pos:pos+n]+=x[:n,None]*gain*np.array([1-pan*.35,1+pan*.35])
 # New100BPM lightly syncopated electric-key/pluck score, not a reused soundtrack.
 chords=[[55,62,67,71,76],[57,64,67,72,76],[53,60,65,69,74],[48,55,60,64,69]]
 for bar,start in enumerate(np.arange(0,34,beat*4)):
  for k,m in enumerate(chords[bar%4]):
   t=np.arange(round(1.8*SR))/SR;f=440*2**((m-69)/12);wave=(np.sin(2*np.pi*f*t)+.23*np.sin(2*np.pi*f*2*t)+.08*np.sin(2*np.pi*f*3*t))*np.exp(-t*3)*np.minimum(t/.008,1)
   add(start+k*.023,wave,.027,(-1)**k*.5)
  for offset,m in [(1.5*beat,chords[bar%4][2]+12),(3*beat,chords[bar%4][3]+12)]:
   t=np.arange(round(.7*SR))/SR;add(start+offset,np.sin(2*np.pi*440*2**((m-69)/12)*t)*np.exp(-t*5)*np.minimum(t/.006,1),.017,.5)
 for i,at in enumerate(np.arange(0,34,beat)):
  t=np.arange(round(.28*SR))/SR
  if i%2==0:add(at,np.sin(2*np.pi*(48*t+.75*(1-np.exp(-25*t))))*np.exp(-t*22),.08)
  if i%4 in [1,3]:add(at,rng.normal(0,1,len(t))*np.exp(-t*45),.011,-.4)
  add(at+beat/2,rng.normal(0,1,len(t))*np.exp(-t*95),.009,.7)
 for at in [11.2,13.2,23.2]:
  t=np.arange(round(.07*SR))/SR;add(at,np.sin(2*np.pi*1000*t)*np.exp(-t*80),.04)
 for at in [8.55,14.15,26.2,31.55]:
  t=np.arange(round(.48*SR))/SR;noise=np.convolve(rng.normal(0,1,len(t)),np.ones(35)/35,mode='same');add(at,noise*np.sin(np.pi*t/.48)**2,.06)
 for k,m in enumerate([55,62,67,71,74]):
  t=np.arange(round(2.8*SR))/SR;add(33.1+k*.04,np.sin(2*np.pi*440*2**((m-69)/12)*t)*np.exp(-t*1.5)*np.minimum(t/.012,1),.025)
 t=np.arange(D*SR)/SR;env=np.minimum(t/.08,1)*np.minimum((D-t)/1.0,1)
 # Score authored with quiet speech windows, without affecting native dialogue.
 for a,b in [(start-.15,start+end-begin+.15) for begin,end,start in cuts]:
  env*=np.interp(t,[0,a-.15,a,b,b+.25,D],[1,1,.32,.32,1,1])
 music*=env[:,None];write_wav(P/'assets/score.wav',music)
 (P/'audio-plan.json').write_text(json.dumps({'duration':D,'native_source':str(story_source),'native_source_sha256':sha(story_source),'gain':gain,'sample_rate':SR,'cuts':[{'source_start':a,'source_end':b,'timeline_start':s} for a,b,s in cuts],'voice':'Native single Veo take; first experience on camera, reflection over arrival','score':'Original100BPM plucked keys/percussion, seed91614','generation_estimate_cents':0,'final_speech_sha256':sha(P/'assets/speech.wav'),'final_score_sha256':sha(P/'assets/score.wav')},indent=2)+'\n')
 print('Staged three reviewed clips, exact native voice excerpts and new original score.')
if __name__=='__main__':main()
