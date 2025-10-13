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
