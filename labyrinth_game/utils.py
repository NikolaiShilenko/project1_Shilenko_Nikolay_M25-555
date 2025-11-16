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


def trigger_trap(game_state):
    """Активация ловушки с негативными последствиями для игрока

    Args:
        game_state (dict): текущее состояние игры
    """
    print("Ловушка активирована! Пол стал дрожать...")

    inventory = game_state['player_inventory']

    # Проверяем есть ли предметы в инвентаре
    if inventory:
        # Выбираем случайный предмет для удаления
        random_index = pseudo_random(game_state['steps_taken'], len(inventory))
        lost_item = inventory.pop(random_index)
        print(f"Из вашего инвентаря выпал и потерялся: {lost_item}")

    else:
        # Инвентарь пуст - игрок получает "урон"
        damage_chance = pseudo_random(game_state['steps_taken'], 10)

        if damage_chance < 3:  # 30% шанс проигрыша
            print("Каменная плита с грохотом обрушивается на вас! Игра окончена.")
            game_state['game_over'] = True
        else:
            print("Вам удалось увернуться от падающих камней! Вы уцелели.")


def random_event(game_state):
    """Случайные события при перемещении игрока

    Args:
        game_state (dict): текущее состояние игры
    """
    # Проверяем, произойдет ли событие (10% шанс)
    event_chance = pseudo_random(game_state['steps_taken'], 10)
    if event_chance != 0:
        return  # Событие не происходит

    # Выбираем тип события
    event_type = pseudo_random(game_state['steps_taken'] + 1, 3)
    current_room = game_state['current_room']

    if event_type == 0:
        # Сценарий 1: Находка
        print("Вы заметили что-то блестящее на полу... Это монетка!")
        game_state['rooms'][current_room]['items'].append('coin')

    elif event_type == 1:
        # Сценарий 2: Испуг
        print("Вы слышите подозрительный шорох из темноты...")
        if 'sword' in game_state['player_inventory']:
            print("Вы достаёте меч, и существо ретируется!")
        else:
            print("Шорох усиливается... Вам стало не по себе.")

    elif event_type == 2:
        # Сценарий 3: Срабатывание ловушки
        if (current_room == 'trap_room' and
                'torch' not in game_state['player_inventory']):
            print("Вы слышите щелчок под ногой... Это ловушка!")
            trigger_trap(game_state)
        else:
            print("Показалось, что что-то щёлкнуло, но ничего не произошло.")

