"""Local evidence, never a synthetic aesthetic score. Optional CPU speech check."""
import argparse
from dataclasses import asdict
import json
import subprocess
from pathlib import Path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--speech', action='store_true')
    parser.add_argument('--root', type=Path, default=Path('artifacts/library-loop'),
                        help='Experiment directory holding outputs/ and evidence/.')
    parser.add_argument('--speech-match', default='ugc,interview',
                        help='Comma-separated run-id substrings to transcribe.')
    args = parser.parse_args()
    root = args.root
    speech_match = [m for m in args.speech_match.split(',') if m]
    evidence = root / 'evidence'
    evidence.mkdir(exist_ok=True)
    model = None
    for path in sorted((root / 'outputs').glob('*.mp4')):
        target = evidence / (path.stem + '.json')
        data = json.loads(target.read_text()) if target.exists() else {}
        if not data:
            probe = json.loads(subprocess.check_output(['ffprobe', '-v', 'error', '-show_format',
                '-show_streams', '-of', 'json', str(path)]))
            duration = float(probe['format']['duration'])
            decode = subprocess.run(['ffmpeg', '-v', 'error', '-i', str(path), '-f', 'null', '-'], capture_output=True)
            sheet = evidence / (path.stem + '.jpg')
            subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', str(path), '-vf',
                f'fps=8/{duration},scale=480:270,tile=4x2', '-frames:v', '1', str(sheet)], check=True)
            data = {'path': str(path), 'probe': probe, 'full_decode_ok': decode.returncode == 0,
                    'decode_errors': decode.stderr.decode(), 'contact_sheet': str(sheet)}
        if args.speech and any(m in path.stem for m in speech_match) and 'transcript' not in data:
            if model is None:
                from faster_whisper import WhisperModel
                model = WhisperModel('base.en', device='cpu', compute_type='int8', download_root='.context/whisper-models')
            segments, info = model.transcribe(str(path), language='en', word_timestamps=True)
            data['transcript'] = [{'start': s.start, 'end': s.end, 'text': s.text,
                                  'words': [asdict(w) for w in s.words]} for s in segments]
            data['speech_note'] = 'Local Whisper base.en automatic transcript; not human listening or proof of lip sync.'
        target.write_text(json.dumps(data, indent=2) + '\n')
        print(path.stem, 'decode:', data['full_decode_ok'],
              'speech:', [s['text'] for s in data.get('transcript', [])], flush=True)


if __name__ == '__main__':
    main()
