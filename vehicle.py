import settings as stgs

import pygame as pg


class Car:
    def __init__(self, x: int, y: int, speed: int, color: str = None) -> None:
        self.x = x
        self.y = y
        self.speed = speed
        self.color = color
        self

    def update(self) -> None:
        self.x += self.speed

    def set_speed(self, speed: int) -> None:
        self.speed = speed

    def render(self, surf: pg.Surface) -> None:
        pass
