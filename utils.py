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
            img: pg.Surface = load_image(img_name, scale_factor)
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