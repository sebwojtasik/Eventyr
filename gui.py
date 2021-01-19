from utilities import *
from settings import *


class Menu:
    def __init__(self, game, state):
        self.state = state
        self.current_option = 0
        self.game = game
        self.dim_screen = pygame.Surface(self.game.screen.get_size()).convert_alpha()
        self.dim_screen.fill((0, 0, 0, 120))

    def update(self):
        while True:
            if self.state == 'main_menu':
                self.show_main_menu()
            elif self.state == 'continue':
                break
            elif self.state == 'new_game':
                break
            elif self.state == 'options':
                self.show_options()
            elif self.state == 'pause':
                self.show_pause_menu()
            else:
                self.game.quit()
            pygame.display.flip()

    def show_main_menu(self):
        background = pygame.Surface((WIDTH, HEIGHT))
        background.fill(YELLOW)
        self.game.screen.blit(background, (0, 0))
        foreground = pygame.Surface((500, HEIGHT))
        foreground.fill(ORANGE)
        self.game.screen.blit(foreground, (WIDTH / 2 - 250, 0))
        draw_text(self.game, 'Eventyr', self.game.title_font, 105, WHITE, WIDTH / 2, HEIGHT / 2 - 200, align='center')
        entries = {0: ['Continue', self.game.secondary_font, 20, WHITE, WIDTH / 2, HEIGHT / 2, 'continue'],
                   1: ['New Game', self.game.secondary_font, 20, WHITE, WIDTH / 2, HEIGHT / 2 + 50, 'new_game'],
                   2: ['Options', self.game.secondary_font, 20, WHITE, WIDTH / 2, HEIGHT / 2 + 100, 'options'],
                   3: ['Exit', self.game.secondary_font, 20, WHITE, WIDTH / 2, HEIGHT / 2 + 150, 'exit']}
        for entry in entries:
            if entry == self.current_option:
                draw_text(self.game, f'-- {entries[entry][0]} --', entries[entry][1], entries[entry][2],
                          entries[entry][3], entries[entry][4], entries[entry][5], align='center')
            else:
                draw_text(self.game, entries[entry][0], entries[entry][1], entries[entry][2], entries[entry][3],
                          entries[entry][4], entries[entry][5], align='center')
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    self.state = entries[self.current_option][6]
                if event.key == pygame.K_w:
                    if self.current_option == 0:
                        self.current_option = 3
                    else:
                        self.current_option -= 1
                if event.key == pygame.K_s:
                    if self.current_option == 3:
                        self.current_option = 0
                    else:
                        self.current_option += 1
                if event.key == pygame.K_ESCAPE:
                    self.state = 'exit'

    def show_options(self):
        background = pygame.Surface((WIDTH, HEIGHT))
        background.fill(YELLOW)
        self.game.screen.blit(background, (0, 0))
        foreground = pygame.Surface((500, HEIGHT))
        foreground.fill(ORANGE)
        self.game.screen.blit(foreground, (WIDTH / 2 - 250, 0))
        draw_text(self.game, 'Options', self.game.title_font, 105, WHITE, WIDTH / 2, HEIGHT / 2, align='center')
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_BACKSPACE:
                    self.state = 'main_menu'


#  TODO: find a way to do it inside menu class (?) and fix lagging
def show_pause_menu(self):
    self.screen.blit(self.dim_screen, (0, 0))
    foreground = pygame.Surface((500, HEIGHT))
    foreground.fill(ORANGE)
    self.screen.blit(foreground, (WIDTH / 2 - 250, 0))
    draw_text(self, 'Paused', self.title_font, 105, WHITE, WIDTH / 2, HEIGHT / 2 - 200, align='center')
    entries = {0: ['Continue', self.secondary_font, 20, WHITE, WIDTH / 2, HEIGHT / 2, 'continue'],
               1: ['Exit to main menu', self.secondary_font, 20, WHITE, WIDTH / 2, HEIGHT / 2 + 50, 'main_menu'],
               2: ['Exit to desktop', self.secondary_font, 20, WHITE, WIDTH / 2, HEIGHT / 2 + 100, 'exit']}
    for entry in entries:
        if entry == self.pause_menu_current_option:
            draw_text(self, f'-- {entries[entry][0]} --', entries[entry][1], entries[entry][2],
                      entries[entry][3], entries[entry][4], entries[entry][5], align='center')
        else:
            draw_text(self, entries[entry][0], entries[entry][1], entries[entry][2], entries[entry][3],
                      entries[entry][4], entries[entry][5], align='center')

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            print(self.pause_menu_current_option)
            if event.key == pygame.K_w:
                if self.pause_menu_current_option == 0:
                    self.pause_menu_current_option = 2
                else:
                    self.pause_menu_current_option -= 1
            if event.key == pygame.K_s:
                if self.pause_menu_current_option == 2:
                    self.pause_menu_current_option = 0
                else:
                    self.pause_menu_current_option += 1
            if event.key == pygame.K_RETURN:
                if entries[self.pause_menu_current_option][6] == 'continue':
                    self.paused = not self.paused
                elif entries[self.pause_menu_current_option][6] == 'main_menu':
                    self.playing = False
                    self.show_start_screen()
                else:
                    self.quit()
