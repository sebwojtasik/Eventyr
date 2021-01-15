import pygame
from settings import *
from sprites import *

class Wall(pygame.sprite.Sprite):
    def __init__(self, game, x, y, width, height):
        self._layer = OBSTACLE_LAYER
        self.groups = game.walls
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.rect = pygame.Rect(x, y, width, height)
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y
