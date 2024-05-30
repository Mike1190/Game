import sys

import pygame  # импортируем модуль

from scripts.utils import load_image, load_images, Animation
from scripts.entities import PhysicsEntity, Player
from scripts.tilemap import Tilemap
from scripts.clouds import Clouds

class Game:
    def __init__(self):
        pygame.init()  # запускаем модуль

        pygame.display.set_caption('Game')  # название игры
        self.screen = pygame.display.set_mode((640, 480))  # задаем экран
        self.display = pygame.Surface((320, 240))

        self.clock = pygame.time.Clock()  # внутреннее время игры

        self.movement = [False, False]

        self.assets = {
            'decor': load_images('tiles/decor'),
            'grass': load_images('tiles/grass'),
            'large_decor': load_images('tiles/large_decor'),
            'stone': load_images('tiles/stone'),
            'player': load_image('entities/player/player.png'),
            'background': load_image('background.png'),
            'clouds': load_images('clouds'),
            'player/idle': Animation(load_images('entities/player/idle'), img_dur=6),
            'player/run': Animation(load_images('entities/player/run'), img_dur=4),
            'player/jump': Animation(load_images('entities/player/jump')),
            'player/slide': Animation(load_images('entities/player/slide')),
            'player/wall_slide': Animation(load_images('entities/player/wall_slide')),
        }

        self.clouds = Clouds(self.assets['clouds'], count=16)

        self.player = Player(self,  (50, 50), (8, 15))

        self.tilemap = Tilemap(self, tile_size=16)
        self.tilemap.load('map.json')

        self.scroll = [0, 0]  # камера

    def run(self):
        while True:
            self.display.blit(self.assets['background'], (0, 0))  # экран обновляется каждое мгновение и заполняется указанным цветом

            self.scroll[0] += (self.player.rect().centerx - self.display.get_width() / 2 - self.scroll[0]) / 5  # в примере 30, но тогда больше подстройки камеры (перемещение экрана)
            self.scroll[1] += (self.player.rect().centery - self.display.get_height() / 2 - self.scroll[1]) / 5 # в примере 30, но тогда больше подстройки камеры (перемещение экрана)
            render_scroll = (int(self.scroll[0]), int(self.scroll[1]))  # плавность камеры

            self.clouds.update()
            self.clouds.render(self.display, offset=render_scroll)

            self.tilemap.render(self.display, offset=render_scroll)

            self.player.update(self.tilemap, (self.movement[1] - self.movement[0], 0))
            self.player.render(self.display, offset=render_scroll)


            for event in pygame.event.get():  # обрабатываем события
                if event.type == pygame.QUIT:  # если выход
                    pygame.quit()  # то выходим
                    sys.exit()  # закрываем игру
                if event.type == pygame.KEYDOWN:  # если мы нажали клавишу
                    if event.key == pygame.K_LEFT or event.key == pygame.K_a:  # клавиша влево или a
                        self.movement[0] = True  # например, жмем влево, меняем расположение по оси Х
                    if event.key == pygame.K_RIGHT or event.key == pygame.K_d:  # клавиша вправо или d
                        self.movement[1] = True  # например, жмем вправо, меняем расположение по оси Х
                    if event.key == pygame.K_UP or event.key == pygame.K_w:
                        self.player.velocity[1] = -3
                if event.type == pygame.KEYUP:  # если мы отпустили клавишу
                    if event.key == pygame.K_LEFT or event.key == pygame.K_a:  # клавиша влево или a
                        self.movement[0] = False
                    if event.key == pygame.K_RIGHT or event.key == pygame.K_d:  # клавиша вправо или d
                        self.movement[1] = False

            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
            pygame.display.update()  # обновляем экран
            self.clock.tick(60)  # 60 кадров в секунду

Game().run()