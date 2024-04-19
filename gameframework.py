import pygame
import random
from pygame.math import Vector2
from pygame.transform import rotozoom

from utils import load_sprite, wrap_position

# Constants
UP = pygame.math.Vector2(0, -1)  # Define the UP vector


class Game:
    def __init__(self):
        self.score = 0
        self.high_score = 0
        self.game_over = False

    def update_score(self, points):
        self.score += points
        if self.score > self.high_score:
            self.high_score = self.score


class GameController:
    def __init__(self, game, chameleon):
        self.game = game
        self.chameleon = chameleon

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.chameleon.rotate(
                clockwise=False
            )  # Rotate chameleon counterclockwise for left arrow
        if keys[pygame.K_RIGHT]:
            self.chameleon.rotate(
                clockwise=True
            )  # Rotate chameleon clockwise for right arrow
        if keys[pygame.K_SPACE]:
            self.chameleon.stick_out_tongue()  # Trigger chameleon action for spacebar


class GameView:
    def __init__(self, game, chameleon):
        self.game = game
        self.chameleon = chameleon
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Welcome to Chameleon")

    def display_game(self):
        self.screen.fill((0, 0, 0))
        # Rotate chameleon image based on its direction
        rotated_surface = pygame.transform.rotate(
            self.chameleon.image, -self.chameleon.direction.angle_to(UP)
        )
        rotated_rect = rotated_surface.get_rect(
            center=self.chameleon.rect.center
        )
        self.screen.blit(rotated_surface, rotated_rect)
        pygame.display.update()


class Chameleon:
    def __init__(self):
        # Start in center screen
        self.position = pygame.math.Vector2(400, 300)
        self.image = pygame.Surface(
            (50, 50)
        )  # Placeholder image, replace which images
        self.rect = self.image.get_rect(center=self.position)

        # Start action should be rest
        self.action = False

        # Start by existing (not dead yet since no contact with flies)
        self.existence = True

        # Direction vector
        self.direction = pygame.math.Vector2(UP)

    def rotate(self, clockwise=True):
        sign = 1 if clockwise else -1
        angle = 5 * sign  # Rotation angle in degrees
        self.direction.rotate_ip(angle)  # Rotate direction vector in place

    def stick_out_tongue(self):
        # Implement the behavior for sticking out tongue
        pass  # Placeholder, need to implement (change out images from no tongue to tongue out)


class Fly:
    def __init__(self):
        # Start in random locations from edge of screen
        self.position = [random.randint(0, 800), random.randint(0, 600)]

        # Start flying in at different speeds between 0 and 1
        self.action = [random.uniform(0, 1), random.uniform(0, 1)]

        # Start by existing (not dead yet since no contact with flies)
        self.existence = True


def main():
    game = Game()
    chameleon = Chameleon()
    game_view = GameView(game, chameleon)
    game_controller = GameController(game, chameleon)
    # Create 10 flies
    flies = [Fly() for _ in range(10)]

    while not game.game_over:
        game_controller.handle_input()
        # GAME LOGIC HERE
        # Need to take in inputs
        game_view.display_game()

    pygame.quit()


if __name__ == "__main__":
    main()
