import pygame
from .settings_ui import HEIGHT, WIDTH

import importlib
try:
    puzzle_utils = importlib.import_module("puzzle.core.utils")
except Exception:
    try:
        puzzle_utils = importlib.import_module("src.puzzle.core.utils")
    except Exception:
        puzzle_utils = None


class Play:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 48)
        self.tile_font = pygame.font.Font(None, 56)

        # board là danh sách 3x3; sử dụng puzzle_utils.shuffle_board khi có
        if puzzle_utils and hasattr(puzzle_utils, "shuffle_board"):
            self.board = puzzle_utils.shuffle_board(moves=40)
        else:
            # fallback: solved board
            self.board = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]

        # hình học vẽ ô
        self.cols = 3
        self.btn_w = 120
        self.btn_h = 120
        self.start_x = (WIDTH - (self.btn_w * self.cols + 10 * (self.cols - 1))) // 2
        self.start_y = 120
        self.spacing = 10
        self.win = False

    def board_to_rects(self):
        rects = []
        for r in range(3):
            for c in range(3):
                x = self.start_x + c * (self.btn_w + self.spacing)
                y = self.start_y + r * (self.btn_h + self.spacing)
                rects.append(pygame.Rect(x, y, self.btn_w, self.btn_h))
        return rects

    def draw(self):
        self.screen.fill((8, 10, 14))
        rects = self.board_to_rects()
        for idx, rect in enumerate(rects):
            r = idx // 3
            c = idx % 3
            val = self.board[r][c]
            if val == 0:
                # ô trống
                pygame.draw.rect(self.screen, (30, 30, 30), rect, border_radius=8)
            else:
                pygame.draw.rect(self.screen, (60, 140, 220), rect, border_radius=8)
                txt = self.tile_font.render(str(val), True, (255, 255, 255))
                tr = txt.get_rect(center=rect.center)
                self.screen.blit(txt, tr)

        if self.win:
            wfont = pygame.font.Font(None, 64)
            msg = wfont.render("You win!", True, (255, 220, 80))
            mr = msg.get_rect(center=(WIDTH // 2, 60))
            self.screen.blit(msg, mr)

    def button_layout(self):
        # API tương thích: trả về rect của các ô
        return self.board_to_rects()

    def handle_input(self, event):
        # xử lý input từ người chơi (nhấp chuột)
        if self.win:
            return
        rects = self.button_layout()
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mx, my = event.pos
            for idx, rect in enumerate(rects):
                if rect.collidepoint((mx, my)):
                    r = idx // 3
                    c = idx % 3
                    val = self.board[r][c]
                    if val != 0 and puzzle_utils:
                        new_board, moved = puzzle_utils.move_tile(self.board, val)
                        if moved:
                            self.board = new_board
                            if puzzle_utils.is_solved(self.board):
                                self.win = True
                    break
