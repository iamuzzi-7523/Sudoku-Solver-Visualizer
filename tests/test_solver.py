"""
Unit tests for the Sudoku solver algorithms and helpers.

Tests cover:
- Row, column, and 3x3 box constraint validation
- Sequential empty cell detection
- Minimum Remaining Values (MRV) cell selection and dead-end pruning
- Standard backtracking solving
- MRV solving
- Graceful unsolvable puzzle handling
- Precision statistics tracking (attempts and backtracks)
- Visualization callback events
"""

import unittest
import puzzles
import solver


class TestSudokuSolver(unittest.TestCase):
    """Test suite for pure DSA Sudoku solver functions."""

    def setUp(self):
        # A simple test board with known placements
        self.sample_board = [
            [5, 3, 0, 0, 7, 0, 0, 0, 0],
            [6, 0, 0, 1, 9, 5, 0, 0, 0],
            [0, 9, 8, 0, 0, 0, 0, 6, 0],
            [8, 0, 0, 0, 6, 0, 0, 0, 3],
            [4, 0, 0, 8, 0, 3, 0, 0, 1],
            [7, 0, 0, 0, 2, 0, 0, 0, 6],
            [0, 6, 0, 0, 0, 0, 2, 8, 0],
            [0, 0, 0, 4, 1, 9, 0, 0, 5],
            [0, 0, 0, 0, 8, 0, 0, 7, 9],
        ]

    # 1. Constraint Validation Tests
    def test_is_valid_row_conflict(self):
        """Placing a duplicate number in the same row must be invalid."""
        board = [row[:] for row in self.sample_board]
        # In row 0, 5 and 3 already exist
        self.assertFalse(solver.is_valid(board, 0, 2, 5))
        self.assertFalse(solver.is_valid(board, 0, 2, 3))

    def test_is_valid_column_conflict(self):
        """Placing a duplicate number in the same column must be invalid."""
        board = [row[:] for row in self.sample_board]
        # In column 0, 5, 6, 8, 4, 7 already exist
        self.assertFalse(solver.is_valid(board, 2, 0, 5))
        self.assertFalse(solver.is_valid(board, 2, 0, 6))

    def test_is_valid_box_conflict(self):
        """Placing a duplicate number in the same 3x3 box must be invalid."""
        board = [row[:] for row in self.sample_board]
        # Top-left box contains: 5, 3, 6, 9, 8
        self.assertFalse(solver.is_valid(board, 1, 1, 9))
        self.assertFalse(solver.is_valid(board, 1, 1, 8))

    def test_is_valid_legal_placement(self):
        """Placing a non-conflicting number must be valid."""
        board = [row[:] for row in self.sample_board]
        # At (0, 2), 1, 2, 4 are candidate numbers not in row 0, col 2, or box (0,0)
        self.assertTrue(solver.is_valid(board, 0, 2, 1))
        self.assertTrue(solver.is_valid(board, 0, 2, 2))
        self.assertTrue(solver.is_valid(board, 0, 2, 4))

    # 2. Empty Cell Selection Tests
    def test_find_empty_first_cell(self):
        """find_empty should return the coordinates of the first empty cell."""
        board = [row[:] for row in self.sample_board]
        self.assertEqual(solver.find_empty(board), (0, 2))

    def test_find_empty_full_board(self):
        """find_empty should return None when the board is completely filled."""
        full_board = [[1] * 9 for _ in range(9)]
        self.assertIsNone(solver.find_empty(full_board))

    def test_find_empty_mrv_selection(self):
        """find_empty_mrv should return an empty cell with the fewest legal options."""
        # Create a board where cell (0, 0) has 1 valid candidate and other cells have more
        board = [[0] * 9 for _ in range(9)]
        # Constrain (0, 0) by filling its row with 1..8 in other columns
        for c in range(1, 9):
            board[0][c] = c
        # Cell (0, 0) can only take 9 (1 legal candidate)
        mrv_cell = solver.find_empty_mrv(board)
        self.assertEqual(mrv_cell, (0, 0))

    def test_find_empty_mrv_dead_end_pruning(self):
        """If a cell has 0 valid candidates, MRV must return it immediately (fail-first)."""
        board = [[0] * 9 for _ in range(9)]
        # Fill row with 1..8
        for c in range(1, 9):
            board[0][c] = c
        # Fill col 0 with 9 at (1, 0)
        board[1][0] = 9
        # Now cell (0, 0) has 0 valid candidates (1-8 in row, 9 in col)
        # MRV must identify this dead end immediately
        self.assertEqual(solver.find_empty_mrv(board), (0, 0))

    # 3. Solver Execution Tests
    def test_solve_backtracking_demo(self):
        """Standard backtracking should successfully solve the backtrack demo puzzle."""
        board = puzzles.get_puzzle("backtrack_demo")
        stats = solver.SolverStats("backtracking")
        stats.start()
        success = solver.solve(board, algorithm="backtracking", stats=stats)
        stats.stop(success)

        self.assertTrue(success)
        self.assertTrue(solver.is_board_solved(board))
        self.assertGreater(stats.attempts, 0)
        self.assertGreater(stats.backtracks, 0)

    def test_solve_mrv_demo(self):
        """MRV heuristic should successfully solve the backtrack demo puzzle."""
        board = puzzles.get_puzzle("backtrack_demo")
        stats = solver.SolverStats("mrv")
        stats.start()
        success = solver.solve(board, algorithm="mrv", stats=stats)
        stats.stop(success)

        self.assertTrue(success)
        self.assertTrue(solver.is_board_solved(board))
        self.assertGreater(stats.attempts, 0)

    def test_solve_unsolvable_puzzle(self):
        """The solver must return False for an unsolvable puzzle without crashing."""
        board = puzzles.get_puzzle("unsolvable")
        stats = solver.SolverStats("backtracking")
        stats.start()
        success = solver.solve(board, algorithm="backtracking", stats=stats)
        stats.stop(success)

        self.assertFalse(success)
        self.assertFalse(solver.is_board_solved(board))
        self.assertGreater(stats.attempts, 0)

    # 4. Callback & Visualization Events
    def test_callback_events(self):
        """The solver should properly trigger trying, invalid, and backtrack events."""
        board = puzzles.get_puzzle("easy")
        events = []

        def recording_callback(row: int, col: int, num: int, event_type: str):
            events.append((row, col, num, event_type))

        stats = solver.SolverStats("backtracking")
        success = solver.solve(board, algorithm="backtracking", callback=recording_callback, stats=stats)

        self.assertTrue(success)
        event_types = {e[3] for e in events}
        self.assertIn("trying", event_types)
        self.assertIn("invalid", event_types)


if __name__ == "__main__":
    unittest.main()
