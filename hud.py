import pygame as pg
from settings import *


def draw_player_health(surface, x, y, percentage):
    if percentage < 0:
        percentage = 0
    fill = percentage * HEALTH_BAR_LENGTH
    outline_rect = pg.Rect(x, y, HEALTH_BAR_LENGTH, HEALTH_BAR_HEIGHT)
    fill_rect = pg.Rect(x, y, fill, HEALTH_BAR_HEIGHT)
    if percentage > 0.7:
        color = GREEN
    elif percentage > 0.4:
        color = YELLOW
    else:
        color = RED
    pg.draw.rect(surface, color, fill_rect)
    pg.draw.rect(surface, BLACK, outline_rect, 2)
