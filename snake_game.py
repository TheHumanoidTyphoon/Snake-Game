import random
import sys
import tkinter as tk
from tkinter import messagebox

import pygame
from pygame import mixer

class Cube:
    NUM_ROWS = 20
    BOARD_WIDTH = 500

    def __init__(self, position, color=(240, 120, 7)):
        """
        A Cube object that represents a single block in the game.
        
        Args:
        
            position (tuple): The position of the cube on the game board.
            color (tuple): The color of the cube.
        """
        self.position = position
        self.direction_x, self.direction_y = 1, 0
        self.color = color

    def move(self, direction_x, direction_y):
        """
        Move the cube in the given direction.
        
        Args:
            direction_x (int): The x-direction to move in.
            direction_y (int): The y-direction to move in.
        """
        self.direction_x, self.direction_y = direction_x, direction_y
        self.position = (self.position[0] + direction_x, self.position[1] + direction_y)

    def draw(self, surface, has_eyes=False):
        """
        Draw the cube on the game board.
        
        Args:
            surface (pygame.Surface): The surface to draw on.
            has_eyes (bool): Whether to draw the eyes on the cube.
        """
        square_size = self.BOARD_WIDTH // self.NUM_ROWS
        i, j = self.position
        rect = pygame.Rect(i * square_size + 1, j * square_size + 1, square_size - 2, square_size - 2)
        pygame.draw.rect(surface, self.color, rect)
        if has_eyes:
            centre = square_size // 2
            radius = 3
            circle1 = (i * square_size + centre - radius, j * square_size + 8)
            circle2 = (i * square_size + square_size - radius * 2, j * square_size + 8)
            pygame.draw.circle(surface, (0, 0, 0), circle1, radius)
            pygame.draw.circle(surface, (0, 0, 0), circle2, radius)



class Snake:
    def __init__(self, color, position):
        """
        Initializes the Snake object with a given color and position.

        Parameters:
        - color (tuple): RGB tuple representing the color of the snake.
        - position (tuple): Tuple representing the initial position of the snake.

        Returns:
        - None
        """
        self.color = color
        self.body = [Cube(position)]
        self.direction_x, self.direction_y = 0, 1
        self.turns = {}

    def move(self):
        """
        Moves the snake in the current direction and handles user input.

        Parameters:
        - None

        Returns:
        - None
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        self.direction_x, self.direction_y = self.turns.get(
            self.body[0].position, (self.direction_x, self.direction_y))

        if keys[pygame.K_LEFT]:
            self.turns[self.body[0].position] = (-1, 0)
        elif keys[pygame.K_RIGHT]:
            self.turns[self.body[0].position] = (1, 0)
        elif keys[pygame.K_UP]:
            self.turns[self.body[0].position] = (0, -1)
        elif keys[pygame.K_DOWN]:
            self.turns[self.body[0].position] = (0, 1)

        for i, cube in enumerate(self.body):
            current_position = cube.position[:]
            if current_position in self.turns:
                cube.move(*self.turns[current_position])
                if i == len(self.body) - 1:
                    self.turns.pop(current_position)
            else:
                if cube.direction_x == -1 and cube.position[0] <= 0:
                    cube.position = (cube.NUM_ROWS-1, cube.position[1])
                elif cube.direction_x == 1 and cube.position[0] >= cube.NUM_ROWS-1:
                    cube.position = (0, cube.position[1])
                elif cube.direction_y == 1 and cube.position[1] >= cube.NUM_ROWS-1:
                    cube.position = (cube.position[0], 0)
                elif cube.direction_y == -1 and cube.position[1] <= 0:
                    cube.position = (cube.position[0], cube.NUM_ROWS-1)
                else:
                    cube.move(cube.direction_x, cube.direction_y)

    def reset(self, position):
        """
        Resets the snake to its initial state with a new position.

        Parameters:
        - position (tuple): Tuple representing the new position of the snake.

        Returns:
        - None
        """
        self.head = Cube(position)
        self.body = []
        self.body.append(self.head)
        self.turns = {}
        self.direction_x = 0
        self.direction_y = 1

    def add_cube(self):
        """
        Adds a new cube to the end of the snake.

        Parameters:
        - None

        Returns:
        - None
        """
        tail = self.body[-1]
        move_x, move_y = tail.direction_x, tail.direction_y

        if move_x == 1 and move_y == 0:
            self.body.append(Cube((tail.position[0]-1, tail.position[1])))
        elif move_x == -1 and move_y == 0:
            self.body.append(Cube((tail.position[0]+1, tail.position[1])))
        elif move_x == 0 and move_y == 1:
            self.body.append(Cube((tail.position[0], tail.position[1]-1)))
        elif move_x == 0 and move_y == -1:
            self.body.append(Cube((tail.position[0], tail.position[1]+1)))

        self.body[-1].direction_x = move_x
        self.body[-1].direction_y = move_y

    def draw(self, surface):
        """
        Draws the snake on the given surface.

        Args:
            surface: A Pygame surface object on which to draw the snake.

        Returns:
            None.
        """
        for i, body_segment in enumerate(self.body):
            if i == 0:
                body_segment.draw(surface, True)
            else:
                body_segment.draw(surface)


def draw_grid(surface_width, rows, surface):
    """
    Draw a grid on the game surface.

    Parameters:
    surface_width (int): The width of the game surface.
    rows (int): The number of rows in the game grid.
    surface: The game surface to draw the grid on.
    """
    cell_size = surface_width // rows

    coord_x = 0
    coord_y = 0
    for row_num in range(rows):
        coord_x = coord_x + cell_size
        coord_y = coord_y + cell_size

        pygame.draw.line(surface, (255, 255, 255), (coord_x, 0), (coord_x, surface_width))
        pygame.draw.line(surface, (255, 255, 255), (0, coord_y), (surface_width, coord_y))

def redraw_window(surface, score, level):
    """
    Redraw the game window.

    Parameters:
    surface: The game surface to redraw.
    score (int): The current score of the game.
    level (int): The current level of the game.
    """
    global rows, width, snake, snack
    surface.fill((0, 0, 0))
    # Change background color based on snake length
    if len(snake.body) < 10:
        bg_color = (0, 0, 0)
    elif len(snake.body) < 20:
        bg_color = (0, 0, 255)
    else:
        bg_color = (255, 0, 0)
    surface.fill(bg_color)

    # Change snack color based on snake length
    if len(snake.body) < 10:
        snack.color = (45, 235, 240)
    elif len(snake.body) < 20:
        snack.color = (0, 255, 0)  # change to green
    else:
        snack.color = (255, 255, 0)  # change to yellow
    snack.color = snack.color

    draw_grid(width, rows, surface)
    snake.draw(surface)
    snack.draw(surface)

    # Create score and level text objects
    font = pygame.font.SysFont('comisans', 25)
    score_text = font.render('Score: ' + str(score), True, (255, 255, 255))
    level_text = font.render('Level: ' + str(level), True, (255, 255, 255))

    # Blit the text objects onto the surface
    surface.blit(score_text, (10, 10))
    surface.blit(level_text, (width - level_text.get_width() - 10, 10))

    pygame.display.update()


def random_snack(rows, snake):
    """
    Generate a random snack for the snake.

    Parameters:
    rows (int): The number of rows in the game grid.
    snake: The snake object.

    Returns:
    tuple: The x and y coordinates of the random snack.
    """
    snake_body = snake.body

    while True:
        snack_x = random.randrange(rows)
        snack_y = random.randrange(rows)
        if len(list(filter(lambda position_z: position_z.position == (snack_x, snack_y), snake_body))) > 0:
            continue
        else:
            break

    return (snack_x, snack_y)


def message_box(subject, content):
    """
    Display a message box with a yes or no question.

    Parameters:
    subject (str): The title of the message box.
    content (str): The message to display in the message box.

    Returns:
    bool: True if the player clicked "yes", False if the player clicked "no".
    """
    root = tk.Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    answer = messagebox.askyesno(subject, content)  # save the return value
    try:
        root.destroy()
    except:
        pass

    if answer:  # if the player clicked "yes"
        snake.reset((10, 10))
    else:  # if the player clicked "no"
        flag = False  # set flag to False to exit the game loop
        pygame.quit()  # quit the game


def main():
    """
    The main function for running the game.
    """
    global width, rows, snake, snack
    width = 500
    rows = 20
    score = 0
    level = 0

    window = pygame.display.set_mode((width, width), score, level)

    # Title and Icon
    pygame.display.set_caption("Snake Game")
    icon = pygame.image.load("Images\creature_snake_1_orange-_1_.ico")
    pygame.display.set_icon(icon)

    snake = Snake((255, 0, 0), (10, 10))
    snack = Cube(random_snack(rows, snake), color=(45, 235, 240))
    flag = True

    clock = pygame.time.Clock()
    cube_count = 0

    while flag:
        pygame.time.delay(50)
        clock.tick(10)
        snake.move()
        if snake.body[0].position == snack.position:
            snake.add_cube()
            snack = Cube(random_snack(rows, snake), color=(45, 235, 240))
            cube_count += 1

            pygame.mixer.init()
            add_cube_sound = mixer.Sound("Sounds/food_G1U6tlb.wav")
            add_cube_sound.play()

        for body_index in range(len(snake.body)):
            if snake.body[body_index].position in list(map(lambda position_z: position_z.position, snake.body[body_index+1:])):
                pygame.mixer.init()
                add_cube_sound = mixer.Sound("Sounds/game_over_sound.wav")
                add_cube_sound.play()

                answer = messagebox.askyesno('You Lost!', 'Play Again...')
                if answer:  # if the player clicked "yes"
                    snake.reset((10, 10))
                else:  # if the player clicked "no"
                    flag = False  # set flag to False to exit the game loop
                    pygame.quit()  # quit the game
                break

        if cube_count == 9:
            level += 1
            cube_count = 0

        score = len(snake.body)
        redraw_window(window, score=score, level=level)


def main_menu(window):
    """
    The main menu for the game.

    Parameters:
    window: The game surface.

    Returns:
    None
    """
    run = True
    while run:
        window.fill((0, 0, 0))

        # Title and Icon
        pygame.display.set_caption("Snake Game")
        icon = pygame.image.load("Images\creature_snake_1_orange-_1_.ico")
        pygame.display.set_icon(icon)

        # Set up the font
        pygame.font.init()
        play_font = pygame.font.SysFont("comicsans", 30)
        title_font = pygame.font.SysFont("comicsans", 70)

        # Create the text surfaces
        title = title_font.render("Snake", True, (255, 255, 255))
        title_rect = title.get_rect(center=(width//2, width//2 - 60))

        play_text = play_font.render("Press any key to play", True, (255, 255, 255))
        play_text_rect = play_text.get_rect(center=(width//2, width//2 + 60))

        # Draw the text surfaces onto the screen
        window.blit(title, title_rect)
        window.blit(play_text, play_text_rect)

        # Update the display
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                main()

    pygame.display.quit()


width = 500
window = pygame.display.set_mode((width, width))
main_menu(window)


