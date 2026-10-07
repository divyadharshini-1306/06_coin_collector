# Coin Collector

A Pygame game: move the player with the arrow keys and collect coins before time runs out.

## Setup
    python -m venv venv
    source venv/Scripts/activate     # Git Bash on Windows
    pip install -r requirements.txt
    python main.py

## Controls
- Arrow keys: move
- R: restart (on the game-over screen)

## What was done
- **Bug fix:** collected coins were never removed, so standing on one scored every frame. Coins are now removed on pickup and a new one spawns.
- **Coin types:** bronze (+1), silver (+3), gold (+5), with different sizes, colors and spawn chances.
- **Obstacles:** solid walls that block the player; coins never spawn inside them.
- **Timed round:** 30-second countdown, game-over screen with final score, R to restart.

## Structure
    main.py
    game/  (game_engine, player, coin, collection, obstacle, renderer)