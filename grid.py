import matplotlib.pyplot as plt
from matplotlib import colors
from typing import List, Optional, Tuple
from copy import deepcopy
from cell import Cell
from constants import Constants
from utils import frange, print_json


class GridError(Exception):
    pass


class Grid:
    def __init__(self, side_length: int = 21):
        self.side_length: int = side_length
        self.matrix: List[List[Cell]] = [[Cell() for _ in range(side_length)] for _ in range(side_length)]
        self._default_next_matrix = [[None] * side_length for _ in range(side_length)]
        self._next_matrix: [List[List[Optional[Cell]]]] = deepcopy(self._default_next_matrix)

        self._cell_shifts: List[Tuple[int, int]] = []
        for shift_y in [1, 0, -1]:
            for shift_x in [-1, 0, 1]:
                self._cell_shifts.append((shift_y, shift_x))
        self._cell_shifts.remove((0, 0))

    def _get_cell(self, row: int, column: int) -> 'Cell':
        """Get Cell object by specified coordinates."""

        if not 0 <= row < len(self.matrix) or not 0 <= column < len(self.matrix[0]):
            raise GridError("Tried to target cell outside of the grid")

        return self.matrix[row][column]

    def _get_surrounding_cells(self, row: int, column: int) -> List[Optional[Cell]]:
        """Get a list of surrounding cells starting with northwest cell."""

        result: List[Optional[Cell]] = []
        for shift_y, shift_x in self._cell_shifts:
            try:
                cell = self._get_cell(row + shift_y, column + shift_x)
            except GridError:
                cell = None
            result.append(cell)

        return result

    def place_propagator(self, row: int, column: int) -> None:
        """Place source of information propagation."""

        propagator_cell = self._get_cell(row, column)
        propagator_cell.make_propagator()

    @staticmethod
    def _process_cell(new_cell: Cell, surrounding_cells: List[Optional[Cell]]) -> None:
        for surrounding_cell in surrounding_cells:
            if surrounding_cell is None:
                continue
            if surrounding_cell.info_trust > Constants.trust_threshold:
                # print("!!!")
                # print(new_cell.info_trust)
                if new_cell.is_full():
                    return
                new_cell.increment_info_points()
                # print(new_cell.info_trust)

    def _write_next_matrix(self) -> None:
        """Write default values to next_matrix field."""

        self.matrix = deepcopy(self._next_matrix)
        self._next_matrix: [List[List[Optional[Cell]]]] = deepcopy(self._default_next_matrix)

    async def next(self) -> None:
        """Simulate one time step in information propagation process."""

        for row in range(self.side_length):
            for column in range(self.side_length):
                cell = self._get_cell(row, column)
                updated_cell = deepcopy(cell)
                surrounding_cells = self._get_surrounding_cells(row, column)
                self._process_cell(updated_cell, surrounding_cells)
                # print(f"After {updated_cell.info_trust}")
                self._next_matrix[row][column] = updated_cell

        # print_json([[x.info_trust for x in row] for row in self.matrix])
        self._write_next_matrix()

    def draw(self) -> None:
        """Draw current grid status."""

        data = [[cell.info_trust for cell in row] for row in self.matrix]
        # print_json(data)
        cmap = colors.ListedColormap(['white', 'lightgray', 'gray', 'darkgray', 'dimgray'])
        bounds = [0, 0.2, 0.4, 0.6, 0.8, 1]
        norm = colors.BoundaryNorm(bounds, cmap.N)
        fig, ax = plt.subplots()
        ax.imshow(data, cmap=cmap, norm=norm)
        ax.grid(which='major', axis='both', linestyle='-', color='k', linewidth=2)
        ax.set_yticks([x for x in frange(-.5, self.side_length, 1)])
        ax.set_xticks([x for x in frange(-.5, self.side_length, 1)])
        plt.show(block=False)
        plt.pause(0.3)
        plt.close()
