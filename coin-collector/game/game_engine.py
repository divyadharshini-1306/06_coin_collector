"""
GameEngine: owns the player and all coins.

Task 1: collected coins are removed so each coin scores exactly once.
Task 2: coins come in three types (bronze, silver, gold) with different values.
"""

import random
import pygame

from game.player import Player
from game.coin import Coin
from game.collection import check_collection
from game.renderer import WIDTH, HEIGHT

NUM_COINS = 6
COIN_TYPE_NAMES = ["bronze", "silver", "gold"]


class GameEngine:
    def __init__(self):
        self.player = Player(x=WIDTH / 2, y=HEIGHT / 2)
        # Cycle through the types so every round has bronze, silver and gold
        self.coins = [
            self._random_coin(COIN_TYPE_NAMES[i % len(COIN_TYPE_NAMES)])
            for i in range(NUM_COINS)
        ]
        self.score = 0

    def _random_coin(self, coin_type):
        x = random.randint(30, WIDTH - 30)
        y = random.randint(30, HEIGHT - 30)
        return Coin(x=x, y=y, radius=12, coin_type=coin_type)

    def handle_input(self, keys_pressed):
        dx = dy = 0
        if keys_pressed[pygame.K_UP]:
            dy -= self.player.speed
        if keys_pressed[pygame.K_DOWN]:
            dy += self.player.speed
        if keys_pressed[pygame.K_LEFT]:
            dx -= self.player.speed
        if keys_pressed[pygame.K_RIGHT]:
            dx += self.player.speed
        self.player.move(dx, dy, WIDTH, HEIGHT)

    def update(self):
        collected = check_collection(self.player, self.coins)
        for coin in collected:
            self.score += coin.value
            self.coins.remove(coin)

    def draw(self, surface, font):
        from game import renderer
        renderer.draw_scene(surface, self.player, self.coins)
        renderer.draw_text(surface, font, f"Score: {self.score}", (10, 10))