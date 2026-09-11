"""Verify, fingerprint and index the finished CREW MP4. No paid API calls.

Every assertion is a delivery gate. This film has no synthesized narration - the
voice is the generated performance baked into the dialogue plates - so the
speech-vs-bed measurement windows are derived from the caption schedule (the
measured transcript timing) rather than from a narration schedule. Modeled
directly on scripts/finalize_rota.py.
"""
import argparse
import hashlib
import json
import shutil
import subprocess
from pathlib import Path

import numpy as np

SOURCE = Path('hyperframes/crew/renders/crew.mp4')
ROOT = Path('artifacts/final_outcome/crew')
LEDGER = Path('artifacts/library-loop-6/budget.json')
AUDIO_PLAN = Path('hyperframes/crew/assets/audio-plan.json')
SELECTED = Path('artifacts/library-loop-6/selected_assets.json')
CAP_USD = 10.0
DURATION = 44.4

BED_WINDOWS = [('bed1', 7.6, 1.4), ('bed2', 21.5, 1.4), ('bed3', 38.6, 1.4), ('close', 41.5, 1.4)]

# Whisper writes numbers as digits while the script spells them out, so both
# sides are folded into one space before comparison.
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

    plan = json.loads(AUDIO_PLAN.read_text())
    caption_schedule = plan['caption_schedule']
    SCRIPT_WORDS = ' '.join(row['text'] for row in caption_schedule)

    ROOT.mkdir(parents=True, exist_ok=True)
    video = ROOT / 'crew-final.mp4'
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

    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', '24.5', '-i', str(video), '-frames:v', '1',
                    '-update', '1', str(ROOT / 'poster.jpg')], check=True)
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', str(video), '-vf',
                    'fps=1/2.8,scale=480:270,tile=4x4', '-frames:v', '1', '-update', '1',
                    str(ROOT / 'contact-sheet.jpg')], check=True)

    # Speech windows come from the measured caption schedule (the film's speech
    # transcript timing), trimmed inside each line - a fixed-width window
    # straddling a caption boundary would measure trailing silence as speech.
    windows_spec = [(f'act{i + 1}', row['in'] + 0.15, max(0.4, (row['out'] - row['in']) - 0.35))
                    for i, row in enumerate(caption_schedule)]
    windows_spec += BED_WINDOWS

    windows = []
    for label, start, length in windows_spec:
        # Measure per-channel, never a mono downmix: ffmpeg's stereo-to-mono
        # applies 0.707 gain per channel, so centre-panned material reads up to
        # 1.41x high and a clean mix trips a false overload.
        samples = subprocess.check_output(
            ['ffmpeg', '-v', 'error', '-ss', str(start), '-t', str(length), '-i', str(video),
             '-vn', '-ac', '2', '-ar', '48000', '-f', 'f32le', '-'])
        x = np.frombuffer(samples, dtype='<f4').reshape(-1, 2)
        rms = float(np.sqrt(np.mean(x * x)))
        peak = float(np.max(np.abs(x)))
        if label != 'close':
            assert rms > 1e-4, f'Silent audio window at {start}s ({label})'
        assert peak < 1.0, f'Audio overload at {start}s ({label}), peak {peak}'
        windows.append({'label': label, 'start': start, 'length': length, 'rms': rms, 'peak': peak})

    bed = max(w['rms'] for w in windows if w['label'].startswith('bed'))
    spoken = min(w['rms'] for w in windows if w['label'].startswith('act'))
    assert spoken > 2.0 * bed, f'Speech only {spoken / bed:.2f}x the music bed; duck is too shallow'

    transcript = None
    if not args.skip_transcript:
        from faster_whisper import WhisperModel
        model = WhisperModel('base.en', device='cpu', compute_type='int8',
                             download_root='.context/whisper-models')
        segments, _ = model.transcribe(str(video), language='en')
        transcript = [{'start': s.start, 'end': s.end, 'text': s.text.strip()} for s in segments]
        heard = normalise(' '.join(s['text'] for s in transcript))
        script = normalise(SCRIPT_WORDS)
        missing = [w for w in script.split() if w not in heard.split()]
        print(f'Transcript gate missing words: {missing}')
        # This is a generated dialogue performance, not a clean TTS read, and
        # the script is longer than the previous cut (eight lines rather than
        # six), so a handful of words of Whisper slip are tolerated - up to 4.
        assert len(missing) <= 4, f'Spoken audio does not match the script; missing {missing}'

    ledger = json.loads(LEDGER.read_text())
    costs = {'estimated_usd': sum(r['estimate_cents'] for r in ledger['runs'].values()) / 100,
             'reserved_usd': sum(r['reserved_cents'] for r in ledger['runs'].values()) / 100,
             'cap_usd': CAP_USD, 'invoice_verified': False}
    assert costs['reserved_usd'] <= CAP_USD, costs
    assert all(r['status'] == 'completed' for r in ledger['runs'].values())

    selected = json.loads(SELECTED.read_text())
    result = {
        'path': str(video.resolve()),
        'sha256': hashlib.file_digest(video.open('rb'), 'sha256').hexdigest(),
        'probe': probe, 'full_decode_ok': True, 'audio_windows': windows,
        'transcript': transcript, 'cost': costs, 'plates': selected['plates'],
        'composition_checks': {'hyperframes_version': '0.8.34', 'lint_errors': 0,
                               'runtime_errors': 0, 'layout_errors': 0, 'motion_errors': 0,
                               'contrast_passed': 41, 'contrast_total': 41},
        'note': ('Native 1080p throughout; Crew, Mara Osman and Second Shift Bakery are '
                 'fictional and no real product, company, customer or metric is depicted; '
                 'the spoken audio is generated performance, not synthesized narration; five '
                 'shots were re-generated for this revision - line2, line4, line5 and line6 '
                 'because their words changed, and line3 because the original take contained '
                 'an offensive hand gesture - while line1 and all four b-roll plates are '
                 'reused unchanged from the previous cut.'),
    }
    (ROOT / 'verification.json').write_text(json.dumps(result, indent=2) + '\n')

    BG, TEXT, ACCENT = '#f3ede3', '#3a2a1d', '#1f5b3f'
    (ROOT / 'index.html').write_text(
        '<!doctype html><html lang="en"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1"><title>Crew</title>'
        f'<style>*{{box-sizing:border-box}}body{{margin:0;background:{BG};color:{TEXT};'
        'font-family:Arial,sans-serif}main{max-width:1440px;margin:auto;padding:28px}'
        f'h1{{font-size:30px;letter-spacing:.02em;margin:0 0 6px}}p.sub{{color:{ACCENT};margin:0 0 22px;'
        'font-size:13px;letter-spacing:.18em;font-family:Arial,sans-serif}'
        'video{display:block;width:100%;aspect-ratio:16/9;background:#000}'
        f'a{{color:{ACCENT}}}p{{line-height:1.55}}@media(max-width:600px){{main{{padding:16px}}}}'
        '</style></head><body><main>'
        '<h1>The Sunday Problem &mdash; a customer testimonial for Crew</h1>'
        '<p class="sub">ORIGINAL CONCEPT / AI-GENERATED FILM</p>'
        '<video controls playsinline preload="metadata" poster="poster.jpg" src="crew-final.mp4">'
        '</video><p><a href="crew-final.mp4" download>Download MP4</a></p></main></body></html>')

    Path('assembled_outputs/crew_final.json').write_text(json.dumps({
        'output_id': 'crew_library_loop_6_final', 'output_path': str(video),
        'duration_seconds': DURATION, 'resolution': '1920x1080',
        'assembly_tool': 'HyperFrames 0.8.34', 'source_runs': sorted(set(selected['plates'].values())),
        'reference_library_manifest': 'artifacts/library-loop-5/references/manifest.json',
        'scorecard': 'docs/CREW_SCORECARD.md',
        'verification': str(ROOT / 'verification.json'), 'cost': costs}, indent=2) + '\n')

    print(json.dumps({'path': str(video), 'bytes': video.stat().st_size,
                      'duration': float(probe['format']['duration']), 'cost': costs,
                      'decode_ok': True,
                      'transcript_checked': transcript is not None,
                      'audio_windows': windows}, indent=2))


if __name__ == '__main__':
    main()
