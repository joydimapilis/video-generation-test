import pytest

from amarillo.loop_plan import prepare_plan


def plan(root, runs=None):
    return {'budget_root': str(root), 'runs': runs or [
        {'id': 'a', 'estimate_cents': 100, 'endpoint': 'model', 'input': {'prompt': 'test'}}]}


def test_declared_budget_is_used_and_cannot_be_redirected(tmp_path):
    p = plan(tmp_path / 'original')
    root, ledger, summary = prepare_plan(p)
    assert root == tmp_path / 'original'
    assert summary['reserved_after_cents'] == 115
    with pytest.raises(ValueError, match='conflicts'):
        prepare_plan(p, tmp_path / 'fresh')
    assert ledger.read()['runs'] == {}


def test_whole_batch_preflight_and_hard_cap(tmp_path):
    runs = [{'id': str(i), 'estimate_cents': 500, 'endpoint': 'model', 'input': {'prompt': str(i)}} for i in range(2)]
    with pytest.raises(ValueError, match='entire plan'):
        prepare_plan(plan(tmp_path, runs))
    with pytest.raises(ValueError, match='maximum'):
        prepare_plan(plan(tmp_path), cap_cents=1001)


def test_resume_preserves_uncertain_charges_and_rejects_relabelled_retry(tmp_path):
    p = plan(tmp_path)
    _, ledger, _ = prepare_plan(p)
    ledger.reserve('a', 100, p['runs'][0])
    ledger.update('a', status='submission_unknown')
    assert prepare_plan(p)[2]['new_requests'] == 0
    p['runs'][0] = {**p['runs'][0], 'id': 'retry'}
    with pytest.raises(ValueError, match='Identical request'):
        prepare_plan(p)


def test_invalid_ids_and_duplicate_requests(tmp_path):
    p = plan(tmp_path)
    p['runs'][0]['id'] = '../escape'
    with pytest.raises(ValueError, match='safe filenames'):
        prepare_plan(p)
    p = plan(tmp_path)
    p['runs'].append({**p['runs'][0], 'id': 'b'})
    with pytest.raises(ValueError, match='Identical request'):
        prepare_plan(p)
