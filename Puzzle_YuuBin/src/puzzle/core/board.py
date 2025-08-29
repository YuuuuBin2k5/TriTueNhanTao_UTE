"""Trợ giúp Board: lớp nhẹ bao bọc trạng thái 8-puzzle.

Lớp này là một wrapper tiện lợi xung quanh các hàm thuần trong
`puzzle.core.utils` nếu tồn tại. Nó lưu trữ trạng thái bảng và
cung cấp các phương thức đơn giản để UI sử dụng.
"""
from copy import deepcopy
import importlib
from typing import List, Optional, Tuple

try:
    utils = importlib.import_module("puzzle.core.utils")
except Exception:
    try:
        utils = importlib.import_module("src.puzzle.core.utils")
    except Exception:
        utils = None

BoardType = List[List[int]]


class Board:
    def __init__(self, size: int = 3, board: Optional[BoardType] = None, shuffle_moves: int = 0):
        self.size = size
        if board is not None:
            # sao chép board được cung cấp
            self._board = deepcopy(board)
        else:
            if utils and hasattr(utils, "create_solved_board"):
                self._board = utils.create_solved_board()
            else:
                # fallback: tạo board đã giải
                n = size * size
                flat = [(i + 1) % n for i in range(n)]
                self._board = [flat[i * size:(i + 1) * size] for i in range(size)]

        if shuffle_moves and utils and hasattr(utils, "shuffle_board"):
            self._board = utils.shuffle_board(self._board, moves=shuffle_moves)

    @property
    def board(self) -> BoardType:
    # trả về bản sao để tránh code bên ngoài vô tình sửa state nội bộ
        return deepcopy(self._board)

    def as_list(self) -> List[int]:
        return [v for row in self._board for v in row]

    def find(self, tile: int) -> Optional[Tuple[int, int]]:
        """Tìm vị trí (hàng,cột) của ô có giá trị `tile` hoặc None."""
        if utils and hasattr(utils, "find_tile"):
            return utils.find_tile(self._board, tile)
        for r, row in enumerate(self._board):
            for c, v in enumerate(row):
                if v == tile:
                    return (r, c)
        return None

    def can_move(self, tile: int) -> bool:
        """Trả về True nếu ô có thể di chuyển vào ô trống."""
        if utils and hasattr(utils, "can_move"):
            return utils.can_move(self._board, tile)
        pos = self.find(tile)
        empty = self.find(0)
        if pos is None or empty is None:
            return False
        return abs(pos[0] - empty[0]) + abs(pos[1] - empty[1]) == 1

    def move_tile(self, tile: int) -> bool:
        """Cố gắng di chuyển ô có giá trị `tile`. Trả về True nếu đã di chuyển."""
        if utils and hasattr(utils, "move_tile"):
            newb, moved = utils.move_tile(self._board, tile)
            if moved:
                self._board = newb
            return moved

        # fallback manual swap
        pos = self.find(tile)
        empty = self.find(0)
        if pos is None or empty is None:
            return False
        if abs(pos[0] - empty[0]) + abs(pos[1] - empty[1]) != 1:
            return False
        r1, c1 = pos
        r0, c0 = empty
        self._board[r0][c0], self._board[r1][c1] = self._board[r1][c1], self._board[r0][c0]
        return True

    def is_solved(self) -> bool:
        """Kiểm tra xem board có ở trạng thái đã giải hay không."""
        if utils and hasattr(utils, "is_solved"):
            return utils.is_solved(self._board)
        # fallback
        n = self.size * self.size
        flat = self.as_list()
        return flat == [(i + 1) % n for i in range(n)]

    def shuffle(self, moves: int = 100) -> None:
        """Xáo trộn board bằng `moves` lượt di chuyển hợp lệ (nếu có utils)."""
        if utils and hasattr(utils, "shuffle_board"):
            self._board = utils.shuffle_board(self._board, moves=moves)
        else:
            # fallback: thực hiện các bước di chuyển ngẫu nhiên
            import random
            for _ in range(max(1, moves)):
                empty = self.find(0)
                if not empty:
                    break
                r0, c0 = empty
                choices = []
                for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                    r, c = r0 + dr, c0 + dc
                    if 0 <= r < self.size and 0 <= c < self.size:
                        choices.append(self._board[r][c])
                if not choices:
                    break
                choice = random.choice(choices)
                self.move_tile(choice)

