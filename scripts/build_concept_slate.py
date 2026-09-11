"""Render the concept slate document and check it against measured evidence.

Costs printed here are estimates from published per-second pricing. Nothing in
the slate has been generated, so no ledger reservation is made or implied.
"""
import json
import math
from pathlib import Path

SLATE = Path('prompt_library/concept_slate.json')
PATTERNS = Path('prompt_library/library_loop_patterns.json')
LEDGER = Path('artifacts/library-loop/budget.json')
OUT = Path('docs/LIBRARY_LOOP_CONCEPTS.md')


def scene_cost(slate, scene):
    rate = slate['rates_usd_per_second'][scene['tool']]
    # Providers bill whole seconds; round up the way the runner reserves.
    return math.ceil(scene['seconds_billed']) * rate


def validate(slate):
    known = {p['id'] for p in json.loads(PATTERNS.read_text())['patterns']}
    problems = []
    for concept in slate['concepts']:
        covered = 0
        for scene in concept['scenes']:
            if scene['pattern_id'] not in known:
                problems.append(f"{concept['id']}/{scene['index']}: unknown pattern {scene['pattern_id']}")
            if scene['tool'] not in slate['rates_usd_per_second']:
                problems.append(f"{concept['id']}/{scene['index']}: unpriced tool {scene['tool']}")
            start, end = (float(x) for x in scene['time'].split('-'))
            if start != covered:
                problems.append(f"{concept['id']}/{scene['index']}: starts at {start}, previous scene ended at {covered}")
            covered = end
        if covered != concept['duration_seconds']:
            problems.append(f"{concept['id']}: scenes cover {covered}s, stated duration {concept['duration_seconds']}s")
    return problems


def remaining_budget():
    if not LEDGER.exists():
        return None
    data = json.loads(LEDGER.read_text())
    reserved = sum(run['reserved_cents'] for run in data['runs'].values())
    return (data['limit_cents'] - reserved) / 100


def main():
    slate = json.loads(SLATE.read_text())
    problems = validate(slate)
    if problems:
        raise SystemExit('Slate is inconsistent:\n' + '\n'.join(problems))

    headroom = remaining_budget()
    lines = ['# Concept Slate: New Video Ideas and Per-Scene Routing', '',
             slate['note'], '',
             'Every concept below is derived from the inspected library references and routed',
             'scene by scene to whichever tool measurably handled that role best in the loop.',
             'Scene prompts instantiate the templates in `prompt_library/library_loop_patterns.json`',
             'and already carry the round-2 repairs: explicit feature counts for product shots,',
             'raw-camera wording to suppress burned-in subtitles, and a speech budget longer than',
             'the line actually needs.', '']

    if headroom is not None:
        lines += [f'Remaining headroom under the $10 cap is **${headroom:.2f}**. No concept in this',
                  'slate fits that, so none has been generated. Running one requires a new,',
                  'explicitly approved budget.', '']

    lines += ['## Routing Rules', '',
              '| Shot type | Route to | Fallback | Evidence | Caution |',
              '| --- | --- | --- | --- | --- |']
    for rule in slate['routing_rules']:
        fallback = rule.get('fallback') or rule.get('premium_alternative') or rule.get('budget_draft') or '--'
        lines.append(f"| {rule['shot_type']} | `{rule['tool']}` | `{fallback}` | {rule['evidence']} | {rule['caution']} |")

    totals = []
    for concept in slate['concepts']:
        cost = sum(scene_cost(slate, scene) for scene in concept['scenes'])
        paid = sum(1 for scene in concept['scenes'] if scene_cost(slate, scene) > 0)
        totals.append((concept, cost, paid))

    lines += ['', '## Slate at a Glance', '',
              '| Concept | Use case | Length | Paid shots | Estimated generation cost |',
              '| --- | --- | ---: | ---: | ---: |']
    for concept, cost, paid in sorted(totals, key=lambda row: row[1]):
        lines.append(f"| {concept['title']} | {concept['use_case']} | {concept['duration_seconds']}s | "
                     f"{paid} | ${cost:.2f} |")
    lines += ['', f'Whole slate if every concept were produced once: '
                  f'**${sum(cost for _, cost, _ in totals):.2f}** estimated, excluding retries.',
              'Measured retry rate in the loop was 4 repairs across 11 requests, so plan for more.', '']

    for concept, cost, _ in totals:
        lines += [f"## {concept['title']}", '',
                  f"- Use case: `{concept['use_case']}`",
                  f"- Length: {concept['duration_seconds']}s",
                  f"- Library references: {', '.join(concept['library_references'])}",
                  f"- Estimated generation cost: ${cost:.2f}", '',
                  concept['premise'], '',
                  f"**Why this routing.** {concept['why_this_routing']}", '',
                  '| # | Time | Role | Tool | Pattern | Est. |',
                  '| ---: | --- | --- | --- | --- | ---: |']
        for scene in concept['scenes']:
            lines.append(f"| {scene['index']} | {scene['time']}s | {scene['role']} | `{scene['tool']}` | "
                         f"`{scene['pattern_id']}` | ${scene_cost(slate, scene):.2f} |")
        lines.append('')
        for scene in concept['scenes']:
            lines += [f"### Scene {scene['index']} — {scene['time']}s, `{scene['tool']}`", '',
                      '```text', scene['prompt'], '```', '',
                      f"Accept when: {scene['acceptance']}", '']
        if concept.get('known_risk'):
            lines += [f"**Known risk.** {concept['known_risk']}", '']

    lines += ['## How to Produce One', '',
              '1. Copy the concept into a run plan shaped like `configs/library_loop_round2.json`,',
              '   one entry per paid scene, with `estimate_cents` computed from the rate table above.',
              '2. Raise the cap deliberately. `BudgetLedger` refuses to change the limit on an existing',
              '   ledger, so a larger run needs its own ledger file and its own approval.',
              '3. `python scripts/run_library_loop.py <plan>` submits once per reserved run and resumes',
              '   persisted queue IDs instead of resubmitting.',
              '4. `python scripts/evaluate_library_loop.py --speech` freezes frames, probes and transcripts.',
              '5. Check each scene against its stated acceptance line before assembling anything.',
              '6. Author every legible element in HyperFrames, then render and verify the full decode.', '',
              '## Limits', '',
              'The routing rules come from one trial per model per role, without repeat seeds or',
              'confidence intervals. They describe what happened here, not a general model ranking.',
              'Untested pairings stay untested: nothing below claims a model cannot do a job it was',
              'never asked to do. All four concepts are fictional products; none is a customer claim.', '']

    OUT.write_text('\n'.join(lines) + '\n')
    summary = (f'Saved {OUT}; {len(slate["concepts"])} concepts; '
               f'${sum(cost for _, cost, _ in totals):.2f} estimated if all produced')
    if headroom is not None:
        summary += f'; ${headroom:.2f} headroom left under the existing cap'
    print(summary)


if __name__ == '__main__':
    main()
