"""One POST per reserved run; resume persisted queue jobs without resubmitting."""
import argparse
import json
import os
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

from amarillo.budget import BudgetLedger



def request(url, payload=None, auth=True):
    headers = {'Content-Type': 'application/json'}
    if auth:
        if urllib.parse.urlparse(url).hostname not in {'queue.fal.run', 'api.fal.ai'}:
            raise ValueError('Refusing to send credentials to an unexpected host')
        headers['Authorization'] = 'Key ' + os.environ['FAL_KEY']
    req = urllib.request.Request(url, data=None if payload is None else json.dumps(payload).encode(), headers=headers)
    with urllib.request.urlopen(req, timeout=60) as result:
        return json.load(result)


def resolve_local_images(payload):
    """Upload any local image referenced by the payload and swap in the URL.

    An image-to-video run names a file on disk; Fal needs a URL. Uploading here
    keeps the run plan readable and keeps the uploaded URL out of version control.
    """
    for field in ('image_url', 'start_image_url', 'end_image_url'):
        value = payload.get(field)
        if not value or not str(value).startswith('local:'):
            continue
        path = Path(str(value)[len('local:'):])
        if not path.exists():
            raise SystemExit(f'Missing local image for {field}: {path}')
        import fal_client
        payload[field] = fal_client.upload_file(path)
    return payload


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('plan', type=Path)
    parser.add_argument('--root', type=Path, default=Path('artifacts/library-loop'),
                        help='Experiment directory holding budget.json and outputs/.')
    parser.add_argument('--cap-cents', type=int, default=1000,
                        help='Hard cap for this experiment. An existing ledger refuses to change it.')
    args = parser.parse_args()
    root = args.root
    plan = json.loads(args.plan.read_text())
    ledger = BudgetLedger(root / 'budget.json', args.cap_cents)
    (root / 'outputs').mkdir(parents=True, exist_ok=True)
    # Submit sequentially and persist each ID before the next submission.
    for run in plan['runs']:
        identifier = run['id']
        if not ledger.reserve(identifier, run['estimate_cents'], run):
            continue
        try:
            queue = request('https://queue.fal.run/' + run['endpoint'], resolve_local_images(run['input']))
            ledger.update(identifier, status='submitted', queue=queue, submitted_at=time.time())
            print(identifier, 'submitted', queue['request_id'], flush=True)
        except Exception as error:
            # A timeout can still incur a charge. Never release or retry automatically.
            ledger.update(identifier, status='submission_unknown', error=str(error))
            print(identifier, 'submission_unknown', str(error), flush=True)
    pending = {r['id'] for r in plan['runs'] if ledger.read()['runs'][r['id']]['status'] in {'submitted', 'running'}}
    while pending:
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
    # Downloads can be resumed without another paid generation.
    for identifier, row in ledger.read()['runs'].items():
        if row['status'] == 'generated':
            path = root / 'outputs' / f'{identifier}.mp4'
            urllib.request.urlretrieve(row['result']['video']['url'], path)
            ledger.update(identifier, status='completed', output_path=str(path))
    data = ledger.read()
    print('Estimated cents:', sum(r['estimate_cents'] for r in data['runs'].values()))
    print('Reserved cents:', sum(r['reserved_cents'] for r in data['runs'].values()))


if __name__ == '__main__':
    main()
