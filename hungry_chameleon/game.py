"""
A simple Pygame-based game module featuring a chameleon catching flies.

The module is structured using the MVC pattern:
- GameModel manages the game's state and object interactions.
- GameView handles all the graphical output.
- GameController orchestrates the game loop, input handling, and updates.
"""

import pygame
from models import Chameleon, Fly
from utils import get_random_position, load_sprite
from pygame.math import Vector2
from pygame.transform import rotozoom


UP = Vector2(0, -1)


# Model
class GameModel:
    """
    Represents the game model, responsible for managing the game state,
    including initializing and updating all game objects.

    Attributes:
        screen (pygame.Surface): The display where game objects are drawn.
        chameleon (Chameleon): The main character controlled by the player.
        fly (list of Fly): List of fly objects that chameleon aims to catch.
    """

    MIN_FLY_DISTANCE = 250

    def __init__(self, screen):
        """
        Initializes the game model with a display surface.

        Args:
            screen (pygame.Surface): The display surface.
        """
        self.screen = screen
        self.chameleon = Chameleon((400, 300), self.screen)
        self.fly = self._init_flies(6)

    def _init_flies(self, count):
        """
        Initializes a specified number of flies at positions at least
        MIN_FLY_DISTANCE away from the chameleon.

        Args:
            count (int): Number of flies to initialize.

        Returns:
            flies (list): A list of initialized flies.
        """
        flies = []
        for _ in range(count):
            while True:
                position = get_random_position(self.screen)
                if (
                    position.distance_to(self.chameleon.position)
                    > self.MIN_FLY_DISTANCE
                ):
                    break
            flies.append(Fly(position, self.screen))
        return flies

    def update(self):
        """
        Updates all game objects in the model. Moves each object and checks
        for collisions.
        """
        for game_object in self.get_game_objects():
            game_object.move()
        self.check_collisions()

    def get_game_objects(self):
        """
        Retrieves all active game objects.

        Returns:
            list: A list containing the chameleon and all flies.
        """
        return [*self.fly, self.chameleon] if self.chameleon else self.fly

    def check_collisions(self):
        """
        Checks for collisions between the chameleon and any fly. Sets the
        chameleon to None if a collision occurs, effectively removing it from
        the game.
        """
        for fly in self.fly:
            if fly.collides_with(self.chameleon):
                if not self.chameleon.tongue:
                    self.chameleon = None
                    break
                self.fly.remove(fly)


# View
class GameView:
    """
    Represents the visual aspect of the game, rendering all visual
    elements on the screen.

    Attributes:
        screen (pygame.Surface): The display surface for drawing the game.
        background (pygame.Surface): The background image of the game scene.
    """

    def __init__(self, screen):
        """
        Initializes the game view with a display surface.

        Args:
            screen (pygame.Surface): The display surface.
        """
        self.screen = screen
        self.background = pygame.transform.scale(
            load_sprite("Sky_Blue", False), (1000, 1000)
        )

    def draw(self, game_objects):
        """
        Draws the background and all active game objects to the screen.

        Args:
            game_objects (list): A list of game objects to be drawn.
        """
        self.screen.blit(self.background, (0, 0))
        for game_object in game_objects:
            # game_object.draw()
            self.draw_object(game_object)
        pygame.display.update()

    def draw_object(self, game_object):
        """
        Draws a game object on the screen.

        Args:
            game_object: An object in the game (fly/chameleon).
        """
        angle = game_object.direction.angle_to(UP)
        rotated_surface = rotozoom(game_object.sprite, angle, 1.0)
        rotated_surface_size = Vector2(rotated_surface.get_size())
        blit_position = game_object.position - rotated_surface_size * 0.5
        self.screen.blit(rotated_surface, blit_position)
        if game_object == Chameleon:
            game_object.sprite = game_object.no_tongue


# Controller
class GameController:
    """
    Controls the game flow, handling game events and updates.

    Attributes:
        model (GameModel): The game's model managing the state.
        view (GameView): The game's view handling rendering.
        clock (pygame.time.Clock): Clock for managing the game's frame rate.
    """

    def __init__(self, model, view):
        """
        Initializes the game controller with the model and view.

        Args:
            model (GameModel): The game model.
            view (GameView): The game view.
        """
        self.model = model
        self.view = view
        self.clock = pygame.time.Clock()
        self._init_pygame()

    def _init_pygame(self):
        """
        Initializes Pygame and sets up the game window.
        """
        pygame.init()
        pygame.display.set_caption("Hungry Chameleon")

    def run(self):
        """
        Main game loop that handles input, updates the game model, and renders
        the game view.
        """
        while True:
            self.handle_input()
            self.model.update()
            self.view.draw(self.model.get_game_objects())
            self.clock.tick(60)

    def handle_input(self):
        """
        Handles user inputs.

        Responds to left and right keys to rotate the chameleon.
        Exits the game if the quit event is triggered or if ESC key is pressed.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (
                event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
            ):
                quit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.model.chameleon.rotate(clockwise=False)
        if keys[pygame.K_RIGHT]:
            self.model.chameleon.rotate(clockwise=True)
        if keys[pygame.K_SPACE]:
            self.model.chameleon.tongue = True
            self.model.chameleon.change_sprite()
