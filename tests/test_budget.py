import tempfile
import unittest
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from amarillo.budget import BudgetLedger


class BudgetTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.path = Path(self.temp.name) / 'budget.json'
        self.ledger = BudgetLedger(self.path)

    def test_cap_includes_buffer_and_failed_runs(self):
        self.ledger.reserve('a', 800, {})
        self.ledger.update('a', status='failed_reserved')
        with self.assertRaises(ValueError):
            self.ledger.reserve('b', 100, {})
        self.assertEqual(set(self.ledger.read()['runs']), {'a'})

    def test_resume_is_idempotent(self):
        self.assertTrue(self.ledger.reserve('a', 100, {'prompt': 'x'}))
        self.assertFalse(BudgetLedger(self.path).reserve('a', 100, {'prompt': 'x'}))
        with self.assertRaises(ValueError):
            self.ledger.reserve('a', 100, {'prompt': 'y'})

    def test_rejects_invalid_money_and_limit_changes(self):
        for value in [-1, 0, float('nan'), True, 1.5]:
            with self.assertRaises(ValueError):
                self.ledger.reserve('a', value, {})
        self.ledger.reserve('a', 100, {})
        with self.assertRaises(ValueError):
            BudgetLedger(self.path, 2000).read()

    def test_reservation_cannot_be_released(self):
        self.ledger.reserve('a', 100, {})
        with self.assertRaises(ValueError):
            self.ledger.update('a', reserved_cents=0)

    def test_interrupted_reservation_is_still_counted(self):
        self.ledger.reserve('a', 800, {'endpoint': 'unknown'})
        resumed=BudgetLedger(self.path)
        self.assertFalse(resumed.reserve('a', 800, {'endpoint': 'unknown'}))
        with self.assertRaises(ValueError):
            resumed.reserve('b', 100, {})

    def test_concurrent_reservations_cannot_overspend(self):
        def reserve(identifier):
            try:
                return BudgetLedger(self.path).reserve(identifier, 500, {})
            except ValueError:
                return False
        with ThreadPoolExecutor(max_workers=2) as pool:
            results=list(pool.map(reserve, ['a','b']))
        self.assertEqual(results.count(True),1)
        self.assertEqual(sum(r['reserved_cents'] for r in self.ledger.read()['runs'].values()),575)


if __name__ == '__main__':
    unittest.main()
