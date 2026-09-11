"""Inspect an arbitrary library slice, given as a JSON list of term/genre pairs.

Generic replacement for the round-specific inspect_library_round*.py scripts:
the slice is supplied on the command line instead of being hardcoded, so the
same script can build a contact sheet manifest for any set of terms. Source
media is read only; nothing is copied into the project.
"""
import argparse
import json
import subprocess
from pathlib import Path

import os

# The reference library lives outside the repo and its path is personal, so it is
# read from the environment rather than hardcoded. Point AMARILLO_LIBRARY_DIR at
# the folder of source videos, or symlink it to data/library.
LIBRARY = Path(os.environ.get('AMARILLO_LIBRARY_DIR', 'data/library'))


def shape_of(width, height):
    if height > width:
        return 'portrait'
    if height == width:
        return 'square'
    return 'landscape'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', required=True, help='Output directory for contact sheets and manifest.json')
    parser.add_argument('--terms', required=True,
                         help='JSON file: a list of {"term": "...", "genre": "..."} objects')
    args = parser.parse_args()

    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    terms = json.loads(Path(args.terms).read_text())

    files = sorted(LIBRARY.glob('*.mp4'))
    manifest = {'library': str(LIBRARY), 'file_count': len(files), 'selection': []}
    for index, entry in enumerate(terms):
        term, genre = entry['term'], entry['genre']
        path = next((p for p in files if term in p.name), None)
        if path is None:
            print('MISSING', term, flush=True)
            continue
        try:
            meta = json.loads(subprocess.check_output([
                'ffprobe', '-v', 'error', '-show_format', '-show_streams', '-of', 'json', str(path)]))
            duration = float(meta['format']['duration'])
            video = next(s for s in meta['streams'] if s['codec_type'] == 'video')
            has_audio = any(s['codec_type'] == 'audio' for s in meta['streams'])
            shape = shape_of(video['width'], video['height'])
            sheet = out / f'{index + 1:02d}-{genre}.jpg'
            # Fit-then-pad so vertical and square library entries letterbox instead of failing.
            if not sheet.exists():
                subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', str(path), '-vf',
                                f'fps=12/{duration},scale=426:240:force_original_aspect_ratio=decrease,'
                                'pad=426:240:(ow-iw)/2:(oh-ih)/2,tile=4x3',
                                '-frames:v', '1', str(sheet)], check=True)
        except (subprocess.CalledProcessError, KeyError, StopIteration, ValueError) as exc:
            print('ERROR', term, '->', path.name, ':', exc, flush=True)
            continue
        manifest['selection'].append({
            'genre': genre, 'source': str(path), 'name': path.name, 'duration': duration,
            'resolution': f"{video['width']}x{video['height']}", 'shape': shape,
            'has_audio': has_audio, 'contact_sheet': str(sheet)})
        print(f"{index + 1} {genre:32} {duration:6.1f}s  {video['width']}x{video['height']}  "
              f"{shape:9}  audio={has_audio}  {path.name[:60]}", flush=True)
    (out / 'manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
    print('Wrote', out / 'manifest.json')


if __name__ == '__main__':
    main()
