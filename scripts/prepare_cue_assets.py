"""Stage generated clips and an original deterministic electronic score."""
import argparse
import json
import shutil
import subprocess
import wave
from pathlib import Path
import numpy as np

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--hook', default='ugc_veo_v1')
    parser.add_argument('--hero', default='hero_kling_v1')
    args = parser.parse_args()
    assets = Path('hyperframes/cue/assets')
    assets.mkdir(exist_ok=True)
    for name in ['Arial.ttf', 'Arial-Bold.ttf', 'gsap.min.js']:
        shutil.copyfile(Path('hyperframes/motion5/assets') / name, assets / name)
    for role, selected in [('hook', args.hook), ('hero', args.hero)]:
        source=Path('artifacts/library-loop/outputs') / f'{selected}.mp4'
        # Physically remove embedded audio to prevent duplicate dialogue in the mix.
        subprocess.run(['ffmpeg','-v','error','-y','-i',str(source),'-an','-c:v','copy',str(assets/f'{role}.mp4')],check=True)
    voice_source=Path('artifacts/library-loop/outputs') / f'{args.hook}.mp4'
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', str(voice_source), '-vn', '-af',
        'afade=t=out:st=5.8:d=0.2,loudnorm=I=-16:TP=-1.5:LRA=7', '-c:a', 'aac', '-b:a', '192k', str(assets / 'voice.m4a')], check=True)
    sr = 48000
    mix = np.zeros((sr * 30, 2))
    rng = np.random.default_rng(42)
    def add(at, sound, gain=1, pan=0):
        start = round(at * sr)
        size = min(len(sound), len(mix) - start)
        if size > 0:
            mix[start:start+size,0] += sound[:size]*gain*(1-pan*.4)
            mix[start:start+size,1] += sound[:size]*gain*(1+pan*.4)
    beat = 60 / 112
    chords = [[50,57,62,66], [47,54,59,62], [43,50,55,59], [45,52,57,61]]
    for bar in range(14):
        notes = chords[bar % 4]
        start = bar * beat * 4
        t = np.arange(round(beat*4.5*sr))/sr
        env = np.minimum(t/.18,1)*np.exp(-t/1.8)
        pad = sum(np.sin(2*np.pi*(440*2**((n-69)/12))*t) for n in notes)*env
        add(start,pad,.016)
        for step,note in enumerate([notes[0]+12,notes[2]+12,notes[1]+24,notes[3]+12]):
            t = np.arange(int(sr*.65))/sr
            f = 440*2**((note-69)/12)
            pluck = (np.sin(2*np.pi*f*t)+.22*np.sin(2*np.pi*2*f*t))*np.exp(-t*9)*np.minimum(t/.005,1)
            add(start+step*beat,pluck,.09,(-1)**step*.5)
            add(start+step*beat+beat*.75,pluck,.027,(-1)**(step+1)*.5)
        if start >= 6:
            for b in range(4):
                t=np.arange(int(sr*.19))/sr
                kick=np.sin(2*np.pi*(48*t+4*(1-np.exp(-t*24))))*np.exp(-t*22)
                add(start+b*beat,kick,.11 if b%2==0 else .05)
                hat=rng.normal(0,1,int(sr*.055))
                hat=np.diff(hat,prepend=0)*np.exp(-np.arange(len(hat))/sr*110)
                add(start+(b+.5)*beat,hat,.006,.5)
    t=np.arange(len(mix))/sr
    gain=np.minimum(t,1)*np.minimum((30-t)/1.8,1)*np.where(t<5.8,.28,1)
    mix=np.clip(mix*gain[:,None],-.95,.95)
    with wave.open(str(assets/'score.wav'),'wb') as out:
        out.setnchannels(2);out.setsampwidth(2);out.setframerate(sr)
        out.writeframes((mix*32767).astype('<i2').tobytes())
    for name in ['click-soft.mp3','whoosh-short.mp3','chime.mp3']:
        shutil.copyfile(Path('/Users/joydimapilis/.agents/skills/media-use/audio/assets/sfx')/name,assets/name)
    Path('artifacts/library-loop/selected_assets.json').write_text(json.dumps({
        'hook':args.hook,'hero':args.hero,'score':'Original local synthesis, seed42, 112BPM',
        'sfx':'Bundled media-use assets','source_library_media_reused':False},indent=2)+'\n')

if __name__=='__main__':
    main()
