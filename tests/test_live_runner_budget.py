import json
import pytest
from amarillo import fal_runner


def write_plan(tmp_path, cost=1, total=0):
    path = tmp_path / 'plan.json'
    path.write_text(json.dumps({'total_estimated_cost_usd': total, 'runs': [
        {'run_id': 'test', 'model_id': 'test', 'endpoint': 'example', 'input': {}, 'estimated_cost_usd': cost}]}))
    return path


def test_cannot_bypass_cap_with_forged_total_or_nan(tmp_path):
    path = write_plan(tmp_path, cost=11, total=0)
    with pytest.raises(SystemExit):
        fal_runner.run_plan(path, tmp_path / 'results.jsonl', True, 10)
    for cap in [float('nan'), float('inf'), 0, -1, True, 10.001]:
        with pytest.raises(ValueError):
            fal_runner.run_plan(path, tmp_path / 'results.jsonl', True, cap)


def test_failed_live_request_is_reserved_and_never_automatically_retried(tmp_path, monkeypatch):
    calls = []
    def run(run, live):
        calls.append(run)
        return {**run, 'status': 'failed', 'error': 'submission timed out'}
    monkeypatch.setattr(fal_runner, 'run_one', run)
    path = write_plan(tmp_path)
    results = tmp_path / 'results.jsonl'
    fal_runner.run_plan(path, results, True, 10)
    fal_runner.run_plan(path, results, True, 10, skip_completed=False)
    assert len(calls) == 1
    budget = json.loads(results.with_suffix('.budget.json').read_text())
    assert sum(r['reserved_cents'] for r in budget['runs'].values()) == 115


def test_historical_failures_count_against_budget(tmp_path, monkeypatch):
    calls = []
    monkeypatch.setattr(fal_runner, 'run_one', lambda *a, **k: calls.append(a))
    results = tmp_path / 'results.jsonl'
    results.write_text(json.dumps({'run_id': 'old', 'status': 'failed', 'estimated_cost_usd': 8}) + '\n')
    with pytest.raises(ValueError, match='budget exceeded'):
        fal_runner.run_plan(write_plan(tmp_path), results, True, 10)
    assert calls == []
