from amarillo.learning import recommend, signature
from amarillo.shot_plan import adapt_interview_input, route_shot
import json
import pytest


def row(endpoint='veo', **changes):
    return dict(key=endpoint, endpoint=endpoint, use_case='interview', image_conditioned=True,
                audio_requested=True, verified_output=True, decision='provisional', legacy_quality=8,
                signature=endpoint, **changes)


def test_routes_only_with_compatible_verified_evidence():
    r = row()
    assert recommend([r], 'interview', has_reference=True, audio=True)['endpoint'] == 'veo'
    for field, value in [('verified_output', False), ('decision', 'reject'), ('legacy_quality', None),
                         ('image_conditioned', False), ('audio_requested', False), ('use_case', 'product_ad')]:
        assert recommend([{**r, field: value}], 'interview', has_reference=True, audio=True)['status'] == 'needs_test'


def test_new_review_changes_route_without_code_change_and_duplicates_do_not_add_support():
    a = row()
    b = {**row('kling'), 'legacy_quality': 9}
    rec = recommend([a, b, b], 'interview', has_reference=True, audio=True)
    assert rec['endpoint'] == 'kling'
    assert rec['reviewed_samples'] == 1
    assert recommend([a, b], 'interview', has_reference=True, audio=True, min_reviews=2)['status'] == 'needs_test'


def test_exact_ui_never_uses_a_generated_text_score():
    assert recommend([], 'exact_ui')['endpoint'] == 'hyperframes'


def test_signature_is_order_independent_even_in_nested_inputs():
    assert signature('x', {'a': {'b': 1, 'c': 2}}) == signature('x', {'a': {'c': 2, 'b': 1}})


def test_external_image_allowances_are_not_video_model_evidence(tmp_path):
    from amarillo.learning import collect_experiments
    loop = tmp_path / 'library-loop-images'
    loop.mkdir()
    (loop / 'budget.json').write_text(json.dumps({'runs': {'image': {
        'payload': {'provider': 'external-image'}, 'status': 'completed',
        'estimate_cents': 100, 'reserved_cents': 115}}}))
    assert collect_experiments(tmp_path) == []


def test_shot_router_uses_saved_evidence_and_adapts_schema(tmp_path):
    p = tmp_path / 'learning.json'
    endpoint = 'fal-ai/kling-video/v3/pro/image-to-video'
    p.write_text(json.dumps({'runs': [row(endpoint)]}))
    assert route_shot('interview', has_reference=True, evidence_path=p) == endpoint
    adapted = adapt_interview_input(endpoint, {'prompt': 'hello', 'duration': '6s',
                                             'image_url': 'local:x.jpg', 'seed': 92, 'resolution': '1080p'})
    assert adapted['duration'] == '6'
    assert adapted['start_image_url'] == 'local:x.jpg'
    assert 'seed' not in adapted and 'resolution' not in adapted
    with pytest.raises(ValueError, match='validated input adapter'):
        adapt_interview_input('new/model', {'prompt': 'hello', 'duration': '6s'})


def test_native_audio_intent_is_preserved_in_learning(tmp_path):
    from amarillo.learning import collect_experiments, requested_audio
    loop = tmp_path / 'library-loop-native'
    loop.mkdir()
    video = loop / 'take.mp4'
    video.write_bytes(b'fixture')
    (loop / 'evidence').mkdir()
    (loop / 'evidence/take.json').write_text(json.dumps({'full_decode_ok': True}))
    request = {'endpoint': 'minimax/h3/image-to-video', 'audio_requested': True,
               'use_case': 'interview', 'input': {'prompt': 'Speak.', 'image_url': 'local:face.png'}}
    (loop / 'budget.json').write_text(json.dumps({'runs': {'take': {
        'payload': request, 'status': 'completed', 'output_path': str(video),
        'estimate_cents': 36, 'reserved_cents': 42}}}))
    (loop / 'scorecard.json').write_text(json.dumps({'runs': [{
        'id': 'take', 'scores': {k: 8 for k in ('prompt_adherence', 'sampled_stability', 'composition', 'edit_readiness')},
        'decision': 'provisional'}]}))
    rows = collect_experiments(tmp_path)
    assert recommend(rows, 'interview', has_reference=True, audio=True)['endpoint'] == request['endpoint']
    assert recommend(rows, 'interview', has_reference=True, audio=False)['status'] == 'needs_test'
    assert requested_audio({'input': {'generate_audio': True}})
    assert not requested_audio({'input': {}})
    with pytest.raises(ValueError, match='boolean'):
        requested_audio({**request, 'audio_requested': 'false'})


def test_h3_adapter_uses_native_audio_and_native_resolution():
    adapted = adapt_interview_input('minimax/h3/image-to-video', {
        'prompt': 'A quiet interview.', 'duration': '6s', 'image_url': 'local:face.png',
        'seed': 812, 'resolution': '1080p', 'generate_audio': True})
    assert adapted['duration'] == 6
    assert adapted['resolution'] == '768P'
    assert adapted['seed'] == 812
    assert 'generate_audio' not in adapted
    with pytest.raises(ValueError, match='duration'):
        adapt_interview_input('minimax/h3/image-to-video', {
            'prompt': 'hello', 'duration': '4s', 'image_url': 'local:face.png'})
