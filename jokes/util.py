from enum import Enum
import discord
import os
import random
random.seed()


# Determine image folder locations
FILE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGES_DIR = os.path.join(os.path.dirname(FILE_DIR), "images")
SALUTES_DIR = os.path.join(IMAGES_DIR, "salutes")
SMASHING_DIR = os.path.join(IMAGES_DIR, "smashing")


def convert_to_boolean(boolean: str) -> bool:
    """Input is converted to boolean
    Parameters
    ----------
    boolean: str
        The input to be converted and verified.
    
    Returns
    -------
    bool
        The converted and verified input.

    Raises
    ------
    ValueError
        Describes problem in conversion and/or verification.
    """
    boolean = boolean.lower()
    if boolean == "true" or boolean == "t" or boolean == "1":
        return True
    elif boolean == "false" or boolean == "f" or boolean == "0":
        return False
    else:
        raise ValueError(f"boolean has to be true/false, t/f, or 1/0")


def convert_to_percentage(percentage: float) -> float:
    """Input is converted to float with typecasting and range is verified.

    Parameters
    ----------
    percentage: float
        The input to be converted and verified.
    
    Returns
    -------
    float
        The converted and verified input.

    Raises
    ------
    ValueError
        Describes problem in conversion and/or verification.
    """
    try:
        percentage = float(percentage)
    except TypeError:
        raise ValueError(f"{percentage} is not a valid float")
    if 0.0 <= percentage <= 100.0:
        return percentage
    else:
        raise ValueError(f"percentage must be in the range [0.0,100.0]")


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


class OptionType(Enum):
    PERCENTAGE = convert_to_percentage
    BOOLEAN = convert_to_boolean


class Option:
    def __init__(self, name:str, default_value:any, 
            option_type:OptionType):
        self.name = name
        self.default_value = default_value
        # I don't know why this object becomes a function,
        # its value, instead of staying an Enum.
        self.type_convertor = option_type

