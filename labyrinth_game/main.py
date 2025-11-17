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


def process_command(game_state, command):
    """Обработка введенной команды с использованием match/case"""
    command = command.strip().lower()
    parts = command.split()  # Разделяем команду на части
    main_command = parts[0] if parts else ""
    argument = parts[1] if len(parts) > 1 else ""

    match main_command:
        case "выход" | "quit" | "exit":
            game_state['game_over'] = True
            print("Спасибо за игру!")

        case "инвентарь" | "inventory":
            show_inventory(game_state)

        case "помощь" | "help":
            show_help()

        case "осмотр" | "look":
            describe_current_room(game_state)

        case "взять" | "take":
            if argument:
                from .player_actions import pick_up_item
                pick_up_item(game_state, argument)
            else:
                print("Укажите предмет для подбора: взять <предмет>")

        case "использовать" | "use":
            if argument:
                from .player_actions import use_item
                use_item(game_state, argument)
            else:
                print("Укажите предмет для использования: использовать <предмет>")

        case "идти" | "go":
            direction_map = {
                'север': 'north', 'north': 'north',
                'юг': 'south', 'south': 'south',
                'запад': 'west', 'west': 'west',
                'восток': 'east', 'east': 'east'
            }
            if argument in direction_map:
                move_player(game_state, direction_map[argument])
            else:
                print(f"Неизвестное направление: {argument}")

        case _:
            if main_command in ['север', 'north', 'юг', 'south',
                                'запад', 'west', 'восток', 'east']:
                direction_map = {
                    'север': 'north', 'north': 'north',
                    'юг': 'south', 'south': 'south',
                    'запад': 'west', 'west': 'west',
                    'восток': 'east', 'east': 'east'
                }
                move_player(game_state, direction_map[main_command])
            elif main_command in ['решить', 'solve']:
                if game_state['current_room'] == 'treasure_room':
                    attempt_open_treasure(game_state)
                else:
                    solve_puzzle(game_state)
            else:
                print("Неизвестная команда. Введите 'помощь' для списка команд.")


def main():
    """Основной игровой цикл"""
    print("Добро пожаловать в Лабиринт сокровищ!")
    describe_current_room(game_state)

    while not game_state['game_over']:
        command = get_input("\nВведите команду: ")
        process_command(game_state, command)


if __name__ == "__main__":
    main()
