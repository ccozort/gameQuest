
# Sprite classes for platform game
# © 2019 KidsCanCode LLC / All rights reserved.
# mr cozort planted a landmine by importing Sprite directly...
import pygame as pg
from threading import *
import time
from pygame.sprite import Sprite
from settings import *
vec = pg.math.Vector2

class Spritesheet:
    def __init__(self, filename):
        self.spritesheet = pg.image.load(filename).convert()
    def get_image(self, x, y, width, height, xscale, yscale):
        image = pg.Surface((width, height))
        image.blit(self.spritesheet, (0,0), (x,y,width, height))
        image = pg.transform.scale(image, (int(width*xscale), int(height*yscale)))
        return image
class Player(Sprite):
    # include game parameter to pass game class as argument in main...
    def __init__(self, game):
        Sprite.__init__(self)
        self.game = game
        self.walking = False
        self.jumping = False
        self.current_frame = 0
        self.last_update = 0
        self.load_images()
        self.image = self.standing_frames[0]
        # self.image = pg.Surface((30, 40))
        # self.image = self.game.spritesheet.get_image(0,0,32,32, 1)
        self.image.set_colorkey(BLACK)
        # self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.pos = vec(WIDTH / 2, HEIGHT / 2)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.hitpoints = 100
    def load_images(self):
        self.standing_frames = [self.game.spritesheet.get_image(0, 0, 32, 32, 2, 2),
                                self.game.spritesheet.get_image(32, 0, 32, 32, 2, 2)]
        for frame in self.standing_frames:
            frame.set_colorkey(BLACK)
        # self.walk_frames_r = [self.game.spritesheet.get_image(678, 860, 120, 201),
        #                       self.game.spritesheet.get_image(692, 1458, 120, 207)]
        # self.walk_frames_l = []
        # for frame in self.walk_frames_r:
        #     frame.set_colorkey(BLACK)
        #     self.walk_frames_l.append(pg.transform.flip(frame, True, False))
        # self.jump_frame = self.game.spritesheet.get_image(382, 763, 150, 181)
        # self.jump_frame.set_colorkey(BLACK)
    def pew(self):
        if len(self.game.projectiles) > 5:
            lazer = Pewpew(self.game, self.pos.x + self.rect.width/2, self.rect.top, 10, 10)
            # print("trying to pewpewpew")
            self.game.all_sprites.add(lazer)
            # self.game.platforms.add(lazer)
            self.game.projectiles.add(lazer)
    def jump(self):
        self.rect.x += 1
        hits = pg.sprite.spritecollide(self, self.game.platforms, False)
        self.rect.x -= 1
        if hits: 
            self.acc.y = -PLAYER_JUMPPOWER
    def animate(self):
        now = pg.time.get_ticks()
        if not self.jumping and not self.walking:
            if now - self.last_update > 350:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.standing_frames)
                bottom = self.rect.bottom
                self.image = self.standing_frames[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom
    def update(self):
        self.animate()
        self.acc = vec(0, 0.5)
        keys = pg.key.get_pressed()
        if keys[pg.K_a]:
            self.acc.x = -PLAYER_ACC
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
        # if self.pos.y < 0:
        #     self.pos.y = HEIGHT
        # if self.pos.y > HEIGHT:
        #     self.pos.y = 0
        self.rect.midbottom = self.pos
class Monster(Sprite):
    # include game parameter to pass game class as argument in main...
    def __init__(self, game):
        Sprite.__init__(self)
        self.game = game
        # self.image = pg.Surface((30, 40))
        self.walking = False
        self.jumping = False
        self.load_images()
        self.last_update = 0
        self.current_frame = 0
        self.image = self.standing_frames[0]
        # self.image.fill(LIGHTGREEN)
        self.rect = self.image.get_rect()
        # self.rect.center = (WIDTH / 2, HEIGHT / 2)
        # self.pos = vec(WIDTH / 2, HEIGHT / 2)
        # self.vel = vec(0, 0)
        # self.acc = vec(0.5, 0)
        self.hitpoints = 100        
        # self.rect.midbottom = self.pos
    def load_images(self):
        self.standing_frames = [self.game.spritesheet.get_image(0, 160, 32, 32, 2, 2),
                                self.game.spritesheet.get_image(32, 160, 32, 32, 2, 2)]
        for frame in self.standing_frames:
            frame.set_colorkey(BLACK)
    def animate(self):
        now = pg.time.get_ticks()
        if not self.jumping and not self.walking:
            if now - self.last_update > 350:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.standing_frames)
                bottom = self.rect.bottom
                self.image = self.standing_frames[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom
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
        # self.image = pg.Surface((w, h))
        self.image = self.game.spritesheet.get_image(0,256,128,16, 1, 1)
        self.image.set_colorkey(BLACK)
        # self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.spawn()
    def spawn(self):
        self.mob = Monster(self.game)
        self.mob.rect.midbottom = self.rect.midtop
        self.game.monsters.add(self.mob)
        self.game.all_sprites.add(self.mob)
    def update(self):
        # pass
        self.mob.animate()
        self.mob.rect.midbottom = self.rect.midtop
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