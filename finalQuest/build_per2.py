# KidsCanCode - Game Development with Pygame video series
# Shmup game - part 1
# Video link: https://www.youtube.com/watch?v=nGufy7weyGY
# Player sprite and movement
import pygame as pg
from pygame.sprite import Sprite
import random
from os import path
from pathlib import Path
img_folder = Path("img")
bg_img = img_folder / "bg.png"
print(bg_img)

game_dir = path.join(path.dirname(__file__))
print(game_dir)

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

# Load all game graphics
background = pg.image.load(path.join(game_dir + "/img/bg.png")).convert()
background_rect = background.get_rect()
player_img = pg.image.load(path.join(game_dir + "/img/player.png")).convert()
mob_img = pg.image.load(path.join(game_dir + "/img/mob.png")).convert()
lazer_img = pg.image.load(path.join(game_dir + "/img/lazer.png")).convert()
# meteor_img = pg.image.load(path.join(img_dir, "meteorBrown_med1.png")).convert()
# bullet_img = pg.image.load(path.join(img_dir, "laserRed16.png")).convert()

font_name = pg.font.match_font('arial')
def draw_text(surf, text, size, x, y):
    font = pg.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

def draw__health(surf, x, y, w):
    outline_rect = pg.Rect(x, y, 100, 20)
    fill_rect = pg.Rect(x, y, w, 20)
    pg.draw.rect(surf, RED, fill_rect)
    pg.draw.rect(surf, WHITE, outline_rect, 2)

class Player(Sprite):
    def __init__(self):
        Sprite.__init__(self)
        # self.image = pg.Surface((50,40))
        self.image = pg.transform.scale(player_img, (50, 40))
        # self.image = player_img
        # self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT -10
        self.speedx = 0
        self.speedy = 0
    def update(self):
        self.speedx = 0
        self.speedy = 0
        keystate = pg.key.get_pressed()
        if keystate[pg.K_a]:
            self.speedx = -8
        if keystate[pg.K_d]:
            self.speedx = 8
        # if keystate[pg.K_SPACE]:
        #     self.pew()
        # if keystate[pg.K_w]:
        #     self.speedy = -8
        # if keystate[pg.K_s]:
        #     self.speedy = 8
        self.rect.x += self.speedx
        self.rect.y += self.speedy
    def pew(self):
        lazer = Lazer(self.rect.centerx, self.rect.top)
        all_sprites.add(lazer)
        lazers.add(lazer)
        # print('trying to shoot..')

class Mob(Sprite):
    def __init__(self):
        Sprite.__init__(self)
        # self.image = pg.Surface((30,30))
        self.image = mob_img
        # self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(0, WIDTH - self.rect.width)
        self.rect.y = random.randrange(0, 250)
        self.speedy = random.randrange(1, 10)
        self.speedx = random.randrange(1, 8)
        self.hitpoints = 10      
    def update(self):
        self.health_image = pg.Surface(self.hitpoints, 10)
        self.health_rect.x = self.x
        self.health_rect.y = self.y
        self.rect.x += self.speedx
        # self.rect.y += self.speedy
        if self.rect.x > WIDTH or self.rect.x < 0:
            self.speedx*=-1
            self.rect.y += random.randrange(5,25)
        if self.rect.top > HEIGHT + 10:
            self.rect.y = 0
        if self.hitpoints <= 0:
            self.kill()   

class Lazer(Sprite):
    def __init__(self, x, y):
        Sprite.__init__(self)
        self.image = lazer_img
        # self.image = pg.Surface((5,10))
        # self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10
    def update(self):
        self.rect.y += self.speedy
        if self.rect.y < 0:
            self.kill()
            # print(len(lazers))

all_sprites = pg.sprite.Group()
mobs = pg.sprite.Group()
lazers = pg.sprite.Group()
player = Player()
all_sprites.add(player)
for i in range(8):
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)

# game loop
running = True
while running:
    # do stuff over and over
    clock.tick(FPS)

    for event in pg.event.get():
        # check for window close
        if event.type == pg.QUIT:
            running = False
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                player.pew()

    # Update the sprites in the game
    all_sprites.update()

    hits = pg.sprite.spritecollide(player, mobs, False)

    if hits:
        running = False 

    for m in mobs:
        lhits = pg.sprite.spritecollide(m, lazers, False)
        if lhits:
            m.hitpoints-=1
            print(m.hitpoints)


    # Draw or render
    screen.fill(RED)
    screen.blit(background, background_rect)
    all_sprites.draw(screen)
    pg.display.flip()

pg.quit()
