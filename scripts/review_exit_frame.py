"""Extract candidates, then record a visually reviewed handoff with source provenance."""
import argparse
import hashlib
import json
import subprocess
from pathlib import Path


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('source', type=Path)
    parser.add_argument('--at', type=float, nargs='+', required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--approve-reason')
    args = parser.parse_args()
    probe = json.loads(subprocess.check_output(['ffprobe', '-v', 'error', '-show_format',
                        '-show_streams', '-of', 'json', str(args.source)]))
    duration = float(probe['format']['duration'])
    if any(t < 0 or t >= duration for t in args.at):
        raise ValueError('Candidate times must fall inside source footage')
    if args.approve_reason and len(args.at) != 1:
        raise ValueError('Approve exactly one inspected candidate')
    args.output.mkdir(parents=True, exist_ok=True)
    for at in args.at:
        path = args.output / f'exit-{at:.3f}.png'
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', str(at), '-i', str(args.source),
                        '-frames:v', '1', str(path)], check=True)
        print(path)
    if args.approve_reason:
        record = {'source': str(args.source), 'source_sha256': digest(args.source),
                  'source_duration': duration, 'selected_at': args.at[0],
                  'previous_cut_end': args.at[0], 'reference': str(path),
                  'reference_sha256': digest(path), 'reviewed': True,
                  'review_reason': args.approve_reason,
                  'limitation': 'Source timestamp seeks to a decoded frame; inspect the rendered joint, not just this still.'}
        (args.output / 'selection.json').write_text(json.dumps(record, indent=2) + '\n')


if __name__ == '__main__':
    main()
