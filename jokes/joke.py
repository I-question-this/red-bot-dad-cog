from abc import ABC, abstractmethod
import discord
import random
from redbot.core import checks, commands, Config
from redbot.core.bot import Red


class Joke(ABC): 
    JOKES = dict()

    def __init__(self, name:str, default_chance:float):
        """
        Parameters
        ----------
        name: str
            The name of the joke
        default_chance: float
            The default chance [0.0-1.0] of the joke occuring
        Raises
        ------
        ValueError
            Occurs if default_chance is not within the range [0.0,100.0]
        """
        # Set up saved values
        self.name = name
        if 0.0 <= default_chance <= 100.0:
            self.default_chance = default_chance
        else:
            raise ValueError(f"default_chance must be in the range [0.0,100.0]")
        self.JOKES[self.name] = self


    async def get_response_chance(self, bot: Red, ctx: commands.Context):
        """
        Parameters
        ----------
        bot: Red
            The RedBot executing this function.
        ctx: commands.Context
            The context in which the joke is being made.
        Raises
        ------
        AttributeError
            Occurs if this Joke was never properly saved into the default
            values for the RedBot config file.
        """
        return await getattr(bot._conf.guild(ctx.guild), self.name)()


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
        chance = await self.get_response_chance(bot, msg)
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


    def register_guild_settings(self, guild_settings: dict):
        """Modifies the given dictionary of guild settings to include our own.
        Parameters
        ----------
        guild_settings: dict
            The dictionary to modify.
        """
        guild_settings[self.name] = self.default_chance


    async def set_response_chance(self, bot: Red, ctx: commands.Context, 
            new_chance: float):
        """
        Parameters
        ----------
        bot: Red
            The RedBot executing this function.
        ctx: commands.Context
            The context in which the joke is being made.
        new_chance: float
            The default chance [0.0,100.0] of the joke occuring
        Raises
        ------
        ValueError
            Occurs if default_chance is not within the range [0.0,100.0]
        """
        if not (0.0 <= new_chance <= 100.0):
            raise ValueError(f"new_chance must be in the range [0.0,100.0]")

        await getattr(bot._conf.guild(ctx.guild), self.name)\
            .set(new_chance)

