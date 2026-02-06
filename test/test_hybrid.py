from decimal import Decimal
import unittest

from src.otyg_risk_base.montecarlo import MonteCarloRange
from src.otyg_risk_base.hybrid import HybridRisk

class TestHybridRisk(unittest.TestCase):
    def test_set_qualitative(self):
        risk = HybridRisk({'threat_event_frequency': {'min':0,'probable':1,'max':2}, 'vulnerability': {'min':0,'probable':2,'max':3}, 'loss_magnitude':{'min':1,'probable':2,'max':3}, 'budget': 10000, 'currency':"SEK"})
        self.assertEqual(risk.qualitative.overall_risk, "Very High")
        self.assertEqual(risk.qualitative.overall_likelihood, "High")
        self.assertEqual(risk.qualitative.impact, "Very High")
    
    def test_equality(self):
        risk = HybridRisk({'threat_event_frequency': {'min':0,'probable':1,'max':2}, 'vulnerability': {'min':1,'probable':2,'max':3}, 'loss_magnitude':{'min':3,'probable':4,'max':5}, 'budget': 10000, 'currency':"SEK"})
        self.assertTrue(risk == risk)
        risk_mod = HybridRisk({'threat_event_frequency': {'min':1,'probable':3,'max':5}, 'vulnerability': {'min':1,'probable':2,'max':3}, 'loss_magnitude':{'min':3,'probable':4,'max':5}, 'budget': 10000, 'currency':"SEK"})
        self.assertFalse(risk == risk_mod)
    
    def test_serialization_deserialization(self):
        risk = HybridRisk({'threat_event_frequency': MonteCarloRange(min=0, probable=1, max=2), 'vulnerability':  MonteCarloRange(min=1, probable=2, max=3), 'loss_magnitude': MonteCarloRange(min=4, probable=5, max=6), 'budget': 10000, 'currency':"SEK"})
        risk_new = HybridRisk.from_dict(risk.to_dict())
        self.assertTrue(risk == risk_new)
        risk = HybridRisk({'threat_event_frequency': {'min':0,'probable':1,'max':2}, 'vulnerability': {'min':1,'probable':2,'max':3}, 'loss_magnitude':{'min':3,'probable':4,'max':5}, 'budget': 10000, 'currency':"SEK"})
        risk_new = HybridRisk.from_dict(risk.to_dict())
        self.assertTrue(risk == risk_new)
        risk_mod = HybridRisk({'threat_event_frequency': {'min':1,'probable':3,'max':5}, 'vulnerability': {'min':1,'probable':2,'max':3}, 'loss_magnitude':{'min':3,'probable':4,'max':5}, 'budget': 10000, 'currency':"SEK"})
        risk_new = HybridRisk.from_dict(risk_mod.to_dict())
        self.assertFalse(risk == risk_new)
        self.assertTrue(risk_mod == risk_new)

    def test_ui_bugg(self):
        values = {'threat_event_frequency': {'min': 0.023, 'probable': 0.12250000000000001, 'max': 0.222},
                  'vulnerability': {'min': 0.0, 'probable': 0.085, 'max': 0.17},
                  'loss_magnitude': {'min': 0.005, 'probable': 0.01, 'max': 0.02},
                  'budget': Decimal('1000000'), 'currency': 'SEK',
                  'mappings': {
                      'likelihood_initiation_or_occurence': [{'value': 1, 'low': 0.01, 'high': 0.1}, {'value': 2, 'low': 0.1, 'high': 1}, {'value': 3, 'low': 1, 'high': 10}, {'value': 4, 'low': 10, 'high': 100}, {'value': 5, 'low': 100, 'high': 1000}],
                      'likelihood_adverse_impact': [{'value': 1, 'low': 0.01, 'high': 0.12}, {'value': 2, 'low': 0.12, 'high': 0.25}, {'value': 3, 'low': 0.25, 'high': 0.5}, {'value': 4, 'low': 0.5, 'high': 0.75}, {'value': 5, 'low': 0.75, 'high': 1}], 
                      'impact': [{'value': 1, 'low': 0.0001, 'high': 0.005}, {'value': 2, 'low': 0.005, 'high': 0.01}, {'value': 3, 'low': 0.01, 'high': 0.02}, {'value': 4, 'low': 0.02, 'high': 0.05}, {'value': 5, 'low': 0.05, 'high': 1}], 
                      'num_to_text': {'5': 'Very High', '4': 'High', '3': 'Moderate', '2': 'Low', '1': 'Very Low', '0': 'Very Low'}, 
                      'risk': [{'value': 1, 'low': 1, 'high': 5}, {'value': 2, 'low': 5, 'high': 9}, {'value': 3, 'low': 9, 'high': 13}, {'value': 4, 'low': 13, 'high': 20}, {'value': 5, 'low': 20, 'high': 26}]}}
        risk = HybridRisk(values=values)
        self.assertIsNotNone(risk.qualitative.overall_risk)
        values = {'threat_event_frequency': {'min': 0.0, 'probable': 0.0, 'max': 0.0},
 'vulnerability': {'min': 0.0, 'probable': 0.0, 'max': 0.0},
 'loss_magnitude': {'min': 0.0, 'probable': 0.0, 'max': 0.0},
 'budget': Decimal('1000000'),
 'currency': 'SEK',
 'mappings': {'likelihood_initiation_or_occurence': [{'value': 1, 'low': 0.01, 'high': 0.1},
                                                     {'value': 2,
                                                      'low': 0.1,
                                                      'high': 1},
                                                     {'value': 3,
                                                      'low': 1,
                                                      'high': 10},
                                                     {'value': 4,
                                                      'low': 10,
                                                      'high': 100},
                                                     {'value': 5,
                                                      'low': 100,
                                                      'high': 1000}],
              'likelihood_adverse_impact': [{'value': 1,
                                             'low': 0.01,
                                             'high': 0.12},
                                            {'value': 2,
                                             'low': 0.12,
                                             'high': 0.25},
                                            {'value': 3,
                                             'low': 0.25,
                                             'high': 0.5},
                                            {'value': 4,
                                             'low': 0.5,
                                             'high': 0.75},
                                            {'value': 5,
                                             'low': 0.75,
                                             'high': 1}],
              'impact': [{'value': 1, 'low': 0.0001, 'high': 0.005},
                         {'value': 2, 'low': 0.005, 'high': 0.01},
                         {'value': 3, 'low': 0.01, 'high': 0.02},
                         {'value': 4, 'low': 0.02, 'high': 0.05},
                         {'value': 5, 'low': 0.05, 'high': 1}],
              'num_to_text': {'5': 'Very High',
                              '4': 'High',
                              '3': 'Moderate',
                              '2': 'Low',
                              '1': 'Very Low',
                              '0': 'Very Low'},
              'risk': [{'value': 1, 'low': 1, 'high': 5},
                       {'value': 2, 'low': 5, 'high': 9},
                       {'value': 3, 'low': 9, 'high': 13},
                       {'value': 4, 'low': 13, 'high': 20},
                       {'value': 5, 'low': 20, 'high': 26}]}}
        risk = HybridRisk(values=values)
        self.assertIsNotNone(risk.qualitative.overall_risk)