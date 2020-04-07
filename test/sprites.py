
# Sprite classes for platform game
# © 2019 KidsCanCode LLC / All rights reserved.
# mr cozort planted a landmine by importing Sprite directly...
import pygame as pg
from threading import *
import time
from pygame.sprite import Sprite
from settings import *
vec = pg.math.Vector2

class Player(Sprite):
    # include game parameter to pass game class as argument in main...
    def __init__(self, game):
        Sprite.__init__(self)
        self.game = game
        self.image = pg.Surface((30, 40))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.pos = vec(WIDTH / 2, HEIGHT / 2)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.hitpoints = 100
    def pew(self):
        lazer = Pewpew(self.game, self.pos.x + self.rect.width/2, self.rect.top, 10, 10)
        # print("trying to pewpewpew")
        self.game.all_sprites.add(lazer)
        self.game.platforms.add(lazer)
        self.game.projectiles.add(lazer)
    def jump(self):
        self.rect.x += 1
        hits = pg.sprite.spritecollide(self, self.game.platforms, False)
        self.rect.x -= 1
        if hits: 
            self.acc.y = -10
    def update(self):
        self.acc = vec(0, 0.5)
        keys = pg.key.get_pressed()
        if keys[pg.K_a]:
            self.acc.x = -PLAYER_ACC
            print(self.acc.x)
            print(self.acc)
            print(self.acc.x)
        if keys[pg.K_d]:
            self.acc.x = PLAYER_ACC
        if keys[pg.K_w]:
            self.pew()
            # self.acc.y = -PLAYER_ACC
        if keys[pg.K_s]:
            pass
            # self.acc.y = PLAYER_ACC
        # ALERT - Mr. Cozort did this WAY differently than Mr. Bradfield...
        if keys[pg.K_SPACE]:
            self.jump()
        # apply friction
        self.acc.x += self.vel.x * PLAYER_FRICTION
        # self.acc.y += self.vel.y * PLAYER_FRICTION
        # equations of motion
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        # wrap around the sides of the screen
        if self.pos.x > WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = WIDTH
        if self.pos.y < 0:
            self.pos.y = HEIGHT
        if self.pos.y > HEIGHT:
            self.pos.y = 0
        self.rect.midbottom = self.pos
class Monster(Sprite):
    # include game parameter to pass game class as argument in main...
    def __init__(self, game):
        Sprite.__init__(self)
        self.game = game
        self.image = pg.Surface((30, 40))
        self.image.fill(LIGHTGREEN)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.pos = vec(WIDTH / 2, HEIGHT / 2)
        self.vel = vec(0, 0)
        self.acc = vec(0.5, 0)
        self.hitpoints = 100        
        self.rect.midbottom = self.pos
    def update(self):
        pass
        # self.acc = vec(0.5, 0)
        # apply friction
        # self.acc.x += self.vel.x * MONSTER_FRICTION
        # # self.acc.y += self.vel.y * PLAYER_FRICTION
        # # equations of motion
        # self.vel += self.acc
        # self.pos += self.vel + 0.5 * self.acc
        # # wrap around the sides of the screen
        # # self.vel.x += 5
        # self.rect.midbottom = self.pos 
class Platform(Sprite):
    def __init__(self, game, x, y, w, h):
        Sprite.__init__(self)
        self.game = game
        self.image = pg.Surface((w, h))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.mob = Monster(self.game)
        self.mob.pos = self.rect.midtop
        self.spawn()
    def spawn(self):
        self.game.all_sprites.add(self.mob)
        self.game.monsters.add(self.mob)
    def update(self):
        if self.mob.rect.x > self.rect.width:
            self.mob.acc.x = -0.1
        if self.mob.rect.x < self.rect.x:
            self.mob.acc.x = 0.1
        self.mob.vel += self.mob.acc
        self.mob.pos += self.mob.vel + 0.5 * self.mob.acc
        self.mob.acc = vec(0,0)
        self.mob.rect.midbottom = self.mob.pos

class Pewpew(Sprite):
    def __init__(self, game, x, y, w, h):
        Sprite.__init__(self)
        self.game = game
        self.image = pg.Surface((w, h))
        self.image.fill(LIGHTBLUE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.birth = time.perf_counter_ns()
        self.lifespan = 3000000000

    def update(self):
        # self.rect.y -= 5
        self.now = time.perf_counter_ns()
        if self.now - self.birth > self.lifespan:
            self.kill()