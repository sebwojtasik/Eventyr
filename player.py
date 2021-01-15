import pygame
from settings import *
from sprites import *
from projectiles import *

class Player(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.animation_state = 'idle'
        self.current_frame = 0
        self.last_update = 0
        self.load_images()
        self.image = self.walk_right_frames[0]
        self.rect = self.image.get_rect()
        self.hit_rect = self.rect
        self.hit_rect.center = self.rect.center
        self.velocity = vec(0, 0)
        self.position = vec(x, y)
        self.last_shot = 0
        self.rotation = 0
        self.health = PLAYER_HEALTH
        self.max_health = PLAYER_HEALTH
        self.full_heart = self.game.hearts_spritesheet.get_image(0, 8, 59, 51)
        self.empty_heart = self.game.hearts_spritesheet.get_image(128, 8, 59, 51)

    def load_images(self):
        self.walk_down_frames = [self.game.player_spritesheet.get_image(41, 29, 56, 76),
                                  self.game.player_spritesheet.get_image(170, 33, 56, 73),
                                  self.game.player_spritesheet.get_image(297, 29, 56, 76),
                                  self.game.player_spritesheet.get_image(425, 33, 56, 73)]
        self.walk_down_left_frames = [self.game.player_spritesheet.get_image(41, 157, 56, 76),
                                 self.game.player_spritesheet.get_image(170, 161, 56, 73),
                                 self.game.player_spritesheet.get_image(297, 157, 56, 76),
                                 self.game.player_spritesheet.get_image(425, 161, 56, 73)]
        self.walk_down_right_frames = [self.game.player_spritesheet.get_image(41, 285, 56, 76),
                                      self.game.player_spritesheet.get_image(170, 289, 56, 73),
                                      self.game.player_spritesheet.get_image(297, 285, 56, 76),
                                      self.game.player_spritesheet.get_image(425, 289, 56, 73)]
        self.walk_left_frames = [self.game.player_spritesheet.get_image(41, 413, 56, 76),
                                 self.game.player_spritesheet.get_image(170, 417, 56, 73),
                                 self.game.player_spritesheet.get_image(297, 413, 56, 76),
                                 self.game.player_spritesheet.get_image(425, 417, 56, 73)]
        self.walk_right_frames = [self.game.player_spritesheet.get_image(41, 541, 56, 76),
                                  self.game.player_spritesheet.get_image(170, 545, 56, 73),
                                  self.game.player_spritesheet.get_image(297, 541, 56, 76),
                                  self.game.player_spritesheet.get_image(425, 545, 56, 73)]
        self.walk_up_frames = [self.game.player_spritesheet.get_image(41, 669, 56, 76),
                                  self.game.player_spritesheet.get_image(170, 673, 56, 73),
                                  self.game.player_spritesheet.get_image(297, 669, 56, 76),
                                  self.game.player_spritesheet.get_image(425, 673, 56, 73)]
        self.walk_up_left_frames = [self.game.player_spritesheet.get_image(41, 797, 56, 76),
                                  self.game.player_spritesheet.get_image(170, 801, 56, 73),
                                  self.game.player_spritesheet.get_image(297, 797, 56, 76),
                                  self.game.player_spritesheet.get_image(425, 801, 56, 73)]
        self.walk_up_right_frames = [self.game.player_spritesheet.get_image(41, 925, 56, 76),
                                    self.game.player_spritesheet.get_image(170, 929, 56, 73),
                                    self.game.player_spritesheet.get_image(297, 925, 56, 76),
                                    self.game.player_spritesheet.get_image(425, 929, 56, 73)]

    def get_keys(self):
        self.velocity = vec(0, 0)
        keys = pygame.key.get_pressed()
        self.animation_state = 'idle'
        if keys[pygame.K_a]:
            self.velocity.x = -PLAYER_SPEED
            self.animation_state = 'left'
        if keys[pygame.K_d]:
            self.velocity.x = PLAYER_SPEED
            self.animation_state = 'right'
        if keys[pygame.K_w]:
            self.velocity.y = -PLAYER_SPEED
            self.animation_state = 'up'
        if keys[pygame.K_s]:
            self.velocity.y = PLAYER_SPEED
            self.animation_state = 'down'
        if keys[pygame.K_s] and keys[pygame.K_d]:
            self.animation_state = 'down_right'
        if keys[pygame.K_s] and keys[pygame.K_a]:
            self.animation_state = 'down_left'
        if keys[pygame.K_w] and keys[pygame.K_d]:
            self.animation_state = 'up_right'
        if keys[pygame.K_w] and keys[pygame.K_a]:
            self.animation_state = 'up_left'
        if self.velocity.x != 0 and self.velocity.y != 0:  # prevent from faster diagonal movement
            self.velocity *= 0.7071
        if keys[pygame.K_SPACE]:
            self.get_mouse_angle()
            now = pygame.time.get_ticks()
            if now - self.last_shot > PROJECTILE_RATE:
                self.last_shot = now
                direction = vec(1, 0).rotate(-self.rotation)
                position = self.position + PROJECTILE_OFFSET.rotate(-self.rotation)  # offset the projectile spawn point
                Projectile(self.game, position, direction)

    def get_mouse_angle(self):  # calculate the angle between the character and the cursor
        mousex, mousey = pygame.mouse.get_pos()
        self.rotation = (vec(mousex, mousey) - self.game.player.position - self.game.camera.position).angle_to(vec(1, 0))

    def update(self):
        self.animate()
        self.get_keys()
        self.rect = self.image.get_rect()
        self.rect.center = self.position
        self.position += self.velocity * self.game.delta_time
        self.hit_rect.centerx = self.position.x
        collide_with_rectangles(self, self.game.walls, 'x')
        self.hit_rect.centery = self.position.y
        collide_with_rectangles(self, self.game.walls, 'y')
        self.rect.center = self.hit_rect.center

    def animate(self):
        now = pygame.time.get_ticks()
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