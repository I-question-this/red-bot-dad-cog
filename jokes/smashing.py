from abc import ABC, abstractmethod
import discord
import re
from redbot.core import checks, commands, Config
from redbot.core.bot import Red

from .joke import Joke
from .util import random_image, SMASHING_DIR


class SmashingJoke(Joke):
    def __init__(self):
        # Set up super class
        super().__init__("smashing", 100.0)
        # Set up this class
        self.smashing_re = re.compile(r"smash", re.IGNORECASE)


    async def _make_joke(self, bot: Red, msg: discord.Message) -> bool:
        """Make a rank joke, returning bool as to success.

        Parameters
        ----------
        bot: Red
            The RedBot executing this function.
        msg: discord.Message
            Message to attempt a joke upon

        Returns
        -------
        bool
            Success of joke.
        """
        match = self.smashing_re.search(msg.content)
        if match is None:
            # No joke was possible, stop
            return False
        else:
            # Construct our response
            response = {}
            # Pick random gif
            smashing_gif = random_image(SMASHING_DIR)
            # Construct embed
            embed = discord.Embed.from_dict(response)
            embed.set_image(url=f"attachment://{smashing_gif.filename}")
            # Send embed and smashing gif
            await message.channel.send(embed=embed, file=smashing_gif)
            # Return success
            return True


