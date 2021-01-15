import pygame
from settings import *
from sprites import *
from random import uniform
vec = pygame.math.Vector2

class Projectile(pygame.sprite.Sprite):
    def __init__(self, game, pos, direction):
        self._layer = PROJECTILE_LAYER
        self.groups = game.all_sprites, game.projectiles
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.projectile_img
        self.image = pygame.transform.scale(self.image, (int(TILESIZE * 0.5), int(TILESIZE * 0.5)))
        self.rect = self.image.get_rect()
        self.hit_rect = self.rect
        self.pos = vec(pos)
        self.rect.center = vec(pos)
        spread = uniform(-PROJECTILE_SPREAD, PROJECTILE_SPREAD)
        self.velocity = direction.rotate(spread) * PROJECTILE_SPEED
        self.spawn_time = pygame.time.get_ticks()

    def update(self):
        self.pos += self.velocity * self.game.delta_time
        self.rect.center = self.pos
        if pygame.sprite.spritecollideany(self, self.game.walls):
            self.kill()
        if pygame.time.get_ticks() - self.spawn_time > PROJECTILE_LIFETIME:
            self.kill()
