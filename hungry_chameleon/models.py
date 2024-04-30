"""
This module defines the basic game objects for a simple Pygame-based game.

Classes:
    GameObject: A base class for all movable entities in the game, providing
    common functionality such as drawing, moving, and collision detection.
    Chameleon: A specialized GameObject that represents the player's character.
    It can rotate and potentially stick out its tongue as part of its
    interaction in the game.
    Fly: A target GameObject that moves randomly across the game screen and can
    be caught by the Chameleon.
"""

import pygame
from pygame.math import Vector2
from pygame.transform import rotozoom

from utils import load_sprite, wrap_position, get_random_velocity

UP = Vector2(0, -1)


class GameObject:
    """
    A generic game object class that can be used as a base for all movable
    objects in the game.

    Attributes:
        position (Vector2): The current position of the object on the screen.
        sprite (pygame.Surface): The visual sprite associated with the game
        object.
        radius (float): The radius of the object, used for collision detection.
        velocity (Vector2): The velocity of the object, dictating its movement
        per frame.
        screen (pygame.Surface): The screen on which the object is drawn.
    """

    def __init__(self, position, sprite, velocity, screen):
        """
        Initializes a new game object.

        Args:
            position (tuple): The starting position of the object.
            sprite (pygame.Surface): The sprite image of the object.
            velocity (tuple): The initial velocity of the object.
            screen (pygame.Surface): The game screen where objects are drawn.
        """
        self.position = Vector2(position)
        self.sprite = sprite
        self.radius = sprite.get_width() / 2
        self.velocity = Vector2(velocity)
        self.screen = screen

    def draw(self):
        """
        NOT USED
        Draws the object's sprite at its current position on the screen.
        """
        blit_position = self.position - Vector2(self.radius)
        self.screen.blit(self.sprite, blit_position)

    def move(self):
        """
        Updates the object's position based on its velocity.

        Wraps the position around the screen boundaries if needed.
        """
        self.position = wrap_position(
            self.position + self.velocity, self.screen
        )

    def collides_with(self, other_obj):
        """
        Determines if this object has collided with another object.

        Args:
            other_obj (GameObject): The other game object to check collision
            against.

        Returns:
            bool: True if there is a collision; otherwise, False.
        """
        if other_obj:
            distance = self.position.distance_to(other_obj.position)
            if hasattr(other_obj, "tongue"):
                if other_obj.tongue:
                    return distance < (self.radius + other_obj.radius + 100)
            return distance < (self.radius + other_obj.radius - 10)


class Chameleon(GameObject):
    """
    Represents the Chameleon in the game, capable of rotating and sticking out
    its tongue.

    Attributes:
        direction (Vector2): The current facing direction of the chameleon.
    """

    MANEUVERABILITY = 3

    def __init__(self, position, rotation_point, screen):
        """
        Initializes the Chameleon object.

        Args:
            position (tuple): The initial position of the Chameleon.
            screen (pygame.Surface): The screen on which the Chameleon is drawn.
        """
        self.direction = Vector2(UP)
        self.tongue = False
        self.tongue_out = pygame.transform.scale(
            load_sprite("chameleon_with_tongue"), (150, 500)
        )

        self.no_tongue = pygame.transform.scale(
            load_sprite("chameleon_no_tongue"), (150, 500)
        )
        self.tongue_start_time = 0

        super().__init__(
            position,
            pygame.transform.scale(
                load_sprite("chameleon_no_tongue"), (150, 500)
            ),
            Vector2(0),
            screen,
        )
        self.rotation_point = Vector2(rotation_point)

    def rotate(self, clockwise=True):
        """
        Rotates the Chameleon either clockwise or counterclockwise.

        Args:
            clockwise (bool): True to rotate clockwise; False to rotate
            counterclockwise.
        """
        sign = 1 if clockwise else -1
        angle = self.MANEUVERABILITY * sign
        self.direction.rotate_ip(angle)
        self.position = self.rotation_point + (
            self.position - self.rotation_point
        ).rotate(angle)

    def draw(self):
        """
        NOT USED
        Draws the Chameleon with the current rotation applied to the
        sprite.
        """
        angle = self.direction.angle_to(UP)
        rotated_surface = rotozoom(self.sprite, angle, 1.0)
        rotated_surface_size = Vector2(rotated_surface.get_size())
        blit_position = self.position - rotated_surface_size * 0.5
        self.screen.blit(rotated_surface, blit_position)
        self.sprite = self.no_tongue

    def change_sprite(self):
        """
        Changes chameleon sprite based on spacebar press.
        """
        keys = pygame.key.get_pressed()

        if keys[pygame.K_SPACE]:
            self.sprite = self.tongue_out
            self.tongue = True
            self.tongue_start_time = pygame.time.get_ticks()
        elif (
            self.tongue
            and pygame.time.get_ticks() - self.tongue_start_time >= 1000
        ):
            self.sprite = self.no_tongue
            self.tongue = False

        self.update_tongue_time()

    def update_tongue_time(self):
        """
        Updates the tongue time.
        """
        if (
            self.tongue
            and pygame.time.get_ticks() - self.tongue_start_time >= 1000
        ):
            self.sprite = self.no_tongue
            self.tongue = False

    def move(self):
        """
        Moves the chameleon and changes its sprite.
        """
        self.change_sprite()
        super().move()


class Fly(GameObject):
    """
    Represents a Fly, a target object in the game that the Chameleon tries to
    catch.

    Attributes:
        direction (Vector2): The current flying direction of the fly.
    """

    MANEUVERABILITY = 3

    def __init__(self, position, screen):
        """
        Initializes the Fly object.

        Args:
            position (tuple): The initial position of the Fly.
            screen (pygame.Surface): The screen on which the Fly is drawn.
        """
        self.direction = Vector2(UP)

        super().__init__(
            position,
            pygame.transform.scale(load_sprite("fly"), (30, 30)),
            get_random_velocity(1, 2),
            screen,
        )

    def draw(self):
        """
        NOT USED
        Draws the Fly with the current rotation applied to the sprite.
        """
        angle = self.direction.angle_to(UP)
        rotated_surface = rotozoom(self.sprite, angle, 1.0)
        rotated_surface_size = Vector2(rotated_surface.get_size())
        blit_position = self.position - rotated_surface_size * 0.5
        self.screen.blit(rotated_surface, blit_position)

    def rotate(self, clockwise=True):
        """
        Rotates the Fly either clockwise or counterclockwise.

        Args:
            clockwise (bool): True to rotate clockwise; False to rotate
            counterclockwise.
        """
        sign = 1 if clockwise else -1
        angle = self.MANEUVERABILITY * sign
        self.direction.rotate_ip(angle)
