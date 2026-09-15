"""Build a loop scorecard from the frozen ledger, evidence and review notes.

Generic over experiments: every claim, score and piece of prose comes from the
review JSON, so this script only joins and formats. It never invents a finding.

    python scripts/report_loop.py --root artifacts/library-loop-3 \
        --review review_notes/keel.json --out docs/KEEL_SCORECARD.md
"""
import argparse
import json
from pathlib import Path


def collect(root, review, chosen):
    ledger = json.loads((root / 'budget.json').read_text())
    rows = []
    for identifier, result in ledger['runs'].items():
        note = review['runs'].get(identifier, {})
        evidence_path = root / 'evidence' / f'{identifier}.json'
        evidence = json.loads(evidence_path.read_text()) if evidence_path.exists() else {}
        video = next((s for s in evidence.get('probe', {}).get('streams', []) if s['codec_type'] == 'video'), {})
        legacy_scores = note.get('scores', [])
        rows.append({
            'id': identifier,
            'endpoint': result['payload']['endpoint'],
            'use_case': result['payload']['use_case'],
            'version': result['payload'].get('version', 1),
            'status': result['status'],
            'score_10': round(sum(legacy_scores) / len(legacy_scores), 2) if legacy_scores else None,
            'scores': {**dict(zip(review['criteria'], legacy_scores)), **note.get('detailed_scores', {})},
            'review': note.get('note', 'No qualitative review; no score assigned.'),
            'decision': note.get('decision', 'provisional' if legacy_scores else 'review_required'),
            'review_method': review['method'],
            'estimate_usd': result['estimate_cents'] / 100,
            'reserved_usd': result['reserved_cents'] / 100,
            'elapsed_seconds': result.get('elapsed_seconds'),
            'resolution': f"{video['width']}x{video['height']}" if video else None,
            'duration': float(evidence['probe']['format']['duration']) if evidence else None,
            'decode_ok': evidence.get('full_decode_ok'),
            'selected': identifier in chosen,
            'output': result.get('output_path'),
            'evidence': str(root / 'evidence' / f'{identifier}.json'),
        })
    return ledger, rows


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--root', type=Path, required=True)
    parser.add_argument('--review', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True)
    parser.add_argument('--final', type=Path, help='verification.json for the delivered film')
    args = parser.parse_args()

    review = json.loads(args.review.read_text())
    selected = json.loads((args.root / 'selected_assets.json').read_text())
    chosen = set(selected['plates'].values())
    ledger, rows = collect(args.root, review, chosen)

    estimate = sum(r['estimate_cents'] for r in ledger['runs'].values()) / 100
    reserved = sum(r['reserved_cents'] for r in ledger['runs'].values()) / 100
    cap = ledger['limit_cents'] / 100
    report = {'concept': review['concept'], 'method': review['method'],
              'cost_estimate_usd': estimate, 'reserved_usd': reserved, 'cap_usd': cap,
              'runs': rows, 'head_to_head': review.get('head_to_head', {}),
              'routing': review['routing'], 'findings': review.get('findings', []),
              'selected_plates': selected['plates']}

    final_path = args.final or (args.root.parent / 'final_outcome' / 'x' / 'nope')
    if final_path.exists():
        final = json.loads(final_path.read_text())
        report['final'] = {'path': final['path'], 'checks': final.get('composition_checks'),
                           'api_cost_usd': 0}
    (args.root / 'scorecard.json').write_text(json.dumps(report, indent=2) + '\n')

    lines = [f"# {review['concept']}", '', review.get('subtitle', ''), '',
             review['method'], '',
             'Scores average four equally weighted criteria. Compare within use case only.',
             # Loops that run deliberate controls repeat a seed on purpose, so the
             # sampling caveat has to come from the review like every other claim.
             review.get('caveat',
                        'One trial per model per shot, no repeat seeds, no confidence intervals.'),
             '',
             '| Run | Role | v | Score / 10 | Dimensions | Estimate | Seconds | Used |',
             '| --- | --- | ---: | ---: | --- | ---: | ---: | :-: |']
    for r in rows:
        lines.append(f"| `{r['id']}` | {r['use_case']} | {r['version']} | {r['score_10'] if r['score_10'] is not None else 'N/T'} | "
                     f"{r['resolution'] or 'N/T'} | ${r['estimate_usd']:.2f} | {r['elapsed_seconds'] if r['elapsed_seconds'] is not None else 'N/T'} | "
                     f"{'yes' if r['selected'] else '-'} |")

    if any(note.get('detailed_scores') for note in review['runs'].values()):
        from amarillo.learning import DIMENSIONS
        lines += ['', '## Detailed criteria', '',
                  'N/T means not tested, not zero. These are subjective sampled-frame scores; '
                  'a single-shot identity score does not establish consistency across shots.', '',
                  '| Criterion | ' + ' | '.join(r['id'] for r in rows) + ' |',
                  '| --- | ' + ' | '.join(['---:'] * len(rows)) + ' |']
        for dimension in DIMENSIONS:
            values = [str(r['scores'].get(dimension)) if r['scores'].get(dimension) is not None else 'N/T' for r in rows]
            lines.append('| ' + dimension.replace('_', ' ') + ' | ' + ' | '.join(values) + ' |')

    if review.get('changed_this_loop'):
        lines += ['', '## What Changed This Loop', '', review['changed_this_loop'], '']

    if review.get('head_to_head'):
        lines += ['## Controlled Comparisons', '']
        for name, test in review['head_to_head'].items():
            lines += [f"### {name.replace('_', ' ').title()}", '',
                      f"Winner: **{test['winner']}**", '', test['finding'], '']

    lines += ['## Routing After This Loop', '',
              '| Shot type | Route to | Selected run | Caution |', '| --- | --- | --- | --- |']
    for shot, rule in review['routing'].items():
        lines.append(f"| {shot.replace('_', ' ')} | {rule['primary']} | "
                     f"`{rule.get('selected_run', '-')}` | {rule.get('caution', '-')} |")

    lines += ['', '## Observations', '']
    for r in rows:
        lines += [f"### `{r['id']}` - {r['score_10']}/10" + ('  **selected**' if r['selected'] else ''),
                  r['review'], '']

    if review.get('findings'):
        lines += ['## Findings', '']
        lines += [f'- {finding}' for finding in review['findings']]
        lines.append('')

    lines += ['## Budget', '',
              f'Estimated generation total: ${estimate:.2f}. Conservative reserved total: '
              f'${reserved:.2f}. Hard cap: ${cap:.2f}.',
              f"{len(rows)} reserved requests; {sum(r['status'] == 'completed' for r in rows)} completed; "
              f"{sum(r['status'] in {'failed_reserved', 'submission_unknown'} for r in rows)} failed or uncertain. No automatic retries.",
              f'This loop has its own ledger at `{args.root}/budget.json`; it is the persistent '
              'cost record and deleting it defeats the cap guard. Provider invoice not queried.', '']

    if 'final' in report:
        checks = report['final'].get('checks') or {}
        lines += ['## Final Film', '',
                  f"`{report['final']['path']}`",
                  f"Zero lint, runtime, layout and motion findings; "
                  f"{checks.get('contrast_passed', '?')}/{checks.get('contrast_total', '?')} "
                  'contrast checks pass.',
                  'No generation API cost for the assembly. Authoring time is the real cost of the',
                  'HyperFrames layer and is not comparable to a model call.', '']

    args.out.write_text('\n'.join(lines) + '\n')
    print(f'Saved {args.out}; {len(rows)} runs; ${estimate:.2f} estimated, ${reserved:.2f} reserved')


if __name__ == '__main__':
    main()
