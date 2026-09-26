"""
Core Sudoku Solving Algorithms and Helpers.

This module contains pure Data Structures & Algorithms logic operating strictly
on standard 9x9 Python 2D lists (List[List[int]]).

It has NO dependencies on Pygame, UI classes, or external libraries.
All functions are designed to be read, tested, and understood clearly
and concisely.

Key Functions:
1. is_valid(board, row, col, num)   - Constraint checking (Row, Column, 3x3 Box)
2. find_empty(board)                - Sequential empty cell selection
3. find_empty_mrv(board)            - Minimum Remaining Values heuristic selection
4. solve(board, algorithm, ...)     - Recursive backtracking solver
"""

import time
from typing import List, Tuple, Optional, Callable


class SolverStats:
    """
    Precise performance statistics tracker.

    Definitions:
    - attempts:   Every candidate digit (1-9) tested using is_valid().
    - backtracks: Every time the solver removes a previously placed candidate
                  because that branch led to a dead end.
    - elapsed_time: Wall-clock execution time in seconds.
    """

    def __init__(self, algorithm: str = "backtracking"):
        self.algorithm: str = algorithm
        self.attempts: int = 0
        self.backtracks: int = 0
        self.start_time: float = 0.0
        self.end_time: float = 0.0
        self.is_solved: bool = False

    def start(self) -> None:
        """Start the timer and reset statistics."""
        self.start_time = time.perf_counter()
        self.end_time = 0.0
        self.attempts = 0
        self.backtracks = 0
        self.is_solved = False

    def stop(self, solved: bool = True) -> None:
        """Stop the timer and record completion status."""
        self.end_time = time.perf_counter()
        self.is_solved = solved

    @property
    def elapsed_time(self) -> float:
        """Return elapsed time in seconds."""
        if self.start_time == 0.0:
            return 0.0
        if self.end_time == 0.0:
            return time.perf_counter() - self.start_time
        return self.end_time - self.start_time


def is_valid(board: List[List[int]], row: int, col: int, num: int) -> bool:
    """
    Check if placing 'num' at board[row][col] satisfies all Sudoku constraints:
    1. Row uniqueness:    'num' must not already appear in the given row.
    2. Column uniqueness: 'num' must not already appear in the given column.
    3. 3x3 Box uniqueness: 'num' must not already appear in the 3x3 subgrid.

    Returns:
        True if the placement is valid, False otherwise.
    """
    # 1. Check row constraint
    for c in range(9):
        if board[row][c] == num:
            return False

    # 2. Check column constraint
    for r in range(9):
        if board[r][col] == num:
            return False

    # 3. Check 3x3 subgrid constraint
    box_start_row = (row // 3) * 3
    box_start_col = (col // 3) * 3
    for r in range(box_start_row, box_start_row + 3):
        for c in range(box_start_col, box_start_col + 3):
            if board[r][c] == num:
                return False

    return True


def find_empty(board: List[List[int]]) -> Optional[Tuple[int, int]]:
    """
    Find the next empty cell (value == 0) using standard sequential search
    (row-by-row, left-to-right).

    Returns:
        (row, col) tuple if an empty cell is found, or None if the board is full.
    """
    for r in range(9):
        for c in range(9):
            if board[r][c] == 0:
                return (r, c)
    return None


def find_empty_mrv(board: List[List[int]]) -> Optional[Tuple[int, int]]:
    """
    Minimum Remaining Values (MRV) Heuristic:
    Finds the empty cell with the fewest currently valid candidate numbers (1-9).

    Why this works:
    - Choosing a cell with fewer legal options narrows the branching factor
      at the top of the search tree.
    - If any empty cell has 0 valid candidates, that cell is in an immediate
      dead end. Returning it immediately forces the solver to fail on the very
      next step and backtrack right away (Fail-First Principle), saving massive
      search time.

    Returns:
        (row, col) tuple of the most constrained empty cell, or None if board is full.
    """
    best_cell = None
    min_legal_count = 10  # Maximum possible legal candidates is 9

    for r in range(9):
        for c in range(9):
            if board[r][c] == 0:
                # Count valid candidate numbers for this empty cell
                legal_count = 0
                for num in range(1, 10):
                    if is_valid(board, r, c, num):
                        legal_count += 1

                # Fail-first optimization: 0 candidates means dead-end reached
                if legal_count == 0:
                    return (r, c)

                if legal_count < min_legal_count:
                    min_legal_count = legal_count
                    best_cell = (r, c)

    return best_cell


def count_empty(board: List[List[int]]) -> int:
    """Return the total number of empty cells (cells with value 0)."""
    return sum(row.count(0) for row in board)


def is_board_solved(board: List[List[int]]) -> bool:
    """
    Verify that a board is completely and legally solved.
    Returns True if full and valid, False otherwise.
    """
    for r in range(9):
        for c in range(9):
            val = board[r][c]
            if val == 0:
                return False
            # Check validity without self
            board[r][c] = 0
            valid = is_valid(board, r, c, val)
            board[r][c] = val
            if not valid:
                return False
    return True


def solve(
    board: List[List[int]],
    algorithm: str = "backtracking",
    callback: Optional[Callable[[int, int, int, str], None]] = None,
    stats: Optional[SolverStats] = None,
) -> bool:
    """
    Solve a Sudoku puzzle using recursive backtracking with an optional
    MRV heuristic and visualization callback.

    Core Algorithm Flow:
    1. Select an empty cell (via standard sequential scan or MRV heuristic).
    2. Base Case: If no empty cell remains, the board is solved (return True).
    3. Loop through candidate digits 1 to 9:
       a. Increment attempt counter.
       b. Check if digit is valid using is_valid().
       c. If valid: place candidate, notify callback('trying'), and recurse.
       d. If recursive call succeeds: return True.
       e. If recursive call fails: undo placement (backtrack to 0), increment
          backtrack counter, notify callback('backtrack').
       f. If candidate was invalid: notify callback('invalid') to show rejection.
    4. If all digits 1-9 fail, return False (signals dead-end to parent caller).

    Parameters:
        board: 9x9 list of ints representing the board. Modified in-place.
        algorithm: "backtracking" or "mrv"
        callback: Optional function (row, col, num, event_type) -> None
                  Event types: "trying", "invalid", "backtrack", "solved"
        stats: Optional SolverStats tracker.

    Returns:
        True if the puzzle is solvable, False if no solution exists.
    """
    # 1. Select the next empty cell
    if algorithm == "mrv":
        empty = find_empty_mrv(board)
    else:
        empty = find_empty(board)

    # 2. Base Case: No empty cells remain -> solved!
    if empty is None:
        return True

    row, col = empty

    # 3. Try candidate numbers 1 through 9
    for num in range(1, 10):
        if stats is not None:
            stats.attempts += 1

        if is_valid(board, row, col, num):
            # Place the valid candidate
            board[row][col] = num

            if callback is not None:
                callback(row, col, num, "trying")

            # Recursive step: Continue solving with this candidate placed
            if solve(board, algorithm, callback, stats):
                return True

            # Backtracking step: The candidate didn't lead to a solution.
            # Undo placement by resetting to 0.
            board[row][col] = 0

            if stats is not None:
                stats.backtracks += 1

            if callback is not None:
                callback(row, col, 0, "backtrack")
        else:
            # Candidate violates row, col, or box constraint
            if callback is not None:
                callback(row, col, num, "invalid")

    # 4. Dead end: No candidate worked for this cell -> backtrack
    return False
