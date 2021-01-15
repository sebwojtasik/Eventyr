import pygame
from settings import *
from sprites import *
from pytweening import easeInOutSine


class Item(pygame.sprite.Sprite):
    def __init__(self, game, position, name):
        self._layer = ITEMS_LAYER
        self.groups = game.all_sprites, game.items
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.item_images[name]
        self.rect = self.image.get_rect()
        self.name = name
        self.position = position
        self.rect.center = position
        self.hit_rect = self.rect
        self.hit_rect.center = self.rect.center
        self.position = position
        self.tween = easeInOutSine
        self.step = 0
        self.direction = 1

    def update(self):
        # bobbing motion
        offset = BOB_RANGE * (self.tween(self.step / BOB_RANGE) - 0.5)
        self.rect.centery = self.position.y + offset * self.direction
        self.step += BOB_SPEED
        if self.step > BOB_RANGE:
            self.step = 0
            self.direction *= -1