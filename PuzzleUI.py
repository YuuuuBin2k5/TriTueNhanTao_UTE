import pygame
import sys
import random
import math
from pygame.locals import *
import easygui

# --- Cấu hình cửa sổ ---
WIDTH, HEIGHT = 700, 500
FPS = 60

# --- Màu sắc ---
BLUE = (148, 224, 255)
RED = (250, 77, 77)
BLACK = (0, 0, 0)
TILE_TEXT = (255, 255, 255)        # trắng
EMPTY_COLOR = (13, 27, 71)         # xanh đậm
SHADOW_COLOR = (180, 180, 180)     # bóng đổ

# --- Bảng ---
GRID_SIZE = 3
BOARD_TILE_SIZE = 100

goal = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 0]
]
board = [row[:] for row in goal]  # copy từ goal

# --- Khởi tạo pygame ---
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("8-Puzzle")
font_big = pygame.font.SysFont(None, 100, bold=True)
font = pygame.font.SysFont(None, 40, bold=True)

# --- Fireworks ---
particles = []

def spawn_firework():
    x = random.randint(100, WIDTH-100)
    y = random.randint(50, HEIGHT//2)
    color = random.choice([(255,0,0),(0,255,0),(0,128,255),(255,255,0),(255,0,255)])
    for _ in range(50):
        angle = random.uniform(0, 2*math.pi)
        speed = random.uniform(2, 6)
        dx = speed * math.cos(angle)
        dy = speed * math.sin(angle)
        particles.append([x, y, dx, dy, color, random.randint(30,60)])

def update_fireworks():
    for p in particles[:]:
        p[0] += p[2]
        p[1] += p[3]
        p[3] += 0.1  # gravity
        p[5] -= 1
        if p[5] <= 0:
            particles.remove(p)
        else:
            pygame.draw.circle(screen, p[4], (int(p[0]), int(p[1])), 3)

# --- Nút bấm ---
def draw_button(rect, color, text=None):
    shadow_rect = rect.move(3, 3)
    pygame.draw.rect(screen, SHADOW_COLOR, shadow_rect, border_radius=8)
    pygame.draw.rect(screen, color, rect, border_radius=8)
    pygame.draw.rect(screen, BLACK, rect, 2, border_radius=8)
    if text:
        text_surf = font.render(text, True, TILE_TEXT)
        text_rect = text_surf.get_rect(center=rect.center)
        screen.blit(text_surf, text_rect)

# --- Load ảnh thành tile ---
tiles = None

def load_image_tiles(path):
    """Cắt ảnh thành 3x3 ô; ô cuối là ô trống"""
    global tiles
    image = pygame.image.load(path).convert()
    image = pygame.transform.scale(
        image,
        (GRID_SIZE * BOARD_TILE_SIZE, GRID_SIZE * BOARD_TILE_SIZE)
    )
    tiles = []
    val = 1
    for i in range(GRID_SIZE):
        row = []
        for j in range(GRID_SIZE):
            rect = pygame.Rect(
                j * BOARD_TILE_SIZE,
                i * BOARD_TILE_SIZE,
                BOARD_TILE_SIZE,
                BOARD_TILE_SIZE
            )
            tile_image = image.subsurface(rect).copy()
            if val < GRID_SIZE * GRID_SIZE:
                row.append(tile_image)
            else:
                row.append(None)  # ô trống
            val += 1
        tiles.append(row)

def upload_image():
    """Mở hộp thoại chọn file bằng easygui"""
    global tiles
    file_path = easygui.fileopenbox(
        title="Chọn ảnh để làm puzzle",
        default="*",
        filetypes=["*.png","*.jpg","*.jpeg","*.bmp","*.gif"]
    )
    if file_path:
        load_image_tiles(file_path)
        return True
    return False

# --- Vẽ board ---
def draw_board(board, start_x, start_y, tile_size):
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            value = board[i][j]
            rect = pygame.Rect(
                start_x + j * tile_size,
                start_y + i * tile_size,
                tile_size,
                tile_size
            )
            if value == 0:
                pygame.draw.rect(screen, EMPTY_COLOR, rect, border_radius=8)
            else:
                if tiles:
                    src_r = (value - 1) // GRID_SIZE
                    src_c = (value - 1) % GRID_SIZE
                    tile_img = tiles[src_r][src_c]
                    screen.blit(tile_img, rect)
                    pygame.draw.rect(screen, BLACK, rect, 2, border_radius=8)
                else:
                    draw_button(rect, (100, 180, 255), str(value))

# --- Logic game ---
def find_blank(board):
    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE):
            if board[r][c] == 0:
                return r, c

def move_tile(board, dr, dc):
    r, c = find_blank(board)
    nr, nc = r + dr, c + dc
    if 0 <= nr < GRID_SIZE and 0 <= nc < GRID_SIZE:
        board[r][c], board[nr][nc] = board[nr][nc], board[r][c]

def check_win(board):
    return board == goal

def is_solvable(flat):
    inv = 0
    for i in range(len(flat)):
        for j in range(i+1, len(flat)):
            if flat[i] and flat[j] and flat[i] > flat[j]:
                inv += 1
    return inv % 2 == 0

def shuffle_board():
    nums = list(range(9))
    while True:
        random.shuffle(nums)
        if is_solvable(nums):
            break
    return [nums[i*3:(i+1)*3] for i in range(3)]

# --- Nút chức năng ---
restart_rect = pygame.Rect(280, 420, 100, 50)
upload_rect = pygame.Rect(420, 420, 100, 50)

clock = pygame.time.Clock()
won = False
firework_timer = 0

# --- Vòng lặp chính ---
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN and not won:
            if event.key == K_UP: move_tile(board, -1, 0)
            elif event.key == K_DOWN: move_tile(board, 1, 0)
            elif event.key == K_LEFT: move_tile(board, 0, -1)
            elif event.key == K_RIGHT: move_tile(board, 0, 1)
            if check_win(board):
                won = True
        elif event.type == MOUSEBUTTONDOWN:
            if restart_rect.collidepoint(event.pos):
                board = shuffle_board()
                won = False
                particles.clear()
            elif upload_rect.collidepoint(event.pos):
                if upload_image():
                    board = shuffle_board()
                    won = False
                    particles.clear()

    screen.fill(BLUE)
    draw_board(board, 50, 100, BOARD_TILE_SIZE)

    # Vẽ nút
    draw_button(restart_rect, (0, 200, 0), "Restart")
    draw_button(upload_rect, (0, 120, 200), "Upload")

    # Nếu thắng thì bắn pháo hoa
    if won:
        win_text = font_big.render("YOU WIN!", True, RED)
        text_rect = win_text.get_rect(center=(WIDTH//2, 50))
        screen.blit(win_text, text_rect)
        firework_timer += 1
        if firework_timer % 30 == 0:
            spawn_firework()
        update_fireworks()

    pygame.display.update()
    clock.tick(FPS)
