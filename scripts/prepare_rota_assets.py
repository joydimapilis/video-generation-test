"""Stage ROTA plates and synthesize the score. No TTS: this film's voice is the

dialogue plates' own generated performance, not synthesized narration. Dialogue
plates are staged WITH audio intact; b-roll plates are stripped. Modeled directly
on scripts/prepare_seventeen_assets.py, minus the narration bed.

RotaSerif is converted to WOFF2 via fontTools, which requires the 'fonttools'
and 'brotli' packages to be installed.
"""
import argparse
import json
import shutil
import subprocess
import wave
from pathlib import Path

import numpy as np

SR = 48000
DURATION = 36.6
SERIF_SOURCE = '/System/Library/Fonts/Supplemental/BigCaslon.ttf'
FONTS = {
    'RotaSans': '/System/Library/Fonts/Supplemental/Arial.ttf',
    'RotaSans-Bold': '/System/Library/Fonts/Supplemental/Arial Bold.ttf',
}


def convert_serif(source, target):
    """Chromium's OTS sanitizer rejects this legacy macOS TrueType face, so the
    renderer silently falls back to a default serif - off-design, and different
    on another machine. Converting to WOFF2 makes it embed and makes the render
    deterministic.

    The raw conversion alone still fails OTS: this font's format-12 cmap
    subtable is tagged (platform 0, encoding 1) - "Unicode 1.1", a legacy
    encoding ID that OTS does not recognize as valid for a format-12 table
    (only (3,10) and (0,4)/(0,6) are). Re-tagging it to encoding 4 ("Unicode
    2.0 full repertoire") describes the exact same character map in a
    spec-compliant way, so OTS accepts it.
    """
    from fontTools.ttLib import TTFont
    face = TTFont(source)
    for subtable in face['cmap'].tables:
        if subtable.format == 12 and subtable.platformID == 0 and subtable.platEncID == 1:
            subtable.platEncID = 4
    face.flavor = 'woff2'
    face.save(target)

# role -> run id. talk_d_v1 is deliberately NOT staged (see STORYBOARD.md).
DIALOGUE_PLATES = {'hero': 'talk_hero_v1', 'lineb': 'talk_b_v1', 'linec': 'talk_c_v1', 'lined': 'talk_d_v2'}
BROLL_PLATES = {'dough': 'broll_dough_v1', 'rota': 'broll_rota_v1', 'room': 'broll_room_v1', 'oven': 'broll_oven_v1'}
DROPPED_PLATES = {'talk_d_v1'}

# Dialogue audio tracks, from STORYBOARD.md's "Dialogue audio tracks" table.
# src is the staged asset filename (same mp4 the muted <video> uses).
DIALOGUE_TRACKS = [
    {'track': 'A1', 'role': 'hero', 'src': 'hero.mp4', 'data_start': 0.0, 'media_start': 0.0, 'duration': 7.4},
    {'track': 'A2', 'role': 'lineb', 'src': 'lineb.mp4', 'data_start': 9.6, 'media_start': 0.0, 'duration': 7.0},
    {'track': 'A3', 'role': 'linec', 'src': 'linec.mp4', 'data_start': 16.6, 'media_start': 0.0, 'duration': 5.8},
    {'track': 'A4', 'role': 'lined', 'src': 'lined.mp4', 'data_start': 24.6, 'media_start': 0.0, 'duration': 6.0},
]

# Captions table, from STORYBOARD.md's "Captions" table.
CAPTION_SCHEDULE = [
    {'in': 0.00, 'out': 3.90, 'text': "We're a bakery. Six people, two ovens,"},
    {'in': 4.02, 'out': 6.95, 'text': 'and a lot of very early mornings.'},
    {'in': 9.60, 'out': 15.98, 'text': "Every Sunday night, I'd sit down with a pencil and rebuild the whole week."},
    {'in': 16.60, 'out': 21.90, 'text': "Someone's got an exam. Someone's kid is sick. Start again."},
    {'in': 24.60, 'out': 26.55, 'text': 'Now it takes about nine minutes.'},
    {'in': 27.92, 'out': 29.80, 'text': 'I got my Sundays back.'},
]

# The three merged duck windows given literally in STORYBOARD.md.
MERGED_DUCK_WINDOWS = [(0.00, 7.25), (9.30, 22.20), (24.30, 30.10)]
DUCK_LEVEL = 0.42
DUCK_RAMP = 0.25
SCORE_VOLUME = 0.55


def midi(note):
    return 440.0 * 2 ** ((note - 69) / 12)


def write_wav(path, mix):
    with wave.open(str(path), 'wb') as out:
        out.setnchannels(2)
        out.setsampwidth(2)
        out.setframerate(SR)
        out.writeframes((np.clip(mix, -0.98, 0.98) * 32767).astype('<i2').tobytes())


def duck_envelope():
    """Automation points built from the three merged windows given literally in
    STORYBOARD.md. Points must stay strictly increasing in t, so a duck window
    that starts inside the opening 0->1.0 fade-in (window 1 starts at t=0.00)
    has its ramp-down clamped to begin at the end of that fade-in rather than
    at the window's own start - it cannot duck before the film has faded up.
    """
    points = [{'t': 0.0, 'v': 0.0}, {'t': 0.4, 'v': 1.0}]
    for start, end in MERGED_DUCK_WINDOWS:
        down_start = max(start, points[-1]['t'])
        if down_start > points[-1]['t']:
            points.append({'t': round(down_start, 2), 'v': 1.0})
        points.append({'t': round(down_start + DUCK_RAMP, 2), 'v': DUCK_LEVEL})
        points.append({'t': round(end - DUCK_RAMP, 2), 'v': DUCK_LEVEL})
        points.append({'t': round(end, 2), 'v': 1.0})
    # Warm settle: hold at full under the b-roll resolve, then fade to silence
    # by the very end of the picture, under the close card.
    points.append({'t': 34.6, 'v': 1.0})
    points.append({'t': DURATION, 'v': 0.0})
    assert all(points[i]['t'] < points[i + 1]['t'] for i in range(len(points) - 1)), points
    return {'version': 1, 'lanes': [{'target': 'volume', 'points': points}]}


def synth_score(path):
    """One quiet score, three movements: sparse under the problem (0-24.6s), a
    small lift as the answer arrives (24.6-30.6s), a warm settle under the
    close (30.6-36.6s). Kept quiet and simple - the voice is the whole point
    of an interview, and this is the first film where it is a generated
    performance rather than authored narration. Idiom (sine pads, sub spine,
    soft plucks) reused from scripts/prepare_seventeen_assets.py; seeded for
    determinism.
    """
    rng = np.random.default_rng(366)
    mix = np.zeros((int(SR * DURATION), 2))
    t = np.arange(len(mix)) / SR

    def add(at, sound, gain=1.0, pan=0.0):
        start = int(at * SR)
        size = min(len(sound), len(mix) - start)
        if size > 0:
            mix[start:start + size, 0] += sound[:size] * gain * (1 - pan * 0.45)
            mix[start:start + size, 1] += sound[:size] * gain * (1 + pan * 0.45)

    # Sub spine for the whole film, lifting slightly into movements 2 and 3.
    detune = 1.0 + rng.uniform(-0.0015, 0.0015)
    spine = np.sin(2 * np.pi * midi(29) * t) + 0.4 * np.sin(2 * np.pi * midi(41) * detune * t + 0.5)
    spine *= 0.28 + 0.22 * np.clip((t - 24.6) / 6, 0, 1) + 0.14 * np.clip((t - 30.6) / 6, 0, 1)
    add(0, spine, 0.032)

    # MOVEMENT 1, 0-24.6s: sparse under the problem. One quiet pad per beat,
    # a soft pluck marking time, nothing busy.
    for at, notes, length in [(0.4, [53, 60], 4.6), (5.4, [52, 59], 4.6), (10.4, [50, 57], 4.6),
                              (15.4, [53, 60], 4.6), (20.0, [52, 59], 4.4)]:
        span = np.arange(int(SR * length)) / SR
        env = np.minimum(span / 1.4, 1) * np.minimum((length - span) / 1.8, 1)
        phase = rng.uniform(0, 0.3)
        pad = sum(np.sin(2 * np.pi * midi(n) * span + i * 0.6 + phase) for i, n in enumerate(notes))
        add(at, pad * np.clip(env, 0, 1), 0.014)
    beat = 60 / 72
    idx = 0
    while idx * beat + 1.0 < 24.6:
        at = 1.0 + idx * beat
        span = np.arange(int(SR * 0.4)) / SR
        pluck = np.sin(2 * np.pi * midi(72) * span) * np.exp(-span * 8) * np.minimum(span / .004, 1)
        add(at, pluck, 0.007 if idx % 2 == 0 else 0.004, (-1) ** idx * 0.3)
        idx += 1

    # MOVEMENT 2, 24.6-30.6s: a small lift as the answer arrives.
    for at, notes, length in [(24.6, [55, 62, 65], 4.4)]:
        span = np.arange(int(SR * length)) / SR
        env = np.minimum(span / 0.9, 1) * np.minimum((length - span) / 1.2, 1)
        pad = sum(np.sin(2 * np.pi * midi(n) * span + i * 0.5) for i, n in enumerate(notes))
        add(at, pad * np.clip(env, 0, 1), 0.019)
    step = 60 / 126 / 2
    idx = 0
    while 24.6 + idx * step < 30.6:
        at = 24.6 + idx * step
        span = np.arange(int(SR * 0.10)) / SR
        tick = np.sin(2 * np.pi * 1400 * span) * np.exp(-span * 70)
        add(at, tick, 0.009, (-1) ** idx * 0.35)
        idx += 1

    # MOVEMENT 3, 30.6-36.6s: a warm settle under the close.
    for at, notes, length in [(30.6, [57, 64, 69], 3.6), (33.6, [53, 60, 65], 3.0)]:
        span = np.arange(int(SR * length)) / SR
        env = np.minimum(span / 1.2, 1) * np.minimum((length - span) / 1.6, 1)
        pad = sum(np.sin(2 * np.pi * midi(n) * span + i * 0.5) for i, n in enumerate(notes))
        pad += 0.24 * np.sin(2 * np.pi * midi(notes[-1] + 12) * span)
        add(at, pad * np.clip(env, 0, 1), 0.017)

    gain = np.minimum(t / 0.8, 1) * np.minimum((DURATION - t) / 3.0, 1)
    write_wav(path, mix * gain[:, None])


def decode_stereo(path, seconds, start=0.0):
    """Decode any audio file to stereo float at SR, from `start` for `seconds`."""
    raw = subprocess.check_output(
        ['ffmpeg', '-v', 'error', '-ss', f'{start}', '-i', str(path), '-t', f'{seconds}',
         '-vn', '-ac', '2', '-ar', str(SR), '-f', 'f32le', '-'])
    return np.frombuffer(raw, dtype='<f4').astype(np.float64).reshape(-1, 2)


def predict_mix_peak(assets, envelope, score_volume, dialogue_tracks):
    """Sum score.wav plus every staged dialogue plate's own audio, at its
    composition offset, and return the peak the render will produce.

    Per-channel, never a mono average: averaging L and R would under-report a
    hard-panned peak by half, which would let a clipping mix through to a
    render that the delivery gate then rejects.
    """
    span = int(SR * DURATION)
    summed = np.zeros((span, 2))

    score = decode_stereo(assets / 'score.wav', DURATION)[:span]
    points = envelope['lanes'][0]['points']
    gain = np.interp(np.arange(len(score)) / SR, [p['t'] for p in points], [p['v'] for p in points])
    score = score * score_volume * gain[:, None]
    summed[:len(score)] += score

    for row in dialogue_tracks:
        clip = decode_stereo(assets / row['src'], row['duration'], start=row['media_start'])
        start_i = int(row['data_start'] * SR)
        size = min(len(clip), span - start_i)
        if size > 0:
            summed[start_i:start_i + size] += clip[:size]

    return float(np.max(np.abs(summed)))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--source', type=Path, default=Path('artifacts/library-loop-5/outputs'))
    parser.add_argument('--project', type=Path, default=Path('hyperframes/rota'))
    parser.add_argument('--score-volume', type=float, default=SCORE_VOLUME,
                        help='Must match data-volume on the score track in index.html.')
    args = parser.parse_args()

    assets = args.project / 'assets'
    assets.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(Path('hyperframes/motion5/assets/gsap.min.js'), assets / 'gsap.min.js')
    for name, source in FONTS.items():
        shutil.copyfile(source, assets / f'{name}.ttf')
    convert_serif(SERIF_SOURCE, assets / 'RotaSerif.woff2')

    staged = {}
    for role, run_id in DIALOGUE_PLATES.items():
        source = args.source / f'{run_id}.mp4'
        if not source.exists():
            raise SystemExit(f'Missing plate for {role}: {source}')
        # Dialogue plates keep audio: this film has no synthesized narration,
        # the voice is the performance baked into the plate itself.
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', str(source),
                        '-c', 'copy', str(assets / f'{role}.mp4')], check=True)
        staged[role] = run_id

    for role, run_id in BROLL_PLATES.items():
        source = args.source / f'{run_id}.mp4'
        if not source.exists():
            raise SystemExit(f'Missing plate for {role}: {source}')
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', str(source),
                        '-an', '-c:v', 'copy', str(assets / f'{role}.mp4')], check=True)
        staged[role] = run_id

    synth_score(assets / 'score.wav')
    envelope = duck_envelope()

    (assets / 'audio-plan.json').write_text(json.dumps({
        'score_volume': args.score_volume,
        'music_automation': envelope,
        'dialogue_tracks': DIALOGUE_TRACKS,
        'caption_schedule': CAPTION_SCHEDULE,
    }, indent=2) + '\n')

    predicted = predict_mix_peak(assets, envelope, args.score_volume, DIALOGUE_TRACKS)
    if predicted >= 0.98:
        raise SystemExit(f'Predicted mix peak {predicted:.3f} would clip. '
                         'Lower the score volume or the duck level.')

    Path('artifacts/library-loop-5/selected_assets.json').write_text(json.dumps({
        'plates': staged,
        'dropped': sorted(DROPPED_PLATES),
        'note': ('Dialogue audio is the generated performance baked into each talk_* plate, '
                 'not synthesized narration - this film has no TTS. talk_d_v1 was bought but '
                 'is deliberately unused: the model restarted the clause, dropped the word '
                 '"back" and slurred "Sundays"; talk_d_v2 replaces it.'),
        'score': 'Original local synthesis, seed 366, three-movement structure',
        'plate_audio_stripped_broll': True,
        'plate_audio_kept_dialogue': True,
    }, indent=2) + '\n')

    print(f'Staged {len(staged)} plates; predicted mix peak {predicted:.3f}; '
          f'duck envelope has {len(envelope["lanes"][0]["points"])} points')


if __name__ == '__main__':
    main()
