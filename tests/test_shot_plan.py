from dataclasses import replace
import pytest

from amarillo.references import resolve_local_images
from amarillo.shot_plan import ShotState, interview_prompt, route_shot, validate_join


def test_local_references_are_preflighted_deduplicated_and_nonmutating(tmp_path):
    image = tmp_path / 'frame.jpg'
    image.touch()
    value = 'local:' + str(image)
    payload = {'image_url': value, 'end_image_url': value,
               'elements': [{'reference_image_urls': [value]}], 'prompt': 'local:not-a-file'}
    calls = []
    def upload(path):
        calls.append(path)
        return 'https://example.com/frame.jpg'
    result = resolve_local_images(payload, upload)
    assert len(calls) == 1
    assert payload['image_url'] == value
    assert result['elements'][0]['reference_image_urls'] == [result['image_url']]
    assert result['prompt'] == payload['prompt']
    calls.clear()
    with pytest.raises(ValueError):
        resolve_local_images({**payload, 'end_image_url': 'local:/missing.jpg'}, upload)
    assert calls == []


def test_continuity_separates_position_motion_and_inherits_props():
    state = ShotState(*['fixed'] * 10)
    validate_join(state, state, 'continuous')
    for field in ('travel_direction', 'screen_position', 'prop_state', 'lighting'):
        with pytest.raises(ValueError, match=field):
            validate_join(state, replace(state, **{field: 'changed'}), 'continuous')
    validate_join(state, replace(state, camera='new'), 'cutaway')
    with pytest.raises(ValueError):
        validate_join(state, state, 'typo')
    with pytest.raises(ValueError):
        interview_prompt(state, replace(state, identity='other person'), 'Hello')


def test_routing_requires_real_references():
    with pytest.raises(ValueError):
        route_shot('interview')
    assert route_shot('interview', has_reference=True).endswith('image-to-video')
    assert route_shot('hands').endswith('text-to-video')
    with pytest.raises(ValueError):
        route_shot('hands', continuous=True)
    assert route_shot('exact_ui') == 'hyperframes'
