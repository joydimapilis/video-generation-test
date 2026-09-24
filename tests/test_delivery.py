import json
import subprocess
import sys
from pathlib import Path
import runpy

import pytest

from amarillo.delivery import (reverse_engineering_path, write_reverse_engineering,
                               require_reverse_engineering, require_video_documents)


def record(video):
    return {'video': video.name, 'structure': '0–3s: authored title, then a held ending.',
            'prompts': 'Brief: show the demo name. No generated footage.',
            'models_methods': 'HyperFrames authored HTML and exact typography.',
            'routing_decisions': 'Deterministic rendering preserves readable text.',
            'revisions': 'No revisions were needed.', 'failed_attempts': 'No failed attempts.',
            'final_learnings': 'Keep the title visible for the final two seconds.'}


def test_three_videos_need_three_distinct_colocated_documents(tmp_path):
    videos = [tmp_path / f'film-{i}.mp4' for i in range(3)]
    for i, video in enumerate(videos):
        video.write_bytes(f'video fixture {i}'.encode())
    for video in videos[:2]:
        write_reverse_engineering(video, record(video))
    (tmp_path / 'REPORT.md').write_text('Combined production report for all three films.')
    with pytest.raises(ValueError, match='film-2.reverse-engineering.md'):
        require_video_documents(videos)
    write_reverse_engineering(videos[2], record(videos[2]))
    results = require_video_documents(videos)
    assert len({r['reverse_engineering'] for r in results}) == 3
    assert all(reverse_engineering_path(v).parent == v.parent for v in videos)
    reverse_engineering_path(videos[1]).unlink()
    with pytest.raises(ValueError, match='incomplete'):
        require_video_documents(videos)


def test_document_is_bound_to_one_specific_render(tmp_path):
    a, b = tmp_path / 'a.mp4', tmp_path / 'b.mp4'
    a.write_bytes(b'first render'); b.write_bytes(b'second render')
    write_reverse_engineering(a, record(a))
    reverse_engineering_path(b).write_text(reverse_engineering_path(a).read_text())
    with pytest.raises(ValueError, match='exactly this video'):
        require_reverse_engineering(b)
    a.write_bytes(b'revised render')
    with pytest.raises(ValueError, match='current MP4'):
        require_reverse_engineering(a)
    write_reverse_engineering(a, record(a))
    assert require_reverse_engineering(a)['documentation_complete']


def test_incomplete_or_shared_document_cannot_pass(tmp_path):
    video = tmp_path / 'film.mp4'
    video.write_bytes(b'fixture')
    for changes in ({'video': 'other.mp4'}, {'prompts': ''}, {'failed_attempts': 'TODO'}):
        with pytest.raises(ValueError):
            write_reverse_engineering(video, {**record(video), **changes})
    write_reverse_engineering(video, record(video))
    document = reverse_engineering_path(video)
    text = document.read_text()
    document.write_text(text.replace('## Routing decisions', '## Other notes'))
    with pytest.raises(ValueError, match='Routing decisions'):
        require_reverse_engineering(video)
    document.unlink()
    shared = tmp_path / 'shared.md'
    shared.write_text(text)
    document.symlink_to(shared)
    with pytest.raises(ValueError):
        require_reverse_engineering(video)


def test_cli_exits_nonzero_if_any_video_lacks_its_document(tmp_path):
    video = tmp_path / 'film.mp4'
    video.write_bytes(b'fixture')
    source = tmp_path / 'film.production.json'
    source.write_text(json.dumps(record(video)))
    command = [sys.executable, '-m', 'amarillo.delivery']
    assert subprocess.run(command + ['check', str(video)], capture_output=True).returncode == 1
    assert subprocess.run(command + ['write', str(video), str(source)], capture_output=True).returncode == 0
    assert subprocess.run(command + ['check', str(video)], capture_output=True).returncode == 0


def test_existing_single_finalizer_blocks_before_writing_success(tmp_path, monkeypatch):
    script = Path(__file__).resolve().parents[1] / 'scripts/finalize_cue.py'
    monkeypatch.chdir(tmp_path)
    main = runpy.run_path(str(script))['main']
    with pytest.raises(ValueError, match='cue-final.reverse-engineering.md'):
        main()
    assert not list(tmp_path.rglob('verification.json'))
    assert not (tmp_path / 'assembled_outputs').exists()


def test_existing_batch_finalizer_preflights_every_document(tmp_path, monkeypatch):
    script = Path(__file__).resolve().parents[1] / 'scripts/verify_round8_samples.py'
    root = tmp_path / 'artifacts/library-loop-8'
    root.mkdir(parents=True)
    delivery = tmp_path / 'artifacts/final_outcome/round8'
    delivery.mkdir(parents=True)
    names = ['cue-followthrough', 'cue-object-study', 'crew-availability']
    (root / 'sample-build.json').write_text(json.dumps([{'project': 'hyperframes/' + n} for n in names]))
    for name in names:
        video = delivery / (name + '.mp4')
        video.write_bytes(name.encode())
        if name != names[-1]:
            write_reverse_engineering(video, record(video))
    monkeypatch.chdir(tmp_path)
    main = runpy.run_path(str(script))['main']
    with pytest.raises(ValueError, match='crew-availability.reverse-engineering.md'):
        main()
    assert not (root / 'delivery-verification.json').exists()
    assert not (delivery / 'verification.json').exists()
