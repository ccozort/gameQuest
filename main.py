# KidsCanCode - Game Development with Pygame video series
# Jumpy! (a platform game) - Part 2
# Video link: https://www.youtube.com/watch?v=8LRI0RLKyt0
# Player movement
# © 2019 KidsCanCode LLC / All rights reserved.

# Week of march 23 - Lore
# Modularity, Github, import as
# Modularity is file dependencies
# Classes, methods, functions, data types, ...

import pygame as pg
from pygame.sprite import Group
# from pg.sprite import Group
import random
from settings import *
from sprites import *


# Fancy HUD functions
# def draw_player_health(surf, x, y, pct):
#     if pct < 0:
#         pct = 0
#     BAR_LENGTH = 100
#     BAR_HEIGHT = 20
#     fill = pct * BAR_LENGTH
#     outline_rect = pg.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
#     fill_rect = pg.Rect(x, y, fill, BAR_HEIGHT)
#     if pct > 0.6:
#         col = GREEN
#     elif pct > 0.3:
#         col = YELLOW
#     else:
#         col = RED
#     pg.draw.rect(surf, col, fill_rect)
#     pg.draw.rect(surf, WHITE, outline_rect, 2)
# basic health bar

# basic HUD functions
def draw_player_health(surf, x, y, w):
    outline_rect = pg.Rect(x, y, 100, 20)
    fill_rect = pg.Rect(x, y, w, 20)
    pg.draw.rect(surf, RED, fill_rect)
    pg.draw.rect(surf, WHITE, outline_rect, 2)

# this is the game class, we create a new game at the bottom of the code...
class Game:
    def __init__(self):
        # initialize game window, etc
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.running = True
    def new(self):
        # start a new game
        self.all_sprites = Group()
        self.platforms = Group()
        self.posts = Group()
        self.player = Player(self)
        self.all_sprites.add(self.player)
        ground = Platform(0, HEIGHT-40, WIDTH, 40)
        plat1 = Platform(200, 400, 150, 20)
        plat2 = Platform(150, 300, 150, 20)
        plat3 = Platform(10, 200, 400, 20)
        post1 = Post(WIDTH/2, HEIGHT-95, 20, 55)
        self.all_sprites.add(ground)
        self.platforms.add(ground)
        self.all_sprites.add(plat1)
        self.platforms.add(plat1)
        self.all_sprites.add(plat2)
        self.platforms.add(plat2)
        self.all_sprites.add(post1)
        self.posts.add(post1)
        # you need to add new instances of the platform class to groups or it wont update or draw
        self.all_sprites.add(plat3)
        self.platforms.add(plat3)
        # for plat in range(1,10):
        #     plat = Platform(random.randint(0, WIDTH), random.randint(0, HEIGHT), 200, 20)
        #     self.all_sprites.add(plat)
        #     self.platforms.add(plat)
        self.run()
    def run(self):
        # Game Loop
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()
    def events(self):
        # Game Loop - events
        for event in pg.event.get():
            # check for closing window
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False        
    def update(self):
        # Game Loop - Update
        self.all_sprites.update()
        hits = pg.sprite.spritecollide(self.player, self.platforms, False)
        posthits = pg.sprite.spritecollide(self.player, self.posts, False)
        if hits:
            if self.player.rect.top > hits[0].rect.top:
                print("i hit my head")
                self.player.vel.y = 15
                self.player.rect.top = hits[0].rect.bottom + 5
                self.player.hitpoints -= 5
                # print("hitpoints are now " + str(self.player.hitpoints))
                # print(self.player.hitpoints)
            # print("it collided")
            else:
                self.player.vel.y = 0
                self.player.pos.y = hits[0].rect.top+1
        if posthits:
            self.player.hitpoints -= 0.5
            # print("hitpoints are now " + str(self.player.hitpoints))

    def draw(self):
        # Game Loop - draw
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)
        # draw_player_health(self.screen, 10, 10, self.player.hitpoints/100)
        draw_player_health(self.screen, 10, 10, self.player.hitpoints)
        # *after* drawing everything, flip the display
        pg.display.flip()
    def show_start_screen(self):
        # game splash/start screen
        pass
    def show_go_screen(self):
        # game over/continue
        pass

g = Game()
# g.show_start_screen()
while g.running:
    g.new()
    # g.show_go_screen()

pg.quit()
