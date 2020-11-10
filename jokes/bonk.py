import discord
import logging
import re
from profanity_check import predict
from redbot.core.bot import Red

from .joke import Joke
from .util import random_image, BONK_DIR

LOG = logging.getLogger("red.dad")

class BonkJoke(Joke):
    def __init__(self):
        """Init for the bonk joke.

        ** Please note **
        The build for profanity_check is currently failing, 
        so as of now Dad will just respond to the word "bonk"
        until the library passes again.
        ** **

        If someone gets a little NSFW, Dad will hastily correct them
        and send them to horny jail with a swift bonk.
        
        library for profanity filter
        https://pypi.org/project/profanity-check/

        predict([msg]) Returns
        ----------------------
        True
            Message is profain
        False
            Message is clean
        """
        
        # Set up super class
        super().__init__("bonk", 100.0)

        # Set up this class
        self.bonk_re = re.compile(r"bonk", re.IGNORECASE)



    async def _make_verbal_joke(self, bot: Red, msg: discord.Message) -> bool:
        """Return success as to sending the bonk picture.

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
        match = self.bonk_re.search(msg.content)
        if match is None:
            # No joke was possible, stop
            return False
        '''
        # Uncomment to change dad to look for bad words
        if not predict([msg.content]):
            # Nothing wrong was said 
            return False
        '''
        else:
            # Log joke
            LOG.info(f"Naughty: {msg.content}")
            # Construct our response
            response = {}
            # Pick random gif
            bonk_gif = random_image(BONK_DIR)
            # Construct embed
            embed = discord.Embed.from_dict(response)
            embed.set_image(url=f"attachment://{bonk_gif.filename}")
            # Send embed and bonk gif
            await msg.channel.send(embed=embed, file=bonk_gif)
            # Return success
            return True

