# Snake Game

## Introduction:
This is a classic Snake game implementation using Python's Pygame and Tkinter libraries. The game involves moving the snake around the board to eat the food while avoiding running into the walls or its own body. The snake grows longer with each food eaten, making it harder to avoid colliding with itself or the walls.

## Installation:
To run this game, you need to install Python 3 and the following libraries:

- Pygame
- Tkinter

You can install these libraries using pip:
```python
pip install pygame
pip install tkinter
```
## Usage:
To run the game, simply run the `'snake_game.py'` file in the terminal or Python IDE. The game will start running and the user can use arrow keys to move the snake in the desired direction. The objective is to eat the food and avoid hitting the walls or the snake's body.

## Features:
- The game has a GUI interface built using the Tkinter library.
- The snake moves around the game board using the arrow keys on the keyboard.
- The snake grows in length each time it eats food.
- The game ends if the snake hits the wall or its own body.
- The game keeps track of the player's high score.
- The game can be reset to start over.
## Code:
The code is structured using two classes: `Cube` and `Snake`. `Cube` represents a single block on the game board and `Snake` is responsible for handling the snake's movement and interactions with the board. The game logic is written in the `'snake_game.py'` file.

## Contributing:
Contributions are welcome! If you have any suggestions or improvements, please create a [pull request]() on [GitHub]().

## License:
This game is licensed under the MIT License. See the [LICENSE]() file for details.