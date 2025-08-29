"""Đánh dấu package cấp cao `src`.

File này biến thư mục `src` thành package Python để các import như
`from src.puzzle.game import Game` hoạt động khi chạy bằng `-m`.
"""

__all__ = ["game", "main", "settings", "ui"]