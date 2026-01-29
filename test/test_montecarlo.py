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
    
    def test_equals(self):
        actual = MonteCarloRange(min= 0, probable=1, max=2)
        other = MonteCarloRange(min= 0, probable=1, max=2)
        other_neq = MonteCarloRange(min= 1, probable=2, max=3)
        self.assertTrue(actual == actual)
        self.assertTrue(actual == other)
        self.assertFalse(actual == other_neq)
        self.assertFalse(actual == 1)

    def test_add(self):
        actual = MonteCarloRange(min= 0, probable=1, max=2).add(MonteCarloRange(min= 1, probable=2, max=3))
        expected = MonteCarloRange(min= 1, probable=3, max=5)
        actual_scalar = MonteCarloRange(min= 0, probable=1, max=2).add(1)
        expected_scalar = MonteCarloRange(min= 1, probable=2, max=3)
        not_expected = MonteCarloRange(min= 2, probable=3, max=5)
        self.assertTrue(actual == expected)
        self.assertTrue(actual_scalar == expected_scalar)
        self.assertFalse(actual == not_expected)

        

if __name__ == '__main__':
    unittest.main()