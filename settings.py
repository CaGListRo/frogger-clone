from typing import Final

WINDOW_SIZE: Final[tuple[int]] = (800, 700)

FROG_START_POS: Final[tuple[int]] = (400, 605)

FROG_COLLISION_RECT: Final[tuple[int]] = (32, 32)

FROG_HALF_RECT_SIZE: Final[int] = int(FROG_COLLISION_RECT[0] / 2)

FROG_JUMP_DISTANCE: Final[int] = 43

FROG_LIMITS: Final[dict[int]] = {
    "top": 100,
    "bottom": 564,
    "left": FROG_HALF_RECT_SIZE + FROG_JUMP_DISTANCE,
    "right": WINDOW_SIZE[0] - FROG_HALF_RECT_SIZE - FROG_JUMP_DISTANCE
}

FROG_DEAD_TIME: Final[float] = 0.6

FROG_WATER_COLLISION_HEIGHT: Final[int] = 308

SHOW_FROG_TIME: Final[float] = 3.0

FLY_HOUSE_CENTER_POS: Final[list[tuple[int]]] = [
    (66, 80),
    (231, 80),
    (400, 80),
    (569, 80),
    (734, 80)
]

WATER: Final[dict[list[int]]] = {
    "level 1": [3, 5, 2, 4, 4],  # [medium trunks, turtle pairs, large trunks, small trunks, turtle trios]
    "level 2": [3, 5, 2, 4, 4],  # [medium trunks/one crocodile, turtle pairs, large trunks, small trunks, turtle trios]
    "level 3": [2, 5, 1, 4, 4],
    "level 4": [1, 4, 1, 3, 3],
    "level 5": [1, 3, 1, 2, 2],
}

STREET: Final[dict[list[int]]] = {
    "level 1": [2, 1, 3, 3, 3],  # [trucks, racing cars, big cars, bulldozer, small cars]
    "level 2": [3, 2, 4, 4, 4],
    "level 3": [3, 3, 4, 4, 4],
    "level 4": [4, 3, 5, 5, 5],
    "level 5": [4, 4, 6, 5, 6],
}

STRIPES: Final[dict[int]] = {  # the yellow stripes on the street
    "rows": 4,
    "columns": 55,
    "x start": -5,
    "y start": 410,
    "y spacing": 43,
    "x spacing": 32
}

LANE_HEIGHTS: Final[dict[int]] = {
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

SPACING: Final[dict[int]] = {
    "lane 10": [350, 350, 400, 400, 450],  # medium trunk
    "lane 9": [190, 190, 190, 230, 270],   # turtle pairs
    "lane 8": [550, 550, 650, 650, 650],   # large trunks
    "lane 7": [250, 250, 250, 300, 350],   # small trunks
    "lane 6": [240, 240, 240, 290, 340],   # turtle trios
    "lane 5": [350, 320, 300, 280, 260],   # trucks
    "lane 4": [100, 100, 100, 100, 100],   # racing cars
    "lane 3": [250, 200, 200, 150, 110],   # large cars
    "lane 2": [250, 200, 200, 150, 130],   # bulldozer
    "lane 1": [250, 200, 200, 150, 120],   # small cars
}

START_SPEED: Final[dict[list[int]]] = {
    # [trunks, turtles, trunks, trunks, turtles, trucks, racing cars, cars, bulldozer, cars]
    "level 1": [50, -40, 90, 30, -40, -40, 50, -30, 40, -25],
    "level 2": [70, -30, 50, 70, -50, -55, 90, -50, 50, -40],
    "level 3": [50, -50, 60, 40, -60, -40, 100, -60, 40, -70],
    "level 4": [80, -60, 30, 70, -40, -60, 110, -70, 30, -60],
    "level 5": [90, -70, 70, 90, -70, -75, 130, -80, 60, -90],
}

TURTLES: Final[tuple[int]] = (2, 3)  # number of turtles that swim together (second lane = duos, fifth lane = trios)

TURTLE_SURFACE: Final[list[tuple[int]]] = [
    (105, 38),  # second lane from top with the turtle duos
    (160, 38)   # lowest lane of the water traffic with the turtle trios
]

TURTLE_SPACING: Final[int] = 55

CROCOS_IN_HOUSES: Final[list[bool]] = [False, True, True, True, True]  # [level 1, level 2, level 3]

CROCOS_SWIMMING: Final[list[bool]] = [False, True, True, True, True]  # [level 1, level 2, level 3]

HOUSE_SIZE: Final[tuple[int]] = (70, 57)

HOUSE_TOP_LEFT: Final[list[tuple[int]]] = [(31, 51), (196, 51), (365, 51), (534, 51), (699, 51)]

GRAS_RECTS: Final[list[tuple]] = [(0, 99, 31, 9), (102, 99, 93, 9), (266, 99, 97, 9), (436, 99 ,97, 9), (605, 99, 93, 9), (770, 99, 800, 9)]

SNAKES: Final[list[bool]] = [False, False, True, True, True]  # [level 1, level 2, level 3]

SNAKE_HEAD_RECT: Final[dict[tuple[int]]] = {  # Only the head of the snake is deadly for the frog
    "left": (0, 4, 14, 8),
    "right": (67, 4, 14, 8)
    }

SNAKE_LANE: Final[int] = 346

SNAKE_SPEED: Final[int] = 50

SCORE: Final[dict[int]] = {
    "jump": 10,
    "second": 10,
    "frog in house": 50,
    "frogs left": 100,
    "finish level": 1000
}

TIME_BAR: Final[dict[int]] = {
    "x pos": 590,  # top right
    "y pos": 650,  # top right
    "length": 300,
    "height": 20,
    "time": 60.0
}

FROG_DRAW_HEIGHT: Final[int] = 630  # the y value to draw the remaining frogs