import settings as stgs

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
        self.game: Game = game
        self.pos: pg.Vector2 = pg.Vector2(pos)
        self.start_pos: pg.Vector2 = pg.Vector2(pos)
        self.destination: pg.Vector2 = pg.Vector2()
        self.direction: str = direction
        self.jumping: bool = False
        self.image: pg.Surface = pg.Surface(self.game.images["frog/test"].get_size(), pg.SRCALPHA)
        self.image.blit(self.game.images["frog/test"], (0, 0))
        self.rect: pg.Rect = self.image.get_rect(center=self.pos)
        self.speed: int = 200

    def update(self, dt: float) -> None:
        """
        Update the frog's position and state.
        Args:
        dt (float): The time elapsed since the last update.
        """
        if self.jumping:
            if self.direction == "north":
                self.pos.y -= (self.speed * dt)
                if self.pos.y <= self.destination.y:
                    self.pos.y = self.destination.y
                    self.jumping = False
            elif self.direction == "south":
                self.pos.y += (self.speed * dt)
                if self.pos.y >= self.destination.y:
                    self.pos.y = self.destination.y
                    self.jumping = False
            elif self.direction == "west":
                self.pos.x -= (self.speed * dt)
                if self.pos.x <= self.destination.x:
                    self.pos.x = self.destination.x
                    self.jumping = False
            elif self.direction == "east":
                self.pos.x += (self.speed * dt)
                if self.pos.x >= self.destination.x:
                    self.pos.x = self.destination.x
                    self.jumping = False
            print(self.jumping, self.pos)
            
        self.rect.x = self.pos.x
        self.rect.y = self.pos.y

    def jump(self, direction: str) -> None:
        """
        Make the frog jump in a specified direction.
        Args:
        direction (str): The direction to jump.
        """
        if not self.jumping:
            self.start_pos = self.pos
            if direction == "north" and self.pos.y >= 100:
                self.destination.y = self.pos.y - 42
            elif direction == "south" and self.pos.y <= 538:
                self.destination.y = self.pos.y + 42
            elif direction == "west" and self.pos.x > 42:
                self.destination.x = self.pos.x - 42
            elif direction == "east" and self.pos.y < stgs.WINDOW_SIZE[0] - 43:
                self.destination.x = self.pos.x + 42

        self.direction = direction
        self.jumping = True          

    def render(self, surf: pg.Surface) -> None:
        """
        Render the frog on the given surface.
        Args:
        surf (pg.Surface): The surface to render the frog on.
        """
        surf.blit(self.image, self.rect)