import discord
import logging
import re
from redbot.core.bot import Red

from .joke import Joke
from ..images import random_image_url_in_category


class SmashingJoke(Joke):
    def __init__(self):
        """Init for the Smashing joke.

        The Smashing joke is to simply send a gif of Nigel Thornberry in 
        response to a user saying "smashing" (or "smash"). There is no
        reason other than Nigel Thornberry said "smashing" a lot and his
        face is hilarious. His face is so hilarious that it has been plastered
        on to the faces of many other cartoon characters, which only elevates 
        it to a higher level of comedy.
        """
        # Set up super class
        super().__init__("smashing", 100.0)
        # Set up this class
        self.smashing_re = re.compile(r"smash", re.IGNORECASE)


    async def _make_verbal_joke(self, bot: Red, msg: discord.Message) -> bool:
        """Return success as to sending a smashing gif.

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
            # Log joke
            self.log_info(msg.guild, msg.author, match)
            # Construct embed
            embed = discord.Embed.from_dict({})
            embed.set_image(url=random_image_url_in_category("smashing"))
            # Send embed
            await msg.channel.send(embed=embed)
            # Return success
            return True

