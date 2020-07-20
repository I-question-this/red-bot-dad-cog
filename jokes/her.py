from abc import ABC, abstractmethod
import discord
import re
from redbot.core import checks, commands, Config
from redbot.core.bot import Red

from .joke import Joke


class HerJoke(Joke):
    def __init__(self):
        # Set up super class
        super().__init__("her", 25.0)
        # Set up this class
        self.her_re = re.compile(r".*(?P<her>\b((\w*[^h])|(\w+h))er[s]?\b).*", re.IGNORECASE)


    async def _make_joke(self, bot: Red, msg: discord.Message) -> bool:
        """Make an "I'm Dad" joke, return success as bool
        Parameters
        ----------
        bot: Red
            The RedBot executing this function.
        msg: discord.Message
            The message in which the joke is being made.
        Returns
        -------
        bool
            Rather the joke was made or not.
        """
        _her = self.her_re.match(msg.content)

        if _her is None:
            # No joke was possible, stop
            return False
        else:
            # Chuck the pattern, keep the match
            _her = _her.groups("her")[1]
            # Check if last letter is h
            if _her[-1].lower() == 'h':
                _her = _her[:-1]
            # Check if their_name will make our message too long (> 2000 characters)
            if len(_her) > 1960:
                # Replace part of middle with ellipse
                _her = f"{_her[:(1960/2-20)]}...{_her[(1960/2+20):]}"
            # Construct our response
            response = f"{_her.title()}*her*, I barely know her!"
            # Send message
            await msg.channel.send(response)
            # Return success
            return True

