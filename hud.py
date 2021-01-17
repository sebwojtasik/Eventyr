from settings import *
from sprites import *


def draw_player_health(surface, x, y, health, max_health, hearts_spritesheet):
    full_heart = hearts_spritesheet.get_image(0, 0, 64, 58)
    half_heart = hearts_spritesheet.get_image(64, 0, 64, 58)
    empty_heart = hearts_spritesheet.get_image(128, 0, 64, 58)
    empty_heart.set_alpha(150)
    heart_rect = full_heart.get_rect()
    if health < 0:
        health = 0
    half_hearts_total = health / 20
    half_heart_exists = half_hearts_total - int(half_hearts_total) != 0

    for heart in range(int(max_health / 20)):
        heart_rect.x = x + 35 * heart
        heart_rect.y = y
        if int(half_hearts_total) > heart:
            surface.blit(full_heart, heart_rect)
        elif half_heart_exists and int(half_hearts_total) == heart:
            surface.blit(half_heart, heart_rect)
        else:
            surface.blit(empty_heart, heart_rect)
