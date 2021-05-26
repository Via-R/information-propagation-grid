import matplotlib.pyplot as plt
from typing import Callable, Any, Dict, Tuple
from graders import Falling, Peaking, Growing
from constants import Constants
from utils import frange


class TrustLevel:
    def __init__(self, name: str, value: int):
        self.name = name
        self.value = value


class TrustLevels:
    LOW = TrustLevel("low", 0)
    MEDIUM = TrustLevel("medium", 1)
    HIGH = TrustLevel("high", 2)


class CredibilityEvaluator:
    def __init__(self):
        self._graders = {
            TrustLevels.LOW: Falling.continuous(2, Constants.max_info_points),
            TrustLevels.MEDIUM: Peaking.continuous_sinusoid(Constants.max_info_points / 2),
            TrustLevels.HIGH: Growing.continuous(2, Constants.max_info_points)
        }

    def draw_graders(self) -> None:
        for level, grader in self._graders.items():
            xs = [x for x in frange(Constants.min_info_points, Constants.max_info_points, 0.1)]
            ys = [grader(x) for x in xs]
            plt.plot(xs, ys)
            plt.xlabel('x axis')
            plt.ylabel('f(x) axis')
            plt.title(level.name)
            plt.show(block=False)
            plt.pause(3)
            plt.close()

    def grade(self, intensity: float) -> 'TrustLevel':
        """Find out which level of trust corresponds to specified intensity."""

        grades: Dict[TrustLevel, float] = dict()
        for level, grader in self._graders.items():
            grade = grader(intensity)
            grades[level] = grade

        return max(grades, key=grades.get)
