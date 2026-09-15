"""Recover an explicitly configured or previously used reference library."""
import json
import os
from pathlib import Path


def resolve_library(project=Path('.')):
    configured = os.environ.get('AMARILLO_LIBRARY_DIR')
    if configured:
        path = Path(configured).expanduser()
        if not path.is_dir():
            raise ValueError('AMARILLO_LIBRARY_DIR is not an accessible directory')
        return path
    local = Path(project) / 'data/library'
    if local.is_dir():
        return local
    candidates = set()
    for manifest in (Path(project) / 'artifacts').glob('library-loop*/references/manifest.json'):
        value = json.loads(manifest.read_text()).get('library')
        if value and Path(value).is_dir():
            candidates.add(Path(value).resolve())
    if len(candidates) == 1:
        return candidates.pop()
    raise ValueError('Set AMARILLO_LIBRARY_DIR: no single accessible saved reference library was found')
