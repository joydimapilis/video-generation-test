"""Stage selected ORRIN plates and synthesize an original industrial score.

Plates are stripped of any embedded audio: the score is the only sound bed and a
model-generated room tone would fight it. The score is deterministic (seeded), so
re-running this produces a byte-identical WAV and the render stays reproducible.
"""
import argparse
import json
import shutil
import subprocess
import wave
from pathlib import Path

import numpy as np

SR = 48000
DURATION = 30
ROLES = ['weave', 'hero-macro', 'hero-reveal', 'hands', 'ridge', 'array']
FONTS = {'OrrinSans': '/System/Library/Fonts/Supplemental/Arial.ttf',
         'OrrinSans-Bold': '/System/Library/Fonts/Supplemental/Arial Bold.ttf',
         'OrrinMono': '/System/Library/Fonts/Supplemental/Andale Mono.ttf'}
SFX = ['impact-bass-1.mp3', 'impact-bass-2.mp3', 'riser.mp3', 'whoosh-cinematic.mp3', 'key-press.mp3']
SFX_DIR = Path('/Users/joydimapilis/.agents/skills/media-use/audio/assets/sfx')


def midi(note):
    return 440.0 * 2 ** ((note - 69) / 12)


def synth_score(path):
    """Cold, sparse, mechanical. One sub drone, one slow pulse, metal accents."""
    rng = np.random.default_rng(7)
    mix = np.zeros((SR * DURATION, 2))

    def add(at, sound, gain=1.0, pan=0.0):
        start = round(at * SR)
        size = min(len(sound), len(mix) - start)
        if size > 0:
            mix[start:start + size, 0] += sound[:size] * gain * (1 - pan * 0.45)
            mix[start:start + size, 1] += sound[:size] * gain * (1 + pan * 0.45)

    # Continuous sub drone: the room the whole film sits in.
    t = np.arange(len(mix)) / SR
    drone = (np.sin(2 * np.pi * midi(29) * t)
             + 0.5 * np.sin(2 * np.pi * midi(41) * t + 0.4)
             + 0.22 * np.sin(2 * np.pi * midi(48) * t * 1.002))
    # Slow breathing so a 30s hold never reads as a stuck tone.
    drone *= 0.55 + 0.45 * (0.5 + 0.5 * np.sin(2 * np.pi * t / 7.5))
    add(0, drone, 0.055)

    # Cold pad, one chord per act, tracking the film's six sections.
    for at, notes, length in [(0, [53, 60, 65], 4.4), (4, [53, 60, 67], 4.4),
                              (8, [51, 58, 63], 4.4), (12, [55, 62, 67], 4.4),
                              (16, [53, 60, 65], 6.4), (22, [56, 63, 68], 4.4),
                              (26, [53, 60, 65, 72], 4.5)]:
        span = np.arange(int(SR * length)) / SR
        env = np.minimum(span / 0.9, 1) * np.minimum((length - span) / 1.1, 1)
        env = np.clip(env, 0, 1)
        pad = sum(np.sin(2 * np.pi * midi(n) * span + i) for i, n in enumerate(notes))
        # A touch of detune keeps the pad from sounding like a test tone.
        pad += sum(0.4 * np.sin(2 * np.pi * midi(n) * 1.003 * span) for n in notes)
        add(at, pad * env, 0.019)

    # Machine pulse: a soft mechanical thud every bar, entering once the object does.
    beat = 60 / 84
    for index in range(int(DURATION / beat)):
        at = index * beat
        if at < 4 or at > 28.5:
            continue
        span = np.arange(int(SR * 0.28)) / SR
        thud = np.sin(2 * np.pi * (44 * span + 7 * (1 - np.exp(-span * 30)))) * np.exp(-span * 17)
        loud = 0.10 if index % 4 == 0 else 0.035
        add(at, thud, loud * (0.55 if at < 10 else 1.0))
        if index % 2 == 1 and at > 15:
            tick = rng.normal(0, 1, int(SR * 0.035))
            tick = np.diff(tick, prepend=0) * np.exp(-np.arange(len(tick)) / SR * 150)
            add(at + beat * 0.5, tick, 0.010, 0.6)

    # Metal accents on the section seams.
    for at, pan in [(4.0, -0.5), (8.0, 0.4), (12.0, 0.5), (16.0, -0.35), (22.0, 0.35), (26.0, 0.0)]:
        span = np.arange(int(SR * 1.5)) / SR
        # Inharmonic partials read as struck metal rather than a musical note.
        metal = sum(np.sin(2 * np.pi * f * span) * np.exp(-span * (2.0 + f / 900))
                    for f in (523.3, 784.9, 1174.7, 1661.2, 2217.5))
        add(at, metal * np.minimum(span / 0.002, 1), 0.012, pan)

    # Final swell into the close.
    span = np.arange(int(SR * 4)) / SR
    swell = np.sin(2 * np.pi * midi(41) * span) + 0.6 * np.sin(2 * np.pi * midi(53) * span)
    add(26, swell * np.minimum(span / 1.6, 1) * np.exp(-np.maximum(span - 2.2, 0) * 1.5), 0.05)

    gain = np.minimum(t / 0.8, 1) * np.minimum((DURATION - t) / 2.0, 1)
    mix = np.clip(mix * gain[:, None], -0.95, 0.95)
    with wave.open(str(path), 'wb') as out:
        out.setnchannels(2)
        out.setsampwidth(2)
        out.setframerate(SR)
        out.writeframes((mix * 32767).astype('<i2').tobytes())


def main():
    parser = argparse.ArgumentParser()
    for role in ROLES:
        parser.add_argument(f'--{role}', required=True, dest=role.replace('-', '_'),
                            help=f'Run id for the {role} plate')
    parser.add_argument('--source', type=Path, default=Path('artifacts/library-loop-2/outputs'))
    parser.add_argument('--project', type=Path, default=Path('hyperframes/orrin'))
    args = parser.parse_args()

    assets = args.project / 'assets'
    assets.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(Path('hyperframes/motion5/assets/gsap.min.js'), assets / 'gsap.min.js')
    for name, source in FONTS.items():
        shutil.copyfile(source, assets / f'{name}.ttf')

    selected = {}
    for role in ROLES:
        run_id = getattr(args, role.replace('-', '_'))
        source = args.source / f'{run_id}.mp4'
        if not source.exists():
            raise SystemExit(f'Missing plate for {role}: {source}')
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', str(source),
                        '-an', '-c:v', 'copy', str(assets / f'{role}.mp4')], check=True)
        selected[role] = run_id

    synth_score(assets / 'score.wav')
    for name in SFX:
        shutil.copyfile(SFX_DIR / name, assets / name)

    record = {'plates': selected, 'score': 'Original local synthesis, seed 7, 84 BPM',
              'sfx': 'Bundled media-use assets', 'source_library_media_reused': False,
              'plate_audio_stripped': True}
    Path('artifacts/library-loop-2/selected_assets.json').write_text(json.dumps(record, indent=2) + '\n')
    print('Staged', ', '.join(f'{k}={v}' for k, v in selected.items()))


if __name__ == '__main__':
    main()
