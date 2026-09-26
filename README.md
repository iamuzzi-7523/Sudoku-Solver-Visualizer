# Interactive Sudoku Solver & Algorithm Visualizer

A clean, interactive Python application that visualizes **Recursive Backtracking** and the **Minimum Remaining Values (MRV)** heuristic in real-time using Pygame.

Designed to demonstrate core Data Structures & Algorithms, recursion mechanics, state restoration, and heuristic optimization in an engaging, visual manner.

---

## 1. Project Overview

Most algorithmic solvers simply compute a solution in memory and display the final 9x9 grid. This project makes the **search process visible**:

- **Candidate Testing**: Watch candidate numbers (1–9) being tested against Sudoku constraints.
- **Invalid Rejection**: Visualizes conflicting numbers briefly flashing red as `is_valid()` rejects them.
- **Valid Placement**: Accepted candidates are placed and highlighted in blue.
- **Recursive Backtracking**: When a dead-end is reached, watch the algorithm reset cells back to `0` (amber/orange highlight) and unwind the call stack to explore alternative branches.
- **Heuristic Comparison**: Switch seamlessly between standard sequential search and the **MRV (Minimum Remaining Values)** heuristic to observe how branch pruning impacts attempts and backtracks.

---

## 2. Key Features

- **Real-Time Visualization**: Step-by-step graphical depiction of recursive trial, error, rejection, and backtracking.
- **Pure DSA Solver**: `solver.py` contains 0 UI dependencies, operating strictly on standard `List[List[int]]` 2D arrays.
- **Two Solving Strategies**:
  - `backtracking`: Sequential scanning (row-by-row, left-to-right).
  - `mrv`: Minimum Remaining Values heuristic (picks the empty cell with the fewest legal candidate numbers).
- **Precise Live Metrics**:
  - **Attempts**: Every candidate digit (1–9) tested via `is_valid()`.
  - **Backtracks**: Every time a placed candidate is undone (`board[r][c] = 0`) after a branch failure.
  - **Execution Time**: Real-time timer tracking wall-clock solving duration.
  - **Empty Cells**: Live counter of remaining unassigned cells.
- **Empirically Verified Puzzles**: Includes built-in puzzles (`backtrack_demo`, `easy`, `medium`, `hard`, `unsolvable`) with guaranteed, predictable search spaces.
- **Graceful Failure Handling**: Accurately detects mathematically unsolvable boards without crashing or infinite loops.
- **Dual Mode**: Interactive graphical interface (Pygame) or instant headless terminal benchmark (`--cli`).

---

## 3. System Architecture

The project enforces a strict **Separation of Concerns**: rendering and user events are completely decoupled from algorithmic computation.

```
+-------------------------------------------------------+
|                      Pygame UI                        |
|   (main.py, visualizer.py: 9x9 Grid, Stats, Buttons)  |
+---------------------------+---------------------------+
                            |
           Passes raw 2D    | Optional step_callback(r, c, val, event)
           List[List[int]]  |
                            v
+-------------------------------------------------------+
|                   Solver Controller                   |
|                      (solver.py)                      |
|                                                       |
|   +-------------------+       +-------------------+   |
|   |  find_empty()     |  OR   |  find_empty_mrv() |   |
|   |  (Sequential)     |       |  (Heuristic)      |   |
|   +-------------------+       +-------------------+   |
|                             |                         |
|                             v                         |
|               +---------------------------+           |
|               | is_valid(board, r, c, num)|           |
|               | (Row, Column, 3x3 Box)    |           |
|               +---------------------------+           |
|                             |                         |
|                             v                         |
|               +---------------------------+           |
|               |  solve(board) [Recursion] |           |
|               |  - Place candidate        |           |
|               |  - Recurse                |           |
|               |  - Backtrack (board=0)    |           |
|               +---------------------------+           |
+-------------------------------------------------------+
```

### Why this architecture matters:

- **Testability**: Because `solver.py` has no UI imports, unit tests can execute and verify puzzle logic in milliseconds.
- **Simplicity**: No threads, async event loops, or complex message buses. The visualizer synchronizes with the recursive solver via a simple callback parameter.

---

## 4. Algorithms Explained

### A. Standard Recursive Backtracking

Backtracking is a depth-first search (DFS) over the game's state-space tree:

1. **Find Empty Cell**: Scans row-by-row for the first cell containing `0`.
2. **Base Case**: If no empty cells exist, the board is solved (`return True`).
3. **Candidate Loop**: Try digits `1` through `9`:
   - Test validity using `is_valid(board, row, col, num)`.
   - If valid, assign `board[row][col] = num`.
   - Recursively call `solve(board)`.
   - If the recursive call returns `True`, propagate `True` up the stack.
   - If it returns `False`, undo the assignment (`board[row][col] = 0`) and proceed to the next digit.
4. **Dead End**: If digits 1–9 all fail, return `False` to signal the previous caller to backtrack.

### B. Backtracking + MRV Heuristic

Standard backtracking chooses cells in a static, sequential order regardless of puzzle constraints.

**Minimum Remaining Values (MRV)** dynamically chooses the empty cell that has the **fewest legal candidate values**:

- **Pruning the Branching Factor**: If Cell A has 6 legal options and Cell B has only 1 legal option, picking Cell B first drastically reduces the branching factor at the top of the search tree.
- **Fail-First Principle**: If any cell currently has **0 legal candidates**, MRV selects it immediately. Because no digit 1–9 is valid, the candidate loop fails instantly, triggering immediate backtracking rather than exploring dozens of doomed branches.

> [!NOTE]
> **Heuristic Trade-off**: MRV computes candidate counts for all empty cells at every recursive step. While it often dramatically reduces the number of attempts and backtracks, the per-node computation is higher. Whether it is faster in wall-clock time depends on the specific puzzle.

---

## 5. Complexity Analysis

### Time Complexity

- **Worst-Case Upper Bound (Generalized $N \times N$ Sudoku)**: Solving generalized $N \times N$ Sudoku is NP-complete. For a board with $E$ empty cells, a naive brute-force search would examine $9^E$ combinations in the worst case.
- **With Backtracking & Constraint Propagation**: Constraint validation (`is_valid`) prunes the vast majority of search branches early. For a standard 9x9 board, each constraint check takes $O(1)$ operations ($3 \times 9 = 27$ comparisons).
- **Practical 9x9 Execution**: For our verified puzzles, standard backtracking finishes in $10^2$ to $10^4$ attempts, taking less than **0.02 seconds** headless.

### Space Complexity

- **Grid Storage**: $O(1)$ auxiliary space for the fixed $9 \times 9$ integer array ($81$ ints).
- **Recursion Call Stack**: At most $E$ stack frames, where $E \le 81$ is the number of empty cells. Therefore, maximum call stack depth is $O(E) \le 81$, which is well within Python's default recursion limit ($1000$).
- **Overall Space**: $O(1)$ space complexity for fixed 9x9 Sudoku.

---

## 6. Installation & Execution

### Prerequisites

- Python 3.11+ (Fully tested on Python 3.13)
- Pygame 2.5+

### Installation

```bash
# Clone or navigate to the repository
cd "Sudoku Solver Visualizer"

# Install dependencies
pip install -r requirements.txt
```

### Running the Application

**Interactive GUI Mode (Default):**

```bash
python main.py
```

**Headless CLI Benchmark Mode:**

```bash
python main.py --cli
```

---

## 7. Controls & Hotkeys

| Action               | UI Button    | Keyboard Shortcut |
| :------------------- | :----------- | :---------------- |
| **Start Solving**    | `Solve`      | `[Space]`         |
| **Reset Board**      | `Reset`      | `[R]` or `[Esc]`  |
| **Toggle Algorithm** | `Algo: ...`  | `[A]`             |
| **Cycle Puzzle**     | `Puz: ...`   | `[P]`             |
| **Toggle Speed**     | `Speed: ...` | `[S]`             |

---

## 8. Empirical Puzzle Benchmarks

All built-in puzzles have been empirically verified:

| Puzzle             | Algorithm    | Status        | Attempts | Backtracks | Headless Time |
| :----------------- | :----------- | :------------ | :------- | :--------- | :------------ |
| **backtrack_demo** | Backtracking | Solved        | 307      | 9          | 0.0006 s      |
| **backtrack_demo** | MRV          | Solved        | 226      | 0          | 0.0135 s      |
| **easy**           | Backtracking | Solved        | 96       | 0          | 0.0002 s      |
| **easy**           | MRV          | Solved        | 96       | 0          | 0.0024 s      |
| **medium**         | Backtracking | Solved        | 1,605    | 151        | 0.0020 s      |
| **medium**         | MRV          | Solved        | 246      | 0          | 0.0133 s      |
| **hard**           | Backtracking | Solved        | 9,318    | 1,004      | 0.0116 s      |
| **hard**           | MRV          | Solved        | 2,883    | 289        | 0.1134 s      |
| **unsolvable**     | Backtracking | Failed (Safe) | 963      | 106        | 0.0012 s      |
| **unsolvable**     | MRV          | Failed (Safe) | 9        | 0          | 0.0002 s      |

---

## 9. Live Configuration Demonstrations

To observe how algorithmic heuristics and speed configurations alter execution in real time:

### Demo 1: Algorithmic Strategy Change

Open `config.py` line 14:

```python
# Change from:
SOLVER_ALGORITHM = "backtracking"
# To:
SOLVER_ALGORITHM = "mrv"
```

_Rerun `python main.py`. Observe that attempts drop from 307 to 226 and backtracks drop from 9 to 0 on the demo puzzle._

### Demo 2: Visualization Speed Change

Open `config.py` line 21:

```python
# Change from:
ANIMATION_DELAY = 0.05
# To:
ANIMATION_DELAY = 0.00
```

_Rerun `python main.py`. The solver executes at maximum speed while still rendering the final completed solution._

---

## 10. Automated Testing

Run the full unit test suite using Python's built-in `unittest` runner:

```bash
python -m unittest discover -s tests -p "test_*.py" -v
```

All 15 tests execute and pass in under 0.05 seconds.

---

## 11. Future Improvements

- **Interactive Cell Editing**: Allow users to click empty cells and type custom numbers.
- **Additional Heuristics**: Degree Heuristic (selecting cell with most constraints on other unassigned cells) or Least Constraining Value (LCV).
- **Puzzle Generator**: Random board generator using randomized backtracking and clue-removal with uniqueness validation.
