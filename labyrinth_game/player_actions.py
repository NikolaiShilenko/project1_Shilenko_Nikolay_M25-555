def show_inventory(game_state):
    inventory = game_state['player_inventory']

    if inventory:
        items_display = []
        for item, count in inventory.items():
            if item == 'coin' and count > 1:
                items_display.append(f"{count}x {item}")
            else:
                items_display.append(item)
        print("Ваш инвентарь:", ", ".join(items_display))
    else:
        print("Ваш инвентарь пуст")


def get_input(prompt="> "):
    """Получение ввода от пользователя с обработкой ошибок"""
    try:
        return input(prompt)
    except (KeyboardInterrupt, EOFError):
        print("\nВыход из игры.")
        return "quit"


def move_player(game_state, direction):
    """Перемещение игрока в указанном направлении

    Args:
        game_state (dict): текущее состояние игры
        direction (str): направление движения

    Returns:
        bool: успешно ли выполнено перемещение
    """
    current_room = game_state['current_room']
    rooms = game_state['rooms']
    target_room = rooms[current_room]['exits'].get(direction)

    # Проверяем есть ли выход в указанном направлении
    if target_room:
        # Проверяем переход в treasure_room
        if target_room == 'treasure_room':
            if 'rusty_key' in game_state['player_inventory']:
                print("Вы используете найденный ключ, чтобы открыть путь к сокровищу.")
                game_state['current_room'] = target_room
                game_state['steps_taken'] += 1

                # Вызываем случайное событие после перемещения
                from .utils import random_event
                random_event(game_state)
                return True
            else:
                print("Дверь заперта. Нужен ключ, чтобы пройти дальше.")
                return False

        # Обычное перемещение для других комнат
        game_state['current_room'] = target_room
        game_state['steps_taken'] += 1
        print(f"Вы переместились {direction} в {target_room}.")

        # Вызываем случайное событие после перемещения
        from .utils import random_event
        random_event(game_state)
        return True
    else:
        print(f"Невозможно переместиться {direction}.")
        return False


def pick_up_item(game_state, item_name):
    """Подбор предмета из текущей комнаты"""
    current_room = game_state['current_room']
    room_items = game_state['rooms'][current_room]['items']

    # Запрещаем подбор сундука
    if item_name == 'treasure_chest':
        print("Вы не можете поднять сундук, он слишком тяжелый.")
        return False

    if item_name in room_items:
        # Для монет используем счетчик, остальные предметы уникальны
        inventory = game_state['player_inventory']
        if item_name == 'coin':
            if 'coin' in inventory:
                inventory['coin'] += 1
            else:
                inventory['coin'] = 1
        else:
            inventory[item_name] = 1

        game_state['item_locations'][item_name] = current_room
        room_items.remove(item_name)
        print(f"Вы подобрали: {item_name}")
        return True
    else:
        print(f"Предмет '{item_name}' не найден в этой комнате.")
        return False


def use_item(game_state, item_name):
    """Использование предмета из инвентаря"""
    inventory = game_state['player_inventory']

    if item_name not in inventory:
        print(f"У вас нет предмета '{item_name}'.")
        return False

    match item_name:
        case "torch":
            print("Вы зажигаете факел. Стало светлее и уютнее.")

        case "sword":
            print("Вы размахиваете мечом. Чувствуете себя увереннее.")

        case "bronze_box":
            print("Вы открываете бронзовую шкатулку.")
            if 'rusty_key' not in inventory:
                inventory['rusty_key'] = 1
                print("Внутри вы находите rusty_key!")
            else:
                print("Шкатулка пуста.")

        case _:
            print(f"Вы не знаете, как использовать {item_name}.")
            return False

    return True
