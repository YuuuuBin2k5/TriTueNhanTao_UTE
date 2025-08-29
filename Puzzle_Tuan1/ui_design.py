import random
import pygame
from tkinter import Tk, filedialog

# ================== CẤU HÌNH ==================
WIDTH, HEIGHT = 780, 500     # Kích thước cửa sổ game
FPS = 90                     # Số khung hình/giây (tốc độ refresh)

ROWS, COLS = 3, 3            # Bàn puzzle: 3 hàng 3 cột (8 mảnh + 1 ô trống)

# Layout bảng trái (nơi chơi puzzle)
LEFT_BOARD_X, LEFT_BOARD_Y = 40, 40         # Toạ độ góc trái trên
LEFT_BOARD_W, LEFT_BOARD_H = 420, 420       # Kích thước khung chứa puzzle
GRID_MARGIN = 28                            # Lề trong
CELL_SIZE = 110                             # Kích thước mỗi ô puzzle
GAP = 18                                    # Khoảng cách giữa các ô

# Màu sắc
BG_COLOR = (190, 167, 229)      # Màu nền
BOARD_GREY = (188, 188, 188)    # Màu viền ngoài
BOARD_INNER = (220, 238, 209)   # Màu nền trong bảng
WHITE_TILE = (240, 240, 240)    # Màu tile mặc định (khi không có ảnh)
GOAL_TEXT_COLOR = (40, 160, 40) # Màu chữ "Goal state"
BUTTON_COLOR = (117, 185, 190)  # Màu nền nút
TEXT_COLOR = (220, 238, 209)    # Màu chữ nút

# ================== TIỆN ÍCH ==================
def draw_rounded_rect(surface, rect, color, radius=8, border_color=None, border_width=2):
    """
    Vẽ một hình chữ nhật bo góc (rounded rectangle).
    - surface: nơi vẽ
    - rect: (x, y, w, h)
    - color: màu nền
    - radius: độ bo góc
    - border_color: màu viền
    - border_width: độ dày viền
    """
    x, y, w, h = rect
    shape_surf = pygame.Surface((w, h), pygame.SRCALPHA)  # bề mặt trong suốt
    pygame.draw.rect(shape_surf, color, (0, 0, w, h), border_radius=radius)
    if border_color and border_width > 0:
        pygame.draw.rect(shape_surf, border_color, (0, 0, w, h),
                         width=border_width, border_radius=radius)
    surface.blit(shape_surf, (x, y))


def draw_tile(surface, rect, text, font, bg, fg=(0, 0, 0), radius=12, border=(0, 0, 0)):
    """
        Vẽ 1 ô puzzle (có thể có chữ/ảnh).
        - bg: màu nền
        - fg: màu chữ
    """
    draw_rounded_rect(surface, rect, bg, radius=radius, border_color=border, border_width=3)
    if text is not None:
        txt_surf = font.render(str(text), True, fg)
        txt_rect = txt_surf.get_rect(center=(rect[0] + rect[2] // 2,
                                            rect[1] + rect[3] // 2))
        surface.blit(txt_surf, txt_rect)

def slice_sheet(sheet, rows, cols):
    """
    Cắt 1 ảnh thành nhiều mảnh nhỏ (rows x cols).
    """
    sw, sh = sheet.get_size()
    tw, th = sw // cols, sh // rows
    pieces = []
    for r in range(rows):
        for c in range(cols):
            rect = pygame.Rect(c*tw, r*th, tw, th)
            pieces.append(sheet.subsurface(rect).copy())
    return pieces

def center_crop_square(surface):
    """
    Cắt ảnh thành hình vuông (lấy phần giữa).
    """
    w, h = surface.get_size()
    side = min(w, h)
    x = (w - side) // 2
    y = (h - side) // 2
    return surface.subsurface(pygame.Rect(x, y, side, side)).copy()

def load_and_slice(path, rows=3, cols=3):
    """
    Load ảnh, crop vuông, scale, rồi cắt thành nhiều mảnh puzzle.
    """
    img = pygame.image.load(path).convert_alpha()
    img = center_crop_square(img)
    target = pygame.transform.smoothscale(img, (cols*300, rows*300))
    return slice_sheet(target, rows, cols)

def cell_rect_left(r, c):
    """
    Trả về toạ độ hình chữ nhật của 1 ô (row r, col c) trong bảng trái.
    """
    grid_x = LEFT_BOARD_X + GRID_MARGIN
    grid_y = LEFT_BOARD_Y + GRID_MARGIN
    x = grid_x + c * (CELL_SIZE + GAP)
    y = grid_y + r * (CELL_SIZE + GAP)
    return pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)

def draw_button(screen, rect, text, font, bg, fg):
    """Vẽ 1 nút bấm với chữ giữa."""
    pygame.draw.rect(screen, bg, rect, border_radius=8)
    txt_surf = font.render(text, True, fg)
    x, y, w, h = rect
    txt_rect = txt_surf.get_rect(center=(x + w // 2, y + h // 2))
    screen.blit(txt_surf, txt_rect)


def inversion_count(numbers):
    """Đếm số inversion (bỏ None)."""
    arr = [x for x in numbers if x is not None]
    inv = 0
    for i in range(len(arr)):
        for j in range(i+1, len(arr)):
            if arr[i] > arr[j]:
                inv += 1
    return inv

def is_solvable(numbers, rows=ROWS, cols=COLS):
    """
    Kiểm tra solvability cho bất kỳ rows x cols.
    Quy tắc:
      - Nếu cols lẻ  -> solvable khi inversion chẵn.
      - Nếu cols chẵn -> solvable khi (inversion + blank_row_from_bottom) chẵn.
        (blank_row_from_bottom tính từ 1 ở hàng dưới cùng)
    """
    inv = inversion_count(numbers)
    if cols % 2 == 1:
        return inv % 2 == 0
    else:
        empty_index = numbers.index(None)
        empty_row = empty_index // cols          # 0-based từ trên xuống
        blank_row_from_bottom = rows - empty_row
        return (inv + blank_row_from_bottom) % 2 == 0

def board_random(numbers):
    """
    Trả về 1 hoán vị ngẫu nhiên nhưng đảm bảo solvable.
    numbers: list ví dụ [1,2,...,8,None]
    """
    nums = numbers[:]  # copy để không thay đổi input gốc
    random.shuffle(nums)
    # nếu muốn nhanh: swap 2 tile non-blank để đổi parity thay vì shuffle lại
    # nhưng ở đây loop shuffle là dễ hiểu và an toàn
    while not is_solvable(nums):
        random.shuffle(nums)
    return nums
def check_win(current, goal):
    """Kiểm tra đã thắng chưa (so sánh trạng thái hiện tại với trạng thái đích)."""
    return current == goal

# ================== VẼ BẢNG TRÁI ==================
def draw_left_board(screen, font, numbers, tiles):
    """
    Vẽ toàn bộ bảng puzzle bên trái:
    - khung ngoài, khung trong
    - từng ô (ảnh hoặc số)
    """
    # Vẽ khung ngoài
    draw_rounded_rect(screen, (LEFT_BOARD_X, LEFT_BOARD_Y, LEFT_BOARD_W, LEFT_BOARD_H),
                      BOARD_GREY, radius=12, border_color=(20, 20, 20), border_width=4)
    # Vẽ khung trong
    inner_pad = 8
    draw_rounded_rect(screen, (LEFT_BOARD_X + inner_pad, LEFT_BOARD_Y + inner_pad,
                               LEFT_BOARD_W - 2*inner_pad, LEFT_BOARD_H - 2*inner_pad),
                      BOARD_INNER, radius=10)

    # Vẽ từng ô
    for i in range(ROWS*COLS):
        r, c = divmod(i, COLS)   # chia index -> (row, col)
        rect = cell_rect_left(r, c)
        val = numbers[i]

        if tiles:  # nếu có ảnh
            if val is None:
                screen.fill(BOARD_INNER, rect)  # ô trống
            else:
                img = tiles[val - 1]  # map số 1..8 -> index 0..7
                img_s = pygame.transform.smoothscale(img, (CELL_SIZE, CELL_SIZE))
                screen.blit(img_s, rect.topleft)
        else:  # fallback nếu không có ảnh -> vẽ ô trắng có số
            if val is None:
                draw_tile(screen, rect, 0, font, WHITE_TILE,
                          fg=(50, 50, 50), radius=6, border=(150, 150, 150))
            else:
                draw_tile(screen, rect, val, font, WHITE_TILE,
                          fg=(20, 20, 20), radius=6, border=(160, 160, 160))

# ================== VẼ GOAL STATE ==================
def draw_goal_state(screen, font_big, tiles):
    """
    Vẽ trạng thái đích (goal state) ở bên phải màn hình.
    """
    goal_x, goal_y = 520, 60
    title_surf = font_big.render("Goal state", True, GOAL_TEXT_COLOR)
    screen.blit(title_surf, (goal_x, goal_y - 30))

    small_cell, small_gap = 64, 12
    for i in range(ROWS*COLS):
        r, c = divmod(i, COLS)
        x = goal_x + c * (small_cell + small_gap)
        y = goal_y + 20 + r * (small_cell + small_gap)
        rect = pygame.Rect(x, y, small_cell, small_cell)
        if tiles:
            if i < 8:  # chỉ vẽ 8 mảnh
                img = tiles[i]
                img_s = pygame.transform.smoothscale(img, (small_cell, small_cell))
                screen.blit(img_s, rect.topleft)
            else:
                # mảnh cuối là ô trống
                draw_tile(screen, rect, None, font_big, BOARD_INNER)
        else:
            draw_tile(screen, rect, i+1 if i < 8 else 0, font_big, WHITE_TILE)


# ================== MAIN ==================
def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Puzzle YuuuBin")
    pygame.display.set_icon(pygame.image.load("images/icon.png"))
    clock = pygame.time.Clock()

    # Load ảnh puzzle
    try:
        tiles_full = load_and_slice("images/icon.png", 3, 3)
    except:
        # Nếu không có ảnh thì tạo ô xám
        tiles_full = [pygame.Surface((100, 100), pygame.SRCALPHA) for _ in range(9)]
        for s in tiles_full:
            s.fill((200, 200, 200))

    tiles_for_puzzle = tiles_full[:8]  # chỉ lấy 8 mảnh (1 ô trống để None)

    # Fonts
    big_font = pygame.font.SysFont("arial", 64)
    large_font = pygame.font.SysFont("arial", 56)
    small_font = pygame.font.SysFont("arial", 36)

    # Trạng thái ban đầu
    left_numbers = board_random([1, 2, 3, 4, 5, 6, 7, 8, None])
    goal_numbers = [1, 2, 3, 4, 5, 6, 7, 8, None]  # trạng thái đích
    win = False

    # Nút bấm
    buttonRandom_rect = pygame.Rect(520, 320, 120, 45)
    buttonLoad_rect   = pygame.Rect(660, 320, 120, 45)

    running = True
    while running:
        # ====== Xử lý sự kiện ======
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (
                event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Nút Random
                if buttonRandom_rect.collidepoint(event.pos):
                    left_numbers = board_random([1, 2, 3, 4, 5, 6, 7, 8, None])
                    win = False

                # Nút Load ảnh
                elif buttonLoad_rect.collidepoint(event.pos):
                    Tk().withdraw()
                    path = filedialog.askopenfilename(
                        title="Chọn ảnh",
                        filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.bmp")]
                    )
                    if path:
                        tiles_full = load_and_slice(path, 3, 3)
                        tiles_for_puzzle = tiles_full[:8]
                        left_numbers = board_random([1, 2, 3, 4, 5, 6, 7, 8, None])
                        win = False

                # Click di chuyển mảnh puzzle
                else:
                    mx, my = event.pos
                    empty_idx = left_numbers.index(None)  # vị trí ô trống
                    er, ec = divmod(empty_idx, COLS)

                    for i in range(ROWS*COLS):
                        r, c = divmod(i, COLS)
                        rect = cell_rect_left(r, c)
                        if rect.collidepoint(mx, my) and left_numbers[i] is not None:
                            # chỉ cho phép swap với ô trống kề nhau
                            if (abs(r-er) == 1 and c == ec) or (abs(c-ec) == 1 and r == er):
                                left_numbers[empty_idx], left_numbers[i] = left_numbers[i], None
                                if check_win(left_numbers, goal_numbers):
                                    win = True
                            break

        # ======= VẼ =======
        screen.fill(BG_COLOR)

        # Bảng puzzle
        draw_left_board(screen, large_font, left_numbers, tiles_for_puzzle)

        # Goal state
        draw_goal_state(screen, small_font, tiles_full)

        # Nút
        draw_button(screen, buttonRandom_rect, "Random", small_font, BUTTON_COLOR, TEXT_COLOR)
        draw_button(screen, buttonLoad_rect,   "Load ảnh", small_font, BUTTON_COLOR, TEXT_COLOR)

        # Thông báo chiến thắng
        if win:
            win_text = big_font.render("🎉 Chiến Thắng! 🎉", True, (255, 50, 50))
            screen.blit(win_text, (WIDTH//2 - win_text.get_width()//2, HEIGHT - 80))

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()
