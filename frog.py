import pygame as pg

from typing import TypeVar

Game = TypeVar("Game")

class Frog:
    def __init__(self, game: Game, pos: tuple[int], size: tuple[int], direction: str = "north") -> None:
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

    def jump(self, direction: str) -> None:
        """
        Make the frog jump in a specified direction.
        Args:
        direction (str): The direction to jump.
        """