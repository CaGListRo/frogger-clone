import settings as stgs

import pygame as pg
from icecream import ic
from typing import TypeVar, Final

Game = TypeVar("Game")
Animation = TypeVar("Animation")

class Frog:
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
        self.new_animation()
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
        self.dead: bool = False
        self.dead_timer: float = 0.0

        # collision stuff
        self.rect_size: tuple[int] = stgs.FROG_COLLISION_RECT
        self.collision_rect: pg.Rect = pg.Rect(self.pos.x - self.rect_size[0] // 2, self.pos.y + self.rect_size[1] // 2, self.rect_size[0], self.rect_size[1])

    def new_animation(self) -> None:
        """ Copies the animation from self.game.animations. """
        self.animation: Animation = self.game.animations[f"frog/{self.state}"].copy()

    def set_dead(self, kind: str) -> None:
        """ Sets the frog to be dead. """
        self.dead = True
        self.state = f"dead/{kind}"
        self.new_animation()

    def move_collision_rect(self) -> None:
        """ Moves the collision rect. """
        self.collision_rect.center = self.pos

    def update(self, dt: float) -> None:
        """
        Update the frog's position and state.
        Args:
        dt (float): The time elapsed since the last update.
        """
        if not self.dead:
            old_angle: int = self.angle
            old_state: str = self.state
            
            if self.jumping:
                self.state = "jump"
                if self.direction == "north":
                    self.pos.y -= (self.speed * dt)
                    self.angle = 0
                    if self.pos.y <= self.destination.y:
                        self.pos.y = self.destination.y
                        self.jumping = False

                elif self.direction == "south":
                    self.pos.y += (self.speed * dt)
                    self.angle = 180
                    if self.pos.y >= self.destination.y:
                        self.pos.y = self.destination.y
                        self.jumping = False

                elif self.direction == "west":
                    self.pos.x -= (self.speed * dt)
                    self.angle = 90
                    if self.pos.x <= self.destination.x:
                        self.pos.x = self.destination.x
                        self.jumping = False

                elif self.direction == "east":
                    self.pos.x += (self.speed * dt)
                    self.angle = 270
                    if self.pos.x >= self.destination.x:
                        self.pos.x = self.destination.x
                        self.jumping = False
                self.move_collision_rect()
            else:
                self.state = "idle"

            if old_angle != self.angle:
                self.rotate = True
            
            self.animation.update(dt)
            if self.animation.update(dt):
                self.state = "idle"
                self.new_animation()
                self.animation.update(dt)
            if old_state != self.state:
                self.new_animation()

        else:
            self.dead_timer += dt
            self.animation.update(dt)
            if self.dead_timer >= stgs.FROG_DEAD_TIME:
                self.game.new_frog_or_game_over()
        
    def jump(self, direction: str) -> None:
        """
        Make the frog jump in a specified direction.
        Args:
        direction (str): The direction to jump.
        """
        self.direction = direction
        if not self.jumping:
            self.game.score += stgs.SCORE["jump"]
            self.jumping = True 
            if direction == "north" and self.pos.y >= stgs.FROG_LIMITS["top"]:
                self.destination.y = self.pos.y - stgs.FROG_JUMP_DISTANCE
            elif direction == "south" and self.pos.y <= stgs.FROG_LIMITS["bottom"]:
                self.destination.y = self.pos.y + stgs.FROG_JUMP_DISTANCE
            elif direction == "west" and self.pos.x > stgs.FROG_LIMITS["left"]:
                self.destination.x = self.pos.x - stgs.FROG_JUMP_DISTANCE
            elif direction == "east" and self.pos.x < stgs.FROG_LIMITS["right"]:
                self.destination.x = self.pos.x + stgs.FROG_JUMP_DISTANCE

    def render(self, surf: pg.Surface) -> None:
        """
        Render the frog on the given surface.
        Args:
        surf (pg.Surface): The surface to render the frog on.
        """
        if isinstance(self.animation.get_current_image(), pg.Surface):
            self.image_to_blit = pg.transform.rotate(self.animation.get_current_image(), self.angle)
            self.image_rect = self.image_to_blit.get_rect(center=self.pos)
            surf.blit(self.image_to_blit, self.image_rect)
        pg.draw.rect(surf, "red", self.collision_rect, width=1)
