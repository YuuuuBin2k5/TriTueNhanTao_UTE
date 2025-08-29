# Bài 3
# @author: Đào Nguyễn Nhật Anh
# @date: 2025-8-21
# @description: Bài tập 3


# Tọa độ
dx = [-1, -2, 1, 2, -1, -2, 1, 2]
dy = [-2, -1, 2, 1, 2, 1, -2, -1]

# Kiểm tra nước đi
def check_value(x, y, board, N):
    return 0 <= x < N and 0 <= y < N and board[x][y] == -1 #board để check ô có đi qua chưa


def inBanCo(board):
    for row in board:
        print(row)
    print()

def solve_knight_tour(N):
    # tạo bàn cờ N x N, -1 nghĩa là chưa đi
    board = [[-1 for _ in range(N)] for _ in range(N)]

    # xuất phát từ ô (0,0)
    board[0][0] = 0

    if not solve_util(0, 0, 1, board, N):
        print("Không tìm thấy lời giải")
    else:
        print("Mã đi tuần:")
        inBanCo(board)

def solve_util(x, y, step, board, N):
    # nếu đã đi hết tất cả ô
    if step == N * N:
        return True

    # thử tất cả 8 hướng
    for i in range(8):
        nx, ny = x + dx[i], y + dy[i]
        if check_value(nx, ny, board, N):
            board[nx][ny] = step
            if solve_util(nx, ny, step + 1, board, N):
                return True
            board[nx][ny] = -1  # quay lui

    return False

# chạy thử
if __name__ == "__main__":
    N = int(input("Nhập kích thước bàn cờ (N): "))
    solve_knight_tour(N)

    