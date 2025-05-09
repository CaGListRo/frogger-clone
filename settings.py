from typing import Final

# settings for the crocodile
CROCOS_IN_HOUSES: Final[list[bool]] = [False, True, True, True, True]  # [level 1, level 2, level 3, level 4, level 5]
CROCOS_SWIMMING: Final[list[bool]] = [False, True, True, True, True]  # [level 1, level 2, level 3, level 4, level 5]
HOUSE_CROCO_POS: Final[list[tuple[int]]] = [
    (-34, 56, 16),
    (131, 56, 181),
    (300, 56, 350),
    (469, 56, 519),
    (634, 56, 684),
]
HOUSE_CROCO_SPEED: Final[list[int]] = [50, 60, 70, 80]  # [level 2, level 3, level 4, level 5]
HOUSE_CROCO_STAYING_TIME: Final[list[float]] = [3.5, 4.0, 4.5, 5.0]  # [level 2, level 3, level 4, level 5]
LANE_CROCO_TIMER: Final[list[float]] = [5.0, 4.0, 3.0, 2.0]  # [level 2, level 3, level 4, level 5]
HOUSE_CROCO_WAITING_TIME: Final[list[float]] = [2.0, 1.5, 1.0, 0.5]  # [level 2, level 3, level 4, level 5]

# decoration
STRIPES: Final[dict[int]] = {  # the yellow stripes on the street
    "rows": 4,
    "columns": 55,
    "x start": -5,
    "y start": 410,
    "y spacing": 43,
    "x spacing": 32
}

# settings for the fly
FLY_HOUSE_CENTER_POS: Final[list[tuple[int]]] = [
    (66, 80),
    (231, 80),
    (400, 80),
    (569, 80),
    (734, 80)
]
FLY_SCORES: Final[dict[int]] = {
    "house fly": 100,
    "trunk fly": 200
}
FLY_STATE_TIMER: Final[float] = 1.0
FLY_STAY_TIME: Final[float] = 5.0
FLY_WALK_SPEED: Final[int] = 32
TREE_FLY_CHANCE: Final[list[int]] = [5, 6, 6, 7, 8]
TREE_FLY_TIME: Final[list[int]] = [15, 20, 25, 30, 35]

# settings for the frog
FROG_COLLISION_RECT: Final[tuple[int]] = (30, 30)
FROG_DEAD_TIME: Final[float] = 0.6
FROG_DRAW_HEIGHT: Final[int] = 630  # the y value to draw the remaining frogs
FROG_HALF_RECT_SIZE: Final[int] = int(FROG_COLLISION_RECT[0] / 2)
FROG_JUMP_DISTANCE: Final[int] = 43
FROG_LIMITS: Final[dict[int]] = {
    "top": 100,
    "bottom": 564,
    "left": FROG_HALF_RECT_SIZE + FROG_JUMP_DISTANCE,
    "right": 800 - FROG_HALF_RECT_SIZE - FROG_JUMP_DISTANCE  # 800 is the window width
}
FROG_START_POS: Final[tuple[int]] = (400, 605)
FROG_WATER_COLLISION_HEIGHT: Final[int] = 308
SHOW_FROG_TIME: Final[float] = 3.0

# settings for the traffic  (water and street traffic)
LANE_HEIGHTS: Final[dict[int]] = {  # the center height of each lane
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
SPACING: Final[dict[int]] = {  # [Level 1, Level 2, Level 3, Level 4, Level 5]
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
START_SPEED: Final[dict[list[int]]] = {
    # [trunks, turtles, trunks, trunks, turtles, trucks, racing cars, cars, bulldozer, cars]
    "level 1": [50, 40, 90, 30, 40, 40, 50, 30, 40, 25],
    "level 2": [70, 30, 50, 70, 50, 55, 90, 50, 50, 40],
    "level 3": [50, 50, 60, 40, 60, 40, 100, 60, 40, 70],
    "level 4": [80, 60, 30, 70, 40, 60, 110, 70, 30, 60],
    "level 5": [90, 70, 70, 90, 70, 75, 130, 80, 60, 90],
}
STREET: Final[dict[list[int]]] = {
    "level 1": [2, 1, 3, 3, 3],  # [trucks, racing cars, big cars, bulldozer, small cars]
    "level 2": [3, 2, 4, 4, 4],
    "level 3": [3, 3, 4, 4, 4],
    "level 4": [4, 3, 5, 5, 5],
    "level 5": [4, 4, 6, 5, 6],
}
WATER: Final[dict[list[int]]] = {
    "level 1": [3, 5, 2, 4, 4],  # [medium trunks, turtle pairs, large trunks, small trunks, turtle trios]
    "level 2": [3, 5, 2, 4, 4],  # [medium trunks/one crocodile, turtle pairs, large trunks, small trunks, turtle trios]
    "level 3": [2, 5, 1, 4, 4],
    "level 4": [1, 4, 1, 3, 3],
    "level 5": [1, 3, 1, 2, 2],
}

# settings for the turtles in the traffic
TURTLE_DIVE_TIME: Final[list[int]] = [7, 6, 5, 4, 3]  # in seconds  # [level 1, level 2, level 3, level 4, level 5]
TURTLE_FROG_CARRY_TIME: Final[tuple[float]] = (0.75, 1.5)
TURTLE_SPACING: Final[int] = 55
TURTLE_SURFACE: Final[list[tuple[int]]] = [
    (105, 38),  # second lane from top with the turtle duos
    (160, 38)   # lowest lane of the water traffic with the turtle trios
]
TURTLES: Final[tuple[int]] = (2, 3)  # number of turtles that swim together (second lane = duos, fifth lane = trios)

# settings for the houses
HOUSE_SIZE: Final[tuple[int]] = (70, 57)
HOUSE_TOP_LEFT: Final[list[tuple[int]]] = [
    (31, 51), 
    (196, 51), 
    (365, 51), 
    (534, 51), 
    (699, 51)]
GRAS_RECTS: Final[list[tuple]] = [
    (0, 99, 31, 9), 
    (102, 99, 93, 9), 
    (266, 99, 97, 9), 
    (436, 99 ,97, 9), 
    (605, 99, 93, 9), 
    (770, 99, 800, 9)]

# settings for the snakes
SNAKE_HEAD_RECT: Final[dict[tuple[int]]] = {  # Only the head of the snake is deadly for the frog
    "left": (0, 4, 14, 8),
    "right": (67, 4, 14, 8)
    }
SNAKE_LANE: Final[int] = 346
SNAKE_SPEED: Final[int] = 50
SNAKES: Final[list[bool]] = [False, False, True, True, True]  # [level 1, level 2, level 3, level 4, level 5]
TREE_SNAKE_CHANCE: Final[list[int]] = [0, 0, 8, 7, 6]  # first two are '0' because there are no snakes in level 1 and 2
TREE_SNAKE_TIME: Final[list[int]] = [0, 0, 30, 20, 10]  # first two are '0' because there are no snakes in level 1 and 2

# settings for the game
SCORE: Final[dict[int]] = {
    "jump": 10,
    "second": 10,
    "frog in house": 50,
    "frogs left": 100,
    "finish level": 1000
}
SPEED_UP_SCORE: Final[list[int]] = [1800, 3600, 5400, 7200, 10_000]
TIME_BAR: Final[dict[int]] = {
    "x pos": 590,  # top right
    "y pos": 650,  # top right
    "length": 300,
    "height": 20,
    "time": 60.0
}
WINDOW_SIZE: Final[tuple[int]] = (800, 700)

# settings for the menu
BUTTON_COLORS: Final[dict[tuple[int]]] = {
    # Button colors including the hover, frame and shadow colors.
    'green': {'main_color': (56, 155, 60), 'hover_color': (76, 175, 80), 'shadow_color': (16, 115, 20), 'frame_color': (6, 95, 20)},
    'yellow': {'main_color': (235, 235, 0), 'hover_color': (255, 255, 50), 'shadow_color': (195, 195, 0), 'frame_color': (125, 125, 0)},
    'red': {'main_color': (235, 0, 0), 'hover_color': (255, 50, 50), 'shadow_color': (175, 0, 0), 'frame_color': (100, 0, 0)},
    'white': {'main_color': (235, 235, 235), 'hover_color': (255, 255, 255), 'shadow_color': (175, 175, 175), 'frame_color': (100, 100, 100)}
    }
BUTTON_NAMES: Final[dict[dict[str]]] = {
    "back": {"de": "ZURÜCK", "en": "BACK", "es": "VOLVER", "fr": "RETOUR", "it": "INDIETRO", "tr": "GERİ"},
    "highscores": {"de": "RANGLISTE", "en": "HIGHSCORES", "es": "PUNTUACIONES", "fr": "MEILLEURS SCORES", "it": "CLASSIFICA", "tr": "SKOR TABLOSU"},
    "language": {"de": "DEUTSCH", "en": "ENGLISH", "es": "ESPAÑOL", "fr": "FRANÇAIS", "it": "ITALIANO", "tr": "TÜRKÇE"},
    "options": {"de": "OPTIONEN", "en": "OPTIONS", "es": "OPCIONES", "fr": "OPTIONS", "it": "OPZIONI", "tr": "SEÇENEKLER"},
    "start": {"de": "START", "en": "START", "es": "COMENZAR", "fr": "COMMENCER", "it": "INIZIO", "tr": "BAŞLAT"},
    "quit": {"de": "BEENDEN", "en": "QUIT", "es": "SALIR", "fr": "QUITTER", "it": "USCIRE", "tr": "ÇIKIŞ"},
}
BUTTON_POSITIONS: Final[dict[tuple]] = {"back": (600, 650), "highscores": (412, 50), "options": (218, 50), "start": (24, 50), "quit": (606, 50)}
BUTTON_OFFSET: Final[int] = 5               # is needed for the click animation
BUTTON_SIZE: Final[tuple[int]] = (170, 40)  # (width, height)
LANGUAGE_BUTTON_SIZE: Final[tuple[int]] = (120, 40)  # (width, height)
LANGUAGE_BUTTON_POSITIONS: Final[list[tuple]] = [()]