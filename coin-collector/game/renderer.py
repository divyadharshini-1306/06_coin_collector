"""
renderer: all pygame drawing lives here, kept separate from game logic.
"""

import pygame

WIDTH, HEIGHT = 700, 500
WINDOW_SIZE = (WIDTH, HEIGHT)

COLOR_BG = (35, 45, 35)
COLOR_PLAYER = (80, 180, 255)
COLOR_TEXT = (255, 255, 255)
COLOR_OBSTACLE = (200, 60, 60)
COLOR_OBSTACLE_BORDER = (120, 30, 30)
COLOR_BANNER = (255, 220, 80)

_big_font = None


def _get_big_font():
    global _big_font
    if _big_font is None:
        _big_font = pygame.font.SysFont("consolas", 48)
    return _big_font


def draw_scene(surface, player, coins, obstacles=(), invincible=False):
    surface.fill(COLOR_BG)
    for obstacle in obstacles:
        rect = obstacle.get_rect()
        pygame.draw.rect(surface, COLOR_OBSTACLE, rect)
        pygame.draw.rect(surface, COLOR_OBSTACLE_BORDER, rect, width=3)
    for coin in coins:
        pygame.draw.circle(surface, coin.color, (int(coin.x), int(coin.y)), coin.radius)
    # Blink the player while invincible after a hit
    if not (invincible and (pygame.time.get_ticks() // 100) % 2 == 0):
        pygame.draw.rect(surface, COLOR_PLAYER, player.get_rect(), border_radius=4)


def draw_text(surface, font, text, pos, color=COLOR_TEXT):
    surface.blit(font.render(text, True, color), pos)


def draw_banner(surface, font, text):
    surf = font.render(text, True, COLOR_BANNER)
    rect = surf.get_rect(center=(surface.get_width() // 2, surface.get_height() // 2))
    surface.blit(surf, rect)


def _draw_centered(surface, font, text, center, color):
    surf = font.render(text, True, color)
    surface.blit(surf, surf.get_rect(center=center))


def draw_game_over(surface, font, score):
    overlay = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 170))
    surface.blit(overlay, (0, 0))

    cx = surface.get_width() // 2
    cy = surface.get_height() // 2
    _draw_centered(surface, _get_big_font(), "GAME OVER", (cx, cy - 50), COLOR_BANNER)
    _draw_centered(surface, font, f"Final score: {score}", (cx, cy + 5), COLOR_TEXT)
    _draw_centered(surface, font, "Press R to play again", (cx, cy + 40), COLOR_TEXT)