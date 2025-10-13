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
