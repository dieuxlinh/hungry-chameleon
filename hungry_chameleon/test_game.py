"""
Unit tests for the game module.

This module contains tests for the classes and methods in the game module,
including GameModel, GameView, and GameController. The tests are designed
to ensure that game state management, user interaction handling, and game
rendering are functioning as expected.
"""

import pytest
import pygame
from game import GameModel, GameView, GameController


@pytest.fixture(name="test_screen")
def screen():
    """
    Provides a pygame display context.
    """
    pygame.init()
    return pygame.display.set_mode((800, 600))


@pytest.fixture(name="test_game_model")
def game_model(test_screen):
    """
    Provides a GameModel instance for testing.
    """
    return GameModel(test_screen)


@pytest.fixture(name="test_game_view")
def game_view(test_screen):
    """
    Provides a GameView instance for testing.
    """
    return GameView(test_screen)


@pytest.fixture(name="test_game_controller")
def game_controller(test_game_model, test_game_view):
    """
    Provides a GameController instance for testing.
    """
    return GameController(test_game_model, test_game_view)


def test_game_model_initialization(test_game_model):
    """
    Tests that GameModel initializes with default values for attributes like
    score and game_over.
    """
    assert test_game_model.chameleon is not None
    assert len(test_game_model.fly) > 0
    assert test_game_model.score == 0
    assert test_game_model.high_score >= 0
    assert not test_game_model.game_over


def test_game_model_load_high_score(test_game_model):
    """
    Tests that GameModel correctly loads the high score from a file.
    """
    assert isinstance(test_game_model.load_high_score(), int)


def test_game_model_save_and_load_high_score(test_game_model):
    """
    Tests that GameModel saves to and then loads the high score correctly,
    ensuring data persistence.
    """
    test_game_model.high_score = 100
    test_game_model.save_high_score()
    assert test_game_model.load_high_score() == 100


def test_game_model_check_game_over(test_game_model):
    """
    Tests that GameModel accurately reports the game over status.
    """
    test_game_model.game_over = True
    assert test_game_model.check_game_over()
    test_game_model.game_over = False
    assert not test_game_model.check_game_over()


def test_game_view_initialization(test_game_view):
    """
    Tests that GameView initializes with necessary pygame surfaces for the
    display.
    """
    assert test_game_view.screen is not None
    assert test_game_view.background is not None


def test_game_controller_initialization(test_game_controller):
    """
    Tests that GameController initializes correctly and is ready to start
    running the game loop.
    """
    assert test_game_controller.screen is not None
    assert test_game_controller.model is not None
    assert test_game_controller.view is not None
    assert test_game_controller.running


def test_game_controller_input_handling(test_game_controller):
    """
    Tests that GameController correctly handles user input, particularly
    stopping the game on ESC key.
    """
    pygame.event.post(
        pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_ESCAPE})
    )
    test_game_controller.handle_input()
    assert not test_game_controller.running
