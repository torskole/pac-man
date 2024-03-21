# Imports
from enum import Enum

# Dimensions
HEIGHT = 25
WIDTH = 25
BLOCKSIZE = 25

# Settings
FOG = False
VISIBLE_RANGE = 4
FPS = 60
CHANGE_INTERVAL = FPS//8
GUARD_INTERVAL = CHANGE_INTERVAL//0.8

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
BACKGROUND_COLOR = WHITE

path = f"maze_{HEIGHT}_{WIDTH}.txt"
text_file = ""

class Sprite(Enum):
    FUGITIVE = 10
    GUARD = 20
    BOOST = 30
    NONE = 0
    DOWN = 1
    UP = 2
    LEFT = 3
    RIGHT = 4
    IDLE = 5

def coordinates_to_point(x: int, y: int) -> tuple[int, int]:
    """ Returnerer hvilke punkt som tilsvarer koordinatet """
    return (x // BLOCKSIZE, y // BLOCKSIZE)

def point_to_coordinates(x: int, y: int) -> tuple[int, int]:
    """ Returnerer hvilke koordinat som tilsvarer punktet """
    return x * BLOCKSIZE, y * BLOCKSIZE

def validate_file() -> None:
     """ Dersom filen er tom opprettes en template """
     global text_file
     with open(path) as file:
        if file.read() == "":
            text_file = ""
            for y in range(0, HEIGHT):
                    for _ in range (0, WIDTH):
                        text_file += "."

                    if y != WIDTH-1: # Ikke legg til for den siste
                        text_file += "\n"

            write_file(text_file)

def write_file(str) -> None:
    """ Oppdaterer filen med nytt innhold """
    with open(path, "w") as file:
        file.write(str)

def read_file() -> str:
    """ Returnerer filens innhold """
    global text_file
    with open(path) as file:
        validate_file()
        text_file = file.read()
        return text_file
    
def read_character(x, y) -> list:
    """ Returnerer tegnet for angitt posisjon """
    with open(path) as file:
        validate_file()
        content = file.readlines()
        return content[x][y]