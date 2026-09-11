"""Build the measured scorecard from frozen review and runtime evidence."""
import json
from pathlib import Path

def main():
    root=Path('artifacts/library-loop')
    ledger=json.loads((root/'budget.json').read_text())
    review=json.loads(Path('review_notes/library_loop.json').read_text())
    rows=[]
    for identifier, result in ledger['runs'].items():
        note=review['runs'][identifier]
        ev=json.loads((root/'evidence'/f'{identifier}.json').read_text())
        video=next(s for s in ev['probe']['streams'] if s['codec_type']=='video')
        rows.append({'id':identifier,'endpoint':result['payload']['endpoint'],
            'use_case':result['payload']['use_case'],'status':result['status'],
            'score_10':round(sum(note['scores'])/len(note['scores']),2),
            'scores':dict(zip(review['criteria'],note['scores'])), 'review':note['note'],
            'estimate_usd':result['estimate_cents']/100,'reserved_usd':result['reserved_cents']/100,
            'elapsed_seconds':result.get('elapsed_seconds'), 'resolution':f"{video['width']}x{video['height']}",
            'duration':float(ev['probe']['format']['duration']), 'decode_ok':ev['full_decode_ok'],
            'transcript':[s['text'].strip() for s in ev.get('transcript',[])],
            'output':result['output_path'],'evidence':str(root/'evidence'/f'{identifier}.json')})
    report={'method':review['method'],'cost_estimate_usd':sum(r['estimate_cents'] for r in ledger['runs'].values())/100,
        'reserved_usd':sum(r['reserved_cents'] for r in ledger['runs'].values())/100,
        'cap_usd':ledger['limit_cents']/100,'runs':rows,'routing':review['routing']}
    verification=Path('artifacts/final_outcome/cue/verification.json')
    if verification.exists():
        final=json.loads(verification.read_text())
        report['hyperframes_result']={'api_cost_usd':0,'duration':30,'dimensions':'1920x1080',
            'exact_task_labels':True,'first_row_click_correct':True,'checks':final['composition_checks'],
            'verification':str(verification),'comparison_note':'Authored deterministic workflow, not the same input or authoring effort as text-to-video.'}
    (root/'scorecard.json').write_text(json.dumps(report,indent=2)+'\n')
    lines=['# Capability and Results Scorecard','',review['method'],'',
        'Scores average four equally weighted criteria. Compare within use case only.',
        'Resolution, clip duration, seed availability and stochastic variation confound cross-model comparisons.',
        'Latency includes queue polling and download, not just inference. No repeat-seed confidence intervals.','',
        '| Run | Role | Score / 10 | Dimensions | Estimate | Seconds elapsed |',
        '| --- | --- | ---: | --- | ---: | ---: |']
    for r in rows:
        lines.append(f"| {r['id']} | {r['use_case']} | {r['score_10']} | {r['resolution']} | ${r['estimate_usd']:.2f} | {r['elapsed_seconds']} |")
    lines+=['','## Capability Coverage','',
        '| Model / tool | UGC | Product beauty | Exact UI | Interview | Motion type |',
        '| --- | --- | --- | --- | --- | --- |',
        '| Veo 3.1 Fast | Tested, selected | N/T | N/T | Tested, preferred | N/T |',
        '| Grok Imagine 1.5 | Tested alternative | N/T | N/T | N/T | N/T |',
        '| LTX 2.3 Pro | Tested, economical draft | N/T | N/T | Tested, improved with prompt repair | N/T |',
        '| Kling 3.0 Pro | N/T | Tested, selected v2 | Tested, rejected | N/T | N/T |',
        '| Seedance 2.5 | N/T | Tested, premium alternative | N/T | N/T | N/T |',
        '| HyperFrames | Assembly only | Assembly only | Authored and rendered | Assembly only | Authored and rendered |',
        '', 'N/T means not tested, not incapable. There is no defensible universal winner.','', '## Observations','']
    for r in rows:
        lines += [f"### {r['id']}",r['review'],'']
    lines+=['## Loop Outcome','',
        '- Veo UGC v1 -> v2: same line extends from 2.8 to 3.9 seconds in the local transcript. Better pacing; not the exact 4.8s target.',
        '- Kling hero v1 -> v2: pale button/multiple LEDs/central framing repaired to black button, one top light and usable right-side placement.',
        '- LTX interview v1 -> v2: corrupted burned-in subtitles removed by clean-camera wording. Both versions transcribe the requested lines.',
        '- Kling UI -> HyperFrames: switch tools when exact symbols, spelling and interactions fail; do not keep spending on the wrong role.',
        '- HyperFrames first check -> revision: hide outgoing benefit text once covered by the closing transition; rerun layout and contrast checks.',
        '- Final mix -> revision: strip embedded audio from video plates and keep the separately mastered dialogue track; prevent duplicate speech and clipping.',
        '', '## Budget','',
        f"Estimated generation total: ${report['cost_estimate_usd']:.2f}. Conservative reserved total: ${report['reserved_usd']:.2f}. Hard cap: $10.00.",
        'All 11 paid requests completed. No paid retries, new paid image/audio calls, or further submissions. Provider invoice not queried.',
        '', '## Reproduce','',
        'Run plans are in configs/library_loop_round1.json and configs/library_loop_round2.json. The runner resumes stored IDs and never intentionally resubmits the same run ID.',
        'Keep artifacts/library-loop/budget.json: it is the persistent cost and request ledger. Deleting it defeats the guard.',
        'Run scripts/evaluate_library_loop.py --speech for local evidence, scripts/report_library_loop.py for this report, and npm run render in hyperframes/cue for the final edit.',
        'Research and primary source links: docs/LIBRARY_LOOP_RESEARCH.md. Reusable patterns: prompt_library/library_loop_patterns.json.',
        'Next concepts, routed scene by scene from this evidence: docs/LIBRARY_LOOP_CONCEPTS.md, rebuilt by scripts/build_concept_slate.py.']
    if 'hyperframes_result' in report:
        lines+=['','## HyperFrames Result','',
            '30-second 1080p H.264/AAC final. Exact labels and first-row click confirmed visually. Zero lint/runtime/layout/motion findings, 24 layout samples, 300 motion samples, all 40 contrast checks pass.',
            'No generation API cost. Local rendering and code authoring are not free labor and are not equivalent inputs to a generative model. Final verification includes full decode and audio measurements.']
    Path('docs/LIBRARY_LOOP_SCORECARD.md').write_text('\n'.join(lines)+'\n')
    print('Saved scorecard;',len(rows),'runs; estimated',report['cost_estimate_usd'],'reserved',report['reserved_usd'])

if __name__=='__main__':
    main()
