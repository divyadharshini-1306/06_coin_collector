"""
collection: figures out which coins the player has collected this frame,
and whether the player is touching an obstacle.
"""


def check_collection(player, coins):
    """
    Returns the list of coins the player is currently overlapping.
    """
    player_rect = player.get_rect()
    collected = []
    for coin in coins:
        if player_rect.colliderect(coin.get_rect()):
            collected.append(coin)
    return collected


def check_obstacle_hit(player, obstacles):
    """
    Returns True if the player is currently overlapping any obstacle.
    """
    player_rect = player.get_rect()
    for obstacle in obstacles:
        if player_rect.colliderect(obstacle.get_rect()):
            return True
    return False