import os
import sys

import pygame

pygame.init()
size = width, height = 500, 500
screen = pygame.display.set_mode(size)
FPS = 50
clock = pygame.time.Clock()


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    intro_text = []

    fon = pygame.transform.scale(load_image('fon.jpg'), (width, height))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(FPS)


def load_level(filename):
    filename = "data\\" + filename
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))

    # дополняем каждую строку пустыми клетками ('.')
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


tile_images = {
        'wall': load_image('box.png'),
        'empty': load_image('grass.png')
    }
player_image = load_image('mario.png')

tile_width = tile_height = 50

player = None

all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.tile_type = tile_type
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 15, tile_height * pos_y + 5)

    def move(self, left, right, up, down):
        if left:
            self.rect.x -= tile_width
            if pygame.sprite.spritecollideany(self, tiles_group).tile_type == 'wall':
                self.rect.x += tile_width
        if right:
            self.rect.x += tile_width
            if pygame.sprite.spritecollideany(self, tiles_group).tile_type == 'wall':
                self.rect.x -= tile_width
        if up:
            self.rect.y -= tile_height
            if pygame.sprite.spritecollideany(self, tiles_group).tile_type == 'wall':
                self.rect.y += tile_width
        if down:
            self.rect.y += tile_height
            if pygame.sprite.spritecollideany(self, tiles_group).tile_type == 'wall':
                self.rect.y -= tile_width


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == '@':
                Tile('empty', x, y)
                new_player = Player(x, y)
    # вернем игрока, а также размер поля в клетках
    return new_player, x, y


def game():
    try:
        player, level_x, level_y = generate_level(load_level(input("введите уровень\n")))
    except FileNotFoundError:
        print('Такого файла не существует')
        exit()
    start_screen()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.move(1, 0, 0, 0)
                elif event.key == pygame.K_UP:
                    player.move(0, 0, 1, 0)
                elif event.key == pygame.K_DOWN:
                    player.move(0, 0, 0, 1)
                elif event.key == pygame.K_RIGHT:
                    player.move(0, 1, 0, 0)

        pygame.display.flip()
        all_sprites.draw(screen)
        player_group.draw(screen)
        clock.tick(FPS)


if __name__ == "__main__":
    game()
