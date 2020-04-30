# KidsCanCode - Game Development with Pygame video series
# Shmup game - part 1
# Video link: https://www.youtube.com/watch?v=nGufy7weyGY
# Player sprite and movement
import pygame as pg
from pygame.sprite import Sprite
import random

# global variables
WIDTH = 480
HEIGHT = 600
FPS = 60

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# initialize pygame and create window
pg.init()
pg.mixer.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Shmup!")
clock = pg.time.Clock()

class Player(Sprite):
    def __init__(self):
        Sprite.__init__(self)
        self.image = pg.Surface((50,40))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT -10
        self.speedx = 0
        self.speedy = 0
    
all_sprites = pg.sprite.Group()
player = Player()
all_sprites.add(player)

# game loop
running = True
while running:
    # do stuff over and over
    clock.tick(FPS)

    for event in pg.event.get():
        # check for window close
        if event.type == pg.QUIT:
            running = False

    # Update the sprites in the game
    all_sprites.update()

    # Draw or render
    screen.fill(RED)
    all_sprites.draw(screen)
    pg.display.flip()

pg.quit()
