from credibility import CredibilityEvaluator, TrustLevels, TrustLevel
from constants import Constants


class CellError(Exception):
    pass


class Cell:
    def __init__(self, row, col, width):
        self.info_trust_level: TrustLevel = TrustLevels.LOW
        self._info_points: int = Constants.min_info_points
        self._credibility_evaluator: CredibilityEvaluator = CredibilityEvaluator()

        # Visualization settings
        self.x = int(row * width)
        self.y = int(col * width)
        self.side_size = width

    def increment_info_points(self) -> None:
        """Increment amount of info points stored in the cell."""

        self._set_info_points(self._info_points + 1)

    def decrement_info_points(self) -> None:
        """Decrement amount of info points stored in the cell."""

        self._set_info_points(self._info_points - 1)

    def is_full(self) -> bool:
        """Check if the amount of info points in the cell is already at max."""

        return self._info_points == Constants.max_info_points

    def is_empty(self) -> bool:
        """Check if the amount of info points in the cell is only at min."""

        return self._info_points == Constants.min_info_points

    def make_propagator(self) -> None:
        """Make current cell a propagator of information."""

        self._set_info_points(Constants.max_info_points)

    def _set_info_points(self, points: int) -> None:
        """Set info points amount in the cell."""

        if not Constants.min_info_points <= points <= Constants.max_info_points:
            raise CellError("Cannot set amount of info points bigger than the maximum amount of current environment")

        self._info_points = points
        self.info_trust_level = self._credibility_evaluator.grade(points)
