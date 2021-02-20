import os
import sys
import pygame


def load_sound(name):
    # здесь мы проверяем если ли нужный нам звукойвой файл: если есть, то возвращаем полное его название с директориями,
    # иначе ругаемся
    fullname = os.path.join('data/sounds', name)
    if not os.path.isfile(fullname):
        print(f"Файл с аудиозаписью '{fullname}' не найден")
        sys.exit()

    return fullname


def load_image(name):
    # здесь мы проверяем если ли нужная нам картинка: если есть, то загружаем, иначе ругаемся
    fullname = os.path.join('data\images', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()

    image = pygame.image.load(fullname)
    return image


def load_level(filename):
    # здесь мы проверяем если ли нужный нам файл с уровнем: если есть то загружаем, иначе ругаемся
    filename = os.path.join("data/levels", filename)
    with open(filename, 'r') as mapFile:
        level_map = [ln.strip() for ln in mapFile]
    max_width = max(map(len, level_map))
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


def save_changes(FPS, VOLUME):
    # здесь мы записываем в файл значения фпс и громкости, чтобы они остались на след вход
    save = open(open_save('save.txt'), mode='w', encoding='utf-8')
    save.seek(0)
    save.write('fps ' + str(FPS))
    save.write('\n')
    save.write('volume ' + str(VOLUME))
    save.close()


def load_save():
    # здесь мы загружаем сохранения с последнего входа в игру (фпс и громкость)
    save = open(open_save('save.txt'), mode='r', encoding='utf-8')
    x = save.read().split('\n')
    save.close()
    return x


def open_save(name):
    # здесь мы проверяем если ли нужный нам файл с сохранёными значениями фпс и громкости: если есть, то загружаем,
    # иначе ругаемся
    fullname = os.path.join('data/saves', name)
    if not os.path.isfile(fullname):
        print(f"Файл с сохранением '{fullname}' не найден")
        sys.exit()

    return fullname
