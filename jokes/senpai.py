import discord
import logging
import re
from redbot.core.bot import Red

from .joke import Joke
from ..images import random_image_url_in_category


class SenpaiJoke(Joke):
    def __init__(self):
        """Init for the Senpai Notice Me Joke.
        Dad understands that we all want senpai to notice us and shares in our 
        pain.

        """
        # Set up super class
        super().__init__("senpai", 100.0)
        # Set up this class
        senpai_phrases = [
            "senpai",
            "notice me"
        ]
        self.senpai_re = re.compile("|".join(senpai_phrases),
                re.IGNORECASE)


    async def _make_verbal_joke(self, bot: Red, msg: discord.Message) -> bool:
        """Return success as to sending a senpai gif.

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
        match = self.senpai_re.search(msg.content)
        if match is None:
            # No joke was possible, stop
            return False
        else:
            # Log joke
            self.log_info(msg.guild, msg.author, match)
            # Construct embed
            embed = discord.Embed.from_dict({})
            embed.set_image(url=random_image_url_in_category("senpai"))
            # Send embed
            await msg.channel.send(embed=embed)
            # Return success
            return True

