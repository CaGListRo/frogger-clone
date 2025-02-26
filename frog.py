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
        # image stuff
        self.state: str = "idle"
        self.animation: Animation = self.game.images[f"frog/{self.state}"].copy()
        image_size: tuple[int] = self.animation.get_current_image().get_size()
        self.image: pg.Surface = pg.Surface(image_size, pg.SRCALPHA)
        self.image.blit(self.animation.get_current_image(), (0, 0))
        self.image_to_blit: pg.Surface = self.image
        self.image_rect: pg.Rect = self.image.get_rect(center=pos)
        
        # frog stuff
        frog_pos: tuple[int] = (int(pos[0] - image_size[0] / 2), pos[1])
        self.pos: pg.Vector2 = pg.Vector2(frog_pos)
        self.destination: pg.Vector2 = pg.Vector2()
        self.speed: int = 200
        self.jumping: bool = False
        self.direction: str = direction
        self.old_direction: str = self.direction
        self.angle: int = 0
        self.rotate: bool = False

        # collision stuff
        self.offset: tuple[int] = (-14, -37)     # collision rect offset
        self.rect_size: tuple[int] = (29, 37)  # collision rect size
        self.collision_rect: pg.Rect = pg.Rect(self.pos.x + self.offset[0], self.pos.y + self.offset[1], self.rect_size[0], self.rect_size[1])

    def fix_position(self) -> None:
        """ Fix the position of the frog after a change of direction. """
        if self.direction == "south":
            match self.old_direction:
                case "north":
                    self.pos.y -= 38
                    self.offset = (-14, 0)
                    self.collision_rect.y = self.pos.y + self.offset[1]
                case "east":
                    self.pos.x += 19
                    self.pos.y -= 19
                    self.offset = (37, 14)
                    self.rect_size = (29, 37)
                    self.collision_rect = pg.Rect(self.pos.x + self.offset[0], self.pos.y + self.offset[1], self.rect_size[0], self.rect_size[1])
                case "west":
                    self.pos.x -= 19
                    self.pos.y -= 19
                    self.offset = (-14, -37)
                    self.rect_size = (29, 37)
                    self.collision_rect = pg.Rect(self.pos.x + self.offset[0], self.pos.y + self.offset[1], self.rect_size[0], self.rect_size[1])

        elif self.direction == "north":
            match self.old_direction:
                case "south":
                    self.pos.y += 38
                    self.offset = (-14, -37)
                    self.collision_rect.y = self.pos.y + self.offset[1]
                case "east":
                    self.pos.x += 19
                    self.pos.y += 19
                    self.offset = (-14, -37)
                    self.rect_size = (29, 37)
                    self.collision_rect = pg.Rect(self.pos.x + self.offset[0], self.pos.y + self.offset[1], self.rect_size[0], self.rect_size[1])
                case "west":
                    self.pos.x -= 19
                    self.pos.y += 19
                    self.offset = (-14, -37)
                    self.rect_size = (29, 37)
                    self.collision_rect = pg.Rect(self.pos.x + self.offset[0], self.pos.y + self.offset[1], self.rect_size[0], self.rect_size[1])

        elif self.direction == "west":
            match self.old_direction:
                case "north":
                    self.pos.x += 19
                    self.pos.y -= 19
                    self.offset = (-14, -37)
                    self.rect_size = (37, 29)
                    self.collision_rect = pg.Rect(self.pos.x + self.offset[0], self.pos.y + self.offset[1], self.rect_size[0], self.rect_size[1])
                case "south":
                    self.pos.x += 19
                    self.pos.y += 19
                    self.offset = (-14, -37)
                    self.rect_size = (37, 29)
                    self.collision_rect = pg.Rect(self.pos.x + self.offset[0], self.pos.y + self.offset[1], self.rect_size[0], self.rect_size[1])
                case "east":
                    self.pos.x += 38
                    self.offset = (-37, -14)
                    self.collision_rect.x = self.pos.x + self.offset[0]
            
        elif self.direction == "east":
            match self.old_direction:
                case "north":
                    self.pos.x -= 19
                    self.pos.y -= 19
                    self.offset = (-14, -37)
                    self.rect_size = (37, 29)
                    self.collision_rect = pg.Rect(self.pos.x + self.offset[0], self.pos.y + self.offset[1], self.rect_size[0], self.rect_size[1])
                case "south":
                    self.pos.x -= 19
                    self.pos.y += 19    
                    self.offset = (-14, -37)
                    self.rect_size = (37, 29)
                    self.collision_rect = pg.Rect(self.pos.x + self.offset[0], self.pos.y + self.offset[1], self.rect_size[0], self.rect_size[1])
                case "west":
                    self.pos.x -= 38
                    self.offset = (0, -14)
                    self.collision_rect.x = self.pos.x + self.offset[0]
        self.old_direction = self.direction

    def update(self, dt: float) -> None:
        """
        Update the frog's position and state.
        Args:
        dt (float): The time elapsed since the last update.
        """
        old_angle: int = self.angle
        old_state: str = self.state
        
        if self.jumping:
            self.state = "jump"
            if self.direction == "north":
                self.pos.y -= (self.speed * dt)
                self.angle = 0
                self.collision_rect.y -= (self.speed * dt)
                if self.pos.y <= self.destination.y:
                    self.pos.y = self.destination.y
                    self.jumping = False

            elif self.direction == "south":
                self.pos.y += (self.speed * dt)
                self.angle = 180
                self.collision_rect.y += (self.speed * dt)
                if self.pos.y >= self.destination.y:
                    self.pos.y = self.destination.y
                    self.jumping = False

            elif self.direction == "west":
                self.pos.x -= (self.speed * dt)
                self.angle = 90
                self.collision_rect.x -= (self.speed * dt)
                if self.pos.x <= self.destination.x:
                    self.pos.x = self.destination.x
                    self.jumping = False

            elif self.direction == "east":
                self.pos.x += (self.speed * dt)
                self.angle = 270
                self.collision_rect.x += (self.speed * dt)
                if self.pos.x >= self.destination.x:
                    self.pos.x = self.destination.x
                    self.jumping = False
        else:
            self.state = "idle"

        if old_angle != self.angle:
            self.rotate = True
        
        if old_state != self.state:
            self.animation: Animation = self.game.images[f"frog/{self.state}"].copy()
        self.animation.update(dt)

    def jump(self, direction: str) -> None:
        """
        Make the frog jump in a specified direction.
        Args:
        direction (str): The direction to jump.
        """
        self.direction = direction
        if not self.jumping:
            self.jumping = True 
            if direction == "north" and self.pos.y >= 100:
                if self.old_direction != direction:
                    self.fix_position()
                self.destination.y = self.pos.y - self.JUMP_DISTANCE
            elif direction == "south" and self.pos.y <= 538:
                if self.old_direction != direction:
                    self.fix_position()
                self.destination.y = self.pos.y + self.JUMP_DISTANCE
            elif direction == "west" and self.pos.x > self.JUMP_DISTANCE:
                if self.old_direction != direction:
                    self.fix_position()
                self.destination.x = self.pos.x - self.JUMP_DISTANCE
            elif direction == "east" and self.pos.x < stgs.WINDOW_SIZE[0] - self.JUMP_DISTANCE:
                if self.old_direction != direction:
                    self.fix_position()
                self.destination.x = self.pos.x + self.JUMP_DISTANCE

    def render(self, surf: pg.Surface) -> None:
        """
        Render the frog on the given surface.
        Args:
        surf (pg.Surface): The surface to render the frog on.
        """

        self.image_to_blit = pg.transform.rotate(self.animation.get_current_image(), self.angle)

        self.image_rect = self.image_to_blit.get_rect(center=self.pos)
        surf.blit(self.image_to_blit, self.image_rect)
        pg.draw.rect(surf, "red", self.collision_rect, width=1)
