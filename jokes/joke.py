from abc import ABC, abstractmethod
import discord
import random
random.seed()
from redbot.core import checks, commands, Config
from redbot.core.bot import Red

from .util import Option, OptionType

class NoSuchOption(Exception):
    def __init__(self, option_name):
        self.option_name = option_name

    def __str__(self):
        return f"No such option: {self.option_name}"



class Joke(ABC): 
    def __init__(self, name:str, default_chance:float):
        """
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


