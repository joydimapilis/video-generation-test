"""Crash-safe cumulative reservations for one explicitly bounded experiment."""
import fcntl
import json
import math
import os
from contextlib import contextmanager
from pathlib import Path


class BudgetLedger:
    def __init__(self, path: Path, limit_cents: int = 1000):
        if type(limit_cents) is not int or limit_cents <= 0:
            raise ValueError('Limit must be positive integer cents')
        self.path = Path(path)
        self.limit = limit_cents

    @contextmanager
    def locked(self):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.with_suffix('.lock').open('a') as lock:
            fcntl.flock(lock, fcntl.LOCK_EX)
            data = json.loads(self.path.read_text()) if self.path.exists() else {
                'limit_cents': self.limit, 'runs': {}}
            if data['limit_cents'] != self.limit:
                raise ValueError('Cannot change the existing budget limit')
            yield data
            tmp = self.path.with_suffix('.tmp')
            with tmp.open('w') as output:
                json.dump(data, output, indent=2, allow_nan=False)
                output.flush()
                os.fsync(output.fileno())
            os.replace(tmp, self.path)

    def reserve(self, run_id, estimate_cents, payload):
        if type(estimate_cents) is not int or estimate_cents <= 0:
            raise ValueError('Estimate must be positive integer cents')
        # Keep 15% extra for frame rounding and quoted-price uncertainty.
        reserved = math.ceil(estimate_cents * 115 / 100)
        with self.locked() as data:
            if run_id in data['runs']:
                old = data['runs'][run_id]
                if old['payload'] != payload or old['estimate_cents'] != estimate_cents:
                    raise ValueError('Run ID already bound to a different request')
                return False
            if sum(r['reserved_cents'] for r in data['runs'].values()) + reserved > self.limit:
                raise ValueError('Cumulative budget exceeded; request blocked before submission')
            data['runs'][run_id] = {'estimate_cents': estimate_cents, 'reserved_cents': reserved,
                                    'payload': payload, 'status': 'reserved'}
        return True

    def update(self, run_id, **fields):
        protected = {'estimate_cents', 'reserved_cents', 'payload'}
        if protected.intersection(fields):
            raise ValueError('Reservations and requests are immutable')
        with self.locked() as data:
            data['runs'][run_id].update(fields)

    def read(self):
        with self.locked() as data:
            return data
