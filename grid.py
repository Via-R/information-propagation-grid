import asyncio
import pygame
from asyncio import AbstractEventLoop
from typing import List, Optional, Tuple
from copy import deepcopy
from cell import Cell
from constants import Colors


class GridError(Exception):
    pass


class Grid:
    def __init__(self, window_side_length: int, side_size: int = 21):
        self.side_size: int = side_size
        self._cell_shifts: List[Tuple[int, int]] = []
        for shift_y in [-1, 0, 1]:
            for shift_x in [-1, 0, 1]:
                self._cell_shifts.append((shift_y, shift_x))
        self._cell_shifts.remove((0, 0))

        # Visualization settings
        self.side_length = window_side_length
        self.cell_width = self.side_length // self.side_size
        self.window = pygame.display.set_mode((window_side_length, window_side_length))
        self.window.fill(Colors.WHITE)
        pygame.display.set_caption("Information propagation")

        # Basic grid settings
        self.matrix: List[List[Cell]] = [
            [Cell(row, col, self.cell_width) for col in range(side_size)] for row in range(side_size)
        ]
        self._default_next_matrix = [[None] * side_size for _ in range(side_size)]
        self._next_matrix: [List[List[Optional[Cell]]]] = deepcopy(self._default_next_matrix)

    @staticmethod
    def _process_cell(new_cell: Cell, surrounding_cells: List[Optional[Cell]]) -> None:
        """Change cell status depending on its neighboring cells."""

        for surrounding_cell in surrounding_cells:
            if surrounding_cell is None:
                continue
            if surrounding_cell.info_trust_level.value > 1 and \
                    surrounding_cell.info_trust_level.value >= new_cell.info_trust_level.value:
                # if surrounding_cell.info_points > new_cell.info_points:
                if new_cell.is_full():
                    return
                new_cell.increment_info_points()

    @staticmethod
    def _pygame_event_loop(loop: AbstractEventLoop, event_queue: asyncio.Queue) -> None:
        """Event loop for pygame visualization."""

        while True:
            event = pygame.event.wait()
            asyncio.run_coroutine_threadsafe(event_queue.put(event), loop=loop)

    @staticmethod
    async def _handle_events(event_queue: asyncio.Queue) -> None:
        """Handler for pygame events."""

        while True:
            event = await event_queue.get()
            if event.type == pygame.QUIT:
                break
        asyncio.get_event_loop().stop()

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

    def _write_next_matrix(self) -> None:
        """Write default values to next_matrix field."""

        self.matrix = deepcopy(self._next_matrix)
        self._next_matrix: [List[List[Optional[Cell]]]] = deepcopy(self._default_next_matrix)

    def _draw_grid_lines(self) -> None:
        """Draw grid lines on the grid."""

        for i in range(self.side_size):
            pygame.draw.line(self.window, Colors.GRAY, (0, i * self.cell_width),
                             (self.side_length, i * self.cell_width))
            for j in range(self.side_size):
                pygame.draw.line(
                    self.window, Colors.GRAY, (j * self.cell_width, 0), (j * self.cell_width, self.side_length)
                )

    def _draw_cell(self, cell: Cell) -> None:
        """Draw a cell on the grid."""

        pygame.draw.rect(self.window, cell.info_trust_level.color,
                         (cell.x, cell.y, cell.side_size, cell.side_size))

    def _update_display(self) -> None:
        """Update grid status on screen."""

        for row in self.matrix:
            for cell in row:
                self._draw_cell(cell)

        self._draw_grid_lines()
        pygame.display.update()

    def _next_iteration(self) -> None:
        """Simulate one time step in information propagation process."""

        for row in range(self.side_size):
            for column in range(self.side_size):
                cell = self._get_cell(row, column)
                updated_cell = deepcopy(cell)
                surrounding_cells = self._get_surrounding_cells(row, column)
                self._process_cell(updated_cell, surrounding_cells)
                self._next_matrix[row][column] = updated_cell  # noqa

        self._write_next_matrix()

    async def _animation(self):
        """Coroutine to continue propagation."""

        while True:
            await asyncio.sleep(0.012)
            self._next_iteration()
            self._update_display()

    def place_propagator(self, row: int, column: int) -> None:
        """Place source of information propagation."""

        propagator_cell = self._get_cell(row, column)
        propagator_cell.make_propagator()

    def draw(self) -> None:
        """Start propagation process and its visualization."""

        loop: AbstractEventLoop = asyncio.get_event_loop()
        event_queue: asyncio.Queue = asyncio.Queue()
        pygame_task: asyncio.Future = loop.run_in_executor(None, self._pygame_event_loop, loop, event_queue)  # noqa
        animation_task: asyncio.Future = asyncio.ensure_future(self._animation())
        event_task: asyncio.Future = asyncio.ensure_future(self._handle_events(event_queue))
        try:
            loop.run_forever()
        except KeyboardInterrupt:
            pass
        finally:
            pygame_task.cancel()
            animation_task.cancel()
            event_task.cancel()

        pygame.quit()
