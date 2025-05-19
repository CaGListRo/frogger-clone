import settings as stgs

import pygame as pg
from random import choice
from typing import TypeVar, Final

Animation = TypeVar("Animation")
Game = TypeVar("Game")
    
# [trunks, turtles, trunks, trunks, turtles, trucks, racing cars, cars, bulldozer, cars]
class Truck:
    def __init__(self, game: Game, x: int, y: int) -> None:
        """
        Initialize a truck object.
        Args:
        game (Game): The game object.
        x (int): The center x-coordinate of the truck.
        y (int): The center y-coordinate of the truck.
        """
        self.game: Game = game
        self.pos: pg.Vector2 = pg.Vector2(x, y)
        self.speed: int = stgs.START_SPEED[f"level {str(self.game.level)}"][5]
        self.image: pg.Surface = (choice(self.game.images["trucks"]))
        self.image = pg.transform.rotate(self.image, 180)
        self.rect: pg.Rect = self.image.get_rect(center=self.pos)
        self.half_image_width: int = int(self.game.images["trucks"][1].get_width() // 2)

    def update(self, dt: float) -> None:
        """
        Update the truck's position.
        Args:
        dt (float): The time difference since the last update.
        """
        self.pos.x += self.speed * -1 * dt
        if self.pos.x < -self.half_image_width:
            self.pos.x = stgs.WINDOW_SIZE[0] + self.half_image_width
        self.rect.center = self.pos

    def rise_speed(self, amount: int) -> None:
        """
        Set the truck's speed.
        Args:
        speed (int): The new speed of the truck.
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
    def __init__(self, game: Game, x: int, y: int) -> None:
        """
        Initialize a racing car object.
        Args:
        game (Game): The game object.
        x (int): The center x-coordinate of the racing car.
        y (int): The center y-coordinate of the racing car.
        """
        self.game: Game = game
        self.pos: pg.Vector2 = pg.Vector2(x, y)
        self.speed: int = stgs.START_SPEED[f"level {str(self.game.level)}"][6]
        self.image: pg.Surface = (choice(self.game.images["racing_cars"]))
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
        self.rect.center = self.pos

    def rise_speed(self, amount: int) -> None:
        """
        Set the racing car's speed.
        Args:
        speed (int): The new speed of the racing car.
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
    def __init__(self, game: Game, x: int, y: int) -> None:
        """
        Initialize a large car object.
        Args:
        game (Game): The game object.
        x (int): The center x-coordinate of the large car.
        y (int): The center y-coordinate of the large car.
        """
        self.game: Game = game
        self.pos: pg.Vector2 = pg.Vector2(x, y)
        self.speed: int = stgs.START_SPEED[f"level {str(self.game.level)}"][7]
        self.image: pg.Surface = (choice(self.game.images["large_cars"]))
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
        self.rect.center = self.pos

    def rise_speed(self, amount: int) -> None:
        """
        Set the large car's speed.
        Args:
        speed (int): The new speed of the large car.
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
    TRANSPARENT_COLOR: Final[tuple[int]] = (0, 0, 0, 0)
    def __init__(self, game: Game, x: int, y: int) -> None:
        """
        Initialize a small car object.
        Args:
        game (Game): The game object.
        x (int): The center x-coordinate of the small car.
        y (int): The center y-coordinate of the small car.
        """
        self.game: Game = game
        self.pos: pg.Vector2 = pg.Vector2(x, y)
        self.speed: int = stgs.START_SPEED[f"level {str(self.game.level)}"][8]
        self.animation: Animation = self.game.animations["bulldozer"].copy()
        image_to_blit: pg.Surface = self.animation.get_current_image()
        self.image: pg.Surface = pg.Surface(image_to_blit.get_size(), pg.SRCALPHA)
        self.image.fill(self.TRANSPARENT_COLOR)
        
        self.image.blit(image_to_blit, (0, 0))
        self.rect: pg.Rect = self.image.get_rect(center=self.pos)
        self.half_image_width: int = int(image_to_blit.get_width() // 2)

    def __iter__(self):
        yield self

    def update(self, dt: float) -> None:
        """
        Update the small car's position.
        Args:
        dt (float): The time difference since the last update.
        """
        self.animation.update(dt)
        self.image.fill(self.TRANSPARENT_COLOR)
        image_to_blit: pg.Surface = self.animation.get_current_image()
        self.image.blit(image_to_blit, (0, 0))

        self.pos.x += self.speed * dt
        if self.pos.x > stgs.WINDOW_SIZE[0] + self.half_image_width:
            self.pos.x = -self.half_image_width
        self.rect.center = self.pos

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


class SmallCar:
    def __init__(self, game: Game, x: int, y: int) -> None:
        """
        Initialize a small car object.
        Args:
        game (Game): The game object.
        x (int): The center x-coordinate of the small car.
        y (int): The center y-coordinate of the small car.
        """
        self.game: Game = game
        self.pos: pg.Vector2 = pg.Vector2(x, y)
        self.speed: int = stgs.START_SPEED[f"level {str(self.game.level)}"][9]
        self.image: pg.Surface = (choice(self.game.images["small_cars"]))
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
        self.rect.center = self.pos

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

