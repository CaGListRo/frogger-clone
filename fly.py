import settings as stgs

import pygame as pg
from random import choice
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from utils import Animation
    from game import Game


class HouseFly:
    def __init__(self, game: "Game", pos: tuple[int, int]) -> None:
        """ Initializes an fly object.
        Args:
        game (Game): The game object.
        """
        self.game: "Game" = game
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
    def __init__(self, game: "Game", tree_speed: int, tree_rect: pg.Rect) -> None:
        """ Initializes an fly object.
        Args:
        game (Game): The game object.
        """
        self.game: "Game" = game
        self.tree_speed: int = tree_speed
        self.tree_rect: pg.Rect = tree_rect
        self.state: str = "idle"
        self.pos: pg.Vector2 = pg.Vector2((-50, stgs.LANE_HEIGHTS["lane 7"]))  # the small trees width is 104.4 pixel
        self.speed: int = stgs.FLY_WALK_SPEED
        self.possible_states: list[str] = ["walk", "walk/flutter", "flutter"]
        self.get_animation()
        self.get_current_image()
        self.reset_state_timer()
        self.rect: pg.Rect = self.image.get_rect(center=self.pos)
        self.direction: int = 0
        self.set_angle(angle=0)
        self.half_image_width: int = int(self.image.get_width() / 2)
        
    def get_animation(self) -> None:
        """ Creates an animation object. """
        state: str = self.state if self.state != "caught" else "flutter"
        self.animation: Animation = self.game.animations[f"fly/{state}"]

    def choose_direction(self) -> None:
        """ Chooses the direction -1 for left, 1 for right. """
        self.direction = choice((-1, 1))

    def set_angle(self) -> None:
        """ Sets self.angle according to self.direction. """
        if self.direction == 1:
            self.angle = 270
        elif self.direction == -1:
            self.angle = 90
        else:
            self.angle = 0

    def choose_state(self) -> None:
        """ Chooses the state of the fly. """
        self.state = choice(self.possible_states)

    def get_current_image(self) -> None:
        """ Gets the current image from the animation. """
        self.image: pg.Surface = self.animation.get_current_image()

    def reset_state_timer(self) -> None:
        """ Resets the state timer. """
        self.state_timer: float = stgs.FLY_STATE_TIMER * 2

    def raise_x_speed(self, amount: int) -> None:
        """ Sets the new speed of the tree on which the fly sits on. """
        self.tree_speed += amount

    def set_angle(self, angle: int) -> None:
        """ Sets the rotation angle of the fly. """
        self.angle: int = angle

    def handle_state_animation(self, dt: float) -> None:
        """
        Handles the state and the animation of the fly.
        Args:
        dt (float): The time difference between the last and current frame.
        """
        
        old_state: str = self.state
        if self.state != "caught":
            self.state_timer -= dt
            if self.state_timer <= 0:
                self.choose_state()
                self.reset_state_timer()
                if self.state in ["walk", "walk/flutter"]:
                    self.choose_direction()
                else:
                    self.direction = 0
                    self.set_angle(0)

        if old_state != self.state:
            self.get_animation()

        self.animation.update(dt)
        self.get_current_image()

    def move(self, dt: float) -> None:
        """
        Moves the fly.
        Args:
        dt (float): The time difference between the last and current frame.
        """
        if self.state in ["walk", "walk/flutter"]:
            self.pos.x += ((self.speed * self.direction) + self.tree_speed) * dt
        else: 
            self.pos.x += self.tree_speed * dt

        if self.direction == 1 and self.rect.right > self.tree_rect.right:
            self.rect.right = self.tree_rect.right
            self.pos.x = self.rect.right - self.half_image_width
            self.direction = -1
            self.set_angle(90)
        elif self.direction == -1 and self.rect.left < self.tree_rect.left:
            self.rect.left = self.tree_rect.left
            self.pos.x = self.rect.left + self.half_image_width
            self.direction = 1
            self.set_angle(270)

        self.rect.center = self.pos
        
        if self.pos.x > stgs.WINDOW_SIZE[0] + 25:
            self.game.get_tree_fly_time()
            self.game.tree_fly = None 

    def update(self, dt: float) -> None:
        """
        Updates the tree fly.
        Args:
        dt (float): The time difference between the last and current frame.
        """
        if self.state != "caught":
            self.handle_state_animation(dt)
            self.move(dt)
        else:
            self.handle_state_animation(dt)
        
    def render(self, surf: pg.Surface) -> None:
        """
        Renders the fly onto the given surface.
        Args:
        surf (pg.Surface): The surface to render the fly onto.
        """
        image_to_blit: pg.Surface = pg.transform.rotate(self.image, self.angle)
        surf.blit(image_to_blit, self.rect)
        pg.draw.rect(surf, "red", self.rect, width=1)
        pg.draw.rect(surf, "blue", self.tree_rect, width=1)
    
