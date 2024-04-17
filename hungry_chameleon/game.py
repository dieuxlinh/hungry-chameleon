import pygame

from utils import load_sprite
from models import Chameleon, Fly


class HungryChameleon:
    def __init__(self):
        self._init_pygame()
        self.screen = pygame.display.set_mode((800, 600))
        self.background = pygame.transform.scale(
            load_sprite("background2", False), (1000, 1000)
        )
        self.clock = pygame.time.Clock()

        self.chameleon = Chameleon((400, 300))
        self.fly = [Fly((400, 300)) for _ in range(6)]

    def main_loop(self):
        while True:
            self._handle_input()
            self._process_game_logic()
            self._draw()

    def _get_game_objects(self):
        game_objects = [*self.fly]

        if self.chameleon:
            game_objects.append(self.chameleon)

        return game_objects

    def _init_pygame(self):
        pygame.init()
        pygame.display.set_caption("Hungry Chameleon")

    def _handle_input(self):

        # Quitting the game
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (
                event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
            ):
                quit()
        pass

    def _process_game_logic(self):
        for game_object in self._get_game_objects():
            game_object.move(self.screen)

        if self.chameleon:
            for fly in self.fly:
                if fly.collides_with(self.chameleon):
                    self.chameleon = None
                    break

    def _draw(self):
        self.screen.blit(self.background, (0, 0))
        self.chameleon.draw(self.screen)
        self.fly.draw(self.screen)
        pygame.display.flip()
        self.clock.tick(60)
