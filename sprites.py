import pygame
from settings import *
from utilities import collide_hit_rect


def collide_with_rectangles(sprite, group, direction):
    hits = pygame.sprite.spritecollide(sprite, group, False, collide_hit_rect)
    if direction == 'x':
        if hits:
            if hits[0].rect.centerx > sprite.hit_rect.centerx:
                sprite.position.x = hits[0].rect.left - sprite.hit_rect.width / 2
            if hits[0].rect.centerx < sprite.hit_rect.centerx:
                sprite.position.x = hits[0].rect.right + sprite.hit_rect.width / 2
            sprite.velocity.x = 0
            sprite.hit_rect.centerx = sprite.position.x
    if direction == 'y':
        if hits:
            if hits[0].rect.centery > sprite.hit_rect.centery:
                sprite.position.y = hits[0].rect.top - sprite.hit_rect.height / 2
            if hits[0].rect.centery < sprite.hit_rect.centery:
                sprite.position.y = hits[0].rect.bottom + sprite.hit_rect.height / 2
            sprite.velocity.y = 0
            sprite.hit_rect.centery = sprite.position.y


class Spritesheet:  # utility class for loading and parsing spritesheets
    def __init__(self, filename, alpha=False, colorkey=BLACK):
        self.spritesheet = None
        self.filename = filename
        self.alpha = alpha
        self.colorkey = colorkey

    def get_image(self, x, y, width, height):  # grab an image out of a larger spritesheet
        image = pygame.Surface((width, height))
        if self.alpha:
            self.spritesheet = pygame.image.load(self.filename).convert_alpha()
            image.set_colorkey(self.colorkey)
        else:
            self.spritesheet = pygame.image.load(self.filename).convert()
            image.set_colorkey(self.colorkey)
        image.blit(self.spritesheet, (0, 0), (x, y, width, height))
        image = pygame.transform.scale(image, (width // 2, height // 2))
        return image