"""Original forty-second minimal electronic score, synthesized locally."""
from pathlib import Path
import numpy as np, soundfile as sf, subprocess
R=Path(__file__).resolve().parents[1];A=R/'videos/kite-judgment/assets';sr=48000;D=40;N=sr*D
music=np.zeros((N,2));rng=np.random.default_rng(20260917)
def add(at,x,g=1,pan=0):
 p=round(at*sr);n=min(len(x),N-p)
 if n>0:
  gains=np.sqrt(np.array([1-pan,1+pan])/2)
  music[p:p+n]+=x[:n,None]*g*gains

def key(m,d=2.0):
 t=np.arange(int(d*sr))/sr;f=440*2**((m-69)/12)
 fm=.45*np.sin(2*np.pi*f*2*t)*np.exp(-t*5)
 x=np.sin(2*np.pi*f*t+fm)+.12*np.sin(2*np.pi*3*f*t)*np.exp(-t*8)
 return x*np.minimum(t/.006,1)*np.exp(-t*2.2)*np.minimum((d-t)/.1,1)
def pad(m,d=3.3):
 t=np.arange(int(d*sr))/sr;f=440*2**((m-69)/12)
 x=.7*np.sin(2*np.pi*f*t)+.17*np.sin(2*np.pi*f*1.003*t)+.12*np.sin(2*np.pi*f*2*t)
 return x*np.minimum(t/.7,1)*np.minimum((d-t)/.9,1)
chords=[[50,57,61,64],[54,57,61,64],[45,52,59,61],[52,59,64,66]]
beat=.625
for bar in range(16):
 at=bar*2.5;ch=chords[bar%4]
 # Sparse first four bars, more coherent rhythm after the objects align.
 for j,m in enumerate(ch):
  add(at+.025*j,key(m+12,2.8),.047 if bar<5 else .035,[-.5,.25,-.2,.6][j])
  if bar>=5:add(at,pad(m,3.1),.016,[-.4,.4,-.25,.25][j])
 if 3<=bar<14:
  for off in [0,1.25]:
   t=np.arange(int(.6*sr))/sr;f=440*2**((ch[0]-12-69)/12)
   add(at+off,np.sin(2*np.pi*f*t)*np.minimum(t/.014,1)*np.exp(-t*5),.09)
 if 5<=bar<14:
  for off,m in [(.625,ch[1]+24),(1.875,ch[3]+12)]:
   x=key(m,.9);add(at+off,x,.028,(-1)**bar*.45);add(at+off+.3125,x,.008,-(-1)**bar*.45)
for n,at in enumerate(np.arange(7.5,34.9,beat)):
 t=np.arange(int(.24*sr))/sr
 if n%2==0:add(at,np.sin(2*np.pi*(47*t+.62*(1-np.exp(-35*t))))*np.exp(-t*25),.10)
 else:
  noise=rng.normal(0,1,len(t));sm=np.convolve(noise,np.ones(9)/9,'same')
  add(at,(sm*.65+np.sin(2*np.pi*170*t)*.09)*np.exp(-t*37),.025,.08)
 if at>=14:
  t=np.arange(int(.045*sr))/sr;noise=rng.normal(0,1,len(t));hp=np.r_[0,np.diff(noise)]
  add(at+.3125,hp*np.exp(-t*100),.0025,(-1)**n*.4)
# Warm, unhurried resolution at the lockup, with no success fanfare.
for j,m in enumerate([50,57,61,64,69]):add(36+j*.05,key(m+12,4),.031,(-1)**j*.5)
# Small stereo room reflections, no plugin or external assets.
dry=music.copy()
for delay,g in [(.087,.10),(.173,.065),(.291,.045)]:
 n=int(delay*sr);music[n:]+=dry[:-n,::-1]*g
t=np.arange(N)/sr;music*=np.minimum(t/.18,1)[:,None]*np.minimum((D-t)/1.4,1)[:,None]
sf.write(A/'score-raw.wav',music,sr)
subprocess.run(['ffmpeg','-v','error','-y','-i',str(A/'score-raw.wav'),'-af','loudnorm=I=-19:TP=-2:LRA=7','-ar',str(sr),str(A/'score.wav')],check=True)
sfx=np.zeros((N,2))
for at in [0.25,4.25,4.87,5.49,6.11,6.73,12.0,17.9,21.3,24.7,30.8]:
 t=np.arange(int(.11*sr))/sr
 x=(np.sin(2*np.pi*147*t)*.48+rng.normal(0,.15,len(t)))*np.minimum(t/.003,1)*np.exp(-t*65)
 p=round(at*sr);sfx[p:p+len(x)]+=x[:,None]*.065
sf.write(A/'sfx.wav',sfx,sr)
print('Original score and soft object sounds written; no paid generation.')
