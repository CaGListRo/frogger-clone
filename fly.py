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
            self.game.get_house_fly_time()
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
    def __init__(self, game: Game, x_speed: int, tree_rect: pg.Rect) -> None:
        """ Initializes an fly object.
        Args:
        game (Game): The game object.
        """
        self.game: Game = game
        self.x_speed: int = x_speed
        self.tree_rect: pg.Rect = tree_rect
        self.state: str = "idle"
        self.pos: pg.Vector2 = pg.Vector2((-50, stgs.LANE_HEIGHTS["lane 7"]))  # the small trees width is 104.4 pixel
        self.speed: int = 32
        self.possible_states: list[str] = ["walk", "walk/flutter", "flutter"]
        self.get_animation()
        self.get_current_image()
        self.reset_state_timer()
        self.rect: pg.Rect = self.image.get_rect(center=self.pos)
        self.direction: int = 0
        
    def get_animation(self) -> None:
        """ Creates an animation object. """
        self.animation: Animation = self.game.animations[f"fly/{self.state}"]

    def choose_direction(self) -> None:
        """ Chooses the direction -1 for left, 1 for right. """
        self.direction = choice((-1, 1))

    def choose_state(self) -> None:
        """ Chooses the state of the fly. """
        self.state = choice(self.possible_states)

    def get_current_image(self) -> None:
        """ Gets the current image from the animation. """
        self.image: pg.Surface = self.animation.get_current_image()

    def reset_state_timer(self) -> None:
        """ Resets the state timer. """
        self.state_timer: float = stgs.FLY_STATE_TIMER

    def raise_x_speed(self, amount: int) -> None:
        """ Sets the new speed of the tree on which the fly sits on. """
        self.x_speed += amount

    def update(self, dt: float) -> None:
        """
        Updates the tree fly.
        Args:
        x_speed (int): The speed of the tree the fly is sitting on
        dt (float): The time difference between the last and current frame.
        """
        old_state: str = self.state
        self.state_timer -= dt
        if self.state_timer <= 0:
            self.choose_state()
            self.reset_state_timer()

        if old_state != self.state:
            self.get_animation()
        self.animation.update(dt)
        self.get_current_image()
        
        if self.state in ["walk", "walk/flutter"]:
            self.choose_direction()
            self.pos.x += ((self.speed * self.direction) + self.x_speed) * dt
        else:
            self.direction = 0
            self.pos.x += self.x_speed * dt

        if self.direction > 0 and self.rect.right > self.tree_rect.right:
            self.direction = -1
        elif self.direction < 0 and self.rect.left > self.tree_rect.left:
            self.direction = 1

        # self.tree_rect.x += self.x_speed
        self.rect.center = self.pos
        
        if self.pos.x > stgs.WINDOW_SIZE[0] + 25:
            self.game.get_tree_fly_time()
            self.game.tree_fly = None  

    def render(self, surf: pg.Surface) -> None:
        """
        Renders the fly onto the given surface.
        Args:
        surf (pg.Surface): The surface to render the fly onto.
        """
        if self.direction == 1:
            image_to_blit: pg.Surface = pg.transform.rotate(self.image, 90)
        elif self.direction == -1:
            image_to_blit: pg.Surface = pg.transform.rotate(self.image, 270)
        else:
            image_to_blit: pg.Surface = self.image

        surf.blit(image_to_blit, self.rect)
        pg.draw.rect(surf, "red", self.rect, width=1)
        pg.draw.rect(surf, "blue", self.tree_rect, width=3)
    
