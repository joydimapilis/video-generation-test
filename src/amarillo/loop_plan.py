"""Resolve one persistent experiment budget before any upload or paid request."""
from pathlib import Path
import re

from .budget import BudgetLedger
from .learning import requested_audio, signature


def prepare_plan(plan, root=None, cap_cents=1000, *, approved_cap_cents=None):
    # Default remains $10. A larger ceiling requires an explicit caller-supplied
    # approval, never a value embedded in a generation plan.
    maximum = 1000 if approved_cap_cents is None else approved_cap_cents
    if type(maximum) is not int or maximum <= 0:
        raise ValueError('Approved cap must be positive integer cents')
    if type(cap_cents) is not int or not 0 < cap_cents <= maximum:
        raise ValueError(f'The maximum experiment cap is {maximum} cents')
    declared = plan.get('budget_root')
    if root is not None and declared and Path(root).resolve() != Path(declared).resolve():
        raise ValueError('--root conflicts with the plan budget_root; keep the original ledger')
    root = Path(declared or root or 'artifacts/library-loop')
    ledger = BudgetLedger(root / 'budget.json', cap_cents)
    existing = ledger.read()['runs']
    seen = set()
    pending = []
    # External image-generation allowances share the cumulative budget but
    # have no Fal request to deduplicate. Their reservations still count below.
    fingerprints = {signature(r['payload']['endpoint'], r['payload']['input']): key
                    for key, r in existing.items()
                    if 'endpoint' in r['payload'] and 'input' in r['payload']}
    for run in plan['runs']:
        requested_audio(run)  # validate local audio intent before any submission
        identifier = run['id']
        if not isinstance(identifier, str) or not re.fullmatch(r'[A-Za-z0-9_-]+', identifier):
            raise ValueError('Run IDs must be safe filenames')
        if identifier in seen:
            raise ValueError('Duplicate run ID in plan: ' + identifier)
        seen.add(identifier)
        estimate = run['estimate_cents']
        if type(estimate) is not int or estimate <= 0:
            raise ValueError('Estimate must be positive integer cents')
        if identifier in existing:
            if existing[identifier]['payload'] != run or existing[identifier]['estimate_cents'] != estimate:
                raise ValueError('Run ID already bound to a different request')
            continue
        fingerprint = signature(run['endpoint'], run['input'])
        if fingerprint in fingerprints:
            raise ValueError('Identical request already planned or attempted as ' + fingerprints[fingerprint])
        fingerprints[fingerprint] = identifier
        pending.append(run)
    # Preflight the whole batch, rather than discovering an invalid final row after spending.
    reserved = sum(r['reserved_cents'] for r in existing.values())
    additional = sum((r['estimate_cents'] * 115 + 99) // 100 for r in pending)
    if reserved + additional > cap_cents:
        raise ValueError('Cumulative budget exceeded; entire plan blocked before submission')
    return root, ledger, {'new_requests': len(pending), 'new_estimate_cents': sum(
        r['estimate_cents'] for r in pending), 'reserved_after_cents': reserved + additional,
        'cap_cents': cap_cents}
