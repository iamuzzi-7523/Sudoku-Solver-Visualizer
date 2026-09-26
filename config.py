"""
Configuration settings for the Interactive Sudoku Solver & Algorithm Visualizer.

This file contains primary algorithm and visualization settings at the top
to easily compare search strategies and execution speeds.
"""

# =====================================================================
# DEMONSTRATION & RUNTIME SETTINGS
# =====================================================================

# Solving Algorithm Selection
# Change "backtracking" to "mrv" to show how the cell selection heuristic
# prunes the search space and alters the number of attempts and backtracks.
# Options: "backtracking" | "mrv"
SOLVER_ALGORITHM = "backtracking"

# Visualization Speed / Animation Delay (in seconds)
# Change 0.05 to 0.00 to demonstrate high-speed headless-like execution
# vs step-by-step visual pedagogical execution.
# 0.05 = Step-by-step visual demonstration speed
# 0.00 = Maximum speed (near-instant execution)
ANIMATION_DELAY = 0.05

# Default puzzle loaded on startup
# Options: "backtrack_demo", "easy", "medium", "hard", "unsolvable"
DEFAULT_PUZZLE = "backtrack_demo"


# =====================================================================
# WINDOW & DISPLAY SETTINGS
# =====================================================================

WINDOW_WIDTH = 960
WINDOW_HEIGHT = 640
FPS = 60

# 9x9 Board Dimensions
BOARD_X = 40
BOARD_Y = 50
BOARD_SIZE = 540
CELL_SIZE = BOARD_SIZE // 9  # 60 pixels per cell

# Sidebar Dimensions
SIDEBAR_X = 610
SIDEBAR_Y = 50
SIDEBAR_WIDTH = 310
SIDEBAR_HEIGHT = 540


# =====================================================================
# COLOR PALETTE (Clean, high-contrast, modern UI)
# =====================================================================

# Background and Panels
COLOR_BG = (241, 245, 249)            # Slate 100 - soft off-white background
COLOR_PANEL_BG = (255, 255, 255)      # White sidebar panel
COLOR_GRID_BG = (255, 255, 255)       # White board background
COLOR_PANEL_BORDER = (203, 213, 225)  # Slate 300 - subtle border

# Grid Lines
COLOR_GRID_THIN = (203, 213, 225)     # Slate 300 - cell divider
COLOR_GRID_THICK = (30, 41, 59)       # Slate 800 - 3x3 box divider

# Digits
COLOR_ORIGINAL_DIGIT = (15, 23, 42)   # Slate 900 - bold dark for fixed clues
COLOR_SOLVED_DIGIT = (22, 101, 52)    # Green 800 - dark green for solved digits

# Cell State Visual Highlights
COLOR_CELL_NORMAL = (255, 255, 255)   # White
COLOR_CELL_ORIGINAL = (248, 250, 252) # Very light slate
COLOR_CELL_TRYING = (219, 234, 254)   # Blue 100 - currently placed valid candidate
COLOR_CELL_INVALID = (254, 202, 202)  # Red 200 - invalid candidate rejection flash
COLOR_CELL_BACKTRACK = (254, 215, 170)# Orange 200 - backtracking cell clearing flash
COLOR_CELL_SOLVED = (220, 252, 231)   # Green 100 - solved board flash

# Text Colors for Highlights
COLOR_TEXT_TRYING = (29, 78, 216)     # Blue 700
COLOR_TEXT_INVALID = (185, 28, 28)    # Red 700
COLOR_TEXT_BACKTRACK = (194, 65, 12)  # Orange 700

# UI Text & Buttons
COLOR_TEXT_PRIMARY = (15, 23, 42)     # Slate 900
COLOR_TEXT_SECONDARY = (71, 85, 105)  # Slate 600
COLOR_TEXT_MUTED = (148, 163, 184)    # Slate 400

# Button Styles
COLOR_BTN_PRIMARY = (37, 99, 235)     # Blue 600
COLOR_BTN_PRIMARY_HOVER = (29, 78, 216)
COLOR_BTN_SUCCESS = (22, 163, 74)     # Green 600
COLOR_BTN_DANGER = (220, 38, 38)      # Red 600
COLOR_BTN_SECONDARY = (226, 232, 240) # Slate 200
COLOR_BTN_SECONDARY_HOVER = (203, 213, 225)
