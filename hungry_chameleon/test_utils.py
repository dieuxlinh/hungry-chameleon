"""
Unit tests for the utility functions in the utils module.

This module contains tests for various utility functions that support game
functionality, including sprite loading, position wrapping, and random
position and velocity generation.
"""

import pytest
import pygame

from utils import (
    load_sprite,
    wrap_position,
    get_random_position,
    get_random_velocity,
)


@pytest.fixture(name="test_screen")
def screen():
    """
    Provides a pygame display context.
    """
    pygame.init()
    return pygame.display.set_mode((800, 600))


def test_load_sprite():
    """
    Tests that the load_sprite function correctly loads a sprite file and
    returns a pygame surface.
    """
    pygame.display.set_mode((800, 600))
    sprite = load_sprite("background", False)
    assert isinstance(sprite, pygame.Surface)


def test_wrap_position(test_screen):
    """
    Tests that wrap_position correctly wraps a position around the screen
    boundaries when exceeding them.
    """
    pos = wrap_position(pygame.math.Vector2(810, 610), test_screen)
    assert 0 <= pos.x < 800 and 0 <= pos.y < 600


def test_get_random_position(test_screen):
    """
    Tests that get_random_position generates a position within the screen
    boundaries.
    """
    pos = get_random_position(test_screen)
    assert 0 <= pos.x < 800 and 0 <= pos.y < 600


def test_get_random_velocity():
    """
    Tests that get_random_velocity generates a velocity vector with magnitude
    within specified limits.
    """
    velocity = get_random_velocity(1, 10)
    assert 1 <= velocity.length() <= 10
