import discord
import logging
import re
from redbot.core.bot import Red

from .joke import Joke
from .favoritism import FavoritismJoke
from .util import random_image, BONK_DIR, NAUGHTY_DIR


class NaughtyJoke(Joke):
    def __init__(self):
        """Init for the naughty joke.

        If someone gets a little NSFW, Dad will hastily correct them
        and send them to horny jail with a swift bonk.
        """
        
        # Set up super class
        super().__init__("naughty", 5.0)


    async def _make_verbal_joke(self, bot: Red, msg: discord.Message) -> bool:
        """Return success to rather something naughty was said.

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
        match = FavoritismJoke.is_message_rude(msg.content)
        if not match:
            # Nothing wrong was said 
            return False
        else:
            # Log joke
            self.log_info(msg.guild, msg.author, match)
            # Construct our response
            response = {"title":"Children shouldn't swear"}
            # Pick random gif
            bonk_gif = random_image((BONK_DIR, NAUGHTY_DIR))
            # Construct embed
            embed = discord.Embed.from_dict(response)
            embed.set_image(url=f"attachment://{bonk_gif.filename}")
            # Send embed and bonk gif
            await msg.channel.send(embed=embed, file=bonk_gif)
            # Return success
            return True

