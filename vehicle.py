import settings as stgs

import pygame as pg
from random import choice
from typing import Final, TYPE_CHECKING

if TYPE_CHECKING:
    from utils import Animation
    from game import Game
    
# [trunks, turtles, trunks, trunks, turtles, trucks, racing cars, cars, bulldozer, cars]
class Truck:
    def __init__(self, game: "Game", x: int, y: int) -> None:
        """
        Initialize a truck object.
        Args:
        game ("Game"): The game object.
        x (int): The center x-coordinate of the truck.
        y (int): The center y-coordinate of the truck.
        """
        self.game: "Game" = game
        self.pos: pg.Vector2 = pg.Vector2(x, y)
        self.speed: int = stgs.START_SPEED[f"level {str(self.game.level)}"][5]
        self.image: pg.Surface = (choice(self.game.image_lists["trucks"]))
        self.image = pg.transform.rotate(self.image, 180)
        self.rect: pg.Rect = self.image.get_rect(center=self.pos)
        self.half_image_width: int = int(self.game.image_lists["trucks"][1].get_width() // 2)

    def update(self, dt: float) -> None:
        """
        Update the truck's position.
        Args:
        dt (float): The time difference since the last update.
        """
        self.pos.x += self.speed * -1 * dt
        if self.pos.x < -self.half_image_width:
            self.pos.x = stgs.WINDOW_SIZE[0] + self.half_image_width
        self.rect.center = (int(self.pos.x), int(self.pos.y))  # collision_rect.center = tuple, self.pos = Vector2

    def rise_speed(self, amount: int) -> None:
        """
        Rise the truck's speed.
        Args:
        amount (int): The amount the speed should be risen.
        """
        self.speed += amount

    def render(self, surf: pg.Surface) -> None:
        """
        Render the truck to the given surface.
        Args:
        surf (pg.Surface): The surface to render the truck on.
        """
        surf.blit(self.image, self.rect)
        pg.draw.rect(surf, "red", self.rect, width=2)


class RacingCar:
    def __init__(self, game: "Game", x: int, y: int) -> None:
        """
        Initialize a racing car object.
        Args:
        game ("Game"): The game object.
        x (int): The center x-coordinate of the racing car.
        y (int): The center y-coordinate of the racing car.
        """
        self.game: "Game" = game
        self.pos: pg.Vector2 = pg.Vector2(x, y)
        self.speed: int = stgs.START_SPEED[f"level {str(self.game.level)}"][6]
        self.image: pg.Surface = (choice(self.game.image_lists["racing_cars"]))
        self.rect: pg.Rect = self.image.get_rect(center=self.pos)
        self.half_image_width: int = int(self.image.get_width() // 2)

    def update(self, dt: float) -> None:
        """
        Update the racing car's position.
        Args:
        dt (float): The time difference since the last update.
        """
        self.pos.x += self.speed * dt
        if self.pos.x > stgs.WINDOW_SIZE[0] + self.half_image_width:
            self.pos.x = -self.half_image_width
        self.rect.center = (int(self.pos.x), int(self.pos.y))  # collision_rect.center = tuple, self.pos = Vector2

    def rise_speed(self, amount: int) -> None:
        """
        Rise the racing car's speed.
        Args:
        amount (int): The amount the speed should be risen.
        """
        self.speed += amount

    def render(self, surf: pg.Surface) -> None:
        """
        Render the racing car to the given surface.
        Args:
        surf (pg.Surface): The surface to render the racing car on.
        """
        surf.blit(self.image, self.rect)
        pg.draw.rect(surf, "red", self.rect, width=2)


class LargeCar:
    def __init__(self, game: "Game", x: int, y: int) -> None:
        """
        Initialize a large car object.
        Args:
        game ("Game"): The game object.
        x (int): The center x-coordinate of the large car.
        y (int): The center y-coordinate of the large car.
        """
        self.game: "Game" = game
        self.pos: pg.Vector2 = pg.Vector2(x, y)
        self.speed: int = stgs.START_SPEED[f"level {str(self.game.level)}"][7]
        self.image: pg.Surface = (choice(self.game.image_lists["large_cars"]))
        self.image = pg.transform.rotate(self.image, 180)
        self.rect: pg.Rect = self.image.get_rect(center=self.pos)
        self.half_image_width: int = int(self.image.get_width() // 2)

    def update(self, dt: float) -> None:
        """
        Update the large car's position.
        Args:
        dt (float): The time difference since the last update.
        """
        self.pos.x += self.speed * -1 * dt
        if self.pos.x < -self.half_image_width:
            self.pos.x = stgs.WINDOW_SIZE[0] + self.half_image_width
        self.rect.center = (int(self.pos.x), int(self.pos.y))  # collision_rect.center = tuple, self.pos = Vector2

    def rise_speed(self, amount: int) -> None:
        """
        Rise the large car's speed.
        Args:
        amount (int): The amount the speed should be risen.
        """
        self.speed += amount

    def render(self, surf: pg.Surface) -> None:
        """
        Render the large car to the given surface.
        Args:
        surf (pg.Surface): The surface to render the large car on.
        """
        surf.blit(self.image, self.rect)
        pg.draw.rect(surf, "red", self.rect, width=2)


class Bulldozer:
    TRANSPARENT_COLOR: Final[tuple[int, int, int, int]] = (0, 0, 0, 0)
    def __init__(self, game: "Game", x: int, y: int) -> None:
        """
        Initialize a small car object.
        Args:
        game ("Game"): The game object.
        x (int): The center x-coordinate of the small car.
        y (int): The center y-coordinate of the small car.
        """
        self.game: "Game" = game
        self.pos: pg.Vector2 = pg.Vector2(x, y)
        self.speed: int = stgs.START_SPEED[f"level {str(self.game.level)}"][8]
        self.animation: Animation = self.game.animations["bulldozer"].copy()
        self.image: pg.Surface
        self.get_current_image()
        if isinstance(self.image, pg.Surface):
            self.half_image_width: int = int(self.image.get_width() // 2)
        self.rect: pg.Rect = self.image.get_rect(center=self.pos)

    def __iter__(self):
        yield self

    def get_current_image(self) -> None:
        image_to_blit = self.animation.get_current_image()
        if isinstance(image_to_blit, pg.Surface):

            if not hasattr(self, "image"):
                self.image: pg.Surface = pg.Surface(image_to_blit.get_size(), pg.SRCALPHA)
            self.image.fill(self.TRANSPARENT_COLOR)
            self.image.blit(image_to_blit, (0, 0)) 
            
    def update(self, dt: float) -> None:
        """
        Update the small car's position.
        Args:
        dt (float): The time difference since the last update.
        """
        self.animation.update(dt)
        self.image.fill(self.TRANSPARENT_COLOR)
        self.get_current_image()

        self.pos.x += self.speed * dt
        if self.pos.x > stgs.WINDOW_SIZE[0] + self.half_image_width:
            self.pos.x = -self.half_image_width
        self.rect.center = (int(self.pos.x), int(self.pos.y))  # collision_rect.center = tuple, self.pos = Vector2

    def rise_speed(self, amount: int) -> None:
        """
        Rise the Bulldozers speed.
        Args:
        amount (int): The amount the speed should be risen.
        """
        self.speed += amount

    def render(self, surf: pg.Surface) -> None:
        """
        Render the small car to the given surface.
        Args:
        surf (pg.Surface): The surface to render the small car on.
        """
        self.get_current_image()
        surf.blit(self.image, self.rect)
        pg.draw.rect(surf, "red", self.rect, width=2)


class SmallCar:
    def __init__(self, game: "Game", x: int, y: int) -> None:
        """
        Initialize a small car object.
        Args:
        game ("Game"): The game object.
        x (int): The center x-coordinate of the small car.
        y (int): The center y-coordinate of the small car.
        """
        self.game: "Game" = game
        self.pos: pg.Vector2 = pg.Vector2(x, y)
        self.speed: int = stgs.START_SPEED[f"level {str(self.game.level)}"][9]
        self.image: pg.Surface = (choice(self.game.image_lists["small_cars"]))
        self.image = pg.transform.rotate(self.image, 180)
        self.rect: pg.Rect = self.image.get_rect(center=self.pos)
        self.half_image_width: int = int(self.image.get_width() // 2)

    def update(self, dt: float) -> None:
        """
        Update the small car's position.
        Args:
        dt (float): The time difference since the last update.
        """
        self.pos.x += self.speed * -1 * dt
        if self.pos.x < -self.half_image_width:
            self.pos.x = stgs.WINDOW_SIZE[0] + self.half_image_width
        self.rect.center = (int(self.pos.x), int(self.pos.y))  # collision_rect.center = tuple, self.pos = Vector2

    def rise_speed(self, amount: int) -> None:
        """
        Set the small car's speed.
        Args:
        speed (int): The new speed of the small car.
        """
        self.speed += amount

    def render(self, surf: pg.Surface) -> None:
        """
        Render the small car to the given surface.
        Args:
        surf (pg.Surface): The surface to render the small car on.
        """
        surf.blit(self.image, self.rect)
        pg.draw.rect(surf, "red", self.rect, width=2)

