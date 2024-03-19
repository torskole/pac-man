import pygame
from pygame.locals import (K_UP, K_DOWN, K_LEFT, K_RIGHT, K_w, K_s, K_a, K_d)
from utils import *
import random

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
        self.requested_coordinates = []
        for y in range(HEIGHT):
            self.coordinates.append([])
            for x in range(0, WIDTH):
                match read_character(x,y):
                    case "W":
                        self.coordinates[y].append({"type": False, "color": BLACK})
                    case "S":
                        self.coordinates[y].append({"type": "Spawnpoint", "color":  YELLOW})
                    case "G":
                        self.coordinates[y].append({"type": "Guard", "color":  BLUE})
                    case "B":
                        self.coordinates[y].append({"type": True, "color":  GREEN})
                    case _:
                        self.coordinates[y].append({"type": None, "color": WHITE})

    def render_grid(self):
        for y in range(0, len(self.coordinates)):
            for x in range (0, len(self.coordinates[y])):
                pygame.draw.rect(surface, self.coordinates[x][y]["color"], pygame.Rect(BLOCKSIZE*x, BLOCKSIZE*y, BLOCKSIZE, BLOCKSIZE), 10)

    def find_type(self, type):
        type_coordinates = []
        for y in range(0, len(self.coordinates)):
            for x in range (0, len(self.coordinates[y])):
                if self.coordinates[x][y]["type"] == type:
                    type_coordinates.append([x, y])
        return type_coordinates
    
    def check_available_position(self, x, y):
        try:
            if self.coordinates[x][y]["type"] == False:
                return False
            return True
        except:
            print("Checked for non-existent wall")
    
    def pick_spawnpoint(self):
        spawnpoints = self.find_type("Spawnpoint")
        spawnpoint = random.choice(spawnpoints)
        return spawnpoint

    def clear_references(self, type):
        points = self.find_type(type)
        for point in points:
            self.coordinates[point[0]][point[1]]["type"] = None
            self.coordinates[point[0]][point[1]]["color"] = WHITE

    def booster():
        return

class MovingFigure:
    def __init__(self, game, x, y, sprite) -> None:
        self.game = game
        self.current_position = {"x": x, "y": y}
        self.new_position = {"x": 0, "y": 0}
        self.direction = {"x": 0, "y": 0}
        self.sprite = sprite

    def create_new_postions(self, direction):
        return self.current_position["x"] + direction["x"], self.current_position["y"] + direction["y"]

    def request_move(self):
        self.new_position["x"], self.new_position["y"] = self.create_new_postions({"x": self.direction["x"], "y": self.direction["y"]})
        # self.new_position["x"] = self.current_position["x"] + self.direction["x"]
        # self.new_position["y"] = self.current_position["y"] + self.direction["y"]

        if self.direction["x"] != 0: # If moving along x-axis and going outside of the maze
            if self.new_position["x"] >= WIDTH:
                if self.game.check_available_position(0, self.new_position["y"]):
                # if game.coordinates[0][self.new_position["y"]]["type"] != False:
                    self.new_position["x"] = 0
                else:
                    self.direction["x"] = 0
                    return False
            
            if self.new_position["x"] < 0:
                # if game.coordinates[WIDTH-1][self.new_position["y"]]["type"] != False:
                if self.game.check_available_position(WIDTH-1, self.new_position["y"]):
                    self.new_position["x"] = WIDTH-1
                else:
                    self.direction["x"] = 0
                    return False
            
        if self.direction["y"] != 0: # If moving along y-axis and going outside of the maze
        #     if game.coordinates[self.current_position["x"]+1][self.current_position["y"]]["type"] == False:

            if self.new_position["y"] >= HEIGHT:
                # if game.coordinates[self.new_position["x"]][0]["type"] != False:
                if self.game.check_available_position(self.new_position["x"], 0):
                    self.new_position["y"] = 0
                else:
                    self.direction["y"] = 0
                    return False

            if self.new_position["y"] < 0:
                # if game.coordinates[self.new_position["x"]][HEIGHT-1]["type"] != False:
                if self.game.check_available_position(self.new_position["x"], HEIGHT-1):
                    self.new_position["y"] = HEIGHT-1
                else:
                    self.direction["y"] = 0
                    return False
            
        # if game.coordinates[self.new_position["x"]][self.new_position["y"]]["type"] != None: # If hitting a wall
        if not self.game.check_available_position(self.new_position["x"], self.new_position["y"]):
            self.direction["x"] = 0
            self.direction["y"] = 0
            return False

        return True

class Guard(MovingFigure):
    def __init__(self, game, x, y, sprite) -> None:
        super().__init__(game, x, y, sprite)

    def request_move(self):
        available_directions = [self.direction]

        if self.direction["x"] != 0:
            new_position1 = self.create_new_postions({"x": 0, "y": -1})
            new_position2 = self.create_new_postions({"x": 0, "y": 1})

        if self.direction["y"] != 0:
            new_position1 = self.create_new_postions({"x": -1, "y": 0})
            new_position2 = self.create_new_postions({"x": 1, "y": 0})
        
        if self.game.check_available_position(new_position1[0], new_position1[1]):
            if self.direction["y"] != 0:
                new_direction = {"x": (new_position1[0] - self.current_position["x"]), "y": 0}
                available_directions.append(new_direction)
            if self.direction["x"] != 0:
                new_direction = {"x": 0, "y": (new_position1[1] - self.current_position["y"])}
                available_directions.append(new_direction)
                
        if self.game.check_available_position(new_position2[0], new_position2[1]):
            #print(new_position2[0], new_position2[1])
            if self.direction["y"] != 0:
                new_direction = {"x": (new_position2[0] - self.current_position["x"]), "y": 0}
                #print(new_direction, new_position2[0], self.current_position["x"])
                available_directions.append(new_direction)
            if self.direction["x"] != 0:
                new_direction = {"x": 0, "y": (new_position2[1] - self.current_position["y"])}
                #print(new_direction)
                available_directions.append(new_direction)

        if available_directions != []:
            new_direction = random.choice(available_directions)
            #print(self.direction, new_direction)
            self.direction["x"] = new_direction["x"] 
            self.direction["y"] = new_direction["y"]

        return super().request_move()

    def move(self):
        if self.direction["x"] == 0 and self.direction["y"] == 0:
            axis, _ = random.choice(list(self.direction.items()))
            random_direction = random.choice([-1, 1])
            self.direction[axis] = random_direction

        if self.request_move():
            game.coordinates[self.current_position["x"]][self.current_position["y"]]["color"] = WHITE
            game.coordinates[self.new_position["x"]][self.new_position["y"]]["color"] = BLUE

            self.current_position["x"] = self.new_position["x"]
            self.current_position["y"] = self.new_position["y"]


class Pacman(MovingFigure):
    def __init__(self, game, x, y, sprite) -> None:
        super().__init__(game, x, y, sprite)
        self.health = 2
        
    def move(self):
        if self.request_move():
            if game.coordinates[self.new_position["x"]][self.new_position["y"]]["type"] == True:
                print(game.find_type(True))

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
spawnpoint = game.pick_spawnpoint()

active_pacman = Pacman(game, spawnpoint[0], spawnpoint[1], None)
guards = []
frames = 0


for guard in game.find_type("Guard"):
    guards.append(Guard(game, guard[0], guard[1], None))

game.clear_references("Guard")
game.clear_references("Spawnpoint")

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
            for guard in guards:
                guard.move()

            for guard in guards:
                if (active_pacman.current_position["x"] == guard.current_position["x"] and
                        active_pacman.current_position["y"] == guard.current_position["y"]):
                    print("Pacman collided with a guard!")

            for ghost_number in range(len(guards)):
                for compared_ghost_number in range(ghost_number + 1 , len(guards)):
                    original_ghost = guards[ghost_number]
                    compared_ghost = guards[compared_ghost_number]
                    if (original_ghost.current_position["x"] == compared_ghost.current_position["x"] and
                            original_ghost.current_position["y"] == compared_ghost.current_position["y"]):
                        guard.direction["x"] *= -1; guard.direction["y"] *= -1

        game.render_grid()
        pygame.display.flip()
        clock.tick(FPS)
        frames += 1

    pygame.quit()
