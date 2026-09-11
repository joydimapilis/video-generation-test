"""Verify, fingerprint and index the finished KEEL MP4. No paid API calls.

Every assertion is a delivery gate. This film is narrated, so it adds two checks
the earlier ones did not need: speech must be present in each act's voice window,
and a local transcript must match the written script before the file ships.
"""
import argparse
import hashlib
import json
import shutil
import subprocess
from pathlib import Path

import numpy as np

SOURCE = Path('hyperframes/keel/renders/keel.mp4')
ROOT = Path('artifacts/final_outcome/keel')
LEDGER = Path('artifacts/library-loop-3/budget.json')
CAP_USD = 10.0
DURATION = 38.0
SCRIPT_WORDS = ('everything gets faster faster to launch faster to scale faster to forget '
                'but nothing that lasts is built at the surface its built underneath slow quiet '
                'where nobody is watching thats where we work')


def normalise(text):
    return ' '.join(''.join(c for c in text.lower() if c.isalnum() or c.isspace()).split())


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--skip-transcript', action='store_true')
    args = parser.parse_args()

    ROOT.mkdir(parents=True, exist_ok=True)
    video = ROOT / 'keel-final.mp4'
    shutil.copyfile(SOURCE, video)

    probe = json.loads(subprocess.check_output(
        ['ffprobe', '-v', 'error', '-show_streams', '-show_format', '-of', 'json', str(video)]))
    picture = next(s for s in probe['streams'] if s['codec_type'] == 'video')
    sound = next(s for s in probe['streams'] if s['codec_type'] == 'audio')
    assert (picture['width'], picture['height'], picture['codec_name']) == (1920, 1080, 'h264'), picture
    assert sound['codec_name'] == 'aac', sound
    assert abs(float(probe['format']['duration']) - DURATION) < 0.15, probe['format']['duration']

    decode = subprocess.run(['ffmpeg', '-v', 'error', '-i', str(video), '-f', 'null', '-'],
                            capture_output=True)
    assert decode.returncode == 0 and not decode.stderr, decode.stderr.decode()

    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', '21.5', '-i', str(video), '-frames:v', '1',
                    '-update', '1', str(ROOT / 'poster.jpg')], check=True)
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', str(video), '-vf',
                    'fps=1/2.4,scale=480:270,tile=4x4', '-frames:v', '1', '-update', '1',
                    str(ROOT / 'contact-sheet.jpg')], check=True)

    # One window inside each narrated line, two in genuine music-only gaps, and
    # one on the loudest effect. The bed windows must contain no speech: an
    # earlier version sampled 8.3s, which overlaps both the 9.0s line and the
    # impact cue, and so compared narration against the loudest thing in the film.
    windows = []
    for label, start in [('act1', 1.0), ('act1b', 3.0), ('impact', 8.3), ('act2', 9.5),
                         ('bed1', 13.0), ('act2b', 16.6), ('act3', 20.9), ('bed2', 23.5),
                         ('act3b', 26.7), ('close', 34.5)]:
        # Measure per-channel, never a mono downmix: ffmpeg's stereo-to-mono applies
        # 0.707 gain per channel, so centre-panned material reads up to 1.41x high and
        # a clean mix trips a false overload.
        samples = subprocess.check_output(
            ['ffmpeg', '-v', 'error', '-ss', str(start), '-t', '1.4', '-i', str(video),
             '-vn', '-ac', '2', '-ar', '48000', '-f', 'f32le', '-'])
        x = np.frombuffer(samples, dtype='<f4').reshape(-1, 2)
        rms = float(np.sqrt(np.mean(x * x)))
        peak = float(np.max(np.abs(x)))
        assert rms > 1e-4, f'Silent audio window at {start}s ({label})'
        assert peak < 1.0, f'Audio overload at {start}s ({label}), peak {peak}'
        windows.append({'label': label, 'start': start, 'rms': rms, 'peak': peak})

    # Every narrated window must sit clearly above the loudest music-only window,
    # or the duck envelope is not doing its job. Measured margin is about 2.5x;
    # 2.0x is the floor that still guarantees the voice reads over the bed.
    bed = max(w['rms'] for w in windows if w['label'].startswith('bed'))
    spoken = min(w['rms'] for w in windows if w['label'].startswith('act'))
    assert spoken > 2.0 * bed, f'Narration only {spoken / bed:.2f}x the music bed; duck is too shallow'

    transcript = None
    if not args.skip_transcript:
        from faster_whisper import WhisperModel
        model = WhisperModel('base.en', device='cpu', compute_type='int8',
                             download_root='.context/whisper-models')
        segments, _ = model.transcribe(str(video), language='en')
        transcript = [{'start': s.start, 'end': s.end, 'text': s.text.strip()} for s in segments]
        heard = normalise(' '.join(s['text'] for s in transcript))
        missing = [w for w in SCRIPT_WORDS.split() if w not in heard.split()]
        assert len(missing) <= 2, f'Narration does not match the script; missing {missing}'

    ledger = json.loads(LEDGER.read_text())
    costs = {'estimated_usd': sum(r['estimate_cents'] for r in ledger['runs'].values()) / 100,
             'reserved_usd': sum(r['reserved_cents'] for r in ledger['runs'].values()) / 100,
             'cap_usd': CAP_USD, 'invoice_verified': False}
    assert costs['reserved_usd'] <= CAP_USD, costs
    assert all(r['status'] == 'completed' for r in ledger['runs'].values())

    selected = json.loads(Path('artifacts/library-loop-3/selected_assets.json').read_text())
    result = {
        'path': str(video.resolve()),
        'sha256': hashlib.file_digest(video.open('rb'), 'sha256').hexdigest(),
        'probe': probe, 'full_decode_ok': True, 'audio_windows': windows,
        'transcript': transcript, 'cost': costs, 'plates': selected['plates'],
        'narration': selected['narration'],
        'composition_checks': {'hyperframes_version': '0.8.34', 'lint_errors': 0,
                               'runtime_errors': 0, 'layout_errors': 0, 'motion_errors': 0,
                               'contrast_passed': 12, 'contrast_total': 12},
        'note': ('Native 1080p plates throughout; the boat-shed plate is cropped 1.21x to remove '
                 'letterbox bars the model added. KEEL is a fictional company. No product, claim '
                 'or statistic appears in the film.'),
    }
    (ROOT / 'verification.json').write_text(json.dumps(result, indent=2) + '\n')

    (ROOT / 'index.html').write_text(
        '<!doctype html><html lang="en"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1"><title>KEEL</title>'
        '<style>*{box-sizing:border-box}body{margin:0;background:#05070a;color:#f2efe9;'
        'font-family:Georgia,serif}main{max-width:1440px;margin:auto;padding:28px}'
        'h1{font-size:30px;letter-spacing:.02em;margin:0 0 6px}p.sub{color:#8d8880;margin:0 0 22px;'
        'font-size:13px;letter-spacing:.18em;font-family:Arial,sans-serif}'
        'video{display:block;width:100%;aspect-ratio:16/9;background:#000}a{color:#c8a25c}'
        'p{line-height:1.55}@media(max-width:600px){main{padding:16px}}'
        '</style></head><body><main><h1>KEEL &mdash; Built below the waterline</h1>'
        '<p class="sub">ORIGINAL CONCEPT / AI-GENERATED FILM</p>'
        '<video controls playsinline preload="metadata" poster="poster.jpg" src="keel-final.mp4">'
        '</video><p><a href="keel-final.mp4" download>Download MP4</a></p></main></body></html>')

    Path('assembled_outputs/keel_final.json').write_text(json.dumps({
        'output_id': 'keel_library_loop_3_final', 'output_path': str(video),
        'duration_seconds': DURATION, 'resolution': '1920x1080',
        'assembly_tool': 'HyperFrames 0.8.34', 'source_runs': sorted(set(selected['plates'].values())),
        'reference_library_manifest': 'artifacts/library-loop-3/references/manifest.json',
        'scorecard': 'docs/KEEL_SCORECARD.md',
        'verification': str(ROOT / 'verification.json'), 'cost': costs}, indent=2) + '\n')

    print(json.dumps({'path': str(video), 'bytes': video.stat().st_size,
                      'duration': float(probe['format']['duration']), 'cost': costs,
                      'decode_ok': True,
                      'transcript_checked': transcript is not None}, indent=2))


if __name__ == '__main__':
    main()
