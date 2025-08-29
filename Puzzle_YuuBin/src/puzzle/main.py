"""Trình khởi động cho trò puzzle.

Chạy từ thư mục gốc project. Mặc định sử dụng giao diện Pygame.
"""
# puzzle/main.py
import importlib

try:
    # Prefer package-relative import when run with -m
    from .game import Game
except Exception:
    # Fallback for direct script execution: make sure 'src' is on sys.path
    import os
    import sys

    THIS_DIR = os.path.dirname(__file__)      # src/puzzle
    SRC_DIR = os.path.abspath(os.path.join(THIS_DIR, ".."))  # src
    if SRC_DIR not in sys.path:
        sys.path.insert(0, SRC_DIR)
    # import via top-level module name
    Game = importlib.import_module("puzzle.game").Game


if __name__ == "__main__":
    game = Game()
    game.run()
