from enum import Enum
import discord
import os
import random
random.seed()


def convert_to_boolean(boolean: str) -> bool:
    """Input is converted to boolean
    Parameters
    ----------
    boolean: str
        The input to be converted and verified.
    
    Returns
    -------
    bool
        The converted and verified input.  Raises ------
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


def convert_to_non_zero_positive_int(nz_p_int: int) -> float:
    """Input is converted to a non-zero positive integer.

    Parameters
    ----------
    nz_p_int: int
        The input to be converted and verified.
    
    Returns
    -------
    int
        The converted and verified input.

    Raises
    ------
    ValueError
        Describes problem in conversion and/or verification.
    """
    try:
        nz_p_int = int(nz_p_int)
    except TypeError:
        raise ValueError(f"{nz_p_int} is not a valid integer")
    if nz_p_int > 0:
        return nz_p_int
    else:
        raise ValueError(f"Must be an integer above 0")


class OptionType(Enum):
    """The recognized types to convert strings into types
    Note that the value of the enums is a method that turns
    a string into the specified type, even doing sanity
    checks on the converted value.
    """
    BOOLEAN = convert_to_boolean
    HIDDEN = "HIDDEN" # Don't expose this to the users
    NONZERO_POSITIVE_INTEGER = convert_to_non_zero_positive_int
    PERCENTAGE = convert_to_percentage


class Option:
    def __init__(self, name:str, default_value, 
            option_type:OptionType):
        """The init for the Option object.
        The use of this object is to define an option denoted by the name
        with a default value and a method to convert user input 
        (strings) into the proper type for saving.

        Parameters
        ----------
        name: str
            The name of the option.
        default_value: any
            The default value for this option.
        option_type: OptionType
            The Enum containing the method to convert
            strings into the required type.
        """
        self.name = name
        self.default_value = default_value
        # I don't know why this object becomes a function,
        # its value, instead of staying an Enum.
        self.type_convertor = option_type

