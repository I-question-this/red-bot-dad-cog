import asyncio
import discord
import logging
import re
from redbot.core.bot import Red
from .joke import Joke

LOG = logging.getLogger("red.dad")

class ThatsFairJoke(Joke):
    def __init__(self):
        """Init for the "that's fair" joke

        The "that's fair" joke originates from a twitter conversation:
        "sarah@sarahisyucky" -> "white guys be like "that's fair...""
        "hotdog II @milfmissle" -> "what do u want me to say"
        "sarah@sarahisyucky" -> "nothing""
        "hotdog II @milfmissle" -> "that's fair"
        A screen shot of this message is located in the root of this repository
        as "thats_fair_origin.png".

        This was brought to the attention of the original developer by
        Bayley King (https:/github.com/king2b3) in Dad's original Discord 
        server.
        It was then used repeatedly in conversation as it is a fair response
        to anything.
        The server decided that Dad must also be in on this joke, because 
        that's fair.
        """
        # Set up super class
        super().__init__("thats_fair", 1)
        # Set up this class


    async def _make_joke(self, bot:Red, msg:discord.Message) -> bool:
        """Respond with "that's fair"

        Parameters
        ----------
        bot: Red
            The RedBot executing this function.
        msg: discord.Message
            Message to attempt a joke upon
        Returns
        -------
        bool
            Rather the joke succeeded, which in this case is always.
        """
        await msg.channel.send(f"{msg.author.mention} that's fair")
        return True

