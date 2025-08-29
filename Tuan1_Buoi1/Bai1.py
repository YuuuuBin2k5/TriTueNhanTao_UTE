#Bài 1
# @author: Đào Nguyễn Nhật Anh
# @date: 2025-8-21 
# @description: Bài tập 1

# Đọc file
def docFile(fileName):
    with open(fileName, "r", encoding="utf-8") as f:
        n = int(f.readline().strip())  # số đỉnh
        matrix = []
        for _ in range(n):
            row = [1 if int(x) != 0 else 0 for x in f.readline().split()]
            if len(row) != n:
                raise ValueError("Dòng ma trận không đủ/sai số cột")
            matrix.append(row)
    return matrix

# Kiểm tra đồ thị
def kiemTraDoThi(matrix):
    for i in range(len(matrix)):
        for j in range(len(matrix)):
            if matrix[i][j] != matrix[j][i]:
                return True  # Đồ thị có hướng
    
    return False #Đồ thị vô hướng

#Duyệt đồ thị theo chiều sâu
def DFS(matrix, visited, dinh):
    temp = [dinh]
    component = []

    while temp:
        u = temp.pop()
        if not visited[u]:
            visited[u] = True
            component.append(u) # Các đỉnh thành phần liên thông

            for v in range(len(matrix[u]) - 1, -1, -1): #
                if matrix[u][v] == 1 and not visited[v]:
                    temp.append(v)
    return component

#Duyệt đồ thị theo chiều rộng
def BFS(matrix, visited, dinh): 
    temp = [dinh]
    visited = [False] * len(matrix)
    result = []
    while temp:
        u = temp.pop(0)
        if  not visited[u]:
            visited[u] = True
            result.append(u)
            for v in range(len(matrix[u])):
                if matrix[u][v] != 0 and not visited[v]:
                    temp.append(v)
                    
    return result

# Tìm các thành phần liên thông
def cacThanhPhanLienThong(matrix):
    visited = [False] * len(matrix)
    result = []
    for i in range(len(matrix)):
        if not visited[i]:
            component = DFS(matrix, visited, i)
            result.append((component))
    return result

if __name__ == "__main__":
    matrix = docFile("text.txt")

    #Kiểm tra đồ thị
    check = kiemTraDoThi(matrix)
    if check:
        print("Đồ thị có hướng")
    else:
        print("Đồ thị vô hướng")

    # Các thành phần liên thông là
    components = cacThanhPhanLienThong(matrix)
    for i, component in enumerate(components):
        print(f"Thành phần liên thông {i + 1}: {component}")

    # Tập đỉnh
    tap_dinh = set()
    for component in components:
        tap_dinh.update(component)
    print(f"Tập đỉnh của đồ thị: {tap_dinh}")

    # Tập cạnh (ma trận kề)
    tap_canh = set()
    for i in range(len(matrix)):
        for j in range(i + 1, len(matrix)): #Duyệt nửa đồ thị
            if matrix[i][j] == 1:
                tap_canh.add((i, j))
    print(f"Tập cạnh của đồ thị: {tap_canh}")

    # kết quả BFS
    dinh = int(input("Nhập đỉnh đi của BFS: "))
    bfs = BFS(matrix, [False] * len(matrix), dinh)
    print(f"Kết quả BFS: {bfs}")

    # Kết quả DFS
    dinh = int(input("Nhập đỉnh đi của DFS: "))
    dfs = DFS(matrix, [False] * len(matrix), dinh)
    print(f"Kết quả DFS: {dfs}")