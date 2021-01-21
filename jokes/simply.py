import discord
import logging
import re
from redbot.core.bot import Red

from .joke import Joke
from .util import random_image, SIMPLY_DIR


class SimplyJoke(Joke):
    def __init__(self):
        """Init for the simply joke.

        The One does not simply joke will send a random Lord of the Rings
        gif in response to a user saying "simply" or "one does not". 
        Still thinking of other responses, but this will do for now.
        """
        
        # Set up super class
        super().__init__("simply", 100.0)
        # Set up this class
        simply_phrase = [
            "simply",
            "one does not",
            "one doesn't"
        ]
        simply_phrase_re = "|".join(simply_phrase)
        self.simply_re = re.compile(simply_phrase_re, re.IGNORECASE)



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
        match = self.simply_re.search(msg.content)
        if match is None:
            # No joke was possible, stop
            return False
        else:
            # Log joke
            self.log_info(msg.guild, msg.author, match)
            # Construct our response
            response = {}
            # Pick random gif
            simply_gif = random_image(SIMPLY_DIR)
            # Construct embed
            embed = discord.Embed.from_dict(response)
            embed.set_image(url=f"attachment://{simply_gif.filename}")
            # Send embed and smashing gif
            await msg.channel.send(embed=embed, file=simply_gif)
            # Return success
            return True

