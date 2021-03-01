import os
import pygame
import sys

FPS = 50
player = None
fl = True
clock = pygame.time.Clock()
# группы спрайтов
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
pygame.init()
size = width, height = 500, 500
screen = pygame.display.set_mode(size)
xxx, yyy = 0, 0


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname).convert()
    except SystemError:
        print(f"Файл с изображением '{fullname}' не найден")
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
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
player_image = load_image('mario.png', -1)

tile_width = tile_height = 50


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
            save = self.rect.x
            self.rect.x -= tile_width
            if pygame.sprite.spritecollideany(self, tiles_group).tile_type == 'wall':
                self.rect.x = save
                return False
            self.rect.x = save
        if right:
            save = self.rect.x
            self.rect.x += tile_width
            if pygame.sprite.spritecollideany(self, tiles_group).tile_type == 'wall':
                self.rect.x = save
                return False
            self.rect.x = save
        if up:
            save = self.rect.y
            self.rect.y -= tile_height
            if pygame.sprite.spritecollideany(self, tiles_group).tile_type == 'wall':
                self.rect.y = save
                return False
            self.rect.y = save
        if down:
            save = self.rect.y
            self.rect.y += tile_height
            if pygame.sprite.spritecollideany(self, tiles_group).tile_type == 'wall':
                self.rect.y = save
                return False
            self.rect.y = save
        return True


def generate_level(level):
    global fl, xxx, yyy, all_sprites, tiles_group, player_group
    all_sprites = pygame.sprite.Group()
    tiles_group = pygame.sprite.Group()
    player_group = pygame.sprite.Group()
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == '@' and fl:
                Tile('empty', x, y)
                new_player = Player(x, y)
                xxx, yyy = x, y
                fl = False
            elif not fl and level[y][x] == '@':
                Tile('empty', x, y)
    if not fl:
        new_player = Player(xxx, yyy)
    # вернем игрока, а также размер поля в клетках
    return new_player, x, y


def game():
    file = input("введите название файла с картой уровня:\n")
    file = load_level(file)
    player, level_x, level_y = generate_level(file)
    start_screen()
    while True:
        spis = []
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if player.move(1, 0, 0, 0):
                        for i in range(len(file)):
                            ppp = ''
                            ppp += file[i][-1]
                            ppp += file[i][:-1]
                            spis.append(ppp)
                        file = spis[::]
                        player, level_x, level_y = generate_level(file)
                elif event.key == pygame.K_UP:
                    if player.move(0, 0, 1, 0):
                        spis.append(file[-1])
                        spis.extend(file[:-1])
                        file = spis[::]
                        player, level_x, level_y = generate_level(file)
                elif event.key == pygame.K_DOWN:
                    if player.move(0, 0, 0, 1):
                        spis = file[1:]
                        spis.append(file[0])
                        file = spis[::]
                        player, level_x, level_y = generate_level(file)
                elif event.key == pygame.K_RIGHT:
                    if player.move(0, 1, 0, 0):
                        for i in range(len(file)):
                            ppp = ''
                            ppp += file[i][1:]
                            ppp += file[i][0]
                            spis.append(ppp)
                        file = spis[::]
                        player, level_x, level_y = generate_level(file)

        pygame.display.flip()
        all_sprites.draw(screen)
        player_group.draw(screen)
        clock.tick(FPS)


if __name__ == "__main__":
    game()
