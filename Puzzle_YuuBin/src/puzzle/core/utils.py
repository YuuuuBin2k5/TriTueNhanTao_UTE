"""Các hàm trợ giúp cho trò chơi 8-puzzle.

Module này cung cấp logic thuần cho trò trượt ô 3x3 (8-puzzle):
- tạo bảng ở trạng thái giải đúng
- tìm vị trí ô / ô trống
- kiểm tra và thực hiện phép di chuyển
- xáo trộn bảng bằng các bước di chuyển hợp lệ (đảm bảo có thể giải được)

Tất cả hàm hoạt động trên và trả về cấu trúc danh sách Python thuần (danh sách các danh sách).
"""
from copy import deepcopy
import random
from typing import List, Tuple, Optional


Board = List[List[int]]  # 3x3 board, 0 represents the empty tile


def create_solved_board() -> Board:
	"""Trả về bảng 3x3 ở trạng thái đã giải.

	Ví dụ:
		[[1,2,3],[4,5,6],[7,8,0]]
	"""
	return [[1, 2, 3], [4, 5, 6], [7, 8, 0]]


def find_tile(board: Board, tile: int) -> Optional[Tuple[int, int]]:
	"""Trả về (hàng, cột) của giá trị ô, hoặc None nếu không tìm thấy."""
	for r, row in enumerate(board):
		for c, v in enumerate(row):
			if v == tile:
				return (r, c)
	return None


def is_adjacent(pos1: Tuple[int, int], pos2: Tuple[int, int]) -> bool:
	"""Trả về True nếu hai vị trí kề nhau theo hàng hoặc cột."""
	return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1]) == 1


def can_move(board: Board, tile: int) -> bool:
	"""Trả về True nếu ô có thể di chuyển vào vị trí ô trống."""
	pos = find_tile(board, tile)
	empty = find_tile(board, 0)
	if pos is None or empty is None:
		return False
	return is_adjacent(pos, empty)


def move_tile(board: Board, tile: int) -> Tuple[Board, bool]:
	"""Trả về (board_mới, moved).

	Nếu ô nằm cạnh ô trống thì trả về bảng mới với hai ô hoán vị và moved=True.
	Ngược lại trả về bản sao của bảng ban đầu và moved=False.
	"""
	pos = find_tile(board, tile)
	empty = find_tile(board, 0)
	if pos is None or empty is None:
		return deepcopy(board), False
	if not is_adjacent(pos, empty):
		return deepcopy(board), False

	new_board = deepcopy(board)
	r1, c1 = pos
	r0, c0 = empty
	new_board[r0][c0], new_board[r1][c1] = new_board[r1][c1], new_board[r0][c0]
	return new_board, True


def board_to_list(board: Board) -> List[int]:
	"""Chuyển board thành danh sách 9 số (một chiều)."""
	return [v for row in board for v in row]


def is_solved(board: Board) -> bool:
	"""Trả về True nếu board ở trạng thái đã giải."""
	return board == create_solved_board()


def get_possible_moves(board: Board) -> List[int]:
	"""Trả về danh sách các giá trị ô có thể di chuyển vào ô trống."""
	empty = find_tile(board, 0)
	if empty is None:
		return []
	r0, c0 = empty
	candidates = []
	for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
		r, c = r0 + dr, c0 + dc
		if 0 <= r < 3 and 0 <= c < 3:
			candidates.append(board[r][c])
	return candidates


def shuffle_board(board: Optional[Board] = None, moves: int = 100) -> Board:
	"""Trả về một board đã được xáo trộn bằng `moves` lượt di chuyển hợp lệ.

	Bắt đầu từ board đầu vào hoặc bảng đã giải, thực hiện các hoán vị cạnh
	ô trống ngẫu nhiên. Cách này đảm bảo board có thể giải được.
	"""
	if board is None:
		board = create_solved_board()
	b = deepcopy(board)
	for _ in range(max(1, moves)):
		options = get_possible_moves(b)
		if not options:
			break
		choice = random.choice(options)
		b, _ = move_tile(b, choice)
	return b


