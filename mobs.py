import pygame
from settings import *
from random import choice
from sprites import *


class Mob(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self._layer = MOB_LAYER
        self.groups = game.all_sprites, game.mobs
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.load_images()
        self.image = game.mobs_spritesheet.get_image(8, 48, 47, 39).copy()
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.hit_rect = self.rect.copy()
        self.position = vec(x, y)
        self.velocity = vec(0, 0)
        self.acceleration = vec(0, 0)
        self.rect.center = self.position
        self.hit_rect.center = self.rect.center
        self.rotation = 0
        self.max_health = MOB_HEALTH
        self.health = MOB_HEALTH
        self.current_frame = 0
        self.last_update = 0
        self.speed = choice(MOB_SPEED)
        self.target = game.player

    def load_images(self):
        self.jump_frames = [self.game.mobs_spritesheet.get_image(8, 48, 47, 39).copy(),
                     self.game.mobs_spritesheet.get_image(72, 52, 47, 35).copy(),
                     self.game.mobs_spritesheet.get_image(132, 56, 55, 31).copy(),
                     self.game.mobs_spritesheet.get_image(200, 52, 47, 35).copy()]

    def avoid_other_mobs(self):  # make mobs keep a distance from each other
        for mob in self.game.mobs:
            if mob != self:
                distance = self.position - mob.position
                if 0 < distance.length() < MOB_AVOID_RADIUS:
                    self.acceleration += distance.normalize()

    def update(self):
        self.animate()
        target_distance = self.target.position - self.position
        if target_distance.length_squared() < MOB_DETECT_RADIUS**2:
            self.rotation = target_distance.angle_to(vec(1, 0))
            # self.image = pygame.transform.rotate(self.image, self.rotation) #  rotating of the mob toward the player
            self.image.set_colorkey(WHITE)
            self.rect.center = self.position
            self.acceleration = vec(1, 0).rotate(-self.rotation)
            self.avoid_other_mobs()
            self.acceleration.scale_to_length(self.speed)
            self.acceleration += self.velocity * -1
            self.velocity += self.acceleration * self.game.delta_time
            self.position += self.velocity * self.game.delta_time + 0.5 * self.acceleration * self.game.delta_time ** 2
            self.hit_rect.centerx = self.position.x
            collide_with_rectangles(self, self.game.walls, 'x')
            self.hit_rect.centery = self.position.y
            collide_with_rectangles(self, self.game.walls, 'y')
            self.rect.center = self.hit_rect.center
        if self.health <= 0:
            self.kill()

    def animate(self):
        now = pygame.time.get_ticks()
        self.image = self.jump_frames[self.current_frame].copy()
        if now - self.last_update > 200:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.jump_frames)
            self.image = self.jump_frames[self.current_frame].copy()

    def draw_mob_health_bar(self):
        if self.health / self.max_health * 100 > 70:
            col = GREEN
        elif self.health / self.max_health * 100 > 40:
            col = YELLOW
        else:
            col = RED
        width = int(self.rect.width * self.health / self.max_health)
        self.health_bar = pygame.Rect(0, 0, width, 5)
        if self.health < self.max_health:  # only draw once monster has less than 100 HP
            pygame.draw.rect(self.image, col, self.health_bar)
            pygame.draw.rect(self.image, BLACK, self.health_bar, 2)
