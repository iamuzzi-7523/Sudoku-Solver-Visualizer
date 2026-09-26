# 5–10 Minute Technical Interview Guide

> **Target Audience**: B.Tech Computer Science Campus Placement Interviewers  
> **Project**: Interactive Sudoku Solver & Algorithm Visualizer

---

## 1. Presentation Timeline (0:00 – 10:00)

```
0:00 - 1:00  | Project Introduction (The Elevator Pitch)
1:00 - 2:00  | Live Screen-Share Demonstration (Pygame UI)
2:00 - 4:00  | Architecture & Separation of Concerns (UI vs Pure DSA)
4:00 - 6:00  | Core Code Walkthrough (solve, is_valid, find_empty_mrv)
6:00 - 8:00  | Live Code Modification (Demo A: MRV switch; Demo B: Speed toggle)
8:00 - 10:00 | Answering Technical & DSA Questions
```

---

## 2. Minute 0:00–1:00: Natural Student Introduction

### What to Say:
> *"Hi, for my technical project I built an Interactive Sudoku Solver and Algorithm Visualizer using Python and Pygame.*  
> *Most solvers simply compute the answer off-screen and show the final board. My goal was to make recursive backtracking and state restoration visually understandable.*  
> *I also implemented the Minimum Remaining Values (MRV) heuristic from constraint satisfaction problems so I could empirically analyze how different cell selection strategies affect search tree depth, attempts, and backtracks.*  
> *I intentionally avoided complex frameworks or external solver libraries. The core solver is pure Python list manipulation so that every line of logic is fully testable and transparent."*

---

## 3. Minute 1:00–2:00: Live Screen-Share Demonstration

### Step-by-Step Action Plan:
1. **Open Terminal** and launch:
   ```bash
   python main.py
   ```
2. **Explain the Interface**:
   - Point out the 9x9 board on the left with fixed clues in bold dark blue.
   - Point out the live metrics on the right: **Attempts**, **Backtracks**, **Execution Time**, and **Empty Cells**.
3. **Press `[Space]` (or click Solve)**:
   - *"Here, the solver explores candidates 1 through 9."*
   - *"When a number violates a row, column, or 3x3 box rule, it briefly flashes red and is rejected."*
   - *"When valid, it turns blue and the solver recurses into the next cell."*
   - *"When it hits a dead end in row 1, watch the cell turn orange: it resets to 0 and backtracks to try the next alternative."*
4. **Completion**:
   - Point out the solved green board and final statistics (Attempts: 307, Backtracks: 9).

---

## 4. Minute 2:00–4:00: Architecture Explanation

### What to Open:
Show the project directory in your editor:
```
├── main.py        (Event loop & user interaction)
├── visualizer.py  (Pygame graphics, rendering & buttons)
├── board.py       (UI board state & original clue tracking)
├── solver.py      (PURE DSA logic: recursion, validation, MRV)
├── puzzles.py     (Empirically benchmarked puzzles)
└── config.py      (Centralized interview configuration switches)
```

### Key Talking Point (Separation of Concerns):
> *"One critical design decision I made was keeping `solver.py` completely independent from Pygame and the UI.*  
> *`solver.py` does not import Pygame, does not use UI classes, and operates solely on standard `List[List[int]]` 2D arrays.*  
> *To visualize solving without tangling the algorithm with rendering code, the `solve()` function accepts an optional `callback(r, c, val, event_type)`.*  
> *This means our automated unit tests can run the exact same solver headless in under 0.03 seconds."*

---

## 5. Minute 4:00–6:00: Core Code Walkthrough

Open [solver.py](file:///e:/AI/projects/Sudoku%20Solver%20Visualizer/solver.py) and show these exact functions in order:

### 1. `is_valid(board, row, col, num)`
```python
def is_valid(board: List[List[int]], row: int, col: int, num: int) -> bool:
    # 1. Row check
    for c in range(9):
        if board[row][c] == num:
            return False
    # 2. Column check
    for r in range(9):
        if board[r][col] == num:
            return False
    # 3. 3x3 Box check
    box_start_row = (row // 3) * 3
    box_start_col = (col // 3) * 3
    for r in range(box_start_row, box_start_row + 3):
        for c in range(box_start_col, box_start_col + 3):
            if board[r][c] == num:
                return False
    return True
```
- **Explain**: Checks row, column, and 3x3 box in 27 constant-time operations ($O(1)$).
- **Likely Question**: *"Why `(row // 3) * 3`?"*
  - **Answer**: *"Integer division maps rows 0, 1, 2 to 0; 3, 4, 5 to 3; and 6, 7, 8 to 6, giving the top-left index of that 3x3 box."*

---

### 2. `solve(board, algorithm, callback, stats)`
```python
    if empty is None:
        return True  # Base Case: puzzle complete!

    row, col = empty
    for num in range(1, 10):
        if is_valid(board, row, col, num):
            board[row][col] = num           # 1. Place candidate
            if solve(board, ...):           # 2. Recurse
                return True
            board[row][col] = 0             # 3. Backtrack (Reset to 0)
    return False                            # 4. Dead end
```
- **Explain**:
  - The **Base Case** is when `empty is None` (all 81 cells filled legally).
  - Highlighting **State Restoration**: Point out `board[row][col] = 0`. *"If I forget to reset this to 0, future recursive branches would see this cell as occupied, corrupting the search state."*

---

### 3. `find_empty_mrv(board)`
```python
def find_empty_mrv(board: List[List[int]]) -> Optional[Tuple[int, int]]:
    best_cell = None
    min_legal_count = 10
    for r in range(9):
        for c in range(9):
            if board[r][c] == 0:
                legal_count = sum(1 for n in range(1, 10) if is_valid(board, r, c, n))
                if legal_count == 0:
                    return (r, c)  # Fail-first optimization!
                if legal_count < min_legal_count:
                    min_legal_count = legal_count
                    best_cell = (r, c)
    return best_cell
```
- **Explain**:
  - *"Instead of choosing the next empty cell sequentially, MRV counts valid candidate digits for every empty cell and chooses the most constrained one."*
  - *"Notice the fail-first check: if a cell has 0 valid candidates, this board state cannot possibly lead to a solution. Returning that cell immediately causes the candidate loop to fail and backtrack right away, saving hundreds of doomed branches."*

---

## 6. Minute 6:00–8:00: Live Code Modification

Tell the interviewer:
> *"Now I'd like to make a quick live code change to demonstrate the difference between the two search strategies."*

### LIVE DEMO A: Algorithmic Change
1. Open [config.py](file:///e:/AI/projects/Sudoku%20Solver%20Visualizer/config.py#L14).
2. Change line 14:
   ```python
   # Original:
   SOLVER_ALGORITHM = "backtracking"

   # Change to:
   SOLVER_ALGORITHM = "mrv"
   ```
3. Save the file and rerun:
   ```bash
   python main.py
   ```
4. Press `[Space]` to solve.
5. **Point out the metrics comparison**:
   - **Backtracking**: 307 attempts, 9 backtracks.
   - **MRV**: 226 attempts, 0 backtracks!
   - *"MRV selected cells with fewer choices first, effectively eliminating unnecessary search paths."*

---

### LIVE DEMO B: Runtime / Visualization Speed Change
1. Open [config.py](file:///e:/AI/projects/Sudoku%20Solver%20Visualizer/config.py#L21).
2. Change line 21:
   ```python
   # Original:
   ANIMATION_DELAY = 0.05

   # Change to:
   ANIMATION_DELAY = 0.00
   ```
3. Save and rerun:
   ```bash
   python main.py
   ```
4. Press `[Space]`. It solves in milliseconds.
5. Explain: *"This demonstrates that the delay controls visual pacing for pedagogical purposes, while the underlying algorithmic complexity remains identical."*

---

## 7. Minute 8:00–10:00: Expected Interview Questions & Quick Answers

| Question | Recommended Answer |
| :--- | :--- |
| **What is the worst-case time complexity?** | *"Sudoku generalized to $N \times N$ is NP-complete with exponential worst-case $9^E$ where $E$ is empty cells. For a fixed 9x9 board with backtracking constraint checks, practical execution takes between $10^2$ and $10^4$ operations."* |
| **What is the space complexity?** | *"Auxiliary space is $O(1)$ for the 9x9 board ($81$ ints). Call stack space is bounded by the number of empty cells ($E \le 81$), which easily fits within Python's default stack limit of 1000."* |
| **Why not use a 1D list instead of a 2D list?** | *"A 1D list of length 81 with index arithmetic `r * 9 + c` works, but a 2D list `board[r][c]` directly mirrors the row-column geometry of Sudoku, making constraint validation and interview explanations much cleaner."* |
| **Does MRV always solve faster than standard backtracking?** | *"No. MRV calculates candidate counts across all empty cells at every step. While it usually reduces attempts and backtracks, the per-step overhead can make it slightly slower in wall-clock time on very easy puzzles."* |
| **What happens if a puzzle has no solution?** | *"All candidate numbers 1–9 fail in the root cell, and `solve()` returns `False`. The visualizer catches this and displays a clear 'Unsolvable' status without crashing."* |
