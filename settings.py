from typing import Final

WINDOW_SIZE: Final[tuple[int]] = (800, 700)

FROG_START_POS: Final[tuple[int]] = (400, 597)

WATER: Final[dict[list[int]]] = {
    "level 1": [3, 5, 2, 4, 4],  # [medium trunks, turtle pairs, large trunks, small trunks, turtle trios]
    "level 2": [3, 5, 2, 4, 4],  # [medium trunks/one crocodile, turtle pairs, large trunks, small trunks, turtle trios]
    "level 3": [2, 5, 1, 4, 4],
}

STREET: Final[dict[list[int]]] = {
    "level 1": [2, 1, 3, 3, 3],  # [trucks, racing cars, big cars, bulldozer, small cars]
    "level 2": [3, 2, 4, 4, 4],
    "level 3": [3, 2, 5, 4, 4],
}

SPACING: Final[dict[int]] = {
    "lane 10": 350,  # medium trunk
    "lane 9": 160,   # turtle pairs
    "lane 8": 550,   # large trunks
    "lane 7": 250,   # small trunks
    "lane 6": 200,   # turtle trios
    "lane 5": 350,   # trucks
    "lane 4": 250,   # racing cars
    "lane 3": 250,   # large cars
    "lane 2": 250,   # bulldozer
    "lane 1": 250,   # small cars
}

START_SPEED: Final[dict[list[int]]] = {
    # [trunks, turtles, trunks, trunks, turtles, trucks, racing cars, cars, bulldozer, cars]
    "level 1": [50, -40, 90, 30, -40, -40, 50, -30, 40, -25],
    "level 2": [70, -30, 50, 70, -50, -50, 90, -50, 50, -40],
}

TURTLES: Final[tuple[int]] = (2, 3)  # number of turtles that swim together (second lane = duos, fifth lane = trios)

TURTLE_SURFACE: Final[list[tuple[int]]] = [
    (105, 38),  # second lane from top with the turtle duos
    (160, 38)   # lowest lane of the water traffic with the turtle trios
]

CROCS_IN_HOUSES: Final[list[bool]] = [False, True, True]  # [level 1, level 2, level 3]

HOUSE_SIZE: Final[tuple[int]] = (70, 57)

HOUSE_TOP_LEFT: Final[list[tuple[int]]] = [(31, 25), (196, 25), (365, 25), (534, 25), (699, 25)]

SNAKES: Final[list[bool]] = [False, False, True]  # [level 1, level 2, level 3]

SNAKE_SPEED: Final[int] = 50

SCORE: Final[dict[int]] = {
    "jump": 10,
    "second": 20,
    "frog in house": 50,
    "frogs left": 100,
    "finish level": 1000
}