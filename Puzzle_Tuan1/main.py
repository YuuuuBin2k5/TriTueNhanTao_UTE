import pygame
import pygame.gfxdraw
from Game import board_random, find_blank, solve_with_meta, dfs, bfs, ucs, astar_h1, astar_h2, greedy, TileMoveAnim, write_config_and_restart, save_player_info
from ui import draw_button, draw_board, draw_board_goal, draw_history_panel, draw_victory, load_and_slice
from config import *
import time
from tkinter import Tk, filedialog
import tkinter.simpledialog
import math
import traceback
from multiprocessing import Process, Queue
from ui import draw_decor_vertical_lines
from collections import OrderedDict
from ui import draw_list


# ================== MAIN ==================
def main():
    # ... (Toàn bộ code khởi tạo không thay đổi) ...
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Puzzle YuuuBin")
    pygame.display.set_icon(pygame.image.load("./images/iconGame.png"))
    clock = pygame.time.Clock()

    font = pygame.font.SysFont("Poppins", 36, bold=True)
    font_Goal = pygame.font.SysFont("Poppins", 36, bold=True)
    small_font = pygame.font.SysFont("Poppins", 24)

    left_cell_w = max(8, min(LEFT_BOARD_W // COLS, LEFT_BOARD_H // ROWS))
    left_cell_h = max(8, min(LEFT_BOARD_H // ROWS, LEFT_BOARD_W // COLS))
    right_cell_w = max(8, min(GOAL_BOARD_W // COLS, GOAL_BOARD_H // ROWS))
    right_cell_h = max(8, min(GOAL_BOARD_H // ROWS, GOAL_BOARD_W // COLS))

    try:
        tiles_full = load_and_slice("images/play.png", ROWS, COLS, left_cell_w, left_cell_h)
    except Exception as e:
        tiles_full = [pygame.Surface((left_cell_w, left_cell_h)) for _ in range(ROWS*COLS - 1)]
        for t in tiles_full: t.fill((200,200,200))
    try:
        tiles_goal = load_and_slice("images/play.png", ROWS, COLS, right_cell_w, right_cell_h)
    except Exception as e:
        tiles_goal = [pygame.Surface((right_cell_w, right_cell_h)) for _ in range(ROWS*COLS - 1)]
        for t in tiles_goal: t.fill((220,220,220))

    goal = list(range(1, ROWS*COLS)) + [None]
    left_numbers = board_random(goal)
    # Lưu lại trạng thái xuất phát để hiện đúng trong History
    start_board = left_numbers[:]
    moves = 0
    # Chỉ bắt đầu đếm thời gian khi người chơi thực hiện nước đi đầu tiên
    start_time = None
    # Thông tin người chơi
    player_name = None

    ai_solution, ai_step_idx = None, 0
    ai_auto, ai_counter, ai_delay = False, 0, 10
    ai_display = None
    mode = None
    in_menu = True
    options = ["DFS", "BFS", "UCS", "Astar (h1)", "Astar (h2)", "Greedy"]
    single_solution, single_step_idx = None, 0
    single_auto, single_counter, single_delay = False, 0, 5
    algo_choice = options[0]
    current_puzzle_state = 'Ready'

    btn_single = pygame.Rect(WIDTH//2-120, 180, 240, 60)
    btn_ai = pygame.Rect(WIDTH//2-120, 260, 240, 60)
    btn_custom = pygame.Rect(WIDTH//2-120, 340, 240, 60)
    btn_exit = pygame.Rect(WIDTH//2-120, 420, 240, 60)
    btn_random = pygame.Rect(BTN_X + 100, BTN_Y+50, BTN_W, BTN_H)
    btn_load   = pygame.Rect(BTN_X + 100, BTN_Y+130, BTN_W, BTN_H)
    btn_auto   = pygame.Rect(BTN_X + 100, BTN_Y+150, BTN_W, BTN_H)
    btn_solve  = pygame.Rect(BTN_X + 100, BTN_Y+210, BTN_W, BTN_H)
    btn_reset  = pygame.Rect(370 , 300, BTN_W, BTN_H)
    btn_history = pygame.Rect(BTN_X +100, BTN_Y+290, BTN_W, BTN_H)

    anim = None
    anim_board = None
    anim_moves = 0
    anim_time = 0
    running = True
    selected = options[0]
    dropdown_open = False
    rect = pygame.Rect(btn_solve.x, btn_solve.y + btn_solve.height + 10, btn_solve.width+100, 35)
    prev_board = None
    prev_moves = None
    prev_start_time = None
    error_message = None
    error_timer = 0
    history = []
    history_open = False
    history_scroll = 0
    history_close_rect = None
    # Cờ đánh dấu đã lưu kết quả chưa để tránh ghi lặp
    result_saved = False

    max_depth_dfs = 20
    dfs_depth_text = str(max_depth_dfs)
    dfs_depth_val = max_depth_dfs

    input_box_w, input_box_h = 120, 36
    input_rows_text = str(ROWS)
    input_cols_text = str(COLS)
    input_rows_val = ROWS
    input_cols_val = COLS
    input_active = None
    input_rows_rect = pygame.Rect(LEFT_BOARD_X+30, LEFT_BOARD_Y + LEFT_BOARD_H + 60, input_box_w, input_box_h)
    input_cols_rect = pygame.Rect(LEFT_BOARD_X + input_box_w + 120, LEFT_BOARD_Y + LEFT_BOARD_H + 60, input_box_w, input_box_h)

    dfs_input_rect = pygame.Rect(btn_solve.x, btn_solve.y - 60, 70, 35)
    
    while running:
        try:
            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()[0]
            btn_list = [btn_single, btn_ai, btn_exit, btn_random, btn_load, btn_auto, btn_solve, btn_reset, btn_history]
            hovered_btn = None
            pressed_btn = None
            for btn in btn_list:
                if btn.collidepoint(mouse_pos):
                    hovered_btn = btn
                    if mouse_pressed:
                        pressed_btn = btn
                    break
            # Trong thời gian auto-solve (AI hoặc Single), khóa mọi thao tác người dùng
            input_locked = (ai_auto or single_auto)
            for ev in pygame.event.get():
                if ev.type == pygame.QUIT:
                    running = False
                elif ev.type == pygame.MOUSEWHEEL:
                    if history_open and not input_locked:
                        scroll_step = 40
                        history_scroll = max(0, history_scroll - ev.y * scroll_step)
                elif ev.type == pygame.MOUSEBUTTONDOWN:
                    if input_locked:
                        # Bỏ qua mọi click khi đang tự động giải
                        continue
                    if history_open and history_close_rect and history_close_rect.collidepoint(ev.pos):
                        history_open = False
                        continue
                    if in_menu:
                        if btn_single.collidepoint(ev.pos):
                            in_menu = False; mode = "single"; result_saved = False
                            # Hỏi tên người chơi khi vào chế độ Single (nếu chưa có)
                            if player_name is None:
                                try:
                                    Tk().withdraw()
                                    name = tkinter.simpledialog.askstring("Người chơi", "Nhập tên của bạn:")
                                    if name:
                                        player_name = name.strip()
                                except Exception:
                                    player_name = None
                        elif btn_ai.collidepoint(ev.pos):
                            in_menu = False; mode = "ai"; result_saved = False
                            meta = solve_with_meta(algo_choice, left_numbers, goal, max_depth_dfs)
                            ai_solution = meta['solution']
                            if ai_solution:
                                ai_auto, ai_display = True, ai_solution[0][:]
                                prev_board = left_numbers[:]
                                prev_moves = moves
                                prev_start_time = start_time
                                history.append(meta)
                        elif btn_custom.collidepoint(ev.pos):
                            in_menu = False
                        elif btn_exit.collidepoint(ev.pos):
                            running = False
                    else:
                        if input_locked:
                            # Khóa tương tác trên gameplay khi auto-solve
                            continue
                        if mode == "single":
                            if dropdown_open:
                                option_clicked = False
                                for i, option in enumerate(options):
                                    opt_rect = pygame.Rect(rect.x , rect.y + rect.height + i*rect.height, rect.width, rect.height)
                                    if opt_rect.collidepoint(ev.pos):
                                        selected = option
                                        algo_choice = selected
                                        single_solution, single_step_idx, single_auto = None, 0, False
                                        ai_solution, ai_step_idx, ai_auto = None, 0, False
                                        dropdown_open = False
                                        option_clicked = True
                                        break
                                if option_clicked:
                                    continue 
                                if not rect.collidepoint(ev.pos):
                                    dropdown_open = False
                            elif rect.collidepoint(ev.pos):
                                dropdown_open = True
                            
                        # Logic xử lý click cho tất cả các ô nhập liệu (ĐÃ SỬA)
                        clicked_on_input = False
                        if mode == "single" and algo_choice == "DFS":
                            if dfs_input_rect.collidepoint(ev.pos):
                                input_active = 'dfs'
                                clicked_on_input = True
                        
                        if not clicked_on_input and input_rows_rect.collidepoint(ev.pos):
                            input_active = 'rows'
                            clicked_on_input = True
                        elif not clicked_on_input and input_cols_rect.collidepoint(ev.pos):
                            input_active = 'cols'
                            clicked_on_input = True
                            
                        if not clicked_on_input:
                            input_active = None

                        if btn_random.collidepoint(ev.pos):
                            left_numbers = board_random(goal)
                            start_board = left_numbers[:]
                            moves = 0
                            start_time = None
                            current_puzzle_state = 'Randomized'
                            result_saved = False
                            single_solution, single_step_idx, single_auto = None, 0, False
                            ai_solution = None
                            if mode=="ai":
                                meta = solve_with_meta(algo_choice, left_numbers, goal, max_depth_dfs)
                                ai_solution = meta['solution']
                                if ai_solution:
                                    history.append(meta)
                            ai_step_idx, ai_display, ai_auto = 0, left_numbers[:], (mode=="ai" and ai_solution)
                        elif btn_load.collidepoint(ev.pos):
                            Tk().withdraw()
                            path = filedialog.askopenfilename(filetypes=[("Image files","*.png;*.jpg")])
                            if path: 
                                tiles_full[:] = load_and_slice(path, ROWS, COLS, left_cell_w, left_cell_h)
                                tiles_goal[:] = load_and_slice(path, ROWS, COLS, right_cell_w, right_cell_h)
                        elif btn_auto.collidepoint(ev.pos) and mode=="ai":
                            meta = solve_with_meta(algo_choice, left_numbers, goal, max_depth_dfs)
                            ai_solution = meta['solution']
                            if ai_solution:
                                ai_step_idx, ai_auto, ai_display = 0, True, ai_solution[0][:]
                                prev_board = left_numbers[:]
                                prev_moves = moves
                                prev_start_time = start_time
                                history.append(meta)
                                result_saved = False
                        elif mode=="single" and btn_solve.collidepoint(ev.pos):
                            try:
                                # <<< THAY ĐỔI THEO YÊU CẦU >>>: Quay lại logic thông báo lỗi đơn giản cho DFS
                                meta = solve_with_meta(algo_choice, left_numbers, goal, max_depth_dfs)
                                single_solution = meta['solution']

                                if single_solution:
                                    # Tìm thấy lời giải, xử lý như bình thường
                                    prev_board = left_numbers[:]
                                    prev_moves = moves
                                    prev_start_time = start_time
                                    single_step_idx, single_auto = 0, True
                                    history.append(meta)
                                    result_saved = False
                                elif algo_choice == "DFS":
                                    # Nếu là DFS và không tìm thấy, chỉ hiện thông báo
                                    error_message = f"Không tìm thấy lời giải với độ sâu {max_depth_dfs}.\nHãy tăng giới hạn và thử lại."
                                    error_timer = 240 # Hiện thông báo trong 4 giây

                            except Exception as e:
                                print("[ERROR] Exception during solve click handling:")
                                traceback.print_exc()
                                single_solution = None
                        elif left_numbers == goal and btn_reset.collidepoint(ev.pos):
                            if prev_board:
                                left_numbers = prev_board[:]
                                start_board = left_numbers[:]
                                moves = prev_moves if prev_moves is not None else 0
                                start_time = prev_start_time if prev_start_time is not None else None
                                prev_board = None; prev_moves = None; prev_start_time = None
                            else:
                                left_numbers = board_random(goal)
                                start_board = left_numbers[:]
                                moves = 0
                                start_time = None
                            single_solution, single_step_idx, single_auto = None, 0, False
                            ai_solution, ai_step_idx, ai_auto, ai_display = None, 0, False, None
                            current_puzzle_state = 'Ready'
                            result_saved = False
                        elif btn_history.collidepoint(ev.pos):
                            history_open = not history_open
                        else:
                            if not dropdown_open:
                                mx, my = ev.pos
                                if LEFT_BOARD_X <= mx < LEFT_BOARD_X + LEFT_BOARD_W and LEFT_BOARD_Y <= my < LEFT_BOARD_Y + LEFT_BOARD_H:
                                    c = (mx - LEFT_BOARD_X) // left_cell_w
                                    r = (my - LEFT_BOARD_Y) // left_cell_h
                                    if 0 <= r < ROWS and 0 <= c < COLS:
                                        idx_blank = find_blank(left_numbers)
                                        row_b, col_b = divmod(idx_blank, COLS)
                                        if abs(row_b - r) + abs(col_b - c) == 1 and not anim:
                                            num = left_numbers[r * COLS + c]
                                            now_click = time.time()
                                            # Bắt đầu timer ở nước đi đầu tiên của người chơi
                                            if start_time is None:
                                                start_time = now_click
                                            anim = TileMoveAnim(num, (r, c), (row_b, col_b), now_click)
                                            anim_board = left_numbers[:]; anim_moves = moves; anim_time = start_time
                                            prev_board = None; prev_moves = None; prev_start_time = None
                elif ev.type == pygame.KEYDOWN:
                    if input_locked:
                        # Khoá mọi nhập liệu khi auto-solve
                        continue
                    if input_active == 'dfs':
                        if ev.key == pygame.K_BACKSPACE: dfs_depth_text = dfs_depth_text[:-1]
                        elif ev.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                            try:
                                if dfs_depth_text.strip() != '':
                                    v = int(dfs_depth_text)
                                    dfs_depth_val = max(1, min(1000, v))
                                    dfs_depth_text = str(dfs_depth_val)
                                    max_depth_dfs = dfs_depth_val
                            except:
                                dfs_depth_text = str(max_depth_dfs)
                            input_active = None
                        else:
                            ch = ev.unicode
                            if ch.isdigit(): dfs_depth_text += ch
                    elif input_active:
                        if ev.key == pygame.K_BACKSPACE:
                            if input_active == 'rows': input_rows_text = input_rows_text[:-1]
                            else: input_cols_text = input_cols_text[:-1]
                        elif ev.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                            try:
                                if input_active == 'rows' and input_rows_text.strip() != '': v = int(input_rows_text); input_rows_val = max(2, min(10, v))
                                elif input_active == 'cols' and input_cols_text.strip() != '': v = int(input_cols_text); input_cols_val = max(2, min(10, v))
                                write_config_and_restart(input_rows_val, input_cols_val)
                            except: pass
                            input_active = None
                        else:
                            ch = ev.unicode
                            if ch.isdigit():
                                if input_active == 'rows': input_rows_text += ch
                                else: input_cols_text += ch
            
            # ... (Phần code update và vẽ giao diện không thay đổi) ...
            # Update auto solve single
            if mode == "single" and single_auto and single_solution is not None and not anim:
                single_counter += 1
                if single_counter >= single_delay:
                    single_counter = 0
                    if single_step_idx < len(single_solution):
                        curr_state = single_solution[single_step_idx]
                        if curr_state is not None and isinstance(curr_state, list):
                            left_numbers = curr_state[:]
                            if single_step_idx > 0: moves += 1
                        else:
                            single_auto = False; single_solution = None; single_step_idx = 0
                        single_step_idx += 1
                    else:
                        # Kết thúc auto-solve single
                        single_auto = False
                        # Nếu sau khi tự động giải xong đạt goal, lưu kết quả là "Algorithm" thay vì người chơi
                        if left_numbers == goal:
                            elapsed = int(time.time() - start_time) if start_time else 0
                            save_player_info(
                                name=player_name or 'Guest',
                                moves=moves,
                                elapsed_seconds=elapsed,
                                rows=ROWS,
                                cols=COLS,
                                algorithm=f"Auto {algo_choice}"
                            )
                            result_saved = True
            # Update AI auto
            if mode=="ai" and ai_auto and ai_solution and not anim:
                ai_counter += 1
                if ai_counter >= ai_delay:
                    ai_counter = 0
                    if ai_step_idx < len(ai_solution):
                        ai_display = ai_solution[ai_step_idx][:]; ai_step_idx += 1
                    else:
                        ai_auto = False
            # Vẽ nền
            t = pygame.time.get_ticks() / 1000.0
            grad = pygame.Surface((WIDTH, HEIGHT))
            for y in range(HEIGHT):
                ratio = y / HEIGHT; r = int(30 + 40 * (1 - ratio)); g = int(20 + 30 * (1 - ratio)); b = int(60 + 100 * ratio)
                pygame.draw.line(grad, (r, g, b), (0, y), (WIDTH, y))
            screen.blit(grad, (0,0))
            num_stars = 120
            for i in range(num_stars):
                star_x = int((i*97)%WIDTH + 50*math.sin(t + i)) % WIDTH; star_y = int((i*53)%HEIGHT + 30*math.cos(t*0.7 + i)) % HEIGHT
                star_size = 1 + int(1.5 + math.sin(t*2 + i*1.7))%2; star_alpha = 180 + int(75*abs(math.sin(t*1.5 + i)))
                star_color = (220, 220, 255, star_alpha); s = pygame.Surface((star_size*2, star_size*2), pygame.SRCALPHA)
                pygame.draw.circle(s, star_color, (star_size, star_size), star_size); screen.blit(s, (star_x, star_y))
            # Vẽ giao diện
            if in_menu:
                title = pygame.font.SysFont("Poppins", 60, bold=True).render("Puzzle Game", True, (120,80,255)); screen.blit(title, (WIDTH//2-title.get_width()//2, 100))
                draw_button(screen, btn_single, "Single Player", font, is_hovered=(hovered_btn==btn_single), is_pressed=(pressed_btn==btn_single))
                draw_button(screen, btn_ai, "Play vs AI", font, is_hovered=(hovered_btn==btn_ai), is_pressed=(pressed_btn==btn_ai))
                draw_button(screen, btn_exit, "Exit", font, is_hovered=(hovered_btn==btn_exit), is_pressed=(pressed_btn==btn_exit))
            else:
                if anim and not anim.done: draw_board(screen, anim_board, tiles_full, LEFT_BOARD_X, LEFT_BOARD_Y, "Board Nè", font, False, anim_moves, anim_time, anim, cell_w=left_cell_w, cell_h=left_cell_h)
                else: draw_board(screen, left_numbers, tiles_full, LEFT_BOARD_X, LEFT_BOARD_Y, "Board Nè", font, False, moves, start_time, cell_w=left_cell_w, cell_h=left_cell_h)
                if mode=="ai":
                    draw_board(screen, ai_display if ai_display else left_numbers, tiles_full, AI_BOARD_X, AI_BOARD_Y, "AI Board", font, False, 0, None, cell_w=left_cell_w, cell_h=left_cell_h)
                    draw_button(screen, btn_auto, "AI Solve", small_font, is_hovered=(hovered_btn==btn_auto), is_pressed=(pressed_btn==btn_auto))
                if mode=="single":
                    draw_button(screen, btn_history, "History", small_font, is_hovered=(hovered_btn==btn_history), is_pressed=(pressed_btn==btn_history))
                    draw_board_goal(screen, goal, tiles_goal, GOAL_X, GOAL_Y, "Goal", font_Goal)
                    draw_button(screen, btn_solve, f"Solve", small_font, is_hovered=(hovered_btn==btn_solve), is_pressed=(pressed_btn==btn_solve))
                    draw_button(screen, btn_random, "Random", small_font, is_hovered=(hovered_btn==btn_random), is_pressed=(pressed_btn==btn_random))
                    draw_button(screen, btn_load, "Load Img", small_font, is_hovered=(hovered_btn==btn_load), is_pressed=(pressed_btn==btn_load))
                    try: font_dropdown = pygame.font.Font("Orbitron-Bold.ttf", 24)
                    except: font_dropdown = pygame.font.SysFont("Poppins", 24, bold=True)
                    rect = pygame.Rect(btn_solve.x-250, btn_solve.y + btn_solve.height -230, btn_solve.width +30, 35)
                    pygame.draw.rect(screen, (180,120,255), rect, 4, border_radius=18)
                    text = font_dropdown.render(selected, True, (255,255,255)); screen.blit(text, (rect.x+18, rect.y+7))
                    pygame.gfxdraw.filled_trigon(screen, rect.right-25, rect.y+rect.height//2-5, rect.right-10, rect.y+rect.height//2-5, rect.right-17, rect.y+rect.height//2+8, (200,200,255))
                    if dropdown_open:
                        draw_list(screen, pygame.Rect(rect.x, rect.y+rect.height, rect.width, rect.height), selected, options, font_dropdown)
                    if left_numbers == goal:
                        draw_victory(screen, font, t)
                        draw_button(screen, btn_reset, "Reset", small_font, is_hovered=(hovered_btn==btn_reset), is_pressed=(pressed_btn==btn_reset))
                        # Khi người chơi tự tay giải xong (không phải auto), lưu thông tin
                        if not ai_auto and not single_auto and not result_saved:
                            elapsed = int(time.time() - start_time) if start_time else 0
                            save_player_info(
                                name=player_name or 'Guest',
                                moves=moves,
                                elapsed_seconds=elapsed,
                                rows=ROWS,
                                cols=COLS,
                                algorithm='Human'
                            )
                            # Thêm vào History trong game để hiển thị (gộp theo trạng thái xuất phát)
                            try:
                                meta_human = {
                                    'method': f"Human ({player_name or 'Guest'})",
                                    'start': start_board[:],
                                    'goal': goal[:],
                                    'generated': -1,
                                    'visited': -1,
                                    'time': float(elapsed),
                                    'solution': None,
                                    'steps': int(moves)
                                }
                                history.append(meta_human)
                            except Exception:
                                pass
                            result_saved = True
                
                draw_decor_vertical_lines(screen)
                rows_color = (255,255,255) if input_active == 'rows' else (235,235,235); cols_color = (255,255,255) if input_active == 'cols' else (235,235,235)
                pygame.draw.rect(screen, rows_color, input_rows_rect, border_radius=6); pygame.draw.rect(screen, cols_color, input_cols_rect, border_radius=6)
                pygame.draw.rect(screen, (100,100,100), input_rows_rect, 2, border_radius=6); pygame.draw.rect(screen, (100,100,100), input_cols_rect, 2, border_radius=6)
                r_label = small_font.render("Rows:", True, (0,0,0)); screen.blit(r_label, (input_rows_rect.x - 68, input_rows_rect.y + (input_box_h - r_label.get_height())//2))
                c_label = small_font.render("Cols:", True, (0,0,0)); screen.blit(c_label, (input_cols_rect.x - 68, input_cols_rect.y + (input_box_h - c_label.get_height())//2))
                rows_txt = small_font.render(input_rows_text, True, (0,0,0)); screen.blit(rows_txt, (input_rows_rect.x + 8, input_rows_rect.y + (input_box_h - rows_txt.get_height())//2))
                cols_txt = small_font.render(input_cols_text, True, (0,0,0)); screen.blit(cols_txt, (input_cols_rect.x + 8, input_cols_rect.y + (input_box_h - cols_txt.get_height())//2))
                if mode == "single" and algo_choice == "DFS":
                    # ĐÃ SỬA: Thay đổi vị trí ô nhập liệu Depth
                    dfs_input_rect = pygame.Rect(btn_solve.x -40, btn_solve.y - 220, 70, 35)
                    dfs_label = small_font.render("Depth:", True, (255,255,255)); screen.blit(dfs_label, (dfs_input_rect.x - dfs_label.get_width() - 8, dfs_input_rect.y + (dfs_input_rect.height - dfs_label.get_height())//2))
                    dfs_color = (255,255,255) if input_active == 'dfs' else (235,235,235); pygame.draw.rect(screen, dfs_color, dfs_input_rect, border_radius=8)
                    pygame.draw.rect(screen, (100,100,100), dfs_input_rect, 2, border_radius=8)
                    dfs_txt_surf = small_font.render(dfs_depth_text, True, (0,0,0)); screen.blit(dfs_txt_surf, (dfs_input_rect.x + 8, dfs_input_rect.y + (dfs_input_rect.height - dfs_txt_surf.get_height())//2))
                if history_open:
                    panel_rect = pygame.Rect(BTN_X-440, BTN_Y+70, 750, 400)
                    try:
                        history_groups = OrderedDict()
                        for entry in history:
                            board = entry.get('start', entry.get('board', [None]*(ROWS*COLS))); key = tuple(board)
                            if key not in history_groups: history_groups[key] = {'rows': ROWS, 'cols': COLS, 'results': []}
                            res = {'algorithm': entry.get('method', 'N/A'), 'steps': entry.get('steps', 0), 'visited_count': entry.get('visited', -1), 'generated_count': entry.get('generated', -1), 'execution_time': entry.get('time', 0.0)}
                            history_groups[key]['results'].append(res)
                        fonts = {'state': pygame.font.SysFont("Poppins", 22, bold=True), 'btn': small_font, 'label': small_font}
                        colors = {'bg': (30, 34, 40), 'border': (80, 80, 140), 'title': (255, 255, 255), 'black': (0, 0, 0), 'white': (255, 255, 255), 'box': (240, 240, 250), 'tile': (200, 200, 220), 'text': (20, 20, 40)}
                        close_rect = pygame.Rect(panel_rect.right - 36, panel_rect.y + 16, 24, 24); history_close_rect = close_rect
                        group_padding, row_height, header_height = 40, 35, 110
                        total_height = sum(header_height + (len(g['results']) * row_height) + group_padding for g in history_groups.values())
                        content_height = max(0, panel_rect.height - 140); max_scroll = max(0, total_height - content_height)
                        history_scroll = max(0, min(history_scroll, max_scroll))
                        draw_history_panel(screen, history_groups, history_scroll, panel_rect, close_rect, fonts, colors, tiles_full)
                    except Exception as e: traceback.print_exc()
                if error_timer and error_message:
                    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA); overlay.fill((0,0,0,160)); screen.blit(overlay, (0,0))
                    lines = error_message.splitlines(); em_font = pygame.font.SysFont("Poppins", 20, bold=True)
                    y0 = HEIGHT//2 - (len(lines)*22)//2
                    for i, line in enumerate(lines):
                        txt = em_font.render(line, True, (255,200,200)); screen.blit(txt, (WIDTH//2 - txt.get_width()//2, y0 + i*22))
                    error_timer = max(0, error_timer-1)
            pygame.display.flip()
            clock.tick(FPS)
        except Exception as e:
            tb = traceback.format_exc(); print("[UNCAUGHT EXCEPTION]", tb)
            error_message = tb; error_timer = 240
            continue
        if anim and anim.done:
            idx_blank = find_blank(anim_board); idx_tile = anim.start_pos[0]*COLS + anim.start_pos[1]
            anim_board[idx_blank], anim_board[idx_tile] = anim_board[idx_tile], anim_board[idx_blank]
            left_numbers = anim_board[:]; moves = anim_moves + 1; start_time = anim_time
            anim = None; anim_board = None
    pygame.quit()

if __name__ == "__main__":
    main()