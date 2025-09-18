from collections import deque
import heapq

# ================= Cấu hình =================
start = (1, 2, 3,
         0, 8, 7,
         6, 4, 5)  # 0 = ô trống

goal = (1, 2, 3,
        7, 4, 0,
        8, 5, 6)

ROWS, COLS = 3, 3

# ================= Hàm tiện ích =================
def get_blank_pos(state):
    return divmod(state.index(0), COLS)  # (row, col)

def swap(state, r1, c1, r2, c2):
    lst = list(state)
    idx1, idx2 = r1*COLS+c1, r2*COLS+c2
    lst[idx1], lst[idx2] = lst[idx2], lst[idx1]
    return tuple(lst)

def successors(state):
    r, c = get_blank_pos(state)
    moves = []
    for dr, dc, act in [(-1,0,"W"), (0,-1,"A"), (0,1,"D"), (1,0,"S")]:
        nr, nc = r+dr, c+dc
        if 0 <= nr < ROWS and 0 <= nc < COLS:
            moves.append((swap(state,r,c,nr,nc), act))
    return moves

def reconstruct_path(parent, move, end):
    path = []
    while end in move:
        path.append(move[end])
        end = parent[end]
    return path[::-1]

def print_state(state):
    for i in range(0, 9, 3):
        print(state[i:i+3])
    print()
    
# ================= BFS =================
def BFS(start, goal):
    q = deque([start])
    parent = {}
    move = {}
    visited = {start}
    while q:
        s = q.popleft()
        if s == goal:
            return reconstruct_path(parent, move, s)
        for nxt, act in successors(s):
            if nxt not in visited:
                visited.add(nxt)
                parent[nxt] = s
                move[nxt] = act
                q.append(nxt)
    return None

# ================= DFS =================
def DFS(start, goal, limit=1000):
    stack = [start]
    parent = {}
    move = {}
    visited = {start}
    while stack:
        s = stack.pop()
        if s == goal:
            return reconstruct_path(parent, move, s)
        if len(reconstruct_path(parent, move, s)) < limit:
            for nxt, act in successors(s):
                if nxt not in visited:
                    visited.add(nxt)
                    parent[nxt] = s
                    move[nxt] = act
                    stack.append(nxt)
    return None

# ================= Iterative Deepening =================
def DLS(state, goal, limit, parent, move, visited):
    if state == goal: return True
    if limit == 0: return False
    for nxt, act in successors(state):
        if nxt not in visited:
            visited.add(nxt)
            parent[nxt] = state
            move[nxt] = act
            if DLS(nxt, goal, limit-1, parent, move, visited):
                return True
    return False

def ID(start, goal, max_depth=5):
    for depth in range(1, max_depth+1):
        parent, move, visited = {}, {}, {start}
        if DLS(start, goal, depth, parent, move, visited):
            return reconstruct_path(parent, move, goal)
    return None

# ================= UCS =================
def UCS(start, goal):
    pq = [(0, start)]
    parent, move = {}, {}
    cost = {start: 0}
    while pq:
        g, s = heapq.heappop(pq)
        if s == goal:
            return reconstruct_path(parent, move, s)
        for nxt, act in successors(s):
            new_g = g + 1
            if nxt not in cost or new_g < cost[nxt]:
                cost[nxt] = new_g
                parent[nxt] = s
                move[nxt] = act
                heapq.heappush(pq, (new_g, nxt))
    return None

# ================= Chạy thử =================
print("=== BFS ===")
path_bfs = BFS(start, goal)
print("Đường đi:", path_bfs, "\nSố bước:", len(path_bfs))

print("=== DFS (giới hạn 50) ===")
path_dfs = DFS(start, goal, limit=50)
print("Đường đi:", path_dfs, "\nSố bước:", len(path_dfs) if path_dfs else "Không tìm thấy")

print("=== ID (d ≤ 5) ===")
path_id = ID(start, goal, max_depth=5)
print("Kết quả:", path_id)

print("=== UCS ===")
path_ucs = UCS(start, goal)
print("Đường đi:", path_ucs, "\nSố bước:", len(path_ucs))
