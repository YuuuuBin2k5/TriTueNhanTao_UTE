import pygame
import math


class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 64)
        self.options = ["Start", "Settings", "Quit"]
        self.selected_option = 0
        self.action = None  # 'start', 'settings', 'quit'

    # Tính toán vị trí và kích thước của các nút trên màn hình.
    def _button_layout(self):
        """Trả về danh sách rect của các nút dựa trên kích thước màn hình hiện tại."""
        w, h = self.screen.get_size()
        btn_w = min(400, w - 200)
        btn_h = 72
        start_y = h // 3
        spacing = 24
        rects = []
        for i in range(len(self.options)):
            x = (w - btn_w) // 2
            y = start_y + i * (btn_h + spacing)
            rects.append(pygame.Rect(x, y, btn_w, btn_h))
        return rects

    def draw(self):
        self.screen.fill((12, 14, 20))
        rects = self._button_layout()
        now = pygame.time.get_ticks()

        for i, rect in enumerate(rects):
            hovered = (i == self.selected_option)

            # base and border colors
            base = (30, 34, 44)
            highlight = (50, 130, 255)
            border = (140, 140, 160)

            color = highlight if hovered else base

            # draw button background
            pygame.draw.rect(self.screen, color, rect, border_radius=10)

            # pulsing glow for hovered button
            if hovered:
                phase = (now % 800) / 800.0
                pulse = 0.5 + 0.5 * math.sin(phase * 2 * math.pi)
                glow_alpha = int(80 * pulse)
                glow = pygame.Surface((rect.w + 8, rect.h + 8), pygame.SRCALPHA)
                glow.fill((80, 160, 255, glow_alpha))
                self.screen.blit(glow, (rect.x - 4, rect.y - 4), special_flags=0)

            # border
            pygame.draw.rect(self.screen, border, rect, 3, border_radius=10)

            # text
            txt_color = (255, 255, 255) if hovered else (220, 220, 220)
            text = self.font.render(self.options[i], True, txt_color)
            text_rect = text.get_rect(center=rect.center)
            self.screen.blit(text, text_rect)

        # small footer hint
        hint = pygame.font.Font(None, 20).render("Use mouse or ↑↓ and Enter", True, (160, 160, 170))
        self.screen.blit(hint, (10, self.screen.get_height() - 30))

    # Xử lý sự kiện từ người dùng (chuột và bàn phím).
    def handle_input(self, event):
        rects = self._button_layout()

        if event.type == pygame.MOUSEMOTION:
            mx, my = event.pos
            for i, r in enumerate(rects):
                if r.collidepoint(mx, my):
                    self.selected_option = i
                    break

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mx, my = event.pos
            for i, r in enumerate(rects):
                if r.collidepoint(mx, my):
                    opt = self.options[i]
                    if opt == "Start":
                        self.action = "start"
                    elif opt == "Settings":
                        self.action = "settings"
                    elif opt == "Quit":
                        self.action = "quit"

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_option = (self.selected_option - 1) % len(self.options)
            elif event.key == pygame.K_DOWN:
                self.selected_option = (self.selected_option + 1) % len(self.options)
            elif event.key == pygame.K_RETURN:
                opt = self.options[self.selected_option]
                if opt == "Start":
                    self.action = "start"
                elif opt == "Settings":
                    self.action = "settings"
                elif opt == "Quit":
                    self.action = "quit"

    def select_button(self):
        # legacy API kept
        opt = self.options[self.selected_option]
        if opt == "Start":
            self.action = "start"
        elif opt == "Settings":
            self.action = "settings"
        elif opt == "Quit":
            self.action = "quit"

    def pop_action(self):
        a = self.action
        self.action = None
        return a