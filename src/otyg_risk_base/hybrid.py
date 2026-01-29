#
# BSD 3-Clause License
#
# Copyright (c) 2026, Martin Vesterlund
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its
#    contributors may be used to endorse or promote products derived from
#    this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#



from .quantitative_risk import QuantitativeRisk

class QuantitativeToQualitativeMappingThresholds():
    DEFAULT_PROBABILITY = [
                         {'value':1, 'text':'Mycket låg', 'threshold': 0.1},
                         {'value':2, 'text':'Låg', 'threshold': 0.5},
                         {'value':3, 'text':'Medel', 'threshold': 8.0},
                         {'value':4, 'text':'Hög', 'threshold': 13.0},
                         {'value':5, 'text':'Mycket hög', 'threshold': 13.01}]

    DEFAULT_CONSEQUENCE = [
                         {'value':1, 'text':'Försumbar påverkan', 'threshold': 0.001},
                         {'value':2, 'text':'Begränsad påverkan', 'threshold': 0.005},
                         {'value':3, 'text':'Märkbar påverkan', 'threshold': 0.02},
                         {'value':4, 'text':'Allvarlig påverkan', 'threshold': 0.05},
                         {'value':5, 'text':'Kritisk påverkan', 'threshold': 0.051}]

    DEFAULT_RISK = [
                         {'value': 'very_low', 'text':'Mycket låg', 'threshold':3},
                         {'value': 'low', 'text':'Låg', 'threshold':6},
                         {'value': 'middle', 'text':'Medel', 'threshold':10},
                         {'value': 'high', 'text':'Hög', 'threshold':15},
                         {'value': 'critical', 'text':'Mycket hög', 'threshold':25}]

    def __init__(self, thresholds:dict = None):
        if not thresholds:
            thresholds = dict()
        self.probability_values = thresholds.get('probability', self.DEFAULT_PROBABILITY)
        self.consequence_values = thresholds.get('consequence', self.DEFAULT_CONSEQUENCE)
        self.risk_values = thresholds.get('risk', self.DEFAULT_RISK)

    def to_dict(self):
        return {
            "probability": self.probability_values,
            "consequence": self.consequence_values,
            "risk": self.risk_values
        }

class HybridRisk(QuantitativeRisk):
    def __init__(self, values:dict=None):
        if values:
            super().__init__(values=values)
        else:
            super()
        if not values or 'thresholds' not in values:
            self.thresholds = QuantitativeToQualitativeMappingThresholds()
        elif isinstance(values.get('thresholds'), QuantitativeToQualitativeMappingThresholds):
            self.thresholds = values.get('thresholds')
        else:
            self.thresholds = QuantitativeToQualitativeMappingThresholds(thresholds=values.get('thresholds'))
        
        self.risk = {
            'probability': values.get('probability') if values else self.calculate_probability(),
            'consequence': values.get('consequence') if values else self.calculate_consequence(),
            'risk': values.get('risk') if values else self.calculate_risk()}
    
    def get(self):
        return self.risk.copy()
    
    def calculate_risk(self):
        value = self.risk['probability'] * self.risk['consequence']
        self.__set_values('risk', value, self.thresholds.risk_values)
        self.risk['risk'] = value
    
    def calculate_probability(self):
        self.__set_values('probability', self.loss_event_frequency.probable, self.thresholds.probability_values)

    def __set_values(self, key, non_discreet_value, thresholds):
        threshold_max = max(thresholds, key=lambda x:x['threshold'])
        value = 0
        text = ""
        if non_discreet_value >= threshold_max['threshold']:
            value = threshold_max['value']
            text = threshold_max['text']
        else:
            for x in reversed(thresholds):
                if non_discreet_value <= x['threshold']:
                    value = x['value']
                    text = x['text']
        if key=="risk":
            self.risk.update({'level': value})
        self.risk.update({key: value})
        self.risk.update({key + '_text': text})
    
    def calculate_consequence(self):
        self.__set_values('consequence', self.loss_magnitude.probable, self.thresholds.consequence_values)

    def to_dict(self):
        me = super().to_dict()
        me.update(self.risk)
        me.update({"thresholds": self.thresholds.to_dict()})
        return me
    
    def __hash__(self):
        return hash((super().__hash__(), str(self.risk), str(self.thresholds.to_dict())))
    
    def __eq__(self, other):
        if isinstance(other, HybridRisk):
            return self.__hash__() == other.__hash__() 
    
    def __repr__(self):
        return str(self.to_dict())

    def __str__(self):
        return f"Sannolikhet: {str(self.risk['probability'])} ({self.risk['probability_text']})\nKonsekvens: {str(self.risk['consequence'])} ({self.risk['consequence_text']})\nRisk: {str(self.risk['risk'])} ({self.risk['risk_text']})"
