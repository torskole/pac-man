HEIGHT = 25
WIDTH = 25
BLOCKSIZE = 25
FPS = 60
CHANGE_INTERVAL = FPS//5

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

path = f"maze_{HEIGHT}_{WIDTH}.txt"
text_file = ""

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
    #print("Written")

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