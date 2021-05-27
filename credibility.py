import random

import matplotlib.pyplot as plt
from typing import Callable, Any, Dict, Tuple
from graders import Falling, Peaking, Growing, Dot
from constants import Constants, Colors, Probabilities
from utils import frange


class TrustLevel:
    def __init__(self, name: str, value: int, color: Tuple[int, int, int]):
        self.name = name
        self.value = value
        self.color = color


class TrustLevels:
    NULL = TrustLevel("null", 0, Colors.WHITE)
    LOW = TrustLevel("low", 1, Colors.GREEN)
    MEDIUM = TrustLevel("medium", 2, Colors.BLUE)
    HIGH = TrustLevel("high", 3, Colors.RED)


class TrustArchetypes:
    NORMAL = {
        TrustLevels.NULL: Dot.dot(Constants.min_info_points),
        TrustLevels.LOW: Falling.continuous(2, Constants.max_info_points),
        TrustLevels.MEDIUM: Peaking.continuous_sinusoid(Constants.max_info_points / 2),
        TrustLevels.HIGH: Growing.continuous(2, Constants.max_info_points)
    }
    REVERSED = {
        TrustLevels.NULL: Dot.dot(Constants.min_info_points),
        TrustLevels.LOW: Growing.continuous(2, Constants.max_info_points),
        TrustLevels.MEDIUM: Peaking.continuous_sinusoid(Constants.max_info_points / 2),
        TrustLevels.HIGH: Falling.continuous(2, Constants.max_info_points)
    }


class CredibilityEvaluator:
    def __init__(self, forced_normal: bool = False):
        if not forced_normal and random.random() < Probabilities.reversed_trust:
            self._graders = TrustArchetypes.REVERSED
        else:
            self._graders = TrustArchetypes.NORMAL

    def draw_graders(self) -> None:
        """Show all grader functions of this cell."""

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
