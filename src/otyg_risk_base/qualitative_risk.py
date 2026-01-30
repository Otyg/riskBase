
from typing import Dict, Tuple


class QualitativeRisk():
    SCALE:Dict[str, int] = {
        5: 'Very High',
        4: 'High',
        3: 'Moderate',
        2: 'Low',
        1: 'Very Low',
    }

    RANGE_MAP: Tuple[Tuple[range, str], ...] = (
        (range(1, 5), "Very Low"),
        (range(5, 9), "Low"),
        (range(9, 13), "Moderate"),
        (range(13, 20), "High"),
        (range(20, 26), "Very High")
    )
    
    
    def __init__(self, likelihood_init:int=1, likelihood_impact:int=1, impact:int=1):
        self.overall_likelihood:str = self.get_calculated_text(value=likelihood_impact*likelihood_init)
        self.overall_likelihood_num:int = self.reverse_scale(self.overall_likelihood)
        self.likelihood_initiation_or_occurence:str = self.SCALE.get(likelihood_init)
        self.likelihood_adverse_impact:str = self.SCALE.get(likelihood_impact)
        self.impact:str = self.SCALE.get(impact)
        self.overall_risk:str = self.get_calculated_text(self.overall_likelihood_num*impact)

    def get(self):
        return {'risk': self.overall_risk, 'likelihood': self.overall_likelihood, 'impact': self.impact}
    
    def get_calculated_text(self, value:int) -> str:
        for r, label in self.RANGE_MAP:
            if value in r:
                return label
        raise RuntimeError(f"{value} not covered by mapping.")
    
    def reverse_scale(self, value:str) -> int:
        return next(label for label, x in self.SCALE.items() if x == value)