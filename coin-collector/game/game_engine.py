"""
GameEngine: owns the player, coins, obstacles and round state.

Task 1: collected coins are removed so each coin scores exactly once.
Task 2: coins come in three types (bronze, silver, gold).
Task 3: obstacles cost a life; a short invincibility window stops a single
        touch from draining lives every frame.
Task 4: 30-second round; ends when time runs out or lives reach zero.
        Press R on the game-over screen to start a new round.
"""

import math
import random
import pygame

from game.player import Player
from game.coin import Coin
from game.obstacle import Obstacle
from game.collection import check_collection, check_obstacle_hit
from game.renderer import WIDTH, HEIGHT

NUM_COINS = 6
NUM_OBSTACLES = 4
COIN_TYPE_NAMES = ["bronze", "silver", "gold"]

START_LIVES = 3
ROUND_SECONDS = 30
INVINCIBLE_MS = 1000  # grace period after an obstacle hit


class GameEngine:
    def __init__(self):
        self.reset()

    def reset(self):
        """Start a fresh round: score, lives, timer, coins and obstacles."""
        self.player = Player(x=WIDTH / 2, y=HEIGHT / 2)
        self.obstacles = self._make_obstacles()
        self.coins = self._make_coins()
        self.score = 0
        self.lives = START_LIVES
        self.round_start = pygame.time.get_ticks()
        self.time_left = ROUND_SECONDS
        self.invincible_until = 0
        self.game_over = False

    # ---------- spawning ----------

    def _make_obstacles(self):
        """Obstacles stay inside the play area and away from the player's start."""
        safe_zone = self.player.get_rect().inflate(160, 160)
        obstacles = []
        while len(obstacles) < NUM_OBSTACLES:
            size = 36
            x = random.randint(size, WIDTH - size)
            y = random.randint(size, HEIGHT - size)
            candidate = Obstacle(x=x, y=y, size=size)
            rect = candidate.get_rect()
            if rect.colliderect(safe_zone):
                continue
            if any(rect.colliderect(o.get_rect().inflate(30, 30)) for o in obstacles):
                continue
            obstacles.append(candidate)
        return obstacles

    def _make_coins(self):
        """A batch of coins cycling bronze/silver/gold, never inside an obstacle."""
        coins = []
        for i in range(NUM_COINS):
            coin_type = COIN_TYPE_NAMES[i % len(COIN_TYPE_NAMES)]
            while True:
                coin = self._random_coin(coin_type)
                if not any(coin.get_rect().colliderect(o.get_rect().inflate(10, 10))
                           for o in self.obstacles):
                    break
            coins.append(coin)
        return coins

    def _random_coin(self, coin_type):
        x = random.randint(30, WIDTH - 30)
        y = random.randint(30, HEIGHT - 30)
        return Coin(x=x, y=y, radius=12, coin_type=coin_type)

    # ---------- per-frame ----------

    def handle_input(self, keys_pressed):
        if self.game_over:
            if keys_pressed[pygame.K_r]:
                self.reset()
            return

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
        if self.game_over:
            return

        now = pygame.time.get_ticks()

        # Timer
        elapsed = (now - self.round_start) / 1000
        self.time_left = max(0, ROUND_SECONDS - elapsed)
        if self.time_left <= 0:
            self.game_over = True
            return

        # Coins: each collected coin scores once and is removed
        collected = check_collection(self.player, self.coins)
        for coin in collected:
            self.score += coin.value
            self.coins.remove(coin)
        if not self.coins:
            self.coins = self._make_coins()  # keep the round going

        # Obstacles: lose one life per hit, then a brief grace period
        if now >= self.invincible_until and check_obstacle_hit(self.player, self.obstacles):
            self.lives -= 1
            self.invincible_until = now + INVINCIBLE_MS

        if self.lives <= 0:
            self.game_over = True

    def draw(self, surface, font):
        from game import renderer
        invincible = pygame.time.get_ticks() < self.invincible_until
        renderer.draw_scene(surface, self.player, self.coins, self.obstacles, invincible)
        renderer.draw_text(surface, font, f"Score: {self.score}", (10, 10))
        renderer.draw_text(surface, font, f"Lives: {self.lives}", (10, 38))
        renderer.draw_text(surface, font, f"Time: {math.ceil(self.time_left)}", (WIDTH - 110, 10))
        if self.game_over:
            renderer.draw_game_over(surface, font, self.score)