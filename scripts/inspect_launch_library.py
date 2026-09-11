"""Read a deliberately varied library subset without modifying source media."""
import json
import subprocess
from pathlib import Path

import os

# The reference library lives outside the repo and its path is personal, so it is
# read from the environment rather than hardcoded. Point AMARILLO_LIBRARY_DIR at
# the folder of source videos, or symlink it to data/library.
LIBRARY = Path(os.environ.get('AMARILLO_LIBRARY_DIR', 'data/library'))
OUT = Path('artifacts/library-loop/references')
TERMS = ['Motion-5-', 'Content Rewards', 'Pocket-Introducing',
         'SupersonikAI-', 'Tarun-Amasa', 'Cluely-Introducing-Cluely-for-Customer']


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    files = sorted(LIBRARY.glob('*.mp4'))
    manifest = {'library': str(LIBRARY), 'file_count': len(files), 'selection': []}
    for index, term in enumerate(TERMS):
        path = next(p for p in files if term in p.name)
        meta = json.loads(subprocess.check_output([
            'ffprobe', '-v', 'error', '-show_format', '-show_streams', '-of', 'json', str(path)]))
        duration = float(meta['format']['duration'])
        sheet = OUT / f'{index + 1:02d}.jpg'
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', str(path), '-vf',
                        f'fps=8/{duration},scale=480:-1,pad=480:270:(ow-iw)/2:(oh-ih)/2,tile=4x2',
                        '-frames:v', '1', str(sheet)], check=True)
        manifest['selection'].append({'source': str(path), 'duration': duration,
                                      'probe': meta, 'contact_sheet': str(sheet)})
        print(index + 1, path.name, duration, flush=True)
    (OUT / 'manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')


if __name__ == '__main__':
    main()
