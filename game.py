from utils import load_image, load_images
from utils import Animation, Button
import settings as stgs
from snake import MiddleSnake
from fly import HouseFly
from frog import Frog
from vehicle import Truck, RacingCar, LargeCar, Bulldozer, SmallCar
from water import Tree, Turtle, Ripple, HouseCrocodile, LaneCrocodile
from time_bar import TimeBar

from icecream import ic

import pygame as pg
from time import perf_counter as pc
from random import choice
from random import randint as ri
import sys
from typing import Final


class Game:
    def __init__(self) -> None:
        """ Initializes the game class. """
        pg.init()
        # set up screen
        self.screen: pg.display = pg.display.set_mode(stgs.WINDOW_SIZE)

        self.running: bool = True
        self.fps: int = 0

        self.level: int = 2
        self.frog_time: int = 0                      # this ist the time one frog needed from the start to "his" house
        self.show_frog_time: bool = False            # In the original game the needed time is shown in the center of the screen
        self.show_time: float = stgs.SHOW_FROG_TIME  # how long the frog time is shown
        self.score: int = 0
        self.speed_ups: list[bool] = [False, False, False, False, False]
        self.game_state: str = "menu"

        # fonts
        self.score_font: pg.font.Font = pg.font.SysFont("Comic Sans", 32)

        # load images
        self.images: dict[pg.Surface] = {
            "game background": load_image("background/game background.png"),
            "menu background": load_image("background/menu background.png"),
            "house crocodile": load_image("crocodile/house/crocodile.png"),
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
            "crocodile/closed": Animation(load_images("crocodile/swimming closed/", scale_factor=0.9), animation_duration=1),
            "crocodile/open": Animation(load_images("crocodile/swimming open/", scale_factor=0.9), animation_duration=1),
            "fly/idle": Animation(load_images("fly/idle/", scale_factor=0.8), animation_duration=0.8),
            "fly/walk": Animation(load_images("fly/walk/", scale_factor=0.8), animation_duration=0.8),
            "fly/walk/flutter": Animation(load_images("fly/walk flutter/", scale_factor=0.8), animation_duration=0.8),
            "fly/flutter": Animation(load_images("fly/flutter/", scale_factor=0.8), animation_duration=0.8),
            "frog/idle": Animation(load_images("frog/idle/", scale_factor=0.85), animation_duration=1),
            "frog/jump": Animation(load_images("frog/jump/", scale_factor=0.85), animation_duration=0.4, loop=False),
            "frog/dead/street": Animation(load_images("frog/dead/street/"), animation_duration=stgs.FROG_DEAD_TIME, loop=False),
            "frog/dead/water": Animation(load_images("frog/dead/water/"), animation_duration=stgs.FROG_DEAD_TIME, loop=False),
            "snake": Animation(load_images("snake/", scale_factor=0.8), animation_duration=0.6),
            "turtle/swimming": Animation(load_images("turtle/swimming/", scale_factor=0.9), animation_duration=1),
            "turtle/diving": Animation(load_images("turtle/diving/", scale_factor=0.9), animation_duration=3, loop=False),
        }

        self.direction_pressed: bool = False
        
        self.initialize_menu()
        self.initialize_game()  # <------------------------------------------ MOVE WHEN GAME STATES GET IMPLEMENTED

        self.house_rects: list[pg.Rect] = [pg.Rect(stgs.HOUSE_TOP_LEFT[0][0], stgs.HOUSE_TOP_LEFT[0][1], stgs.HOUSE_SIZE[0], stgs.HOUSE_SIZE[1]),
                                           pg.Rect(stgs.HOUSE_TOP_LEFT[1][0], stgs.HOUSE_TOP_LEFT[1][1], stgs.HOUSE_SIZE[0], stgs.HOUSE_SIZE[1]),
                                           pg.Rect(stgs.HOUSE_TOP_LEFT[2][0], stgs.HOUSE_TOP_LEFT[2][1], stgs.HOUSE_SIZE[0], stgs.HOUSE_SIZE[1]),
                                           pg.Rect(stgs.HOUSE_TOP_LEFT[3][0], stgs.HOUSE_TOP_LEFT[3][1], stgs.HOUSE_SIZE[0], stgs.HOUSE_SIZE[1]),
                                           pg.Rect(stgs.HOUSE_TOP_LEFT[4][0], stgs.HOUSE_TOP_LEFT[4][1], stgs.HOUSE_SIZE[0], stgs.HOUSE_SIZE[1]),]
        
        self.gras_rects: list[pg.Rect] = [pg.Rect(element) for element in stgs.GRAS_RECTS]

        # entities
        self.house_crocodile: None | HouseCrocodile = None
        self.house_fly: None | HouseFly = None
        self.middle_snake: None | MiddleSnake = None
        
    def initialize_menu(self) -> None:
        """ Initialize the game menu. """
        self.start_button: Button = Button(100, 100, "Start", "green")

    def initialize_game(self) -> None:
        """ Initializes the game. """
        self.frogs: int = 7
        self.clear_houses()
        self.create_ripples()
        self.create_traffic()
        self.create_water_traffic()
        self.create_frog()
        self.create_time_bar()
        if stgs.CROCOS_IN_HOUSES[self.level - 1]:
            self.get_crocodile_time()
        if stgs.SNAKES[self.level - 1]:
            self.get_snake_time()
        self.get_fly_time()

    def get_crocodile_time(self) -> None:
        """ Sets the time of the next appearance of a crocodile in a house. """
        self.crocodile_time: int | float = ri(10, 30)

    def get_snake_time(self) -> None:
        """ Sets the time of the next appearance of the snake. """
        self.snake_time: int | float = ri(5, 10)

    def get_fly_time(self) -> None:
        """ Sets the time of the next appearance of the fly. """
        self.fly_time: int | float = ri(10, 30)

    def calculate_time_score(self) -> None:
        """ Calculates the score for the remaining time. """
        self.score += self.time_bar.get_time() * 10

    def create_new_ripple(self) -> None:
        """ Creates a new ripple at a random y-position. """
        self.ripples.append(Ripple(self, pos=(-10, ri(25, 258))))

    def create_ripples(self) -> None:
        """ Creates a list of ripples. """
        self.ripples: list[Ripple] = [Ripple(self, pos=(-5 + i * ri(30, 60), ri(50, 284))) for i in range(100)]

    def create_house_crocodile(self) -> None:
        """ Creates a crocodile in a random house. """
        self.house_crocodile = HouseCrocodile(self, ri(0, 4))

    def create_house_fly(self) -> None:
        """ Creates a fly in a random house. """
        self.house_fly = HouseFly(self, stgs.FLY_HOUSE_CENTER_POS[ri(0, 4)])

    def create_frog(self) -> None:
        """ Creates a frog at the start position. """
        self.frog: Frog = Frog(self, stgs.FROG_START_POS)
        self.frogs -= 1

    def create_middle_snake(self) -> None:
        """ Creates a snake that crawls over the green in the middle of the screen. """
        self.middle_snake = MiddleSnake(self)

    def create_water_traffic(self) -> None:
        """ Creates water traffic. """
        crocodile: int = 10  # choose a high number to never get a crocodile if in the level is no crocodile
        if stgs.CROCOS_SWIMMING[self.level - 1]:
            crocodile = ri(0, stgs.WATER[f"level {self.level}"][0] - 1)

        sinking_pair: int = ri(0, stgs.WATER[f"level {self.level}"][1] - 1)
        sinking_trio: int = ri(0, stgs.WATER[f"level {self.level}"][4] - 1)

        self.water_traffic: list[Animation | pg.Surface] = [
            [LaneCrocodile(self, 750 - i * stgs.SPACING["lane 10"][self.level - 1], stgs.LANE_HEIGHTS["lane 10"], 0) if i == crocodile else Tree(self, 750 - i * stgs.SPACING["lane 10"][self.level - 1], stgs.LANE_HEIGHTS["lane 10"], "medium", 0) for i in range(stgs.WATER[f"level {self.level}"][0])],
            [Turtle(self, 150 + i * stgs.SPACING["lane 9"][self.level - 1], stgs.LANE_HEIGHTS["lane 9"], 1, True if i == sinking_pair else False)  for i in range(stgs.WATER[f"level {self.level}"][1])],
            [Tree(self, 650 - i * stgs.SPACING["lane 8"][self.level - 1], stgs.LANE_HEIGHTS["lane 8"], "large", 2) for i in range(stgs.WATER[f"level {self.level}"][2])],
            [Tree(self, 450 - i * stgs.SPACING["lane 7"][self.level - 1], stgs.LANE_HEIGHTS["lane 7"], "small", 3) for i in range(stgs.WATER[f"level {self.level}"][3])],
            [Turtle(self, 250 + i * stgs.SPACING["lane 6"][self.level - 1], stgs.LANE_HEIGHTS["lane 6"], 4, True if i == sinking_trio else False) for i in range(stgs.WATER[f"level {self.level}"][4])],
        ]

    def create_time_bar(self) -> None:
        """ Creates a time bar at the bottom of the screen. """
        self.time_bar: TimeBar = TimeBar(self)

    def create_traffic(self) -> None:
        """ Creates traffic on the road. """
        self.traffic: list[Animation | pg.Surface] = [
            [Truck(self, 700 - i * stgs.SPACING["lane 5"][self.level - 1], stgs.LANE_HEIGHTS["lane 5"]) for i in range(stgs.STREET[f"level {self.level}"][0])],
            [RacingCar(self, 400 - i * stgs.SPACING["lane 4"][self.level - 1], stgs.LANE_HEIGHTS["lane 4"]) for i in range(stgs.STREET[f"level {self.level}"][1])],
            [LargeCar(self, 800 - i * stgs.SPACING["lane 3"][self.level - 1], stgs.LANE_HEIGHTS["lane 3"]) for i in range(stgs.STREET[f"level {self.level}"][2])],
            [Bulldozer(self, 400 - i * stgs.SPACING["lane 2"][self.level - 1], stgs.LANE_HEIGHTS["lane 2"]) for i in range(stgs.STREET[f"level {self.level}"][3])],
            [SmallCar(self, 600 - i * stgs.SPACING["lane 1"][self.level - 1], stgs.LANE_HEIGHTS["lane 1"]) for i in range(stgs.STREET[f"level {self.level}"][4])],]

    def clear_houses(self) -> None:
        """ Clears the houses list. """
        self.houses: list[int] = [False, False, False, False, False]

    def new_frog_or_game_over(self) -> None:
        """ Checks if a new frog can be created or if the game is over. """
        if self.frogs > 0:  
            self.handle_time_bar()
            self.create_frog()
        else:
            raise NotImplementedError

    def handle_time_bar(self) -> None:
        """ Deletes the old time bar and creates a new one. """
        del self.time_bar
        self.create_time_bar()

    def handle_water_traffic_collision(self, collision_object: object, lane_index, element_index) -> bool:
        """
        Handles collision with water traffic.
        Args:
        collision_object: The object that collided with the frog.
        lane_index: The index of the lane where the collision occurred.
        element_index: The index of the element in the lane where the collision occurred.
        """
        collided: bool = False
        offset: float = self.distances[lane_index][element_index]
        if self.frog.collision_rect.left >= collision_object.rect.left - 10 and self.frog.collision_rect.right <= collision_object.rect.right + 10:
            collided = True
            if self.frog.collision_rect.top <= collision_object.rect.bottom - 19 and self.frog.collision_rect.bottom >= collision_object.rect.top + 19:
                if not self.frog.jumping:
                    self.frog.pos.x = collision_object.pos.x + offset
                    self.frog.move_collision_rect()
        return collided

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
        # collisions with traffic on the street
        for lane in self.traffic:
            for vehicle in lane:
                if self.frog.collision_rect.colliderect(vehicle.rect):
                    self.frog.set_dead("street")

        # collision with the snake head
        if self.middle_snake != None:
            if self.frog.collision_rect.colliderect(self.middle_snake.head_rect):
                self.frog.set_dead("water")
 
        # collisions with water traffic
        collided_list: list[bool] = []
        for lane_index, lane in enumerate(self.water_traffic):
            for element_index, element in enumerate(lane):
                if lane_index == 1 or lane_index == 4:  # lane_index 1 and 4 are the turtles
                    if not element.diving:
                        collided: bool = self.frog.collision_rect.colliderect(element.rect)
                        collided_list.append(collided)
                else:
                    collided: bool = self.frog.collision_rect.colliderect(element.rect)
                    collided_list.append(collided)
                if collided:
                    self.handle_water_traffic_collision(element, lane_index, element_index)
        
        # collision with the gras around the houses -> death of one frog
        for gras_rect in self.gras_rects:
            if self.frog.collision_rect.colliderect(gras_rect):
                self.frog.set_dead("water")

        # collision with the house rects
        for idx, rect in enumerate(self.house_rects):
            if self.frog.collision_rect.colliderect(rect) and not self.frog.dead:
                if self.house_crocodile:
                    if self.house_rects[idx].colliderect(self.house_crocodile.rect):
                        self.frog.set_dead("water")
                else:
                    if not self.houses[idx]:
                        self.houses[idx] = True
                        self.calculate_time_score()
                        if self.house_fly:
                            if self.house_rects[idx].colliderect(self.house_fly.rect):
                                self.score += stgs.FLY_SCORES["house fly"]
                                self.get_fly_time()
                        if False in self.houses:
                            self.frog_time = 60 - self.time_bar.get_time()  # the time the frog needed to get home
                            self.show_frog_time = True
                            self.new_frog_or_game_over()
                        else:
                            self.proceed_level()
                    else:
                        self.frog.set_dead("water")

        # collision with the water
        if self.frog.pos.y <= stgs.FROG_WATER_COLLISION_HEIGHT and True not in collided_list:
            self.frog.set_dead("water")

    def check_speed_up(self) -> None:
        """ Checks if the traffic according to the score has to sped up. """
        for idx, score in enumerate(stgs.SPEED_UP_SCORE):
            if self.score >= score and not self.speed_ups[idx]:
                self.speed_up_traffic(self.level * 10)
                self.speed_ups[idx] = True
            elif self.score >= score and self.speed_ups[idx]:
                continue
            else:
                break

    def proceed_level(self) -> None:
        """ Proceeds to the next level. """
        if self.level < 5:
            self.level += 1
            self.initialize_game()
        else:
            raise NotImplementedError

    def speed_up_traffic(self, amount: int) -> None:
        """ Speeds up the traffic by a certain amount. """
        for lane in self.traffic:
            for vehicle in lane:
                vehicle.rise_speed(amount)
        for lane in self.water_traffic:
            for element in lane:
                element.rise_speed(amount)

    def time_up(self) -> None:
        """ Is called from the time bar object, if the time is up. """
        self.new_frog_or_game_over()

    def event_handler(self) -> None:
        """ Handles events in the game. """
        # get events
        for event in pg.event.get():
            # handle quit event
            if event.type == pg.QUIT:
                self.running = False
            
            # check key events while playing the game
            if self.game_state == "play":
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
        """
        Updates all objects in the game.
        Args:
        dt (float): The time since the last update.
        """
        # update time bar
        self.time_bar.update(dt)

        # update ripples
        for ripple in self.ripples:
            ripple.update(dt)

        # update the water traffic
        for lane in self.water_traffic:
            for element in lane:
                element.update(dt)

        # update house fly
        if self.house_fly:
            self.house_fly.update(dt)

        # update house crocodile
        if self.house_crocodile:
            self.house_crocodile.update(dt)

        # update middle snake
        if self.middle_snake:
            self.middle_snake.update(dt)

        # update the frog
        self.frog.update(dt)

        # update the traffic on the street
        for lane in self.traffic:
            for vehicle in lane:
                vehicle.update(dt)

    def update_variables(self, dt: float) -> None:
        """
        Updates all variables in the game.
        Args:
        dt (float): The time since the last update.
        """  
        # update frog time
        if self.show_frog_time:
            self.show_time -= dt
            if self.show_time <= 0:
                self.show_frog_time = False
                self.show_time = stgs.SHOW_FROG_TIME

        # update fly time
        self.fly_time -= dt
        if self.fly_time <= 0 and self.house_fly == None:
            self.create_house_fly()

        # update snake time
        if stgs.SNAKES[self.level - 1] and self.middle_snake == None:
            self.snake_time -= dt
            if self.snake_time <= 0:
                self.create_middle_snake()

        # update crocodile time if there is a crocodile in the level
        if stgs.CROCOS_IN_HOUSES[self.level - 1] and self.house_crocodile == None:
            self.crocodile_time -= dt
            if self.crocodile_time <= 0:
                self.create_house_crocodile()

    def render_game(self) -> None:
        """ Renders the game while playing. """
        # draw houses to have a background behind the background
        self.screen.blit(self.images["houses"], (0, 0))
        # draw background
        self.screen.blit(self.images["game background"], (0, 26))
        # draw ripples
        for ripple in self.ripples:
            ripple.render(self.screen)
        # draw stripes
        for i in range(4):
            for j in range(55):
                pos: tuple[int] = (stgs.STRIPES["x start"] + j * stgs.STRIPES["x spacing"], 
                                   stgs.STRIPES["y start"] + i * stgs.STRIPES["y spacing"])
                self.screen.blit(self.images["stripe"], pos)
        # draw water traffic
        for lane in self.water_traffic:
            for element in lane:
                element.render(self.screen)
        # draw frog time
        if self.show_frog_time:
            time_to_blit: pg.Surface = self.score_font.render(f"{int(self.frog_time)} Seconds", True, "white", "black")
            pos: tuple[int] = (int(stgs.WINDOW_SIZE[0] // 2 - time_to_blit.get_width() // 2), 
                               int(stgs.WINDOW_SIZE[1] // 2 - time_to_blit.get_height() // 2))
            self.screen.blit(time_to_blit, pos)
        # draw house crocodile
        if self.house_crocodile:
            self.house_crocodile.render(self.screen)
        # draw house fly
        if self.house_fly:
            self.house_fly.render(self.screen)
        # draw frog
        self.frog.render(self.screen)
        # draw traffic
        for lane in self.traffic:
            for vehicle in lane:
                vehicle.render(self.screen)
        # draw snake
        if self.middle_snake:
            self.middle_snake.render(self.screen)
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

        # showing gras rects for testing
        for gras_rect in self.gras_rects:
            pg.draw.rect(self.screen, "darkorange", gras_rect, width=1)
            
        # draw time bar
        self.time_bar.render(self.screen)

    def draw_screen(self) -> None:
        """ Draws the game screen. """
        pg.display.set_caption(f"     F R O G G E R - C L O N E          FPS:{self.fps}")
        # clear the screen
        self.screen.fill((0, 0, 0))
        if self.game_state == "menu":
            self.screen.blit(self.images["menu background"], (0, 0))
            self.start_button.render(self.screen)
        elif self.game_state == "play":
            self.render_game()
                
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

            # check for traffic speed ups
            self.check_speed_up()

            # playing the game
            if self.game_state == "play":
                self.update_variables(dt)
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