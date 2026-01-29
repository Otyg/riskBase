import unittest

from src.otyg_risk_base.quantitative_risk import QuantitativeRisk



class TestQuantitativeRisk(unittest.TestCase):
    def test_no_arg(self):
        risk = QuantitativeRisk()
        self.assertIsInstance(risk, QuantitativeRisk)
        for s in ["threat_event_frequency","vulnerability","loss_event_frequency","loss_magnitude","annual_loss_expectancy","budget","currency"]:
            self.assertIn(s, risk.to_dict())

if __name__ == '__main__':
    unittest.main()