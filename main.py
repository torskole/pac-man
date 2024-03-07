import pygame
from pygame.locals import (K_UP, K_DOWN, K_LEFT, K_RIGHT, K_w, K_s, K_a, K_d)

pygame.init()

WINDOW_WIDTH = 500
WINDOW_HEIGHT = 500

surface = pygame.display.set_mode([WINDOW_WIDTH, WINDOW_HEIGHT])

clock = pygame.time.Clock()
maze = pygame.image.load("maze.png").convert_alpha()
maze = pygame.transform.scale(maze, (WINDOW_WIDTH, WINDOW_HEIGHT))

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

class Game:
    def __init__(self) -> None:
        self.current_score = 0
        self.current_level = 1

class Pacman:
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y

    def move(self, keys):
        if keys[K_UP] or keys[K_w]: # Upwards
            self.y -= 1
        if keys[K_DOWN] or keys[K_s]: # Downwards
            self.y += 1
        if keys[K_LEFT] or keys[K_a]: # Left
            self.x -= 1
        if keys[K_RIGHT] or keys[K_d]: # Right
            self.x += 1

    def render_pacman(self, keys):
        self.move(keys)
        pygame.draw.rect(surface, WHITE, pygame.Rect(self.x, self.y, 20, 20))
        
active = True

active_pacman = Pacman(0, 0)

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

    surface.fill(WHITE)
    surface.blit(maze, (0, 0))
    active_pacman.render_pacman(keys)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
