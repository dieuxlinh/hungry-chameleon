"""
Entry point for a Pygame-based application, Hungry Chameleon.
"""

import pygame
from game import GameController, GameModel, GameView

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((800, 600), pygame.DOUBLEBUF)
    model = GameModel(screen)
    view = GameView(screen)
    controller = GameController(model, view)
    controller.run()
