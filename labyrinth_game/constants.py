ROOMS = {
    'entrance': {
        'description': 'Вы в темном входе лабиринта. Стены покрыты мхом.',
        'exits': {'east': 'library', 'south': 'trap_room'},
        'items': ['torch'],
        'puzzle': None
    },
    'hall': {
        'description': 'Большой зал с эхом. По центру стоит пьедестал.',
        'exits': {'west': 'armory', 'north': 'observatory'},
        'items': [],
        'puzzle': (
            'На пьедестале надпись: "Назовите число после девяти". '
            'Введите ответ цифрой или словом.',
            '10',
            ['10', 'десять']
        )
    },
    'trap_room': {
        'description': 'Комната исписанная древними символами. На полу странные плиты',
        'exits': {'north': 'entrance', 'east': 'orangery'},
        'items': ['rusty_key'],
        'puzzle': (
            'Чтобы спастись, назовите слово "шаг" '
            'три раза подряд',
            'шагшагшаг'
        )
    },
    'library': {
        'description': 'Пыльная библиотека. На полках старые свитки.',
        'exits': {'west': 'entrance', 'south': 'armory'},
        'items': ['ancient_book'],
        'puzzle': (
            'В свитке загадка: "Что принадлежит тебе, но другие '
            'используют это чаще?"',
            'имя',
            ['имя', 'name']
        )
    },
    'armory': {
        'description': 'Старая оружейная комната. На стенах висит оружие.',
        'exits': {'north': 'library', 'east': 'hall', 'south': 'treasure_room'},
        'items': ['sword', 'bronze_box'],
        'puzzle': None
    },
    'treasure_room': {
        'description': 'Комната с большим сундуком сокровищ.',
        'exits': {'north': 'armory'},
        'items': ['treasure_chest'],
        'puzzle': (
            'Сколько будет: квадратный корень из 100? '
            'Ответ цифрой или словом.',
            '10',
            ['10', 'десять']
        )
    },
    'orangery': {
        'description': 'Оранжерея с экзотическими растениями. '
                       'В центре растет золотое дерево.',
        'exits': {'west': 'trap_room', 'north': 'observatory'},
        'items': ['golden_tree', 'dried_spring', 'exotic_flowers'],
        'puzzle': (
            'Дерево шепчет: "В руках не удержать, в решете не унести. '
            'Что это?" (ответ одно слово)',
            'вода',
            ['вода', 'water']
        )
    },
    'observatory': {
        'description': 'Обсерватория с телескопом. На столе звездные карты.',
        'exits': {'south': 'hall', 'west': 'orangery'},
        'items': ['star_map', 'telescope'],
        'puzzle': (
            'Карта показывает последовательность: 2, 4, 6, ? '
            'Какое следующее число? Ответ цифрой или словом.',
            '8',
            ['8', 'восемь']
        )
    }
}

COMMANDS = {
    "go <direction>/идти <направление>": "перейти в направлении",
    "look/осмотр": "осмотреть текущую комнату",
    "take <item>/взять <предмет>": "подобрать предмет",
    "use <item>/использовать <предмет>": "использовать предмет",
    "solve/решить": "решить загадку",
    "inventory/инвентарь": "показать инвентарь",
    "help/помощь": "показать справку по командам",
    "quit/выход": "выйти из игры"
}

# Вероятности и настройки игры
EVENT_PROBABILITY = 5  # 1/5 = 20% шанс случайного события
TRAP_DAMAGE_PROBABILITY = 3  # 30% шанс проигрыша при пустом инвентаре
MAX_DAMAGE_CHANCE = 10  # Максимальное значение для проверки урона

# Настройки псевдослучайного генератора (исключение по условию)
PSEUDO_RANDOM_MULTIPLIER_1 = 12.9898
PSEUDO_RANDOM_MULTIPLIER_2 = 43758.5453

# Типы случайных событий
EVENT_TYPES_COUNT = 3  # Количество типов случайных событий
EVENT_FIND_ITEM = 0    # Находка предмета
EVENT_SCARE = 1        # Испуг
EVENT_TRAP = 2         # Ловушка
