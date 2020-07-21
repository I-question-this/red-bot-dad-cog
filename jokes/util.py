import discord
import os
import random
random.seed()


# Determine image folder locations
FILE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGES_DIR = os.path.join(os.path.dirname(FILE_DIR), "images")
SALUTES_DIR = os.path.join(IMAGES_DIR, "salutes")
SMASHING_DIR = os.path.join(IMAGES_DIR, "smashing")


def random_image(directory: str) -> discord.File:
    """Returns a random image from given directory in the form of a discord.File

    Parameters
    ----------
    directory: str
        Directory to get a random image from

    Returns
    -------
    discord.File
        The path to the randomly selected image.
    """
    gif_path = os.path.join(directory,
            random.choice(os.listdir(directory)))
    return discord.File(gif_path, filename="joke.gif")
