from enum import Enum

FOG = False
VISIBLE_RANGE = 4

HEIGHT = 25
WIDTH = 25
BLOCKSIZE = 25
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

def coordinates_to_point(x, y) -> tuple[int]:
    return (x // BLOCKSIZE, y // BLOCKSIZE)

def point_to_coordinates(x, y) -> tuple[int]:
    return x * BLOCKSIZE, y * BLOCKSIZE

def validate_file():
     global text_file
     with open(path) as file:
        if file.read() == "":
            text_file = ""
            #print("Writing")
            for y in range(0, HEIGHT):
                    for _ in range (0, WIDTH):
                        text_file += "."

                    if y != WIDTH-1: # Ikke legg til for den siste
                        text_file += "\n"

            write_file(text_file)

def write_file(str):
    with open(path, "w") as file:
        file.write(str)

def read_file():
    global text_file
    with open(path) as file:
        validate_file()
        text_file = file.read()
        return text_file
    
def read_character(x, y):
    with open(path) as file:
        validate_file()
        content = file.readlines()
        return content[x][y]