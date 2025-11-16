#!/usr/bin/env python3

from .constants import ROOMS
from .player_actions import get_input, move_player, show_inventory
from .utils import describe_current_room

# Состояние игрока и игры
game_state = {
    'player_inventory': [],  # Инвентарь игрока
    'current_room': 'entrance',  # Текущая комната
    'game_over': False,  # Флаг окончания игры
    'steps_taken': 0,  # Количество шагов
    'rooms': ROOMS  # Добавляем комнаты в game_state
}


def main():
    """Основной игровой цикл"""
    print("Добро пожаловать в Лабиринт сокровищ!")
    describe_current_room(game_state)

    while not game_state['game_over']:
        command = get_input("\nВведите команду: ").strip().lower()

        if command == "quit":
            game_state['game_over'] = True
            print("Спасибо за игру!")
        elif command == 'инвентарь':
            show_inventory(game_state)
        elif command in ['север', 'юг', 'запад', 'восток']:
            # Преобразуем русские направления в английские
            direction_map = {'север': 'north', 'юг': 'south',
                             'запад': 'west', 'восток': 'east'}
            move_player(game_state, direction_map[command])
            describe_current_room(game_state)
        else:
            print("Неизвестная команда. Попробуйте 'инвентарь', "
                  "'выход' или направление")


if __name__ == "__main__":
    main()

