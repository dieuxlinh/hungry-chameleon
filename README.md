# Softdes-2024 final project

An interactive game where user’s control the orientation of a chameleon trying to catch all the moving flies.  

## How to Use

1. Clone the project repository to your local machine.
```
git clone https://github.com/olincollege/softdes-hungry-chameleon-.git 
```
2. Navigate to the project directory:
```
cd hungry-chameleon
```
3. Install the required packages and libraries by running the following command:
```
pip install -r requirements.txt 
```


## Usage
Run the game by executing main.py:
```
python main.py
```

### Project Structure

    `main.py` Entry point for the application.
    `game.py` Contains the game logic following the MVC pattern.
    `models.py` Defines game objects like Chameleon and Fly.
    `utils.py` Helper functions for game operations.
    `test_game.py` Unit tests for the game.py module
    `test_utils.py` Unit tests for the utils.py module


### File Description 
    `main.py` Initializes Pygame, sets up the game model, view, and controller, and starts the game loop.
    `game.py` Managing game state, graphical output, and game loop.
    `models.py` Contains the game objects. 
    `utils.py`  Helper functions for sprite loading, position wrapping, and generating random positions and velocities.
    `test_game.py` Unit tests for the game.py module
    `test_utils.py` Unit tests for the utils.py module
