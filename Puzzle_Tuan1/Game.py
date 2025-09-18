import os
import re
import sys
import pygame
import random
from tkinter import Tk, filedialog, simpledialog
from collections import deque
import math
import heapq
import tkinter.simpledialog
from config import *
import heapq
import time
import tkinter
import json
from datetime import datetime

# ================== HỖ TRỢ ANIMATION ==================
class TileMoveAnim:
    def __init__(self, num, start_pos, end_pos, start_time, duration=0.18):
        self.num = num
        self.start_pos = start_pos  # (row, col)
        self.end_pos = end_pos      # (row, col)
        self.start_time = start_time
        self.duration = duration
        self.done = False
    def get_pos(self, now):
        t = min(1, (now - self.start_time) / self.duration)
        r = self.start_pos[0] + (self.end_pos[0] - self.start_pos[0]) * t
        c = self.start_pos[1] + (self.end_pos[1] - self.start_pos[1]) * t
        if t >= 1: self.done = True
        return r, c



# ================== HÀM HỖ TRỢ ==================
def board_random(numbers):
    nums = numbers[:]
    while True:
        random.shuffle(nums)
        if is_solvable(nums):
            return nums
        
def is_solvable(state):
    n = int(len(state)**0.5)
    arr = [x for x in state if x is not None]
    inv = 0
    for i in range(len(arr)):
        for j in range(i+1, len(arr)):
            if arr[i] > arr[j]:
                inv += 1

    # Kiểm tra vị trí của ô trống
    blank_row_from_bottom = n - (state.index(None) // n)
    if n % 2 == 1:
        return inv % 2 == 0
    else:
        return (inv + blank_row_from_bottom) % 2 == 0

def find_blank(board): 
    return board.index(None)

def move_tile(board, pos):
    idx = find_blank(board)
    row, col = divmod(idx, COLS)
    r2, c2 = divmod(pos, COLS)
    if abs(row - r2) + abs(col - c2) == 1:
        board[idx], board[pos] = board[pos], board[idx]

# ================== BFS ==================
def bfs(start, goal):
    q = deque([(start, [])])
    seen = {tuple(start)}
    generated = 0
    visited = 0

    while q:
        state, path = q.popleft()
        visited += 1
        if state == goal:
            return [start] + path, generated, visited

        idx = state.index(None)
        row, col = divmod(idx, COLS)
        for dx, dy in [(0,1),(0,-1),(1,0),(-1,0)]:
            r2, c2 = row + dx, col + dy
            if 0 <= r2 < ROWS and 0 <= c2 < COLS:
                new_state = state[:]
                swap = r2*COLS+c2
                new_state[idx], new_state[swap] = new_state[swap], new_state[idx]

                if tuple(new_state) not in seen:
                    seen.add(tuple(new_state))
                    q.append((new_state, path + [new_state]))
                    generated += 1

    return None, generated, visited

# ================== DFS ==================
def dfs(start, goal, max_depth=1000):
    stack = [(start, [], 0)]
    seen = {tuple(start)}
    generated = 0
    visited = 0

    while stack:
        state, path, depth = stack.pop()
        visited += 1
        if state == goal:
            return [start] + path, generated, visited
        if depth < max_depth:
            idx = state.index(None)
            row, col = divmod(idx, COLS)
            for dr, dc in [(0,1),(0,-1),(1,0),(-1,0)]:
                r2, c2 = row+dr, col+dc
                if 0 <= r2 < ROWS and 0 <= c2 < COLS:
                    new_state = state[:]
                    swap = r2*COLS+c2
                    new_state[idx], new_state[swap] = new_state[swap], new_state[idx]
                    if tuple(new_state) not in seen:
                        seen.add(tuple(new_state))
                        stack.append((new_state, path + [new_state], depth+1))
                        generated += 1
    return None, generated, visited

# ================== UCS ==================
def ucs(start, goal):
    counter = 0
    heap = [(0, counter, tuple(start), [])]  # (cost, counter, state(tuple), path)
    seen = {}

    generated = 0
    visited = 0

    while heap:
        cost, _, state, path = heapq.heappop(heap)
        visited += 1
        if state in seen and seen[state] <= cost:
            continue
        seen[state] = cost
        if list(state) == goal:
            return [list(start)] + [list(s) for s in path], generated, visited
        idx = state.index(None)
        row = idx // COLS
        col = idx % COLS
        a = [(0,1),(0,-1),(1,0),(-1,0)]
        for dx, dy in a:
            r2 = row + dx
            c2 = col + dy
            if 0 <= r2 < ROWS and 0 <= c2 < COLS:
                new_state = list(state)
                swap = r2*COLS+c2
                new_state[idx], new_state[swap] = new_state[swap], new_state[idx]
                t_new = tuple(new_state)
                new_cost = cost + 1  # Mỗi bước cost=1
                if t_new not in seen or new_cost < seen.get(t_new, float('inf')):
                    counter += 1
                    heapq.heappush(heap, (new_cost, counter, t_new, path + [t_new]))
                    generated += 1
    return None, generated, visited

# ================== A* và Greedy ==================
def heuristic_h1(state, goal):
    # Số lượng ô sai vị trí
    return sum(1 for i, v in enumerate(state) if v is not None and goal[i] is not None and v != goal[i])

def astar_h1(start, goal):
    return _astar(start, goal, heuristic_h1)

def heuristic_h2(state, goal):
    # Tổng khoảng cách Manhattan
    n = int(len(state) ** 0.5)
    total = 0
    for idx, v in enumerate(state):
        if v is not None and v in goal:
            goal_idx = goal.index(v)
            x1, y1 = divmod(idx, n)
            x2, y2 = divmod(goal_idx, n)
            total += abs(x1-x2) + abs(y1-y2)
    return total

def astar_h2(start, goal):
    return _astar(start, goal, heuristic_h2)

def greedy(start, goal):
    return _greedy(start, goal, heuristic_h1)

def _astar(start, goal, h_func):
    frontier = []
    counter = 0
    h0 = h_func(start, goal)

    generated = 0
    visited = 0

    if h0 is None:
        h0 = float('inf')
    # heap entry: (f, counter, g, state, path) --> counter breaks ties and avoids comparing lists
    heapq.heappush(frontier, (h0, counter, 0, start, [start]))
    explored = set()
    while frontier:
        f, _, g, state, path = heapq.heappop(frontier)
        visited += 1
        if tuple(state) in explored:
            continue
        explored.add(tuple(state))
        if state == goal:
            return path, generated, visited
        idx = state.index(None)
        n = int(len(state) ** 0.5)
        x, y = divmod(idx, n)
        for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
            nx, ny = x+dx, y+dy
            if 0<=nx<n and 0<=ny<n:
                nidx = nx*n+ny
                new_state = state[:]
                new_state[idx], new_state[nidx] = new_state[nidx], new_state[idx]
                if tuple(new_state) not in explored:
                    hval = h_func(new_state, goal)
                    try:
                        hval = int(hval)
                    except:
                        hval = float('inf')
                    counter += 1
                    heapq.heappush(frontier, (g+1+hval, counter, g+1, new_state, path+[new_state]))
                    generated += 1
    return None, generated, visited

def _greedy(start, goal, h_func):
    frontier = []
    counter = 0
    h0 = h_func(start, goal)

    generated = 0
    visited = 0

    if h0 is None:
        h0 = float('inf')
    heapq.heappush(frontier, (h0, counter, start, [start]))
    explored = set()
    while frontier:
        h, _, state, path = heapq.heappop(frontier)
        visited += 1
        if tuple(state) in explored:
            continue
        explored.add(tuple(state))
        if state == goal:
            return path, generated, visited
        idx = state.index(None)
        n = int(len(state) ** 0.5)
        x, y = divmod(idx, n)
        for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
            nx, ny = x+dx, y+dy
            if 0<=nx<n and 0<=ny<n:
                nidx = nx*n+ny
                new_state = state[:]
                new_state[idx], new_state[nidx] = new_state[nidx], new_state[idx]
                if tuple(new_state) not in explored:
                    hval = h_func(new_state, goal)
                    if hval is None:
                        hval = float('inf')
                    counter += 1
                    heapq.heappush(frontier, (hval, counter, new_state, path+[new_state]))
                    generated += 1
    return None, generated, visited


# Solver wrapper that collects metadata
def solve_with_meta(name, start, goal, max_depth_for_dfs=None):
    t0 = time.time()
    sol, gen, vis = None, -1, -1

    if name == 'BFS':
        sol, gen, vis = bfs(start, goal)
    elif name == 'DFS':
        # pass max_depth nếu có
        if max_depth_for_dfs is None:
            sol, gen, vis = dfs(start, goal)
        else:
            sol, gen, vis = dfs(start, goal, max_depth_for_dfs)
    elif name == 'UCS':
        sol, gen, vis = ucs(start, goal)
    elif name == 'Astar (h1)':
        sol, gen, vis = astar_h1(start, goal)
    elif name == 'Astar (h2)':
        sol, gen, vis = astar_h2(start, goal)
    elif name == 'Greedy':
        sol, gen, vis = greedy(start, goal)
    t1 = time.time()

    meta = {
        'method': name,
        'start': start[:],
        'goal': goal[:],
        'generated': gen if gen is not None else -1,
        'visited': vis if vis is not None else -1,
        'time': t1 - t0,
        'solution': sol,
        'steps': (len(sol)-1) if sol else 0,
    }
    return meta

def ask_for_depth_process(queue, prompt, initial_value):
    """Runs a tkinter dialog in a separate process to avoid event loop conflicts."""
    root = tkinter.Tk()
    root.withdraw()
    # Bring the dialog to the front
    root.lift()
    root.attributes('-topmost', True)
    root.after_idle(root.attributes, '-topmost', False)
    
    result = simpledialog.askinteger(
        "Độ sâu DFS",
        prompt,
        parent=root,
        initialvalue=initial_value,
        minvalue=1,
        maxvalue=1000
    )
    root.destroy()
    queue.put(result)

def write_config_and_restart(new_rows, new_cols):
        cfg_path = os.path.join(os.path.dirname(__file__), 'config.py')
        try:
            with open(cfg_path, 'r', encoding='utf-8') as f: txt = f.read()
            new_line = f'ROWS, COLS = {new_rows}, {new_cols}'
            txt2 = re.sub(r"ROWS\s*,\s*COLS\s*=\s*\d+\s*,\s*\d+", new_line, txt)
            with open(cfg_path, 'w', encoding='utf-8') as f: f.write(txt2)
            pygame.quit()
            os.execv(sys.executable, [sys.executable] + sys.argv)
        except Exception as e: print('Failed to write config and restart:', e)

def save_player_info(name, moves, elapsed_seconds, rows, cols, algorithm='Human', filename='player_scores.jsonl'):
    """Append player's solve info to a JSONL file stored alongside the game files.

    Each line is a JSON object with keys: name, algorithm, moves, time_sec, rows, cols, timestamp.
    Returns the file path written to.
    """
    try:
        record = {
            'name': name,
            'algorithm': algorithm,
            'moves': int(moves) if moves is not None else None,
            'time_sec': float(elapsed_seconds) if elapsed_seconds is not None else None,
            'rows': int(rows),
            'cols': int(cols),
            'timestamp': datetime.now().isoformat(timespec='seconds')
        }
        path = os.path.join(os.path.dirname(__file__), filename)
        with open(path, 'a', encoding='utf-8') as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")
        return path
    except Exception as e:
        # Fail silently to avoid breaking the game loop; optionally print
        print('Failed to save player info:', e)
        return None