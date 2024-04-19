import pygame

from utils import load_sprite
from models import Chameleon, Fly
from utils import get_random_position, load_sprite


class HungryChameleon:
    MIN_FLY_DISTANCE = 250

    def __init__(self):
        self._init_pygame()
        self.screen = pygame.display.set_mode((800, 600))
        self.background = pygame.transform.scale(
            load_sprite("Sky_Blue", False), (1000, 1000)
        )
        self.clock = pygame.time.Clock()

        self.chameleon = Chameleon((400, 300))
        self.fly = []

        for _ in range(6):
            while True:
                position = get_random_position(self.screen)
                if (
                    position.distance_to(self.chameleon.position)
                    > self.MIN_FLY_DISTANCE
                ):
                    break
            self.fly.append(Fly(position))

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
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (
                event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
            ):
                quit()

        is_keys_pressed = pygame.key.get_pressed()

        if is_keys_pressed[pygame.K_LEFT]:
            self.chameleon.rotate(
                clockwise=False
            )  # Rotate chameleon counterclockwise for left arrow
        if is_keys_pressed[pygame.K_RIGHT]:
            self.chameleon.rotate(
                clockwise=True
            )  # Rotate chameleon clockwise for right arrow
        if is_keys_pressed[pygame.K_SPACE]:
            pass
            # self.chameleon.stick_out_tongue()  # Trigger chameleon action for spacebar

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
        for game_object in self._get_game_objects():
            game_object.draw(self.screen)
        pygame.display.flip()
        self.clock.tick(60)
