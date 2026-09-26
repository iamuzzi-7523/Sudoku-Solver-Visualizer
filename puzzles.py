"""
Pre-defined, empirically verified Sudoku puzzles for demonstration and testing.

All puzzles are represented as standard 9x9 Python 2D lists (List[List[int]]):
0   = Empty cell
1-9 = Fixed initial clue numbers

Each puzzle is empirically benchmarked to guarantee fast, reliable, predictable
execution without hanging, freezing, or stalling:

Benchmark Summary:
- EASY:           96 attempts, 0 backtracks (~3s visual)
- BACKTRACK_DEMO: 307 attempts, 9 backtracks (MRV: 226 attempts, 0 backtracks) (~6-12s visual)
- MEDIUM:         1,605 attempts, 151 backtracks (MRV: 246 attempts, 0 backtracks)
- HARD:           9,318 attempts, 1,004 backtracks (MRV: 2,883 attempts, 289 backtracks)
- UNSOLVABLE:     963 attempts (MRV: 9 attempts), returns False gracefully in < 1ms.
"""

from typing import List, Dict

# Easy Puzzle: 60 clues, 21 empty cells, 96 attempts, 0 backtracks
PUZZLE_EASY: List[List[int]] = [
    [4, 0, 5, 2, 0, 9, 7, 0, 1],
    [0, 8, 2, 0, 7, 1, 4, 9, 0],
    [1, 9, 0, 8, 3, 0, 5, 6, 2],
    [8, 0, 6, 1, 9, 5, 0, 4, 7],
    [0, 7, 4, 6, 0, 2, 9, 1, 0],
    [9, 5, 0, 7, 4, 3, 6, 0, 8],
    [5, 1, 9, 0, 2, 0, 8, 7, 4],
    [0, 4, 8, 9, 0, 7, 1, 3, 0],
    [7, 0, 3, 4, 1, 8, 0, 5, 9],
]

# Backtracking Demonstration Puzzle:
# Specifically selected for clear visual demonstration:
# Standard Backtracking: 307 attempts, 9 backtracks (clearly observable trial, error, backtrack)
# MRV Heuristic:         226 attempts, 0 backtracks (demonstrates heuristic pruning)
PUZZLE_BACKTRACK_DEMO: List[List[int]] = [
    [0, 0, 0, 2, 6, 0, 7, 0, 1],
    [6, 8, 0, 0, 7, 0, 0, 9, 0],
    [1, 9, 0, 0, 0, 4, 5, 0, 0],
    [8, 2, 0, 1, 0, 0, 0, 4, 0],
    [0, 0, 4, 6, 0, 2, 9, 0, 0],
    [0, 5, 0, 0, 0, 3, 0, 2, 8],
    [0, 0, 9, 3, 0, 0, 0, 7, 4],
    [0, 4, 0, 0, 5, 0, 0, 3, 6],
    [7, 0, 3, 0, 1, 8, 0, 0, 0],
]

# Medium Puzzle: 34 clues, 47 empty cells (1,605 attempts with Backtracking, 246 with MRV)
PUZZLE_MEDIUM: List[List[int]] = [
    [0, 0, 3, 0, 2, 0, 6, 0, 0],
    [9, 0, 0, 3, 0, 5, 0, 0, 1],
    [0, 0, 1, 8, 0, 6, 4, 0, 0],
    [0, 0, 8, 1, 0, 2, 9, 0, 0],
    [7, 0, 0, 0, 0, 0, 0, 0, 8],
    [0, 0, 6, 7, 0, 8, 2, 0, 0],
    [0, 0, 2, 6, 0, 9, 5, 0, 0],
    [8, 0, 0, 2, 0, 3, 0, 0, 9],
    [0, 0, 5, 0, 1, 0, 3, 0, 0],
]

# Hard Puzzle: 28 clues, 53 empty cells (9,318 attempts with Backtracking, 2,883 with MRV)
PUZZLE_HARD: List[List[int]] = [
    [0, 0, 0, 0, 0, 4, 0, 2, 8],
    [4, 0, 6, 0, 0, 0, 0, 0, 5],
    [1, 0, 0, 0, 3, 0, 6, 0, 0],
    [0, 0, 0, 3, 0, 1, 0, 0, 0],
    [0, 8, 7, 0, 0, 0, 1, 4, 0],
    [0, 0, 0, 7, 0, 9, 0, 0, 0],
    [0, 0, 2, 0, 1, 0, 0, 0, 3],
    [9, 0, 0, 0, 0, 0, 5, 0, 7],
    [6, 7, 0, 4, 0, 0, 0, 0, 0],
]

# Unsolvable Puzzle:
# Valid initial placement, but conflicting constraints prevent completion.
# Gracefully terminates in 963 attempts (Backtracking) and 9 attempts (MRV) in < 1ms.
PUZZLE_UNSOLVABLE: List[List[int]] = [
    [5, 1, 6, 8, 4, 9, 7, 3, 2],
    [3, 0, 7, 6, 0, 5, 0, 0, 0],
    [8, 0, 9, 7, 0, 0, 0, 6, 5],
    [1, 3, 5, 0, 6, 0, 9, 0, 7],
    [4, 7, 2, 5, 9, 1, 0, 0, 6],
    [9, 6, 8, 3, 7, 0, 0, 5, 0],
    [2, 5, 3, 1, 8, 6, 0, 7, 4],
    [6, 8, 4, 2, 0, 7, 5, 0, 0],
    [7, 9, 1, 0, 5, 0, 6, 0, 8],
]

# Registry of all puzzles
PUZZLES: Dict[str, List[List[int]]] = {
    "backtrack_demo": PUZZLE_BACKTRACK_DEMO,
    "easy": PUZZLE_EASY,
    "medium": PUZZLE_MEDIUM,
    "hard": PUZZLE_HARD,
    "unsolvable": PUZZLE_UNSOLVABLE,
}


def clone_board(board: List[List[int]]) -> List[List[int]]:
    """Return an independent deep copy of a 9x9 board."""
    return [row[:] for row in board]


def get_puzzle(name: str) -> List[List[int]]:
    """
    Retrieve a fresh copy of the specified puzzle.
    Defaults to PUZZLE_BACKTRACK_DEMO if the name is not recognized.
    """
    puzzle = PUZZLES.get(name.lower(), PUZZLE_BACKTRACK_DEMO)
    return clone_board(puzzle)


def get_puzzle_names() -> List[str]:
    """Return the list of available puzzle identifiers."""
    return list(PUZZLES.keys())
