"""Local temporal diagnostics, reference provenance and ordered transcript checks.

Pixel changes flag seams, not identity, naturalness, or motion quality.
"""
import hashlib
import json
import re
import subprocess
from pathlib import Path

import numpy as np


ROOT = Path('artifacts/library-loop-6')


def frames(path, start, duration, crop=None):
    filters = ([crop] if crop else []) + ['fps=24', 'scale=160:90']
    raw = subprocess.check_output(['ffmpeg', '-v', 'error', '-ss', str(start), '-i', str(path),
        '-t', str(duration), '-vf', ','.join(filters), '-pix_fmt', 'rgb24', '-f', 'rawvideo', '-'])
    return np.frombuffer(raw, np.uint8).reshape(-1, 90, 160, 3).astype(np.float32) / 255


def boundary(a, b, end, crop=None):
    left = frames(a, end - 1, 1, crop)
    right = frames(b, 0, 1, crop)
    changes = np.mean(np.abs(np.diff(np.concatenate([left, right]), axis=0)), axis=(1, 2, 3))
    seam = len(left) - 1
    return {'boundary_mean_absolute_pixel_change': float(changes[seam]),
            'adjacent_median_change': float(np.median(np.delete(changes, seam))),
            'one_second_either_side_changes': changes.tolist(),
            'note': 'Diagnostic only; stationary or frozen faces can also score low.'}


def words(text):
    return re.findall(r"[a-z]+(?:'[a-z]+)?", text.lower())


def main():
    result = {'method': '24 fps, 160x90 RGB; one second each side; no perceptual or identity score'}
    original = ROOT / 'outputs/line4_product_v1.mp4'
    new = ROOT / 'outputs/realism_line4_v2.mp4'
    following = ROOT / 'outputs/realism_line5_chained.mp4'
    for label, a, b, end in [
        ('original_common_anchor', original, ROOT / 'outputs/line5_how_v1.mp4', 5.125),
        ('new_exit_conditioned', new, following, 5.125),
        ('new_prompt_common_anchor_control', new, ROOT / 'outputs/realism_line5_control.mp4', 5.125),
    ]:
        if b.exists():
            result[label] = {'full_frame': boundary(a, b, end),
                             'head_region': boundary(a, b, end, 'crop=720:640:420:20')}
    result['speech'] = {}
    for config in Path('configs').glob('crew_realism_*.json'):
        for run in json.loads(config.read_text())['runs']:
            evidence = ROOT / 'evidence' / (run['id'] + '.json')
            if not evidence.exists() or 'line' not in run:
                continue
            transcript = json.loads(evidence.read_text()).get('transcript', [])
            text = ' '.join(s['text'] for s in transcript)
            result['speech'][run['id']] = {'expected': run['line'], 'recognized': text,
                'ordered_words_equal': words(text) == words(run['line']),
                'note': 'Automatic Whisper base.en, not human listening or proof of lip sync.'}
    selection = json.loads((ROOT / 'realism/selected/selection.json').read_text())
    result['reference_hash_matches'] = hashlib.sha256(Path(selection['reference']).read_bytes()).hexdigest() == selection['reference_sha256']
    data = json.loads((ROOT / 'budget.json').read_text())
    result['cost'] = {'estimated_cents': sum(r['estimate_cents'] for r in data['runs'].values()),
                      'reserved_cents': sum(r['reserved_cents'] for r in data['runs'].values()),
                      'limit_cents': data['limit_cents']}
    target = ROOT / 'realism/diagnostics.json'
    target.write_text(json.dumps(result, indent=2) + '\n')
    print(target)
    print(json.dumps({k: v for k, v in result.items() if k in {'speech', 'cost'}}, indent=2))


if __name__ == '__main__':
    main()
