from typing import Optional

from credibility import CredibilityEvaluator


class Cell:
    def __init__(self):
        self.info_points: int = 0
        self.credibility_evaluator: CredibilityEvaluator = CredibilityEvaluator()
