"""One POST per reserved run; resume persisted queue jobs without resubmitting."""
import argparse
import json
import os
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

from amarillo.budget import BudgetLedger
from amarillo.references import resolve_local_images
from amarillo.loop_plan import prepare_plan
from amarillo.learning import requested_audio



def request(url, payload=None, auth=True):
    headers = {'Content-Type': 'application/json'}
    if auth:
        if urllib.parse.urlparse(url).hostname not in {'queue.fal.run', 'api.fal.ai'}:
            raise ValueError('Refusing to send credentials to an unexpected host')
        headers['Authorization'] = 'Key ' + os.environ['FAL_KEY']
    req = urllib.request.Request(url, data=None if payload is None else json.dumps(payload).encode(), headers=headers)
    with urllib.request.urlopen(req, timeout=60) as result:
        return json.load(result)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('plan', type=Path)
    parser.add_argument('--root', type=Path,
                        help='Experiment directory holding budget.json and outputs/.')
    parser.add_argument('--cap-cents', type=int, default=1000,
                        help='Hard cap for this experiment. An existing ledger refuses to change it.')
    parser.add_argument('--approved-cap-cents', type=int,
                        help='Explicit user-approved ceiling above the default $10; does not reset or change a ledger.')
    parser.add_argument('--dry-run', action='store_true', help='Validate budget without uploads or generation.')
    parser.add_argument('--poll-timeout', type=float, default=1200,
                        help='Seconds to poll before returning; resume with the same plan.')
    parser.add_argument('--evaluate', action='store_true',
                        help='Extract local technical/speech evidence and refresh cross-loop learning afterward.')
    args = parser.parse_args()
    plan = json.loads(args.plan.read_text())
    root, ledger, summary = prepare_plan(plan, args.root, args.cap_cents,
                                         approved_cap_cents=args.approved_cap_cents)
    print(json.dumps(summary), flush=True)
    if args.dry_run:
        return
    if not os.environ.get('FAL_KEY') and summary['new_requests']:
        raise SystemExit('FAL_KEY is required; no requests reserved or submitted')
    (root / 'outputs').mkdir(parents=True, exist_ok=True)
    # Submit sequentially and persist each ID before the next submission.
    for run in plan['runs']:
        identifier = run['id']
        if not ledger.reserve(identifier, run['estimate_cents'], run):
            continue
        try:
            resolved = resolve_local_images(run['input'])
            ledger.update(identifier, resolved_input=resolved)
            queue = request('https://queue.fal.run/' + run['endpoint'], resolved)
            ledger.update(identifier, status='submitted', queue=queue, submitted_at=time.time())
            print(identifier, 'submitted', queue['request_id'], flush=True)
        except Exception as error:
            # A timeout can still incur a charge. Never release or retry automatically.
            ledger.update(identifier, status='submission_unknown', error=str(error))
            print(identifier, 'submission_unknown', str(error), flush=True)
    pending = {r['id'] for r in plan['runs'] if ledger.read()['runs'][r['id']]['status'] in {'submitted', 'running'}}
    deadline = time.monotonic() + args.poll_timeout
    while pending and time.monotonic() < deadline:
        for identifier in sorted(pending):
            row = ledger.read()['runs'][identifier]
            try:
                status = request(row['queue']['status_url'])
                if status['status'] != 'COMPLETED':
                    ledger.update(identifier, status='running', queue_status=status['status'])
                    continue
                result = request(row['queue']['response_url'])
                ledger.update(identifier, result=result, status='generated')
                path = root / 'outputs' / f'{identifier}.mp4'
                urllib.request.urlretrieve(result['video']['url'], path)
                ledger.update(identifier, status='completed', output_path=str(path),
                              elapsed_seconds=round(time.time() - row['submitted_at'], 2))
                pending.remove(identifier)
                print(identifier, 'completed', path, flush=True)
            except urllib.error.HTTPError as error:
                if error.code in {400, 401, 403, 404, 422}:
                    ledger.update(identifier, status='failed_reserved', error=error.read().decode()[:2000])
                    pending.remove(identifier)
                    print(identifier, 'failed_reserved', error.code, flush=True)
                else:
                    print(identifier, 'transient poll error', error.code, flush=True)
            except Exception as error:
                print(identifier, 'poll/download error', str(error), flush=True)
        if pending:
            print('Pending:', ', '.join(sorted(pending)), flush=True)
            time.sleep(15)
    if pending:
        print('Polling paused. Resume this same plan to retrieve pending jobs without paying again.', flush=True)
    # Downloads can be resumed without another paid generation.
    for identifier, row in ledger.read()['runs'].items():
        if row['status'] == 'generated':
            path = root / 'outputs' / f'{identifier}.mp4'
            urllib.request.urlretrieve(row['result']['video']['url'], path)
            ledger.update(identifier, status='completed', output_path=str(path))
    data = ledger.read()
    print('Estimated cents:', sum(r['estimate_cents'] for r in data['runs'].values()))
    print('Reserved cents:', sum(r['reserved_cents'] for r in data['runs'].values()))
    if args.evaluate:
        speech_ids = [r['id'] for r in plan['runs'] if requested_audio(r)]
        command = [sys.executable, str(Path(__file__).with_name('evaluate_library_loop.py')), '--root', str(root)]
        if speech_ids:
            command += ['--speech', '--speech-match', ','.join(speech_ids)]
        subprocess.run(command, check=True)
        from amarillo.learning import save_learning
        learning = save_learning(root.parent)
        print('Learning refreshed; outputs needing qualitative review:', len(learning['needs_review']))


if __name__ == '__main__':
    main()
