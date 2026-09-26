# Final Project Walkthrough: Interactive Sudoku Solver & Visualizer

A comprehensive guide explaining the mechanics, algorithms, architecture, and live-modification procedures of the project.

---

## A. What the Project Does

The project is an interactive desktop application that visually demonstrates how computers solve constraint-satisfaction problems using **Recursive Backtracking** and the **Minimum Remaining Values (MRV)** heuristic.

Instead of computing the solution silently and displaying only the result, the application visualizes the step-by-step decision-making process:
1. Candidate digits (1–9) are evaluated against row, column, and 3x3 box rules.
2. Invalid candidates flash red and are rejected.
3. Valid candidates are placed and highlighted in blue.
4. When a dead-end occurs, the visualizer highlights cell resets in orange and steps backward up the recursion tree.
5. Live metrics track the exact number of attempts, backtracks, and wall-clock execution time.

---

## B. File-by-File Explanation

### 1. `solver.py` (Pure DSA Engine)
- Contains zero Pygame or UI code. Operates strictly on `List[List[int]]`.
- **`is_valid(board, row, col, num)`**: Validates row, column, and 3x3 box constraints ($O(1)$).
- **`find_empty(board)`**: Sequential search finding the first cell with `0`.
- **`find_empty_mrv(board)`**: Evaluates candidate counts for all empty cells and selects the one with the fewest legal values. Includes fail-first dead-end detection.
- **`solve(board, algorithm, callback, stats)`**: Recursive backtracking solver. Accepts an optional callback to stream events to the UI.
- **`SolverStats`**: Class tracking `attempts`, `backtracks`, and `elapsed_time`.

### 2. `board.py` (UI State Model)
- Encapsulates board state for the Pygame UI:
  - `grid`: The active 9x9 matrix.
  - `initial_grid`: Copy of the puzzle clues used for resetting.
  - `original_mask`: 9x9 boolean matrix identifying fixed, immutable clues.
  - `cell_states`: 9x9 matrix of visual states (`"normal"`, `"original"`, `"trying"`, `"invalid"`, `"backtrack"`, `"solved"`).

### 3. `visualizer.py` (Rendering Engine)
- Pygame drawing routines:
  - Renders the 9x9 grid with 1px cell dividers and 3px box dividers.
  - Draws color-coded digits and background highlights.
  - Renders the sidebar metrics dashboard and legend.
  - Draws rounded interactive buttons with hover state transitions.
  - Displays dynamic status messages.

### 4. `main.py` (Controller & Entry Point)
- Coordinates user input events, hotkeys, and the main rendering loop.
- Intercepts Pygame events inside the solver callback so the user can abort or close the window during active solving.
- Contains the `--cli` argument parser for headless benchmarking.

### 5. `config.py` (Central Configuration)
- Places primary interview live levers at the very top (`SOLVER_ALGORITHM`, `ANIMATION_DELAY`, `DEFAULT_PUZZLE`).
- Defines all window dimensions, coordinates, font families, and high-contrast color codes.

### 6. `puzzles.py` (Curated Datasets)
- Pre-defined 9x9 puzzle matrices (`easy`, `medium`, `hard`, `backtrack_demo`, `unsolvable`).
- All puzzles are empirically benchmarked to guarantee fast execution without stalling or freezing.

---

## C. Program Execution Flow

```
[Start App] (main.py)
   |
   +--> Read config.py defaults (SOLVER_ALGORITHM, ANIMATION_DELAY)
   +--> Initialize SudokuBoard and Pygame display
   |
[Event Loop]
   |
   +--> User clicks "Solve" or presses [Space]
   |       |
   |       v
   |    solver.solve(board.grid, algorithm, step_callback, stats)
   |       |
   |       +--> (For each step) Invokes step_callback()
   |       |       |
   |       |       +--> Update cell_states in board
   |       |       +--> visualizer.render()
   |       |       +--> Process Pygame events (check for abort)
   |       |       +--> time.sleep(ANIMATION_DELAY)
   |       |
   |       v
   |    solve() returns True or False
   |       |
   |       +--> True:  mark_all_solved() -> Green highlight & success message
   |       +--> False: Red status banner -> "No valid solution exists"
   |
   +--> User clicks "Reset" / "Algo" / "Puzzle" -> update state & redraw
```

---

## D. How the Solver Works

The solver implements Depth-First Search with constraint satisfaction:

1. **Find Target Cell**: Selects an unassigned cell ($0$) using either sequential order or MRV.
2. **Base Case**: If no cells are empty, every cell has been legally filled. Return `True`.
3. **Iterate Candidates**: For each candidate digit $n \in \{1, 2, \dots, 9\}$:
   - Check constraints via `is_valid()`.
   - If valid, write `board[row][col] = n`.
   - Make recursive call `solve(board)`.
   - If recursion returns `True`, return `True` immediately (unwind stack).
   - If recursion returns `False`, reset `board[row][col] = 0` (backtrack).
4. **Failure Signal**: If digits 1–9 all fail, return `False` to the caller.

---

## E. How Recursion Works

Recursion relies on the system **Call Stack**:
- Each call to `solve()` represents a single empty cell assignment.
- When `solve()` calls itself, Python pushes a new stack frame containing the current board reference and local variables (`row`, `col`, `num`).
- When a candidate succeeds down to the final cell, each recursive call returns `True`, unwinding the stack back to the root call.
- The maximum stack depth equals the number of empty cells ($E \le 81$), which is well below Python's default recursion limit of $1000$.

---

## F. How Backtracking Works

Backtracking is the process of **undoing a previous decision when that decision leads to a dead end**.

Consider this sequence:
1. Solver places `1` at Cell $(0, 2)$. This placement is currently valid.
2. The solver advances to Cell $(0, 3)$ and attempts numbers 1–9.
3. Every number from 1–9 conflicts with existing row, col, or box constraints.
4. Cell $(0, 3)$ cannot be filled. Therefore, the earlier choice of `1` at Cell $(0, 2)$ was either directly or indirectly flawed.
5. The recursive call for Cell $(0, 3)$ returns `False`.
6. Control returns to Cell $(0, 2)$, which executes:
   ```python
   board[row][col] = 0  # Undo placement!
   ```
7. Cell $(0, 2)$ now tests candidate `2`.

---

## G. How MRV Works

Standard backtracking selects empty cells in a fixed, static order:
$(0, 0) \to (0, 1) \to (0, 2) \dots$

**Minimum Remaining Values (MRV)** selects cells dynamically:
1. Scan every empty cell $(r, c)$ on the board.
2. Count how many digits ($1$ to $9$) currently satisfy `is_valid(board, r, c, num)`.
3. Select the cell with the smallest candidate count.
4. If a cell has **0 valid candidates**, return it immediately!

---

## H. What Each Statistic Means

- **Attempts**:  
  Every candidate digit ($1$ to $9$) evaluated using `is_valid()`. Incremented on every single constraint test.
- **Backtracks**:  
  Every occurrence where a previously placed candidate is removed (`board[row][col] = 0`) because that branch failed to produce a valid solution.
- **Execution Time**:  
  Total elapsed wall-clock time from start to termination measured using `time.perf_counter()`.
- **Empty Cells**:  
  The current count of cells containing `0`. Starts at the puzzle's initial empty cell count and decreases as candidates are placed.

---

## I. What Happens When a Number Is Invalid

1. The candidate loop tests `is_valid(board, row, col, num)`.
2. A duplicate exists in the row, column, or 3x3 box; `is_valid()` returns `False`.
3. In headless mode, the solver simply proceeds to the next candidate digit.
4. In visual mode, `callback(row, col, num, "invalid")` is invoked.
5. The visualizer marks that cell as `"invalid"`, rendering the candidate in **red**.
6. The app sleeps for `ANIMATION_DELAY` and reverts the cell to `"normal"`, making the rejection clearly visible.

---

## J. What Happens When the Solver Reaches a Dead End

1. All digits 1–9 have been tested for the current cell, and none led to a solution.
2. The function exits the candidate loop and reaches `return False`.
3. The current stack frame terminates and pops off the call stack.
4. Execution resumes in the caller function (the previous cell), which triggers the backtrack step:
   - Increments `stats.backtracks += 1`.
   - Clears `board[row][col] = 0`.
   - Notifies callback with `"backtrack"`.

---

## K. Why Resetting the Cell to 0 Is Necessary

The board is passed by reference across all recursive calls:
- If `board[row][col] = 0` was omitted during backtracking, the rejected number would remain on the grid.
- Subsequent recursive branches checking `is_valid()` would see this cell as occupied by that digit, causing false constraint violations.
- Resetting to `0` restores the board state to exactly what it was before the flawed guess was made.

---

## L. Why MRV Can Reduce Search

1. **Branching Factor Reduction**:  
   If a cell has 7 options and another cell has only 1 option, choosing the cell with 1 option limits the branching factor at this tree node to 1 instead of 7.
2. **Fail-First Principle**:  
   If a previous choice caused another empty cell to have **zero legal candidates**, that entire subtree is guaranteed to fail. MRV immediately selects that 0-candidate cell, fails on attempt 1, and backtracks right away, avoiding thousands of useless operations.

---

## M. How UI and Solver Communicate

The UI and solver are completely decoupled:
- `solver.py` accepts an optional `callback` function with signature:
  `callback(row: int, col: int, num: int, event_type: str) -> None`
- When `solver.solve()` runs:
  - It passes event notifications (`"trying"`, `"invalid"`, `"backtrack"`).
  - The callback updates `board.cell_states[row][col]`, renders the frame via `visualizer.render()`, and applies `time.sleep(ANIMATION_DELAY)`.
  - The callback also pumps `pygame.event.get()`, allowing user aborts (`[R]` or `[Esc]`) to raise `StopSolvingException`, cleanly unwinding the recursion.
- In headless mode (`--cli` or unit tests), `callback=None`, allowing the solver to run at native Python speed with zero rendering overhead.

---

## N. How to Modify the Project Live in an Interview

### Modification 1: Changing Solving Algorithm
1. Open `config.py` in your code editor.
2. Locate line 14:
   ```python
   SOLVER_ALGORITHM = "backtracking"
   ```
3. Change `"backtracking"` to `"mrv"`:
   ```python
   SOLVER_ALGORITHM = "mrv"
   ```
4. Run `python main.py` in the terminal and click `Solve`.
5. Point out to the interviewer that on the demo puzzle, backtracks drop from **9** down to **0**, and attempts drop from **307** down to **226**.

### Modification 2: Changing Visualization Speed
1. Open `config.py`.
2. Locate line 21:
   ```python
   ANIMATION_DELAY = 0.05
   ```
3. Change `0.05` to `0.00`:
   ```python
   ANIMATION_DELAY = 0.00
   ```
4. Run `python main.py` and click `Solve`.
5. The puzzle completes near-instantly, demonstrating the difference between visual pacing and raw algorithmic speed.
