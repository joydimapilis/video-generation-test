"""Resolve the general production library; never fall back to Phase 2 media."""
import json
import os
from pathlib import Path


def general_library_path(value, project=Path('.')):
    project = Path(project).resolve()
    path = Path(value).expanduser()
    if not path.is_absolute():
        path = project / path
    path = path.resolve()
    reserved = (project / 'references/human-realism').resolve()
    if ('human-realism' in path.parts or path == reserved
            or reserved in path.parents or path in reserved.parents):
        raise ValueError('Phase 2 movement references cannot be used as the general video library')
    if not path.is_dir():
        raise ValueError(f'General video library is not accessible: {path}')
    return path


def resolve_library(project=Path('.')):
    project = Path(project).resolve()
    configured = os.environ.get('AMARILLO_LIBRARY_DIR')
    if configured:
        return general_library_path(configured, project)
    local = project / 'data/library'
    if local.exists() or local.is_symlink():
        return general_library_path(local, project)
    candidates = set()
    for manifest in (project / 'artifacts').glob('library-loop*/references/manifest.json'):
        value = json.loads(manifest.read_text()).get('library')
        if value:
            try:
                candidates.add(general_library_path(value, project))
            except ValueError:
                continue
    if len(candidates) == 1:
        return candidates.pop()
    raise ValueError('Set AMARILLO_LIBRARY_DIR or data/library to the general video library; '
                     'no single accessible general library was found. Phase 2 is excluded.')


def require_reference_review(path, project=Path('.')):
    """Validate recorded agent review before planning; preparation is not review."""
    record = json.loads(Path(path).read_text())
    library = resolve_library(project)
    if general_library_path(record['library'], project) != library:
        raise ValueError('Reference review does not match the configured general library')
    if not record.get('references'):
        raise ValueError('Review at least one relevant general-library video before planning')
    for reference in record['references']:
        source = Path(reference['source']).resolve()
        if not source.is_file() or not source.is_relative_to(library):
            raise ValueError(f'Review source is missing or outside the general library: {source}')
        if 'human-realism' in source.parts:
            raise ValueError('Phase 2 reference is not permitted in core review')
        if reference.get('footage_reviewed') is not True:
            raise ValueError('Actual footage/pacing review is required; a contact sheet alone is insufficient')
        for key in ('relevance', 'pacing', 'techniques', 'application'):
            if not isinstance(reference.get(key), str) or not reference[key].strip():
                raise ValueError(f'Missing reference review finding: {key}')
    return record
