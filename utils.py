import os
import pygame as pg
from typing import Final

BASE_PATH: Final[str] = "images/"
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
    img_path = BASE_PATH + img_name
    try:
        img: pg.Surface = pg.image.load(img_path).convert_alpha()
        if scale_factor == 1:
            return img
        else:
            return scale_image(image = img, scale_factor = scale_factor)
    except FileNotFoundError as e:
        print(f"File not found: {e}")

def load_images(image_path: str, scale_factor: int|float = 1) -> list[pg.Surface]:
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
        for img_name in os.listdir(BASE_PATH + image_path):
            img: pg.Surface = load_image(image_path + img_name, scale_factor)
            images.append(img)
        return images
    except NotADirectoryError as e:
        print(f"Path is not a directory: {e}")

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

    def copy(self) -> object:
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
    
    def get_current_image(self) -> pg.Surface | None:
        """
        Returns the current image in the animation.
        Returns:
        pg.Surface: the current image in the animation
        """
        if not self.done:
            return self.images[self.image_index]
        else:
            return None