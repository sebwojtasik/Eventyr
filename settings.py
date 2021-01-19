import pygame
vec = pygame.math.Vector2

# define some colors (R, G, B)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGREY = (40, 40, 40)
LIGHTGREY = (100, 100, 100)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (251, 185, 84)
BROWN = (106, 55, 5)
ORANGE = (247, 150, 23)

# game settings
FULLSCREEN = False
WIDTH = 1024
HEIGHT = 768
FPS = 60
TITLE = "Eventyr - WIP"

TILESIZE = 32
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
PROJECTILE_OFFSET = vec(0, 0)
PROJECTILE_SPREAD = 7
PROJECTILE_DAMAGE = 10

# mob settings
MOBS_IMG = 'slime.png'
MOB_SPEED = [80, 100, 120]
MOB_HEALTH = 100
MOB_KNOCKBACK = 10
MOB_AVOID_RADIUS = 50
MOB_DAMAGE = 10
MOB_DETECT_RADIUS = 300

# items
ITEM_IMAGES = {'health_potion': 'health_potion.png', 'npc': 'johanne.png'}
HEALTH_POTION_AMOUNT = 20
BOB_RANGE = 12
BOB_SPEED = 0.25

# sounds
BG_MUSIC = ['Red Carpet Wooden Floor.mp3', 'Foggy Woods.mp3', 'Celestial.mp3']
# BG_MUSIC = 'Windless Slopes.mp3'
SLIME_IDLE_SOUNDS = ['slime1.wav', 'slime2.wav', 'slime3.wav']
SLIME_HIT_SOUNDS = ['slime_hit.wav']
SOUND_EFFECTS = {'fireball': 'fireball.wav', 'player_hit': ['player_hit.wav']}
# layers
OBSTACLE_LAYER = 1
PLAYER_LAYER = 2
PROJECTILE_LAYER = 1
MOB_LAYER = 2
EFFECTS_LAYER = 4
ITEMS_LAYER = 1

if FULLSCREEN:
    # TODO: find a cleaner way to enable fullscreen
    pygame.init()
    info_object = pygame.display.Info()

    # game settings
    WIDTH = info_object.current_w
    HEIGHT = info_object.current_h
