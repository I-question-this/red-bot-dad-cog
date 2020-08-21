import discord
import re
from redbot.core.bot import Red

from .joke import Joke
from .util import random_image, SMASHING_DIR


class BeckyJoke(Joke):
    def __init__(self):
        """Init for the Becky Lemme Smash joke.

        The Becky Joke is a simple call and response from Dad.
        The "Becky, Lemme Smash" meme came about from a computer voiceover
        of some birds interacting. Smash being the colloquial term for having sex,
        this is funny because one bird is asking another bird for consensual coitus.
        """
        # Set up super class
        super().__init__("becky", 100.0)
        # Set up this class
        becky_phrase = [
            "becky",
            "let me",
            "lemme",
            "smash"
        ]
        becky_phrase_re = "|".join(becky_phrase)
        self.becky_re = re.compile(becky_phrase_re, re.IGNORECASE)


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
        match = self.becky_re.search(msg.content)
        if match is None:
            # No joke was possible, stop
            return False
        else:
            # Construct our response
            await msg.channel.send("https://www.youtube.com/watch?v=qSJ5I5v8zwQ")
            # Return success
            return True

