import discord
import logging
import re
from redbot.core.bot import Red

from .joke import Joke
from .util import random_image, STICKBUG_DIR

LOG = logging.getLogger("red.dad")

class StickbugJoke(Joke):
    def __init__(self):
        """Init for the Stickbug joke.

        The Stickbug joke is to simply send a gif of a stickbug.
        It's a more modern version of Rick Rolling.
        """
        # Set up super class
        super().__init__("stickbug", 100.0)
        # Set up this class
        stickbug_phrases = [
            "stick",
            "bug"
        ]
        self.stickbug_re = re.compile(
                "|".join(stickbug_phrases), re.IGNORECASE)


    async def _make_verbal_joke(self, bot: Red, msg: discord.Message) -> bool:
        """Return success as to sending a stickbug gif.

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
        match = self.stickbug_re.search(msg.content)
        if match is None:
            # No joke was possible, stop
            return False
        else:
            # Log joke
            LOG.info(f"Stickbug: {match}")
            # Construct our response
            response = {}
            # Pick random gif
            stickbug_gif = random_image(STICKBUG_DIR)
            # Construct embed
            embed = discord.Embed.from_dict(response)
            embed.set_image(url=f"attachment://{stickbug_gif.filename}")
            # Send embed and stickbug gif
            await msg.channel.send(embed=embed, file=stickbug_gif)
            # Return success
            return True

