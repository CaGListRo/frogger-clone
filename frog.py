import settings as stgs

import pygame as pg

from typing import TypeVar, Final

Game = TypeVar("Game")
Animation = TypeVar("Animation")

class Frog:
    JUMP_DISTANCE: Final[int] = 43
    def __init__(self, game: Game, pos: tuple[int], direction: str = "north") -> None:
        """
        Initialize a Frog object.
        Args:
        pos (tuple[int]): The initial position of the frog.
        size (tuple[int]): The size of the frog.
        direction (str): The initial direction of the frog. Defaults to "north".
        """        
        self.game: Game = game
        self.state: str = "idle"
        self.animation: Animation = self.game.images[f"frog/{self.state}"].copy()
        image_size: tuple[int] = self.animation.get_current_image().get_size()
        frog_pos: tuple[int] = (int(pos[0] - image_size[0] / 2), pos[1])
        self.pos: pg.Vector2 = pg.Vector2(frog_pos)
        self.image: pg.Surface = pg.Surface(image_size, pg.SRCALPHA)
        self.image.blit(self.animation.get_current_image(), (0, 0))
        self.rect: pg.Rect = self.image.get_rect(topleft=self.pos)
        self.speed: int = 200
        self.jumping: bool = False
        self.direction: str = direction
        self.destination: pg.Vector2 = pg.Vector2()

    def update(self, dt: float) -> None:
        """
        Update the frog's position and state.
        Args:
        dt (float): The time elapsed since the last update.
        """
        self.animation.update(dt)
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
            if direction == "north" and self.pos.y >= 100:
                self.destination.y = self.pos.y - self.JUMP_DISTANCE
            elif direction == "south" and self.pos.y <= 538:
                self.destination.y = self.pos.y + self.JUMP_DISTANCE
            elif direction == "west" and self.pos.x > self.JUMP_DISTANCE:
                self.destination.x = self.pos.x - self.JUMP_DISTANCE
            elif direction == "east" and self.pos.x < stgs.WINDOW_SIZE[0] - self.JUMP_DISTANCE:
                self.destination.x = self.pos.x + self.JUMP_DISTANCE

        self.direction = direction
        self.jumping = True          

    def render(self, surf: pg.Surface) -> None:
        """
        Render the frog on the given surface.
        Args:
        surf (pg.Surface): The surface to render the frog on.
        """
        surf.blit(self.image, self.rect)