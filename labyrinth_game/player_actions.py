def show_inventory(game_state):
    """Отображение инвентаря игрока"""
    inventory = game_state['player_inventory']

    if inventory:
        print("Ваш инвентарь:", ", ".join(inventory))
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

    # Проверяем есть ли выход в указанном направлении
    if direction in rooms[current_room]['exits']:
        # Перемещаем игрока
        game_state['current_room'] = rooms[current_room]['exits'][direction]
        game_state['steps_taken'] += 1

        print(f"Вы переместились {direction} в {game_state['current_room']}.")

        # Вызываем случайное событие после перемещения
        from .utils import random_event
        random_event(game_state)

        return True
    else:
        print(f"Невозможно переместиться {direction}.")
        return False

