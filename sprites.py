import pygame as pg
from settings import *
vec = pg.math.Vector2


class Spritesheet:
    # utility class for loading and parsing spritesheets
    def __init__(self, filename):
        self.spritesheet = pg.image.load(filename).convert()

    def get_image(self, x, y, width, height):
        # grab an image out of a larger spritesheet
        image = pg.Surface((width, height))
        image.blit(self.spritesheet, (0, 0), (x, y, width, height))
        image = pg.transform.scale(image, (width // 2, height // 2))
        return image

class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.animation_state = 'idle'
        self.current_frame = 0
        self.last_update = 0
        self.load_images()
        self.image = self.walk_right_frames[0]
        self.rect = self.image.get_rect()
        self.vel = vec(0, 0)
        self.pos = vec(x, y) * TILESIZE

    def load_images(self):
        self.walk_down_frames = [self.game.player_spritesheet.get_image(41, 29, 56, 76),
                                  self.game.player_spritesheet.get_image(170, 33, 56, 73),
                                  self.game.player_spritesheet.get_image(297, 29, 56, 76),
                                  self.game.player_spritesheet.get_image(425, 33, 56, 73)]
        for frame in self.walk_down_frames:
            frame.set_colorkey(WHITE)
        self.walk_down_left_frames = [self.game.player_spritesheet.get_image(41, 157, 56, 76),
                                 self.game.player_spritesheet.get_image(170, 161, 56, 73),
                                 self.game.player_spritesheet.get_image(297, 157, 56, 76),
                                 self.game.player_spritesheet.get_image(425, 161, 56, 73)]
        for frame in self.walk_down_left_frames:
            frame.set_colorkey(WHITE)
        self.walk_down_right_frames = [self.game.player_spritesheet.get_image(41, 285, 56, 76),
                                      self.game.player_spritesheet.get_image(170, 289, 56, 73),
                                      self.game.player_spritesheet.get_image(297, 285, 56, 76),
                                      self.game.player_spritesheet.get_image(425, 289, 56, 73)]
        for frame in self.walk_down_right_frames:
            frame.set_colorkey(WHITE)
        self.walk_left_frames = [self.game.player_spritesheet.get_image(41, 413, 56, 76),
                                 self.game.player_spritesheet.get_image(170, 417, 56, 73),
                                 self.game.player_spritesheet.get_image(297, 413, 56, 76),
                                 self.game.player_spritesheet.get_image(425, 417, 56, 73)]
        for frame in self.walk_left_frames:
            frame.set_colorkey(WHITE)
        self.walk_right_frames = [self.game.player_spritesheet.get_image(41, 541, 56, 76),
                                  self.game.player_spritesheet.get_image(170, 545, 56, 73),
                                  self.game.player_spritesheet.get_image(297, 541, 56, 76),
                                  self.game.player_spritesheet.get_image(425, 545, 56, 73)]
        for frame in self.walk_right_frames:
            frame.set_colorkey(WHITE)
        self.walk_up_frames = [self.game.player_spritesheet.get_image(41, 669, 56, 76),
                                  self.game.player_spritesheet.get_image(170, 673, 56, 73),
                                  self.game.player_spritesheet.get_image(297, 669, 56, 76),
                                  self.game.player_spritesheet.get_image(425, 673, 56, 73)]
        for frame in self.walk_up_frames:
            frame.set_colorkey(WHITE)
        self.walk_up_left_frames = [self.game.player_spritesheet.get_image(41, 797, 56, 76),
                                  self.game.player_spritesheet.get_image(170, 801, 56, 73),
                                  self.game.player_spritesheet.get_image(297, 797, 56, 76),
                                  self.game.player_spritesheet.get_image(425, 801, 56, 73)]
        for frame in self.walk_up_left_frames:
            frame.set_colorkey(WHITE)
        self.walk_up_right_frames = [self.game.player_spritesheet.get_image(41, 925, 56, 76),
                                    self.game.player_spritesheet.get_image(170, 929, 56, 73),
                                    self.game.player_spritesheet.get_image(297, 925, 56, 76),
                                    self.game.player_spritesheet.get_image(425, 929, 56, 73)]
        for frame in self.walk_up_right_frames:
            frame.set_colorkey(WHITE)

    def get_keys(self):
        self.vel = vec(0, 0)
        keys = pg.key.get_pressed()
        self.animation_state = 'idle'
        if keys[pg.K_a]:
            self.vel.x = -PLAYER_SPEED
            self.animation_state = 'left'
        if keys[pg.K_d]:
            self.vel.x = PLAYER_SPEED
            self.animation_state = 'right'
        if keys[pg.K_w]:
            self.vel.y = -PLAYER_SPEED
            self.animation_state = 'up'
        if keys[pg.K_s]:
            self.vel.y = PLAYER_SPEED
            self.animation_state = 'down'
        if keys[pg.K_s] and keys[pg.K_d]:
            self.animation_state = 'down_right'
        if keys[pg.K_s] and keys[pg.K_a]:
            self.animation_state = 'down_left'
        if keys[pg.K_w] and keys[pg.K_d]:
            self.animation_state = 'up_right'
        if keys[pg.K_w] and keys[pg.K_a]:
            self.animation_state = 'up_left'
        # prevent from faster diagonal movement
        if self.vel.x != 0 and self.vel.y != 0:
            self.vel *= 0.7071

    def collide_with_walls(self, direction):
        if direction == 'x':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vel.x > 0:
                    self.pos.x = hits[0].rect.left - self.rect.width
                if self.vel.x < 0:
                    self.pos.x = hits[0].rect.right
                self.vel.x = 0
                self.rect.x = self.pos.x
        if direction == 'y':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vel.y > 0:
                    self.pos.y = hits[0].rect.top - self.rect.height
                if self.vel.y < 0:
                    self.pos.y = hits[0].rect.bottom
                self.vel.y = 0
                self.rect.y = self.pos.y

    def update(self):
        self.animate()
        self.get_keys()
        self.pos += self.vel * self.game.dt
        self.rect.x = self.pos.x
        self.collide_with_walls('x')
        self.rect.y = self.pos.y
        self.collide_with_walls('y')

    def animate(self):
        now = pg.time.get_ticks()
        if self.animation_state != 'idle':
            if self.animation_state == 'down':
                if now - self.last_update > 200:
                    self.last_update = now
                    self.current_frame = (self.current_frame + 1) % len(self.walk_down_frames)
                    self.image = self.walk_down_frames[self.current_frame]
            if self.animation_state == 'down_left':
                if now - self.last_update > 200:
                    self.last_update = now
                    self.current_frame = (self.current_frame + 1) % len(self.walk_down_left_frames)
                    self.image = self.walk_down_left_frames[self.current_frame]
            if self.animation_state == 'down_right':
                if now - self.last_update > 200:
                    self.last_update = now
                    self.current_frame = (self.current_frame + 1) % len(self.walk_down_right_frames)
                    self.image = self.walk_down_right_frames[self.current_frame]
            if self.animation_state == 'left':
                if now - self.last_update > 200:
                    self.last_update = now
                    self.current_frame = (self.current_frame + 1) % len(self.walk_left_frames)
                    self.image = self.walk_left_frames[self.current_frame]
            if self.animation_state == 'right':
                if now - self.last_update > 200:
                    self.last_update = now
                    self.current_frame = (self.current_frame + 1) % len(self.walk_right_frames)
                    self.image = self.walk_right_frames[self.current_frame]
            if self.animation_state == 'up':
                if now - self.last_update > 200:
                    self.last_update = now
                    self.current_frame = (self.current_frame + 1) % len(self.walk_up_frames)
                    self.image = self.walk_up_frames[self.current_frame]
            if self.animation_state == 'up_left':
                if now - self.last_update > 200:
                    self.last_update = now
                    self.current_frame = (self.current_frame + 1) % len(self.walk_up_left_frames)
                    self.image = self.walk_up_left_frames[self.current_frame]
            if self.animation_state == 'up_right':
                if now - self.last_update > 200:
                    self.last_update = now
                    self.current_frame = (self.current_frame + 1) % len(self.walk_up_right_frames)
                    self.image = self.walk_up_right_frames[self.current_frame]


class Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(LIGHTGREY)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
