import pygame as pg
vec = pg.math.Vector2

# define some colors (R, G, B)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGREY = (40, 40, 40)
LIGHTGREY = (100, 100, 100)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BROWN = (106, 55, 5)

# game settings
WIDTH = 1024   # 16 * 64 or 32 * 32 or 64 * 16
HEIGHT = 768  # 16 * 48 or 32 * 24 or 64 * 12
FPS = 60
TITLE = "Eventyr - WIP"
BGCOLOR = BROWN

TILESIZE = 48
GRIDWIDTH = WIDTH / TILESIZE
GRIDHEIGHT = HEIGHT / TILESIZE

WALL_IMG = 'tileGreen_39.png'

# player settings
PLAYER_HEALTH = 100
PLAYER_SPEED = 250
PLAYER_IMG = 'character.png'

# fireball settings
FIREBALL_IMG = 'fireball.png'
FIREBALL_SPEED = 500
FIREBALL_LIFETIME = 1000
FIREBALL_RATE = 150
FIREBALL_OFFSET = vec(15, 5)
FIREBALL_SPREAD = 7
FIREBALL_DAMAGE = 10

# mob settings
MOBS_IMG = 'mobs.png'
MOB_SPEED = 175
MOB_HEALTH = 100
MOB_KNOCKBACK = 10

MOB_DAMAGE = 5