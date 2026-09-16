"""Original deterministic 36s instrumental score and timed interface foley.
No borrowed recording or previous-video audio. 100 BPM, soft felt-key synthesis,
muted bass and brushed percussion. Musical density opens after product reveal.
"""
from pathlib import Path
import json, wave
import numpy as np
SR=48000; DUR=36; N=SR*DUR
rng=np.random.default_rng(150916)
mix=np.zeros((N,2),dtype=np.float64); fx=np.zeros_like(mix)
def add(dest,sound,at,gain=1,pan=0):
    start=int(at*SR); count=min(len(sound),N-start)
    if count<=0:return
    dest[start:start+count,0]+=sound[:count]*gain*np.sqrt((1-pan)/2)
    dest[start:start+count,1]+=sound[:count]*gain*np.sqrt((1+pan)/2)
def note(midi,duration=2.8):
    t=np.arange(int(SR*duration))/SR; f=440*2**((midi-69)/12)
    attack=1-np.exp(-t/0.005)
    # Gentle inharmonic overtones and tiny deterministic detune: felt-key timbre.
    s=np.sin(2*np.pi*f*t)*np.exp(-t/1.65)
    s+=.23*np.sin(2*np.pi*f*2.002*t)*np.exp(-t/.55)
    s+=.085*np.sin(2*np.pi*f*3.005*t)*np.exp(-t/.23)
    s+=.024*np.sin(2*np.pi*f*5.004*t)*np.exp(-t/.09)
    return s*attack*np.minimum(1,(duration-t)/.15)
beat=.6
# Fmaj7, C6/E, Dm7, Bbmaj7; fresh melody, no previously used score.
chords=[[53,57,60,64],[52,55,60,64],[50,53,57,60],[46,53,57,62]]
for bar in range(14):
    base=bar*2.4; ch=chords[(bar//2)%4]
    for j,n in enumerate(ch[1:]):
        add(mix,note(n+12,2.3),base+.025*j,.044 if base<9.6 else .058,[-.27,.03,.25][j])
    if base>=9.6:
        add(mix,note(ch[0]-12,1.4),base,.10,-.08)
        add(mix,note(ch[0]-12,1),base+1.2,.07,.08)
    elif bar%2==0:
        add(mix,note(ch[0],2),base,.07,-.1)
    pattern=[ch[2]+12,ch[3]+12,ch[1]+12,ch[2]+12]
    for k,n in enumerate(pattern):
        if base<9.6 and k%2:continue
        add(mix,note(n,1.1),base+.6*k+.3,.045 if base<9.6 else .053,(-1)**k*.32)
    if 9.6<=base<31.2:
        for k in range(8):
            t=np.arange(int(.11*SR))/SR
            noise=rng.normal(0,1,len(t)); noise=np.convolve(noise,np.ones(5)/5,'same')
            brush=noise*np.exp(-t/0.022)*(1-np.exp(-t/.002))
            add(mix,brush,base+.3*k,.022 if k%2 else .014,(-1)**k*.37)
        for k in [0,2]:
            t=np.arange(int(.21*SR))/SR
            kick=np.sin(2*np.pi*(49*t+15*.028*(1-np.exp(-t/.028))))*np.exp(-t/.062)
            add(mix,kick,base+.6*k,.08,0)
# Warm ending cadence, fading tail.
for j,n in enumerate([41,53,57,60,65]):add(mix,note(n,3.5),32.4+j*.035,.065,j*.08-.16)
# Short stereo room, no external IR.
for delay,level in [(.079,.14),(.137,.09),(.223,.055)]:
    d=int(delay*SR); original=mix.copy();mix[d:]+=original[:-d,::-1]*level
fade=np.minimum(1,np.arange(N)/(.35*SR))*np.minimum(1,(N-np.arange(N))/(1.4*SR))
mix*=fade[:,None]
# Dry soft tactile clicks aligned with actual visible click feedback.
cues=[5.75,6.55,7.35,8.02,8.7,9.3,14.05,22.98]
for at in cues:
    t=np.arange(int(.07*SR))/SR
    click=(rng.normal(0,1,len(t))*.32+np.sin(2*np.pi*820*t)) * np.exp(-t/.007) * (1-np.exp(-t/.0007))
    add(fx,click,at,.11,.07)
for at,notes in [(16.65,[72,76]),(23.75,[65,72,76])]:
    for j,n in enumerate(notes):add(fx,note(n,.8),at+j*.075,.035,0)
# Quiet broad paper-like swish for order reflow, not a futuristic sound.
t=np.arange(int(.55*SR))/SR
noise=rng.normal(0,1,len(t));noise=np.convolve(noise,np.ones(20)/20,'same')
add(fx,noise*np.sin(np.pi*t/.55)**2,10.05,.045,-.1)
peak=float(np.max(np.abs(mix+fx)))
# Predictable safe gain; preserve headroom for AAC.
gain=min(2,.65/max(peak,1e-9));mix*=gain;fx*=gain
out=Path('videos/portion/assets')
def write(p,x):
    with wave.open(str(p),'wb') as f:f.setnchannels(2);f.setsampwidth(2);f.setframerate(SR);f.writeframes((x*32767).astype('<i2').tobytes())
write(out/'score.wav',mix);write(out/'ui-sfx.wav',fx)
(out/'audio-plan.json').write_text(json.dumps({'duration':DUR,'sample_rate':SR,'bpm':100,'seed':150916,'voice':'none','provenance':'Original deterministic synthesis for Portion','clicks':cues,'peak_sum_dbfs':20*np.log10(np.max(np.abs(mix+fx))),'rms_dbfs':20*np.log10(np.sqrt(np.mean((mix+fx)**2)))},indent=2))
print((out/'audio-plan.json').read_text())
