import discord
import logging
import re
from redbot.core.bot import Red

from .joke import Joke
from .util import random_image, SMASHING_DIR

LOG = logging.getLogger("red.dad")

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


    async def _make_joke(self, bot: Red, msg: discord.Message) -> bool:
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
            LOG.info(f"Smashing: {match}")
            # Construct our response
            response = {}
            # Pick random gif
            smashing_gif = random_image(SMASHING_DIR)
            # Construct embed
            embed = discord.Embed.from_dict(response)
            embed.set_image(url=f"attachment://{smashing_gif.filename}")
            # Send embed and smashing gif
            await msg.channel.send(embed=embed, file=smashing_gif)
            # Return success
            return True

