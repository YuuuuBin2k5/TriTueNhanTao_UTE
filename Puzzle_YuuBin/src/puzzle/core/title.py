"""Bộ vẽ tiêu đề sử dụng trong UI.

Cung cấp lớp trợ giúp nhỏ để vẽ tiêu đề trò chơi và subtitle tùy chọn
sử dụng phông của pygame.
"""
import pygame
from typing import Optional, Tuple


class Title:
    def __init__(self, text: str, subtitle: Optional[str] = None, pos: Optional[Tuple[int, int]] = None):
        self.text = text
        self.subtitle = subtitle
        self.pos = pos  # (x,y) center position; if None caller will position
        # fonts are created lazily when drawing to avoid pygame init order problems
        self._font = None
        self._subfont = None

    def _ensure_fonts(self):
        if self._font is None:
            self._font = pygame.font.Font(None, 64)
        if self.subtitle and self._subfont is None:
            self._subfont = pygame.font.Font(None, 28)

    def draw(self, screen: pygame.Surface, center_pos: Optional[Tuple[int, int]] = None):
        self._ensure_fonts()
        cx, cy = center_pos if center_pos is not None else (screen.get_width() // 2, 40)
        text_surf = self._font.render(self.text, True, (255, 230, 130))
        text_rect = text_surf.get_rect(center=(cx, cy))
        screen.blit(text_surf, text_rect)
        if self.subtitle:
            sub_surf = self._subfont.render(self.subtitle, True, (200, 200, 200))
            sub_rect = sub_surf.get_rect(center=(cx, cy + 40))
            screen.blit(sub_surf, sub_rect)
# puzzle/core/tile.py
import pygame

class Tile:
    def __init__(self, number, rect, font, color=(200,200,200)):
        self.number = number
        self.rect = rect
        self.font = font
        self.color = color

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        if self.number != 0:
            text = self.font.render(str(self.number), True, (0,0,0))
            text_rect = text.get_rect(center=self.rect.center)
            screen.blit(text, text_rect)
