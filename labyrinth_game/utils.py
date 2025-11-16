import math

from .constants import ROOMS


def describe_current_room(game_state):
    """Описание текущей комнаты игрока"""
    # Получаем данные о текущей комнате из ROOMS
    current_room_name = game_state['current_room']
    room_data = ROOMS[current_room_name]

    # Выводим название комнаты в верхнем регистре
    print(f"== {current_room_name.upper()} ==")

    # Выводим описание комнаты
    print(room_data['description'])

    # Выводим список предметов, если они есть
    if room_data['items']:
        print("Заметные предметы:", ", ".join(room_data['items']))

    # Выводим доступные выходы
    if room_data['exits']:
        exits = [
            f"{direction} ({room})"
            for direction, room in room_data['exits'].items()
        ]
        print("Выходы:", ", ".join(exits))

    # Сообщение о загадке, если она есть
    if room_data['puzzle'] is not None:
        print("Кажется, здесь есть загадка (используйте команду solve).")


def pseudo_random(seed, modulo):
    """Генератор псевдослучайных чисел на основе синуса

    Args:
        seed (int): начальное значение (например, количество шагов)
        modulo (int): верхняя граница диапазона [0, modulo)

    Returns:
        int: псевдослучайное число в диапазоне [0, modulo)
    """
    # Вычисляем синус от seed умноженного на большое число
    sin_value = math.sin(seed * 12.9898)

    # Умножаем на другое большое число для "размазывания" значений
    multiplied = sin_value * 43758.5453

    # Получаем дробную часть
    fractional_part = multiplied - math.floor(multiplied)

    # Приводим к нужному диапазону и возвращаем целое число
    return math.floor(fractional_part * modulo)


