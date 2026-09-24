"""Check delivered comparison structure, decode, source provenance and audio order."""
from amarillo.delivery import require_reverse_engineering

import hashlib
import json
from pathlib import Path
import subprocess
import numpy as np

ROOT = Path('artifacts/library-loop-7')


def pcm(path):
    raw = subprocess.check_output(['ffmpeg', '-v', 'error', '-i', str(path), '-vn',
                                   '-ac', '1', '-ar', '16000', '-f', 'f32le', '-'])
    return np.frombuffer(raw, dtype='<f4').astype(np.float64)


def main():
    path = ROOT / 'interview-comparison.mp4'
    require_reverse_engineering(path)
    probe = json.loads(subprocess.check_output(['ffprobe', '-v', 'error', '-show_format',
                                               '-show_streams', '-of', 'json', str(path)]))
    video = next(s for s in probe['streams'] if s['codec_type'] == 'video')
    assert (video['width'], video['height'], video['r_frame_rate']) == (1920, 1080, '24/1')
    assert abs(float(probe['format']['duration']) - 24) < .1
    decoded = subprocess.run(['ffmpeg', '-v', 'error', '-i', str(path), '-f', 'null', '-'], capture_output=True)
    assert decoded.returncode == 0 and not decoded.stderr, decoded.stderr.decode()
    sources = json.loads(Path('hyperframes/interview-models/sources.json').read_text())
    for source in sources:
        assert hashlib.sha256(Path(source['source']).read_bytes()).hexdigest() == source['sha256']
        assert hashlib.sha256(Path(source['asset']).read_bytes()).hexdigest() == source['sha256']
    wave = pcm(path)
    audio = []
    for start, source in [(0, 'veo'), (6, 'kling-contract'), (12, 'veo'), (18, 'kling-restrained')]:
        original = pcm(Path('hyperframes/interview-models/assets') / (source + '.mp4'))[4000:88000]
        candidate = wave[start * 16000 + 4000:start * 16000 + 88000]
        correlation = float(np.dot(original, candidate) / (np.linalg.norm(original) * np.linalg.norm(candidate)))
        assert correlation > .9, (source, correlation)
        audio.append({'start_seconds': start, 'source': source, 'pcm_correlation': correlation})
    ledger = json.loads((ROOT / 'budget.json').read_text())
    reserved = sum(r['reserved_cents'] for r in ledger['runs'].values())
    assert reserved <= ledger['limit_cents'] <= 1000
    data = {'path': str(path), 'sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
            'duration': float(probe['format']['duration']), 'resolution': '1920x1080',
            'fps': 24, 'decode_ok': True, 'source_hashes_match': True,
            'audio_order': audio, 'mono_audio_peak': float(np.abs(wave).max()),
            'reserved_cents': reserved, 'cap_cents': ledger['limit_cents'],
            'limits': 'Audio correlation verifies source/order, not naturalness or lip sync. No audience review.'}
    (ROOT / 'comparison-verification.json').write_text(json.dumps(data, indent=2) + '\n')
    print(json.dumps(data, indent=2))


if __name__ == '__main__':
    main()
