import settings as stgs

import pygame as pg
from random import choice, randint
from typing import TypeVar, Final
from icecream import ic

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
        self.pos: pg.Vector2 = pg.Vector2((x, y))
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
        self.pos.x += self.speed * dt
        if self.pos.x > stgs.WINDOW_SIZE[0] + self.half_image_width:
            self.pos.x = -self.half_image_width
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
        pg.draw.rect(surf, "red", self.rect, width=2)


class Turtle:
    TRANSPARENT_COLOR: Final[tuple[int]] = (0, 0, 0, 0)
    def __init__(self, game: Game, x: int, y: int, lane: int, sinkable: bool = False) -> None:
        """
        Initialize a turtle object.
        Args:
        game (Game): The game object.
        x (int): The center x-coordinate of the turtle.
        y (int): The center y-coordinate of the turtle.
        lane (int): The lane of the turtle.
        sinkable (bool): Whether the turtle can dive. Defaults to False.
        """
        self.game: Game = game
        self.pos: pg.Vector2 = pg.Vector2((x, y))
        self.speed: int = stgs.START_SPEED[f"level {self.game.level}"][lane]
        self.sinkable: bool = sinkable  # the general ability to dive
        self.state: str = "swimming"
        self.diving: bool = False     # if it is actually diving
        self.get_new_animation()
        
        image_to_blit: pg.Surface = self.animation.get_current_image()
        surface_selector: int = 0 if lane == 1 else 1
        self.turtles_selector: int = 0 if lane == 1 else 1
        self.image_size: tuple[int] = stgs.TURTLE_SURFACE[surface_selector]
        self.image: pg.Surface = pg.Surface(self.image_size, pg.SRCALPHA)
        self.draw_image(image_to_blit=image_to_blit)
        
        self.rect: pg.Rect = self.image.get_rect(center=self.pos)

        if self.sinkable:
            self.dive_timer: int | float = stgs.TURTLE_DIVE_TIME[self.game.level - 1]
            self.carry_timer: int | float = stgs.TURTLE_FROG_CARRY_TIME

    def get_new_animation(self) -> None:
        """ Get a new animation for the turtle. """
        self.animation: Animation = self.game.animations[f"turtle/{self.state}"].copy()

    def update(self, dt: float) -> None:
        """
        Update the turtle's position.
        Args:
        dt (float): The time difference since the last update.
        """
        old_state: str = self.state
        if self.sinkable:
            self.dive_timer -= dt
            if self.dive_timer <= 0:
                self.state = "diving"
                self.carry_timer -= dt
                if self.carry_timer <= 0:
                    self.diving = True if not self.diving else False
                    self.carry_timer = stgs.TURTLE_FROG_CARRY_TIME
        
        if self.animation.update(dt):
            self.state = "swimming"
            self.diving = False
            self.dive_timer = stgs.TURTLE_DIVE_TIME[self.game.level - 1]
        if old_state != self.state:
            self.get_new_animation()

        self.image.fill(self.TRANSPARENT_COLOR)
        image_to_blit: pg.Surface = self.animation.get_current_image()
        self.draw_image(image_to_blit=image_to_blit)

        self.pos.x += self.speed * dt
        if self.pos.x < 0 - self.image_size[0] // 2:
            self.pos.x = stgs.WINDOW_SIZE[0] + self.image_size[0] // 2

        self.rect.center = self.pos

    def set_speed(self, speed: int) -> None:
        """
        Set the turtle's speed.
        Args:
        speed (int): The new speed of the turtle.
        """
        self.speed = speed

    def draw_image(self, image_to_blit: pg.Surface) -> None:
        """ Draw the turtle's image. """
        self.image.fill(self.TRANSPARENT_COLOR)
        for i in range(stgs.TURTLES[self.turtles_selector]):
            self.image.blit(image_to_blit, (0 + i * stgs.TURTLE_SPACING, 0))
        
    def render(self, surf: pg.Surface) -> None:
        """
        Render the turtle to the given surface.
        Args:
        surf (pg.Surface): The surface to render the turtle on.
        """
        surf.blit(self.image, self.rect)
        #pg.draw.rect(surf, "red", self.rect, width=2)


class Ripple:
    def __init__(self, game: Game, pos: tuple[int]) -> None:
        """
        Initialize a ripple.
        Args:
        game (Game): The game instance.
        pos (tuple[int]): The position of the ripple.
        """
        self.game: Game = game
        self.pos: pg.Vector2 = pg.Vector2(pos)
        self.image: pg.Surface = choice(self.game.images["ripple"])
        self.speed: int = randint(30, 90)
        self.timer: float = 0.0
        self.change_time: float = 0.3

    def update(self, dt: float) -> None:
        """
        Update the ripple's position.
        Args:
        dt (float): The time difference since the last update.
        """
        # system to change the image of the ripple for mor natural look
        self.timer += dt
        if self.timer >= self.change_time:
            self.image = choice(self.game.images["ripple"])
            self.timer = 0.0
        # make it go right
        self.pos.x += self.speed * dt
        # delete it, if it is of screen
        if self.pos.x > stgs.WINDOW_SIZE[0]:
            self.game.ripples.remove(self)
            self.game.create_new_ripple()

    def render(self, surf: pg.Surface) -> None:
        """
        Render the ripple to the given surface.
        Args:
        surf (pg.Surface): The surface to render the ripple on.
        """
        surf.blit(self.image, (int(self.pos.x), int(self.pos.y)))


class LaneCrocodile:
    pass


class HouseCrocodile:
    def __init__(self, game: Game, house: int) -> None:
        """
        Initialize a house crocodile object.
        Args:
        game (Game): The game instance.
        house (int): The number of the house in which the crocodile should appear.
        """