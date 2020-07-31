from abc import ABC, abstractmethod
import discord
import random
random.seed()
from redbot.core import commands
from redbot.core.bot import Red

from .util import Option, OptionType


class NoSuchOption(Exception):
    def __init__(self, option_name:str):
        """Init for NoSuchOption exception
        This will be thrown when a user requests an option that doesn't exist
        """
        self.option_name = option_name

    def __str__(self):
        return f"No such option: {self.option_name}"



class Joke(ABC): 
    def __init__(self, name:str, default_chance:float):
        """Init for the abstract Joke object.
        The purpose of this object is to generalize the flow of the typical 
        joke. These jokes are structured in that they will:
            1: Attempt to make the joke with some specified percent chance.
            2: If randomness allows they will then scan the message to see if 
               the joke applies.
            3: If it applies it will respond with the joke, and return True.
               If it does not, or if randomness did not allow an attempt it
               will return False.
        The idea is that Dad will attempt all possible jokes in a random order
        upon receiving a message until either a joke succeeds or he runs out of
        jokes. Since each joke is only supposed to happen a specified amount of
        time this class also uses the Option class to generalize creating that 
        setting for each guild. It has been setup so that Jokes can create 
        other options if needed.
        Parameters
        ----------
        name: str
            The name of the joke
        default_chance: float
            The default chance [0.0,100.0] of the joke occuring
        Raises
        ------
        ValueError
            Occurs if default_chance is not within the range [0.0,100.0]
        """
        # Set up saved values
        self.name = name
        # Set up options
        self.guild_options = [
                Option(f"{self.name}_chance", default_chance, 
                    OptionType.PERCENTAGE)
                ]


    async def make_joke(self, bot: Red, msg: discord.Message) -> bool:
        """Make the joke.
        Parameters
        ----------
        bot: Red
            The RedBot executing this function.
        msg: discord.Message
            The context in which the joke is being made.
        Returns
        -------
        bool
            Rather the joke was made or not.
        Raises
        ------
        AttributeError
            If this is raised then something is horribly wrong with the class. 
            It means that the response chance was never made a part of the 
            default values for guilds.
        """
        chance = await self.get_guild_option(bot, msg.channel, 
                f"{self.name}_chance")
        if  random.uniform(0.0, 100.0) <= chance:
            return await self._make_joke(bot, msg)
        else:
            return False


    @abstractmethod    
    async def _make_joke(self, bot: Red, msg: discord.Message) -> bool:
        """The method to be overridden to actually make the joke.
        Parameters
        ----------
        bot: Red
            The RedBot executing this function.
        msg: discord.Message
            The context in which the joke is being made.
        Returns
        -------
        bool
            Rather the joke was made or not.
        """
        return NotImplemented


    def register_guild_settings(self, default_guild_settings: dict, 
            guild_options_information: dict):
        """Modifies the given dictionaries of guild settings to include our own.
        Parameters
        ----------
        default_guild_settings: dict
            The dictionary to modify via inserting default values.
        guild_options_information: dict
            The dictionary to modify via inserting the Option objects.
        """
        for opt in self.guild_options:
            default_guild_settings[opt.name] = opt.default_value
            guild_options_information[opt.name] = opt


    @staticmethod
    async def get_guild_option(bot: Red, ctx: commands.Context, 
            option_name: str) -> any:
        """
        Parameters
        ----------
        bot: Red
            The RedBot executing this function.
        ctx: commands.Context
            The context in which the joke is being made.
        option_name: str
            The option to get.
        Returns
        -------
        any
            The requested value.
        Raises
        ------
        NoSuchOption
            Raised if the given option_name does not exist
        """
        try:
            return await getattr(bot._conf.guild(ctx.guild), option_name)()
        except AttributeError:
            raise NoSuchOption(option_name)


    @staticmethod
    async def set_guild_option_value(bot: Red, ctx: commands.Context, 
            option_name: str, new_value: any):
        """
        Parameters
        ----------
        bot: Red
            The RedBot executing this function.
        ctx: commands.Context
            The context in which the joke is being made.
        option_name: str
            The option to set the value of.
        new_value: any
            The new value for the option.
        Raises
        ------
        NoSuchOption
            Raised if the given option_name does not exist
        """
        try:
            # Get the type converter
            converter = bot.guild_options_information[option_name]
            # Convert the new value
            new_value = converter.type_convertor(new_value)
            # Set the value
            await getattr(bot._conf.guild(ctx.guild), option_name)\
                .set(new_value)
        except (AttributeError, KeyError):
            raise NoSuchOption(option_name)


