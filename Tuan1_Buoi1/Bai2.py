#Bài 1
# @author: Đào Nguyễn Nhật Anh
# @date: 2025-8-21 
# @description: Bài 2: Bài toán 8 quân hậu

# Kiểm tra có thể đặt hậu tại (row, col) không
def is_safe(row, col):
    for r in range(row):
        c = queen_pos[r]
        if c == col:  # cùng cột
            return False
        if abs(c - col) == abs(r - row):  # cùng đường chéo
            return False
    return True

# Đệ quy đặt hậu
def solve(row=0):
    if row == N:
        print_solution()
        return
    for col in range(N):
        if is_safe(row, col):
            queen_pos[row] = col
            solve(row + 1)  # đặt tiếp hàng sau
            queen_pos[row] = -1  # backtrack (bỏ thử)

# In bàn cờ
def print_solution():
    for r in range(N):
        line = ""
        for c in range(N):
            if queen_pos[r] == c:
                line += "Q "
            else:
                line += ". "
        print(line)
    print("\n" + "-" * 20 + "\n")

# Chạy chương trình
if __name__ == "__main__":
    # Kích thước bàn cờ
    N = int(input("Nhập kích thước bàn cờ (N): "))
    queen_pos = [-1] * N  # queen_pos[i] = cột đặt hậu ở hàng i
    solve()
