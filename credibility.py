from typing import Callable, Any, Dict
from graders import Falling, Peaking, Growing
from constants import Constants


class Levels:
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class CredibilityEvaluator:
    def __init__(self):
        self._graders = {
            Levels.LOW: Growing.continuous(2, Constants.max_info_points),
            Levels.MEDIUM: Peaking.continuous_sinusoid(Constants.max_info_points / 2),
            Levels.HIGH: Falling.continuous(2, Constants.max_info_points)
        }

    def grade(self, intensity: float) -> str:
        """Find out which level of trust corresponds to specified intensity."""

        grades: Dict[float, str] = dict()
        for level, grader in self._graders.items():
            grade = grader(intensity)
            grades[grade] = level

        final_grade = max(grades)

        return grades[final_grade]
