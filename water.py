import settings as stgs

import pygame as pg
from random import choice
from typing import TypeVar, Final

Animation = TypeVar("Animation")
Game = TypeVar("Game")

class Tree:
    def __init__(self, game: Game, x: int, y: int, size: str, lane: int) -> None:
        """
        Initialize a tree object.
        Args:
        game (Game): The game object.
        x (int): The center x-coordinate of the tree.
        y (int): The center y-coordinate of the tree.
        size (str): The size of the tree. (large/medium/small)
        lane (int): The lane of the tree.
        """
        self.game: Game = game
        self.pos: tuple[int] = (x, y)
        self.speed: int = stgs.START_SPEED[f"level {str(self.game.level)}"][lane]
        self.image: pg.Surface = (choice(self.game.images[f"tree/{size}"]))
        self.rect: pg.Rect = self.image.get_rect(center=self.pos)
        self.half_image_width: int = int(self.image.get_width() // 2)

    def update(self, dt: float) -> None:
        """
        Update the tree's position.
        Args:
        dt (float): The time difference since the last update.
        """
        self.pos = (self.pos[0] + self.speed * dt, self.pos[1])
        if self.pos[0] > stgs.WINDOW_SIZE[0] + self.half_image_width:
            self.pos = (-self.half_image_width, self.pos[1])
        self.rect.center = self.pos

    def set_speed(self, speed: int) -> None:
        """
        Set the tree's speed.
        Args:
        speed (int): The new speed of the tree.
        """
        self.speed = speed

    def render(self, surf: pg.Surface) -> None:
        """
        Render the tree to the given surface.
        Args:
        surf (pg.Surface): The surface to render the tree on.
        """
        surf.blit(self.image, self.rect)


class Turtle:
    TRANSPARENT_COLOR: Final[tuple[int]] = (0, 0, 0, 0)
    def __init__(self, game: Game, x: int, y: int, lane: int, sinking: bool = False) -> None:
        """
        Initialize a turtle car object.
        Args:
        game (Game): The game object.
        x (int): The center x-coordinate of the turtle car.
        y (int): The center y-coordinate of the turtle car.
        """
        self.game: Game = game
        self.pos: tuple[int] = (x, y)
        self.speed: int = stgs.START_SPEED[f"level {self.game.level}"][lane]
        self.animation: Animation = self.game.images["test_turtle"].copy()
        image_to_blit: pg.Surface = self.animation.get_current_image()
        self.image: pg.Surface = pg.Surface(image_to_blit.get_size(), pg.SRCALPHA)
        self.image.fill(self.TRANSPARENT_COLOR)
        
        self.image.blit(image_to_blit, (0, 0))
        self.rect: pg.Rect = self.image.get_rect(center=self.pos)
        self.half_image_width: int = int(image_to_blit.get_width() // 2)

    def update(self, dt: float) -> None:
        """
        Update the turtle's position.
        Args:
        dt (float): The time difference since the last update.
        """
        self.animation.update(dt)
        self.image.fill(self.TRANSPARENT_COLOR)
        image_to_blit: pg.Surface = self.animation.get_current_image()
        self.image.blit(image_to_blit, (0, 0))

        self.pos = (self.pos[0] + self.speed * dt, self.pos[1])
        if self.pos[0] < 0 - self.half_image_width:
            self.pos = (stgs.WINDOW_SIZE[0] + self.half_image_width, self.pos[1])
        self.rect.center = self.pos

    def set_speed(self, speed: int) -> None:
        """
        Set the turtle's speed.
        Args:
        speed (int): The new speed of the turtle.
        """
        self.speed = speed

    def render(self, surf: pg.Surface) -> None:
        """
        Render the turtle to the given surface.
        Args:
        surf (pg.Surface): The surface to render the turtle on.
        """
        surf.blit(self.image, self.rect)