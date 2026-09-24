import json
from pathlib import Path

import pytest

from amarillo.library import resolve_library, require_reference_review


@pytest.fixture(autouse=True)
def no_external_library(monkeypatch):
    monkeypatch.delenv('AMARILLO_LIBRARY_DIR', raising=False)


def manifest(project, name, library):
    path = project / 'artifacts' / name / 'references/manifest.json'
    path.parent.mkdir(parents=True)
    path.write_text(json.dumps({'library': str(library)}))


def test_saved_phase2_manifest_cannot_be_a_core_fallback(tmp_path):
    reserved = tmp_path / 'references/human-realism'
    reserved.mkdir(parents=True)
    manifest(tmp_path, 'library-loop-computer-realism', 'references/human-realism')
    with pytest.raises(ValueError, match='Phase 2 is excluded'):
        resolve_library(tmp_path)
    general = tmp_path / 'general'
    general.mkdir()
    manifest(tmp_path, 'library-loop-original', 'general')
    assert resolve_library(tmp_path) == general.resolve()


def test_explicit_phase2_and_symlink_alias_rejected(tmp_path, monkeypatch):
    reserved = tmp_path / 'references/human-realism'
    reserved.mkdir(parents=True)
    alias = tmp_path / 'alias'
    alias.symlink_to(reserved, target_is_directory=True)
    for path in (reserved, alias):
        monkeypatch.setenv('AMARILLO_LIBRARY_DIR', str(path))
        with pytest.raises(ValueError, match='Phase 2'):
            resolve_library(tmp_path)
    monkeypatch.delenv('AMARILLO_LIBRARY_DIR')
    (tmp_path / 'data').mkdir()
    (tmp_path / 'data/library').symlink_to(alias, target_is_directory=True)
    with pytest.raises(ValueError, match='Phase 2'):
        resolve_library(tmp_path)


def test_local_library_and_environment_precedence(tmp_path, monkeypatch):
    general = tmp_path / 'general'
    general.mkdir()
    (tmp_path / 'data').mkdir()
    (tmp_path / 'data/library').symlink_to(general, target_is_directory=True)
    assert resolve_library(tmp_path) == general
    override = tmp_path / 'override'
    override.mkdir()
    monkeypatch.setenv('AMARILLO_LIBRARY_DIR', 'override')
    assert resolve_library(tmp_path) == override
    monkeypatch.setenv('AMARILLO_LIBRARY_DIR', 'missing')
    with pytest.raises(ValueError, match='not accessible'):
        resolve_library(tmp_path)


def test_review_gate_requires_footage_and_findings_from_general_library(tmp_path, monkeypatch):
    library = tmp_path / 'general'
    library.mkdir()
    source = library / 'launch.mp4'
    source.write_bytes(b'fixture')
    monkeypatch.setenv('AMARILLO_LIBRARY_DIR', str(library))
    record = {'library': str(library), 'references': [{
        'source': str(source), 'footage_reviewed': True, 'relevance': 'UI launch',
        'pacing': '3-second opening', 'techniques': 'Match cut', 'application': 'Show the same input becoming output'}]}
    path = tmp_path / 'reference-review.json'
    path.write_text(json.dumps(record))
    assert require_reference_review(path, tmp_path) == record
    record['references'][0]['footage_reviewed'] = False
    path.write_text(json.dumps(record))
    with pytest.raises(ValueError, match='Actual footage'):
        require_reference_review(path, tmp_path)
    record['references'][0]['footage_reviewed'] = True
    record['references'][0]['pacing'] = ''
    path.write_text(json.dumps(record))
    with pytest.raises(ValueError, match='pacing'):
        require_reference_review(path, tmp_path)


def test_brief_planning_cannot_skip_references(tmp_path):
    from amarillo.briefing import compose_brief_plan
    output = tmp_path / 'plan.json'
    with pytest.raises(ValueError, match='Review the general video library'):
        compose_brief_plan('A short launch film', tmp_path / 'patterns.json',
                           tmp_path / 'recommendations.json', output)
    assert not output.exists()
