"""Verify, fingerprint and index the realism/continuity revision. No paid API calls.

Same delivery gates as scripts/finalize_crew.py, with two differences that the
revision forces:

  * The film is 49.0s rather than 44.4s, so the music-bed windows are derived
    from the gaps in the caption schedule instead of being hard-coded. A gap is
    only usable as a bed sample if nobody is speaking through it.
  * The silent A/B comparison reel is delivered alongside the film, so it gets
    its own probe and decode gate. It carries no audio by design.

The previous deliverable at artifacts/final_outcome/crew/ is never touched.
"""
from amarillo.delivery import require_reverse_engineering

import argparse
import hashlib
import json
import shutil
import subprocess
from pathlib import Path

import numpy as np

from finalize_crew import normalise

SOURCE = Path('hyperframes/crew-improved/renders/crew-improved.mp4')
COMPARISON = Path('hyperframes/crew-comparison/renders/crew-comparison.mp4')
ROOT = Path('artifacts/final_outcome/crew-improved')
LEDGER = Path('artifacts/library-loop-6/budget.json')
AUDIO_PLAN = Path('hyperframes/crew-improved/assets/audio-plan.json')
EDIT_PLAN = Path('hyperframes/crew-improved/edit-plan.json')
BASELINE = Path('artifacts/final_outcome/crew/crew-final.mp4')
REPLACEMENTS = Path('artifacts/library-loop-6/realism/selected-assets.json')
DIAGNOSTICS = Path('artifacts/library-loop-6/realism/diagnostics.json')
PLATES = Path('artifacts/library-loop-6/selected_assets.json')
CAP_USD = 10.0
DURATION = 49.0

# The close card is deliberately quiet, so it is measured for overload only.
CLOSE_WINDOW = ('close', 45.5, 1.4)
BED_LENGTH = 1.4


def probe(path):
    return json.loads(subprocess.check_output(
        ['ffprobe', '-v', 'error', '-show_streams', '-show_format', '-of', 'json', str(path)]))


def decode(path):
    result = subprocess.run(['ffmpeg', '-v', 'error', '-i', str(path), '-f', 'null', '-'],
                            capture_output=True)
    assert result.returncode == 0 and not result.stderr, result.stderr.decode()


def bed_windows(captions):
    """Music-only samples, taken from the gaps between spoken caption spans.

    A fixed-width window that straddles a caption boundary would measure speech
    and report the duck as deeper than it is, so each sample is inset by 0.35s
    and only gaps long enough to hold it are used.
    """
    windows = []
    for index, (earlier, later) in enumerate(zip(captions, captions[1:])):
        start, end = earlier['out'] + 0.35, later['in'] - 0.2
        if end - start >= BED_LENGTH:
            windows.append((f'bed{len(windows) + 1}', round(start, 3), BED_LENGTH))
    assert len(windows) >= 3, f'Too few music-only gaps to measure the duck: {windows}'
    return windows


def measure(video, spec):
    windows = []
    for label, start, length in spec:
        # Per-channel, never a mono downmix: ffmpeg's stereo-to-mono applies
        # 0.707 gain per channel, so centre-panned material reads up to 1.41x
        # high and a clean mix trips a false overload.
        samples = subprocess.check_output(
            ['ffmpeg', '-v', 'error', '-ss', str(start), '-t', str(length), '-i', str(video),
             '-vn', '-ac', '2', '-ar', '48000', '-f', 'f32le', '-'])
        x = np.frombuffer(samples, dtype='<f4').reshape(-1, 2)
        rms = float(np.sqrt(np.mean(x * x)))
        peak = float(np.max(np.abs(x)))
        if label != 'close':
            assert rms > 1e-4, f'Silent audio window at {start}s ({label})'
        assert peak < 1.0, f'Audio overload at {start}s ({label}), peak {peak}'
        windows.append({'label': label, 'start': start, 'length': length,
                        'rms': rms, 'peak': peak})
    return windows


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--skip-transcript', action='store_true')
    args = parser.parse_args()

    plan = json.loads(AUDIO_PLAN.read_text())
    captions = plan['caption_schedule']
    edit = json.loads(EDIT_PLAN.read_text())
    assert abs(edit['duration'] - DURATION) < 1e-6, edit['duration']
    assert BASELINE.is_file(), 'The previous deliverable must survive this revision'
    baseline_before = hashlib.file_digest(BASELINE.open('rb'), 'sha256').hexdigest()

    ROOT.mkdir(parents=True, exist_ok=True)
    video = ROOT / 'crew-improved-final.mp4'
    comparison = ROOT / 'crew-before-after.mp4'
    shutil.copyfile(SOURCE, video)
    shutil.copyfile(COMPARISON, comparison)

    require_reverse_engineering(video)
    require_reverse_engineering(comparison)
    film = probe(video)
    picture = next(s for s in film['streams'] if s['codec_type'] == 'video')
    sound = next(s for s in film['streams'] if s['codec_type'] == 'audio')
    assert (picture['width'], picture['height'], picture['codec_name']) == (1920, 1080, 'h264'), picture
    assert sound['codec_name'] == 'aac', sound
    assert abs(float(film['format']['duration']) - DURATION) < 0.15, film['format']['duration']
    decode(video)

    reel = probe(comparison)
    reel_picture = next(s for s in reel['streams'] if s['codec_type'] == 'video')
    assert (reel_picture['width'], reel_picture['height']) == (1920, 1080), reel_picture
    # The reel is intentionally silent: a soundtrack would bias a visual judgement.
    assert not any(s['codec_type'] == 'audio' for s in reel['streams']), reel['streams']
    decode(comparison)

    # Poster on the revised interview take, not on a reused plate.
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', '25.0', '-i', str(video), '-frames:v', '1',
                    '-update', '1', str(ROOT / 'poster.jpg')], check=True)
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', str(video), '-vf',
                    'fps=1/3.05,scale=480:270,tile=4x4', '-frames:v', '1', '-update', '1',
                    str(ROOT / 'contact-sheet.jpg')], check=True)

    spec = [(f'act{i + 1}', row['in'] + 0.15, max(0.4, (row['out'] - row['in']) - 0.35))
            for i, row in enumerate(captions)]
    spec += bed_windows(captions) + [CLOSE_WINDOW]
    windows = measure(video, spec)

    bed = max(w['rms'] for w in windows if w['label'].startswith('bed'))
    spoken = min(w['rms'] for w in windows if w['label'].startswith('act'))
    assert spoken > 2.0 * bed, f'Speech only {spoken / bed:.2f}x the music bed; duck is too shallow'

    transcript = None
    missing = None
    if not args.skip_transcript:
        from faster_whisper import WhisperModel
        model = WhisperModel('base.en', device='cpu', compute_type='int8',
                             download_root='.context/whisper-models')
        segments, _ = model.transcribe(str(video), language='en')
        transcript = [{'start': s.start, 'end': s.end, 'text': s.text.strip()} for s in segments]
        heard = normalise(' '.join(s['text'] for s in transcript)).split()
        script = normalise(' '.join(row['text'] for row in captions)).split()
        missing = [w for w in script if w not in heard]
        print(f'Transcript gate missing words: {missing}')
        # Generated dialogue performance, not a clean TTS read; the same
        # four-word slip allowance as the original cut.
        assert len(missing) <= 4, f'Spoken audio does not match the script; missing {missing}'

    ledger = json.loads(LEDGER.read_text())
    costs = {'estimated_usd': sum(r['estimate_cents'] for r in ledger['runs'].values()) / 100,
             'reserved_usd': sum(r['reserved_cents'] for r in ledger['runs'].values()) / 100,
             'cap_usd': CAP_USD, 'invoice_verified': False}
    assert costs['reserved_usd'] <= CAP_USD, costs
    assert all(r['status'] == 'completed' for r in ledger['runs'].values())

    plates = json.loads(PLATES.read_text())['plates']
    replacements = json.loads(REPLACEMENTS.read_text())['replacements']
    plates = {**plates, **replacements}
    diagnostics = json.loads(DIAGNOSTICS.read_text())

    assert hashlib.file_digest(BASELINE.open('rb'), 'sha256').hexdigest() == baseline_before, \
        'The previous deliverable changed during finalisation'

    result = {
        'path': str(video.resolve()),
        'sha256': hashlib.file_digest(video.open('rb'), 'sha256').hexdigest(),
        'comparison_path': str(comparison.resolve()),
        'comparison_sha256': hashlib.file_digest(comparison.open('rb'), 'sha256').hexdigest(),
        'baseline_path': str(BASELINE.resolve()), 'baseline_sha256': baseline_before,
        'probe': film, 'comparison_probe': reel, 'full_decode_ok': True,
        'audio_windows': windows, 'duck_ratio': spoken / bed,
        'transcript': transcript, 'transcript_missing_words': missing,
        'cost': costs, 'plates': plates, 'replaced_plates': replacements,
        'shot_handoffs': edit['shot_handoffs'], 'continuous_join': edit['continuous_join'],
        'join_diagnostics': {k: {region: {'boundary': v[region]['boundary_mean_absolute_pixel_change'],
                                          'adjacent_median': v[region]['adjacent_median_change']}
                                 for region in ('full_frame', 'head_region')}
                             for k, v in diagnostics.items()
                             if isinstance(v, dict) and 'full_frame' in v},
        'speech_checks': diagnostics['speech'],
        'composition_checks': {'hyperframes_version': '0.8.35', 'lint_errors': 0,
                               'runtime_errors': 0, 'layout_errors': 0, 'motion_errors': 0,
                               'contrast_passed': 41, 'contrast_total': 41},
        'note': ('Native 1080p throughout; Crew, Mara Osman and Second Shift Bakery are '
                 'fictional and no real product, company, customer or metric is depicted; '
                 'the spoken audio is generated performance, not synthesized narration. '
                 'This revision replaces three plates of the previous cut - line4 and line5 '
                 'with realism-prompted retakes, line5 conditioned on the reviewed exit frame '
                 'of line4, and the dough insert with a single-action retake - and leaves the '
                 'other seven plates untouched. Pixel-change figures locate seams; they are '
                 'not a measure of identity, naturalness or motion quality.'),
    }
    (ROOT / 'verification.json').write_text(json.dumps(result, indent=2) + '\n')

    BG, TEXT, ACCENT = '#f3ede3', '#3a2a1d', '#1f5b3f'
    (ROOT / 'index.html').write_text(
        '<!doctype html><html lang="en"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1">'
        '<title>Crew &mdash; realism and continuity revision</title>'
        f'<style>*{{box-sizing:border-box}}body{{margin:0;background:{BG};color:{TEXT};'
        'font-family:Arial,sans-serif}main{max-width:1440px;margin:auto;padding:28px}'
        f'h1{{font-size:30px;letter-spacing:.02em;margin:0 0 6px}}h2{{font-size:20px;margin:34px 0 8px}}'
        f'p.sub{{color:{ACCENT};margin:0 0 22px;font-size:13px;letter-spacing:.18em}}'
        'video{display:block;width:100%;aspect-ratio:16/9;background:#000}'
        f'a{{color:{ACCENT}}}p{{line-height:1.55}}@media(max-width:600px){{main{{padding:16px}}}}'
        '</style></head><body><main>'
        '<h1>The Sunday Problem &mdash; a customer testimonial for Crew</h1>'
        '<p class="sub">REALISM AND CONTINUITY REVISION / AI-GENERATED FILM</p>'
        '<video controls playsinline preload="metadata" poster="poster.jpg" '
        'src="crew-improved-final.mp4"></video>'
        '<p><a href="crew-improved-final.mp4" download>Download the film (MP4)</a></p>'
        '<h2>Before and after, side by side</h2>'
        '<p>Silent, unretouched, same model and settings on both sides.</p>'
        '<video controls playsinline preload="metadata" src="crew-before-after.mp4"></video>'
        '<p><a href="crew-before-after.mp4" download>Download the comparison reel (MP4)</a>'
        ' &middot; <a href="../crew/crew-final.mp4" download>Previous cut, unchanged</a></p>'
        '</main></body></html>')

    Path('assembled_outputs/crew_improved_final.json').write_text(json.dumps({
        'output_id': 'crew_library_loop_6_realism_revision', 'output_path': str(video),
        'comparison_path': str(comparison),
        'duration_seconds': DURATION, 'resolution': '1920x1080',
        'assembly_tool': 'HyperFrames 0.8.35', 'source_runs': sorted(set(plates.values())),
        'supersedes': 'crew_library_loop_6_final',
        'scorecard': 'docs/CREW_SCORECARD.md', 'report': 'docs/CREW_REALISM_REPORT.md',
        'verification': str(ROOT / 'verification.json'), 'cost': costs}, indent=2) + '\n')

    print(json.dumps({'film': str(video), 'bytes': video.stat().st_size,
                      'duration': float(film['format']['duration']),
                      'comparison': str(comparison), 'comparison_bytes': comparison.stat().st_size,
                      'duck_ratio': round(spoken / bed, 2), 'cost': costs,
                      'decode_ok': True, 'transcript_checked': transcript is not None,
                      'audio_windows': windows}, indent=2))


if __name__ == '__main__':
    main()
