import pygame
import random


class Game:
    def __init__(self):
        self.score = int
        self.high_score = int
        self.game_over = False

    def update_score(self, points):
        self.score += points
        if self.score > self.high_score:
            self.high_score = self.score


class GameController:
    def __init__(self, game):
        self.game = game

    def input(self):
        # ESC key for quit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()


class GameView:
    def __init__(self, game):
        self.game = game
        pygame.init()
        # Setting the initial display
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Welcome to Chameleon")

    def display_game(self):
        self.screen.fill((0, 0, 0))  # Clear the screen
        # Display chameleon, flies, score, etc.
        pygame.display.update()


class Chameleon:
    def __init__(self):
        # Start in center sreen
        self.position = [400, 300]

        # This is wrong, but start action should be rest
        self.action = False

        # Start by existing (not dead yet since no contact with flies)
        self.existence = True


class Fly:
    def __init__(self):
        # Start in random locations from edge of sreen
        self.position = [random.randint(0, 800), random.randint(0, 600)]

        # Start flying in at different speeds between 0 and 1
        self.action = [random.uniform(0, 1), random.uniform(0, 1)]

        # Start by existing (not dead yet since no contact with flies)
        self.existence = True


def main():
    game = Game()
    game_view = GameView(game)
    game_controller = GameController(game)
    chameleon = Chameleon()
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
