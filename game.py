from utils import load_image, load_images
from utils import Animation
import settings as stgs
from snake import Snake
from frog import Frog
from vehicle import Truck, RacingCar, LargeCar, Bulldozer, SmallCar
from water import Tree, Turtle, Ripple

from icecream import ic

import pygame as pg
from time import perf_counter as pc
from random import randint as ri
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

        self.level: int = 1
        self.frogs: int = 7
        self.score: int = 0

        # fonts
        self.score_font: pg.font.Font = pg.font.SysFont("Comic Sans", 32)

        # load images
        self.images: dict[pg.Surface] = {
            "background": load_image("background/game background.png"),
            "houses": load_image("background/houses background.png"),
            "tree/large": load_images("objects/large trees/", scale_factor=0.9),
            "tree/medium": load_images("objects/medium trees/", scale_factor=0.9),
            "tree/small": load_images("objects/small trees/", scale_factor=0.9),
            "trucks": load_images("trucks/"),
            "racing_cars": load_images("racing cars/", scale_factor=0.8),
            "large_cars": load_images("large cars/", scale_factor=0.9),            
            "small_cars": load_images("small cars/", scale_factor=0.85),
            "stripe": load_image("objects/stripe.png", scale_factor=0.75),
            "frog/house": load_image("frog/house/frog.png"),
            "frog/life": load_image("frog/idle/frog0001.png", scale_factor=0.7),
            "ripple": load_images("water/", scale_factor=2),
        }

        # create animations
        self.animations: dict[Animation] = {
            "bulldozer": Animation(load_images("bulldozer/", scale_factor=0.9), animation_duration=0.4),
            "frog/idle": Animation(load_images("frog/idle/", scale_factor=0.85), animation_duration=1),
            "frog/jump": Animation(load_images("frog/jump/", scale_factor=0.85), animation_duration=0.4, loop=False),
            "turtle/swimming": Animation(load_images("turtle/swimming/", scale_factor=0.9), animation_duration=1),
            "snake": Animation(load_images("snake/", scale_factor=0.8), animation_duration=0.6)
        }

        self.direction_pressed: bool = False
        
        self.clear_houses()
        self.create_traffic()
        self.create_water_traffic()
        self.create_frog()

        self.ripples: list[Ripple] = [Ripple(self, pos=(-5 + i * ri(30, 60), ri(25, 258))) for i in range(100)]
        self.house_rects: list[pg.Rect] = [pg.Rect(stgs.HOUSE_TOP_LEFT[0][0], stgs.HOUSE_TOP_LEFT[0][1], stgs.HOUSE_SIZE[0], stgs.HOUSE_SIZE[1]),
                                           pg.Rect(stgs.HOUSE_TOP_LEFT[1][0], stgs.HOUSE_TOP_LEFT[1][1], stgs.HOUSE_SIZE[0], stgs.HOUSE_SIZE[1]),
                                           pg.Rect(stgs.HOUSE_TOP_LEFT[2][0], stgs.HOUSE_TOP_LEFT[2][1], stgs.HOUSE_SIZE[0], stgs.HOUSE_SIZE[1]),
                                           pg.Rect(stgs.HOUSE_TOP_LEFT[3][0], stgs.HOUSE_TOP_LEFT[3][1], stgs.HOUSE_SIZE[0], stgs.HOUSE_SIZE[1]),
                                           pg.Rect(stgs.HOUSE_TOP_LEFT[4][0], stgs.HOUSE_TOP_LEFT[4][1], stgs.HOUSE_SIZE[0], stgs.HOUSE_SIZE[1]),]

        # test snake
        self.snake: Snake = Snake(self)

    def create_new_ripple(self) -> None:
        """ Creates a new ripple at a random y-position. """
        self.ripples.append(Ripple(self, pos=(-10, ri(25, 258))))

    def create_frog(self) -> None:
        """ Creates a frog at the start position. """
        self.frog: Frog = Frog(self, stgs.FROG_START_POS)
        self.frogs -= 1

    def create_water_traffic(self) -> None:
        """ Creates water traffic. """
        self.water_traffic: list[Animation | pg.Surface] = [
            [Tree(self, 750 - i * stgs.SPACING["lane 10"], stgs.LANE_HEIGHTS["lane 10"], "medium", 0) for i in range(stgs.WATER[f"level {self.level}"][0])],
            [Turtle(self, 150 + i * stgs.SPACING["lane 9"], stgs.LANE_HEIGHTS["lane 9"], 1)  for i in range(stgs.WATER[f"level {self.level}"][1])],
            [Tree(self, 650 - i * stgs.SPACING["lane 8"], stgs.LANE_HEIGHTS["lane 8"], "large", 2) for i in range(stgs.WATER[f"level {self.level}"][2])],
            [Tree(self, 450 - i * stgs.SPACING["lane 7"], stgs.LANE_HEIGHTS["lane 7"], "small", 3) for i in range(stgs.WATER[f"level {self.level}"][3])],
            [Turtle(self, 250 + i * stgs.SPACING["lane 6"], stgs.LANE_HEIGHTS["lane 6"], 4) for i in range(stgs.WATER[f"level {self.level}"][4])],
        ]
        
    def create_traffic(self) -> None:
        """ Creates traffic on the road. """
        self.traffic: list[Animation | pg.Surface] = [
            [Truck(self, 700 - i * stgs.SPACING["lane 5"], stgs.LANE_HEIGHTS["lane 5"]) for i in range(stgs.STREET[f"level {self.level}"][0])],
            [RacingCar(self, 400 - i * stgs.SPACING["lane 4"], stgs.LANE_HEIGHTS["lane 4"]) for i in range(stgs.STREET[f"level {self.level}"][1])],
            [LargeCar(self, 800 - i * stgs.SPACING["lane 3"], stgs.LANE_HEIGHTS["lane 3"]) for i in range(stgs.STREET[f"level {self.level}"][2])],
            [Bulldozer(self, 400 - i * stgs.SPACING["lane 2"], stgs.LANE_HEIGHTS["lane 2"]) for i in range(stgs.STREET[f"level {self.level}"][3])],
            [SmallCar(self, 600 - i * stgs.SPACING["lane 1"], stgs.LANE_HEIGHTS["lane 1"]) for i in range(stgs.STREET[f"level {self.level}"][4])],]

    def clear_houses(self) -> None:
        """ Clears the houses list. """
        self.houses: list[int] = [False, False, False, False, False]

    def new_frog_or_game_over(self) -> None:
        """ Checks if a new frog can be created or if the game is over. """
        if self.frogs > 0:
            self.create_frog()
        else:
            raise NotImplementedError

    def handle_water_traffic_collision(self, collision_object: object, lane_index, element_index) -> None:
        """
        Handles collision with water traffic.
        Args:
        collision_object: The object that collided with the frog.
        lane_index: The index of the lane where the collision occurred.
        element_index: The index of the element in the lane where the collision occurred.
        """
        offset: float = self.distances[lane_index][element_index]
        if self.frog.collision_rect.top <= collision_object.rect.bottom - 19 and self.frog.collision_rect.bottom >= collision_object.rect.top + 19:
            if not self.frog.jumping:
                self.frog.pos.x = collision_object.pos.x + offset
                self.frog.move_collision_rect()        

    def calculate_distances(self) -> None:
        """ Checks the distances on the x axis from the frog to the water objects. """
        self.distances: list[int] = []
        for idx, lane in enumerate(self.water_traffic):
            lane_list: list[int] = []
            for element in lane:
                    lane_list.append(self.frog.pos.x - element.pos.x)
            self.distances.append(lane_list)

    def check_collisions(self) -> None:
        """ Checks for collisions between the player and other objects. """
        # # collisions with traffic
        # for lane in self.traffic:
        #     for vehicle in lane:
        #         if self.frog.collision_rect.colliderect(vehicle.rect):
        #             del self.frog
        #             self.new_frog_or_game_over()
        
        # collisions with water traffic
        for lane_index, lane in enumerate(self.water_traffic):
            for element_index, element in enumerate(lane):
                if self.frog.collision_rect.colliderect(element.rect):
                    self.handle_water_traffic_collision(element, lane_index, element_index)
        
        # collision with the house rects
        for idx, rect in enumerate(self.house_rects):
            if self.frog.collision_rect.colliderect(rect):
                if not self.houses[idx]:
                    self.houses[idx] = True
                    self.new_frog_or_game_over()
                else:
                    self.new_frog_or_game_over()  # needs to be changed when there is a dying animation
                    
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
                    self.direction_pressed = True
                if event.key == pg.K_DOWN or event.key == pg.K_s:
                    self.direction_pressed = True
                if event.key == pg.K_LEFT or event.key == pg.K_a:
                    self.direction_pressed = True
                if event.key == pg.K_RIGHT or event.key == pg.K_d:
                    self.direction_pressed = True

            if event.type == pg.KEYUP and not self.frog.jumping:
                if (event.key == pg.K_UP or event.key == pg.K_w) and self.direction_pressed:
                    self.frog.jump("north")
                    self.direction_pressed = False
                if (event.key == pg.K_DOWN or event.key == pg.K_s) and self.direction_pressed:
                    self.frog.jump("south")
                    self.direction_pressed = False
                if (event.key == pg.K_LEFT or event.key == pg.K_a) and self.direction_pressed:
                    self.frog.jump("west")
                    self.direction_pressed = False
                if (event.key == pg.K_RIGHT or event.key == pg.K_d) and self.direction_pressed:
                    self.frog.jump("east")
                    self.direction_pressed = False
                
    def update_objects(self, dt: float) -> None:
        # update ripples
        for ripple in self.ripples:
            ripple.update(dt)
        # update test snake
        self.snake.update(dt)
        # update the water traffic
        for lane in self.water_traffic:
            for element in lane:
                element.update(dt)

        # update the frog
        self.frog.update(dt)
        # update the traffic on the street
        for lane in self.traffic:
            for vehicle in lane:
                vehicle.update(dt)

    def draw_screen(self) -> None:
        """ Draws the game screen. """
        pg.display.set_caption(f"     F R O G G E R - C L O N E          FPS:{self.fps}")
        # clear the screen
        self.screen.fill((0, 0, 0))
        # draw houses to have a background behind the background
        self.screen.blit(self.images["houses"], (0, 0))
        # draw background
        self.screen.blit(self.images["background"], (0, 26))
        # draw ripples
        for ripple in self.ripples:
            ripple.render(self.screen)
        # draw stripes
        for i in range(4):
            for j in range(55):
                self.screen.blit(self.images["stripe"], (stgs.STRIPES["x start"] + j * stgs.STRIPES["x spacing"], stgs.STRIPES["y start"] + i * stgs.STRIPES["y spacing"]))
        # draw water traffic
        for lane in self.water_traffic:
            for element in lane:
                element.render(self.screen)

        # draw frog
        self.frog.render(self.screen)
        # draw traffic
        for lane in self.traffic:
            for vehicle in lane:
                vehicle.render(self.screen)
        # draw snake
        self.snake.render(self.screen)
        # draw houses
        self.screen.blit(self.images["houses"], (0, 26))
        # draw house rects for test
        for rect in self.house_rects:
            pg.draw.rect(self.screen, "red", rect, width=1)
        # render and blit score
        score_shadow: pg.Surface = self.score_font.render(f"Score: {str(self.score)}", True, "black")
        score_to_blit: pg.Surface = self.score_font.render(f"Score: {str(self.score)}", True, "white")
        self.screen.blit(score_shadow, (12, 2))
        self.screen.blit(score_to_blit, (10, 0))
        # draw frogs in houses if they're at home
        for i in range(5):
            if self.houses[i]:
                multiplicand: int = 167 if i != 3 else 169
                self.screen.blit(self.images["frog/house"], (35 + i * multiplicand, 52))
        # draw the remaining frogs
        for i in range(self.frogs):
            self.screen.blit(self.images["frog/life"], (10 + i * 32, stgs.FROG_DRAW_HEIGHT))
        
        pg.display.update()

    def main(self) -> None:
        """ Runs the main game loop. """
        self.calculate_distances()
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

            self.update_objects(dt)
            self.check_collisions()
            if self.frog.pos.y <= 333:
                self.calculate_distances()

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