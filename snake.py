import settings as stgs

import pygame as pg

from random import choice
from typing import Final, TYPE_CHECKING

if TYPE_CHECKING:
    from utils import Animation
    from game import Game


class MiddleSnake:
    TRANSPARENT_COLOR: Final[tuple[int, int, int, int]] = (0, 0, 0, 0)
    def __init__(self, game: "Game") -> None:
        """
        Initializes an middle snake object.
        A snake that crawls on the gras stripe in the middle of the screen.
        The direction is randomly chosen by the snake itself.
        Args:
        game: The game object.
        """
        self.game: "Game" = game
        self.animation: Animation = self.game.animations["snake"].copy()
        self.image: pg.Surface
        self.direction: str = choice(["left", "right"])
        self.get_current_image()
        
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

    def get_current_image(self) -> None:
        """ Gets the current image of the animation and blits it on self.image. """
        image_to_blit: pg.Surface | bool = self.animation.get_current_image()
        if isinstance(image_to_blit, pg.Surface):
            if not hasattr(self, "image"):
                image_size: tuple[int, int] = image_to_blit.get_size()
                self.half_image_height: int = int(image_size[1] / 2)
                self.image_length: int = image_size[0]
                self.image: pg.Surface = pg.Surface(image_size, pg.SRCALPHA)
            flip: bool = True if self.direction == "right" else False
            image_to_blit = pg.transform.flip(image_to_blit, flip, False)
            self.image.fill(self.TRANSPARENT_COLOR)
            self.image.blit(image_to_blit, (0, 0))

    def update(self, dt: float) -> None:
        """
        Updates the snake animation.
        Args:
        dt (float): The time since the last frame.
        """
        self.animation.update(dt)
        multiplicand: int = 1 if self.direction == "right" else -1  # -1 = snake heading left, 1 = snake heading right
        self.pos.x += self.speed * multiplicand * dt
        self.head_rect.x = int(self.pos.x + stgs.SNAKE_HEAD_RECT[self.direction][0])
        if self.direction == "right" and self.pos.x > stgs.WINDOW_SIZE[0]:
            self.game.get_middle_snake_time()
            self.game.middle_snake = None
        elif self.direction == "left" and self.pos.x < 0 - self.image_length:
            self.game.get_middle_snake_time()
            self.game.middle_snake = None

    def render(self, surf: pg.Surface) -> None:
        """
        Renders the snake onto the given surface.
        Args:
        surf (pg.Surface): The surface to render the snake onto.
        """
        self.get_current_image()
        surf.blit(self.image, (self.pos.x, self.pos.y - self.half_image_height))
        pg.draw.rect(surf, "red", self.head_rect, width=2)


class TreeSnake:
    TRANSPARENT_COLOR: Final[tuple[int, int, int, int]] = (0, 0, 0, 0)
    def __init__(self, game: "Game", tree_rect: pg.Rect, tree_speed: int) -> None:
        """
        Initializes an tree snake object.
        This snake appears on the large tree trunks every now and then.
        The direction is randomly chosen by the snake itself.
        Args:
        game: The game object.
        """
        self.game: "Game" = game
        self.tree_rect: pg.Rect = tree_rect
        self.tree_speed: int = tree_speed
        self.animation: Animation = self.game.animations["snake"].copy()
        self.image: pg.Surface
        self.direction: str = choice(["left", "right"])
        self.get_current_image()
        y_position: int = stgs.LANE_HEIGHTS["lane 8"]
        x_position: int = -180  # The large tree has a width of 400 pixel. It' scaled to 90% -> 360 pixel -> -360 / 2 => -180
        self.pos: pg.Vector2 = pg.Vector2((x_position, y_position))
        self.rect: pg.Rect = self.image.get_rect(center=self.pos)
        self.speed: int = stgs.SNAKE_SPEED
        self.create_head_rect()

    def create_head_rect(self) -> None:
        """ Creates a rectangle for the snake's head. """
        self.head_rect: pg.Rect = pg.Rect(self.pos.x + stgs.SNAKE_HEAD_RECT[self.direction][0], 
                                          self.pos.y - stgs.SNAKE_HEAD_RECT[self.direction][1], 
                                          stgs.SNAKE_HEAD_RECT[self.direction][2], 
                                          stgs.SNAKE_HEAD_RECT[self.direction][3])

    def get_current_image(self) -> None:
        """ Gets the current image of the animation and blits it on self.image. """
        image_to_blit: pg.Surface | bool = self.animation.get_current_image()
        if isinstance(image_to_blit, pg.Surface):
            if not hasattr(self, "image"):
                image_size: tuple[int, int] = image_to_blit.get_size()
                self.half_image_height: int = int(image_size[1] / 2)
                self.image_length: int = image_size[0]
                self.image: pg.Surface = pg.Surface(image_size, pg.SRCALPHA)
            flip: bool = True if self.direction == "right" else False
            image_to_blit = pg.transform.flip(image_to_blit, flip, False)
            self.image.fill(self.TRANSPARENT_COLOR)
            self.image.blit(image_to_blit, (0, 0))

    def update(self, dt: float) -> None:
        """
        Updates the snake animation and position.
        Args:
        dt (float): The time since the last frame.
        tree_rect (pg.Rect): The rectangle of the tree the snake is on.
        """
        self.animation.update(dt)
        multiplicand: int = 1 if self.direction == "right" else -1  # -1 = snake heading left, 1 = snake heading right
        self.pos.x += (self.tree_speed + (self.speed * multiplicand)) * dt
        self.head_rect.x = int(self.pos.x + stgs.SNAKE_HEAD_RECT[self.direction][0] - 42)  # <--------------- 42 in settings?
        self.rect.center = (int(self.pos.x), int(self.pos.y))
        if self.direction == "right":
            if self.head_rect.right >= self.tree_rect.right:
                self.direction = "left"
        elif self.direction == "left" :
            if self.head_rect.left <= self.tree_rect.left:
                self.direction = "right"
        if self.pos.x > stgs.WINDOW_SIZE[0] + 42:  # <--------------- 42 in settings?
            self.game.get_tree_snake_time()
            self.game.tree_snake = None

    def render(self, surf: pg.Surface) -> None:
        """
        Renders the snake onto the given surface.
        Args:
        surf (pg.Surface): The surface to render the snake onto.
        """
        self.get_current_image()
        surf.blit(self.image, self.rect)
        pg.draw.rect(surf, "red", self.rect, width=2)
        pg.draw.rect(surf, "red", self.head_rect, width=2)