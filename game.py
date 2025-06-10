from utils import load_image, load_images, load_sound
from utils import Animation, Button
import settings as stgs
from snake import MiddleSnake, TreeSnake
from fly import HouseFly, TreeFly
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
from typing import List, Union


class Game:
    def __init__(self) -> None:
        """ Initializes the game class. """
        pg.init()
        # set up screen
        self.screen: pg.Surface = pg.display.set_mode(stgs.WINDOW_SIZE)

        # game and frog settings
        self.running: bool = True
        self.fps: int = 0
        self.level: int = 3
        self.frog_time: int = 0                      # this is the time one frog needed from the start to "his" house
        self.show_frog_time: bool = False            # In the original game the needed time is shown in the center of the screen
        self.show_time: float = stgs.SHOW_FROG_TIME  # this is how long the frog time is shown
        self.score: int = 0
        self.speed_ups: List[bool] = [False, False, False, False, False]
        self.game_state: str = "menu"
        self.languages: List[str] = [language for language in stgs.BUTTON_NAMES["language"]]
        self.language: str = self.languages[1]
        self.back_button: None | Button = None
        self.pause_key_pressed: bool = False
        self.show_pause_text: bool = True
        self.blink_timer: float = stgs.BLINK_TIME
        self.direction_pressed: bool = False
        self.player_name: str = ""

        # fonts
        self.info_font: pg.font.Font = pg.font.SysFont("Comic Sans", 18)
        self.pause_font: pg.font.Font = pg.font.SysFont("Comic Sans", 55)
        self.pause_text_font: pg.font.Font = pg.font.SysFont("Comic Sans", 23)
        self.score_font: pg.font.Font = pg.font.SysFont("Comic Sans", 32)
        
        # load images
        self.image: dict[str, pg.Surface] = {
            "game background": load_image("background/game background.png"),
            "highscores background": load_image("background/highscores background.png"),
            "menu background": load_image("background/menu background.png"),
            "options background": load_image("background/options background.png"),
            "house crocodile": load_image("crocodile/house/crocodile.png"),
            "houses": load_image("background/houses background.png"),
            "stripe": load_image("objects/stripe.png", scale_factor=0.75),
            "frog/house": load_image("frog/house/frog.png"),
            "frog/life": load_image("frog/idle/frog0001.png", scale_factor=0.7)
        }        
        self.image_lists: dict[str, List[pg.Surface]] = {
            "tree/large": load_images("objects/large trees/", scale_factor=0.9),
            "tree/medium": load_images("objects/medium trees/", scale_factor=0.9),
            "tree/small": load_images("objects/small trees/", scale_factor=0.9),
            "trucks": load_images("trucks/"),
            "racing_cars": load_images("racing cars/", scale_factor=0.8),
            "large_cars": load_images("large cars/", scale_factor=0.9),            
            "small_cars": load_images("small cars/", scale_factor=0.85),
            "ripple": load_images("water/", scale_factor=2),
        }

        # create animations
        self.animations: dict[str, Animation] = {
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
 
        # collision rects
        self.house_rects: List[pg.Rect] = [pg.Rect(stgs.HOUSE_TOP_LEFT[0][0], stgs.HOUSE_TOP_LEFT[0][1], stgs.HOUSE_SIZE[0], stgs.HOUSE_SIZE[1]),
                                           pg.Rect(stgs.HOUSE_TOP_LEFT[1][0], stgs.HOUSE_TOP_LEFT[1][1], stgs.HOUSE_SIZE[0], stgs.HOUSE_SIZE[1]),
                                           pg.Rect(stgs.HOUSE_TOP_LEFT[2][0], stgs.HOUSE_TOP_LEFT[2][1], stgs.HOUSE_SIZE[0], stgs.HOUSE_SIZE[1]),
                                           pg.Rect(stgs.HOUSE_TOP_LEFT[3][0], stgs.HOUSE_TOP_LEFT[3][1], stgs.HOUSE_SIZE[0], stgs.HOUSE_SIZE[1]),
                                           pg.Rect(stgs.HOUSE_TOP_LEFT[4][0], stgs.HOUSE_TOP_LEFT[4][1], stgs.HOUSE_SIZE[0], stgs.HOUSE_SIZE[1]),]
        self.gras_rects: List[pg.Rect] = [pg.Rect(element) for element in stgs.GRAS_RECTS]

        # entities
        self.house_crocodile: None | HouseCrocodile = None
        self.house_fly: None | HouseFly = None
        self.middle_snake: None | MiddleSnake = None
        self.tree_fly: None | TreeFly = None
        self.tree_fly_ready: bool = False
        self.tree_snake: None | TreeSnake = None
        self.tree_snake_ready: bool = False

        # audio
        pg.mixer.init()
        self.music_enabled: bool = True
        self.sound_enabled: bool = True
        self.music_volume: float = 0.75
        self.sound_volume: float = 0.75
        self.music_key_pressed: bool = False
        self.sound_key_pressed: bool = False
        self.sounds: dict[str, pg.mixer.Sound] = {
            "frog/jump 1": load_sound("jump 1"),
            "frog/jump 2": load_sound("jump 2"),
            "racing car": load_sound("racing car")
        }
        
        self.initialize_menu()

    def calculate_time_score(self) -> None:
        """ Calculates the score for the remaining time. """
        self.score += self.time_bar.get_time() * stgs.SCORE["second"]

    def calculate_distances(self) -> None:
        """ Checks the distances on the x axis from the frog to the water objects. """
        self.distances: List[List[int]] = []
        for _, lane in enumerate(self.water_traffic):
            lane_list: List[int] = []
            for element in lane:
                lane_list.append(int(self.frog.pos.x - element.pos.x))
            self.distances.append(lane_list)

    def check_buttons(self) -> None:
        """ Checks if the buttons are pressed. """
        if self.game_state == "menu":
            for idx, button in enumerate(self.menu_buttons):
                if button.check_clicked():
                    match idx:
                        case 0:
                            self.game_state = "play"
                            self.initialize_game()
                        case 1:
                            self.create_back_button()
                            self.create_language_buttons()
                            self.load_info()
                            self.game_state = "options"
                        case 2:
                            self.game_state = "highscores"
                            self.create_back_button()
                        case 3:
                            self.running = False

        elif self.game_state == "options" or self.game_state == "highscores":
            if self.back_button and self.back_button.check_clicked():
                self.game_state = "menu"
                self.back_button = None
                self.language_buttons = []
            if self.game_state == "options":   
                for idx, button in enumerate(self.language_buttons):
                    old_language: str = self.language
                    if button.check_clicked():
                        self.language = self.languages[idx]
                    if old_language != self.language:
                        self.create_menu_buttons()
                        self.create_back_button()
                        self.load_info()

    def check_collisions(self) -> None:
        """ Checks for collisions between the player and other objects. """
        # collisions with traffic on the street
        for lane in self.traffic:
            for vehicle in lane:
                if self.frog.collision_rect.colliderect(vehicle.rect):
                    self.frog.set_dead("street")

        # collision with the snake head rects
        if self.middle_snake != None:
            if self.frog.collision_rect.colliderect(self.middle_snake.head_rect):
                self.frog.set_dead("water")
        if self.tree_snake != None:
            if self.frog.collision_rect.colliderect(self.tree_snake.head_rect):
                self.frog.set_dead("water")

        # collision with the tree fly
        if self.tree_fly != None:
            if self.frog.collision_rect.colliderect(self.tree_fly.rect):
                self.frog.carry_fly = True
                self.tree_fly.state = "caught"
                self.tree_fly.rect.center = self.frog.collision_rect.center
 
        # collisions with water traffic
        collided_list: List[bool] = []
        collided: bool = False
        for lane_index, lane in enumerate(self.water_traffic):
            for element_index, element in enumerate(lane):
                if lane_index == 0 and isinstance(element, LaneCrocodile):
                    if element.state == "open" and self.frog.collision_rect.colliderect(element.head_rect):
                        self.frog.set_dead("water")
                if lane_index == 1 or lane_index == 4:  # lane_index 1 and 4 are the turtles
                    if not element.diving:
                        collided = self.frog.collision_rect.colliderect(element.rect)
                        collided_list.append(collided)
                else:
                    collided = self.frog.collision_rect.colliderect(element.rect)
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
                                self.get_house_fly_time()
                        if self.tree_fly and self.tree_fly.state == "caught":
                            self.score += stgs.FLY_SCORES["tree fly"]
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

    def create_menu_buttons(self) -> None:
        """ Creates the buttons for the menu. """
        self.menu_buttons: List[Button] = [        
            Button(pos=stgs.BUTTON_POSITIONS["start"], size=stgs.BUTTON_SIZE, text=stgs.BUTTON_NAMES["start"][self.language], color="green"),
            Button(pos=stgs.BUTTON_POSITIONS["options"], size=stgs.BUTTON_SIZE, text=stgs.BUTTON_NAMES["options"][self.language], color="beige"),
            Button(pos=stgs.BUTTON_POSITIONS["highscores"], size=stgs.BUTTON_SIZE, text=stgs.BUTTON_NAMES["highscores"][self.language], color="beige"),
            Button(pos=stgs.BUTTON_POSITIONS["quit"], size=stgs.BUTTON_SIZE, text=stgs.BUTTON_NAMES["quit"][self.language], color="red")
        ]

    def create_back_button(self) -> None:
        """ Creates the bak button for the options menu and the highscores screen. """
        self.back_button = Button(pos=stgs.BUTTON_POSITIONS["back"], size=stgs.BUTTON_SIZE, text=stgs.BUTTON_NAMES["back"][self.language], color="yellow")

    def create_language_buttons(self) -> None:
        """ Creates the language buttons for the options menu. """
        self.language_buttons: List[Button] = []
        for idx, button in enumerate(stgs.BUTTON_NAMES["language"].values()):
            self.language_buttons.append(Button(pos=(11 + idx * 130, 600), size=stgs.LANGUAGE_BUTTON_SIZE, text=str(button), color="beige"))

    def create_new_ripple(self) -> None:
        """ Creates a new ripple at a random y-position. """
        self.ripples.append(Ripple(self, pos=(-10, ri(25, 300))))

    def create_ripples(self) -> None:
        """ Creates a list of ripples. """
        self.ripples: List[Ripple] = [Ripple(self, pos=(-5 + i * ri(30, 60), ri(50, 300))) for i in range(100)]

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
    
    def create_time_bar(self) -> None:
        """ Creates a time bar at the bottom of the screen. """
        self.time_bar: TimeBar = TimeBar(self)
    
    def create_tree_fly(self, tree_speed: int, tree_rect: pg.Rect) -> None:
        """ Creates an TreeFly object. """
        if self.tree_fly_ready and self.tree_fly == None:
            self.tree_fly_ready = False
            self.tree_fly = TreeFly(self, tree_speed=tree_speed, tree_rect=tree_rect)
        
    def create_tree_snake(self, tree_speed: int, tree_rect: pg.Rect) -> None:
        """ Creates an TreeSnake object. """
        if self.tree_snake_ready and self.tree_snake == None:
            self.tree_snake_ready = False
            self.tree_snake = TreeSnake(self, tree_speed=tree_speed, tree_rect=tree_rect)

    def create_traffic(self) -> None:
        """ Creates traffic on the road. """
        self.traffic: List[List[Union[Truck, RacingCar, LargeCar, Bulldozer, SmallCar]]] = [
            [Truck(self, 700 - i * stgs.SPACING["lane 5"][self.level - 1], stgs.LANE_HEIGHTS["lane 5"]) for i in range(stgs.STREET[f"level {self.level}"][0])],
            [RacingCar(self, 400 - i * stgs.SPACING["lane 4"][self.level - 1], stgs.LANE_HEIGHTS["lane 4"], number=i) for i in range(stgs.STREET[f"level {self.level}"][1])],
            [LargeCar(self, 800 - i * stgs.SPACING["lane 3"][self.level - 1], stgs.LANE_HEIGHTS["lane 3"]) for i in range(stgs.STREET[f"level {self.level}"][2])],
            [Bulldozer(self, 400 - i * stgs.SPACING["lane 2"][self.level - 1], stgs.LANE_HEIGHTS["lane 2"]) for i in range(stgs.STREET[f"level {self.level}"][3])],
            [SmallCar(self, 600 - i * stgs.SPACING["lane 1"][self.level - 1], stgs.LANE_HEIGHTS["lane 1"]) for i in range(stgs.STREET[f"level {self.level}"][4])],]

    def create_water_traffic(self) -> None:
        """ Creates water traffic. """
        crocodile: int = 10  # choose a high number to never get a crocodile if in the level is no crocodile
        if stgs.CROCOS_SWIMMING[self.level - 1]:
            crocodile = ri(0, stgs.WATER[f"level {self.level}"][0] - 1)

        sinking_pair: int = ri(0, stgs.WATER[f"level {self.level}"][1] - 1)
        sinking_trio: int = ri(0, stgs.WATER[f"level {self.level}"][4] - 1)

        self.water_traffic: List[List[Union[LaneCrocodile, Tree, Turtle]]] = [
            [LaneCrocodile(self, 750 - i * stgs.SPACING["lane 10"][self.level - 1], stgs.LANE_HEIGHTS["lane 10"], 0) if i == crocodile else Tree(self, 750 - i * stgs.SPACING["lane 10"][self.level - 1], stgs.LANE_HEIGHTS["lane 10"], "medium", 0) for i in range(stgs.WATER[f"level {self.level}"][0])],
            [Turtle(self, 80 + i * stgs.SPACING["lane 9"][self.level - 1], stgs.LANE_HEIGHTS["lane 9"], 1, True if i == sinking_pair else False)  for i in range(stgs.WATER[f"level {self.level}"][1])],
            [Tree(self, 700 - i * stgs.SPACING["lane 8"][self.level - 1], stgs.LANE_HEIGHTS["lane 8"], "large", 2) for i in range(stgs.WATER[f"level {self.level}"][2])],
            [Tree(self, 800 - i * stgs.SPACING["lane 7"][self.level - 1], stgs.LANE_HEIGHTS["lane 7"], "small", 3) for i in range(stgs.WATER[f"level {self.level}"][3])],
            [Turtle(self, 50 + i * stgs.SPACING["lane 6"][self.level - 1], stgs.LANE_HEIGHTS["lane 6"], 4, True if i == sinking_trio else False) for i in range(stgs.WATER[f"level {self.level}"][4])],
        ]

    def clear_houses(self) -> None:
        """ Clears the houses list. """
        self.houses: List[int] = [False, False, False, False, False]

    def initialize_menu(self) -> None:
        """ Initialize the game menu. """
        self.music_start_stop()
        self.create_menu_buttons()

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
            self.get_middle_snake_time()
            self.get_tree_snake_time()
        self.get_house_fly_time()
        self.get_tree_fly_time()
        self.music_start_stop()

    def get_crocodile_time(self) -> None:
        """ Sets the time of the next appearance of a crocodile in a house. """
        self.crocodile_time: int | float = ri(10, 30)

    def get_house_fly_time(self) -> None:
        """ Sets the time of the next appearance of the house fly. """
        self.house_fly_time: int | float = ri(10, 30)

    def get_middle_snake_time(self) -> None:
        """ Sets the time of the next appearance of the snake. """
        self.middle_snake_time: int | float = ri(5, 10)

    def get_tree_fly_time(self) -> None:
        """ Sets the time of the next possible appearance of the tree fly. """
        self.tree_fly_time: int | float = stgs.TREE_FLY_TIME[self.level - 1]
    
    def get_tree_snake_time(self) -> None:
        """ Sets the time of the next possible appearance of the tree snake. """
        self.tree_snake_time: int | float = stgs.TREE_SNAKE_TIME[self.level - 1]

    def new_frog_or_game_over(self) -> None:
        """ Checks if a new frog can be created or if the game is over. """
        if self.frogs > 0:  
            self.handle_time_bar()
            self.create_frog()
            if self.tree_fly and self.tree_fly.state == "caught":
                self.tree_fly = None
                self.get_tree_fly_time()
        else:
            self.game_state = "game over"

    def handle_time_bar(self) -> None:
        """ Deletes the old time bar and creates a new one. """
        del self.time_bar
        self.create_time_bar()

    def handle_water_traffic_collision(self, collision_object: Union["Turtle", "Tree", "LaneCrocodile"], lane_index: int, element_index: int) -> bool:
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
                vehicle.rise_speed(amount=amount)
        for lane in self.water_traffic:
            for element in lane:
                element.rise_speed(amount=amount)
        if self.tree_fly:
            self.tree_fly.raise_x_speed(amount=amount)

    def time_up(self) -> None:
        """ Is called from the time bar object, if the time is up. """
        self.new_frog_or_game_over()

    def load_highscores(self) -> None:
        """ Loads the highscores from the highscores.list and puts them in a python list of lists. """
        with open("highscores.list", "r") as file:
            self.highscores: List[List[str]] = [line.strip().split() for line in file.readlines()]

    def sort_highscores(self) -> None:
        """ Sorts the highscores list with bubble sort. """
        while True:
            bubbled: bool = False
            for i in range(len(self.highscores) - 1):
                if int(self.highscores[i][0]) < int(self.highscores[i + 1][0]):
                    self.highscores[i + 1], self.highscores[i] = self.highscores[i], self.highscores[i + 1]
                    bubbled = True
            if not bubbled:
                del self.highscores[-1]
                break
    
    def write_highscores(self) -> None:
        """ Writes self.highscores to highscores.list. """
        with open("highscores.list", "w", encoding="utf-8") as highscores_file:
            for i in range(10):
                for j in range(2):
                    highscores_file.write(self.highscores[i][j])
                    if j == 1:
                        highscores_file.write("\n")
                    else:
                        highscores_file.write(" ")

    def load_info(self) -> None:
        """ Loads the info text in the selected language. """
        self.info_text: List[str] = []
        file_path: str = f"info/{self.language}.txt"
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                self.info_text = file.readlines()
                self.info_text = [line.strip() for line in self.info_text]
        except FileNotFoundError as e:
            print(f"Error: {e}")

    def music_start_stop(self) -> None:
        """ Starts or stops the music. """
        number: str = "1" if self.game_state == "menu" else "2"
        if self.music_enabled:
            pg.mixer.music.load(f"audio/Theme {number}.mp3")
            pg.mixer.music.set_volume(self.music_volume)
            pg.mixer.music.play(loops=-1)
        else:
            pg.mixer.music.stop()

    def event_handler(self) -> None:
        """ Handles events in the game. """
        # get events
        for event in pg.event.get():
            # handle quit event
            if event.type == pg.QUIT:
                self.running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_m:
                    self.music_key_pressed = True
                if event.key == pg.K_s:
                    self.sound_key_pressed = True
            if event.type == pg.KEYUP:
                if event.key == pg.K_m and self.music_key_pressed:
                    self.music_enabled = False if self.music_enabled == True else True
                    self.music_key_pressed = False
                    self.music_start_stop()
                if event.key == pg.K_s and self.sound_key_pressed:
                    self.sound_enabled = False if self.sound_enabled == True else True
                    self.sound_key_pressed = False
            
            # check key events while playing the game
            if self.game_state == "play" or self.game_state == "pause":
                if event.type == pg.KEYDOWN:
                    
                    if (event.key == pg.K_UP or event.key == pg.K_w) and self.game_state != "pause":
                        self.direction_pressed = True
                    if (event.key == pg.K_DOWN or event.key == pg.K_s) and self.game_state != "pause":
                        self.direction_pressed = True
                    if (event.key == pg.K_LEFT or event.key == pg.K_a) and self.game_state != "pause":
                        self.direction_pressed = True
                    if (event.key == pg.K_RIGHT or event.key == pg.K_d) and self.game_state != "pause":
                        self.direction_pressed = True
                    if event.key == pg.K_p and not self.pause_key_pressed:
                        self.pause_key_pressed = True                    

                if event.type == pg.KEYUP:
                    if (event.key == pg.K_UP or event.key == pg.K_w) and self.direction_pressed and not self.frog.jumping:
                        self.frog.jump("north")
                        self.direction_pressed = False
                        if self.tree_fly and self.tree_fly.state == "caught":
                            self.tree_fly.set_angle(angle = 0)
                    if (event.key == pg.K_DOWN or event.key == pg.K_s) and self.direction_pressed and not self.frog.jumping:
                        self.frog.jump("south")
                        self.direction_pressed = False
                        if self.tree_fly and self.tree_fly.state == "caught":
                            self.tree_fly.set_angle(angle = 180)
                    if (event.key == pg.K_LEFT or event.key == pg.K_a) and self.direction_pressed and not self.frog.jumping:
                        self.frog.jump("west")
                        self.direction_pressed = False
                        if self.tree_fly and self.tree_fly.state == "caught":
                            self.tree_fly.set_angle(angle = 90)
                    if (event.key == pg.K_RIGHT or event.key == pg.K_d) and self.direction_pressed and not self.frog.jumping:
                        self.frog.jump("east")
                        self.direction_pressed = False
                        if self.tree_fly and self.tree_fly.state == "caught":
                            self.tree_fly.set_angle(angle = 270)
                    if event.key == pg.K_p and self.pause_key_pressed:
                        self.game_state = "pause" if self.game_state == "play" else "play"
                        self.pause_key_pressed = False
            
            elif self.game_state == "game over":
                lowest_highscore: int = int(self.highscores[-1][0])
                if self.score > lowest_highscore:
                    if event.type == pg.KEYDOWN:
                        if event.key == pg.K_BACKSPACE and len(self.player_name) > 0:
                            self.player_name = self.player_name[0:-1]
                        elif event.key == pg.K_RETURN and len(self.player_name) > 0:
                            self.highscores.append([str(self.score), self.player_name])
                            self.sort_highscores()
                            self.write_highscores()
                            self.create_back_button()
                            self.player_name = ""
                            self.game_state = "highscores"
                        else:
                            if len(self.player_name) < 8:
                                self.player_name += event.unicode

                
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

        # update tree fly
        if self.tree_fly:
            self.tree_fly.update(dt)

        # update house crocodile
        if self.house_crocodile:
            self.house_crocodile.update(dt)

        # update middle snake
        if self.middle_snake:
            self.middle_snake.update(dt)

        # update tree snake
        if self.tree_snake:
            self.tree_snake.update(dt)

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
        # update crocodile time if there is a crocodile in the level
        if stgs.CROCOS_IN_HOUSES[self.level - 1] and self.house_crocodile == None:
            self.crocodile_time -= dt
            if self.crocodile_time <= 0:
                self.create_house_crocodile()

        # update frog time
        if self.show_frog_time:
            self.show_time -= dt
            if self.show_time <= 0:
                self.show_frog_time = False
                self.show_time = stgs.SHOW_FROG_TIME

        # update house fly time
        self.house_fly_time -= dt
        if self.house_fly_time <= 0 and self.house_fly == None:
            self.create_house_fly()

        # update snake times
        if stgs.SNAKES[self.level - 1] and self.middle_snake == None:
            self.middle_snake_time -= dt
            if self.middle_snake_time <= 0:
                self.create_middle_snake()
        if stgs.SNAKES[self.level - 1] and self.tree_snake == None:
            self.tree_snake_time -= dt
            if self.tree_snake_time <= 0:
                if ri(1, 10) > stgs.TREE_SNAKE_CHANCE[self.level - 1]:
                    self.tree_snake_ready = True

        # update tree fly time
        self.tree_fly_time -= dt
        if self.tree_fly_time <= 0 and self.tree_fly == None:
            if ri(1, 10) > stgs.TREE_FLY_CHANCE[self.level - 1]:
                self.tree_fly_ready = True
      
    def render_game(self) -> None:
        """ Renders the game while playing. """
        # draw houses to have a background behind the background
        self.screen.blit(self.image["houses"], (0, 0))
        # draw background
        self.screen.blit(self.image["game background"], (0, 26))
        # draw ripples
        for ripple in self.ripples:
            ripple.render(self.screen)
        # draw stripes
        for i in range(4):
            for j in range(55):
                pos: tuple[int, int] = (stgs.STRIPES["x start"] + j * stgs.STRIPES["x spacing"], 
                                        stgs.STRIPES["y start"] + i * stgs.STRIPES["y spacing"])
                self.screen.blit(self.image["stripe"], pos)
        # draw water traffic
        for lane in self.water_traffic:
            for element in lane:
                element.render(self.screen)
        # draw frog time
        if self.show_frog_time:
            time_to_blit: pg.Surface = self.score_font.render(f"{int(self.frog_time)} Seconds", True, "white", "black")
            pos: tuple[int, int] = (int(stgs.WINDOW_SIZE[0] // 2 - time_to_blit.get_width() // 2), 
                                    int(stgs.WINDOW_SIZE[1] // 2 - time_to_blit.get_height() // 2))
            self.screen.blit(time_to_blit, pos)
        
        # draw frog
        self.frog.render(self.screen)
        # draw house crocodile
        if self.house_crocodile:
            self.house_crocodile.render(self.screen)
        # draw house fly
        if self.house_fly:
            self.house_fly.render(self.screen)
        # draw tree fly
        if self.tree_fly:
            self.tree_fly.render(self.screen)
        
        # draw traffic
        for lane in self.traffic:
            for vehicle in lane:
                vehicle.render(self.screen)
        # draw middle snake
        if self.middle_snake:
            self.middle_snake.render(self.screen)
        # draw tree snake
        if self.tree_snake:
            self.tree_snake.render(self.screen)
        # draw houses
        self.screen.blit(self.image["houses"], (0, 26))
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
                self.screen.blit(self.image["frog/house"], (35 + i * multiplicand, 52))
        # draw the remaining frogs
        for i in range(self.frogs):
            self.screen.blit(self.image["frog/life"], (10 + i * 32, stgs.FROG_DRAW_HEIGHT))

        # showing gras rects for testing
        for gras_rect in self.gras_rects:
            pg.draw.rect(self.screen, "darkorange", gras_rect, width=1)
            
        # draw time bar
        self.time_bar.render(self.screen)

        if self.game_state == "pause":
            surf: pg.Surface = pg.Surface(stgs.WINDOW_SIZE, pg.SRCALPHA)
            surf.fill((200, 200, 200, 50))
            self.screen.blit(surf, (0, 0))
            shadow: pg.Surface = self.pause_font.render(stgs.PAUSE["pause"][self.language], True, "black")
            text: pg.Surface = self.pause_font.render(stgs.PAUSE["pause"][self.language], True, "white")
            x_pos: int = int(stgs.WINDOW_SIZE[0] / 2 - text.get_width() / 2)
            y_pos: int = int(stgs.WINDOW_SIZE[1] / 2 - text.get_height() / 2)
            self.screen.blit(shadow, (x_pos - 3, y_pos + 3))
            self.screen.blit(text, (x_pos, y_pos))
            if self.show_pause_text:
                shadow: pg.Surface = self.pause_text_font.render(stgs.PAUSE["text"][self.language], True, "black")
                text: pg.Surface = self.pause_text_font.render(stgs.PAUSE["text"][self.language], True, "white")
                x_pos: int = int(stgs.WINDOW_SIZE[0] / 2 - text.get_width() / 2)
                y_pos: int = int(stgs.WINDOW_SIZE[1] / 3 * 2 - text.get_height() / 2)
                self.screen.blit(shadow, (x_pos - 2, y_pos + 2))
                self.screen.blit(text, (x_pos, y_pos))
        elif self.game_state == "game over":
            surf: pg.Surface = pg.Surface(stgs.WINDOW_SIZE, pg.SRCALPHA)
            surf.fill((200, 200, 200, 50))
            self.screen.blit(surf, (0, 0))
            shadow: pg.Surface = self.pause_font.render(stgs.GAME_OVER["game over"][self.language], True, "black")
            text: pg.Surface = self.pause_font.render(stgs.GAME_OVER["game over"][self.language], True, "white")
            x_pos: int = int(stgs.WINDOW_SIZE[0] / 2 - text.get_width() / 2)
            y_pos: int = int(stgs.WINDOW_SIZE[1] / 2 - text.get_height() / 2)
            self.screen.blit(shadow, (x_pos - 3, y_pos + 3))
            self.screen.blit(text, (x_pos, y_pos))

    def render_menu(self) -> None:
        """ Renders the main menu. """
        self.screen.blit(self.image["menu background"], (0, 0))
        for button in self.menu_buttons:
            button.render(self.screen)

    def render_options(self) -> None:
        """ Renders the options menu. """
        self.screen.blit(self.image["options background"], (0, 0))
        for idx, line in enumerate(self.info_text):
            shadow: pg.Surface = self.info_font.render(str(line), True, "black")
            text: pg.Surface = self.info_font.render(str(line), True, "white")
            self.screen.blit(shadow, (52, 52 + idx * 30))
            self.screen.blit(text, (50, 50 + idx * 30))
        if self.back_button:
            self.back_button.render(self.screen)
        for button in self.language_buttons:
            button.render(self.screen)

    def render_highscores(self) -> None:
        """ Render the high scores screen. """
        self.screen.blit(self.image["highscores background"], (0, 0))
        # Render high score entries
        for index, (score, name) in enumerate(self.highscores):
            score = score if score != "0" else "00000"
            # calculating the real rank
            int_number: int = index + 1
            # making a string out of the number with a '0' in front of numbers under 10
            str_number: str = f"{int_number}" if int_number > 9 else f"0{int_number}"
            # render the strings as shadow and text
            number_shadow: pg.Surface = self.score_font.render(f"{str_number}.", True, "black")
            number_text: pg.Surface = self.score_font.render(f"{str_number}.", True, "white")
            score_shadow: pg.Surface = self.score_font.render(score, True, "black")
            score_text: pg.Surface = self.score_font.render(score, True, "white")
            name_shadow: pg.Surface = self.score_font.render(name, True, "black")
            name_text: pg.Surface = self.score_font.render(name, True, "white")
            # blit shadow and text
            self.screen.blit(number_shadow, (102, 22 + index * 35))
            self.screen.blit(number_text, (100, 20 + index * 35))
            self.screen.blit(score_shadow, (202, 22 + index * 35))
            self.screen.blit(score_text, (200, 20 + index * 35))
            self.screen.blit(name_shadow, (352, 22 + index * 35))
            self.screen.blit(name_text, (350, 20 + index * 35))
        if self.game_state == "game over":
            name_to_blit: pg.Surface = self.score_font.render(self.player_name, True, "white")
            self.screen.blit(name_to_blit, (int(stgs.WINDOW_SIZE[0] / 2 - 200), stgs.WINDOW_SIZE[0] - 150))
        if self.back_button and self.game_state != "game over":
            self.back_button.render(self.screen)

    def draw_screen(self) -> None:
        """ Draws the game screen. """
        pg.display.set_caption(f"     F R O G G E R - C L O N E          FPS:{self.fps}")
        # clear the screen
        self.screen.fill((0, 0, 0))
        if self.game_state == "menu":
            self.render_menu()
        elif self.game_state == "play" or self.game_state == "pause":
            self.render_game()
        # showing the highscores
        elif self.game_state == "highscores" or self.game_state == "game over":
            self.render_highscores()
        # showing the options menu
        elif self.game_state == "options":
            self.render_options()
                
        pg.display.update()

    def main(self) -> None:
        """ Runs the main game loop. """
        # self.calculate_distances()
        old_time: float = pc()
        fps_timer: float = 0.0
        fps_counter: int = 0
        self.load_highscores()

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
            if self.game_state != "play" and self.game_state != "pause":
                self.check_buttons()

            # playing the game
            elif self.game_state == "play":
                self.update_variables(dt)
                self.update_objects(dt)
                self.check_collisions()
                if self.frog.pos.y <= 353:
                    self.calculate_distances()

            # let the pause text blink
            elif self.game_state == "pause":
                self.blink_timer -= dt
                if self.blink_timer <= 0:
                    self.show_pause_text = False if self.show_pause_text == True else True
                    self.blink_timer = stgs.BLINK_TIME

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