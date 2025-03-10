import settings as stgs

import pygame as pg
from typing import TypeVar

Game = TypeVar("Game")


class TimeBar:
    def __init__(self, game: Game) -> None:
        """
        Initializes an TimeBar object.
        Args:
        game (Game): The game object.
        """
        self.game: Game = game
        self.time: float = stgs.TIME_BAR["time"]
        self.max_time: float = stgs.TIME_BAR["time"]
        self.length: int = stgs.TIME_BAR["length"]
        self.max_length: int = stgs.TIME_BAR["length"]
        self.height: int = stgs.TIME_BAR["height"]
        self.pos: tuple[int] = (stgs.TIME_BAR["x pos"], stgs.TIME_BAR["y pos"])  # top right corner
        self.r: int = 0
        self.g: int = 255
        self.b: int = 0
        self.one_third_length: float = self.max_length / 3
        self.two_third_length: float = self.one_third_length * 2
        self.steps: float = 255 / (self.one_third_length)
        self.stop: bool = False

    def update(self, dt: float) -> None:
        """
        Updates the TimeBar object.
        Args:
        dt (float): The time difference since the last update.
        """
        if not self.stop:
            self.time -= dt
        if self.time <= 0:
            self.game.time_up()
        self.calculate_length()
        self.calculate_color()

    def calculate_length(self) -> None:
        """ Calculates the length of the TimeBar object. """
        self.length = int(self.time * self.max_length / self.max_time)

    def calculate_color(self) -> None:
        """ Calculates the color of the TimeBar object. """
        if self.length > self.two_third_length:
            self.r = (self.max_length - self.length) * self.steps
            if self.r > 255:
                self.r = 255
        elif self.length > self.one_third_length:
            self.g = 255 - (self.two_third_length - self.length) * (self.steps / 2)
            if self.g < 165:
                self.g = 165
        else:
            self.g = 165 - (self.one_third_length - self.length) * (self.steps / 2)
            if self.g < 0:
                self.g = 0

    def get_time(self) -> int:
        """ Returns the current time rounded to seconds. """
        return round(self.time)
    
    def stop_time(self) -> None:
        """ Stops the time. """
        self.stop = True

    def render(self, surf: pg.Surface) -> None:
        """
        Renders the TimeBar object to the given surface.
        Args:
        surf (pg.Surface): The surface to render the TimeBar object to.
        """
        pg.draw.rect(surf, (self.r, self.g, self.b), (self.pos[0] - self.length, self.pos[1], self.length, self.height), border_radius=5)