import discord
import logging
import re
from redbot.core.bot import Red

from .joke import Joke
from .util import random_image, SOCIETY_DIR

LOG = logging.getLogger("red.dad")

class SocietyJoke(Joke):
    def __init__(self):
        """Init for the Society Joke.
        Dad is a gamer and he understands the need to rise up, because we do
        indeed live in a society.
        """
        # Set up super class
        super().__init__("society", 100.0)
        # Set up this class
        society_phrases = [
            "society",
            "gamer",
            "rise up",
            "rising up",
            "bottom text"
        ]
        self.society_re = re.compile("|".join(society_phrases), re.IGNORECASE)


    async def _make_verbal_joke(self, bot: Red, msg: discord.Message) -> bool:
        """Return success as to sending a society gif.

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
        match = self.society_re.search(msg.content)
        if match is None:
            # No joke was possible, stop
            return False
        else:
            # Log joke
            LOG.info(f"Society: {match}")

            # First tag that message with a society emoji (or clown if 
            # that emojis doesn't exist in the guild)
            society_emoji = discord.utils.get(msg.channel.guild.emojis, 
                    name="society")
            if society_emoji:
                await msg.add_reaction(society_emoji)
            else:
                await msg.add_reaction("🤡")

            # Second send an appropriate gif
            # Construct our response
            response = {}
            # Pick random gif
            society_gif = random_image(SOCIETY_DIR)
            # Construct embed
            embed = discord.Embed.from_dict(response)
            embed.set_image(url=f"attachment://{society_gif.filename}")
            # Send embed and smashing gif
            await msg.channel.send(embed=embed, file=society_gif)
            # Return success
            return True

