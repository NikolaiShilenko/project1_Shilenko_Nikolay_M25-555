#!/usr/bin/env python3

from .constants import COMMANDS, ROOMS
from .player_actions import get_input, move_player, show_inventory
from .utils import attempt_open_treasure, describe_current_room, solve_puzzle

# Состояние игрока и игры
game_state = {
    'player_inventory': {},
    'current_room': 'entrance',
    'game_over': False,
    'steps_taken': 0,
    'rooms': ROOMS,
    'item_locations': {}
}


def show_help():
    """Показать справку по командам"""
    print("\n=== ДОСТУПНЫЕ КОМАНДЫ ===")
    for command, description in COMMANDS.items():
        print(f"{command:<16} - {description}")
    print("========================\n")


def process_command(command, game_state):
    """Обработка введенной команды"""
    command = command.strip().lower()

    if command in ['выход', 'quit']:
        game_state['game_over'] = True
        print("Спасибо за игру!")
        return

    elif command in ['инвентарь', 'inventory']:
        show_inventory(game_state)

    elif command in ['помощь', 'help']:
        show_help()

    elif command in ['север', 'north', 'юг', 'south',
                     'запад', 'west', 'восток', 'east']:
        direction_map = {
            'север': 'north', 'north': 'north',
            'юг': 'south', 'south': 'south',
            'запад': 'west', 'west': 'west',
            'восток': 'east', 'east': 'east'
        }
        move_player(game_state, direction_map[command])

    elif command in ['решить', 'solve']:
        if game_state['current_room'] == 'treasure_room':
            attempt_open_treasure(game_state)
        else:
            solve_puzzle(game_state)

    elif command.startswith('взять ') or command.startswith('take '):
        item = command.split(' ', 1)[1]
        from .player_actions import pick_up_item
        pick_up_item(game_state, item)

    else:
        print("Неизвестная команда. Введите 'помощь' для списка команд.")


def main():
    """Основной игровой цикл"""
    print("Добро пожаловать в Лабиринт сокровищ!")
    describe_current_room(game_state)

    while not game_state['game_over']:
        command = get_input("\nВведите команду: ")
        process_command(command, game_state)

        # Показываем описание комнаты после каждого действия (кроме выхода)
        if not game_state['game_over']:
            describe_current_room(game_state)


if __name__ == "__main__":
    main()
