from abc import ABC, abstractmethod
import discord
import re
from redbot.core import checks, commands, Config
from redbot.core.bot import Red

from .joke import Joke
from .util import random_image, SALUTES_DIR


class RankJoke(Joke):
    def __init__(self):
        # Set up super class
        super().__init__("rank", 25.0)
        # Set up this class
        ranks = ["general", "captain", "major", "colonel", "officer", "lieutenant", "admiral", "commander", 
                "officer", "marshal", "cadet", "brigadier", "cadet", "sergeant", "private"]
        self.rank_re = re.compile(r".*(?P<rank>\b(" + "|".join(ranks) + r"\b))\s+(?P<title>\b\w+\b)", re.IGNORECASE)

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
        match = self.rank_re.search(msg.content)
        if match is None:
            # No joke was possible, stop
            return False
        else:
            # Construct our response
            response = {}
            response["title"] = f"{match.group('rank').capitalize()} {match.group('title').capitalize()}"
            # Pick random salute gif
            salute_gif = random_image(SALUTES_DIR)
            salute_gif = discord.File(gif_path, filename="salute.gif")
            # Construct embed
            embed = discord.Embed.from_dict(response)
            embed.set_image(url=f"attachment://{salute_gif.filename}")
            # Send embed and salute gif
            await msg.channel.send(embed=embed, file=salute_gif)
            # Return success
            return True
