import settings as stgs

import pygame as pg

from random import choice
from typing import TypeVar, Final

Game = TypeVar("Game")
Animation = TypeVar("Animation")


class MiddleSnake:
    TRANSPARENT_COLOR: Final[tuple[int]] = (0, 0, 0, 0)
    def __init__(self, game: Game) -> None:
        """
        Initializes an snake object.
        Args:
        game: The game object.
        """
        self.game: Game = game
        self.animation: Animation = self.game.animations["snake"].copy()
        image_to_blit: pg.Surface = self.animation.get_current_image()
        image_size: tuple[int] = image_to_blit.get_size()
        self.half_image_height: int = int(image_size[1] / 2)
        self.image_length: int = image_size[0]
        self.image: pg.Surface = pg.Surface(image_size, pg.SRCALPHA)
        self.image.fill(self.TRANSPARENT_COLOR)
        self.image.blit(image_to_blit, (0, 0))
        self.direction: str = choice(["left", "right"])
        y_position: int = stgs.SNAKE_LANE
        x_position: int = -self.image_length if self.direction == "right" else stgs.WINDOW_SIZE[0]
        self.pos: pg.Vector2 = pg.Vector2((x_position, y_position))
        self.speed: int = stgs.SNAKE_SPEED
        self.create_head_rect()

    def create_head_rect(self) -> None:
        """ Creates a rectangle for the snake's head. """
        self.head_rect: pg.Rect = pg.Rect(self.pos.x + stgs.SNAKE_HEAD_RECT[self.direction][0], 
                                          self.pos.y - stgs.SNAKE_HEAD_RECT[self.direction][1], 
                                          stgs.SNAKE_HEAD_RECT[self.direction][2], 
                                          stgs.SNAKE_HEAD_RECT[self.direction][3])

    def update(self, dt: float) -> None:
        """
        Updates the snake animation.
        Args:
        dt (float): The time since the last frame.
        """
        self.animation.update(dt)
        multiplicand: int = 1 if self.direction == "right" else -1  # -1 = snake heading left, 1 = snake heading right
        self.pos.x += self.speed * multiplicand * dt
        self.head_rect.x = self.pos.x + stgs.SNAKE_HEAD_RECT[self.direction][0]
        if self.direction == "right" and self.pos.x > stgs.WINDOW_SIZE[0]:
            self.game.get_snake_time()
            self.game.middle_snake = None
        elif self.direction == "left" and self.pos.x < 0 - self.image_length:
            self.game.get_snake_time()
            self.game.middle_snake = None

    def render(self, surf: pg.Surface) -> None:
        """
        Renders the snake onto the given surface.
        Args:
        surf (pg.Surface): The surface to render the snake onto.
        """
        image_to_blit: pg.Surface = self.animation.get_current_image()
        flip: bool = True if self.direction == "right" else False
        image_to_blit = pg.transform.flip(image_to_blit, flip, False)
        self.image.fill(self.TRANSPARENT_COLOR)
        self.image.blit(image_to_blit, (0, 0))
        surf.blit(self.image, (self.pos.x, self.pos.y - self.half_image_height))
        pg.draw.rect(surf, "red", self.head_rect, width=2)