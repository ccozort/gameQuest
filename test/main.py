# KidsCanCode - Game Development with Pygame video series
# Jumpy! (a platform game) - Part 2
# Video link: https://www.youtube.com/watch?v=8LRI0RLKyt0
# Player movement
# © 2019 KidsCanCode LLC / All rights reserved.

# Week of march 23 - Lore
# Modularity, Github, import as, 

import pygame as pg
from threading import *
from time import *
from pygame.sprite import Group
# from pg.sprite import Group
import random
from settings import *
from sprites import *
from os import path

class Game:
    def __init__(self):
        # initialize game window, etc
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.running = True
        self.font_name = pg.font.match_font(FONT_NAME)
        self.load_data()
    def load_data(self):
        self.dir = path.dirname(__file__)
        img_dir = path.join(self.dir, 'img')
        # with open(path.join(self.dir, HS_FILE), 'r') as f:
        #     try:
        #         self.highscore = int(f.read())
        #     except:
        #         self.highscore = 0
        self.spritesheet = Spritesheet(path.join(img_dir, SPRITESHEET))
    def new(self):
        # start a new game
        self.score = 0
        self.all_sprites = Group()
        self.platforms = Group()
        self.monsters = Group()
        self.platcount = 0
        self.projectiles = Group()
        self.player = Player(self)
        self.all_sprites.add(self.player)
        # ground = Platform(self, 0, HEIGHT-40, WIDTH, 40)
        # self.all_sprites.add(ground)
        # self.platforms.add(ground)
        self.tempGroup = Group()
        # generates platforms that don't touch each other...
        # cite sources...
        for plat in range(0, 6):
            if len(self.platforms) < 2:
                plat = Platform(self, random.randint(0,WIDTH-100), random.randint(0,HEIGHT-100), 100, 15)
                self.platforms.add(plat)
                self.all_sprites.add(plat)
                plat.spawn()
                # print(self.platforms)
            # break
            while True:
                newPlat = Platform(self, random.randint(0,WIDTH-100), random.randint(0,HEIGHT-100), 100, 15)
                self.tempGroup.add(newPlat)
                selfCollide = pg.sprite.groupcollide(self.tempGroup, self.platforms, True, False)
                allCollide = pg.sprite.groupcollide(self.tempGroup, self.all_sprites, True, False)
                if not selfCollide and not allCollide:
                    self.platforms.add(newPlat)
                    self.all_sprites.add(newPlat)
                    self.tempGroup.remove(newPlat)
                    # print(len(self.tempGroup))
                    break

        self.run()
    def platGen(self):
        newPlat = Platform(self, random.randint(0,WIDTH-100), random.randint(-25, 0), 100, 15)
        self.platforms.add(newPlat)
        self.all_sprites.add(newPlat)
        # self.tempGroup.add(newPlat)
        # selfCollide = pg.sprite.groupcollide(self.tempGroup, self.platforms, True, False)
        # allCollide = pg.sprite.groupcollide(self.tempGroup, self.all_sprites, True, False)
        # if not selfCollide:
        #     self.platforms.add(newPlat)
        #     self.all_sprites.add(newPlat)
        #     self.tempGroup.remove(newPlat)
        #     # print(len(self.tempGroup))
    def run(self):
        # Game Loop
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()
    def update(self):
        # Update - listen to see if anything changes...
        self.all_sprites.update()
        for p in self.projectiles:
            # print(p.birth)
            if p.rect.y < 0:
                p.kill()
                # print(self.projectiles)
        if self.player.rect.bottom > HEIGHT:
            for sprite in self.all_sprites:
                sprite.rect.y -= max(self.player.vel.y, 10)
                if sprite.rect.bottom < 0:
                    sprite.kill()
            if len(self.platforms) == 0:
                self.playing = False
        phits = pg.sprite.groupcollide(self.projectiles, self.platforms, False, False)
        if phits:
            pass
            # print("a projectile collided with a plat...")
        hits = pg.sprite.spritecollide(self.player, self.platforms, False)
        if hits:
            self.player.vel.y = 0
            self.player.pos.y = hits[0].rect.top+1
            # if self.player.rect.top > hits[0].rect.top:
            #     # print("i hit my head")
            #     self.player.vel.y = 15
            #     self.player.rect.top = hits[0].rect.bottom + 5
            # else:
            #     self.player.vel.y = 0
            #     self.player.pos.y = hits[0].rect.top+1
        if self.player.rect.top <= HEIGHT / 4:
            self.player.pos.y += int(abs(self.player.vel.y))
            for plat in self.platforms:
                plat.rect.y += int(abs(self.player.vel.y))
                if plat.rect.top > HEIGHT:
                    plat.kill()
            for mob in self.monsters:
                mob.rect.y += int(abs(self.player.vel.y))
                if mob.rect.bottom > HEIGHT:
                    mob.kill()
                    print(self.monsters)
                    # print(len(self.platforms))
        while len(self.platforms) < 7:
            self.platGen()     
    def events(self):
        # Game Loop - events
        for event in pg.event.get():
            # check for closing window
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
    def draw(self):
        # Game Loop - draw
        self.screen.fill(LIGHTBLUE)
        self.all_sprites.draw(self.screen)
        self.draw_text(str(self.score), 22, WHITE, WIDTH/2, 15)
        # *after* drawing everything, flip the display
        pg.display.flip()
    def show_start_screen(self):
        # game splash/start screen
        self.screen.fill(BLACK)
        self.draw_text("Leapin' Wizards", 48, WHITE, WIDTH/2, HEIGHT/4)
        self.draw_text("Arrows to move, Space to jump", 22, WHITE, WIDTH/2, HEIGHT/2)
        self.draw_text("Press key to play", 22, WHITE, WIDTH / 2, HEIGHT * 3 / 4)
        pg.display.flip()
        self.wait_for_key()
    def show_go_screen(self):
        # game over/continue
        if not self.running:
            return
        self.screen.fill(BLACK)
        self.draw_text("Leapin' Wizards", 48, WHITE, WIDTH/2, HEIGHT/4)
        self.draw_text("Arrows to move, Space to jump", 22, WHITE, WIDTH/2, HEIGHT/2)
        self.draw_text("Press key to play", 22, WHITE, WIDTH / 2, HEIGHT * 3 / 4)
        pg.display.flip()
        self.wait_for_key()
    def wait_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                if event.type == pg.KEYUP:
                    waiting = False
    def draw_text(self, text, size, color, x, y):
        font = pg.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (int(x), int(y))
        self.screen.blit(text_surface, text_rect)


g = Game()
g.show_start_screen()
while g.running:
    g.new()
    g.show_go_screen()

pg.quit()
