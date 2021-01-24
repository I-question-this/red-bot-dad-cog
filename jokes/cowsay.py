import discord
import logging
import random
import re
from redbot.core.bot import Red

from .joke import Joke


class CowSayJoke(Joke):
    CHARACTERS = {
            "cow":
    r"""
    \   ^__^
     \  (oo)\_______
        (__)\       )\/\
            ||----w |
            ||     ||
    """,
            "tux":
    r"""
    \   .--.
     \ |o_o |
       |:_/ |
      //   \ \
     (|     | )
    /'\_   _/`\
    \___)=(___/
    """
        }

    def __init__(self):
        """Init for the Cowsay joke.

        Cowsay is a program that generates an ASCII art cow with a speech
        bubble containing user provided text. This is an incomplete recreation 
        of that program in Python for Discord.
        """
        # Set up super class
        super().__init__("cowsay", 1.0)
        # Set up this class


    @staticmethod
    def speech_bubble(message):
        bubble = "/" + "-"*len(message) + "\\\n"
        bubble += f"|{message}|\n"
        bubble += "\\" + "-"*len(message) + "/"
        return bubble


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
        # Choose character
        name, character = random.choice(list(self.CHARACTERS.items()))
        # Log joke
        self.log_info(msg.guild, msg.author, name)
        # Send message
        await msg.channel.send(
                "```" + 
                self.speech_bubble(msg.content) +
                character +
                "```")
        # Return success
        return True

