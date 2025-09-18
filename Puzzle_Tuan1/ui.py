import pygame
import math
from config import *
import time

# ================== VẼ ==================

def draw_decor_vertical_lines(screen):
    # Xác định cụm nút bên phải
    btn_top = BTN_Y+50
    btn_bot = BTN_Y+480
    line_h = btn_bot - btn_top
    # Đường trái cụm nút - nét dày, neon, glow
    grad_left = pygame.Surface((5, line_h), pygame.SRCALPHA)
    for y in range(line_h):
        ratio = y / line_h
        color = (
            int(160 + 80*ratio),
            int(100 + 120*ratio),
            int(255 - 60*ratio),
            255
        )
        pygame.draw.line(grad_left, (color[0],color[1],color[2],60), (0,y), (15,y), 8)
        pygame.draw.line(grad_left, (color[0],color[1],color[2],120), (3,y), (12,y), 4)
        pygame.draw.line(grad_left, color, (5,y), (10,y), 2)
    screen.blit(grad_left, (BTN_X + 80, btn_top))
    # Đường phải cụm nút - nét dày, neon, glow
    grad_right = pygame.Surface((5, line_h), pygame.SRCALPHA)
    for y in range(line_h):
        ratio = y / line_h
        color = (
            int(255 - 60*ratio),
            int(160 + 80*ratio),
            int(220 + 30*ratio),
            255
        )
        pygame.draw.line(grad_right, (color[0],color[1],color[2],60), (0,y), (15,y), 8)
        pygame.draw.line(grad_right, (color[0],color[1],color[2],120), (3,y), (12,y), 4)
        pygame.draw.line(grad_right, color, (5,y), (10,y), 2)
    screen.blit(grad_right, (BTN_X + 120 + BTN_W, btn_top))

def load_and_slice(path, rows, cols, cell_w, cell_h):
    img = pygame.image.load(path).convert_alpha()
    target_w = int(cell_w * cols)
    target_h = int(cell_h * rows)
    img_scaled = pygame.transform.smoothscale(img, (target_w, target_h))
    tiles = []
    for r in range(rows):
        for c in range(cols):
            if r == rows - 1 and c == cols - 1:
                continue
            rect = pygame.Rect(c * cell_w, r * cell_h, cell_w, cell_h)
            tiles.append(img_scaled.subsurface(rect).copy())
    return tiles

def draw_button_panel(screen, x, y, w, h):
    shadow_rect = pygame.Rect(x+4, y+4, w, h)
    pygame.draw.rect(screen, (50, 50, 50, 80), shadow_rect, border_radius=20)
    panel_rect = pygame.Rect(x, y, w, h)
    pygame.draw.rect(screen, (245, 245, 255), panel_rect, border_radius=20)
    pygame.draw.rect(screen, (200, 200, 220), panel_rect, 3, border_radius=20)
    return panel_rect

def draw_victory(screen, font, t=0):
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    alpha = min(220, int(80 + 120 * abs((t%60)/60-0.5)))
    overlay.fill((255,255,255, alpha))
    screen.blit(overlay, (0,0))
    for i in range(30):
        x = (i*30 + (t*7)%60*15) % WIDTH
        y = (t*8 + i*17) % HEIGHT
        color = (255,215,0) if i%2==0 else (120,200,255)
        pygame.draw.circle(screen, color, (x, y), 6)
    text = font.render("🎉 YOU WIN! 🎉", True, (255,120,40))
    screen.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2 - 50))

def draw_board(screen, board, tiles, x, y, label, font, is_goal=False, moves=0, start_time=None, anim=None, cell_w=None, cell_h=None):
    # Nền bàn (dùng kích thước cố định LEFT_BOARD_W/LEFT_BOARD_H)
    bg_color = GOAL_BOARD_COLOR if is_goal else BOARD_COLOR
    # Shadow ngoài nhẹ cho khung bao
    shadow = pygame.Surface((LEFT_BOARD_W, LEFT_BOARD_H), pygame.SRCALPHA)
    pygame.draw.rect(shadow, SHADOW_COLOR, shadow.get_rect(), border_radius=0)
    screen.blit(shadow, (x+4, y+4))
    # Board nền vuông, không bo góc
    pygame.draw.rect(screen, bg_color, (x, y, LEFT_BOARD_W, LEFT_BOARD_H), border_radius=0)
    # Viền ngoài mảnh màu pastel
    pygame.draw.rect(screen, VIEN_COLOR, (x, y, LEFT_BOARD_W, LEFT_BOARD_H), 2, border_radius=0)

    # fallback sizes nếu None
    if cell_w is None: cell_w = BOARD_CELL_SIZE
    if cell_h is None: cell_h = BOARD_CELL_SIZE

    gap = 2
    anim_tile = anim.num if anim else None
    for i, num in enumerate(board):
        r, c = divmod(i, COLS)
        if num is not None and num != anim_tile:
            # Không để GAP ở board chính để không bị hở
            rect = pygame.Rect(
                x + c * cell_w,
                y + r * cell_h,
                cell_w - gap * 2,
                cell_h - gap * 2
            )
            # Không shadow, không bo góc, không viền, không GAP
            tile_img = pygame.transform.smoothscale(tiles[num-1], (rect.width, rect.height))
            screen.blit(tile_img, rect.topleft)

    # Vẽ tile đang animate (nếu có)
    if anim and not anim.done:
        now = time.time()
        rr, cc = anim.get_pos(now)  # rr,cc có thể là float
        rect = pygame.Rect(
            x + cc * cell_w,
            y + rr * cell_h,
            cell_w,
            cell_h
        )
        tile_img = pygame.transform.smoothscale(tiles[anim.num-1], (rect.width, rect.height))
        screen.blit(tile_img, rect.topleft)

    # Nhãn
    text_color = TEXT_COLOR if not is_goal else TEXT_SUB_COLOR
    txt = font.render(label, True, text_color)
    screen.blit(txt, (x + LEFT_BOARD_W//2 - txt.get_width()//2, y-40))

    # Steps & Time (nếu không phải goal)
    if not is_goal:
        elapsed = int(time.time() - start_time) if start_time else 0
        m, s = divmod(elapsed, 60)
        time_text = pygame.font.SysFont("Arial", 20).render(f"Time: {m:02}:{s:02}", True, TEXT_SUB_COLOR)
        screen.blit(time_text, (x + LEFT_BOARD_W//2 - time_text.get_width()//2, y + LEFT_BOARD_H + 10))
        steps_text = pygame.font.SysFont("Arial", 20).render(f"Steps: {moves}", True, TEXT_SUB_COLOR)
        screen.blit(steps_text, (x + LEFT_BOARD_W//2 - steps_text.get_width()//2, y + LEFT_BOARD_H + 35))

def draw_board_goal(screen, board, tiles, x, y, label, font):
    # Nền bàn
    # Shadow ngoài nhẹ cho khung bao goal
    shadow = pygame.Surface((GOAL_BOARD_W, GOAL_BOARD_H), pygame.SRCALPHA)
    pygame.draw.rect(shadow, SHADOW_COLOR, shadow.get_rect(), border_radius=0)
    screen.blit(shadow, (x+4, y+4))
    pygame.draw.rect(screen, GOAL_BOARD_COLOR, (x, y, GOAL_BOARD_W, GOAL_BOARD_H), border_radius=0)
    # Viền ngoài mảnh màu pastel
    pygame.draw.rect(screen, VIEN_COLOR, (x, y, GOAL_BOARD_W, GOAL_BOARD_H), 2, border_radius=0)

    # Tính kích thước mỗi ô dựa vào Rows/Cols
    goal_cell_w = GOAL_BOARD_W // COLS
    goal_cell_h = GOAL_BOARD_H // ROWS

    for i, num in enumerate(board):
        r, c = divmod(i, COLS)
        if num is not None:
            rect = pygame.Rect(
                x + c * goal_cell_w,
                y + r * goal_cell_h,
                goal_cell_w,
                goal_cell_h
            )
            # Không shadow, không bo góc, không viền, không GAP
            tile_img = pygame.transform.scale(tiles[num-1], (rect.width, rect.height))
            screen.blit(tile_img, rect.topleft)

    # Vẽ nhãn
    txt = font.render(label, True, TEXT_SUB_COLOR)
    screen.blit(txt, (x + GOAL_BOARD_W//2 - txt.get_width()//2, y-40))

def draw_button(screen, rect, text, font, is_hovered=False, is_pressed=False):
    # Hình chữ nhật, hiệu ứng hover/click hiện đại
    base_rect = rect.copy()
    color = BUTTON_COLOR
    border_color = VIEN_COLOR
    txt_color = BUTTON_TEXT_COLOR
    scale = 1.0
    if is_pressed:
        scale = 0.96
        color = BUTTON_HOVER_COLOR
        border_color = VIEN_HOVER_COLOR
    elif is_hovered:
        scale = 1.08
        color = BUTTON_HOVER_COLOR
        border_color = VIEN_HOVER_COLOR
    # Zoom hiệu ứng
    if scale != 1.0:
        new_w = int(rect.width * scale)
        new_h = int(rect.height * scale)
        base_rect = pygame.Rect(
            rect.centerx - new_w//2,
            rect.centery - new_h//2,
            new_w, new_h
        )
    # Shadow nhẹ khi hover
    if is_hovered or is_pressed:
        shadow = pygame.Surface((base_rect.width+8, base_rect.height+8), pygame.SRCALPHA)
        pygame.draw.rect(shadow, SHADOW_COLOR, shadow.get_rect(), border_radius=0)
        screen.blit(shadow, (base_rect.x-4, base_rect.y-4))
    # Vẽ nút
    pygame.draw.rect(screen, color, base_rect, border_radius=0)
    pygame.draw.rect(screen, border_color, base_rect, 2, border_radius=0)
    txt = font.render(text, True, txt_color)
    screen.blit(txt, (base_rect.centerx - txt.get_width()//2, base_rect.centery - txt.get_height()//2))
  
def draw_list(screen, rect, selected, options, font):
    import pygame.gfxdraw
    icon_font = pygame.font.SysFont("Segoe UI Symbol", 22)
    rects = []
    panel_h = rect.height * len(options)
    panel = pygame.Surface((rect.width+16, panel_h+16), pygame.SRCALPHA)
    pygame.draw.rect(panel, (80,40,120,100), panel.get_rect(), border_radius=26)
    screen.blit(panel, (rect.x-8, rect.y), special_flags=pygame.BLEND_RGBA_ADD)
    for i, option in enumerate(options):
        opt_rect = pygame.Rect(rect.x, rect.y + i*rect.height, rect.width, rect.height)
        grad = pygame.Surface((opt_rect.width, opt_rect.height), pygame.SRCALPHA)
        for y in range(opt_rect.height):
            ratio = y / opt_rect.height
            r = int(120 + 80*ratio)
            g = int(80 + 100*ratio)
            b = int(255 - 40*ratio)
            a = 255
            pygame.draw.line(grad, (r,g,b,a), (0,y), (opt_rect.width,y))
        screen.blit(grad, (opt_rect.x, opt_rect.y))
        is_hover = opt_rect.collidepoint(pygame.mouse.get_pos())
        if is_hover:
            pygame.draw.rect(screen, (255,255,255,60), opt_rect, border_radius=18)
        if option == selected:
            pygame.draw.rect(screen, (180,255,255), opt_rect, 3, border_radius=18)
        else:
            pygame.draw.rect(screen, (180,120,255), opt_rect, 1, border_radius=18)
        # Icon đều, nhỏ hơn, căn giữa dòng
        icon = None
        if 'DFS' in option:
            icon = icon_font.render("🧩", True, (255,255,255))
        elif 'BFS' in option:
            icon = icon_font.render("🌳", True, (255,255,255))
        elif 'UCS' in option:
            icon = icon_font.render("💎", True, (255,255,255))
        elif 'Astar' in option:
            icon = icon_font.render("⭐", True, (255,255,255))
        elif 'Greedy' in option:
            icon = icon_font.render("⚡", True, (255,255,255))
        text = font.render(option, True, (255,255,255))
        icon_x = opt_rect.x + 16
        icon_y = opt_rect.y + (opt_rect.height - icon.get_height())//2 if icon else opt_rect.y+6
        text_x = opt_rect.x + 52
        text_y = opt_rect.y + (opt_rect.height - text.get_height())//2
        if icon:
            screen.blit(icon, (icon_x, icon_y))
            screen.blit(text, (text_x, text_y))
        else:
            screen.blit(text, (opt_rect.x+18, opt_rect.y+7))
        rects.append(opt_rect)
    return rects
def draw_text_outline(screen, text, pos, color, outline_color, outline_width=1, center=False, font=None):
    """Draw text with an outline for readability."""
    if font is None:
        font = pygame.font.SysFont("Poppins", 20)
    base = font.render(text, True, color)
    ox, oy = pos
    if center:
        ox -= base.get_width() // 2
        oy -= base.get_height() // 2
    # draw outline by blitting same text several times offset
    for dx in range(-outline_width, outline_width+1):
        for dy in range(-outline_width, outline_width+1):
            if dx == 0 and dy == 0:
                continue
            screen.blit(font.render(text, True, outline_color), (ox+dx, oy+dy))
    screen.blit(base, (ox, oy))


def draw_text(screen, text, pos, color, center=False, font=None):
    if font is None:
        font = pygame.font.SysFont("Poppins", 18)
    surf = font.render(text, True, color)
    x, y = pos
    if center:
        x -= surf.get_width() // 2
        y -= surf.get_height() // 2
    screen.blit(surf, (x, y))


def flat_to_matrix(flat, rows, cols):
    """Convert flat list/iterable into matrix (list of lists) row-major."""
    mat = []
    for r in range(rows):
        row = []
        for c in range(cols):
            idx = r*cols + c
            if idx < len(flat):
                row.append(flat[idx])
            else:
                row.append(None)
        mat.append(row)
    return mat


def draw_matrix(screen, matrix, x, y, cell_w, cell_h, fonts, colors, tiles):
    """Vẽ một ma trận puzzle nhỏ sử dụng hình ảnh các ô."""
    rows = len(matrix)
    cols = len(matrix[0]) if rows > 0 else 0
    for r in range(rows):
        for c in range(cols):
            val = matrix[r][c]
            rect = pygame.Rect(x + c * cell_w, y + r * cell_h, cell_w - 1, cell_h - 1)
            
            # Chỉ vẽ ô nếu giá trị không phải là 0 (ô trống)
            if val is not None and val != 0:
                # Sử dụng hình ảnh từ danh sách `tiles`
                tile_img = pygame.transform.smoothscale(tiles[val - 1], (rect.width, rect.height))
                screen.blit(tile_img, rect.topleft)

            # Vẽ viền cho ô trống để dễ nhìn
            if val == 0:
                pygame.draw.rect(screen, colors.get('border', (120, 120, 160)), rect, 1)


def draw_history_panel(screen, history_groups, scroll_offset, panel_rect, close_rect, fonts, colors, tiles):
    """Vẽ panel lịch sử theo nhóm, with ms time and layout.

    `history_groups` expected to be an ordered dict or dict mapping
    state_tuple -> {'rows':R, 'cols':C, 'results':[{'algorithm':..,'steps':..,'visited_count':..,'generated_count':..,'execution_time':..}, ...]}
    """
    # 1. Vẽ các thành phần chung của panel
    pygame.draw.rect(screen, colors['bg'], panel_rect, border_radius=15)
    pygame.draw.rect(screen, colors['border'], panel_rect, 3, border_radius=15)
    draw_text_outline(screen, "Solve History", (panel_rect.centerx, panel_rect.top + 40),
                      colors['title'], colors['black'], 2, center=True, font=fonts['state'])
    pygame.draw.rect(screen, (200, 50, 50), close_rect, border_radius=5)
    draw_text(screen, "X", close_rect.center, colors['white'], center=True, font=fonts['btn'])

    # 2. Tạo vùng cắt và vẽ tiêu đề cho bảng
    header_y = panel_rect.y + 85
    content_y_start = header_y + 35
    content_rect = pygame.Rect(panel_rect.x + 20, content_y_start, panel_rect.width - 40, panel_rect.bottom - content_y_start - 20)

    # Định nghĩa vị trí X cho từng cột
    table_x_start = panel_rect.x + 160
    col_x = {
        "algo": table_x_start,
        "steps": table_x_start + 130,
        "visited": table_x_start + 210,
        "generated": table_x_start + 310,
        "time": table_x_start + 430,
    }

    # Vẽ dòng tiêu đề của bảng
    draw_text_outline(screen, "Algorithm", (col_x["algo"], header_y), colors['white'], colors['black'], 1, font=fonts['btn'])
    draw_text_outline(screen, "Steps", (col_x["steps"], header_y), colors['white'], colors['black'], 1, font=fonts['btn'])
    draw_text_outline(screen, "Visited", (col_x["visited"], header_y), colors['white'], colors['black'], 1, font=fonts['btn'])
    draw_text_outline(screen, "Generated", (col_x["generated"], header_y), colors['white'], colors['black'], 1, font=fonts['btn'])
    draw_text_outline(screen, "Time (ms)", (col_x["time"], header_y), colors['white'], colors['black'], 1, font=fonts['btn'])

    # Vẽ đường kẻ ngang dưới tiêu đề
    pygame.draw.line(screen, colors['border'], (panel_rect.x + 20, header_y + 25), (panel_rect.right - 20, header_y + 25), 2)

    # 3. Vẽ nội dung các hàng
    screen.set_clip(content_rect)

    if not history_groups:
        draw_text_outline(screen, "No history yet.", panel_rect.center, colors['white'], colors['black'], 1, center=True, font=fonts['label'])
    else:
        y_cursor = content_rect.top - scroll_offset

        group_padding, row_height, header_height = 40, 35, 110

        # iterate in insertion order if dict-like, else iterate items
        for state_tuple, group_data in history_groups.items():
            group_height = header_height + (len(group_data['results']) * row_height) + group_padding

            if y_cursor + group_height > content_rect.top and y_cursor < content_rect.bottom:
                # Vẽ puzzle mini đại diện cho nhóm
                rows, cols = group_data.get('rows', ROWS), group_data.get('cols', COLS)
                matrix = flat_to_matrix(list(state_tuple), rows, cols) if isinstance(state_tuple, (list, tuple)) else flat_to_matrix(list(state_tuple), rows, cols)
                puzzle_w, puzzle_h = 100, 100
                puzzle_x, puzzle_y = content_rect.left + 10, y_cursor + 5

                frame_rect = pygame.Rect(puzzle_x, puzzle_y, puzzle_w, puzzle_h)
                padding = 2
                grid_w, grid_h = puzzle_w - padding*2, puzzle_h - padding*2
                cell_width, cell_height = max(8, grid_w // cols), max(8, grid_h // rows)
                pygame.draw.rect(screen, colors['box'], frame_rect, border_radius=8)
                draw_matrix(screen, matrix, puzzle_x + padding, puzzle_y + padding, cell_width, cell_height, fonts, colors, tiles)

                # Vẽ bảng kết quả cho nhóm
                for i, result in enumerate(group_data['results']):
                    # Căn chỉnh vị trí Y của hàng đầu tiên ngang với puzzle mini
                    row_y = puzzle_y + (i * row_height)

                    draw_text_outline(screen, result.get('algorithm', result.get('method', 'N/A')), (col_x["algo"], row_y), colors['white'], colors['black'], 1, font=fonts['btn'])
                    draw_text_outline(screen, str(result.get('steps', result.get('steps', 0))), (col_x["steps"], row_y), colors['white'], colors['black'], 1, font=fonts['btn'])
                    draw_text_outline(screen, str(result.get('visited_count', result.get('visited', 'N/A'))), (col_x["visited"], row_y), colors['white'], colors['black'], 1, font=fonts['btn'])
                    draw_text_outline(screen, str(result.get('generated_count', result.get('generated', 'N/A'))), (col_x["generated"], row_y), colors['white'], colors['black'], 1, font=fonts['btn'])

                    # Chuyển đổi giây sang mili giây (* 1000) và làm tròn
                    exec_time = result.get('execution_time', result.get('time', 0.0))
                    time_ms = exec_time * 1000
                    draw_text_outline(screen, f"{time_ms:.1f}", (col_x["time"], row_y), colors['white'], colors['black'], 1, font=fonts['btn'])

            y_cursor += group_height

    screen.set_clip(None)