#!/usr/bin/env python3

from .constants import ROOMS

# Состояние игрока и игры
game_state = {
    'player_inventory': [],      # Инвентарь игрока
    'current_room': 'entrance',  # Текущая комната
    'game_over': False,          # Флаг окончания игры
    'steps_taken': 0             # Количество шагов
}

def main():
    print("Первая попытка запустить проект!")

if __name__ == "__main__":
    main()
