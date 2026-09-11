"""Inspect a second, deliberately different library slice: hardware and field launches.

Round 1 sampled software/UI launches. This slice targets the genres those six
references never covered, so the next concept is not a restatement of the first.
Source media is read only; nothing is copied into the project.
"""
import json
import subprocess
from pathlib import Path

import os

# The reference library lives outside the repo and its path is personal, so it is
# read from the environment rather than hardcoded. Point AMARILLO_LIBRARY_DIR at
# the folder of source videos, or symlink it to data/library.
LIBRARY = Path(os.environ.get('AMARILLO_LIBRARY_DIR', 'data/library'))
OUT = Path('artifacts/library-loop-2/references')
TERMS = [
    ('1X-NEO-The-Home-Robot', 'consumer_hardware_launch'),
    ('Airbound-Airbound-Raises', 'hardware_funding_announcement'),
    ('Apollyon-Dynamics', 'field_test_footage'),
    ('Beyond-Reach-Labs', 'deployable_hardware_field'),
    ('Extropic-Hello-Thermo-World', 'deep_tech_launch'),
    ('Friend-Introducing-Friend', 'emotional_consumer_hardware'),
    ('ElevenLabs-ElevenLabs-Raises', 'funding_milestone'),
    ('Aurus-Built-with-Intention', 'brand_sizzle'),
]


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    files = sorted(LIBRARY.glob('*.mp4'))
    manifest = {'library': str(LIBRARY), 'file_count': len(files),
                'slice': 'hardware, field and milestone launches', 'selection': []}
    for index, (term, genre) in enumerate(TERMS):
        path = next((p for p in files if term in p.name), None)
        if path is None:
            print('MISSING', term, flush=True)
            continue
        meta = json.loads(subprocess.check_output([
            'ffprobe', '-v', 'error', '-show_format', '-show_streams', '-of', 'json', str(path)]))
        duration = float(meta['format']['duration'])
        video = next(s for s in meta['streams'] if s['codec_type'] == 'video')
        has_audio = any(s['codec_type'] == 'audio' for s in meta['streams'])
        sheet = OUT / f'{index + 1:02d}-{genre}.jpg'
        # Fit-then-pad so vertical and square library entries letterbox instead of failing.
        if not sheet.exists():
            subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', str(path), '-vf',
                            f'fps=12/{duration},scale=426:240:force_original_aspect_ratio=decrease,'
                            'pad=426:240:(ow-iw)/2:(oh-ih)/2,tile=4x3',
                            '-frames:v', '1', str(sheet)], check=True)
        manifest['selection'].append({
            'genre': genre, 'source': str(path), 'name': path.name, 'duration': duration,
            'resolution': f"{video['width']}x{video['height']}", 'has_audio': has_audio,
            'contact_sheet': str(sheet)})
        print(f"{index + 1} {genre:32} {duration:6.1f}s  {video['width']}x{video['height']}  "
              f"audio={has_audio}  {path.name[:60]}", flush=True)
    (OUT / 'manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
    print('Wrote', OUT / 'manifest.json')


if __name__ == '__main__':
    main()
