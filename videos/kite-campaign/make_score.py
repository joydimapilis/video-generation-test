"""Original deterministic score, no external samples or generation provider."""
from pathlib import Path
import json
import wave
import numpy as np

ROOT = Path(__file__).resolve().parent
SR = 48000
DURATION = 36
audio = np.zeros((SR * DURATION, 2), dtype=np.float64)
rng = np.random.default_rng(925)

def place(signal, start, gain=1.0, pan=0.0):
    offset = round(start * SR)
    n = min(len(signal), len(audio) - offset)
    if n > 0:
        audio[offset:offset+n, 0] += signal[:n] * gain * (1-pan*.3)
        audio[offset:offset+n, 1] += signal[:n] * gain * (1+pan*.3)

def pluck(midi, length=1.4):
    t = np.arange(round(length*SR))/SR
    f = 440 * 2**((midi-69)/12)
    return (np.sin(2*np.pi*f*t)+.24*np.sin(4*np.pi*f*t)+.08*np.sin(6*np.pi*f*t)) * (1-np.exp(-t*120)) * np.exp(-t*4)

beat = 60/120
chords = [[50,57,62,66],[47,54,59,62],[43,50,55,59],[45,52,57,61]]
for b in range(66):
    start = b*beat
    chord = chords[(b//8)%4]
    if b%2 == 0:
        t = np.arange(int(.28*SR))/SR
        kick = np.sin(2*np.pi*(48*t+32*.03*(1-np.exp(-t/.03))))*np.exp(-t*23)*(1-np.exp(-t*700))
        place(kick,start,.14)
    if b%4 == 0:
        place(pluck(chord[0]-12,2.0),start,.12)
    for half in range(2):
        midi=chord[(b+half)%4]+12
        place(pluck(midi),start+half*beat/2,.10,(-1)**b*.55)
    if b%2 == 1:
        t=np.arange(int(.08*SR))/SR
        noise=rng.normal(0,1,len(t)); noise=np.r_[0,np.diff(noise)]
        place(noise*np.exp(-t*70)*(1-np.exp(-t*1000)),start,.018)

# Final chord and restrained UI accents at meaningful actions.
for note in [50,57,62,66]: place(pluck(note+12,3),34,.09)
for start in [2.65,5.3,10.4,16.4,20.35,24.0,31.6]: place(pluck(86,.35),start,.035)
t=np.arange(len(audio))/SR
envelope=np.minimum(t/.12,1)*np.minimum(np.maximum((36-t)/1.8,0),1)
audio*=envelope[:,None]
peak=float(np.max(np.abs(audio)))
audio*=.64/max(peak,.00001)
out=ROOT/'assets/score.wav'
with wave.open(str(out),'wb') as f:
    f.setnchannels(2);f.setsampwidth(2);f.setframerate(SR)
    f.writeframes((np.clip(audio,-1,1)*32767).astype('<i2').tobytes())
(ROOT/'audio_meta.json').write_text(json.dumps({'bgm':{'path':'assets/score.wav','volume':1},'voices':[],'sfx':[],'bgm_pending':False,'provenance':'Original local deterministic composition: make_score.py; no samples, no API spend; 120 BPM; attack and final fade baked in'},indent=2))
(ROOT/'audio-review.json').write_text(json.dumps({'duration_seconds':36,'sample_rate':SR,'channels':2,'peak_dbfs':round(20*np.log10(np.max(np.abs(audio))),2),'rms_dbfs':round(20*np.log10(np.sqrt(np.mean(audio**2))),2),'clipped_samples':int(np.sum(np.abs(audio)>=1)),'first_five_seconds_rms_dbfs':round(20*np.log10(np.sqrt(np.mean(audio[:5*SR]**2))),2),'last_second_rms_dbfs':round(20*np.log10(np.sqrt(np.mean(audio[-SR:]**2))),2),'review_limit':'Numerical waveform and synthesis review, not independent perceptual listening. No narration or speech sync claims.','local_cost_usd':0},indent=2))
print(out)
