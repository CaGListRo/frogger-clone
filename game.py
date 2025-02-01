from utils import load_image, load_images
import settings as stgs

import pygame as pg
from time import perf_counter as pc
import sys


class Game:
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
        }

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
                    print("Up key pressed")
                if event.key == pg.K_DOWN or event.key == pg.K_s:
                    print("Down key pressed")
                if event.key == pg.K_LEFT or event.key == pg.K_a:
                    print("Left key pressed")
                if event.key == pg.K_RIGHT or event.key == pg.K_d:
                    print("Right key pressed")

    def draw_screen(self) -> None:
        """ Draws the game screen. """
        pg.display.set_caption(f"     F R O G G E R - C L O N E          FPS:{self.fps}")
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.images["background"], (0, 0))
        
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