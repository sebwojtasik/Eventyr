from utilities import *
from settings import *


def show_main_menu(self):
    boolean = True
    while boolean:
        draw_text(self, 'Eventyr', self.title_font, 105, WHITE, WIDTH / 2, HEIGHT / 2 - 75, align='center')
        draw_text(self, 'Play', self.title_font, 50, WHITE, WIDTH / 2, HEIGHT / 2 + 75, align='center')
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    boolean = False
        pygame.display.flip()