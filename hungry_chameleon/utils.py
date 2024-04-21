"""
Helper functions for a Pygame-based game, Hungry Chameleon.

Functions:
    load_sprite: Loads and optionally converts a sprite image from the assets
    directory.
    wrap_position: Wraps a game object's position to keep it within the screen
    boundaries.
    get_random_position: Generates a random position within the screen bounds.
    get_random_velocity: Generates a random velocity vector within specified
    speed limits.
"""

import random
from pygame.image import load
from pygame.math import Vector2


def load_sprite(name, with_alpha=True):
    """
    Loads a sprite from the specified file path and applies pixel format
    conversion.

    Args:
        name (str): The name of the sprite file (without file extension).
        with_alpha (bool): If True, convert the sprite to include an alpha
        channel.

    Returns:
        The loaded and converted sprite.
    """
    path = f"assets/sprites/{name}.png"
    loaded_sprite = load(path)

    if with_alpha:
        return loaded_sprite.convert_alpha()
    else:
        return loaded_sprite.convert()


def wrap_position(position, screen):
    """
    Wraps the position around the edges of the surface to create a seamless
    effect.

    Args:
        position (Vector2): The original position vector.
        screen (pygame.Surface): The surface whose dimensions to use for
        wrapping.

    Returns:
        The wrapped position vector.
    """
    x, y = position
    w, h = screen.get_size()
    return Vector2(x % w, y % h)


def get_random_position(screen):
    """
    Generates a random position within the boundaries of the given screen.

    Args:
        screen (pygame.Surface): The surface to get the width and height for
        boundaries.

    Returns:
        A vector representing a random position within the screen.
    """
    return Vector2(
        random.randrange(screen.get_width()),
        random.randrange(screen.get_height()),
    )


def get_random_velocity(min_speed, max_speed):
    """
    Generates a random velocity vector with a magnitude between specified min
    and max speeds.

    Args:
        min_speed (int): The minimum speed of the velocity vector.
        max_speed (int): The maximum speed of the velocity vector.

    Returns:
        A vector representing the random velocity.
    """
    speed = random.randint(min_speed, max_speed)
    angle = random.randrange(0, 360)
    return Vector2(speed, 0).rotate(angle)
