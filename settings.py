from typing import Final, TypedDict, Dict, List, Tuple

# Type-Definition for complex structures
class ButtonColorInfo(TypedDict):
    main_color: Tuple[int, int, int]
    hover_color: Tuple[int, int, int]
    shadow_color: Tuple[int, int, int]
    frame_color: Tuple[int, int, int]

class LanguageTexts(TypedDict):
    de: str
    en: str
    es: str
    fr: str
    it: str
    tr: str

# settings for the crocodile
CROCOS_IN_HOUSES: Final[List[bool]] = [False, True, True, True, True]  # [level 1, level 2, level 3, level 4, level 5]
CROCOS_SWIMMING: Final[List[bool]] = [False, True, True, True, True]  # [level 1, level 2, level 3, level 4, level 5]
HOUSE_CROCO_POS: Final[List[Tuple[int, int, int]]] = [
    (-34, 56, 16),
    (131, 56, 181),
    (300, 56, 350),
    (469, 56, 519),
    (634, 56, 684),
]
HOUSE_CROCO_SPEED: Final[List[int]] = [50, 60, 70, 80]  # [level 2, level 3, level 4, level 5]
HOUSE_CROCO_STAYING_TIME: Final[List[float]] = [3.5, 4.0, 4.5, 5.0]  # [level 2, level 3, level 4, level 5]
LANE_CROCO_TIMER: Final[List[float]] = [5.0, 4.0, 3.0, 2.0]  # [level 2, level 3, level 4, level 5]
HOUSE_CROCO_WAITING_TIME: Final[List[float]] = [2.0, 1.5, 1.0, 0.5]  # [level 2, level 3, level 4, level 5]

# decorations
STRIPES: Final[Dict[str, int]] = {  # the yellow stripes on the street
    "rows": 4,
    "columns": 55,
    "x start": -5,
    "y start": 410,
    "y spacing": 43,
    "x spacing": 32
}

# settings for the fly
FLY_HOUSE_CENTER_POS: Final[List[Tuple[int, int]]] = [
    (66, 80),
    (231, 80),
    (400, 80),
    (569, 80),
    (734, 80)
]
FLY_SCORES: Final[Dict[str, int]] = {
    "house fly": 100,
    "tree fly": 200
}
FLY_STATE_TIMER: Final[float] = 1.0
FLY_STAY_TIME: Final[float] = 5.0
FLY_WALK_SPEED: Final[int] = 32
TREE_FLY_CHANCE: Final[List[int]] = [5, 6, 6, 7, 8]
TREE_FLY_TIME: Final[List[int]] = [15, 20, 25, 30, 35]

# settings for the frog
FROG_COLLISION_RECT: Final[Tuple[int, int]] = (30, 30)
FROG_DEAD_TIME: Final[float] = 0.6
FROG_DRAW_HEIGHT: Final[int] = 630  # the y value to draw the remaining frogs
FROG_HALF_RECT_SIZE: Final[int] = int(FROG_COLLISION_RECT[0] / 2)
FROG_JUMP_DISTANCE: Final[int] = 43
FROG_LIMITS: Final[Dict[str, int]] = {
    "top": 100,
    "bottom": 564,
    "left": FROG_HALF_RECT_SIZE + FROG_JUMP_DISTANCE,
    "right": 800 - FROG_HALF_RECT_SIZE - FROG_JUMP_DISTANCE  # 800 is the window width
}
FROG_START_POS: Final[Tuple[int, int]] = (400, 605)
FROG_WATER_COLLISION_HEIGHT: Final[int] = 308
SHOW_FROG_TIME: Final[float] = 3.0

# settings for the traffic (water and street traffic)
LANE_HEIGHTS: Final[Dict[str, int]] = {  # the center height of each lane
    "lane 10": 130,  # medium trunk
    "lane 9": 173,   # turtle pairs
    "lane 8": 217,   # large trunks
    "lane 7": 260,   # small trunks
    "lane 6": 303,   # turtle trios
    "lane 5": 389,   # trucks
    "lane 4": 433,   # racing cars
    "lane 3": 476,   # large cars
    "lane 2": 519,   # bulldozer
    "lane 1": 562,   # small cars
}
SPACING: Final[Dict[str, List[int]]] = {  # [Level 1, Level 2, Level 3, Level 4, Level 5]
    "lane 10": [350, 350, 400, 400, 450],  # medium trunk
    "lane 9": [190, 190, 190, 230, 270],   # turtle pairs
    "lane 8": [550, 550, 650, 650, 650],   # large trunks
    "lane 7": [250, 250, 250, 300, 350],   # small trunks
    "lane 6": [240, 240, 240, 290, 340],   # turtle trios
    "lane 5": [350, 320, 300, 280, 260],   # trucks
    "lane 4": [150, 150, 150, 150, 150],   # racing cars
    "lane 3": [250, 200, 200, 150, 120],   # large cars
    "lane 2": [250, 200, 200, 150, 130],   # bulldozer
    "lane 1": [250, 200, 200, 150, 120],   # small cars
}
START_SPEED: Final[Dict[str, List[int]]] = {
    "level 1": [50, 40, 90, 30, 40, 40, 50, 30, 40, 25],
    "level 2": [70, 30, 50, 70, 50, 55, 90, 50, 50, 40],
    "level 3": [50, 50, 60, 40, 60, 40, 100, 60, 40, 70],
    "level 4": [80, 60, 30, 70, 40, 60, 110, 70, 30, 60],
    "level 5": [90, 70, 70, 90, 70, 75, 130, 80, 60, 90],
}
STREET: Final[Dict[str, List[int]]] = {
    "level 1": [2, 1, 3, 3, 3],
    "level 2": [3, 2, 4, 4, 4],
    "level 3": [3, 3, 4, 4, 4],
    "level 4": [4, 3, 5, 5, 5],
    "level 5": [4, 4, 6, 5, 6],
}
WATER: Final[Dict[str, List[int]]] = {
    "level 1": [3, 5, 2, 4, 4],
    "level 2": [3, 5, 2, 4, 4],
    "level 3": [2, 5, 1, 4, 4],
    "level 4": [1, 4, 1, 3, 3],
    "level 5": [1, 3, 1, 2, 2],
}

# settings for the turtles in the traffic
TURTLE_DIVE_TIME: Final[List[int]] = [7, 6, 5, 4, 3]  # in seconds
TURTLE_FROG_CARRY_TIME: Final[Tuple[float, float]] = (0.75, 1.5)
TURTLE_SPACING: Final[int] = 55
TURTLE_SURFACE: Final[List[Tuple[int, int]]] = [
    (105, 38),  # second lane from top with the turtle duos
    (160, 38)   # lowest lane of the water traffic with the turtle trios
]
TURTLES: Final[Tuple[int, int]] = (2, 3)  # number of turtles that swim together

# settings for the houses
HOUSE_SIZE: Final[Tuple[int, int]] = (70, 57)
HOUSE_TOP_LEFT: Final[List[Tuple[int, int]]] = [
    (31, 51), 
    (196, 51), 
    (365, 51), 
    (534, 51), 
    (699, 51)]
GRAS_RECTS: Final[List[Tuple[int, int, int, int]]] = [
    (0, 99, 31, 9), 
    (102, 99, 93, 9), 
    (266, 99, 97, 9), 
    (436, 99, 97, 9), 
    (605, 99, 93, 9), 
    (770, 99, 800, 9)]

# settings for the snakes
SNAKE_HEAD_RECT: Final[Dict[str, Tuple[int, int, int, int]]] = {
    "left": (0, 4, 14, 8),
    "right": (67, 4, 14, 8)
}
SNAKE_LANE: Final[int] = 346
SNAKE_SPEED: Final[int] = 50
SNAKES: Final[List[bool]] = [False, False, True, True, True]
TREE_SNAKE_CHANCE: Final[List[int]] = [0, 0, 8, 7, 6]
TREE_SNAKE_TIME: Final[List[int]] = [0, 0, 30, 20, 10]

# settings for the game
SCORE: Final[Dict[str, int]] = {
    "jump": 10,
    "second": 10,
    "frog in house": 50,
    "frogs left": 100,
    "finish level": 1000
}
SPEED_UP_SCORE: Final[List[int]] = [1800, 3600, 5400, 7200, 10_000]
TIME_BAR: Final[Dict[str, float]] = {
    "x pos": 590.0,
    "y pos": 650.0,
    "length": 300.0,
    "height": 20.0,
    "time": 60.0
}
WINDOW_SIZE: Final[Tuple[int, int]] = (800, 700)

# settings for the menu
BUTTON_COLORS: Final[Dict[str, ButtonColorInfo]] = {
    'green': {
        'main_color': (56, 155, 60),
        'hover_color': (76, 175, 80),
        'shadow_color': (16, 115, 20),
        'frame_color': (6, 95, 20)
    },
    'yellow': {
        'main_color': (235, 235, 0),
        'hover_color': (255, 255, 50),
        'shadow_color': (195, 195, 0),
        'frame_color': (125, 125, 0)
    },
    'red': {
        'main_color': (235, 0, 0),
        'hover_color': (255, 50, 50),
        'shadow_color': (175, 0, 0),
        'frame_color': (100, 0, 0)
    },
    'white': {
        'main_color': (235, 235, 235),
        'hover_color': (255, 255, 255),
        'shadow_color': (175, 175, 175),
        'frame_color': (100, 100, 100)
    },
    'beige': {
        'main_color': (235, 220, 195),
        'hover_color': (245, 230, 210),
        'shadow_color': (185, 170, 145),
        'frame_color': (120, 105, 80)
    }
}
BUTTON_FONT_SIZE: Final[int] = 20
BUTTON_NAMES: Final[Dict[str, LanguageTexts]] = {
    "back": {
        "de": "ZURÜCK", "en": "BACK", "es": "VOLVER", 
        "fr": "RETOUR", "it": "INDIETRO", "tr": "GERİ"
    },
    "highscores": {
        "de": "RANGLISTE", "en": "HIGHSCORES", "es": "RÉCORDS", 
        "fr": "CLASSEMENT", "it": "CLASSIFICA", "tr": "SKOR TABLOSU"
    },
    "language": {
        "de": "DEUTSCH", "en": "ENGLISH", "es": "ESPAÑOL", 
        "fr": "FRANÇAIS", "it": "ITALIANO", "tr": "TÜRKÇE"
    },
    "options": {
        "de": "OPTIONEN", "en": "OPTIONS", "es": "OPCIONES", 
        "fr": "OPTIONS", "it": "OPZIONI", "tr": "SEÇENEKLER"
    },
    "start": {
        "de": "START", "en": "START", "es": "COMENZAR", 
        "fr": "COMMENCER", "it": "INIZIO", "tr": "BAŞLAT"
    },
    "quit": {
        "de": "BEENDEN", "en": "QUIT", "es": "SALIR", 
        "fr": "QUITTER", "it": "USCIRE", "tr": "ÇIKIŞ"
    },
}
BUTTON_POSITIONS: Final[Dict[str, Tuple[int, int]]] = {
    "back": (600, 650),
    "highscores": (412, 50),
    "options": (218, 50),
    "start": (24, 50),
    "quit": (606, 50)
}
BUTTON_OFFSET: Final[int] = 5
BUTTON_SIZE: Final[Tuple[int, int]] = (170, 40)
LANGUAGE_BUTTON_SIZE: Final[Tuple[int, int]] = (120, 40)
LANGUAGE_BUTTON_POSITIONS: Final[List[Tuple[int, int]]] = []

# settings for the pause screen
PAUSE: Final[Dict[str, LanguageTexts]] = {
    "pause": {
        "de": "PAUSE", "en": "PAUSE", "es": "PAUSA", 
        "fr": "PAUSE", "it": "PAUSA", "tr": "DURAKLATILDI"
    },
    "text": {
        "de": "Drücke [P], um fortzufahren.", 
        "en": "Press [P] to resume.", 
        "es": "Presiona [P] para continuar.", 
        "fr": "Appuyez sur [P] pour reprendre.", 
        "it": "Premi [P] per continuare.", 
        "tr": "Devam etmek için [P] tuşuna basın."
    }
}
BLINK_TIME: Final[float] = 0.8