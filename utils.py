from __future__ import annotations

import settings as stgs

import os
import pygame as pg

from typing import Final, List, Iterator, Optional

IMAGE_BASE_PATH: Final[str] = "images/"
SOUND_BASE_PATH: Final[str] = "audio/"
def load_image(img_name: str, scale_factor: int|float = 1) -> pg.Surface:
    """ 
    Loads an image from the given path and let it scale by the given factor.
    e.g. example_folder/example_image.png
    Args:
    img_name (str): name of the image to load
    scale_factor (float): factor to scale the image by
    Returns:
    pg.Surface: the loaded and scaled image
    """
    img_path = IMAGE_BASE_PATH + img_name
    try:
        img: pg.Surface = pg.image.load(img_path).convert_alpha()
        if scale_factor == 1:
            return img
        else:
            return scale_image(image = img, scale_factor = scale_factor)
    except FileNotFoundError as e:
        print(f"File not found: {e}")
        return pg.Surface((32, 32), pg.SRCALPHA)  # in case of failure return an transparent surface

def load_images(image_path: str, scale_factor: int|float = 1) -> List[pg.Surface]:
    """ 
    Loads a list of images from the given path and let them scale by the given factor.
    e.g. example_folder/example_image.png
    Args:
    image_path (str): path to the images to load
    scale_factor (float): factor to scale the image by
    Returns:
    list[pg.Surface]: the loaded and scaled images
    """
    images: list[pg.Surface] = []
    try:
        for img_name in os.listdir(IMAGE_BASE_PATH + image_path):
            img: pg.Surface = load_image(image_path + img_name, scale_factor)
            images.append(img)
        return images
    except NotADirectoryError as e:
        print(f"Path is not a directory: {e}")
        return [pg.Surface((32, 32), pg.SRCALPHA)]  # in case of failure return a list with an transparent surface in it

def scale_image(image: pg.Surface, scale_factor: float) -> pg.Surface:
    """
    Scales an image by the given factor.
    Args:
    image (pg.Surface): the image to scale
    scale_factor (float): factor to scale the image by
    Returns:
    pg.Surface: the scaled image
    """
    return pg.transform.scale(image, (int(image.get_width() * scale_factor), int(image.get_height() * scale_factor)))

def load_sound(sound_name: str) -> pg.mixer.Sound:
    """
    Loads a sound and returns it as a pg.mixer.Sound object.
    Args:
        sound_name (str): The name of the sound to load.
    Returns:
        pg.mixer.Sound: The loaded sound object or an empty sound if loading fails.
    """
    try:
        sound = pg.mixer.Sound(SOUND_BASE_PATH + sound_name + ".mp3")
        return sound
    except FileNotFoundError as e:
        print(f"Error: {e}")
        return pg.mixer.Sound(buffer=bytearray()) 

    
class Animation:
    def __init__(self, images: list[pg.Surface], animation_duration: float, loop: bool = True) -> None:
        """
        Creates an animation from a list of images.
        Args:
        images (list[pg.Surface]): the images to use for the animation
        animation_duration (float): the duration of the animation in seconds
        loop (bool): whether the animation should loop or not
        """
        self.images: list[pg.Surface] = images
        self.animation_duration: float = animation_duration
        self.image_duration: float = animation_duration / len(self.images)
        self.loop: bool = loop
        self.image_index: int = 0
        self.image_timer: float = 0.0
        self.done: bool = False

    def __iter__(self) -> Iterator["Animation"]:
        yield self

    def copy(self) -> Animation:
        """ Returns a copy of the animation object. """
        return Animation(images = self.images, animation_duration = self.animation_duration, loop = self.loop)
    
    def update(self, dt: float) -> None | bool:
        """
        Updates the animation by one frame.
        Args:
        dt (float): the time since the last update in seconds
        Returns:
        bool: whether the animation has finished or not
        """
        if not self.done:
            self.image_timer += dt
            if self.image_timer >= self.image_duration:
                self.image_timer = 0.0
                self.image_index += 1
                if self.image_index >= len(self.images):
                    if self.loop:
                        self.image_index = 0
                    else:
                        self.done = True
                        return self.done
    
    def get_current_image(self) -> pg.Surface | bool:
        """
        Returns the current image in the animation.
        Returns:
        pg.Surface: the current image in the animation
        """
        if not self.done:
            return self.images[self.image_index]
        else:
            self.done = True
            return self.done
        

class Button:
    """ A button class that can be used to create buttons in the game. """
    def __init__(self, pos: tuple[int, int], size: tuple[int, int], text: str, color: str) -> None:
        """ Initializes a button object.
        Args:
        pos (tuple(int)): The topleft position of the button
        text (str): The text to be displayed on the button
        color (str): The color of the button (green, yellow, red, white)
        """
        self.pos: pg.Vector2 = pg.Vector2(pos)
        self.size: tuple[int, int] = size
        
        self.shadow_color: tuple[int, int, int] = stgs.BUTTON_COLORS[color]["shadow_color"]
        self.main_color: tuple[int, int, int] = stgs.BUTTON_COLORS[color]["main_color"]
        self.frame_color: tuple[int, int, int] = stgs.BUTTON_COLORS[color]["frame_color"]
        self.hover_color: tuple[int, int, int] = stgs.BUTTON_COLORS[color]["hover_color"]
        self.color: tuple[int, int, int] = self.main_color
        font: pg.font.Font = pg.font.SysFont("comicsans", stgs.BUTTON_FONT_SIZE)
        self.text: pg.Surface = font.render(text, True, "white")
        self.text_shadow: pg.Surface = font.render(text, True, "black")
        self.text_pos: tuple[int, int] = (int(self.pos.x + self.size[0] // 2 - self.text.get_width() // 2),
                                     int(self.pos.y + self.size[1] // 2 - self.text.get_height() // 2))
        self.clicked: bool = False
        self.offset: int = stgs.BUTTON_OFFSET
        self.rect: pg.Rect = self.create_rect()

    def check_clicked(self) -> None | bool:
        """ Checks if the button is clicked. Returns True if the button is clicked else None. """
        if self.rect.collidepoint(pg.mouse.get_pos()):
            self.color = self.hover_color
            if pg.mouse.get_pressed()[0]:
                self.clicked = True
                self.offset = 0
            if not pg.mouse.get_pressed()[0] and self.clicked:
                self.clicked = False
                self.offset = stgs.BUTTON_OFFSET

                return True
        else:
            self.color = self.main_color
            self.clicked = False

    def create_rect(self) -> pg.Rect:
        """ Creates a rectangle for the button. """
        return pg.Rect(self.pos.x, self.pos.y - self.offset, self.size[0], self.size[1])

    def render(self, surf: pg.Surface) -> None:
        """ Renders the button on the given surface.
        Args:
        surf (pg.Surface): the surface to render the button on
        """
        self.rect = self.create_rect()
        pg.draw.rect(surf, self.shadow_color, (self.pos.x, self.pos.y, self.size[0], self.size[1]), border_radius=5)
        pg.draw.rect(surf, self.color, self.rect, border_radius=5)
        pg.draw.rect(surf, self.frame_color, self.rect, width=3, border_radius=5)
        surf.blit(self.text_shadow, (self.text_pos[0], self.text_pos[1] - self.offset))
        surf.blit(self.text, (self.text_pos[0] - 2, self.text_pos[1] - self.offset - 2))

