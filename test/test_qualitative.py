import unittest

from src.otyg_risk_base.qualitative_risk import QualitativeRisk



class TestQuantitativeRisk(unittest.TestCase):
    def test_output(self):
        risk = QualitativeRisk()
        expected = {'risk': "Very Low", 'likelihood': "Very Low", 'impact': "Very Low"}
        self.assertEqual(risk.get(), expected)
        risk = QualitativeRisk(likelihood_init=3, likelihood_impact=3, impact=5)
        expected = {'risk': "High", 'likelihood': "Moderate", 'impact': "Very High"}
        self.assertEqual(risk.get(), expected)

if __name__ == '__main__':
    unittest.main()