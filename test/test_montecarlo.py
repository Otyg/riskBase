from decimal import Decimal
import unittest

from src.otyg_risk_base.montecarlo import MonteCarloRange



class TestMonteCarloRange(unittest.TestCase):
    def test_no_arg(self):
        mr = MonteCarloRange()
        self.assertEqual(mr.probable, Decimal(0))
    def test_probable_less_than_min(self):
        with self.assertRaises(ValueError):
            mc = MonteCarloRange(min= 1, probable=0, max=2)
        

if __name__ == '__main__':
    unittest.main()