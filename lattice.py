from cell import Cell


class Lattice:
    def __init__(self, side_length: int = 21):
        self.side_length = side_length
        self.matrix = [[Cell() for _ in range(side_length)] for x in range(side_length)]

    def place_propagator(self, row: int, column: int) -> None:
        """Place source of information propagation."""

