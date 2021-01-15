import pygame
vec = pygame.math.Vector2

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
FULLSCREEN = True
WIDTH = 1024
HEIGHT = 768
FPS = 60
TITLE = "Eventyr - WIP"

TILESIZE = 48
CURSOR_SIZE = 24
CURSOR_IMG = 'cursor.png'

# player settings
PLAYER_HEALTH = 100
PLAYER_SPEED = 250
PLAYER_IMG = 'character.png'
HEALTH_BAR_LENGTH = 100
HEALTH_BAR_HEIGHT = 20
HEARTS_IMG = 'hearts.png'

# fireball settings
PROJECTILE_IMG = 'fireball.png'
PROJECTILE_SPEED = 400
PROJECTILE_LIFETIME = 1500
PROJECTILE_RATE = 250
PROJECTILE_OFFSET = vec(15, 5)
PROJECTILE_SPREAD = 7
PROJECTILE_DAMAGE = 10

# mob settings
MOBS_IMG = 'mobs.png'
MOB_SPEED = [80, 100, 120]
MOB_HEALTH = 100
MOB_KNOCKBACK = 2
MOB_AVOID_RADIUS = 50
MOB_DAMAGE = 5

# layers
OBSTACLE_LAYER = 1
PLAYER_LAYER = 2
PROJECTILE_LAYER = 1
MOB_LAYER = 2
EFFECTS_LAYER = 3

if FULLSCREEN:
    # TODO: find a cleaner way to enable fullscreen
    pygame.init()
    info_object = pygame.display.Info()

    # game settings
    WIDTH = info_object.current_w
    HEIGHT = info_object.current_h
