"""Resolve explicit local image references without changing the saved request."""
from copy import deepcopy
from pathlib import Path


IMAGE_FIELDS = {'image_url', 'start_image_url', 'end_image_url', 'frontal_image_url',
                'image_urls', 'reference_image_urls'}


def resolve_local_images(payload, upload=None):
    result = deepcopy(payload)
    references = []

    def visit(value, field=None, parent=None, key=None):
        if isinstance(value, dict):
            for k, v in value.items():
                visit(v, k, value, k)
        elif isinstance(value, list):
            for i, v in enumerate(value):
                visit(v, field, value, i)
        elif field in IMAGE_FIELDS and isinstance(value, str) and value.startswith('local:'):
            path = Path(value[6:]).expanduser().resolve()
            if not path.is_file():
                raise ValueError(f'Missing local image for {field}: {path}')
            references.append((parent, key, path))

    # Validate every path before uploading anything.
    visit(result)
    if references and upload is None:
        import fal_client
        upload = fal_client.upload_file
    uploaded = {}
    for parent, key, path in references:
        if path not in uploaded:
            uploaded[path] = upload(path)
        parent[key] = uploaded[path]
    return result
