"""Stage SEVENTEEN plates, assemble the narration bed, and synthesize the score.

The narration is the timing spine of this film: every cut, caption and music duck
is derived from VO_SCHEDULE below, so the schedule lives in one place and the
music-duck automation envelope for index.html is printed from it rather than
hand-written twice. Modeled directly on scripts/prepare_keel_assets.py.
"""
import argparse
import json
import os
import shutil
import subprocess
import sys
import wave
from pathlib import Path

import numpy as np

SR = 48000
DURATION = 42.0
FONTS = {'SeventeenSans': '/System/Library/Fonts/Supplemental/Arial.ttf',
         'SeventeenSans-Bold': '/System/Library/Fonts/Supplemental/Arial Bold.ttf'}
SFX_DIR = Path('/Users/joydimapilis/.agents/skills/media-use/audio/assets/sfx')
# (file, start second, slot length, volume). One source of truth: the composition
# builder reads these back out of audio-plan.json, and the mix predictor sums them
# at these exact offsets rather than assuming a worst case that never happens.
SFX_CUES = [
    ('key-press.mp3', 3.4, 0.4, 0.18),
    ('key-press.mp3', 24.0, 0.4, 0.14),
]
SFX = sorted({cue[0] for cue in SFX_CUES})

# role -> run id. street_walk_v1 is deliberately not staged (see STORYBOARD.md).
PLATES = {
    'hero': 'hero_night_v1', 'hands': 'hands_laptop_v1', 'lookup': 'char_lookup_v1',
    'rain': 'window_rain_v1', 'coffee': 'coffee_dawn_v1', 'desk': 'desk_empty_v1',
    'react': 'char_react_v1', 'exhale': 'char_exhale_v1', 'city': 'city_dawn_v1',
}
DROPPED_PLATES = {'street_walk_v1'}

# (clip file, start second, text) - durations are measured from the TTS run,
# never hardcoded, and filled in below.
VO_LINES = [
    ('l01.wav', 0.80, "Ada shipped her first app on a Tuesday."),
    ('l02.wav', 6.60, "Nobody came."),
    ('l03.wav', 11.50, "So she shipped another one. And another."),
    ('l04.wav', 20.00, "Sixteen times, nobody came."),
    ('l05.wav', 24.40, "On the seventeenth, someone did."),
    ('l06.wav', 31.80, "Then eleven more."),
    ('l07.wav', 35.40, "It isn't a rocket ship. It's a start."),
]
VOICE = 'bf_emma'
SPEED = 0.94
DUCK_PAD = 0.30
DUCK_LEVEL = 0.55


def midi(note):
    return 440.0 * 2 ** ((note - 69) / 12)


def read_wav(path):
    with wave.open(str(path), 'rb') as handle:
        frames = handle.readframes(handle.getnframes())
        data = np.frombuffer(frames, dtype='<i2').astype(np.float64) / 32768.0
        if handle.getnchannels() == 2:
            data = data.reshape(-1, 2).mean(axis=1)
        rate = handle.getframerate()
    if rate != SR:
        target = int(len(data) * SR / rate)
        data = np.interp(np.linspace(0, len(data), target, endpoint=False),
                         np.arange(len(data)), data)
    return data


def write_wav(path, mix):
    with wave.open(str(path), 'wb') as out:
        out.setnchannels(2)
        out.setsampwidth(2)
        out.setframerate(SR)
        out.writeframes((np.clip(mix, -0.98, 0.98) * 32767).astype('<i2').tobytes())


def generate_narration(vo_dir, hyperframes_python):
    """Generate each narration line with local Kokoro and measure its duration."""
    vo_dir.mkdir(parents=True, exist_ok=True)
    env = os.environ.copy()
    env['HYPERFRAMES_PYTHON'] = hyperframes_python
    schedule = []
    for name, start, text in VO_LINES:
        out_path = f'assets/vo/{name}'
        cmd = ['npx', 'hyperframes@0.8.34', 'tts', text, '-v', VOICE, '-s', str(SPEED),
               '-o', out_path, '--json']
        result = subprocess.run(cmd, env=env, capture_output=True, text=True)
        if result.returncode != 0:
            sys.stderr.write(result.stdout + '\n' + result.stderr + '\n')
            raise SystemExit(f'tts failed for {name}')
        payload = json.loads(result.stdout)
        duration = float(payload['durationSeconds'])
        schedule.append((name, start, duration, text))
    return schedule


def build_voice(vo_dir, out_path, schedule):
    """Place each measured line at its scheduled offset on one 42s bed."""
    mix = np.zeros((int(SR * DURATION), 2))
    for name, at, _length, _text in schedule:
        clip = read_wav(vo_dir / name)
        # Short fades kill the click the synth leaves at clip edges.
        edge = int(SR * 0.012)
        window = np.ones(len(clip))
        window[:edge] = np.linspace(0, 1, edge)
        window[-edge:] = np.linspace(1, 0, edge)
        clip = clip * window
        start = int(at * SR)
        size = min(len(clip), len(mix) - start)
        mix[start:start + size, 0] += clip[:size]
        mix[start:start + size, 1] += clip[:size]
    peak = float(np.max(np.abs(mix)))
    mix *= (0.72 / peak) if peak > 0 else 1.0
    write_wav(out_path, mix)
    return float(np.max(np.abs(mix)))


def duck_envelope(schedule):
    """Automation points for the music track, derived from the same schedule.

    Back-to-back lines share one duck. Emitting a window per line and then
    dropping out-of-order points would silently un-duck between two lines that
    are only fractions of a second apart, which is exactly where the mix clips
    - so overlapping windows are merged first and the envelope is built from
    the merged spans.
    """
    windows = sorted((at - DUCK_PAD, at + length + DUCK_PAD) for _, at, length, _ in schedule)
    merged = []
    for start, end in windows:
        if merged and start <= merged[-1][1] + 0.12:
            merged[-1][1] = max(merged[-1][1], end)
        else:
            merged.append([start, end])

    points = [{'t': 0.0, 'v': 0.0}, {'t': 1.2, 'v': 1.0}]
    for start, end in merged:
        ramp = min(0.25, (end - start) / 4)
        points += [
            {'t': round(start, 2), 'v': 1.0},
            {'t': round(start + ramp, 2), 'v': DUCK_LEVEL},
            {'t': round(end - ramp, 2), 'v': DUCK_LEVEL},
            {'t': round(end, 2), 'v': 1.0},
        ]
    points += [{'t': 38.0, 'v': 1.0}, {'t': DURATION, 'v': 0.0}]
    points = [p for p in points if 0.0 <= p['t'] <= DURATION]
    cleaned = []
    for point in points:
        if cleaned and point['t'] <= cleaned[-1]['t']:
            cleaned[-1] = point
            continue
        cleaned.append(point)
    assert all(cleaned[i]['t'] < cleaned[i + 1]['t'] for i in range(len(cleaned) - 1))
    return {'version': 1, 'lanes': [{'target': 'volume', 'points': cleaned}]}


def synth_score(path):
    """Three movements matching the acts: sparse/small, a little more motion, a
    warm resolve, fading out by the end. Kept quiet and simple - the film is
    carried by voice, not score."""
    rng = np.random.default_rng(17)
    mix = np.zeros((int(SR * DURATION), 2))
    t = np.arange(len(mix)) / SR

    def add(at, sound, gain=1.0, pan=0.0):
        start = int(at * SR)
        size = min(len(sound), len(mix) - start)
        if size > 0:
            mix[start:start + size, 0] += sound[:size] * gain * (1 - pan * 0.45)
            mix[start:start + size, 1] += sound[:size] * gain * (1 + pan * 0.45)

    # Sub spine for the whole film, lifting slightly into the warm resolve.
    spine = np.sin(2 * np.pi * midi(29) * t) + 0.4 * np.sin(2 * np.pi * midi(41) * t + 0.5)
    spine *= 0.35 + 0.35 * np.clip((t - 19.6) / 8, 0, 1) + 0.2 * np.clip((t - 24.0) / 10, 0, 1)
    add(0, spine, 0.045)

    # MOVEMENT 1, 0-19.6s: sparse and small. One quiet pad per beat, a soft
    # pluck marking the passage of each shipped app, nothing busy.
    for at, notes, length in [(0.4, [53, 60], 4.4), (5.0, [52, 59], 4.4),
                              (9.6, [50, 57], 4.4), (14.2, [53, 60], 5.2)]:
        span = np.arange(int(SR * length)) / SR
        env = np.minimum(span / 1.4, 1) * np.minimum((length - span) / 1.6, 1)
        pad = sum(np.sin(2 * np.pi * midi(n) * span + i * 0.6) for i, n in enumerate(notes))
        add(at, pad * np.clip(env, 0, 1), 0.018)
    beat = 60 / 76
    index = 0
    while index * beat + 1.0 < 19.6:
        at = 1.0 + index * beat
        span = np.arange(int(SR * 0.4)) / SR
        pluck = np.sin(2 * np.pi * midi(72) * span) * np.exp(-span * 8) * np.minimum(span / .004, 1)
        add(at, pluck, 0.010 if index % 2 == 0 else 0.006, (-1) ** index * 0.35)
        index += 1

    # MOVEMENT 2, 19.6-24.0s: a little more motion, the ship log rolling in.
    for at, notes, length in [(19.6, [55, 62, 65], 4.6)]:
        span = np.arange(int(SR * length)) / SR
        env = np.minimum(span / 0.8, 1) * np.minimum((length - span) / 1.0, 1)
        pad = sum(np.sin(2 * np.pi * midi(n) * span + i * 0.5) for i, n in enumerate(notes))
        add(at, pad * np.clip(env, 0, 1), 0.021)
    step = 60 / 132 / 2
    idx = 0
    while 19.6 + idx * step < 24.0:
        at = 19.6 + idx * step
        span = np.arange(int(SR * 0.10)) / SR
        tick = np.sin(2 * np.pi * 1480 * span) * np.exp(-span * 70)
        add(at, tick, 0.014, (-1) ** idx * 0.4)
        idx += 1

    # MOVEMENT 3, 24.0-42.0s: warm resolve, fading out by the end.
    for at, notes, length in [(24.4, [57, 64, 69], 5.4), (29.0, [55, 62, 67], 5.6),
                              (33.8, [53, 60, 65, 72], 5.4), (38.2, [53, 60, 65], 3.8)]:
        span = np.arange(int(SR * length)) / SR
        env = np.minimum(span / 1.2, 1) * np.minimum((length - span) / 1.6, 1)
        pad = sum(np.sin(2 * np.pi * midi(n) * span + i * 0.5) for i, n in enumerate(notes))
        pad += sum(0.35 * np.sin(2 * np.pi * midi(n) * 1.003 * span) for n in notes)
        pad += 0.22 * np.sin(2 * np.pi * midi(notes[-1] + 12) * span)
        add(at, pad * np.clip(env, 0, 1), 0.022)
    beat = 60 / 66
    idx = 0
    while 24.6 + idx * beat < 38.0:
        at = 24.6 + idx * beat
        span = np.arange(int(SR * 0.5)) / SR
        pluck = np.sin(2 * np.pi * midi(76) * span) * np.exp(-span * 6.5) * np.minimum(span / .004, 1)
        add(at, pluck, 0.012 if idx % 2 == 0 else 0.006, (-1) ** idx * 0.3)
        idx += 1

    gain = np.minimum(t / 0.8, 1) * np.minimum((DURATION - t) / 3.0, 1)
    write_wav(path, mix * gain[:, None])


def decode_stereo(path, seconds):
    """Decode any audio file to stereo float at SR, trimmed to a slot length."""
    raw = subprocess.check_output(
        ['ffmpeg', '-v', 'error', '-i', str(path), '-t', f'{seconds}',
         '-vn', '-ac', '2', '-ar', str(SR), '-f', 'f32le', '-'])
    return np.frombuffer(raw, dtype='<f4').astype(np.float64).reshape(-1, 2)


def predict_mix_peak(assets, envelope, score_volume):
    """Sum every finished track offline and return the peak the render will produce.

    Per-channel, never a mono average: averaging L and R would under-report a
    hard-panned peak by half, which would let a clipping mix through to a
    render that the delivery gate then rejects.
    """
    span = int(SR * DURATION)
    summed = np.zeros((span, 2))
    for name in ('voice.wav', 'score.wav'):
        track = decode_stereo(assets / name, DURATION)[:span]
        if name == 'score.wav':
            points = envelope['lanes'][0]['points']
            gain = np.interp(np.arange(len(track)) / SR,
                             [p['t'] for p in points], [p['v'] for p in points])
            track = track * score_volume * gain[:, None]
        summed[:len(track)] += track

    for name, at, length, volume in SFX_CUES:
        clip = decode_stereo(assets / name, length) * volume
        start = int(at * SR)
        size = min(len(clip), span - start)
        if size > 0:
            summed[start:start + size] += clip[:size]
    return float(np.max(np.abs(summed)))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--source', type=Path, default=Path('artifacts/library-loop-4/outputs'))
    parser.add_argument('--project', type=Path, default=Path('hyperframes/seventeen'))
    parser.add_argument('--drop', default='', help='Comma-separated roles to skip staging.')
    parser.add_argument('--score-volume', type=float, default=0.88,
                        help='Must match data-volume on the score track in index.html.')
    parser.add_argument('--hyperframes-python',
                        default=str(Path('.venv/bin/python').absolute()),
                        help='Absolute path to the Python interpreter the local Kokoro TTS uses.')
    args = parser.parse_args()

    assets = args.project / 'assets'
    assets.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(Path('hyperframes/motion5/assets/gsap.min.js'), assets / 'gsap.min.js')
    for name, source in FONTS.items():
        shutil.copyfile(source, assets / f'{name}.ttf')
    for name in SFX:
        shutil.copyfile(SFX_DIR / name, assets / name)

    dropped = {d for d in args.drop.split(',') if d}
    staged = {}
    for role, run_id in PLATES.items():
        if role in dropped:
            continue
        source = args.source / f'{run_id}.mp4'
        if not source.exists():
            raise SystemExit(f'Missing plate for {role}: {source}')
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', str(source),
                        '-an', '-c:v', 'copy', str(assets / f'{role}.mp4')], check=True)
        staged[role] = run_id

    # Run the TTS CLI from the project directory, matching the KEEL precedent.
    cwd = os.getcwd()
    os.chdir(args.project)
    try:
        schedule = generate_narration(Path('assets/vo'), args.hyperframes_python)
    finally:
        os.chdir(cwd)

    peak = build_voice(assets / 'vo', assets / 'voice.wav', schedule)
    synth_score(assets / 'score.wav')
    envelope = duck_envelope(schedule)
    (assets / 'audio-plan.json').write_text(json.dumps(
        {'score_volume': args.score_volume, 'music_automation': envelope,
         'sfx_cues': [{'src': n, 'at': a, 'duration': d, 'volume': v} for n, a, d, v in SFX_CUES],
         'vo_schedule': [{'file': n, 'start': a, 'duration': length, 'text': text}
                         for n, a, length, text in schedule]},
        indent=2) + '\n')

    predicted = predict_mix_peak(assets, envelope, args.score_volume)
    if predicted >= 0.98:
        raise SystemExit(f'Predicted mix peak {predicted:.3f} would clip. '
                         'Lower the voice normalisation, the score volume or the duck level.')

    Path('artifacts/library-loop-4/selected_assets.json').write_text(json.dumps({
        'plates': staged, 'dropped': sorted(DROPPED_PLATES),
        'narration': {'engine': f'Kokoro-82M local, voice {VOICE}, speed {SPEED}',
                      'lines': len(schedule),
                      'schedule': [[n, a, length] for n, a, length, _ in schedule],
                      'peak': peak},
        'score': 'Original local synthesis, seed 17, three-movement structure',
        'sfx': 'Bundled media-use assets', 'source_library_media_reused': False,
        'plate_audio_stripped': True}, indent=2) + '\n')

    print(f'Staged {len(staged)} plates; voice peak {peak:.2f}; '
          f'duck envelope has {len(envelope["lanes"][0]["points"])} points; '
          f'predicted mix peak {predicted:.3f}')
    for name, at, length, text in schedule:
        print(f'  {name}: start={at:.2f}s duration={length:.3f}s text={text!r}')
    print('data-automation=\'' + json.dumps(envelope) + '\'')


if __name__ == '__main__':
    main()
