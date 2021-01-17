import pygame
import sys
from os import path
from settings import *
from sprites import *
from player import *
from obstacles import *
from mobs import *
from tilemap import *
from items import *
from hud import *
import pyscroll


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        pygame.key.set_repeat(500, 100)
        pygame.mouse.set_visible(False)  # hide the cursor
        self.load_data()

    def load_data(self):
        game_folder = path.dirname(__file__)
        img_folder = path.join(game_folder, 'img')
        map_folder = path.join(game_folder, 'maps')
        sfx_folder = path.join(game_folder, 'sfx')
        music_folder = path.join(game_folder, 'music')
        self.map = TiledMap(path.join(map_folder, 'world0.tmx'))
        self.title_font = path.join(img_folder, 'BreatheFire.otf')
        self.dim_screen = pygame.Surface(self.screen.get_size()).convert_alpha()
        self.dim_screen.fill((0, 0, 0, 120))
        self.map_img = self.map.make_map()
        self.map_rect = self.map_img.get_rect()
        self.player_spritesheet = Spritesheet(path.join(img_folder, PLAYER_IMG), colorkey=WHITE)
        self.mobs_spritesheet = Spritesheet(path.join(img_folder, MOBS_IMG), alpha=False, colorkey=BLACK)
        self.projectile_img = pygame.image.load(path.join(img_folder, PROJECTILE_IMG)).convert_alpha()
        self.cursor = pygame.image.load(path.join(img_folder, CURSOR_IMG)).convert_alpha()
        self.cursor = pygame.transform.scale(self.cursor, (CURSOR_SIZE, CURSOR_SIZE))
        self.hearts_spritesheet = Spritesheet(path.join(img_folder, HEARTS_IMG), True, colorkey=BLACK)
        # item loading
        self.item_images = {}
        for item in ITEM_IMAGES:
            self.item_images[item] = pygame.image.load(path.join(img_folder, ITEM_IMAGES[item])).convert_alpha()
        # music loading
        pygame.mixer.music.load(path.join(music_folder, 'Windless Slopes.mp3'))
        for song in BG_MUSIC:
            pygame.mixer.music.queue(path.join(music_folder, song))
        # sound loading
        self.sound_effects = {}
        for key in SOUND_EFFECTS:
            if isinstance(SOUND_EFFECTS[key], str):
                self.sound_effects[key] = pygame.mixer.Sound(path.join(sfx_folder, SOUND_EFFECTS[key]))
            else:
                self.sound_effects[key] = []
                for sound in SOUND_EFFECTS[key]:
                    self.sound_effects[key].append(pygame.mixer.Sound(path.join(sfx_folder, sound)))
        #  set_volume(...) to change volume
        self.slime_idle_sounds = []
        for sound in SLIME_IDLE_SOUNDS:
            self.slime_idle_sounds.append(pygame.mixer.Sound(path.join(sfx_folder, sound)))

    def new(self):  # initialize all variables and do all the setup for a new game
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.walls = pygame.sprite.Group()
        self.mobs = pygame.sprite.Group()
        self.projectiles = pygame.sprite.Group()
        self.items = pygame.sprite.Group()
        for tile_object in self.map.tmxdata.objects:  # spawn all the game objects from map data
            object_center = vec(tile_object.x + tile_object.width / 2, tile_object.y + tile_object.height / 2)
            if tile_object.name == 'player':
                self.player = Player(self, object_center.x, object_center.y)
            if tile_object.name == 'building' or tile_object.name == 'edge':
                Wall(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height)
            if tile_object.name == 'tree':
                Wall(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height)
            if tile_object.name == 'slime':
                Mob(self, object_center.x, object_center.y)
            if tile_object.type == 'item':
                Item(self, object_center, tile_object.name)
        self.camera = Camera(self.map.width, self.map.height)
        self.draw_debug = False
        self.paused = False

    def run(self):  # game loop - set self.playing = False to end the game
        self.playing = True
        pygame.mixer.music.play(loops=1)
        while self.playing:
            self.delta_time = self.clock.tick(FPS) / 1000
            self.events()
            if not self.paused:
                self.update()
            self.draw()

    @staticmethod
    def quit():
        pygame.quit()
        sys.exit()

    def update(self):
        # update portion of the game loop
        self.all_sprites.update()
        self.camera.update(self.player)
        # player hits items
        hits = pygame.sprite.spritecollide(self.player, self.items, False)
        for hit in hits:
            if hit.name == 'health_potion' and self.player.health < self.player.max_health:
                hit.kill()
                self.player.heal_amount += HEALTH_POTION_AMOUNT
        # mobs hit player
        hits = pygame.sprite.spritecollide(self.player, self.mobs, False, collide_hit_rect)
        for hit in hits:
            if random() < 0.75:  # play idle sounds
                choice(self.sound_effects['player_hit']).play()
            self.player.health -= MOB_DAMAGE
            hit.velocity = vec(0, 0)
            if self.player.health <= 0:
                self.playing = False
        if hits:
            self.player.position += vec(MOB_KNOCKBACK, 0).rotate(-hits[0].rotation)
        # projectile hit mobs
        hits = pygame.sprite.groupcollide(self.mobs, self.projectiles, False, True)
        for hit in hits:
            hit.health -= PROJECTILE_DAMAGE
            hit.velocity = vec(0, 0)

    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pygame.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pygame.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))

    def draw(self):
        pygame.display.set_caption('Eventyr WIP - FPS: {:.1f}'.format(self.clock.get_fps()))
        self.screen.blit(self.map_img, self.camera.apply_rect(self.map_rect))  # draw map
        for sprite in self.all_sprites:
            if isinstance(sprite, Mob):
                sprite.draw_mob_health_bar()
            self.screen.blit(sprite.image, self.camera.apply(sprite))  # draw character
            if self.draw_debug:
                pygame.draw.rect(self.screen, RED, self.camera.apply_rect(sprite.hit_rect), 1)
        if self.draw_debug:
            self.draw_grid()
            for wall in self.walls:
                pygame.draw.rect(self.screen, RED, self.camera.apply_rect(wall.rect), 1)
        # HUD functions
        draw_player_health(self.screen, 10, 10, self.player.health, self.player.max_health, self.hearts_spritesheet)
        if self.paused:
            self.screen.blit(self.dim_screen, (0, 0))
            draw_text(self, 'Paused', self.title_font, 105, WHITE, WIDTH / 2, HEIGHT / 2, align='center')
        self.screen.blit(self.cursor, (pygame.mouse.get_pos()))
        pygame.display.flip()

    def events(self):
        # catch all events here
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.quit()
                if event.key == pygame.K_h:  # enable debug mode
                    self.draw_debug = not self.draw_debug
                if event.key == pygame.K_p:
                    self.paused = not self.paused

    def show_start_screen(self):
        pass

    def show_go_screen(self):
        pass


# create the game object
g = Game()
g.show_start_screen()
while True:
    g.new()
    g.run()
    g.show_go_screen()
