import settings as stgs

import pygame as pg
from random import choice
from typing import TypeVar, Final

Game = TypeVar("Game")

# [trunks, turtles, trunks, trunks, turtles, trucks, racing cars, cars, bulldozer, cars]
class SmallCar:
    TRANSPARENT_COLOR: Final[tuple[int]] = (0, 0, 0, 0)
    def __init__(self, game: Game, x: int, y: int) -> None:
        self.game = game
        self.pos = (x, y)
        self.speed = stgs.START_SPEED[f"level {str(self.game.level)}"][9]
        self.image = (choice(self.game.images["small_cars"]))
        self.image = pg.transform.rotate(self.image, 180)
        self.rect = self.image.get_rect(center=self.pos)

    def update(self, dt: float) -> None:
        self.pos = (self.pos[0] + self.speed * dt, self.pos[1])
        if self.pos[0] < -35:
            self.pos = (stgs.WINDOW_SIZE[0] + 35, self.pos[1])
        self.rect.center = self.pos

    def set_speed(self, speed: int) -> None:
        self.speed = speed

    def render(self, surf: pg.Surface) -> None:
        surf.blit(self.image, self.rect)

