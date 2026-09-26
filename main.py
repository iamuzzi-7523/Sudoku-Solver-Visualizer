"""
Main Application Entry Point for Interactive Sudoku Solver & Algorithm Visualizer.

Provides:
- Interactive Pygame GUI loop with real-time algorithm visualization
- Headless CLI mode (via '--cli' flag) for fast testing and automated evaluation
- Hotkey controls:
    [Space] : Start solving
    [R]     : Reset board / abort current solve
    [A]     : Toggle algorithm (Standard Backtracking vs MRV Heuristic)
    [P]     : Cycle through puzzles (Demo, Easy, Medium, Hard, Unsolvable)
    [S]     : Toggle animation speed (0.05s vs 0.00s)
"""

import sys
import time
import argparse
import warnings

# Suppress known harmless Pygame 2.6.1 pkg_resources deprecation warning on Python 3.13
warnings.filterwarnings("ignore", message=".*pkg_resources is deprecated.*")

import pygame
import config
import puzzles
import solver
from board import SudokuBoard
from visualizer import SudokuVisualizer, Button


class StopSolvingException(Exception):
    """Exception raised when user requests to abort or reset during solving."""
    pass


class SudokuApp:
    """Coordinates the Pygame UI, user inputs, and the Sudoku solver."""

    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Sudoku Solver & Algorithm Visualizer")

        self.screen = pygame.display.set_mode((config.WINDOW_WIDTH, config.WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()
        self.visualizer = SudokuVisualizer(self.screen)

        # State initialization from config.py defaults
        self.current_algo: str = config.SOLVER_ALGORITHM
        self.current_delay: float = config.ANIMATION_DELAY
        self.current_puzzle: str = config.DEFAULT_PUZZLE
        self.is_solving: bool = False

        self.board = SudokuBoard(self.current_puzzle)
        self.stats = solver.SolverStats(self.current_algo)

        # Setup sidebar buttons
        self.setup_buttons()

    def setup_buttons(self) -> None:
        """Create and position interactive buttons in the sidebar."""
        sx = config.SIDEBAR_X
        sy = config.SIDEBAR_Y

        # Row 1: Solve and Reset
        btn_solve = Button(
            rect=(sx + 20, sy + 355, 130, 32),
            text="Solve (Space)",
            callback=self.on_solve_clicked,
            bg_color=config.COLOR_BTN_SUCCESS,
            hover_color=(21, 128, 61),
        )
        btn_reset = Button(
            rect=(sx + 160, sy + 355, 130, 32),
            text="Reset (R)",
            callback=self.on_reset_clicked,
            bg_color=config.COLOR_BTN_DANGER,
            hover_color=(185, 28, 28),
        )

        # Row 2: Algorithm Switcher
        btn_algo = Button(
            rect=(sx + 20, sy + 395, 270, 32),
            text=f"Algo: {self.current_algo.upper()}",
            callback=self.on_toggle_algo_clicked,
            bg_color=config.COLOR_BTN_PRIMARY,
            hover_color=config.COLOR_BTN_PRIMARY_HOVER,
        )

        # Row 3: Puzzle Switcher and Speed Toggle
        btn_puzzle = Button(
            rect=(sx + 20, sy + 435, 130, 32),
            text=f"Puz: {self.current_puzzle[:7]}",
            callback=self.on_cycle_puzzle_clicked,
            bg_color=config.COLOR_BTN_SECONDARY,
            hover_color=config.COLOR_BTN_SECONDARY_HOVER,
            text_color=config.COLOR_TEXT_PRIMARY,
        )
        btn_speed = Button(
            rect=(sx + 160, sy + 435, 130, 32),
            text=f"Speed: {'Fast' if self.current_delay == 0.0 else 'Norm'}",
            callback=self.on_toggle_speed_clicked,
            bg_color=config.COLOR_BTN_SECONDARY,
            hover_color=config.COLOR_BTN_SECONDARY_HOVER,
            text_color=config.COLOR_TEXT_PRIMARY,
        )

        self.visualizer.buttons = {
            "solve": btn_solve,
            "reset": btn_reset,
            "algo": btn_algo,
            "puzzle": btn_puzzle,
            "speed": btn_speed,
        }

    def update_button_labels(self) -> None:
        """Refresh button texts when state changes."""
        self.visualizer.buttons["algo"].text = f"Algo: {self.current_algo.upper()}"
        self.visualizer.buttons["puzzle"].text = f"Puz: {self.current_puzzle[:7]}"
        self.visualizer.buttons["speed"].text = f"Speed: {'Fast' if self.current_delay == 0.0 else 'Norm'}"

    # ---------------- Button & Hotkey Handlers ----------------

    def on_solve_clicked(self) -> None:
        """Trigger solving process."""
        if self.is_solving:
            return

        # If already solved or filled, reset first
        if self.board.count_empty() == 0:
            self.board.reset()

        self.run_visual_solver()

    def on_reset_clicked(self) -> None:
        """Reset the board to initial clues and clear stats."""
        self.is_solving = False
        self.board.reset()
        self.stats = solver.SolverStats(self.current_algo)
        self.visualizer.set_status("Board reset to initial puzzle state.", config.COLOR_TEXT_SECONDARY)

    def on_toggle_algo_clicked(self) -> None:
        """Toggle between Standard Backtracking and MRV heuristic."""
        if self.is_solving:
            return
        self.current_algo = "mrv" if self.current_algo == "backtracking" else "backtracking"
        self.stats = solver.SolverStats(self.current_algo)
        self.update_button_labels()
        self.visualizer.set_status(f"Switched algorithm to {self.current_algo.upper()}.", config.COLOR_BTN_PRIMARY)

    def on_cycle_puzzle_clicked(self) -> None:
        """Cycle to the next preset puzzle."""
        if self.is_solving:
            return
        names = puzzles.get_puzzle_names()
        curr_idx = names.index(self.current_puzzle) if self.current_puzzle in names else 0
        next_idx = (curr_idx + 1) % len(names)
        self.current_puzzle = names[next_idx]
        self.board.load_puzzle(self.current_puzzle)
        self.stats = solver.SolverStats(self.current_algo)
        self.update_button_labels()
        self.visualizer.set_status(f"Loaded puzzle: {self.current_puzzle.upper()}", config.COLOR_TEXT_SECONDARY)

    def on_toggle_speed_clicked(self) -> None:
        """Toggle animation speed between normal (0.05s) and fast (0.00s)."""
        self.current_delay = 0.00 if self.current_delay > 0.0 else 0.05
        self.update_button_labels()
        speed_label = "Instant (0.00s)" if self.current_delay == 0.0 else "Normal (0.05s)"
        self.visualizer.set_status(f"Speed set to {speed_label}.", config.COLOR_TEXT_SECONDARY)

    # ---------------- Visual Solver Runner ----------------

    def run_visual_solver(self) -> None:
        """
        Execute solver.solve() with real-time Pygame visualization callback.
        """
        self.is_solving = True
        self.visualizer.set_status(f"Solving using {self.current_algo.upper()}...", config.COLOR_BTN_PRIMARY)
        self.stats = solver.SolverStats(self.current_algo)
        self.stats.start()

        def step_callback(row: int, col: int, num: int, event_type: str) -> None:
            # Check for user input during solving (e.g. exit window or abort)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit(0)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r or event.key == pygame.K_ESCAPE:
                        raise StopSolvingException("Solving aborted by user.")

            # Update board state
            if event_type == "trying":
                self.board.set_cell(row, col, num, "trying")
            elif event_type == "invalid":
                self.board.set_cell(row, col, num, "invalid")
            elif event_type == "backtrack":
                self.board.set_cell(row, col, 0, "backtrack")

            # Render display update
            self.visualizer.render(
                self.board,
                self.stats,
                self.current_algo,
                self.current_puzzle,
                self.current_delay,
            )

            # Revert invalid cell back to 0 so rejected digit doesn't linger
            if event_type == "invalid":
                if self.current_delay > 0:
                    time.sleep(self.current_delay)
                self.board.set_cell(row, col, 0, "normal")
            elif self.current_delay > 0:
                time.sleep(self.current_delay)

        try:
            # Run the pure DSA solve function on the raw 2D grid
            success = solver.solve(
                board=self.board.grid,
                algorithm=self.current_algo,
                callback=step_callback,
                stats=self.stats,
            )

            self.stats.stop(success)

            if success:
                self.board.mark_all_solved()
                self.visualizer.set_status(
                    f"Solved! Time: {self.stats.elapsed_time:.3f}s | Backtracks: {self.stats.backtracks}",
                    config.COLOR_BTN_SUCCESS,
                )
            else:
                self.visualizer.set_status(
                    "Unsolvable: No valid solution exists for this puzzle!",
                    config.COLOR_BTN_DANGER,
                )

        except StopSolvingException:
            self.board.reset()
            self.stats.stop(False)
            self.visualizer.set_status("Solving aborted by user.", config.COLOR_TEXT_SECONDARY)

        finally:
            self.is_solving = False

    # ---------------- Main Event Loop ----------------

    def run(self) -> None:
        """Main application loop."""
        running = True
        while running:
            mouse_pos = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.on_solve_clicked()
                    elif event.key == pygame.K_r:
                        self.on_reset_clicked()
                    elif event.key == pygame.K_a:
                        self.on_toggle_algo_clicked()
                    elif event.key == pygame.K_p:
                        self.on_cycle_puzzle_clicked()
                    elif event.key == pygame.K_s:
                        self.on_toggle_speed_clicked()

                # Process button clicks
                if not self.is_solving:
                    for btn in self.visualizer.buttons.values():
                        btn.handle_event(event)

            # Update hover states
            for btn in self.visualizer.buttons.values():
                btn.update(mouse_pos)

            # Render scene
            self.visualizer.render(
                self.board,
                self.stats,
                self.current_algo,
                self.current_puzzle,
                self.current_delay,
            )
            self.clock.tick(config.FPS)

        pygame.quit()


def run_cli() -> None:
    """Run solver in headless terminal mode across all built-in puzzles."""
    print("=" * 70)
    print("INTERACTIVE SUDOKU SOLVER - HEADLESS BENCHMARK MODE")
    print("=" * 70)
    print(f"{'PUZZLE':<16} | {'ALGORITHM':<14} | {'SOLVED':<6} | {'ATTEMPTS':<8} | {'BACKTRACKS':<10} | {'TIME'}")
    print("-" * 70)

    for puzzle_name in puzzles.get_puzzle_names():
        for algo in ["backtracking", "mrv"]:
            grid = puzzles.get_puzzle(puzzle_name)
            stats = solver.SolverStats(algo)
            stats.start()
            is_solved = solver.solve(grid, algorithm=algo, stats=stats)
            stats.stop(is_solved)

            print(
                f"{puzzle_name:<16} | "
                f"{algo:<14} | "
                f"{str(is_solved):<6} | "
                f"{stats.attempts:<8,} | "
                f"{stats.backtracks:<10,} | "
                f"{stats.elapsed_time:.4f} s"
            )
    print("=" * 70)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Sudoku Solver & Algorithm Visualizer")
    parser.add_argument("--cli", action="store_true", help="Run in headless terminal benchmark mode")
    args = parser.parse_args()

    if args.cli:
        run_cli()
    else:
        app = SudokuApp()
        app.run()
