import random
from files import *
pygame.font.init()
import numpy as np
from AI import PatrolAI
import threading


def terminate():
    # здесь мы завершаем программу полностью и записываем сохранения
    save_changes(FPS, volume)
    pygame.quit()
    sys.exit()


def exit_screen():
    # появляется специальный экран перед выходом чтобы переспросить намериния выхода
    exit_win_x, exit_win_y = (width - 400) // 2, (height - 200) // 2

    while True:
        # выставляем громкость, чтобы музыка не меняла её сама и не выключалась, пишем /100, т.к. громкость в
        # интерфейсе в процентах, а в классе pygame.mixer она во float
        fon.set_volume(volume / 100)
        # рисуем само окно с кнопками
        screen.blit(tile_images['exit_win'], (exit_win_x, exit_win_y))
        screen.blit(tile_images['yes'], (exit_win_x + 110, exit_win_y + 110))
        screen.blit(tile_images['no'], (exit_win_x + 230, exit_win_y + 110))

        # обычный проход по событиям и отслеживания выключения проги, нажатия esc, что означает возвращение на
        # предыдущую стадию либо предлог выйти из игры на главном экране; если мы видим нажатие мыши, то
        # мы проверяем было ли нажатие на экран вообще, а если было, то было ли нажатие на какую-то из кнопок
        # и если было, то выполняем её функцию
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                terminate()
            elif ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_ESCAPE:
                    return
            elif ev.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_focused():
                    pos_x, pos_y = pygame.mouse.get_pos()
                    if exit_win_x + 110 <= pos_x <= exit_win_x + 170 and exit_win_y + 110 <= pos_y < exit_win_y + 140:
                        terminate()
                    if exit_win_x + 230 <= pos_x <= exit_win_x + 290 and exit_win_y + 110 <= pos_y < exit_win_y + 140:
                        return

        pygame.display.flip()
        clock.tick(FPS)


def start_screen():
    pygame.mouse.set_visible(True)
    # запускаем фоновую музыку
    fon.play(-1)

    while True:
        # ставим громкость
        fon.set_volume(volume / 100)
        # рисуем окно с интерфейсом
        screen.fill('black')
        screen.blit(tile_images['play'], (width - 450, 100))
        screen.blit(tile_images['rules'], (width - 450, 330))
        screen.blit(tile_images['settings_2'], (width - 450, 510))
        screen.blit(tile_images['exit'], (width - 450, 690))
        screen.blit(tile_images['name'], (200, 250))

        # проверяем то, что я описал в exit_screen
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                terminate()
            elif ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_ESCAPE:
                    exit_screen()
            elif ev.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_focused():
                    pos_x, pos_y = pygame.mouse.get_pos()
                    if width - 450 <= pos_x <= width and 100 <= pos_y < 300:
                        fon.stop()
                        return True
                    if width - 450 <= pos_x <= width and 330 <= pos_y < 480:
                        rules()
                    if width - 450 <= pos_x <= width and 510 <= pos_y < 660:
                        settings()
                    if width - 450 <= pos_x <= width and 690 <= pos_y < 840:
                        exit_screen()

        pygame.display.flip()
        clock.tick(FPS)


def lose_screen():
    screen.fill('black')

    lose_win_x, lose_win_y = (width - 800) // 2, (height - 600) // 2

    font = pygame.font.SysFont('Rubik', 36)

    text = "press any key to continue"

    colors = [(255, 255, 255), (223, 223, 233), (191, 191, 191), (159, 159, 159), (127, 127, 127), (95, 95, 95),
              (63, 63, 63), (31, 31, 31), (0, 0, 0), (31, 31, 31), (63, 63, 63), (95, 95, 95), (127, 127, 127),
              (159, 159, 159), (191, 191, 191), (223, 223, 233)]

    i = 0

    fade_count = 1

    press_call_down = 150

    while True:
        fon.set_volume(volume / 100)

        screen.blit(tile_images['lose_screen'], (lose_win_x + 30, lose_win_y))

        if press_call_down == 0:
            rend_text = font.render(text, False, colors[i % 16])

            screen.blit(rend_text, (lose_win_x + 180, lose_win_y + 600))

        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                terminate()
            elif (ev.type == pygame.KEYDOWN or (ev.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_focused()))\
                    and press_call_down == 0:
                return

        if fade_count % 11 == 0:
            i += 1

        if press_call_down > 0:
            press_call_down -= 1

        fade_count += 1
        fade_count %= 11

        pygame.display.flip()
        clock.tick(FPS)


def win_screen():
    win_win_x, win_win_y = (width - 800) // 2, (height - 600) // 2

    text = "press any key to continue"

    win_text = 'Y O U   W O N !'

    colors = [(255, 255, 255), (223, 223, 233), (191, 191, 191), (159, 159, 159), (127, 127, 127), (95, 95, 95),
              (63, 63, 63), (31, 31, 31), (0, 0, 0), (31, 31, 31), (63, 63, 63), (95, 95, 95), (127, 127, 127),
              (159, 159, 159), (191, 191, 191), (223, 223, 233)]

    i = 0

    fade_count = 1

    press_call_down = 250

    call_down = 0

    while True:
        screen.fill('black')
        fon.set_volume(volume / 100)
        if call_down == 0:
            for _ in range(10):
                pos = [random.randint(50, width), random.randint(50, height)]

                create_particles(pos)

                call_down = 60

        font = pygame.font.SysFont('Rubik', 72)

        rend_text = font.render(win_text, True, (76, 255, 0))

        screen.blit(rend_text, (win_win_x + 180, win_win_y))

        if press_call_down == 0:
            font = pygame.font.SysFont('Rubik', 36)

            rend_text = font.render(text, False, colors[i % 16])

            screen.blit(rend_text, (win_win_x + 170, win_win_y + 600))

        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                terminate()
            elif (ev.type == pygame.KEYDOWN or (ev.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_focused())) \
                    and press_call_down == 0:
                return

        if fade_count % 11 == 0:
            i += 1

        fade_count += 1
        fade_count %= 11

        if call_down > 0:
            call_down -= 1

        if press_call_down > 0:
            press_call_down -= 1

        particles_gr.update()
        particles_gr.draw(screen)

        pygame.display.flip()
        clock.tick(FPS)


def pause_menu():
    pygame.mouse.set_visible(True)
    screen.fill('black')
    menu_x, menu_y = (width - 400) // 2, (height - 500) // 2

    while True:
        # аналогично start_screen, только со своими функциями
        fon.set_volume(volume / 100)
        screen.blit(tile_images['menu'], (menu_x, menu_y))
        screen.blit(tile_images['resume'], (menu_x + 100, menu_y + 150))
        screen.blit(tile_images['settings'], (menu_x + 100, menu_y + 250))
        screen.blit(tile_images['quit'], (menu_x + 100, menu_y + 350))

        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                terminate()
            elif ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_ESCAPE:
                    return True
            elif ev.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_focused():
                    pos_x, pos_y = pygame.mouse.get_pos()
                    if menu_x + 100 <= pos_x <= menu_x + 300 and menu_y + 150 <= pos_y < menu_y + 200:
                        return True
                    elif menu_x + 100 <= pos_x <= menu_x + 300 and menu_y + 250 <= pos_y < menu_y + 300:
                        settings()
                    elif menu_x + 100 <= pos_x <= menu_x + 300 and menu_y + 350 <= pos_y < menu_y + 400:
                        return False

        pygame.display.flip()
        clock.tick(FPS)


def rules():
    screen.fill('black')
    rules_win_x, rules_win_y = (width - 500) // 2, (height - 600) // 2
    # rules_text = ["ЗАСТАВКА", "",
    #               "Правила игры",
    #               "Если в правилах несколько строк,",
    #               "приходится выводить их построчно"]
    #
    # fon_im = pygame.transform.scale(load_image('fon.jpg'), (width, height))
    # screen.blit(fon_im, (0, 0))
    # font = pygame.font.Font(None, 30)
    # text_coord = 50
    # for lines in rules_text:
    #     string_rendered = font.render(lines, True, pygame.Color('white'))
    #     intro_rect = string_rendered.get_rect()
    #     text_coord += 10
    #     intro_rect.top = text_coord
    #     intro_rect.x = 10
    #     text_coord += intro_rect.height
    #     screen.blit(string_rendered, intro_rect)

    # на закомменченое не обращай внимания, это было в уроке, в игре оно роли не играет никакой
    # дальше здесь аналогично start_screen
    while True:
        screen.fill('black')

        fon.set_volume(volume / 100)
        screen.blit(tile_images['rules_win'], (rules_win_x, rules_win_y))
        screen.blit(tile_images['back'], (rules_win_x + 175, rules_win_y + 500))

        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                terminate()
            elif ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_ESCAPE:
                    return
            elif ev.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_focused():
                    pos_x, pos_y = pygame.mouse.get_pos()
                    if rules_win_x + 175 <= pos_x <= rules_win_x + 325 \
                            and rules_win_y + 500 <= pos_y < rules_win_y + 550:
                        return

        pygame.display.flip()
        clock.tick(FPS)


def settings():
    screen.fill('black')
    global FPS, volume
    pygame.mouse.set_visible(True)
    set_win_x, set_win_y = (width - 400) // 2, (height - 500) // 2
    # ставим шрифт чтобы писать фпс и громкость
    font = pygame.font.Font(None, 50)

    # рисуем окно настроек с изменяемыми громкостью и фпс, можешь потыкать на стрелочки посмотреть,
    # как меняется всё, чтобы понять суть
    # потом аналогичко start_screen
    while True:
        fon.set_volume(volume / 100)
        screen.blit(tile_images['settings_win'], (set_win_x, set_win_y))
        screen.blit(tile_images['volume'], (set_win_x + 100, set_win_y + 150))
        screen.blit(tile_images['vol_place'], (set_win_x + 150, set_win_y + 150))
        screen.blit(font.render(' ' + str(volume) + ' %', True, pygame.Color('#FF8C00')),
                    (set_win_x + 147, set_win_y + 160))
        if volume < 100:
            screen.blit(tile_images['arrow_up'], (set_win_x + 260, set_win_y + 150))
        if volume > 0:
            screen.blit(tile_images['arrow_down'], (set_win_x + 260, set_win_y + 175))
        screen.blit(tile_images['fps'], (set_win_x + 100, set_win_y + 250))
        screen.blit(tile_images['fps_place'], (set_win_x + 160, set_win_y + 250))
        screen.blit(font.render(' ' + str(FPS) + ' ', True, pygame.Color('#FF8C00')),
                    (set_win_x + 170, set_win_y + 260))
        if FPS < 120:
            screen.blit(tile_images['arrow_up'], (set_win_x + 260, set_win_y + 250))
        if FPS > 20:
            screen.blit(tile_images['arrow_down'], (set_win_x + 260, set_win_y + 275))
        screen.blit(tile_images['back'], (set_win_x + 125, set_win_y + 375))

        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                terminate()
            elif ev.type == pygame.KEYDOWN and ev.key == pygame.K_ESCAPE:
                return
            elif ev.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_focused():
                    pos_x, pos_y = pygame.mouse.get_pos()
                    if set_win_x + 125 <= pos_x <= set_win_x + 275 and set_win_y + 375 <= pos_y < set_win_y + 425:
                        return
                    if set_win_x + 260 <= pos_x <= set_win_x + 300 and set_win_y + 150 <= pos_y < set_win_y + 175:
                        if volume < 100:
                            volume += 10
                    if set_win_x + 260 <= pos_x <= set_win_x + 300 and set_win_y + 175 <= pos_y < set_win_y + 200:
                        if volume > 0:
                            volume -= 10
                    if set_win_x + 260 <= pos_x <= set_win_x + 300 and set_win_y + 250 <= pos_y < set_win_y + 275:
                        if FPS < 120:
                            FPS += 10
                    if set_win_x + 260 <= pos_x <= set_win_x + 300 and set_win_y + 275 <= pos_y < set_win_y + 300:
                        if FPS > 20:
                            FPS -= 10

        pygame.display.flip()
        clock.tick(FPS)


def generate_level(lvl):
    # считываем лвл и строим его, делая группы спрайтов для всех блоков
    new_player, x, y = None, None, None
    for y in range(len(lvl)):
        for x in range(len(lvl[y])):
            if lvl[y][x] == '.':
                Grass('empty', x, y)
            elif lvl[y][x] == '#':
                Block('wall', x, y)
            elif lvl[y][x] == '@':
                Grass('empty', x, y)
                new_player = Player(x, y)
            elif lvl[y][x] == '?':
                Grass('empty', x, y)
                mob = Mob(x, y)
    return new_player, x, y


def grass_choose():
    x = random.randint(0, 3)
    return grass_pack[x]


tile_width = tile_height = ceil = 50

grass_pack = ['grass.png', 'grass4.jpg', 'grass2.jpg', 'grass3.jpg']

# это словарь со всеми изображениями, которые доступны по их названию
tile_images = {
    # 'wall': load_image('box.png'),
    'wall': pygame.transform.scale(load_image('block2.jpg'), (ceil, ceil)),
    # 'empty': load_image('grass.png'),
    'empty': pygame.transform.scale(load_image(grass_choose()), (ceil, ceil)),
    'settings': load_image('gui/settings.png'),
    'quit': load_image('gui/quit.png'),
    'resume': load_image('gui/resume.png'),
    'volume': load_image('gui/volume.png'),
    'player': load_image('player_walk.png'),
    'back': load_image('gui/back.png'),
    'rules': load_image('gui/rules.png'),
    'menu': load_image('gui/menu.png'),
    'settings_win': load_image('gui/settings_win.png'),
    'arrow_up': load_image('gui/arrow_up.png'),
    'arrow_down': load_image('gui/arrow_down.png'),
    'fps': load_image('gui/fps.png'),
    'fps_place': load_image('gui/fps_place.png'),
    'vol_place': load_image('gui/vol_place.png'),
    'play': load_image('gui/play.png'),
    'settings_2': load_image('gui/settings_2.png'),
    'exit': load_image('gui/exit.png'),
    'rules_win': load_image('gui/rules_win.png'),
    'yes': load_image('gui/yes.png'),
    'no': load_image('gui/no.png'),
    'exit_win': load_image('gui/exit_win.png'),
    'idle': pygame.transform.scale(load_image('idle.png'), (ceil - 1, ceil - 1)),
    'lose_screen': load_image('lose_screen.png'),
    'star': load_image('star.png'),
    'water': load_image('water.jpg'),
    'fire': pygame.transform.scale(load_image('fire.png'), (20, 20)),
    'name': load_image('name.png')
}


def cut_sheet(sheet, columns, rows):
    # функция режущая пластину с colums на rows кадров на отдельные кадры и засовывает их в group_image
    rect = pygame.Rect(0, 0, sheet.get_width() // columns, sheet.get_height() // rows)

    frames = []
    for j in range(rows):
        row = []
        for i in range(columns):
            frame_location = (rect.w * i,  rect.h * j)
            row.append(pygame.transform.scale(sheet.subsurface(pygame.Rect(
                frame_location, rect.size)), (ceil - 1, ceil - 1)))
        frames.append(row)

    return frames


def create_particles(position):
    # количество создаваемых частиц
    particle_count = 25
    # возможные скорости
    numbers = range(-10, 10)
    for _ in range(particle_count):
        Particle(position, random.choice(numbers), random.choice(numbers))


def render_bar(pos, size, current, maxx, colors, render_text: bool = False, font=None):
    """Если render_text == True, то на полосе будудут отображены цифры
    Если True, то необходимо передать font - шрифт для отрисовки тектса"""
    if render_text and font is None:
        raise ValueError('Не передан font при render_text==True')

    w, h = size
    bar = pygame.surface.Surface((w, h), )
    k = current / maxx

    pygame.draw.rect(bar, colors['true'], [0, 0, w * k, h])
    pygame.draw.rect(bar, colors['missing'], [w * k, 0, w * (1 - k), h])
    pygame.draw.rect(bar, colors['borders'], bar.get_rect(), 2)

    # Рисуем
    w_bar, h_bar = bar.get_size()
    screen.blit(bar, (pos[0] - w_bar // 2, pos[1], w_bar, h_bar))

    if render_text:
        # Создаём текст
        text = f' {int(current)} / {int(maxx)} '
        text = font.render(text, True, (255, 255, 255), )

        w_txt, h_txt = text.get_size()
        screen.blit(text, (pos[0] - w_txt // 2, pos[1] - h_bar // 2 + h_txt // 2, w_txt, h_txt))


class Sprite(pygame.sprite.Sprite):
    def post_draw(self, surf, *args, **kwargs):
        pass

    def flip(self):
        self.image = pygame.transform.flip(self.image, True, False)


class SpriteGroup(pygame.sprite.Group):
    def post_draw(self, surf, *args, **kwargs):
        for spr in self.sprites():
            spr.post_draw(surf, *args, **kwargs)


class Block(Sprite):
    # класс стены, ничего особеного, просто добавляем её в свою группу и она будет огрождать
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(obstacles_gr, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Grass(Sprite):
    # класс травы, т.к. вместе с блоками у меня их ужить не получилось, разделил на 2 класса, травка просто лежит и всё
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(flours_gr, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Particle(pygame.sprite.Sprite):
    # сгенерируем частицы разного размера
    fire = [tile_images['star']]
    for scale in (20, 25, 30, 35, 40, 45, 50):
        fire.append(pygame.transform.scale(fire[0], (scale, scale)))

    def __init__(self, pos, dx, dy, fir=0):
        super().__init__(all_sprites, particles_gr)
        self.image = random.choice(self.fire)
        self.rect = self.image.get_rect()
        if fir:
            self.image = tile_images['fire']

        # у каждой частицы своя скорость — это вектор
        self.velocity = [dx, dy]
        # и свои координаты
        self.rect.x, self.rect.y = pos

        # гравитация будет одинаковой (значение константы)
        self.gravity = 1

    def update(self):
        # применяем гравитационный эффект:
        # движение с ускорением под действием гравитации
        self.velocity[1] += self.gravity
        # перемещаем частицу
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
        # убиваем, если частица ушла за экран
        if not self.rect.colliderect(0, 0, width, height):
            self.kill()


class Character:
    """Класс для объектов со здоровьем и маной,
    Смертный персонаж"""

    # Отрисовка полос здоровья и маны
    stat_font = pygame.font.SysFont('Arial Black', 12)

    bar_offset_health = (0, -34)
    bar_size_health = (128, 16)
    bar_colors_health = {
        'missing': (200, 0, 0),  # Цвет недостающего здоровья
        'true': (0, 200, 0),  # Цвет текущего здоровья
        'borders': (128, 128, 128),  # Рамки
    }

    bar_offset_mana = (0, -24)
    bar_size_mana = (100, 10)
    bar_colors_mana = {
        'missing': (20, 20, 20),  # Цвет недостающей маны
        'true': (0, 0, 200),  # Цвет текущей маны
        'borders': (128, 128, 128),  # Рамки
    }

    # Здоровье и мана
    mana: list  # Список из двух элементов: [текущее значение, максимальное]
    health: list  # Список из двух элементов: [текущее значение, максимальное]

    # Передвижение
    speed: int  # Необходимо указывать в дочерних классах
    velocity: np.array
    position: np.array

    # Направение взгяда
    facing: int  # -1 - смотрит влево, 1 - направо

    def __init__(self, pos: list,  health: list, mana: list, velocity=None):
        self.mana: list = mana
        self.health: list = health

        self.speed = self.__class__.speed
        self.velocity = np.array([0, 0], dtype=np.float32) if velocity is None else np.array(velocity, dtype=np.float32)
        self.position = np.array(pos, dtype=np.float32)

        self.facing = 1

    def update(self, pl):
        v = self.velocity
        self.position += v
        # print(self.velocity, 1)

        # Направление взгляда
        if v[0] > 0 and self.facing == -1 or v[0] < 0 and self.facing == 1:
            if hasattr(self, 'flip'):
                self.flip()
                self.facing = -self.facing

        # Проверка коллизии
        if hasattr(self, 'rect'):
            pass
            # block_hit_list = []
            # for block in obstacles_gr:
            #     if pygame.sprite.collide_rect(pl, block):
            #         block_hit_list.append(block)
            #
            # for block in block_hit_list:
            #     if self.velocity[0] > 0 and self.position[0] + ceil > block.rect.left:
            #         self.position[0] = block.rect.left - ceil
            #     elif self.velocity[0] < 0 and self.position[0] < block.rect.right:
            #         self.position[0] = block.rect.right
            #
            # block_hit_list = []
            # for block in obstacles_gr:
            #     if pygame.sprite.collide_rect(pl, block):
            #         block_hit_list.append(block)
            #
            # for block in block_hit_list:
            #     if self.velocity[1] > 0 and self.position[1] + ceil > block.rect.top:
            #         self.position[1] = block.rect.top - ceil
            #     elif self.velocity[1] < 0 and self.position[1] < block.rect.bottom:
            #         self.position[1] = block.rect.bottom
            # if collided:
            #     c = collided[0]
            #
            #     right = self.position[0] + self.rect[2]
            #     left = self.position[0]
            #     top = self.position[1] + self.rect[3]
            #     bottom = self.position[1]

        # Обнуляем скорость
        v = 0

        if hasattr(self, 'rect'):
            self.rect.x = int(self.position[0])
            self.rect.y = int(self.position[1])

    # STATS && PARAMS
    def get_damage(self, amount):
        self.health[0] -= amount
        if self.health[0] <= 0:
            self.health[0] = 0
            self.die()

    def spent_mana(self, amount):
        self.mana[0] -= amount

    def regen_mana(self, amount):
        self.mana[0] += amount
        if self.mana[0] > self.mana[1]:
            self.mana[0] = self.mana[1]

    def die(self):
        if hasattr(self, 'kill'):
            self.kill()

    def is_alive(self):
        return self.health[0] > 0

    # RENDER
    def render_health(self, pl, pos: list = None):
        """Если передан pos, то здоровье нарисуется в переданной точке
        Иначе он нарисуется чуть выше этого персонажа"""
        if pos is None:
            if hasattr(self, 'rect'):
                pos = pl.position
                pos = [pos[0] + self.rect.w // 2 + self.bar_offset_health[0], pos[1] + self.bar_offset_health[1]]
            else:
                return

        # Создаём полосу здоровья
        render_bar((pos[0] + 25, pos[1] + 40), self.bar_size_health, *self.health, colors=self.bar_colors_health,
                   render_text=True, font=self.stat_font)

    def render_mana(self, pl, pos: list = None):
        """Если передан pos, то здоровье нарисуется в переданной точке
                Иначе он нарисуется чуть выше этого персонажа"""
        if pos is None:
            if hasattr(self, 'rect'):
                pos = pl.position
                pos = [pos[0] + self.rect.w // 2 + self.bar_offset_mana[0],
                       pos[1] + self.bar_offset_mana[1] + self.bar_size_mana[1]]
            else:
                return

        render_bar((pos[0] + 25, pos[1] + 60), self.bar_size_health, *self.mana, colors=self.bar_colors_mana,
                   render_text=True, font=self.stat_font)


class Player(Sprite, Character):
    arrow_delay = 90

    mana_regen = 7 / 60

    speed = 5

    # класс игрока, самый сложный
    def __init__(self, pos_x, pos_y):
        super().__init__(player_gr, all_sprites)
        pos_x *= tile_width
        pos_y *= tile_height

        self.health = [250, 250]
        self.mana = [120, 120]
        Character.__init__(self, [pos_x, pos_y], self.health, self.mana)

        # группа с картинками, каждая из которых отдельный кадр из анимации бега
        self.walk_frames = cut_sheet(tile_images['player'], 8, 1)
        self.walk_time = 0
        self.walk_frames_delay = 5

        self.cur_image = 0
        self.cur_row = 0
        # сначала он стоит
        self.image = self.walk_frames[0][0]
        self.rect = self.image.get_rect()
        self.rect.x = pos_x
        self.rect.y = pos_y
        # заводим переменную проверки на взгляд влево и кол-во кадров, чтобы менять анимацию каждый 5ый кадр,
        # т.к. иначе при большом фпс он будет слишком быстро двигаться, а перемещаться будет медленно,
        # что не свойственно для таких движений
        self.left_sight = False
        self.frame_count = 0

        # arrow
        self.current_arrow_delay = 0
        self.arrow_delay = self.__class__.arrow_delay

    def walk(self, x, y):
        if x and y:
            m = ((self.speed ** 2) / 2) ** 0.5
            self.velocity = [x * m, y * m]
        else:
            self.velocity = [self.speed * x, self.speed * y]

        if hasattr(self, 'walk_time'):
            self.walk_time += 1

    def update(self):
        # ARROW
        if self.current_arrow_delay < self.arrow_delay:
            self.current_arrow_delay += 1
        else:
            self.regen_mana(self.mana_regen)

        self.rect.x += self.velocity[0]

        # UPDATE ANIMATION
        if any(self.velocity):
            if self.walk_time >= len(self.walk_frames[0]) * self.walk_frames_delay:
                self.walk_time = 0
            self.image = self.walk_frames[0][self.walk_time // self.walk_frames_delay]
        else:
            self.image = self.walk_frames[0][0]

        # коллизия
        block_hit_list = []
        for block in obstacles_gr:
            if pygame.sprite.collide_rect(self, block):
                block_hit_list.append(block)

        for block in block_hit_list:
            if self.velocity[0] > 0 and self.rect.right > block.rect.left:
                self.rect.right = block.rect.left - 1
            elif self.velocity[0] < 0 and self.rect.left < block.rect.right:
                self.rect.left = block.rect.right + 1

        self.rect.y += self.velocity[1]

        block_hit_list = []
        for block in obstacles_gr:
            if pygame.sprite.collide_rect(self, block):
                block_hit_list.append(block)

        for block in block_hit_list:
            if self.velocity[1] > 0 and self.rect.bottom > block.rect.top:
                self.rect.bottom = block.rect.top - 1

            elif self.velocity[1] < 0 and self.rect.top < block.rect.bottom:
                self.rect.top = block.rect.bottom + 1

        # PLAYER
        # Character.update(self, self)

        # Если смотрит влево, то поворачиваем картинку
        if self.facing == -1 and self.velocity[0] > 0 or self.facing == 1 and self.velocity[0] < 0:
            self.flip()

        # Character.render_mana(self, self, [self.rect.x, self.rect.y])
        # Character.render_health(self, self, [self.rect.x, self.rect.y])

    def post_draw(self, surf, *args, **kwargs):
        Character.render_health(self, self, [self.rect.x, self.rect.y])
        Character.render_mana(self, self, [self.rect.x, self.rect.y])

    def shoot_arrow(self):
        if self.current_arrow_delay < self.arrow_delay:
            return

        ARROW_SPEED = 10

        # VELOCITY
        if not any(self.velocity):
            velocity = [ARROW_SPEED * self.facing, 0]

        else:
            velocity = [ARROW_SPEED, ARROW_SPEED]
            if self.velocity[0] < 0:
                velocity[0] *= -1
            elif not self.velocity[0]:
                velocity[0] = 0

            if self.velocity[1] < 0:
                velocity[1] *= -1
            elif not self.velocity[1]:
                velocity[1] = 0

        #
        if player.mana[0] >= 20:
            Arrow(arrow_gr, self.rect.x, self.rect.y, velocity)
            self.current_arrow_delay = 0
            player.mana[0] -= 20


class Mob(Sprite, Character, PatrolAI):
    image = tile_images['idle']

    mana_regen = 11 / 50

    speed = 5

    def __init__(self, pos_x, pos_y):
        super().__init__(enemies_gr, all_sprites)
        PatrolAI.__init__(self, pygame.rect.Rect(0, 0, 400, 400), )

        pos_x *= tile_width
        pos_y *= tile_height

        self.health = [200, 200]
        self.mana = [0, 500]

        Character.__init__(self, [pos_x, pos_y], self.health, self.mana)

        self.rect = self.image.get_rect()
        self.rect.x = pos_x
        self.rect.y = pos_y

        self.velocity = [0, 0]

        self.damage = 20

        self.call_down = 0

        self.walk_call_down = 0

        self.facing = 1

    def update(self, *args, **kwargs) -> None:
        # PatrolAI.update(self, self)

        if pygame.sprite.collide_mask(self, player):
            # Particle((self.rect.x, self.rect.y), 5, 0, 1)
            # Particle((self.rect.x, self.rect.y), -5, 0, 1)
            # Particle((self.rect.x, self.rect.y), 0, -5, 1)
            # Particle((self.rect.x, self.rect.y), 0, 5, 1)
            # Particle((self.rect.x, self.rect.y), 3.5, 3.5, 1)
            # Particle((self.rect.x, self.rect.y), -3.5, 3.5, 1)
            # Particle((self.rect.x, self.rect.y), -3.5, -3.5, 1)
            # Particle((self.rect.x, self.rect.y), 3.5, -3.5, 1)
            self.attack()

        self.update_move()

        if self.walk_call_down > 0:
            self.velocity = [0, 0]

        self.rect.x += self.velocity[0] * 2

        block_hit_list = []

        for block in obstacles_gr:
            if pygame.sprite.collide_rect(self, block):
                block_hit_list.append(block)

        for block in block_hit_list:
            if self.velocity[0] > 0 and self.rect.right > block.rect.left:
                self.rect.right = block.rect.left - 1
            elif self.velocity[0] < 0 and self.rect.left < block.rect.right:
                self.rect.left = block.rect.right + 1

        self.rect.y += self.velocity[1] * 2

        block_hit_list = []

        for block in obstacles_gr:
            if pygame.sprite.collide_rect(self, block):
                block_hit_list.append(block)

        for block in block_hit_list:
            if self.velocity[1] > 0 and self.rect.bottom > block.rect.top:
                self.rect.bottom = block.rect.top - 1

            elif self.velocity[1] < 0 and self.rect.top < block.rect.bottom:
                self.rect.top = block.rect.bottom + 1

        # Character.update(self, self)

        if self.velocity[0] > 0 and self.facing == -1 or self.velocity[0] < 0 and self.facing == 1:
            if hasattr(self, 'flip'):
                self.flip()
                self.facing = -self.facing

        self.regen_mana(self.mana_regen)

        if self.call_down > 0:
            self.call_down -= 1

        if self.walk_call_down > 0:
            self.walk_call_down -= 1

    def die(self):
        super().die()

    def attack(self):
        if self.mana[0] >= 50:
            if self.call_down == 0:
                self.mana[0] -= 50
                player.get_damage(self.damage)
                self.call_down = 60
                self.walk_call_down = 20

    def post_draw(self, surf, *args, **kwargs):
        Character.render_health(self, self, [self.rect.x, self.rect.y])
        Character.render_mana(self, self, [self.rect.x, self.rect.y])

    def update_move(self):
        x, y = player.rect.x, player.rect.y
        if x < self.rect.x:
            if y < self.rect.y:
                self.velocity = [-1, -1]
            elif y > self.rect.y:
                self.velocity = [-1, 1]
            else:
                self.velocity = [-1, 0]
        elif x > self.rect.x:
            if y < self.rect.y:
                self.velocity = [1, -1]
            elif y > self.rect.y:
                self.velocity = [1, 1]
            else:
                self.velocity = [1, 0]
        else:
            if y < self.rect.y:
                self.velocity = [0, -1]
            elif y > self.rect.y:
                self.velocity = [0, 1]
            else:
                self.velocity = [0, 0]


class Projectile(Sprite):
    """Класс базового снаряда"""

    def __init__(self, gr, x, y, velocity, size=(20, 20)):
        super().__init__(all_sprites, gr)
        self.rect = pygame.rect.Rect(x, y, *size)
        self.velocity = np.array(velocity, dtype=np.float32)

    def update(self, *args, **kwargs) -> None:
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]

    def post_draw(self, surf, *args, **kwargs):
        """Писать отрисовку снаряда тут"""
        pass


class Arrow(Projectile):
    def __init__(self, gr, x, y, velocity, size=(20, 20), damage=20):
        super().__init__(gr, x, y, velocity, size)
        self.size = size
        self.mana_cost = 30
        self.damage = damage

    def post_draw(self, surf, *args, **kwargs):
        pygame.draw.circle(surf, (255, 255, 255), [self.rect.x - self.velocity[0] * 2,
                                                   self.rect.y - self.velocity[1] * 2], self.size[0] // 3)

        pygame.draw.circle(surf, (255, 255, 255), [self.rect.x - self.velocity[0],
                                                   self.rect.y - self.velocity[1]], self.size[0] // 2.5)

        pygame.draw.circle(surf, (255, 200, 200), [self.rect.x, self.rect.y], self.size[0] // 2)

    def update(self, *args, **kwargs):
        super().update(*args, **kwargs)

        collide = pygame.sprite.spritecollide(self, enemies_gr, False)
        if collide:
            for x in collide:
                x.get_damage(self.damage)
            self.kill()

        collide = pygame.sprite.spritecollide(self, obstacles_gr, False)
        if collide:
            self.kill()


class Camera:
    def __init__(self):
        self.dx = 0
        self.dy = 0

    def move_by(self, x, y):
        self.dx += x
        self.dy += y

    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy
        if hasattr(obj, 'position'):
            obj.position[0] += self.dx
            obj.position[1] += self.dy

    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - width // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - height // 2)


def update_hero_movement(keys):
    x, y = 0, 0
    for k in move_direction_keys.keys():
        if keys[k]:
            x += move_direction_keys[k][0]
            y += move_direction_keys[k][1]
    player.walk(x, y)


if __name__ == '__main__':
    # НАСТРОЙКА, СОЗДАНИЕ ОКНА
    pygame.mixer.pre_init(44100, -16, 1, 512)
    pygame.init()
    width, height = 1400, 900
    size = width, height
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('Game')
    pygame.mouse.set_visible(True)

    # НАСТРОЙКИ
    fon = pygame.mixer.Sound(load_sound('Happy Walk.mp3'))
    FPS = 60
    volume = 60

    fs = 0
    ws = 0

    for line in load_save():
        line = line.split()
        if line[0] == 'fps':
            FPS = int(line[1])
        elif line[0] == 'volume':
            volume = int(line[1])

    clock = pygame.time.Clock()

    # ОСНОВНОЙ GAME LOOP
    running = False
    while True:
        if start_screen():
            # КНОПКИ
            move_direction_keys = {
                pygame.K_w: (0.0, -1.0),
                pygame.K_s: (0.0, 1.0),
                pygame.K_a: (-1.0, 0.0),
                pygame.K_d: (1.0, 0.0)
            }
            keys_pressed = {
                pygame.K_w: False,
                pygame.K_s: False,
                pygame.K_a: False,
                pygame.K_d: False
            }

            running = True
            camera = Camera()

            # ГРУППЫ СПРАЙТОВ
            # игра
            all_sprites = SpriteGroup()
            obstacles_gr = SpriteGroup()
            flours_gr = SpriteGroup()
            player_gr = SpriteGroup()
            enemies_gr = SpriteGroup()
            arrow_gr = SpriteGroup()
            # меню
            pause_menu_buttons = SpriteGroup()
            settings_buttons = SpriteGroup()
            particles_gr = SpriteGroup()

            # ЗАГРУЖАЕМ УРОВЕНЬ
            player, level_x, level_y = generate_level(load_level('map.txt'))
            pygame.mouse.set_visible(False)
            fs = 0

        while running:
            if player.health[0] <= 0:
                fs = 1
                break

            if len(enemies_gr) == 0:
                ws = 1
                break

            screen.blit(tile_images['water'], (0, 0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()

                elif event.type == pygame.KEYDOWN:
                    key = event.key
                    if key in keys_pressed.keys():
                        keys_pressed[key] = True

                    if key == pygame.K_q:
                        player.shoot_arrow()

                    if event.key == pygame.K_ESCAPE:
                        running = pause_menu()

                elif event.type == pygame.KEYUP:
                    key = event.key
                    if key in keys_pressed.keys():
                        keys_pressed[key] = False

            # UPDATE
            update_hero_movement(keys_pressed)
            all_sprites.update()
            camera.update(player)
            for sprite in all_sprites:
                camera.apply(sprite)

            # DRAW
            flours_gr.draw(screen)
            obstacles_gr.draw(screen)
            enemies_gr.draw(screen)
            player_gr.draw(screen)

            # POST DRAW
            all_sprites.post_draw(screen)
            arrow_gr.post_draw(screen)

            # FLIP FRAME
            pygame.display.flip()
            clock.tick(FPS)

        if fs:
            fs = 0
            lose_screen()

        if ws:
            ws = 0
            win_screen()
