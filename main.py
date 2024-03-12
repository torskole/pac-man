import pygame
from pygame.locals import (K_UP, K_DOWN, K_LEFT, K_RIGHT, K_w, K_s, K_a, K_d)
from config import *

pygame.init()

width = 25
height = 25
blocksize = 25

WINDOW_WIDTH = width*blocksize
WINDOW_HEIGHT = height*blocksize

surface = pygame.display.set_mode([WINDOW_WIDTH, WINDOW_HEIGHT])

clock = pygame.time.Clock()
maze = pygame.image.load("maze.png").convert_alpha()
maze = pygame.transform.scale(maze, (WINDOW_WIDTH, WINDOW_HEIGHT))

class Game:
    def __init__(self) -> None:
        self.current_score = 0
        self.current_level = 1
        self.coordinates = []
        for column in range(width):
            self.coordinates.append([])
            for _ in range(0, height):
                self.coordinates[column].append({"type": None, "color": WHITE})

    def render_grid(self):
        for x in range(0, len(self.coordinates)):
            for y in range (0, len(self.coordinates[x])):
                pygame.draw.rect(surface, self.coordinates[x][y]["color"], pygame.Rect(blocksize*x, blocksize*y, blocksize, blocksize), 10)

class MovingFigure:
    def __init__(self, game, x, y, sprite) -> None:
        self.game = game
        self.current_position = {"x": x, "y": y}
        self.new_position = [0, 0]
        self.direction = {"x": 0, "y": 0}
        self.sprite = sprite

class Ghost(MovingFigure):
    def __init__(self, game, x, y, sprite) -> None:
        super().__init__(game, x, y, sprite)

class Pacman(MovingFigure):
    def __init__(self, game, x, y, sprite) -> None:
        super().__init__(game, x, y, sprite)
        self.health = 2
        
    def move(self):
        if self.direction["y"] == 1:
            self.new_position[1] = self.current_position["y"] - 1
        elif self.direction["y"] == -1:
            self.new_position[1] = self.current_position["y"] + 1
        if self.direction["x"] == 1:
            self.new_position[0] = self.current_position["x"] + 1
        elif self.direction["x"] == -1:
            self.new_position[0] = self.current_position["x"] - 1

        if self.current_position == self.new_position:
            print(True)
        else:
            print(False)
        #print(self.current_position, self.new_position)

        game.coordinates[self.current_position["x"]][self.current_position["y"]]["color"] = WHITE
        game.coordinates[self.new_position[0]][self.new_position[1]]["color"] = YELLOW

        self.current_position["x"] = self.new_position[0]
        self.current_position["y"] = self.new_position[1]

        self.direction["x"] = 0
        self.direction["y"] = 0

    def queue_movement(self, keys):
        if keys[K_UP] or keys[K_w]: # Upwards
            self.direction["y"] = 1
        if keys[K_DOWN] or keys[K_s]: # Downwards
            self.direction["y"] = -1
        if keys[K_LEFT] or keys[K_a]: # Left
            self.direction["x"] = -1
        if keys[K_RIGHT] or keys[K_d]: # Right
            self.direction["x"] = 1


active = True

game = Game()

active_pacman = Pacman(game, 0, 0, None)
frames = 0

while active:
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                active = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    active = False
            elif event.type == pygame.MOUSEBUTTONUP:
                position = pygame.mouse.get_pos()
                print("Debug: ", surface.get_at(position))

    keys = pygame.key.get_pressed()

    surface.fill(BLACK)
    #surface.blit(maze, (0, 0))
    active_pacman.queue_movement(keys)

    if frames % CHANGE_INTERVAL == 0:
        active_pacman.move()

    game.render_grid()
    pygame.display.flip()
    clock.tick(FPS)
    frames += 1

pygame.quit()
