import settings as stgs

import pygame as pg
from random import choice
from typing import TypeVar

Game = TypeVar("Game")
Animation = TypeVar("Animation")


class HouseFly:
    def __init__(self, game: Game, pos: tuple[int]) -> None:
        """ Initializes an fly object.
        Args:
        game (Game): The game object.
        """
        self.game: Game = game
        self.state: str = "idle"
        self.get_animation()
        self.get_current_image()
        self.rect: pg.Rect = self.image.get_rect(center=pos)
        self.possible_states: list[str] = ["idle", "flutter"]
        self.state_timer: float = stgs.FLY_STATE_TIMER
        self.stay_time: float = stgs.FLY_STAY_TIME

    def update(self, dt: float) -> None:
        """
        Updates the fly object.
        Args:
        dt (float): The time difference between the last and current frame.
        """
        old_state = self.state
        self.state_timer -= dt
        if self.state_timer <= 0:
            self.state = choice(self.possible_states)
            self.state_timer = stgs.FLY_STATE_TIMER
        if old_state != self.state:
            self.get_animation()
        self.animation.update(dt)
        self.get_current_image()
        self.stay_time -= dt
        if self.stay_time <= 0:
            self.game.house_fly = None
        
    def get_animation(self) -> None:
        """ Gets a copy of the current animation from self.games.animations. """
        self.animation: Animation = self.game.animations[f"fly/{self.state}"]

    def get_current_image(self) -> None:
        """ Gets the current image from the animation. """
        self.image: pg.Surface = self.animation.get_current_image()

    def render(self, surf: pg.Surface) -> None:
        """
        Renders the fly onto the given surface.
        Args:
        surf (pg.Surface): The surface to render the fly onto.
        """
        surf.blit(self.image, self.rect)
        pg.draw.rect(surf, "red", self.rect, width=1)


class TreeFly:
    def __init__(self, game: Game) -> None:
        """ Initializes an fly object.
        Args:
        game (Game): The game object.
        """
        self.game: Game = game
        self.state: str = "idle"