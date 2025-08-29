# Bài 4 - Sudoku console (VN)
# @author: Đào Nguyễn Nhật Anh
# @date: 2025-08-22

from copy import deepcopy
N = 9  # Sudoku chuẩn 9x9

# --- Puzzle gốc (0 = ô trống) ---
puzzle = [
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9]
]

# Bản để người chơi thao tác (bắt đầu copy từ puzzle)
board = deepcopy(puzzle)

# ---------- In bàn ----------
def inBanCo(b):
    # đường phân cách ngang
    for i in range(N):
        if i % 3 == 0 and i != 0:
            print("-" * 21)  
        # đường phân cách dọc
        for j in range(N):
            if j % 3 == 0 and j != 0:
                print("|", end=" ")  
            print(b[i][j] if b[i][j] != 0 else ".", end=" ")
        print()

# ---------- Kiểm tra hợp lệ khi đặt số ----------
def checkSo(b, row, col, num):
    # Hàng
    if num in b[row]:
        return False
    # Cột
    for i in range(N):
        if b[i][col] == num:
            return False
    # Ô 3x3
    sr, sc = row - row % 3, col - col % 3
    for i in range(3):
        for j in range(3):
            if b[sr + i][sc + j] == num:
                return False
    return True

# ---------- Đã điền hết bảng chưa ----------
def checkBanCo(b):
    for i in range(N):
        for j in range(N):
            if b[i][j] == 0:
                return False
    return True

# ---------- Kiểm tra đáp án đã điền có đúng không ----------
def checkDapAn(b):
    # Hàng
    for r in range(N):
        seen = set()
        for c in range(N):
            v = b[r][c]
            if v < 1 or v > 9 or v in seen:
                return False
            seen.add(v)
    # Cột
    for c in range(N):
        seen = set()
        for r in range(N):
            v = b[r][c]
            if v < 1 or v > 9 or v in seen:
                return False
            seen.add(v)
    # Các ô 3x3
    for br in range(0, N, 3):
        for bc in range(0, N, 3):
            seen = set()
            for i in range(3):
                for j in range(3):
                    v = b[br + i][bc + j]
                    if v < 1 or v > 9 or v in seen:
                        return False
                    seen.add(v)
    return True

# ---------- Bộ giải backtracking (giải tự động) ----------
def find_empty(b):
    for r in range(N):
        for c in range(N):
            if b[r][c] == 0:
                return r, c
    return None

def solve_backtracking(b):
    pos = find_empty(b)
    if not pos:
        return True  # không còn ô trống → đã giải xong
    r, c = pos
    for num in range(1, 10):
        if checkSo(b, r, c, num):
            b[r][c] = num
            if solve_backtracking(b):
                return True
            b[r][c] = 0  # quay lui
    return False

def showDapAn():
    """Giải đáp án đúng của puzzle gốc và in ra."""
    solved = deepcopy(puzzle)
    if solve_backtracking(solved):
        print("🧩 ĐÁP ÁN ĐÚNG (puzzle gốc):")
        inBanCo(solved)
    else:
        print("⚠️ Puzzle gốc không có lời giải hợp lệ!")

# ---------- Chơi Sudoku ----------
def runSudoku():
    print("Mẹo: nhập số 0 để xóa ô bạn đã điền sai.")
    while True:
        inBanCo(board)

        # Nếu đã điền hết → báo đúng/sai
        if checkBanCo(board):
            print("🎉 Bạn đã điền xong!")
            if checkDapAn(board):
                print("✅ Đáp án ĐÚNG, chúc mừng!")
            else:
                print("❌ Có sai sót trong lời giải!")
            break

        # Nhập lệnh
        try:
            row = int(input("Nhập hàng (0-8): "))
            col = int(input("Nhập cột (0-8): "))
            num = int(input("Nhập số (0 để xóa, 1-9 để điền): "))
        except ValueError:
            print("⚠️ Vui lòng nhập số nguyên!")
            continue

        # Kiểm tra biên
        if not (0 <= row < 9 and 0 <= col < 9):
            print("⚠️ Vị trí không hợp lệ!")
            continue
        if not (0 <= num <= 9):
            print("⚠️ Số không hợp lệ!")
            continue

        # Chỉ cho phép sửa những ô TRỐNG trong puzzle gốc
        if puzzle[row][col] != 0:
            print("⚠️ Ô gốc (đã cho sẵn), không được chỉnh!")
            continue

        # Xóa ô
        if num == 0:
            board[row][col] = 0
            continue

        # Điền số
        if checkSo(board, row, col, num):
            board[row][col] = num
        else:
            print("❌ Số không hợp lệ theo luật Sudoku, thử lại!")

# ---------- Main ----------
if __name__ == "__main__":
    while True:
        print("\n=====SUDOKU=====")
        print("1 <-- Chơi Sudoku")
        print("2 <-- Kiểm tra đáp án hiện tại (board bạn đang điền)")
        print("3 <-- Xem đáp án ĐÚNG (giải tự động puzzle gốc)")
        print("4 <-- In bàn hiện tại")
        print("0 <-- Thoát")
        choice = input("Chọn: ").strip()

        if choice == "1":
            runSudoku()
        elif choice == "2":
            if checkBanCo(board) and checkDapAn(board):
                print("✅ Đáp án hiện tại ĐÚNG!")
            else:
                print("❌ Đáp án hiện tại CHƯA đúng hoặc chưa điền đủ.")
        elif choice == "3":
            showDapAn()
        elif choice == "4":
            inBanCo(board)
        elif choice == "0":
            print("Baiii love you!")
            break
        else:
            print("⚠️Lựa chọn không hợp lệ, vui lòng chọn lại.")
