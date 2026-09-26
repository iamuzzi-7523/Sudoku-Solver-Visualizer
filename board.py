"""
Sudoku Board Model for UI State Management.

This class encapsulates the 9x9 board data, tracks fixed original clues,
maintains visual highlighting states for Pygame rendering, and provides
reset/load methods.

IMPORTANT INTERVIEW NOTE:
To preserve separation of concerns, this class is used solely by the UI layer.
The solver functions in solver.py operate on pure List[List[int]] arrays
and do NOT receive or manipulate this class directly.
"""

from typing import List, Union
import puzzles


class SudokuBoard:
    """
    Manages the 9x9 grid, initial puzzle clues, and visual cell states.

    Cell States:
    - "normal":     Empty editable cell.
    - "original":   Fixed initial clue (non-editable, dark text).
    - "trying":     Candidate number currently placed during active solving.
    - "invalid":    Candidate number rejected by is_valid() (brief red highlight).
    - "backtrack":  Cell value reset to 0 after dead-end (orange highlight).
    - "solved":     Cell confirmed in the final solved board.
    """

    def __init__(self, puzzle_name: str = "backtrack_demo"):
        self.puzzle_name: str = puzzle_name
        self.initial_grid: List[List[int]] = []
        self.grid: List[List[int]] = []
        self.original_mask: List[List[bool]] = []
        self.cell_states: List[List[str]] = []
        self.load_puzzle(puzzle_name)

    def load_puzzle(self, puzzle: Union[str, List[List[int]]]) -> None:
        """
        Load a new puzzle by name or from a 2D list.
        Initializes the fixed-clue mask and cell states.
        """
        if isinstance(puzzle, str):
            self.puzzle_name = puzzle
            raw_grid = puzzles.get_puzzle(puzzle)
        else:
            self.puzzle_name = "custom"
            raw_grid = puzzles.clone_board(puzzle)

        self.initial_grid = puzzles.clone_board(raw_grid)
        self.grid = puzzles.clone_board(raw_grid)

        # Build original mask and initialize visual states
        self.original_mask = [
            [self.initial_grid[r][c] != 0 for c in range(9)]
            for r in range(9)
        ]
        self.cell_states = [
            ["original" if self.original_mask[r][c] else "normal" for c in range(9)]
            for r in range(9)
        ]

    def reset(self) -> None:
        """Reset the board back to its initial puzzle configuration."""
        self.grid = puzzles.clone_board(self.initial_grid)
        self.cell_states = [
            ["original" if self.original_mask[r][c] else "normal" for c in range(9)]
            for r in range(9)
        ]

    def set_cell(self, row: int, col: int, value: int, state: str = "trying") -> None:
        """Update cell value and visual state."""
        self.grid[row][col] = value
        self.cell_states[row][col] = state

    def get_cell(self, row: int, col: int) -> int:
        """Get the value of a cell."""
        return self.grid[row][col]

    def get_state(self, row: int, col: int) -> str:
        """Get the current visual state of a cell."""
        return self.cell_states[row][col]

    def is_original(self, row: int, col: int) -> bool:
        """Return True if cell was an initial puzzle clue, False otherwise."""
        return self.original_mask[row][col]

    def count_empty(self) -> int:
        """Return total number of currently empty cells (value == 0)."""
        return sum(row.count(0) for row in self.grid)

    def mark_all_solved(self) -> None:
        """Set visual state of all cells to solved."""
        for r in range(9):
            for c in range(9):
                if not self.original_mask[r][c]:
                    self.cell_states[r][c] = "solved"
