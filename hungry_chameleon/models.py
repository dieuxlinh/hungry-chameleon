import pygame

from pygame.math import Vector2
from pygame.transform import rotozoom

from utils import load_sprite, wrap_position, get_random_velocity

UP = Vector2(0, -1)


class GameObject:
    def __init__(self, position, sprite, velocity):
        self.position = Vector2(position)
        self.sprite = sprite
        self.radius = sprite.get_width() / 2
        self.velocity = Vector2(velocity)

    def draw(self, surface):
        blit_position = self.position - Vector2(self.radius)
        surface.blit(self.sprite, blit_position)

    def move(self, surface):
        self.position = wrap_position(self.position + self.velocity, surface)

    def collides_with(self, other_obj):
        distance = self.position.distance_to(other_obj.position)
        return distance < self.radius + other_obj.radius


class Chameleon(GameObject):

    MANEUVERABILITY = 3

    def __init__(self, position):
        self.direction = Vector2(UP)

        super().__init__(
            position,
            pygame.transform.scale(
                load_sprite("chamaeleon_no_tongue"), (100, 100)
            ),
            Vector2(0),
        )

    def rotate(self, clockwise=True):
        sign = 1 if clockwise else -1
        angle = self.MANEUVERABILITY * sign
        self.direction.rotate_ip(angle)

    def draw(self, surface):
        angle = self.direction.angle_to(UP)
        rotated_surface = rotozoom(self.sprite, angle, 1.0)
        rotated_surface_size = Vector2(rotated_surface.get_size())
        blit_position = self.position - rotated_surface_size * 0.5
        surface.blit(rotated_surface, blit_position)

    def stick_out_tongue():
        """
        if space bar not pressed:
            image = "chameleon_no_tongue"
        else/ if space bar is pressed:
            image = "chameleon_with_tongue" for 0.5 seconds
        """
        pass


class Fly(GameObject):

    MANEUVERABILITY = 3

    def __init__(self, position):
        self.direction = Vector2(UP)

        super().__init__(
            position,
            pygame.transform.scale(load_sprite("fly"), (20, 20)),
            get_random_velocity(1, 3),
        )

    def draw(self, surface):
        angle = self.direction.angle_to(UP)
        rotated_surface = rotozoom(self.sprite, angle, 1.0)
        rotated_surface_size = Vector2(rotated_surface.get_size())
        blit_position = self.position - rotated_surface_size * 0.5
        surface.blit(rotated_surface, blit_position)

    def rotate(self, clockwise=True):
        sign = 1 if clockwise else -1
        angle = self.MANEUVERABILITY * sign
        self.direction.rotate_ip(angle)
