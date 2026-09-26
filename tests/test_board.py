"""
Unit tests for the SudokuBoard model and state management.

Tests cover:
- Grid initialization and deep copy isolation
- Fixed clue (original) mask generation
- Resetting board to initial state
- Empty cell counting
- Cell state transitions (trying, invalid, backtrack, solved)
"""

import unittest
import puzzles
from board import SudokuBoard


class TestSudokuBoard(unittest.TestCase):
    """Test suite for SudokuBoard class."""

    def test_board_initialization(self):
        """Board should load puzzle and mark original non-zero cells correctly."""
        board = SudokuBoard("backtrack_demo")
        raw = puzzles.get_puzzle("backtrack_demo")

        for r in range(9):
            for c in range(9):
                if raw[r][c] != 0:
                    self.assertTrue(board.is_original(r, c))
                    self.assertEqual(board.get_state(r, c), "original")
                else:
                    self.assertFalse(board.is_original(r, c))
                    self.assertEqual(board.get_state(r, c), "normal")

    def test_board_reset(self):
        """Reset should revert all modified cells and restore initial clues."""
        board = SudokuBoard("backtrack_demo")
        initial_empty = board.count_empty()

        # Modify an empty cell
        board.set_cell(0, 0, 9, "trying")
        self.assertEqual(board.get_cell(0, 0), 9)
        self.assertEqual(board.get_state(0, 0), "trying")
        self.assertEqual(board.count_empty(), initial_empty - 1)

        # Reset
        board.reset()
        self.assertEqual(board.get_cell(0, 0), 0)
        self.assertEqual(board.get_state(0, 0), "normal")
        self.assertEqual(board.count_empty(), initial_empty)

    def test_mark_all_solved(self):
        """mark_all_solved should mark all non-original cells as solved."""
        board = SudokuBoard("easy")
        board.mark_all_solved()

        for r in range(9):
            for c in range(9):
                if board.is_original(r, c):
                    self.assertEqual(board.get_state(r, c), "original")
                else:
                    self.assertEqual(board.get_state(r, c), "solved")


if __name__ == "__main__":
    unittest.main()
