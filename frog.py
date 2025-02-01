import pygame as pg


class Frog:
    def __init__(self, pos: tuple[int], size: tuple[int], direction: str = "north") -> None:
        """
        Initialize a Frog object.
        Args:
        pos (tuple[int]): The initial position of the frog.
        size (tuple[int]): The size of the frog.
        direction (str): The initial direction of the frog. Defaults to "north".
        """
        self.pos: tuple[int] = pos
        self.size: tuple[int] = size
        self.direction: str = direction