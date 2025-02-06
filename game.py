from utils import load_image, load_images
from utils import Animation
import settings as stgs
from frog import Frog

import pygame as pg
from time import perf_counter as pc
import sys
from typing import Final


class Game:
    START_POS: Final[tuple[int]] = (579, 300)
    FROG_SIZE: Final[tuple[int]] = (32, 32)
    def __init__(self) -> None:
        """ Initializes the game class. """
        pg.init()
        # set up screen
        self.screen: pg.display = pg.display.set_mode(stgs.WINDOW_SIZE)

        self.running: bool = True
        self.fps: int = 0

        # load images
        self.images: dict[pg.Surface] = {
            "background": load_image("background/Game background.png"),
            "cars": load_images("cars/"),
            "trucks": load_images("trucks/"),
            "stripe": load_image("objects/stripe.png", scale_factor=0.75),
            "bulldozer": Animation(load_images("bulldozer/"), animation_duration=0.1),
            "frog/house": load_image("frog/house/frog.png")
        }
        
        # create a frog
        self.frog: Frog = Frog(self, self.START_POS, self.FROG_SIZE)

        self.clear_houses()
        

    def clear_houses(self) -> None:
        """ Clears the houses list. """
        self.houses: list[int] = [True, True, True, True, True] #[False, False, False, False, False]

    def event_handler(self) -> None:
        """ Handles events in the game. """
        # get events
        for event in pg.event.get():
            # handle quit event
            if event.type == pg.QUIT:
                self.running = False

            # check key events
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_UP or event.key == pg.K_w:
                    self.frog.jump("north")
                if event.key == pg.K_DOWN or event.key == pg.K_s:
                    self.frog.jump("south")
                if event.key == pg.K_LEFT or event.key == pg.K_a:
                    self.frog.jump("west")
                if event.key == pg.K_RIGHT or event.key == pg.K_d:
                    self.frog.jump("east")

    def draw_screen(self) -> None:
        """ Draws the game screen. """
        pg.display.set_caption(f"     F R O G G E R - C L O N E          FPS:{self.fps}")
        # clear the screen
        self.screen.fill((0, 0, 0))
        # draw background
        self.screen.blit(self.images["background"], (0, 0))
        # draw stripes
        for i in range(4):
            for j in range(55):
                self.screen.blit(self.images["stripe"], (-5 + j * 32, 384 + i * 43))

        for i in range(5):
            multiplicand: int = 167 if i != 3 else 169
            self.screen.blit(self.images["frog/house"], (35 + i * multiplicand, 26))
        
        pg.display.update()

    def main(self) -> None:
        """ Runs the main game loop. """
        old_time: float = pc()
        fps_timer: float = 0.0
        fps_counter: int = 0
        while self.running:
            # calculate delta time
            dt: float = pc() - old_time
            old_time = pc()

            # count frames per second
            fps_timer += dt
            fps_counter += 1
            if fps_timer >= 1:
                self.fps = fps_counter
                fps_counter = 0
                fps_timer = 0.0

            # call the methods
            self.event_handler()
            self.draw_screen()

            # fps break
            if dt < 1 / 60:
                pg.time.wait(int(1000 * ((1 / 60) - dt)))
        
        
        pg.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.main()