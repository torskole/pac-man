import pygame
from pygame.locals import (K_w, K_s, K_g, K_b, K_ESCAPE)
from main import Game
from utils import *

game = Game()

clock = pygame.time.Clock()

current_mode = "W"
delete_mode = False
active = True

def read_point(x, y):
    # Access the global variable text_file
    global text_file
    
    if x >= WIDTH or x < 0 or y >= HEIGHT or y < 0:
        print("Out of range")
        return

    # Open the file in read and write mode
    with open(path, "r+") as file:
        # Read all the lines of the file
        lines = file.readlines()
        # Get the current line at the specified row (x)
        current_line = lines[y]
        # Update the character at the specified column (y) to "X" in the current line
        if delete_mode:
            updated_line = current_line[:x] + "." + current_line[x+1:]
        else:
            updated_line = current_line[:x] + current_mode + current_line[x+1:]
        # Replace the old line with the updated line in the lines list
        lines[y] = updated_line
        # Move the file pointer to the beginning of the file
        file.seek(0)
        # Write the updated lines back to the file
        file.writelines(lines)
    
    # Change the color of the corresponding grid cell in the game display to YELLOW
    if delete_mode:
        game.coordinates[x][y]["color"] = WHITE
    else:
        match current_mode:    
            case "W":
                game.coordinates[x][y]["color"] = BLACK
            case "S":
                game.coordinates[x][y]["color"] = YELLOW
            case "G":
                game.coordinates[x][y]["color"] = BLUE
            case "B":
                game.coordinates[x][y]["color"] = GREEN
            case _:
                game.coordinates[x][y]["color"] = WHITE
    
    # Print a message indicating that the character at the specified position has been changed
    print("Character at position ({}, {}) changed".format(x, y))

if __name__ == "__main__":
    read_file()
    while active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                active = False
            elif event.type == pygame.KEYDOWN:
                keys = pygame.key.get_pressed()
                if keys[K_ESCAPE]:
                    active = False
                elif keys[K_w]:
                    current_mode = "W"
                elif keys[K_s]:
                    current_mode = "S"
                elif keys[K_g]:
                    current_mode = "G"
                elif keys[K_b]:
                    current_mode = "B"
                print("Current mode:", current_mode)  

        mouse_buttons = pygame.mouse.get_pressed()

        if mouse_buttons[0]:
            delete_mode = False
            x,y = pygame.mouse.get_pos()
            point_x, point_y = game.coordinates_to_point(x,y)
            read_point(point_x, point_y)

        if mouse_buttons[1]:
            write_file("")
            game = Game()
            print("Reset")

        if mouse_buttons[2]:
            delete_mode = True
            x,y = pygame.mouse.get_pos()
            point_x, point_y = game.coordinates_to_point(x,y)
            read_point(point_x, point_y)

        game.render_grid()
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()