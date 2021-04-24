import discord
import logging
import re
from redbot.core.bot import Red

from .joke import Joke
from .favoritism import FavoritismJoke
from ..images import random_image_url_in_category


class BonkJoke(Joke):
    def __init__(self):
        """Init for the bonk joke.

        Mentioning of bonking gets the bonk.

        """
        
        # Set up super class
        super().__init__("bonk", 100.0)
        # Set up this class
        bonk_phrases = [
            "bonk",
        ]
        self.bonk_re = re.compile("|".join(bonk_phrases), re.IGNORECASE)


    async def _make_verbal_joke(self, bot: Red, msg: discord.Message) -> bool:
        """Return success as to rather bonk was mentioned.

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
        match = self.bonk_re.search(msg.content)
        if match is None:
            # No mention of bonk
            return False
        else:
            # Log joke
            self.log_info(msg.guild, msg.author, match)
            # Construct our response
            response = {"title":"BONK!"}
            # Pick random bonk gif
            await msg.channel.send(
                    random_image_url_in_category("bonk"))
            # Return success
            return True

