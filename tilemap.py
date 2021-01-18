import pygame
from settings import *
import pytmx
import pyscroll
vec = pygame.math.Vector2


class TiledMap:
    def __init__(self, game, filename):
        self.game = game
        self.tmx_data = pytmx.load_pygame(filename, pixelalpha=True)
        # create new data source for pyscroll
        self.map_data = pyscroll.TiledMapData(self.tmx_data)
        # create new renderer (camera)
        self.map_layer = pyscroll.BufferedRenderer(self.map_data, (WIDTH, HEIGHT))
        # create a group for sprites rendering
        self.group = pyscroll.PyscrollGroup(map_layer=self.map_layer, default_layer=2)

    def render(self, surface):
        self.group.center(self.game.player.rect.center)
        self.group.draw(surface)

    def apply_rect(self, rect):
        return rect.move((-self.game.map.map_layer.view_rect.x, -self.game.map.map_layer.view_rect.y))
