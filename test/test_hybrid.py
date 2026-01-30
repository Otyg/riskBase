import unittest

from src.otyg_risk_base.hybrid import HybridRisk

class TestQuantitativeRisk(unittest.TestCase):
    def test_equality(self):
        risk = HybridRisk({'threat_event_frequency': {'min':0,'probable':1,'max':2}, 'vulnerability': {'min':1,'probable':2,'max':3}, 'loss_magnitude':{'min':3,'probable':4,'max':5}, 'budget': 10000, 'currency':"SEK"})
        self.assertTrue(risk == risk)
        risk_mod = HybridRisk({'threat_event_frequency': {'min':1,'probable':3,'max':5}, 'vulnerability': {'min':1,'probable':2,'max':3}, 'loss_magnitude':{'min':3,'probable':4,'max':5}, 'budget': 10000, 'currency':"SEK"})
        self.assertFalse(risk == risk_mod)
    
    def test_greater_than(self):
        risk = HybridRisk(values={'threat_event_frequency': {'min':0,'probable':1,'max':2}, 'vulnerability': {'min':1,'probable':2,'max':3}, 'loss_magnitude':{'min':3,'probable':4,'max':5}, 'budget': 10000, 'currency':"SEK"})
        self.assertFalse(risk > risk)
        risk_mod = HybridRisk(values={'threat_event_frequency': {'min':10,'probable':30,'max':50}, 'vulnerability': {'min':1,'probable':2,'max':3}, 'loss_magnitude':{'min':30,'probable':40,'max':50}, 'budget': 10000, 'currency':"SEK"})
        self.assertTrue(risk_mod > risk)

    def test_serialization_deserialization(self):
        risk = HybridRisk({'threat_event_frequency': {'min':0,'probable':1,'max':2}, 'vulnerability': {'min':1,'probable':2,'max':3}, 'loss_magnitude':{'min':3,'probable':4,'max':5}, 'budget': 10000, 'currency':"SEK"})
        risk_new = HybridRisk(risk.to_dict())
        self.assertTrue(risk == risk_new)