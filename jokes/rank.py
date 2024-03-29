from abc import ABC, abstractmethod
import discord
import logging
import re
from redbot.core import checks, commands, Config
from redbot.core.bot import Red

from .joke import Joke
from ..images import random_image_url_in_category


class RankJoke(Joke):
    def __init__(self):
        """Init for the Rank joke.

        The Rank joke is where a person says "X Y" where X is a rank in the
        armed forces, and Y is any word. Example: "Major Explanation".
        The joke is to send a gif of a person saluting with the title 
        "Major Explanation" or whatever was actually said. This stems from a
        bit in "How I Met Your Mother".
        """
        # Set up super class
        super().__init__("rank", 100.0)
        # Set up this class
        ranks = [
            "admiral",
            "brigadier",
            "cadet", 
            "captain",
            "colonel",
            "commander",
            "general",
            "marshal",
            "major",
            "officer",
            "lieutenant",
            "private",
            "sergeant"
        ]
        ranks_re = "|".join(ranks)
        self.rank_re = re.compile(
                r".*(?P<rank>\b(" + ranks_re + r"\b))(ly)?" +\
                        r"\s+(?P<title>\b\w+\b)", 
                re.IGNORECASE)


    async def _make_verbal_joke(self, bot: Red, msg: discord.Message) -> bool:
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
            # Log joke
            self.log_info(msg.guild, msg.author, match)
            # Construct our response
            response = {"title": f"{match.group('rank').capitalize()} "\
                                 f"{match.group('title').capitalize()}"}
            # Construct embed
            embed = discord.Embed.from_dict(response)
            embed.set_image(url=random_image_url_in_category("salute"))
            # Send embed
            await msg.channel.send(embed=embed)
            # Return success
            return True

