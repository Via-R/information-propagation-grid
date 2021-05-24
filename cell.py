from typing import Optional
from credibility import CredibilityEvaluator, Levels
from constants import Constants


class CellError(Exception):
    pass


class Cell:
    def __init__(self):
        self.info_points: int = Constants.min_info_points
        self.info_trust: float = 0
        self.info_trust_level: str = Levels.LOW
        self.credibility_evaluator: CredibilityEvaluator = CredibilityEvaluator()

    def _set_info_points(self, points: int) -> None:
        """Set info points amount in the cell."""

        if not Constants.min_info_points <= points <= Constants.max_info_points:
            raise CellError("Cannot set amount of info points bigger than the maximum amount of current environment")

        self.info_points = points
        info_trust, self.info_trust_level = self.credibility_evaluator.grade(points)
        if self.info_trust_level == Levels.LOW:
            self.info_trust = 0.33
        elif self.info_trust_level == Levels.MEDIUM:
            self.info_trust = 0.66
        else:
            self.info_trust = 0.99

    def increment_info_points(self) -> None:
        """Increment amount of info points stored in the cell."""

        self._set_info_points(self.info_points + 1)

    def decrement_info_points(self) -> None:
        """Decrement amount of info points stored in the cell."""

        self._set_info_points(self.info_points - 1)

    def is_full(self) -> bool:
        """Check if the amount of info points in the cell is already at max."""

        return self.info_points == Constants.max_info_points

    def is_empty(self) -> bool:
        """Check if the amount of info points in the cell is only at min."""

        return self.info_points == Constants.min_info_points

    def make_propagator(self) -> None:
        """Make current cell a propagator of information."""

        self._set_info_points(Constants.max_info_points)
