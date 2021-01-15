import pygame as pg
from settings import *
from tilemap import collide_hit_rect
from random import uniform
vec = pg.math.Vector2


def collide_with_walls(sprite, group, dir):
    if dir == 'x':
        hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        if hits:
            if hits[0].rect.centerx > sprite.hit_rect.centerx:
                sprite.pos.x = hits[0].rect.left - sprite.hit_rect.width / 2
            if hits[0].rect.centerx < sprite.hit_rect.centerx:
                sprite.pos.x = hits[0].rect.right + sprite.hit_rect.width / 2
            sprite.vel.x = 0
            sprite.hit_rect.centerx = sprite.pos.x
    if dir == 'y':
        hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        if hits:
            if hits[0].rect.centery > sprite.hit_rect.centery:
                sprite.pos.y = hits[0].rect.top - sprite.hit_rect.height / 2
            if hits[0].rect.centery < sprite.hit_rect.centery:
                sprite.pos.y = hits[0].rect.bottom + sprite.hit_rect.height / 2
            sprite.vel.y = 0
            sprite.hit_rect.centery = sprite.pos.y


class Spritesheet:
    # utility class for loading and parsing spritesheets
    def __init__(self, filename):
        self.spritesheet = pg.image.load(filename).convert()

    def get_image(self, x, y, width, height):
        # grab an image out of a larger spritesheet
        image = pg.Surface((width, height))
        image.blit(self.spritesheet, (0, 0), (x, y, width, height))
        image = pg.transform.scale(image, (width // 2, height // 2))
        # image = pg.transform.scale(image, (TILESIZE, TILESIZE))
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
        self.hit_rect = self.rect
        self.hit_rect.center = self.rect.center
        self.vel = vec(0, 0)
        self.pos = vec(x, y)
        self.last_shot = 0
        self.rot = 0
        self.health = PLAYER_HEALTH

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
        if keys[pg.K_SPACE]:
            self.get_mouse_angle()
            now = pg.time.get_ticks()
            if now - self.last_shot > FIREBALL_RATE:
                self.last_shot = now
                dir = vec(1, 0).rotate(-self.rot)
                pos = self.pos + FIREBALL_OFFSET.rotate(-self.rot)  # offset the fireball spawn point
                Fireball(self.game, pos, dir)

    def get_mouse_angle(self):  # calculate the angle between the character and the cursor
        mousex, mousey = pg.mouse.get_pos()
        self.rot = (vec(mousex, mousey) - self.game.player.pos - self.game.camera.pos).angle_to(vec(1, 0))

    def update(self):
        self.animate()
        self.get_keys()
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.pos += self.vel * self.game.dt
        self.hit_rect.centerx = self.pos.x
        collide_with_walls(self, self.game.walls, 'x')
        self.hit_rect.centery = self.pos.y
        collide_with_walls(self, self.game.walls, 'y')
        self.rect.center = self.hit_rect.center

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


class Mob(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.mobs
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.load_images()
        self.image = game.mobs_spritesheet.get_image(8, 48, 47, 39).copy()
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.hit_rect = self.rect.copy()
        self.hit_rect.center = self.rect.center
        self.pos = vec(x, y)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.rect.center = self.pos
        self.rot = 0
        self.max_health = MOB_HEALTH
        self.health = MOB_HEALTH
        self.current_frame = 0
        self.last_update = 0

    def load_images(self):
        self.jump_frames = [self.game.mobs_spritesheet.get_image(8, 48, 47, 39).copy(),
                     self.game.mobs_spritesheet.get_image(72, 52, 47, 35).copy(),
                     self.game.mobs_spritesheet.get_image(132, 56, 55, 31).copy(),
                     self.game.mobs_spritesheet.get_image(200, 52, 47, 35).copy()]
        for frame in self.jump_frames:
            frame.set_colorkey(WHITE)

    def update(self):
        self.animate()
        self.rot = (self.game.player.pos - self.pos).angle_to(vec(1, 0))
        # self.image = pg.transform.rotate(self.game.mob_img, self.rot) #  optional rotating of the mob toward the player
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.acc = vec(MOB_SPEED, 0).rotate(-self.rot)
        self.acc += self.vel * -1
        self.vel += self.acc * self.game.dt
        self.pos += self.vel * self.game.dt + 0.5 * self.acc * self.game.dt ** 2
        self.hit_rect.centerx = self.pos.x
        collide_with_walls(self, self.game.walls, 'x')
        self.hit_rect.centery = self.pos.y
        collide_with_walls(self, self.game.walls, 'y')
        self.rect.center = self.hit_rect.center
        if self.health <= 0:
            self.kill()

    def animate(self):
        now = pg.time.get_ticks()
        self.image = self.jump_frames[self.current_frame].copy()
        if now - self.last_update > 200:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.jump_frames)
            self.image = self.jump_frames[self.current_frame].copy()

    def draw_health_bar(self):
        if self.health / self.max_health * 100 > 70:
            col = GREEN
        elif self.health / self.max_health * 100 > 40:
            col = YELLOW
        else:
            col = RED
        width = int(self.rect.width * self.health / self.max_health)
        self.health_bar = pg.Rect(0, 0, width, 5)
        if self.health < self.max_health:  # only draw once monster has less than 100 HP
            pg.draw.rect(self.image, col, self.health_bar)
            pg.draw.rect(self.image, BLACK, self.health_bar, 2)


class Fireball(pg.sprite.Sprite):
    def __init__(self, game, pos, dir):
        self.groups = game.all_sprites, game.projectiles
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.fireball_img
        self.image = pg.transform.scale(self.image, (int(TILESIZE * 0.25), int(TILESIZE * 0.25)))
        self.rect = self.image.get_rect()
        self.hit_rect = self.rect
        self.pos = vec(pos)
        self.rect.center = vec(pos)
        spread = uniform(-FIREBALL_SPREAD, FIREBALL_SPREAD)
        self.vel = dir.rotate(spread) * FIREBALL_SPEED
        self.spawn_time = pg.time.get_ticks()

    def update(self):
        self.pos += self.vel * self.game.dt
        self.rect.center = self.pos
        if pg.sprite.spritecollideany(self, self.game.walls):
            self.kill()
        if pg.time.get_ticks() - self.spawn_time > FIREBALL_LIFETIME:
            self.kill()


class Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y, width, height):
        self.groups = game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.wall_img
        self.rect = pg.Rect(x, y, width, height)
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y
