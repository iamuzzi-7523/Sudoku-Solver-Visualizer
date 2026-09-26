"""
Pygame Visualizer for the Interactive Sudoku Solver.

Renders:
1. The 9x9 Sudoku grid with thick 3x3 box borders and thin cell borders.
2. Color-coded cell states (Original, Trying, Invalid Rejection, Backtrack, Solved).
3. Live Statistics Dashboard (Algorithm, Attempts, Backtracks, Time, Empty Cells).
4. Control Buttons (Solve, Reset, Algorithm, Puzzle, Speed) with click & hover states.
5. System Status Messages (Ready, Solving, Solved, Unsolvable).
"""

import pygame
from typing import Dict, Tuple, Optional, Callable
import config
from board import SudokuBoard
from solver import SolverStats


class Button:
    """Clickable UI button with hover effects and clean text rendering."""

    def __init__(
        self,
        rect: Tuple[int, int, int, int],
        text: str,
        callback: Callable[[], None],
        bg_color: Tuple[int, int, int] = config.COLOR_BTN_PRIMARY,
        hover_color: Tuple[int, int, int] = config.COLOR_BTN_PRIMARY_HOVER,
        text_color: Tuple[int, int, int] = (255, 255, 255),
    ):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.callback = callback
        self.bg_color = bg_color
        self.hover_color = hover_color
        self.text_color = text_color
        self.is_hovered = False

    def update(self, mouse_pos: Tuple[int, int]) -> None:
        """Update hover state based on cursor position."""
        self.is_hovered = self.rect.collidepoint(mouse_pos)

    def draw(self, surface: pygame.Surface, font: pygame.font.Font) -> None:
        """Render the button with rounded corners."""
        color = self.hover_color if self.is_hovered else self.bg_color
        pygame.draw.rect(surface, color, self.rect, border_radius=6)
        pygame.draw.rect(surface, config.COLOR_PANEL_BORDER, self.rect, width=1, border_radius=6)

        text_surf = font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def handle_event(self, event: pygame.event.Event) -> bool:
        """Trigger callback on mouse button click."""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.is_hovered:
                self.callback()
                return True
        return False


class SudokuVisualizer:
    """Handles all graphics rendering and UI presentation via Pygame."""

    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.init_fonts()
        self.buttons: Dict[str, Button] = {}
        self.status_message: str = "Ready to solve (Press Space or click Solve)"
        self.status_color: Tuple[int, int, int] = config.COLOR_TEXT_SECONDARY

    def init_fonts(self) -> None:
        """Initialize system fonts with clean typography."""
        font_family = "segoeui,arial,helvetica,sans-serif"
        self.font_large = pygame.font.SysFont(font_family, 26, bold=True)
        self.font_cell = pygame.font.SysFont(font_family, 28, bold=True)
        self.font_title = pygame.font.SysFont(font_family, 18, bold=True)
        self.font_regular = pygame.font.SysFont(font_family, 14)
        self.font_bold = pygame.font.SysFont(font_family, 14, bold=True)
        self.font_small = pygame.font.SysFont(font_family, 12)
        self.font_badge = pygame.font.SysFont(font_family, 12, bold=True)

    def set_status(self, message: str, color: Tuple[int, int, int] = config.COLOR_TEXT_SECONDARY) -> None:
        """Update the status message displayed at the bottom of the sidebar."""
        self.status_message = message
        self.status_color = color

    def draw_board(self, board: SudokuBoard) -> None:
        """Draw the 9x9 Sudoku board, cell backgrounds, and numbers."""
        bx = config.BOARD_X
        by = config.BOARD_Y
        cell_size = config.CELL_SIZE

        # Draw board background
        board_rect = pygame.Rect(bx, by, config.BOARD_SIZE, config.BOARD_SIZE)
        pygame.draw.rect(self.screen, config.COLOR_GRID_BG, board_rect)

        # 1. Draw cell background highlights & numbers
        for r in range(9):
            for c in range(9):
                cx = bx + c * cell_size
                cy = by + r * cell_size
                cell_rect = pygame.Rect(cx, cy, cell_size, cell_size)

                val = board.get_cell(r, c)
                state = board.get_state(r, c)
                is_orig = board.is_original(r, c)

                # Determine background fill color
                if is_orig:
                    bg_color = config.COLOR_CELL_ORIGINAL
                elif state == "invalid":
                    bg_color = config.COLOR_CELL_INVALID
                elif state == "trying":
                    bg_color = config.COLOR_CELL_TRYING
                elif state == "backtrack":
                    bg_color = config.COLOR_CELL_BACKTRACK
                elif state == "solved":
                    bg_color = config.COLOR_CELL_SOLVED
                else:
                    bg_color = config.COLOR_CELL_NORMAL

                pygame.draw.rect(self.screen, bg_color, cell_rect)

                # Determine text color and render value
                if val != 0:
                    if is_orig:
                        num_color = config.COLOR_ORIGINAL_DIGIT
                    elif state == "invalid":
                        num_color = config.COLOR_TEXT_INVALID
                    elif state == "trying":
                        num_color = config.COLOR_TEXT_TRYING
                    elif state == "backtrack":
                        num_color = config.COLOR_TEXT_BACKTRACK
                    elif state == "solved":
                        num_color = config.COLOR_SOLVED_DIGIT
                    else:
                        num_color = config.COLOR_TEXT_PRIMARY

                    txt_surf = self.font_cell.render(str(val), True, num_color)
                    txt_rect = txt_surf.get_rect(center=cell_rect.center)
                    self.screen.blit(txt_surf, txt_rect)

        # 2. Draw grid lines (thin for cells, thick for 3x3 boxes)
        for i in range(10):
            # Line thickness
            width = 3 if (i % 3 == 0) else 1
            color = config.COLOR_GRID_THICK if (i % 3 == 0) else config.COLOR_GRID_THIN

            # Horizontal lines
            y = by + i * cell_size
            pygame.draw.line(self.screen, color, (bx, y), (bx + config.BOARD_SIZE, y), width)

            # Vertical lines
            x = bx + i * cell_size
            pygame.draw.line(self.screen, color, (x, by), (x, by + config.BOARD_SIZE), width)

    def draw_sidebar(
        self,
        board: SudokuBoard,
        stats: SolverStats,
        current_algo: str,
        current_puzzle: str,
        animation_delay: float,
    ) -> None:
        """Render the statistics dashboard, legend, buttons, and status banner."""
        sx = config.SIDEBAR_X
        sy = config.SIDEBAR_Y
        sw = config.SIDEBAR_WIDTH
        sh = config.SIDEBAR_HEIGHT

        # Draw main sidebar container panel
        panel_rect = pygame.Rect(sx, sy, sw, sh)
        pygame.draw.rect(self.screen, config.COLOR_PANEL_BG, panel_rect, border_radius=10)
        pygame.draw.rect(self.screen, config.COLOR_PANEL_BORDER, panel_rect, width=1, border_radius=10)

        curr_y = sy + 16

        # Header Title
        title_surf = self.font_title.render("ALGORITHM VISUALIZER", True, config.COLOR_TEXT_PRIMARY)
        self.screen.blit(title_surf, (sx + 20, curr_y))
        curr_y += 24

        # Active Algorithm Badge
        badge_text = "Backtracking (Sequential)" if current_algo == "backtracking" else "Backtracking + MRV"
        badge_bg = (238, 242, 255) if current_algo == "backtracking" else (243, 232, 255)
        badge_fg = (79, 70, 229) if current_algo == "backtracking" else (147, 51, 234)

        badge_surf = self.font_badge.render(f"Mode: {badge_text}", True, badge_fg)
        badge_rect = pygame.Rect(sx + 20, curr_y, badge_surf.get_width() + 16, 22)
        pygame.draw.rect(self.screen, badge_bg, badge_rect, border_radius=4)
        self.screen.blit(badge_surf, (sx + 28, curr_y + 3))
        curr_y += 32

        # Divider
        pygame.draw.line(self.screen, config.COLOR_PANEL_BORDER, (sx + 20, curr_y), (sx + sw - 20, curr_y), 1)
        curr_y += 12

        # ---------------- Statistics Section ----------------
        stat_title = self.font_bold.render("LIVE METRICS", True, config.COLOR_TEXT_SECONDARY)
        self.screen.blit(stat_title, (sx + 20, curr_y))
        curr_y += 22

        metrics = [
            ("Attempts:", f"{stats.attempts:,}"),
            ("Backtracks:", f"{stats.backtracks:,}"),
            ("Execution Time:", f"{stats.elapsed_time:.3f} s"),
            ("Empty Cells:", f"{board.count_empty()} / 81"),
        ]

        for label, val_str in metrics:
            lbl_surf = self.font_regular.render(label, True, config.COLOR_TEXT_SECONDARY)
            val_surf = self.font_bold.render(val_str, True, config.COLOR_TEXT_PRIMARY)
            self.screen.blit(lbl_surf, (sx + 20, curr_y))
            self.screen.blit(val_surf, (sx + sw - 20 - val_surf.get_width(), curr_y))
            curr_y += 20

        curr_y += 8
        pygame.draw.line(self.screen, config.COLOR_PANEL_BORDER, (sx + 20, curr_y), (sx + sw - 20, curr_y), 1)
        curr_y += 12

        # ---------------- Legend Section ----------------
        leg_title = self.font_bold.render("VISUAL LEGEND", True, config.COLOR_TEXT_SECONDARY)
        self.screen.blit(leg_title, (sx + 20, curr_y))
        curr_y += 20

        legend_items = [
            (config.COLOR_CELL_TRYING, "Valid Candidate Placed"),
            (config.COLOR_CELL_INVALID, "Invalid Candidate (Rejected)"),
            (config.COLOR_CELL_BACKTRACK, "Backtracking (Dead-End Reset)"),
            (config.COLOR_CELL_SOLVED, "Solved Solution"),
        ]

        for col, desc in legend_items:
            # Color swatch
            swatch_rect = pygame.Rect(sx + 20, curr_y + 2, 14, 14)
            pygame.draw.rect(self.screen, col, swatch_rect, border_radius=3)
            pygame.draw.rect(self.screen, config.COLOR_PANEL_BORDER, swatch_rect, width=1, border_radius=3)
            # Label
            desc_surf = self.font_small.render(desc, True, config.COLOR_TEXT_SECONDARY)
            self.screen.blit(desc_surf, (sx + 42, curr_y + 1))
            curr_y += 20

        curr_y += 8
        pygame.draw.line(self.screen, config.COLOR_PANEL_BORDER, (sx + 20, curr_y), (sx + sw - 20, curr_y), 1)
        curr_y += 12

        # ---------------- Control Buttons Section ----------------
        btn_font = self.font_bold
        for btn in self.buttons.values():
            btn.draw(self.screen, btn_font)

        # ---------------- Status Banner at Bottom ----------------
        status_box_rect = pygame.Rect(sx + 20, sy + sh - 48, sw - 40, 32)
        pygame.draw.rect(self.screen, config.COLOR_BG, status_box_rect, border_radius=6)
        pygame.draw.rect(self.screen, config.COLOR_PANEL_BORDER, status_box_rect, width=1, border_radius=6)

        msg_surf = self.font_small.render(self.status_message, True, self.status_color)
        msg_rect = msg_surf.get_rect(center=status_box_rect.center)
        self.screen.blit(msg_surf, msg_rect)

    def render(
        self,
        board: SudokuBoard,
        stats: SolverStats,
        current_algo: str,
        current_puzzle: str,
        animation_delay: float,
    ) -> None:
        """Render the complete scene onto the display."""
        self.screen.fill(config.COLOR_BG)
        self.draw_board(board)
        self.draw_sidebar(board, stats, current_algo, current_puzzle, animation_delay)
        pygame.display.flip()
