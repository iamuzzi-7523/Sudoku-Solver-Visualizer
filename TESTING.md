# Testing Strategy and Test Suite Documentation

This document explains how the Sudoku Solver and Visualizer is tested, how the test suites are structured, and how to verify both automated unit tests and manual UI functionality.

---

## 1. Testing Philosophy

Because `solver.py` is written as pure, headless Data Structures & Algorithms logic with zero GUI dependencies, all core algorithms, edge cases, and constraint verifications are tested using Python's built-in `unittest` framework without needing a display server or window manager.

---

## 2. Automated Unit Tests

### How to Run All Tests
Execute the test runner from the root of the workspace:

```bash
python -m unittest discover -s tests -p "test_*.py" -v
```

### Expected Output
```text
test_board_initialization (test_board.TestSudokuBoard.test_board_initialization)
Board should load puzzle and mark original non-zero cells correctly. ... ok
test_board_reset (test_board.TestSudokuBoard.test_board_reset)
Reset should revert all modified cells and restore initial clues. ... ok
test_mark_all_solved (test_board.TestSudokuBoard.test_mark_all_solved)
mark_all_solved should mark all non-original cells as solved. ... ok
test_callback_events (test_solver.TestSudokuSolver.test_callback_events)
The solver should properly trigger trying, invalid, and backtrack events. ... ok
test_find_empty_first_cell (test_solver.TestSudokuSolver.test_find_empty_first_cell)
find_empty should return the coordinates of the first empty cell. ... ok
test_find_empty_full_board (test_solver.TestSudokuSolver.test_find_empty_full_board)
find_empty should return None when the board is completely filled. ... ok
test_find_empty_mrv_dead_end_pruning (test_solver.TestSudokuSolver.test_find_empty_mrv_dead_end_pruning)
If a cell has 0 valid candidates, MRV must return it immediately (fail-first). ... ok
test_find_empty_mrv_selection (test_solver.TestSudokuSolver.test_find_empty_mrv_selection)
find_empty_mrv should return an empty cell with the fewest legal options. ... ok
test_is_valid_box_conflict (test_solver.TestSudokuSolver.test_is_valid_box_conflict)
Placing a duplicate number in the same 3x3 box must be invalid. ... ok
test_is_valid_column_conflict (test_solver.TestSudokuSolver.test_is_valid_column_conflict)
Placing a duplicate number in the same column must be invalid. ... ok
test_is_valid_legal_placement (test_solver.TestSudokuSolver.test_is_valid_legal_placement)
Placing a non-conflicting number must be valid. ... ok
test_is_valid_row_conflict (test_solver.TestSudokuSolver.test_is_valid_row_conflict)
Placing a duplicate number in the same row must be invalid. ... ok
test_solve_backtracking_demo (test_solver.TestSudokuSolver.test_solve_backtracking_demo)
Standard backtracking should successfully solve the backtrack demo puzzle. ... ok
test_solve_mrv_demo (test_solver.TestSudokuSolver.test_solve_mrv_demo)
MRV heuristic should successfully solve the backtrack demo puzzle. ... ok
test_solve_unsolvable_puzzle (test_solver.TestSudokuSolver.test_solve_unsolvable_puzzle)
The solver must return False for an unsolvable puzzle without crashing. ... ok

----------------------------------------------------------------------
Ran 15 tests in 0.027s

OK
```

---

## 3. Test Coverage Matrix

### A. Constraint Validation (`tests/test_solver.py`)
- `test_is_valid_row_conflict`: Confirms duplicate in row returns `False`.
- `test_is_valid_column_conflict`: Confirms duplicate in column returns `False`.
- `test_is_valid_box_conflict`: Confirms duplicate in 3x3 box returns `False`.
- `test_is_valid_legal_placement`: Confirms non-conflicting candidate returns `True`.

### B. Empty Cell Selection & Heuristics (`tests/test_solver.py`)
- `test_find_empty_first_cell`: Verifies left-to-right, top-to-bottom search.
- `test_find_empty_full_board`: Verifies `None` is returned when 0 empty cells remain (base case trigger).
- `test_find_empty_mrv_selection`: Verifies that MRV selects the cell with the fewest legal candidates.
- `test_find_empty_mrv_dead_end_pruning`: Verifies that when an empty cell has 0 legal options, MRV returns it immediately to trigger instant dead-end pruning (fail-first principle).

### C. Solver Correctness & Edge Cases (`tests/test_solver.py`)
- `test_solve_backtracking_demo`: Verifies that standard backtracking completes with a valid board.
- `test_solve_mrv_demo`: Verifies that MRV completes with a valid board.
- `test_solve_unsolvable_puzzle`: Verifies that a mathematically unsolvable board returns `False` safely without crashing or hanging.
- `test_callback_events`: Verifies that the optional step callback properly captures "trying", "invalid", and "backtrack" event streams.

### D. Board & UI State Model (`tests/test_board.py`)
- `test_board_initialization`: Verifies that initial non-zero digits are marked as read-only original clues.
- `test_board_reset`: Verifies that user edits or solver attempts are cleared back to 0 on reset without modifying initial clues.
- `test_mark_all_solved`: Verifies that the completed board switches all non-original cells to "solved" state.

---

## 4. Headless CLI Benchmark Mode

For quick verification across all built-in puzzles and algorithms without launching the Pygame display:

```bash
python main.py --cli
```

This runs both algorithms on all 5 puzzles and prints an empirical execution table:
- **Attempts**: Exact count of candidate tests.
- **Backtracks**: Exact count of cell resets after branch failure.
- **Elapsed Time**: Wall-clock execution time in seconds.

---

## 5. Manual UI Verification Checklist

When demonstrating the graphical interface live:

1. **Launch**: Run `python main.py`. Window opens at 960x640 with crisp slate/white layout.
2. **Clue Distinction**: Initial puzzle numbers are displayed in bold dark blue; empty cells are white.
3. **Interactive Solve**:
   - Press `[Space]` or click `Solve`.
   - Observe candidate digits tested:
     - Conflicting numbers flash briefly in red ("invalid").
     - Valid candidates are placed in light blue ("trying").
     - Backtracking clears cells back to 0 in light orange ("backtrack").
   - Metrics in sidebar update dynamically.
4. **Completion**:
   - Solved board flashes green; status bar reports elapsed time and backtrack count.
5. **Reset**:
   - Press `[R]` or click `Reset`. Board reverts to initial clues and metrics reset to 0.
6. **Switch Algorithm**:
   - Press `[A]` or click `Algo`. Badge changes from "Backtracking" to "Backtracking + MRV".
   - Click `Solve`. Observe that MRV solves the demo puzzle with 0 backtracks (vs 9 with standard backtracking).
7. **Unsolvable Puzzle Test**:
   - Press `[P]` until `UNSOLVABLE` is loaded.
   - Click `Solve`.
   - The solver runs, exhausts candidates, and displays:  
     `"Unsolvable: No valid solution exists for this puzzle!"` in red without crashing.
