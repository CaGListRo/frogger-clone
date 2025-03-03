import settings as stgs

import pygame as pg

from random import choice
from typing import TypeVar, Final

Game = TypeVar("Game")
Animation = TypeVar("Animation")


class Snake:
    TRANSPARENT_COLOR: Final[tuple[int]] = (0, 0, 0, 0)
    def __init__(self, game: Game, position: str = "green") -> None:
        """ Initializes an snake object. """
        self.animation: Animation = game.images["snake"].copy()
        image_to_blit: pg.Surface = self.animation.get_current_image()
        image_size: tuple[int] = image_to_blit.get_size()
        self.half_image_height: int = int(image_size[1] / 2)
        image_length: int = image_size[0]
        self.image: pg.Surface = pg.Surface(image_size, pg.SRCALPHA)
        self.image.fill(self.TRANSPARENT_COLOR)
        self.image.blit(image_to_blit, (0, 0))
        self.direction: int = choice([-1, 1])  # -1 = snake heading left, 1 = snake heading right
        y_position: int = 320 if position is "green" else 234
        x_position: int = -image_length if self.direction == 1 else stgs.WINDOW_SIZE[0]
        self.pos: pg.Vector2 = pg.Vector2((x_position, y_position))
        self.speed: int = stgs.SNAKE_SPEED

    def update(self, dt: float) -> None:
        """
        Updates the snake animation.
        Args:
        dt (float): The time since the last frame.
        """
        self.animation.update(dt)
        self.pos.x += self.speed * self.direction * dt

    def render(self, surf: pg.Surface) -> None:
        """
        Renders the snake onto the given surface.
        Args:
        surf (pg.Surface): The surface to render the snake onto.
        """
        image_to_blit: pg.Surface = self.animation.get_current_image()
        self.image.fill(self.TRANSPARENT_COLOR)
        self.image.blit(image_to_blit, (0, 0))
        surf.blit(self.image, (self.pos.x, self.pos.y - self.half_image_height))