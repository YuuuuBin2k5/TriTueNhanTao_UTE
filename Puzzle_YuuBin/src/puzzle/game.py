"""Logic lõi cho trò puzzle.

File này điều phối vòng lặp chính, trạng thái game và tích hợp các
UI (Menu / Play / GameOver).
"""
import pygame
import random
from .settings import WIDTH, HEIGHT, TILE_SIZE
from .ui.menu import Menu
from .ui.play import Play

# Robust imports for UI modules: prefer package-relative, then src.* then top-level


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Puzzle Game")

        self.state = "menu"  # 'menu' | 'playing' | 'settings'
        self.menu = Menu(self.screen)
        self.play = None
        self.clock = pygame.time.Clock()


    def state_manager(self):
        # vẽ theo trạng thái hiện tại (không gọi flip ở đây)
        if self.state == "menu":
            self.menu.draw()
        elif self.state == "playing":
            if self.play:
                self.play.draw()

    def run(self):
        running = True
        # obtain FPS setting
        try:
            from .settings import FPS
        except Exception:
            from puzzle.settings import FPS

        while running:
            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                else:
                    if self.state == "menu":
                        self.menu.handle_input(event)
                    elif self.state == "playing" and self.play is not None:
                        # forward events to Play instance if it provides a handler
                        try:
                            handler = getattr(self.play, "handle_input", None)
                            if callable(handler):
                                handler(event)
                        except Exception:
                            # swallow to keep main loop running; Play should be robust
                            pass

            # process menu actions
            if self.state == "menu":
                action = self.menu.pop_action()
                if action == "start":
                    try:
                        self.play = Play(self.screen)
                    except Exception:
                        self.play = None
                    self.state = "playing"
                elif action == "settings":
                    self.state = "settings"
                elif action == "quit":
                    running = False

            # Update
            self.update()

            # Draw
            self.screen.fill((0, 0, 0))
            self.state_manager()
            pygame.display.flip()

            # Tick
            self.clock.tick(FPS)

        pygame.quit()

    def handle_input(self, event):
        # placeholder for non-menu input handling
        pass

    def update(self):
        pass

    def draw(self):
        self.screen.fill((0, 0, 0))
