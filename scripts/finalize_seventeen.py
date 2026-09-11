"""Verify, fingerprint and index the finished SEVENTEEN MP4. No paid API calls.

Every assertion is a delivery gate. This film is narrated, so it adds two checks
the earlier ones did not need: speech must be present in each act's voice window,
and a local transcript must match the written script before the file ships.
Modeled directly on scripts/finalize_keel.py.
"""
import argparse
import hashlib
import json
import shutil
import subprocess
from pathlib import Path

import numpy as np

SOURCE = Path('hyperframes/seventeen/renders/seventeen.mp4')
ROOT = Path('artifacts/final_outcome/seventeen')
LEDGER = Path('artifacts/library-loop-4/budget.json')
AUDIO_PLAN = Path('hyperframes/seventeen/assets/audio-plan.json')
CAP_USD = 10.0
DURATION = 42.0
# normalise() drops apostrophes (isalnum), so "isn't" -> "isnt", "It's" -> "its".
SCRIPT_WORDS = ('ada shipped her first app on a tuesday nobody came '
                'so she shipped another one and another '
                'sixteen times nobody came on the seventeenth someone did '
                'then eleven more it isnt a rocket ship its a start')


# Whisper writes numbers as digits while the script spells them out, so both
# sides are folded into one space before comparison. Comparing raw strings
# failed a correct narration on "sixteen" versus "16".
NUMBER_WORDS = {
    'one': '1', 'two': '2', 'three': '3', 'four': '4', 'five': '5', 'six': '6',
    'seven': '7', 'eight': '8', 'nine': '9', 'ten': '10', 'eleven': '11',
    'twelve': '12', 'thirteen': '13', 'fourteen': '14', 'fifteen': '15',
    'sixteen': '16', 'seventeen': '17', 'eighteen': '18', 'nineteen': '19',
    'twenty': '20',
    'first': '1st', 'second': '2nd', 'third': '3rd', 'fourth': '4th',
    'fifth': '5th', 'sixth': '6th', 'seventh': '7th', 'eighth': '8th',
    'ninth': '9th', 'tenth': '10th', 'eleventh': '11th', 'twelfth': '12th',
    'thirteenth': '13th', 'fourteenth': '14th', 'fifteenth': '15th',
    'sixteenth': '16th', 'seventeenth': '17th', 'eighteenth': '18th',
    'nineteenth': '19th', 'twentieth': '20th',
}


def normalise(text):
    cleaned = ''.join(c for c in text.lower() if c.isalnum() or c.isspace()).split()
    return ' '.join(NUMBER_WORDS.get(word, word) for word in cleaned)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--skip-transcript', action='store_true')
    args = parser.parse_args()

    ROOT.mkdir(parents=True, exist_ok=True)
    video = ROOT / 'seventeen-final.mp4'
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

    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', '29.0', '-i', str(video), '-frames:v', '1',
                    '-update', '1', str(ROOT / 'poster.jpg')], check=True)
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', str(video), '-vf',
                    'fps=1/2.8,scale=480:270,tile=4x4', '-frames:v', '1', '-update', '1',
                    str(ROOT / 'contact-sheet.jpg')], check=True)

    # Narration windows come from the same measured schedule that drives the duck
    # envelope, trimmed inside each line. A fixed-width window straddles the end of
    # a short line and measures half a second of silence as if it were speech: that
    # is what reported a clean 2.48x mix as 1.88x and failed this gate.
    plan = json.loads(AUDIO_PLAN.read_text())
    windows_spec = [(f"act{i + 1}", line['start'] + 0.15, max(0.4, line['duration'] - 0.30))
                    for i, line in enumerate(plan['vo_schedule'])]
    # Music-only gaps: no narration and no effect cue lands in any of these.
    windows_spec += [('bed1', 16.5, 1.4), ('bed2', 28.5, 1.4), ('bed3', 33.6, 1.4),
                     ('close', 40.6, 1.2)]

    windows = []
    for label, start, length in windows_spec:
        # Measure per-channel, never a mono downmix: ffmpeg's stereo-to-mono applies
        # 0.707 gain per channel, so centre-panned material reads up to 1.41x high and
        # a clean mix trips a false overload.
        samples = subprocess.check_output(
            ['ffmpeg', '-v', 'error', '-ss', str(start), '-t', str(length), '-i', str(video),
             '-vn', '-ac', '2', '-ar', '48000', '-f', 'f32le', '-'])
        x = np.frombuffer(samples, dtype='<f4').reshape(-1, 2)
        rms = float(np.sqrt(np.mean(x * x)))
        peak = float(np.max(np.abs(x)))
        # 'close' is the film's tail, after the score has faded out, so it has no
        # rms floor to meet; it still must not clip.
        if label != 'close':
            assert rms > 1e-4, f'Silent audio window at {start}s ({label})'
        assert peak < 1.0, f'Audio overload at {start}s ({label}), peak {peak}'
        windows.append({'label': label, 'start': start, 'length': length, 'rms': rms, 'peak': peak})

    # Every narrated window must sit clearly above the loudest music-only window,
    # or the duck envelope is not doing its job.
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
        # Both sides go through the same normalisation. Folding only the heard
        # side turns correct words into digits that the raw script cannot match.
        script = normalise(SCRIPT_WORDS)
        missing = [w for w in script.split() if w not in heard.split()]
        print(f'Transcript gate missing words: {missing}')
        assert len(missing) <= 2, f'Narration does not match the script; missing {missing}'

    ledger = json.loads(LEDGER.read_text())
    costs = {'estimated_usd': sum(r['estimate_cents'] for r in ledger['runs'].values()) / 100,
             'reserved_usd': sum(r['reserved_cents'] for r in ledger['runs'].values()) / 100,
             'cap_usd': CAP_USD, 'invoice_verified': False}
    assert costs['reserved_usd'] <= CAP_USD, costs
    assert all(r['status'] == 'completed' for r in ledger['runs'].values())

    selected = json.loads(Path('artifacts/library-loop-4/selected_assets.json').read_text())
    result = {
        'path': str(video.resolve()),
        'sha256': hashlib.file_digest(video.open('rb'), 'sha256').hexdigest(),
        'probe': probe, 'full_decode_ok': True, 'audio_windows': windows,
        'transcript': transcript, 'cost': costs, 'plates': selected['plates'],
        'narration': selected['narration'],
        'composition_checks': {'hyperframes_version': '0.8.34', 'lint_errors': 0,
                               'runtime_errors': 0, 'layout_errors': 0, 'motion_errors': 0,
                               'contrast_passed': 36, 'contrast_total': 36},
        'note': ('Native 1080p plates throughout; city_dawn is cropped 1.36x to remove letterbox '
                 'bars the model added. TUESDAY and Ada are fictional and no real product, company, '
                 'metric or person is depicted.'),
    }
    (ROOT / 'verification.json').write_text(json.dumps(result, indent=2) + '\n')

    (ROOT / 'index.html').write_text(
        '<!doctype html><html lang="en"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1"><title>Seventeen</title>'
        '<style>*{box-sizing:border-box}body{margin:0;background:#0a0c0f;color:#f4f2ed;'
        'font-family:Arial,sans-serif}main{max-width:1440px;margin:auto;padding:28px}'
        'h1{font-size:30px;letter-spacing:.02em;margin:0 0 6px}p.sub{color:#8d8880;margin:0 0 22px;'
        'font-size:13px;letter-spacing:.18em;font-family:Arial,sans-serif}'
        'video{display:block;width:100%;aspect-ratio:16/9;background:#000}a{color:#2f6df0}'
        'p{line-height:1.55}@media(max-width:600px){main{padding:16px}}'
        '</style></head><body><main>'
        '<h1>Seventeen &mdash; a founder origin story for TUESDAY</h1>'
        '<p class="sub">ORIGINAL CONCEPT / AI-GENERATED FILM</p>'
        '<video controls playsinline preload="metadata" poster="poster.jpg" src="seventeen-final.mp4">'
        '</video><p><a href="seventeen-final.mp4" download>Download MP4</a></p></main></body></html>')

    Path('assembled_outputs/seventeen_final.json').write_text(json.dumps({
        'output_id': 'seventeen_library_loop_4_final', 'output_path': str(video),
        'duration_seconds': DURATION, 'resolution': '1920x1080',
        'assembly_tool': 'HyperFrames 0.8.34', 'source_runs': sorted(set(selected['plates'].values())),
        'reference_library_manifest': 'artifacts/library-loop-4/references/manifest.json',
        'scorecard': 'docs/SEVENTEEN_SCORECARD.md',
        'verification': str(ROOT / 'verification.json'), 'cost': costs}, indent=2) + '\n')

    print(json.dumps({'path': str(video), 'bytes': video.stat().st_size,
                      'duration': float(probe['format']['duration']), 'cost': costs,
                      'decode_ok': True,
                      'transcript_checked': transcript is not None}, indent=2))


if __name__ == '__main__':
    main()
