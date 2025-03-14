import settings as stgs

import pygame as pg
from typing import TypeVar

Game = TypeVar("Game")


class Fly:
    def __init__(self, game: Game) -> None:
        """ Initializes an fly object.
        Args:
        game (Game): The game object.
        """
        self.game: Game = game
        self.state: str = "idle"