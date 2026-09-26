# Comprehensive Interview Question Bank (35+ Q&As)

Curated questions and student-level answers tailored for technical interviews.

---

## Part 1: Core Python Questions

### Q1. What is the difference between a list and a tuple in Python?
**Answer:** A list is mutable (can be modified after creation with append, remove, or index assignment) and declared with square brackets `[]`. A tuple is immutable (its contents and size cannot change) and declared with parentheses `()`. In this project, the board is represented as a list of lists because cells must be modified and restored in place during backtracking.

### Q2. What does mutability mean, and why is it important in this project?
**Answer:** Mutability means an object's state can change after it is allocated in memory. In this project, `board[row][col] = num` modifies the existing 2D list in place. If the board were immutable (like a tuple of tuples), every candidate placement would require copying the entire 81-element structure, causing significant memory allocations and slowing down recursive execution.

### Q3. How does Python handle function arguments: pass-by-value or pass-by-reference?
**Answer:** Python uses *pass-by-object-reference* (or pass-by-assignment). When passing a mutable object like `board: List[List[int]]`, the function receives a reference to the same list in memory. Changes made inside `solve()` affect the original board. When passing immutable objects like integers (`row`, `col`), reassigning them inside a function does not affect the caller.

### Q4. What is the recursion limit in Python, and how does this project stay safe?
**Answer:** Python has a default recursion limit of 1000 frames to prevent stack overflow from runaway infinite recursion (`sys.getrecursionlimit()`). This project is guaranteed safe because each recursive frame corresponds to filling an empty cell. On a 9x9 board with at most 81 cells, the maximum call stack depth cannot exceed 81, which is far below 1000.

### Q5. What is variable scope in Python, and how does it work inside `solve()`?
**Answer:** Python resolves names using the LEGB rule (Local, Enclosing, Global, Built-in). In `solve()`, variables like `row`, `col`, `empty`, and `num` are local to that specific stack frame. Each recursive invocation gets its own independent local variables, preserving the candidate loop state when deeper calls return.

### Q6. How do Python exceptions work, and where are they used in this project?
**Answer:** Exceptions (`try...except...finally`) handle runtime events and error conditions. In this project, a custom exception `StopSolvingException` is used cleanly to allow the user to abort solving or reset the board mid-execution: when the user presses `[R]`, the event handler raises `StopSolvingException`, which unwinds all active recursive frames immediately and restores the board safely.

### Q7. What are Python type hints, and what benefit do they provide?
**Answer:** Type hints (like `board: List[List[int]]` or `Optional[Tuple[int, int]]`) annotate expected data types for variables, parameters, and return values. They do not impact runtime performance because Python is dynamically typed, but they significantly improve code readability, IDE auto-completion, and static analysis.

### Q8. What is the difference between `deepcopy` and shallow copy?
**Answer:** A shallow copy (`list.copy()` or `lst[:]`) creates a new container but references the same inner child objects. For a 2D list, `board[:]` copies the outer list, but the inner rows still reference the original row lists. A deep copy (or `[row[:] for row in board]`) duplicates both the outer list and each individual row, ensuring full independence.

### Q9. How do Python modules and the `__name__ == "__main__"` idiom work?
**Answer:** Every `.py` file is a module. When executed directly by the Python interpreter (`python main.py`), Python assigns the special variable `__name__ = "__main__"`. If the module is imported elsewhere (`import solver`), `__name__` equals the filename (`"solver"`). This allows files like `main.py` and `solver.py` to contain testable functions alongside runnable entry-point code.

### Q10. What is `time.perf_counter()` and why is it preferred over `time.time()` for benchmarking?
**Answer:** `time.perf_counter()` uses a high-resolution, monotonic hardware clock that cannot go backwards due to system time adjustments. `time.time()` returns wall-clock calendar time, which can drift or be adjusted by the OS. Monotonic clocks are essential for accurate performance profiling.

---

## Part 2: Data Structures & Algorithms Questions

### Q11. What is the difference between Brute Force and Backtracking?
**Answer:** Pure brute force blindly generates all possible combinations ($9^{81}$ for an empty 9x9 board) and checks each completed board at the very end. Backtracking is an optimized depth-first search that applies **constraint validation incrementally**: as soon as a candidate violates a rule, that entire subtree of millions of possibilities is pruned immediately without further exploration.

### Q12. What are the three essential components of a recursive function?
**Answer:**
1. **Base Case**: A terminating condition that stops recursion and returns a result without making further recursive calls (in Sudoku, when no empty cells remain).
2. **Recursive Step**: The function calling itself with a modified, smaller sub-problem (placing a candidate and attempting to solve the remaining empty cells).
3. **Progress Toward Base Case**: Each recursive step reduces the number of empty cells by 1.

### Q13. What is the state-space tree of a backtracking problem?
**Answer:** It is a conceptual tree representing all decision paths. The root node is the initial board. Each node at depth $d$ represents a board state after filling $d$ cells. Edges represent candidate choices ($1$ to $9$). Leaves are either solved boards or dead ends where all candidate choices were exhausted.

### Q14. What causes backtracking in this algorithm?
**Answer:** Backtracking occurs when the solver reaches an empty cell where **none of the numbers 1 through 9 are valid**, or when every valid candidate tested for that cell leads to a subsequent failure. The algorithm must recognize that an earlier decision was incorrect, undo that decision (`board[row][col] = 0`), and try the next alternative in the caller frame.

### Q15. What is the time complexity of the Sudoku solver?
**Answer:** For a generalized $N \times N$ board, Sudoku is NP-complete with exponential worst-case time complexity $O(9^E)$, where $E$ is the number of empty cells. However, for a standard 9x9 board, constraint propagation prunes the vast majority of branches, allowing typical puzzles to solve in $10^2$ to $10^4$ operations (under 0.02 seconds headless).

### Q16. What is the space complexity?
**Answer:** The auxiliary space for the board is $O(1)$ ($9 \times 9 = 81$ integers). The call stack space is proportional to the recursion depth, bounded by the number of empty cells $E \le 81$, giving $O(E) \le O(1)$ for a fixed 9x9 board.

### Q17. What is a Constraint Satisfaction Problem (CSP)?
**Answer:** A CSP consists of a set of variables $X$, domains of values $D$ for each variable, and constraints $C$ that specify allowable combinations of values. In Sudoku, variables are the 81 cells, domains are digits $\{1, \dots, 9\}$, and constraints are all-different across every row, column, and 3x3 block.

### Q18. What is the Minimum Remaining Values (MRV) heuristic?
**Answer:** MRV (also called the "Most Constrained Variable" heuristic) selects the unassigned cell that has the **fewest legal candidate values remaining**. By choosing the most constrained cell first, it minimizes the branching factor at the current node of the search tree.

### Q19. What is the "Fail-First Principle" in constraint satisfaction?
**Answer:** If a search branch is doomed to fail, it is best to fail as early as possible to avoid exploring large dead-end subtrees. In MRV, if any empty cell has 0 valid candidates, picking that cell causes immediate failure on the very next attempt, pruning that branch instantly.

### Q20. Why doesn't MRV always solve faster in wall-clock time?
**Answer:** MRV must scan all empty cells and test candidate validity for each cell at *every* recursive step. This adds $O(E \times 9)$ per-node computational overhead. On very easy puzzles with few backtracks, the overhead of calculating candidate counts can exceed the time saved by pruning, even though attempts and backtracks are reduced.

---

## Part 3: Project-Specific Architecture Questions

### Q21. Why did you choose Python for this project?
**Answer:** Python provides clean, expressive syntax that allows complex recursive algorithms and state restoration to be written clearly in 15–20 lines without boiler-plate clutter. Its standard data structures (`List[List[int]]`) map directly to the 2D grid, making the code easy to read, test, and explain during a 10-minute interview.

### Q22. Why did you choose Pygame over web frameworks like React or Flask?
**Answer:** Pygame runs locally and offline as a standalone desktop application with zero network dependencies, browsers, or web servers. It allows deterministic frame-by-frame rendering and immediate keyboard event handling, which is ideal for real-time algorithm visualization.

### Q23. Why did you separate `solver.py` from `board.py` and `visualizer.py`?
**Answer:** To enforce clean **Separation of Concerns**. `solver.py` contains pure algorithmic logic operating on standard Python lists with zero Pygame imports. This ensures the solver can be tested headless in milliseconds using standard `unittest` without needing a GUI environment.

### Q24. How does the solver communicate with the Pygame UI without threading?
**Answer:** The `solve()` function accepts an optional `callback(row, col, num, event_type)`. Whenever the solver places a number, rejects a candidate, or backtracks, it calls this function. The UI updates the cell state, repaints the display, checks for user interrupt events, and applies `time.sleep(ANIMATION_DELAY)`. If `callback=None`, the solver runs headless at full speed.

### Q25. Why did you use a 2D list instead of a flat 1D list of 81 elements?
**Answer:** A 2D list `board[row][col]` directly models the mathematical rows and columns of Sudoku. While a 1D list with index formula `i = r * 9 + c` works, a 2D list makes constraint validation code (`is_valid`) much more readable and intuitive to defend in an interview.

### Q26. How do you check the 3x3 box constraint in `is_valid()`?
**Answer:**
```python
box_start_row = (row // 3) * 3
box_start_col = (col // 3) * 3
```
Integer division (`// 3`) groups rows 0-2 into 0, 3-5 into 1, and 6-8 into 2. Multiplying by 3 yields the starting row (0, 3, or 6). We then iterate over the 3x3 subgrid using nested loops of range 3.

### Q27. What are your exact definitions of "attempts" and "backtracks"?
**Answer:**
- **Attempts**: The total count of candidate digits (1–9) passed to `is_valid()`. Every time the solver checks a number, `attempts` increments.
- **Backtracks**: The count of times a previously placed candidate is undone (`board[row][col] = 0`) because that branch failed to produce a valid solution.

### Q28. How does your application handle an unsolvable puzzle?
**Answer:** When given an unsolvable puzzle, the solver explores all candidate branches until the root cell's loop completes without finding a solution. The function cleanly returns `False`. The UI catches the `False` return, preserves the board state, and displays `"Unsolvable: No valid solution exists for this puzzle!"` in red without crashing.

### Q29. How would you optimize this solver further?
**Answer:**
1. **Bitmasks / Sets for Constraints**: Instead of looping 9 times to check rows, columns, and boxes, maintain three arrays of bitmasks `rows[9]`, `cols[9]`, and `boxes[9]`. Checking validity would be a bitwise `AND` operation in $O(1)$ CPU time.
2. **Dancing Links (Algorithm X)**: Donald Knuth's exact-cover algorithm represents Sudoku as an exact cover matrix using toroidal doubly linked lists, providing optimal performance for generalized constraint problems.

### Q30. How would you support different Sudoku sizes, such as 4x4 or 16x16?
**Answer:**
Parameterize the grid dimension $N$ and box dimensions $R \times C$ (where $N = R \times C$):
- For 4x4: $N=4, R=2, C=2$, candidate digits 1–4.
- For 16x16: $N=16, R=4, C=4$, candidate digits 1–16.
The `is_valid` loops would iterate up to $N$, and box starting coordinates would use `(row // R) * R` and `(col // C) * C`.

### Q31. What happens if you forget to reset `board[row][col] = 0` during backtracking?
**Answer:** If you don't reset the cell to `0`, the candidate number remains on the board. When subsequent recursive branches test candidates, `is_valid()` will see that cell as already occupied, falsely detecting conflicts. The board state becomes corrupted and the solver will incorrectly report that the puzzle is unsolvable.

### Q32. How can an interviewer verify that your live demo modification works?
**Answer:**
1. In `config.py`, change `SOLVER_ALGORITHM = "backtracking"` to `"mrv"`.
2. Run `python main.py` and press `[Space]`.
3. The UI badge updates to "Mode: Backtracking + MRV".
4. On the demo puzzle, attempts drop from **307** to **226**, and backtracks drop from **9** to **0**. The statistics update dynamically based on actual execution, not hardcoded constants.

### Q33. Why did you avoid using Python threads or multiprocessing for the visualization?
**Answer:** Python's Global Interpreter Lock (GIL) and Pygame's requirement that rendering occurs on the main thread introduce synchronization complexity, race conditions, and deadlocks. By using a lightweight callback mechanism inside the recursive solver, the animation updates synchronously with zero threading overhead.

### Q34. How did you verify that your demo puzzle doesn't freeze the screen-share?
**Answer:** We empirically benchmarked all puzzles in headless mode first. The `backtrack_demo` puzzle takes exactly 307 attempts and 9 backtracks, solving in 0.0006s headless and ~8 seconds visually with `ANIMATION_DELAY = 0.05`. It provides visible trial-and-error without wasting precious interview minutes.

### Q35. What is the difference between unit testing and integration testing in this project?
**Answer:**
- **Unit Testing**: Tests individual functions in isolation (`test_solver.py` tests `is_valid`, `find_empty`, `find_empty_mrv` with specific inputs and outputs).
- **Integration Testing**: Verifies that components work together (e.g. testing that `SudokuBoard`, `solver.solve()`, and callback event streams successfully communicate and produce a fully valid solved board).
