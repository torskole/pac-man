import pygame
from pygame.locals import (K_UP, K_DOWN, K_LEFT, K_RIGHT, K_w, K_s, K_a, K_d)
from utils import *

pygame.init()

WINDOW_WIDTH = WIDTH*BLOCKSIZE
WINDOW_HEIGHT = HEIGHT*BLOCKSIZE

surface = pygame.display.set_mode([WINDOW_WIDTH, WINDOW_HEIGHT])

clock = pygame.time.Clock()
maze = pygame.image.load("maze.png").convert_alpha()
maze = pygame.transform.scale(maze, (WINDOW_WIDTH, WINDOW_HEIGHT))

class Game:
    def __init__(self) -> None:
        self.current_score = 0
        self.current_level = 1
        self.coordinates = []
        for y in range(HEIGHT):
            self.coordinates.append([])
            for x in range(0, WIDTH):
                match read_character(x,y):
                    case "W":
                        self.coordinates[y].append({"type": False, "color": BLACK})
                    case "S":
                        self.coordinates[y].append({"type": None, "color":  YELLOW})
                    case "G":
                        self.coordinates[y].append({"type": None, "color":  BLUE})
                    case "B":
                        self.coordinates[y].append({"type": True, "color":  GREEN})
                    case _:
                        self.coordinates[y].append({"type": None, "color": WHITE})

    def render_grid(self):
        for y in range(0, len(self.coordinates)):
            for x in range (0, len(self.coordinates[y])):
                pygame.draw.rect(surface, self.coordinates[x][y]["color"], pygame.Rect(BLOCKSIZE*x, BLOCKSIZE*y, BLOCKSIZE, BLOCKSIZE), 10)

    def booster():
        return
    
    @staticmethod
    def coordinates_to_point(x,y) -> tuple[int]:
        return (x // BLOCKSIZE, y // BLOCKSIZE)

class MovingFigure:
    def __init__(self, game, x, y, sprite) -> None:
        self.game = game
        self.current_position = {"x": x, "y": y}
        self.new_position = {"x": 0, "y": 0}
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
        self.new_position["x"] = self.current_position["x"] + self.direction["x"]
        self.new_position["y"] = self.current_position["y"] + self.direction["y"]

        if self.direction["x"] != 0: # If moving along x-axis and going outside of the maze
            if self.new_position["x"] >= WIDTH:
                if game.coordinates[0][self.new_position["y"]]["type"] != False:
                    self.new_position["x"] = 0
                else:
                    self.direction["x"] = 0
                    return
            
            if self.new_position["x"] < 0:
                if game.coordinates[WIDTH-1][self.new_position["y"]]["type"] != False:
                    self.new_position["x"] = WIDTH-1
                else:
                    self.direction["x"] = 0
                    return
            
        if self.direction["y"] != 0: # If moving along y-axis and going outside of the maze
            if self.new_position["y"] >= HEIGHT:
                if game.coordinates[self.new_position["x"]][0]["type"] != False:
                    self.new_position["y"] = 0
                else:
                    self.direction["y"] = 0
                    return

            if self.new_position["y"] < 0:
                if game.coordinates[self.new_position["x"]][HEIGHT-1]["type"] != False:
                    self.new_position["y"] = HEIGHT-1
                else:
                    self.direction["y"] = 0
                    return
            
        if game.coordinates[self.new_position["x"]][self.new_position["y"]]["type"] == False: # If hitting a wall
            self.direction["x"] = 0
            self.direction["y"] = 0
            return

        if game.coordinates[self.new_position["x"]][self.new_position["y"]]["type"] == True:
            print("Booster")

        game.coordinates[self.current_position["x"]][self.current_position["y"]]["color"] = WHITE
        game.coordinates[self.new_position["x"]][self.new_position["y"]]["color"] = YELLOW

        self.current_position["x"] = self.new_position["x"]
        self.current_position["y"] = self.new_position["y"]

    def queue_movement(self, keys):
        if keys[K_UP] or keys[K_w]: # Upwards
            self.direction["y"] = -1
            self.direction["x"] = 0
        if keys[K_DOWN] or keys[K_s]: # Downwards
            self.direction["y"] = 1
            self.direction["x"] = 0
        if keys[K_LEFT] or keys[K_a]: # Left
            self.direction["x"] = -1
            self.direction["y"] = 0
        if keys[K_RIGHT] or keys[K_d]: # Right
            self.direction["x"] = 1
            self.direction["y"] = 0


active = True

game = Game()

active_pacman = Pacman(game, 0, 0, None)
frames = 0

if __name__ == "__main__":
    while active:
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    active = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        active = False

        keys = pygame.key.get_pressed()

        surface.fill(BLACK)
        active_pacman.queue_movement(keys)

        if frames % CHANGE_INTERVAL == 0:
            active_pacman.move()

        game.render_grid()
        pygame.display.flip()
        clock.tick(FPS)
        frames += 1

    pygame.quit()
