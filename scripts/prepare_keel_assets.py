"""Stage KEEL plates, assemble the narration bed, and synthesize the score.

The narration is the timing spine of this film: every cut, caption and music duck
is derived from VO_SCHEDULE below, so the schedule lives in one place and the
music-duck automation envelope for index.html is printed from it rather than
hand-written twice.
"""
import argparse
import json
import shutil
import subprocess
import wave
from pathlib import Path

import numpy as np

SR = 48000
DURATION = 38.0
FONTS = {'KeelSerif': '/System/Library/Fonts/Supplemental/Georgia.ttf',
         'KeelSerif-Bold': '/System/Library/Fonts/Supplemental/Georgia Bold.ttf',
         'KeelSans': '/System/Library/Fonts/Supplemental/Arial.ttf',
         'KeelSans-Bold': '/System/Library/Fonts/Supplemental/Arial Bold.ttf'}
SFX_DIR = Path('/Users/joydimapilis/.agents/skills/media-use/audio/assets/sfx')
# (file, start second, slot length, volume). One source of truth: the composition
# builder reads these back out of audio-plan.json, and the mix predictor sums them
# at these exact offsets rather than assuming a worst case that never happens.
SFX_CUES = [
    ('whoosh-short.mp3', 1.60, 0.57, 0.16),
    ('whoosh-short.mp3', 4.10, 0.57, 0.16),
    ('impact-bass-1.mp3', 8.05, 2.11, 0.34),
    ('whoosh-cinematic.mp3', 19.30, 2.40, 0.13),
    ('riser.mp3', 30.60, 1.80, 0.10),
    ('impact-bass-1.mp3', 32.40, 2.11, 0.22),
]
SFX = sorted({cue[0] for cue in SFX_CUES})

# role -> run id. Two of the plates are cut into more than one piece in the edit.
PLATES = {
    'street': 'rush_street_v1', 'transit': 'rush_transit_v1', 'servers': 'rush_servers_v1',
    'typing': 'rush_hands_v2', 'surface': 'water_surface_v1', 'descend': 'water_descend_v1',
    'deep': 'water_deep_v1', 'shed': 'shop_wide_v1', 'plane': 'shop_hands_v1',
    'keel': 'shop_keel_v1',
}

# (clip file, start second, measured duration) - durations come from the TTS run.
VO_SCHEDULE = [
    ('l01.wav', 0.80, 1.813),
    ('l02.wav', 2.80, 2.837),
    ('l03.wav', 5.90, 1.685),
    ('l04.wav', 9.00, 3.200),
    ('l05.wav', 16.30, 2.880),
    ('l06.wav', 20.60, 2.133),
    ('l07.wav', 26.50, 1.536),
]
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


def build_voice(vo_dir, out_path):
    """Place each measured line at its scheduled offset on one 38s bed."""
    mix = np.zeros((int(SR * DURATION), 2))
    for name, at, _ in VO_SCHEDULE:
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


def duck_envelope():
    """Automation points for the music track, derived from the same schedule.

    Back-to-back lines share one duck. Emitting a window per line and then
    dropping out-of-order points would silently un-duck between two lines that
    are only 0.19s apart, which is exactly where the mix clips - so overlapping
    windows are merged first and the envelope is built from the merged spans.
    """
    windows = sorted((at - DUCK_PAD, at + length + DUCK_PAD) for _, at, length in VO_SCHEDULE)
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
    points += [{'t': 34.0, 'v': 1.0}, {'t': DURATION, 'v': 0.0}]
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
    """Three acts: cold pulse, a drop into depth, then a warm resolve."""
    rng = np.random.default_rng(19)
    mix = np.zeros((int(SR * DURATION), 2))
    t = np.arange(len(mix)) / SR

    def add(at, sound, gain=1.0, pan=0.0):
        start = int(at * SR)
        size = min(len(sound), len(mix) - start)
        if size > 0:
            mix[start:start + size, 0] += sound[:size] * gain * (1 - pan * 0.45)
            mix[start:start + size, 1] += sound[:size] * gain * (1 + pan * 0.45)

    # Sub spine for the whole film, lifting slightly as the argument resolves.
    spine = np.sin(2 * np.pi * midi(31) * t) + 0.45 * np.sin(2 * np.pi * midi(43) * t + 0.6)
    spine *= 0.5 + 0.5 * np.clip((t - 6) / 18, 0, 1)
    add(0, spine, 0.05)

    # ACT 1, 0-8.2s: cold sixteenth pulse, tightening.
    step = 60 / 132 / 4
    index = 0
    while index * step < 8.2:
        at = index * step
        span = np.arange(int(SR * 0.12)) / SR
        tick = np.sin(2 * np.pi * 1760 * span) * np.exp(-span * 60)
        noise = rng.normal(0, 1, len(span))
        tick = tick * 0.5 + np.diff(noise, prepend=0) * np.exp(-span * 90) * 0.5
        add(at, tick, 0.020 + 0.020 * (at / 8.2), (-1) ** index * 0.55)
        if index % 4 == 0:
            span = np.arange(int(SR * 0.24)) / SR
            kick = np.sin(2 * np.pi * (52 * span + 9 * (1 - np.exp(-span * 34)))) * np.exp(-span * 19)
            add(at, kick, 0.13)
        index += 1
    for at, notes in [(0.0, [57, 64]), (2.05, [59, 66]), (4.1, [60, 67]), (6.15, [62, 69])]:
        span = np.arange(int(SR * 2.3)) / SR
        env = np.minimum(span / 0.25, 1) * np.exp(-span * 0.9)
        pad = sum(np.sin(2 * np.pi * midi(n) * span) for n in notes)
        add(at, pad * env, 0.016)

    # THE TURN, 8.2s: everything stops, one low impact, then water.
    span = np.arange(int(SR * 3.2)) / SR
    drop = np.sin(2 * np.pi * (40 * span + 14 * (1 - np.exp(-span * 5)))) * np.exp(-span * 1.3)
    add(8.0, drop * np.minimum(span / 0.004, 1), 0.17)

    # ACT 2, 8.2-19.8s: suspended, almost nothing. Depth is the absence of pulse.
    for at, notes, length in [(8.4, [50, 57, 62], 6.0), (14.0, [48, 55, 60], 6.4)]:
        span = np.arange(int(SR * length)) / SR
        env = np.minimum(span / 1.8, 1) * np.minimum((length - span) / 1.8, 1)
        pad = sum(np.sin(2 * np.pi * midi(n) * span + i * 0.7) for i, n in enumerate(notes))
        pad += sum(0.35 * np.sin(2 * np.pi * midi(n) * 1.004 * span) for n in notes)
        add(at, pad * np.clip(env, 0, 1), 0.021)
    for at in [10.4, 13.1, 15.9, 18.2]:
        span = np.arange(int(SR * 2.4)) / SR
        drip = np.sin(2 * np.pi * midi(84) * span) * np.exp(-span * 3.4)
        add(at, drip, 0.011, rng.uniform(-0.6, 0.6))

    # ACT 3, 19.8-32.8s: warm, slow, a rising third that finally resolves.
    for at, notes, length in [(19.6, [53, 60, 65], 5.0), (24.4, [55, 62, 67], 4.6),
                              (28.8, [57, 64, 69], 4.6), (32.6, [53, 60, 65, 72], 5.4)]:
        span = np.arange(int(SR * length)) / SR
        env = np.minimum(span / 1.1, 1) * np.minimum((length - span) / 1.4, 1)
        pad = sum(np.sin(2 * np.pi * midi(n) * span + i * 0.5) for i, n in enumerate(notes))
        pad += sum(0.4 * np.sin(2 * np.pi * midi(n) * 1.003 * span) for n in notes)
        # A quiet octave doubling up top gives the warm act some air.
        pad += 0.25 * np.sin(2 * np.pi * midi(notes[-1] + 12) * span)
        add(at, pad * np.clip(env, 0, 1), 0.024)
    beat = 60 / 66
    for index in range(int((32.6 - 19.8) / beat)):
        at = 19.8 + index * beat
        span = np.arange(int(SR * 0.5)) / SR
        pluck = np.sin(2 * np.pi * midi(72) * span) * np.exp(-span * 7) * np.minimum(span / .004, 1)
        add(at, pluck, 0.014 if index % 2 == 0 else 0.007, (-1) ** index * 0.4)

    gain = np.minimum(t / 0.9, 1) * np.minimum((DURATION - t) / 2.6, 1)
    write_wav(path, mix * gain[:, None])


def decode_stereo(path, seconds):
    """Decode any audio file to stereo float at SR, trimmed to a slot length."""
    raw = subprocess.check_output(
        ['ffmpeg', '-v', 'error', '-i', str(path), '-t', f'{seconds}',
         '-vn', '-ac', '2', '-ar', str(SR), '-f', 'f32le', '-'])
    return np.frombuffer(raw, dtype='<f4').astype(np.float64).reshape(-1, 2)


def predict_mix_peak(assets, envelope, score_volume):
    """Sum every finished track offline and return the peak the render will produce.

    The first KEEL render clipped, and it took a two-and-a-half minute render plus
    the delivery gate to find out. This does the same arithmetic in a second, so a
    level mistake never reaches an encoder again.
    """
    # Per-channel, never a mono average: the first version of this check averaged
    # L and R and so under-reported a hard-panned peak by half, which let a
    # clipping mix through to a render that the delivery gate then rejected.
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
    parser.add_argument('--source', type=Path, default=Path('artifacts/library-loop-3/outputs'))
    parser.add_argument('--project', type=Path, default=Path('hyperframes/keel'))
    parser.add_argument('--drop', default='', help='Comma-separated roles to skip staging.')
    parser.add_argument('--score-volume', type=float, default=0.88,
                        help='Must match data-volume on the score track in index.html.')
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

    peak = build_voice(assets / 'vo', assets / 'voice.wav')
    synth_score(assets / 'score.wav')
    envelope = duck_envelope()
    (assets / 'audio-plan.json').write_text(json.dumps(
        {'score_volume': args.score_volume, 'music_automation': envelope,
         'sfx_cues': [{'src': n, 'at': a, 'duration': d, 'volume': v} for n, a, d, v in SFX_CUES]},
        indent=2) + '\n')

    # Loudest single SFX cue, as a worst-case allowance on top of voice + bed.
    predicted = predict_mix_peak(assets, envelope, args.score_volume)
    if predicted >= 0.98:
        raise SystemExit(f'Predicted mix peak {predicted:.3f} would clip. '
                         'Lower the voice normalisation, the score volume or the duck level.')

    Path('artifacts/library-loop-3/selected_assets.json').write_text(json.dumps({
        'plates': staged, 'dropped': sorted(dropped),
        'narration': {'engine': 'Kokoro-82M local, voice bm_george, speed 0.92',
                      'lines': len(VO_SCHEDULE), 'schedule': VO_SCHEDULE, 'peak': peak},
        'score': 'Original local synthesis, seed 19, three-act structure',
        'sfx': 'Bundled media-use assets', 'source_library_media_reused': False,
        'plate_audio_stripped': True}, indent=2) + '\n')
    print(f'Staged {len(staged)} plates; voice peak {peak:.2f}; '
          f'duck envelope has {len(envelope["lanes"][0]["points"])} points; '
          f'predicted mix peak {predicted:.3f}')
    print('data-automation=\'' + json.dumps(envelope) + '\'')


if __name__ == '__main__':
    main()
