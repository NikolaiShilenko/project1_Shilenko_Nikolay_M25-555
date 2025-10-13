#!/usr/bin/env python3

from .constants import ROOMS
from .player_actions import get_input, show_inventory
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

    # Описываем стартовую комнату
    describe_current_room(game_state)

    # Основной игровой цикл
    while not game_state['game_over']:
        # Считываем команду от пользователя
        command = get_input("\nВведите команду: ").strip().lower()

        if command == "quit":
            game_state['game_over'] = True
            print("Спасибо за игру!")
        elif command == 'инвентарь':
            show_inventory(game_state)
        elif command == 'выход':
            game_state['game_over'] = True
            print("Спасибо за игру!")
        else:
            print("Неизвестная команда. Попробуйте 'инвентарь' или 'выход'")


if __name__ == "__main__":
    main()
