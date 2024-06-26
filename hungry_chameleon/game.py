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
        high_score_file (str): The path of the txt file holding the user's high
        score
        high_score (int): The user's high score
        font (pygame.font): The font used to display text
        tongue_time (int): Stores how long the chameleon has had the tongue out
        game_over (bool): Stores whether the game is active or not
    """

    MIN_FLY_DISTANCE = 250

    def __init__(self, screen):
        """
        Initializes the game model with a display surface.

        Args:
            screen (pygame.Surface): The display surface.
        """
        self.screen = screen
        self.chameleon = Chameleon((400, 300), (400, 300), self.screen)
        self.fly = self._init_flies(6)
        self.score = 0
        self.high_score_file = "HIGH_SCORE_FILE.txt"
        self.high_score = self.load_high_score()
        self.font = pygame.font.Font("assets/fonts/Pulang.ttf", 40)
        self.tongue_time = 0
        self.game_over = False

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
                    self.game_over = True
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

    def check_game_over(self):
        """
        Checks if game is over

        Returns:
            game_over (bool): True if game is over, false otherwise
        """
        return self.game_over


# View
class GameView:
    """
    Represents the visual aspect of the game, rendering all visual
    elements on the screen.

    Attributes:
        screen (pygame.Surface): The display surface for drawing the game.
        background (pygame.Surface): The background image of the game scene.
        font (pygame.font): The font used in the game
        score_font (pygame.font): The font used in the game to display score
        game_over_font (pygame.font): The font used in the game to display game
        over message
        overlay_color (tuple): Holds the background color for instructions page


    """

    def __init__(self, screen):
        """
        Initializes the game view with a display surface.

        Args:
            screen (pygame.Surface): The display surface.
        """
        self.screen = screen
        self.background = pygame.transform.scale(
            load_sprite("background_score", False), (860, 600)
        )
        self.font = pygame.font.Font("assets/fonts/Pulang.ttf", 38)
        self.score_font = pygame.font.Font("assets/fonts/Pulang.ttf", 38)
        self.game_over_font = pygame.font.Font("assets/fonts/Pulang.ttf", 32)
        self.overlay_color = (0, 0, 0, 128)

    def draw(
        self, game_objects, score, high_score, color=(0, 0, 0), game_over=False
    ):
        """
        Draws the background and all active game objects to the screen.

        Args:
            game_objects (list): A list of game objects to be drawn.
            score (int): The player's score
            high_score (int): The user's high score
            color (tuple):  The color black
            game_over (bool): Used to determine if the game is over or not.
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
            color (tuple):  The color ir the text.

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

    def draw_game_over(self, score):
        """
        Draws the game over banner.

        Args:
            score (int): The player's score.
        """
        # Draw semi-transparent overlay
        overlay = pygame.Surface(
            (self.screen.get_width(), self.screen.get_height())
        )
        overlay.fill(self.overlay_color)
        self.screen.blit(overlay, (0, 0))

        # Draw game over text and display score
        game_over_text_line1 = self.game_over_font.render(
            f"Game Over, Your score is {score}.",
            True,
            (255, 0, 0),
        )
        game_over_text_line2 = self.game_over_font.render(
            "Press Enter to restart.",
            True,
            (255, 0, 0),
        )
        game_over_text_rect_line1 = game_over_text_line1.get_rect(
            center=(
                self.screen.get_width() // 2,
                self.screen.get_height() // 2 - 20,
            )
        )
        game_over_text_rect_line2 = game_over_text_line2.get_rect(
            center=(
                self.screen.get_width() // 2,
                self.screen.get_height() // 2 + 20,
            )
        )
        self.screen.blit(game_over_text_line1, game_over_text_rect_line1)
        self.screen.blit(game_over_text_line2, game_over_text_rect_line2)
        pygame.display.flip()


# Controller
class GameController:
    """
    Controls the game flow, handling game events and updates.

    Attributes:
        model (GameModel): The game's model managing the state.
        view (GameView): The game's view handling rendering.
        clock (pygame.time.Clock): Clock for managing the game's frame rate.
        running (bool): checks to see if the game loop is running
        show_instructions (bool): checks whether we are on initial screen
        game_over (bool): checks whether the game is on or over
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
        self.game_over = False
        self._init_pygame()

    def _init_pygame(self):
        """
        Initializes Pygame and sets up the game window.
        """
        pygame.init()
        pygame.display.set_caption("Hungry Chameleon")
        self.screen = pygame.display.set_mode((860, 600))
        self.instructions_font = pygame.font.Font("assets/fonts/Pulang.ttf", 26)
        self.instructions_message_font = pygame.font.Font(
            "assets/fonts/Pulang.ttf", 20
        )
        self.instructions_text = [
            "Welcome to Hungry Chameleon!",
            "",
            "Instructions:",
            "Use LEFT and RIGHT arrow keys to rotate the chameleon.",
            "Press SPACE to catch flies with the chameleon's tongue.",
            "Avoid colliding with flies when chameleon's tongue is not out.",
            "Press ENTER to start the game.",
            "Press ESC at anytime to quit the game.",
        ]
        self.instructions_message = "P.S. Some flies are tougher than others and may need more than 1 attack"

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
                if self.show_instructions:
                    self.show_instructions = False
                elif self.game_over:
                    self.model = GameModel(self.screen)
                    self.game_over = False

        if self.model.chameleon:
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
        """
        Displays the instructions of the game before playing
        """
        # Fill screen with green background
        self.screen.fill((107, 142, 35))
        y_offset = (
            self.screen.get_height() - (len(self.instructions_text) + 2) * 40
        ) // 2
        for line in self.instructions_text:
            text_surface = self.instructions_font.render(line, True, (0, 0, 0))
            text_rect = text_surface.get_rect(
                center=(self.screen.get_width() // 2, y_offset)
            )
            self.screen.blit(text_surface, text_rect)
            y_offset += 40
        instructions_message_surface = self.instructions_message_font.render(
            self.instructions_message, True, (0, 0, 0)
        )
        instructions_message_rect = instructions_message_surface.get_rect(
            center=(self.screen.get_width() // 2, y_offset + 20)
        )
        self.screen.blit(
            instructions_message_surface, instructions_message_rect
        )
        pygame.display.flip()

    def handle_game_over_input(self):
        """
        Handles user input when the game is over.

        Returns:
            bool: True if the game should restart, False otherwise.
        """
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                return True
            if event.type == pygame.QUIT:
                self.running = False
                return False
        return False

    def run(self):
        """
        Initial running game loop, used to remove instructions when enter is
        pressed.
        """
        while self.running:
            self.handle_input()
            if self.show_instructions:
                self.display_instructions()
            else:
                self.game_loop()
        pygame.quit()

    def game_loop(self):
        """
        Game loop. Calls appropriate functions to make the game and input work
        correctly.
        """
        while self.running:
            if self.model.chameleon is None:
                self.game_over = True
            self.handle_input()
            self.model.update()
            self.view.draw(
                self.model.get_game_objects(),
                self.model.score,
                self.model.high_score,
                game_over=self.game_over,
            )
            if self.game_over:
                if self.handle_game_over_input():
                    self.model = GameModel(self.screen)
                    self.game_over = False
            self.clock.tick(60)
