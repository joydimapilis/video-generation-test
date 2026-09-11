"""Stage CREW plates and synthesize the score. No TTS: this film's voice is the

dialogue plates' own generated performance, not synthesized narration. Dialogue
plates are staged WITH audio intact; b-roll plates are stripped. This film reuses
plates from TWO loops: library-loop-5 supplies the unchanged hero/linec dialogue
takes and all four b-roll plates, library-loop-6 supplies the four re-bought
lines whose words changed (line2, line4, line5, line6). Modeled directly on
scripts/prepare_rota_assets.py, minus the narration bed.

CrewSerif is converted to WOFF2 via fontTools, which requires the 'fonttools'
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
DURATION = 44.4
SERIF_SOURCE = '/System/Library/Fonts/Supplemental/BigCaslon.ttf'
FONTS = {
    'CrewSans': '/System/Library/Fonts/Supplemental/Arial.ttf',
    'CrewSans-Bold': '/System/Library/Fonts/Supplemental/Arial Bold.ttf',
}

LOOP5 = Path('artifacts/library-loop-5/outputs')
LOOP6 = Path('artifacts/library-loop-6/outputs')


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


# role -> (source dir, run id). KEEP AUDIO (dialogue): two takes reused
# unchanged from library-loop-5, four takes re-bought this loop because their
# words changed, from library-loop-6.
DIALOGUE_PLATES = {
    'hero': (LOOP5, 'talk_hero_v1'),
    'linec': (LOOP6, 'line3_pain_v2'),
    'line2': (LOOP6, 'line2_schedule_v1'),
    'line4': (LOOP6, 'line4_product_v1'),
    'line5': (LOOP6, 'line5_how_v1'),
    'line6': (LOOP6, 'line6_result_v1'),
}
# STRIP AUDIO (b-roll), all reused unchanged from library-loop-5.
BROLL_PLATES = {
    'dough': (LOOP5, 'broll_dough_v1'),
    'paper': (LOOP5, 'broll_rota_v1'),
    'room': (LOOP5, 'broll_room_v1'),
    'oven': (LOOP5, 'broll_oven_v1'),
}
REUSED_FROM_LOOP_5 = ['hero', 'dough', 'paper', 'room', 'oven']
RE_BOUGHT_THIS_LOOP = ['line2', 'line4', 'line5', 'line6']

# Dialogue audio tracks, from STORYBOARD.md's "Dialogue audio tracks" table.
# src is the staged asset filename (same mp4 the muted <video> uses).
DIALOGUE_TRACKS = [
    {'track': 'A1', 'role': 'hero', 'src': 'hero.mp4', 'data_start': 0.0, 'media_start': 0.0, 'duration': 7.3},
    {'track': 'A2', 'role': 'line2', 'src': 'line2.mp4', 'data_start': 9.3, 'media_start': 1.10, 'duration': 6.4},
    {'track': 'A3', 'role': 'linec', 'src': 'linec.mp4', 'data_start': 15.7, 'media_start': 0.0, 'duration': 5.6},
    {'track': 'A4', 'role': 'line4', 'src': 'line4.mp4', 'data_start': 23.0, 'media_start': 0.0, 'duration': 5.2},
    {'track': 'A5', 'role': 'line5', 'src': 'line5.mp4', 'data_start': 28.2, 'media_start': 0.0, 'duration': 4.2},
    {'track': 'A6', 'role': 'line6', 'src': 'line6.mp4', 'data_start': 32.4, 'media_start': 0.0, 'duration': 6.0},
]

# Captions table, from STORYBOARD.md's "Captions" table.
CAPTION_SCHEDULE = [
    {'in': 0.00, 'out': 3.90, 'text': "We're a bakery. Six people, two ovens,"},
    {'in': 4.02, 'out': 6.95, 'text': 'and a lot of very early mornings.'},
    {'in': 9.55, 'out': 15.55, 'text': "Every Sunday night I'd sit down with a pencil and rebuild the staff schedule."},
    {'in': 15.70, 'out': 21.00, 'text': "Someone's got an exam. Someone's kid is sick. Start again."},
    {'in': 23.00, 'out': 28.00, 'text': 'We use Crew now. Everyone puts their availability on their phone.'},
    {'in': 28.20, 'out': 32.10, 'text': 'It builds the schedule around that, and everyone sees it update.'},
    {'in': 32.40, 'out': 35.00, 'text': 'Now the whole schedule takes about nine minutes.'},
    {'in': 36.66, 'out': 38.20, 'text': 'I got my Sundays back.'},
]

# The three merged duck windows given literally in STORYBOARD.md.
MERGED_DUCK_WINDOWS = [(0.00, 7.25), (9.25, 21.30), (22.70, 38.50)]
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
    # Warm settle: hold at full under the b-roll resolve and the close card,
    # then fade to silence by the very end of the picture.
    points.append({'t': 42.4, 'v': 1.0})
    points.append({'t': DURATION, 'v': 0.0})
    assert all(points[i]['t'] < points[i + 1]['t'] for i in range(len(points) - 1)), points
    return {'version': 1, 'lanes': [{'target': 'volume', 'points': points}]}


def synth_score(path):
    """One quiet score, three movements per STORYBOARD.md's Audio section:
    sparse under the problem (0-23.0s), a small lift as the product arrives
    (23.0-38.4s), a warm settle from 38.4s under the b-roll resolve and the
    close card. Kept quiet and simple - the voice is the whole point of an
    interview. Idiom (sine pads, sub spine, soft plucks) reused verbatim in
    spirit from scripts/prepare_rota_assets.py; seeded for determinism.
    """
    rng = np.random.default_rng(444)
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
    spine *= 0.28 + 0.22 * np.clip((t - 23.0) / 6, 0, 1) + 0.14 * np.clip((t - 38.4) / 6, 0, 1)
    add(0, spine, 0.032)

    # MOVEMENT 1, 0-23.0s: sparse under the problem. One quiet pad per beat,
    # a soft pluck marking time, nothing busy.
    for at, notes, length in [(0.4, [53, 60], 4.6), (5.4, [52, 59], 4.6), (10.4, [50, 57], 4.6),
                              (15.4, [53, 60], 4.6), (19.8, [52, 59], 3.0)]:
        span = np.arange(int(SR * length)) / SR
        env = np.minimum(span / 1.4, 1) * np.minimum((length - span) / 1.8, 1)
        phase = rng.uniform(0, 0.3)
        pad = sum(np.sin(2 * np.pi * midi(n) * span + i * 0.6 + phase) for i, n in enumerate(notes))
        add(at, pad * np.clip(env, 0, 1), 0.014)
    beat = 60 / 72
    idx = 0
    while idx * beat + 1.0 < 23.0:
        at = 1.0 + idx * beat
        span = np.arange(int(SR * 0.4)) / SR
        pluck = np.sin(2 * np.pi * midi(72) * span) * np.exp(-span * 8) * np.minimum(span / .004, 1)
        add(at, pluck, 0.007 if idx % 2 == 0 else 0.004, (-1) ** idx * 0.3)
        idx += 1

    # MOVEMENT 2, 23.0-38.4s: a small lift as the product arrives.
    for at, notes, length in [(23.0, [55, 62, 65], 4.4), (27.6, [53, 60, 64], 4.4),
                              (32.4, [55, 62, 65], 4.4)]:
        span = np.arange(int(SR * length)) / SR
        env = np.minimum(span / 0.9, 1) * np.minimum((length - span) / 1.2, 1)
        pad = sum(np.sin(2 * np.pi * midi(n) * span + i * 0.5) for i, n in enumerate(notes))
        add(at, pad * np.clip(env, 0, 1), 0.019)
    step = 60 / 126 / 2
    idx = 0
    while 23.0 + idx * step < 38.4:
        at = 23.0 + idx * step
        span = np.arange(int(SR * 0.10)) / SR
        tick = np.sin(2 * np.pi * 1400 * span) * np.exp(-span * 70)
        add(at, tick, 0.009, (-1) ** idx * 0.35)
        idx += 1

    # MOVEMENT 3, 38.4-44.4s: a warm settle under the b-roll resolve and the
    # close card.
    for at, notes, length in [(38.4, [57, 64, 69], 3.6), (41.4, [53, 60, 65], 3.0)]:
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
    parser.add_argument('--project', type=Path, default=Path('hyperframes/crew'))
    parser.add_argument('--score-volume', type=float, default=SCORE_VOLUME,
                        help='Must match data-volume on the score track in index.html.')
    args = parser.parse_args()

    assets = args.project / 'assets'
    assets.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(Path('hyperframes/motion5/assets/gsap.min.js'), assets / 'gsap.min.js')
    for name, source in FONTS.items():
        shutil.copyfile(source, assets / f'{name}.ttf')
    convert_serif(SERIF_SOURCE, assets / 'CrewSerif.woff2')

    staged = {}
    for role, (source_dir, run_id) in DIALOGUE_PLATES.items():
        source = source_dir / f'{run_id}.mp4'
        if not source.exists():
            raise SystemExit(f'Missing plate for {role}: {source}')
        # Dialogue plates keep audio: this film has no synthesized narration,
        # the voice is the performance baked into the plate itself.
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', str(source),
                        '-c', 'copy', str(assets / f'{role}.mp4')], check=True)
        staged[role] = run_id

    for role, (source_dir, run_id) in BROLL_PLATES.items():
        source = source_dir / f'{run_id}.mp4'
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

    Path('artifacts/library-loop-6/selected_assets.json').write_text(json.dumps({
        'plates': {role: run_id for role, (_, run_id) in {**DIALOGUE_PLATES, **BROLL_PLATES}.items()},
        'reused_from_loop_5': REUSED_FROM_LOOP_5,
        're_bought_this_loop': RE_BOUGHT_THIS_LOOP,
        'note': ('Only the four lines whose words changed - line2, line4, line5, line6 - were '
                 're-bought this loop, from artifacts/library-loop-6/outputs. The hero and linec '
                 'dialogue takes say nothing that changed and are reused verbatim from '
                 'artifacts/library-loop-5/outputs, along with all four b-roll plates (dough, '
                 'paper, room, oven). Dialogue audio is the generated performance baked into each '
                 'talk_*/line*_v1 plate, not synthesized narration - this film has no TTS.'),
        'score': 'Original local synthesis, seed 444, three-movement structure',
        'plate_audio_stripped_broll': True,
        'plate_audio_kept_dialogue': True,
        'line3_regeneration_note': ('linec was re-generated as line3_pain_v2 '
                                     '(artifacts/library-loop-6/outputs) to remove an offensive '
                                     'hand gesture found in the original talk_c_v1 take; it is no '
                                     'longer reused from library-loop-5.'),
    }, indent=2) + '\n')

    print(f'Staged {len(staged)} plates; predicted mix peak {predicted:.3f}; '
          f'duck envelope has {len(envelope["lanes"][0]["points"])} points')


if __name__ == '__main__':
    main()
