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
        score (int): The player's score
    """

    MIN_FLY_DISTANCE = 250

    def __init__(self, screen):
        """
        Initializes the game model with a display surface.

        Args:
            screen (pygame.Surface): The display surface.
        """
        self.screen = screen
        self.chameleon = Chameleon((400, 190), (400, 290), self.screen)
        self.fly = self._init_flies(6)
        self.score = 0
        self.high_score_file = "HIGH_SCORE_FILE.txt"
        self.high_score = self.load_high_score()
        self.font = pygame.font.Font("Pulang.ttf", 40)
        self.tongue_time = 0

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

    def update_tongue_time(self):
        """
        Updates the tongue time.
        """
        if self.chameleon.tongue:
            self.tongue_time = pygame.time.get_ticks()

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
                if self.chameleon.tongue:
                    self.fly.remove(fly)
                    self.score += 100
                    if self.score > self.high_score:
                        self.high_score = self.score
                        self.save_high_score()
                else:
                    self.chameleon = None
                    break

    def load_high_score(self):
        """
        Loads the high score from the high score file.

        Returns:
            int: The high score.
        """
        with open(self.high_score_file, "r") as f:
            high_score = int(f.read().strip())
            return high_score

    def save_high_score(self):
        """
        Saves the high score to the high score file.
        """
        with open(self.high_score_file, "w") as f:
            f.write(str(self.high_score))


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
            load_sprite("background_score", False), (850, 600)
        )
        self.font = pygame.font.Font("Pulang.ttf", 38)
        self.score_font = pygame.font.Font("Pulang.ttf", 38)
        self.game_over_font = pygame.font.Font("Pulang.ttf", 64)

    def draw(
        self, game_objects, score, high_score, color=(0, 0, 0), game_over=False
    ):
        """
        Draws the background and all active game objects to the screen.

        Args:
            game_objects (list): A list of game objects to be drawn.
        """
        self.screen.blit(self.background, (0, 0))
        for game_object in game_objects:
            game_object.draw()
        self.draw_score(score, color)
        self.draw_high_score(high_score, color)
        if game_over:
            self.draw_game_over(score)
        else:
            for game_object in game_objects:
                self.draw_object(game_object)
        pygame.display.update()

    def draw_score(self, score, color):
        """
        Draws the player's score on the screen.

        Args:
            score (int): The player's score.
        """
        score_text = self.font.render(f"Score: {score}", True, color)
        self.screen.blit(score_text, (40, 13))

    def draw_high_score(self, high_score, color):
        """
        Draws the player's high score on the screen.

        Args:
            high_score (int): The player's high score.
            color (tuple): The color of the text.
            position (tuple): The position of the text on the screen.
        """
        high_score_text = self.font.render(
            f"High Score: {high_score}", True, color
        )
        self.screen.blit(high_score_text, (300, 13))

    def draw_object(self, game_object):
        """
        Draws a game object on the screen.

        Args:
            game_object: An object in the game (fly/chameleon).
        """
        angle = game_object.direction.angle_to(UP)
        if isinstance(game_object, Chameleon):
            rotated_surface = rotozoom(game_object.sprite, angle, 1.0)
            rotated_surface_size = Vector2(rotated_surface.get_size())
            blit_position = game_object.position - rotated_surface_size * 0.5
            self.screen.blit(rotated_surface, blit_position)
            """
        else:
            rotated_surface = rotozoom(game_object.sprite, angle, 1.0)
            rotated_surface_size = Vector2(rotated_surface.get_size())
            blit_position = game_object.position - rotated_surface_size * 0.5
            self.screen.blit(rotated_surface, blit_position)"""

    def draw_game_over(self, score):
        """
        Draws the game over banner.

        Args:
            score (int): The player's score.
        """
        game_over_text = self.game_over_font.render(
            f"Game Over, Your score is {score}, to keep playing press enter.",
            True,
            (255, 0, 0),
        )
        game_over_text_rect = game_over_text.get_rect(
            center=(self.screen.get_width() // 2, self.screen.get_height() // 2)
        )
        self.screen.blit(game_over_text, game_over_text_rect)


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
        self.running = True
        self.show_instructions = True
        self._init_pygame()

    def _init_pygame(self):
        """
        Initializes Pygame and sets up the game window.
        """
        pygame.init()
        pygame.display.set_caption("Hungry Chameleon")
        self.screen = pygame.display.set_mode((860, 600))
        self.instructions_font = pygame.font.Font("Pulang.ttf", 28)
        self.instructions_text = [
            "Welcome to Hungry Chameleon!",
            "",
            "Instructions:",
            "Use LEFT and RIGHT arrow keys to rotate the chameleon.",
            "Press SPACE to catch flies with the chameleon's tongue.",
            "Avoid colliding with flies when chameleon's tongue is not out.",
            "Press ENTER to start the game.",
        ]

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
                self.running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                self.show_instructions = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.model.chameleon.rotate(clockwise=False)
        if keys[pygame.K_RIGHT]:
            self.model.chameleon.rotate(clockwise=True)
        if keys[pygame.K_SPACE]:
            self.model.chameleon.tongue = True
            self.model.chameleon.change_sprite()
        else:
            self.model.chameleon.tongue = False

    def display_instructions(self):
        # Fill screen with green background
        self.screen.fill((107, 142, 35))
        y_offset = 100
        for line in self.instructions_text:
            text_surface = self.instructions_font.render(line, True, (0, 0, 0))
            text_rect = text_surface.get_rect(center=(400, y_offset))
            self.screen.blit(text_surface, text_rect)
            y_offset += 40
        pygame.display.flip()

    def run(self):
        while self.running:
            self.handle_input()
            if self.show_instructions:
                self.display_instructions()
            else:
                self.game_loop()
        pygame.quit()

    def game_loop(self):
        while self.running:
            self.handle_input()
            self.model.update()
            self.view.draw(
                self.model.get_game_objects(),
                self.model.score,
                self.model.high_score,
            )
            self.clock.tick(60)
