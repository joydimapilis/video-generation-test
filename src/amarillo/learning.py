"""Evidence-based routing across loops. Unknown quality stays unknown.

Agent reviews are subjective, not calibrated perceptual measurements. Route only
within the same use case, input mode, audio mode, and scoring rubric.
"""
from collections import defaultdict
import hashlib
import json
from pathlib import Path
from statistics import mean

DIMENSIONS = ('human_realism', 'face_realism', 'hand_body_movement',
              'identity_consistency', 'product_accuracy', 'text_ui_accuracy',
              'camera_movement', 'cinematic_quality', 'transition_quality',
              'entry_exit_continuity', 'context_clarity', 'product_message_clarity',
              'prompt_adherence', 'consistency')
LEGACY = ('prompt_adherence', 'sampled_stability', 'composition', 'edit_readiness')


def requested_audio(request):
    """Use the plan's intent for native-audio models without a provider flag.

    Do not infer successful speech or sound from this value; decoded streams
    and transcripts remain the output evidence. Historical plans keep their
    existing generate_audio behavior.
    """
    declared = request.get('audio_requested')
    if declared is not None:
        if type(declared) is not bool:
            raise ValueError('audio_requested must be a boolean')
        return declared
    return request['input'].get('generate_audio') is True


def signature(endpoint, payload):
    return hashlib.sha256(json.dumps([endpoint, payload], sort_keys=True,
                                    separators=(',', ':')).encode()).hexdigest()


def collect_experiments(artifacts):
    rows = []
    for path in sorted(Path(artifacts).glob('library-loop*/budget.json')):
        root = path.parent
        ledger = json.loads(path.read_text())
        score_path = root / 'scorecard.json'
        reviews = {r['id']: r for r in json.loads(score_path.read_text()).get('runs', [])} if score_path.exists() else {}
        for identifier, result in ledger['runs'].items():
            request = result['payload']
            review = reviews.get(identifier, {})
            evidence_path = root / 'evidence' / f'{identifier}.json'
            evidence = json.loads(evidence_path.read_text()) if evidence_path.exists() else {}
            output = result.get('output_path')
            verified = (result['status'] == 'completed' and output and Path(output).is_file()
                        and evidence.get('full_decode_ok') is True)
            scores = review.get('scores', {}) if verified else {}
            if any(type(v) not in (int, float) or not 0 <= v <= 10 for v in scores.values() if v is not None):
                raise ValueError('Invalid review score: ' + str(score_path) + ':' + identifier)
            payload = request['input']
            image_conditioned = any(k in payload for k in ('image_url', 'start_image_url', 'reference_image_urls'))
            quality = mean(scores[k] for k in LEGACY) if all(scores.get(k) is not None for k in LEGACY) else None
            review_text = review.get('review', '')
            decision = review.get('decision') or ('review_required' if quality is None else
                       'reject' if scores.get('edit_readiness', 0) < 6 else 'provisional')
            rows.append({'key': root.name + '/' + identifier, 'id': identifier,
                         'endpoint': request['endpoint'], 'use_case': request.get('use_case', 'unknown'),
                         'image_conditioned': image_conditioned,
                         'audio_requested': requested_audio(request),
                         'status': result['status'], 'verified_output': bool(verified),
                         'decision': decision, 'scores': {k: scores.get(k) for k in DIMENSIONS},
                         'legacy_scores': {k: scores.get(k) for k in LEGACY},
                         'legacy_quality': round(quality, 3) if quality is not None else None,
                         'review': review_text, 'review_method': review.get('review_method', 'agent review; sampled frames; not audience-tested'),
                         'estimate_cents': result['estimate_cents'], 'reserved_cents': result['reserved_cents'],
                         'elapsed_seconds': result.get('elapsed_seconds'), 'output': output,
                         'evidence': str(evidence_path) if evidence else None,
                         'prompt': payload.get('prompt', ''), 'input': payload,
                         'signature': signature(request['endpoint'], payload),
                         'hypothesis': request.get('hypothesis'), 'error': result.get('error')})
    return rows


def recommend(rows, use_case, *, has_reference=False, audio=False, min_reviews=1):
    if use_case in {'exact_ui', 'text_ui', 'captions'}:
        return {'endpoint': 'hyperframes', 'status': 'deterministic',
                'reason': 'Exact type and interaction states require authored UI.', 'evidence': []}
    groups = defaultdict(list)
    for row in rows:
        if (row['use_case'] == use_case and row['image_conditioned'] == has_reference
                and row['audio_requested'] == audio and row['verified_output']
                and row['decision'] in {'accept', 'provisional'} and row['legacy_quality'] is not None):
            groups[row['endpoint']].append(row)
    candidates = []
    for endpoint, samples in groups.items():
        # Same endpoint/input repeated in copied artifacts must not inflate support.
        samples = list({s['signature']: s for s in samples}.values())
        if len(samples) < min_reviews:
            continue
        candidates.append({'endpoint': endpoint, 'reviewed_samples': len(samples),
                           'mean_legacy_quality': round(mean(s['legacy_quality'] for s in samples), 2),
                           'evidence': [s['key'] for s in samples]})
    candidates.sort(key=lambda c: (-c['mean_legacy_quality'], -c['reviewed_samples'], c['endpoint']))
    if not candidates:
        return {'endpoint': None, 'status': 'needs_test', 'reason': 'No compatible reviewed output.', 'candidates': []}
    return {**candidates[0], 'status': 'provisional', 'candidates': candidates,
            'reason': 'Within-use-case mean of the same four legacy criteria; scene difficulty and resolution vary. Not a human-realism ranking.'}


def build_learning(artifacts=Path('artifacts')):
    rows = collect_experiments(artifacts)
    routes = []
    for use_case, reference, audio in sorted({(r['use_case'], r['image_conditioned'], r['audio_requested']) for r in rows}):
        routes.append({'use_case': use_case, 'has_reference': reference, 'audio': audio,
                       **recommend(rows, use_case, has_reference=reference, audio=audio)})
    statistics = []
    for endpoint in sorted({r['endpoint'] for r in rows}):
        attempts = [r for r in rows if r['endpoint'] == endpoint]
        completed = [r for r in attempts if r['status'] == 'completed']
        usable = [r for r in attempts if r['verified_output'] and r['decision'] in {'accept', 'provisional'}]
        latencies = [r['elapsed_seconds'] for r in completed if r['elapsed_seconds'] is not None]
        statistics.append({'endpoint': endpoint, 'attempts': len(attempts), 'completed': len(completed),
                           'completion_fraction': len(completed) / len(attempts),
                           'provisionally_usable': len(usable),
                           'mean_success_latency_seconds': round(mean(latencies), 2) if latencies else None,
                           'total_estimate_cents': sum(r['estimate_cents'] for r in attempts),
                           'estimated_cents_per_usable_output': round(sum(r['estimate_cents'] for r in attempts) / len(usable), 2) if usable else None})
    return {'method': 'Actual ledger + decoded media + saved agent reviews. Null means not tested; no missing score is inferred.',
            'dimensions': list(DIMENSIONS), 'runs': rows, 'routes': routes, 'model_statistics': statistics,
            'prompt_memory': [{'key': r['key'], 'endpoint': r['endpoint'], 'use_case': r['use_case'],
                               'signature': r['signature'], 'prompt': r['prompt'],
                               'decision': r['decision'], 'finding': r['review'], 'evidence': r['evidence']}
                              for r in rows if r['review']],
            'needs_review': [r['key'] for r in rows if r['verified_output'] and r['decision'] == 'review_required'],
            'failed_attempts': [r['key'] for r in rows if r['status'] in {'failed_reserved', 'submission_unknown'}]}


def save_learning(artifacts=Path('artifacts')):
    data = build_learning(artifacts)
    target = Path(artifacts) / 'learning'
    target.mkdir(parents=True, exist_ok=True)
    (target / 'latest.json').write_text(json.dumps(data, indent=2) + '\n')
    lines = ['# Cross-loop evidence and routing', '', data['method'], '',
             'Routes are provisional within a use case, reference mode, and audio mode. '
             'These averages are not scientific model rankings. Missing face, hands, and continuity scores remain N/T.', '',
             '| Use case | Reference | Audio | Provisional endpoint | Samples | Legacy mean / 10 |',
             '| --- | --- | --- | --- | ---: | ---: |']
    for row in data['routes']:
        lines.append(f"| {row['use_case']} | {row['has_reference']} | {row['audio']} | {row['endpoint'] or 'Needs test'} | {row.get('reviewed_samples', 0)} | {row.get('mean_legacy_quality', 'N/T')} |")
    lines += ['', f"{len(data['runs'])} recorded attempts; {len(data['needs_review'])} decoded outputs await review; {len(data['failed_attempts'])} failed or uncertain submissions remain reserved.", '',
              'The JSON includes all requested dimensions, prompts, settings, evidence, review notes, costs and latency. Null is never zero.']
    (target / 'latest.md').write_text('\n'.join(lines) + '\n')
    return data
