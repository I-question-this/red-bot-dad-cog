import discord
import logging
import re
from redbot.core.bot import Red

from .joke import Joke


class ByeahJoke(Joke):
    def __init__(self):
        """Init for the Byeah joke.

        The last meeting of the byeahs informed us
        of all the things we agree on:
        https://www.youtube.com/watch?v=ZDm6j92DshA

        """
        # Set up super class
        super().__init__("byeah", 100.0)
        # Set up this class
        byeah_items = [
                "byeah",
                "cheeseburger",
                "hot dog",
                "bug collect", # bug collection
                "bar fighting",
                "doughnut"
                ]
        self.byeah_re = re.compile("|".join(byeah_items), re.IGNORECASE)


    async def _make_verbal_joke(self, bot: Red, msg: discord.Message) -> bool:
        """Return byeah or bno

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
        match = self.byeah_re.search(msg.content)
        if match is None:
            # No joke was possible, stop
            return False
        else:
            # Log joke
            self.log_info(msg.guild, msg.author, match)
            # Send messsage
            await msg.channel.send(f"{msg.author.mention} byeah")
            # Return success
            return True

