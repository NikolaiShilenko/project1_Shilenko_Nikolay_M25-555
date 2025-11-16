import math

from .constants import (
    EVENT_FIND_ITEM,
    EVENT_PROBABILITY,
    EVENT_SCARE,
    EVENT_TRAP,
    EVENT_TYPES_COUNT,
    MAX_DAMAGE_CHANCE,
    PSEUDO_RANDOM_MULTIPLIER_1,
    PSEUDO_RANDOM_MULTIPLIER_2,
    ROOMS,
    TRAP_DAMAGE_PROBABILITY,
)


def describe_current_room(game_state):
    """Описание текущей комнаты игрока"""
    current_room_name = game_state['current_room']
    room_data = ROOMS[current_room_name]

    print(f"== {current_room_name.upper()} ==")
    print(room_data['description'])

    if room_data['items']:
        print("Заметные предметы:", ", ".join(room_data['items']))

    if room_data['exits']:
        exits = [
            f"{direction} ({room})"
            for direction, room in room_data['exits'].items()
        ]
        print("Выходы:", ", ".join(exits))

    if room_data['puzzle'] is not None:
        print("Кажется, здесь есть загадка (используйте команду solve).")


def pseudo_random(seed, modulo):
    """Генератор псевдослучайных чисел на основе синуса"""
    sin_value = math.sin(seed * PSEUDO_RANDOM_MULTIPLIER_1)
    multiplied = sin_value * PSEUDO_RANDOM_MULTIPLIER_2
    fractional_part = multiplied - math.floor(multiplied)
    return math.floor(fractional_part * modulo)


def trigger_trap(game_state):
    """Активация ловушки с негативными последствиями для игрока"""
    print("Ловушка активирована! Пол стал дрожать...")

    inventory = game_state['player_inventory']

    if inventory:
        items_list = list(inventory.keys())
        random_index = pseudo_random(game_state['steps_taken'], len(items_list))
        lost_item = items_list[random_index]

        if lost_item == 'coin' and inventory['coin'] > 1:
            inventory['coin'] -= 1
            print("Из вашего инвентаря выпала одна монетка!")
        else:
            del inventory[lost_item]
            print(f"Из вашего инвентаря выпал и потерялся: {lost_item}")

        original_room = game_state['item_locations'].get(lost_item)
        if original_room:
            game_state['rooms'][original_room]['items'].append(lost_item)
            print(f"Предмет {lost_item} вернулся в {original_room}.")

    else:
        damage_chance = pseudo_random(game_state['steps_taken'], MAX_DAMAGE_CHANCE)

        if damage_chance < TRAP_DAMAGE_PROBABILITY:
            print("Каменная плита обрушивается на вас! Игра окончена.")
            game_state['game_over'] = True
        else:
            print("Вам удалось увернуться от падающих камней! Вы уцелели.")


def random_event(game_state):
    """Случайные события при перемещении игрока"""
    event_chance = pseudo_random(game_state['steps_taken'], EVENT_PROBABILITY)
    if event_chance != 0:
        return

    event_type = pseudo_random(game_state['steps_taken'] + 1, EVENT_TYPES_COUNT)
    current_room = game_state['current_room']

    if event_type == EVENT_FIND_ITEM:
        print("Вы заметили что-то блестящее на полу... Это монетка!")
        game_state['rooms'][current_room]['items'].append('coin')

    elif event_type == EVENT_SCARE:
        print("Вы слышите подозрительный шорох из темноты...")
        if 'sword' in game_state['player_inventory']:
            print("Вы достаёте меч, и существо ретируется!")
        else:
            print("Шорох усиливается... Вам стало не по себе.")

    elif event_type == EVENT_TRAP:
        if (current_room == 'trap_room' and
                'torch' not in game_state['player_inventory']):
            print("Вы слышите щелчок под ногой... Это ловушка!")
            trigger_trap(game_state)
        else:
            print("Показалось, что что-то щёлкнуло, но ничего не произошло.")


def normalize_answer(answer):
    """Нормализация ответа - удаление пробелов и приведение к нижнему регистру"""
    return ''.join(answer.strip().lower().split())


def solve_puzzle(game_state):
    """Решение загадки в текущей комнате"""
    current_room_name = game_state['current_room']
    room_data = game_state['rooms'][current_room_name]

    if room_data['puzzle'] is None:
        print("Здесь нет загадки для решения.")
        return

    puzzle_text = room_data['puzzle'][0]
    correct_answer = room_data['puzzle'][1]

    all_answers = [correct_answer]
    if len(room_data['puzzle']) > 2:
        all_answers.extend(room_data['puzzle'][2])

    normalized_answers = [normalize_answer(ans) for ans in all_answers]

    print(f"Загадка: {puzzle_text}")
    user_answer = input("Ваш ответ: ").strip()

    normalized_user_answer = normalize_answer(user_answer)

    if normalized_user_answer in normalized_answers:
        print("Правильно! Загадка решена.")

        inventory = game_state['player_inventory']
        if current_room_name == 'hall':
            print("Пьедестал открывается! Вы получаете ключ от сокровищ.")
            inventory['treasure_key'] = 1
        elif current_room_name == 'trap_room':
            print("Плиты перестали двигаться! Теперь безопасно.")
        elif current_room_name == 'library':
            print("Свиток раскрывается! Вы находите скрытый отсек с картой.")
            inventory['secret_map'] = 1
        elif current_room_name == 'observatory':
            print("Телескоп настраивается! Видите звезды лучше.")
            inventory['enhanced_telescope'] = 1

        room_data['puzzle'] = None

    else:
        print("Неправильный ответ. Попробуйте еще раз.")

        if current_room_name == 'trap_room':
            print("Ловушка активируется!")
            trigger_trap(game_state)


def attempt_open_treasure(game_state):
    """Попытка открыть сундук с сокровищами"""
    if game_state['current_room'] != 'treasure_room':
        print("Здесь нет сундука с сокровищами.")
        return

    inventory = game_state['player_inventory']
    current_room = game_state['rooms']['treasure_room']

    if 'treasure_key' in inventory:
        print("Вы применяете ключ, и замок щёлкает. Сундук открыт!")
        current_room['items'].remove('treasure_chest')
        print("В сундуке сокровище! Вы победили!")
        game_state['game_over'] = True
        return

    print("Сундук заперт. Нет ключа, но есть кодовый замок. Ввести код? (да/нет)")
    choice = input("> ").strip().lower()

    if choice == 'да':
        puzzle_text = current_room['puzzle'][0]
        print(f"Код зашифрован в загадке: {puzzle_text}")
        print("Введите код:")
        code = input("> ").strip()

        correct_code = current_room['puzzle'][1]
        alternative_codes = current_room['puzzle'][2] \
            if len(current_room['puzzle']) > 2 \
            else []

        if code == correct_code or code in alternative_codes:
            print("Замок щёлкает! Сундук открыт!")
            print("В сундуке сокровище! Вы победили!")
            current_room['items'].remove('treasure_chest')
            game_state['game_over'] = True
        else:
            print("Неверный код. Замок не открылся.")
    else:
        print("Вы отступаете от сундука.")
