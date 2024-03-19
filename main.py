import pygame
from pygame.locals import (K_UP, K_DOWN, K_LEFT, K_RIGHT, K_w, K_s, K_a, K_d)
from utils import *
import random

pygame.init()

WINDOW_WIDTH = WIDTH*BLOCKSIZE
WINDOW_HEIGHT = HEIGHT*BLOCKSIZE

surface = pygame.display.set_mode([WINDOW_WIDTH, WINDOW_HEIGHT])
clock = pygame.time.Clock()
sprites = [[Sprite.FUGITIVE, True], [Sprite.GUARD, True], [Sprite.BOOST, False]] # Sprite, variants: true|false

class Game:
    def __init__(self) -> None:
        self.current_score = 0
        self.current_level = 1
        self.scared_guards = False
        self.coordinates = []
        self.boosts = []
        self.guards = []
        self.preloaded_images = {}

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
                        self.coordinates[y].append({"type": "Boost", "color":  GREEN})
                    case _:
                        self.coordinates[y].append({"type": None, "color": BACKGROUND_COLOR})
        
    def load_image(self, key):
        if not key in self.preloaded_images:
            self.preloaded_images[key] = pygame.image.load(f"./sprites/{key}.png").convert_alpha()
        return self.preloaded_images[key]

    def render_grid(self):
        for y in range(0, len(self.coordinates)):
            for x in range (0, len(self.coordinates[y])):
                cell_rect = pygame.Rect(BLOCKSIZE * x, BLOCKSIZE * y, BLOCKSIZE, BLOCKSIZE)
                match self.coordinates[x][y]["type"]:
                    case None:
                        pygame.draw.rect(surface, self.coordinates[x][y]["color"], cell_rect, 10)
                    case False:
                        pygame.draw.rect(surface, self.coordinates[x][y]["color"], cell_rect, 10)
                    case _:
                        sprite_number = self.coordinates[x][y]["type"]
                        image = self.load_image(sprite_number)

                        pygame.draw.rect(surface, BACKGROUND_COLOR, cell_rect, 10)
                        image_width, image_height = image.get_size()
                        max_size = min(BLOCKSIZE, BLOCKSIZE)
                        if image_width > image_height:
                            scaled_width = max_size
                            scaled_height = int(image_height * (max_size / image_width))
                        else:
                            scaled_height = max_size
                            scaled_width = int(image_width * (max_size / image_height))

                        image = pygame.transform.scale(image, (scaled_width, scaled_height))
                        surface.blit(image, (cell_rect.centerx - scaled_width // 2, cell_rect.centery - scaled_height // 2))

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

class MovingFigure:
    def __init__(self, game, x, y, sprite) -> None:
        self.game = game
        self.current_position = {"x": x, "y": y}
        self.new_position = {"x": 0, "y": 0}
        self.direction = {"x": 0, "y": 0}
        self.sprite = sprite
        self.sprite_status = self.sprite.value + Sprite.DOWN.value

    def update_sprite(self):
        match self.direction:
            case {"x": 0, "y": 0}:
                self.sprite_status = self.sprite.value  + Sprite.IDLE.value
            case {"x": -1, "y": _}:
                self.sprite_status = self.sprite.value  + Sprite.LEFT.value
            case {"x": 1, "y": _}:
                self.sprite_status = self.sprite.value  + Sprite.RIGHT.value
            case {"x": _, "y": -1}:
                self.sprite_status = self.sprite.value  + Sprite.UP.value
            case {"x": _, "y": 1}:
                self.sprite_status = self.sprite.value  + Sprite.DOWN.value


    def create_new_postions(self, direction):
        return self.current_position["x"] + direction["x"], self.current_position["y"] + direction["y"]
    
    def move(self):
        self.update_sprite()

    def request_move(self):
        self.new_position["x"], self.new_position["y"] = self.create_new_postions({"x": self.direction["x"], "y": self.direction["y"]})

        if self.direction["x"] != 0: # If moving along x-axis and going outside of the maze
            if self.new_position["x"] >= WIDTH:
                if self.game.check_available_position(0, self.new_position["y"]):
                    self.new_position["x"] = 0
                else:
                    self.direction["x"] = 0
                    return False
            
            if self.new_position["x"] < 0:
                if self.game.check_available_position(WIDTH-1, self.new_position["y"]):
                    self.new_position["x"] = WIDTH-1
                else:
                    self.direction["x"] = 0
                    return False
            
        if self.direction["y"] != 0: # If moving along y-axis and going outside of the maze
            if self.new_position["y"] >= HEIGHT:
                if self.game.check_available_position(self.new_position["x"], 0):
                    self.new_position["y"] = 0
                else:
                    self.direction["y"] = 0
                    return False

            if self.new_position["y"] < 0:
                if self.game.check_available_position(self.new_position["x"], HEIGHT-1):
                    self.new_position["y"] = HEIGHT-1
                else:
                    self.direction["y"] = 0
                    return False
                
        if not self.game.check_available_position(self.new_position["x"], self.new_position["y"]): # If hitting a wall
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
            if self.direction["y"] != 0:
                new_direction = {"x": (new_position2[0] - self.current_position["x"]), "y": 0}
                available_directions.append(new_direction)
            if self.direction["x"] != 0:
                new_direction = {"x": 0, "y": (new_position2[1] - self.current_position["y"])}
                available_directions.append(new_direction)

        if available_directions != []:
            new_direction = random.choice(available_directions)
            self.direction["x"] = new_direction["x"] 
            self.direction["y"] = new_direction["y"]

        return super().request_move()

    def move(self):
        if self.direction["x"] == 0 and self.direction["y"] == 0:
            axis, _ = random.choice(list(self.direction.items()))
            random_direction = random.choice([-1, 1])   
            self.direction[axis] = random_direction

        if self.request_move():
            self.game.coordinates[self.current_position["x"]][self.current_position["y"]]["type"] = None # Ensures previous type stays
            self.game.coordinates[self.new_position["x"]][self.new_position["y"]]["type"] = self.sprite_status

            self.current_position["x"] = self.new_position["x"]
            self.current_position["y"] = self.new_position["y"]
        return super().move()

class Player(MovingFigure):
    def __init__(self, game, x, y, sprite) -> None:
        super().__init__(game, x, y, sprite)
        self.health = 2
        
    def move(self):
        if self.request_move():
            if ([self.new_position["x"], self.new_position["y"]]) in game.boosts: # If on a boost
                game.boosts.pop(game.boosts.index([self.new_position["x"], self.new_position["y"]]))
                game.scared_guards = True

            self.game.coordinates[self.current_position["x"]][self.current_position["y"]]["type"] = None
            self.game.coordinates[self.new_position["x"]][self.new_position["y"]]["type"] = self.sprite_status

            self.current_position["x"] = self.new_position["x"]
            self.current_position["y"] = self.new_position["y"]
        return super().move()

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

active_player = Player(game, spawnpoint[0], spawnpoint[1], Sprite.FUGITIVE)
frames = 0

for guard in game.find_type("Guard"):
    game.guards.append(Guard(game, guard[0], guard[1], Sprite.GUARD))

for boost in game.find_type("Boost"):
    game.boosts.append(boost)

game.clear_references("Guard")
game.clear_references("Spawnpoint")
game.clear_references("Boost")

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
        active_player.queue_movement(keys)

        if frames % CHANGE_INTERVAL == 0:
            for boost in game.boosts:
                game.coordinates[boost[0]][boost[1]]["type"] = Sprite.BOOST.value

            active_player.move()

            for guard in game.guards:
                guard.move()

            for guard in game.guards:
                if (active_player.current_position["x"] == guard.current_position["x"] and
                        active_player.current_position["y"] == guard.current_position["y"]):
                    active_player.health -= 1

            for guard_number in range(len(game.guards)):
                for compared_guard_number in range(guard_number + 1 , len(game.guards)):
                    original_guard = game.guards[guard_number]
                    compared_guard = game.guards[compared_guard_number]
                    if (original_guard.current_position["x"] == compared_guard.current_position["x"] and
                            original_guard.current_position["y"] == compared_guard.current_position["y"]):
                        guard.direction["x"] *= -1; guard.direction["y"] *= -1

        game.render_grid()
        pygame.display.flip()
        clock.tick(FPS)
        frames += 1

    pygame.quit()