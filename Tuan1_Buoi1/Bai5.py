# Bài 5 - Trò chơi 8 số (VN)
# @author: Đào Nguyễn Nhật Anh
# @date: 2025-08-22

import random

# đáp án đúng
dapAn = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 0]
]

# Hàm in bảng trò chơi
def print_board(board):
    for row in board:
        for x in row:
            if x == 0:
                print("*", end=" ")
            else:
                print(x, end=" ")
        print()  # xuống dòng sau mỗi hàng
    print()


# Tìm vị trí của ô trống (0)
def find_Start(board):
    for i in range(3):
        for j in range(3):
            if board[i][j] == 0:
                return i, j

# Kiểm tra bàn đã thắng chưa
def checkWin(board):
    return board == dapAn

# Di chuyển ô trống
def move(board, direction):
    i, j = find_Start(board) #Vị trí hiện tại
    if direction == "w" and i > 0:  # lên
        board[i][j], board[i-1][j] = board[i-1][j], board[i][j]
    elif direction == "s" and i < 2:  # xuống
        board[i][j], board[i+1][j] = board[i+1][j], board[i][j]
    elif direction == "a" and j > 0:  # trái
        board[i][j], board[i][j-1] = board[i][j-1], board[i][j]
    elif direction == "d" and j < 2:  # phải
        board[i][j], board[i][j+1] = board[i][j+1], board[i][j]
    else:
        print("Không thể di chuyển theo hướng đó!")

# Sinh bàn chơi ngẫu nhiên
def generate_board():
    nums = list(range(9))
    random.shuffle(nums)
    board = [nums[i*3:(i+1)*3] for i in range(3)]
    return board

# --- Chương trình chính ---
if __name__ == "__main__":
    board = generate_board()
    print("Trò chơi 8 số - Sắp xếp về trạng thái đúng!\n")
    print("Điều khiển: w (lên), s (xuống), a (trái), d (phải)\n")

    while True:
        print_board(board)
        if checkWin(board):
            print("🎉 Chúc mừng! Bạn đã giải xong!")
            break

        move_input = input("Nhập bước đi (w/s/a/d): ")
        move(board, move_input)
