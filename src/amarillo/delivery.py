"""Per-video reverse-engineering documents and a fail-closed delivery gate.

These checks supplement picture/audio/composition review; they cannot perform it.
"""
import hashlib
import json
import re
from pathlib import Path

SECTIONS = {
    'structure': 'Structure',
    'prompts': 'Prompts',
    'models_methods': 'Models and methods',
    'routing_decisions': 'Routing decisions',
    'revisions': 'Revisions',
    'failed_attempts': 'Failed attempts',
    'final_learnings': 'Final learnings',
}


def reverse_engineering_path(video):
    video = Path(video)
    return video.with_name(video.stem + '.reverse-engineering.md')


def video_hash(video):
    video = Path(video)
    if video.suffix.lower() != '.mp4' or not video.is_file() or video.stat().st_size == 0:
        raise ValueError(f'Final MP4 is missing or empty: {video}')
    with video.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def require_content(value, section):
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f'Reverse-engineering section is missing or empty: {section}')
    if re.search(r'\b(TODO|TBD|PLACEHOLDER)\b|<fill[^>]*>', value, re.I):
        raise ValueError(f'Unfinished reverse-engineering section: {section}')
    return value.strip()


def write_reverse_engineering(video, record):
    """Render one agent-authored production record; never invent missing history."""
    video = Path(video)
    digest = video_hash(video)
    if record.get('video') != video.name:
        raise ValueError('Production record must identify this individual MP4 filename')
    contents = {key: require_content(record.get(key), heading) for key, heading in SECTIONS.items()}
    title = record.get('title') or video.stem
    lines = [f'# Reverse engineering — {title}', '', f'Video: `{video.name}`',
             f'SHA-256: `{digest}`', '']
    for key, heading in SECTIONS.items():
        lines.extend([f'## {heading}', '', contents[key], ''])
    document = reverse_engineering_path(video)
    if document.is_symlink():
        raise ValueError('Each video needs its own document, not a shared symlink')
    document.write_text('\n'.join(lines), encoding='utf-8')
    return require_reverse_engineering(video)


def require_reverse_engineering(video):
    """Raise before completion if the individual document is missing or stale."""
    video = Path(video)
    document = reverse_engineering_path(video)
    if not document.is_file() or document.is_symlink():
        raise ValueError(f'Video is incomplete: required document missing: {document}')
    text = document.read_text(encoding='utf-8')
    if re.findall(r'^Video: `(.+)`$', text, re.M) != [video.name]:
        raise ValueError(f'Document must describe exactly this video: {video.name}')
    if re.findall(r'^SHA-256: `([a-f0-9]{64})`$', text, re.M) != [video_hash(video)]:
        raise ValueError(f'Reverse-engineering document does not match the current MP4: {document}')
    sections = re.split(r'^## (.+)\s*$', text, flags=re.M)
    headings = sections[1::2]
    for heading in SECTIONS.values():
        if headings.count(heading) != 1:
            raise ValueError(f'Required reverse-engineering heading missing or duplicated: {heading}')
        require_content(sections[2 + 2 * headings.index(heading)], heading)
    return {'video': str(video), 'reverse_engineering': str(document),
            'reverse_engineering_sha256': hashlib.sha256(document.read_bytes()).hexdigest(),
            'documentation_complete': True}


def require_video_documents(videos):
    """Every member must pass; one shared report never completes a batch."""
    return [require_reverse_engineering(video) for video in videos]


def main():
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest='command', required=True)
    write = commands.add_parser('write', help='Create one document from one factual production record')
    write.add_argument('video', type=Path)
    write.add_argument('record', type=Path)
    check = commands.add_parser('check', help='Require a separate document for every listed MP4')
    check.add_argument('videos', type=Path, nargs='+')
    args = parser.parse_args()
    try:
        result = (write_reverse_engineering(args.video, json.loads(args.record.read_text()))
                  if args.command == 'write' else require_video_documents(args.videos))
    except (ValueError, OSError, KeyError) as error:
        parser.exit(1, f'{error}\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
