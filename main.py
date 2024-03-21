# Imports
import pygame
from pygame.locals import (K_UP, K_DOWN, K_LEFT, K_RIGHT, K_w, K_s, K_a, K_d)
from utils import *
import random
import sys

# Determine window size
WINDOW_WIDTH = WIDTH*BLOCKSIZE
WINDOW_HEIGHT = HEIGHT*BLOCKSIZE

# Setting up pygame
pygame.init()
surface = pygame.display.set_mode([WINDOW_WIDTH, WINDOW_HEIGHT])
pygame.display.set_caption("Stjel Pepsi for å rømme fengselet")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)

class Game:
    """
    Klasse for å representere spillet.

    Attributter:
        edit_mode (bool): Hvis spillet skal innta redigeringsmodus
        current_score (int): Gjeldende poengsum (ikke implementert)
        scared_guards (bool): Status for om vaktene er skremt (ikke implementert)
        coordinates (list): En todimensjonal liste som inneholder informasjon om hver rute på spillbrettet
        spawnpoints (list): En liste over spawnpunkter for spilleren
        boosts (list): En liste over boostplasseringer på spillbrettet
        guards (list): En liste over vakter på spillbrettet
        preloaded_images (dict): En dictionary som inneholder forhåndslastede bilder for effektiv bildebehandling
        pause_screen (str): Tekst som vises når spillet ikke er aktivt

    Metoder:
        __init__(self, edit_mode: bool): Initialiserer spillattributter
        render_text(self, text: str, color: tuple) -> None: Rendrer en tekst til skjermen
        load_image(self, key: str) -> pygame.Surface: Returnerer et innlastet bilde, eventuelt laster det inn
        draw_grid(self, x: int, y: int) -> None: Tegner rutenettet til spillbrettet
        render_grid(self, active_player: object) -> None: Rendrer det synlige spillbrettet basert på innstillinger
        find_type(self, type: str) -> list: Returnerer alle ruter av en spesifikk type
        create_new_postions(self, position: dict, direction: dict) -> tuple: Returnerer nye posisjon basert på nåværende posisjon og retning
        check_available_position(self, x: int, y: int) -> bool: Returnerer om en gitt posisjon er tilgjengelig
        clear_references(self, type: str) -> None: Fjerner en bestemt type fra brettet
    """
    def __init__(self, edit_mode: bool) -> None:
        self.edit_mode = edit_mode
        self.current_score = 0
        self.scared_guards = False
        self.coordinates = []
        self.spawnpoints = []
        self.boosts = []
        self.guards = []
        self.preloaded_images = {}
        self.pause_screen = "Press 'r' to begin"

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

    @staticmethod
    def render_text(text: str, color: tuple) -> None:
        """ Rendrer en tekst til skjermen """
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)  # Center the text
        surface.blit(text_surface, text_rect)

        
    def load_image(self, key: str) -> pygame.Surface:
        """ Returnerer et innlastet bilde, eventuelt laster det inn """
        if not key in self.preloaded_images:
            self.preloaded_images[key] = pygame.image.load(f"./sprites/{key}.png").convert_alpha()
        return self.preloaded_images[key]

    def draw_grid(self, x: int, y: int) -> None:
        """ Tegner rutenettet til spillbrettet med figurer """
        cell_rect = pygame.Rect(BLOCKSIZE * x, BLOCKSIZE * y, BLOCKSIZE, BLOCKSIZE)
        match self.coordinates[x][y]["type"]:
            case None:
                pygame.draw.rect(surface, self.coordinates[x][y]["color"], cell_rect, 10)
            case False:
                pygame.draw.rect(surface, self.coordinates[x][y]["color"], cell_rect, 10)
            case _:
                if not self.edit_mode:
                    pygame.draw.rect(surface, BACKGROUND_COLOR, cell_rect, 10)
                    sprite_number = self.coordinates[x][y]["type"]
                    image = self.load_image(sprite_number)

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
                else:
                    pygame.draw.rect(surface, self.coordinates[x][y]["color"], cell_rect, 10)

    def render_grid(self, active_player: object = None) -> None:
        """ Rendrer det synlige spillbrettet basert på innstillinger """
        if FOG:
            player_x, player_y = active_player.current_position["x"], active_player.current_position["y"]
            for y in range(player_y - VISIBLE_RANGE, player_y + VISIBLE_RANGE + 1):
                for x in range(player_x - VISIBLE_RANGE, player_x + VISIBLE_RANGE + 1):
                    if 0 <= x < WIDTH and 0 <= y < HEIGHT:  # Ensure within bounds of the grid
                        self.draw_grid(x, y)
        else:
            for y in range(0, len(self.coordinates)):
                for x in range (0, len(self.coordinates[y])):
                    self.draw_grid(x, y)

    def find_type(self, type: str) -> list:
        """ Returnerer alle ruter av en spesifikk type """
        type_coordinates = []
        for y in range(0, len(self.coordinates)):
            for x in range (0, len(self.coordinates[y])):
                if self.coordinates[x][y]["type"] == type:
                    type_coordinates.append([x, y])
        return type_coordinates
    
    def create_new_postions(self, position: dict, direction: dict) -> tuple[int, int]:
        """ Returnerer nye posisjon basert på nåværende posisjon og retning """
        return position["x"] + direction["x"], position["y"] + direction["y"]

    def check_available_position(self, x: int, y: int) -> bool:
        """ Returnerer om en gitt posisjon er tilgjengelig """
        try:
            if self.coordinates[x][y]["type"] == False:
                return False
            return True
        except:
            print("Checked for non-existent wall")

    def clear_references(self, type: str) -> None:
        """ Fjerner en bestemt type fra brettet """
        points = self.find_type(type)
        for point in points:
            self.coordinates[point[0]][point[1]]["type"] = None
            self.coordinates[point[0]][point[1]]["color"] = WHITE

class MovingFigure:
    """
    Klasse som representerer en bevegelig figur i spillet.

    Metoder:
        __init__(self, game: Game, x: int, y: int, sprite: object) -> None: Initialiserer en bevegelig figur
        update_sprite(self) -> None: Oppdaterer figurens sprite status avhengig av retningen den beveger seg
        move(self) -> None: Beveger figuren dersom tillatt
        request_move(self) -> bool: Returnerer om en bevegelse er tillatt eller ikke
    """
    def __init__(self, game: Game, x: int, y: int, sprite: object) -> None:
        self.game = game
        self.current_position = {"x": x, "y": y}
        self.new_position = {"x": 0, "y": 0}
        self.direction = {"x": 0, "y": 0}
        self.sprite = sprite
        self.sprite_status = self.sprite.value + Sprite.DOWN.value

    def update_sprite(self) -> None:
        """ Oppdaterer figurens sprite status avhengig av retningen den beveger seg """
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
    
    def move(self) -> None:
        """ Beveger figuren dersom tillatt """
        self.update_sprite()

    def request_move(self) -> bool:
        """ Returnerer om en bevegelse er tillatt eller ikke  """
        self.new_position["x"], self.new_position["y"] = game.create_new_postions(self.current_position, {"x": self.direction["x"], "y": self.direction["y"]})

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
    """
    Klasse som representerer en vakt i spillet.

    Metoder:
        __init__(self, game, x, y, sprite) -> None: Initialiserer en vakt
        request_move(self) -> bool: Returnerer om en bevegelse er tillatt eller ikke
        move(self) -> None: Beveger vakten dersom tillatt
    """
    def __init__(self, game, x, y, sprite) -> None:
        super().__init__(game, x, y, sprite)

    def request_move(self) -> bool:
        """ Returnerer om en bevegelse er tillatt eller ikke """
        available_directions = [self.direction]

        if self.direction["x"] != 0:
            new_position1 = game.create_new_postions(self.current_position, {"x": 0, "y": -1})
            new_position2 = game.create_new_postions(self.current_position, {"x": 0, "y": 1})

        if self.direction["y"] != 0:
            new_position1 = game.create_new_postions(self.current_position, {"x": -1, "y": 0})
            new_position2 = game.create_new_postions(self.current_position, {"x": 1, "y": 0})
        
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

    def move(self) -> None:
        """ Beveger vakten dersom tillatt """
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
    """
    Klasse som representerer spilleren i spillet.

    Attributter:
        health (int): Antall liv spilleren har

    Metoder:
        __init__(self, game, x, y, sprite) -> None: Initialiserer spilleren
        move(self) -> None: Beveger spilleren dersom tillatt
        queue_movement(self, keys: object) -> None: Setter retningen basert på tastetrykk
    """
    def __init__(self, game, x, y, sprite) -> None:
        super().__init__(game, x, y, sprite)
        self.health = 2
        
    def move(self) -> None:
        """ Beveger spilleren dersom tillatt """
        if self.request_move():
            if ([self.new_position["x"], self.new_position["y"]]) in game.boosts: # If on a boost
                game.boosts.pop(game.boosts.index([self.new_position["x"], self.new_position["y"]]))
                game.scared_guards = True

            self.game.coordinates[self.current_position["x"]][self.current_position["y"]]["type"] = None
            self.game.coordinates[self.new_position["x"]][self.new_position["y"]]["type"] = self.sprite_status

            self.current_position["x"] = self.new_position["x"]
            self.current_position["y"] = self.new_position["y"]
        return super().move()

    def queue_movement(self, keys: object) -> None:
        """ Setter retningen basert på tastetrykk """
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

def start_game() -> None:
    """ Genererer banen, vakter og spilleren og fjerner tidligere spill """
    global game; global active_player
    game = Game(False)
    game.spawnpoints = game.find_type("Spawnpoint")
    spawnpoint = random.choice(game.spawnpoints)
    active_player = Player(game, spawnpoint[0], spawnpoint[1], Sprite.FUGITIVE)

    # Clear previous game
    game.guards.clear()
    game.boosts.clear()

    for guard in game.find_type("Guard"):
        game.guards.append(Guard(game, guard[0], guard[1], Sprite.GUARD))

    for boost in game.find_type("Boost"):
        game.boosts.append(boost)

    # Clear template types from coordinates
    game.clear_references("Guard")
    game.clear_references("Spawnpoint")
    game.clear_references("Boost")

# Global variables
frames = 0
active_game = False
game: Game = None
active_player: Player = None

start_game()

if __name__ == "__main__":
    while True:
        surface.fill(BLACK)
        for event in pygame.event.get():
                    if event.type == pygame.QUIT: # Close game
                        pygame.quit()
                        sys.exit()
                    elif event.type == pygame.KEYDOWN: # Close game
                        if event.key == pygame.K_ESCAPE:
                            pygame.quit()
                            sys.exit()
                        if event.key == pygame.K_r: # Reset game
                            active_game = not active_game
                            start_game()

        keys = pygame.key.get_pressed()

        if active_game: # If not in pause mode
            active_player.queue_movement(keys)
            if frames % CHANGE_INTERVAL == 0: # For each player movement
                if game.boosts == []: # If all boosts are taken, game has been won
                    active_game = False
                    game.pause_screen = "You won! Press 'r' to restart"
                if active_player.health <= 0: # If the player is dead, game has been lost
                    active_game = False
                    game.pause_screen = "You lost! Press 'r' to restart"

                for boost in game.boosts: # Renders boosts
                    game.coordinates[boost[0]][boost[1]]["type"] = Sprite.BOOST.value

                active_player.move() # Moves player

            if frames % GUARD_INTERVAL == 0: # For each guard movement
                for guard in game.guards: # Move guards
                    guard.move()

                for guard in game.guards: # Check if the guard hits the player
                    if (active_player.current_position["x"] == guard.current_position["x"] and active_player.current_position["y"] == guard.current_position["y"]):
                        active_player.health -= 1 # Removes a health point

                # For every guard see if it collides with another guard
                for guard_number in range(len(game.guards)):
                    for compared_guard_number in range(guard_number + 1 , len(game.guards)):
                        original_guard = game.guards[guard_number]
                        compared_guard = game.guards[compared_guard_number]
                        if (original_guard.current_position["x"] == compared_guard.current_position["x"] and
                                original_guard.current_position["y"] == compared_guard.current_position["y"]):
                            guard.direction["x"] *= -1; guard.direction["y"] *= -1 # Reverses direction to ensure the guards don't overlap

            game.render_grid(active_player) # Renders the visible grid based on the player's position
        else:
            game.render_text(game.pause_screen, WHITE) # Renders text for the pause menu

        # Updates screen
        pygame.display.flip()
        clock.tick(FPS)
        frames += 1