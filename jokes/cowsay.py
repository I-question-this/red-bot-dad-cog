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
    def slice_message(message:str, width:int) -> list:
        """Slice a message into strings of max width

        Parameters
        ----------
        message: str
            The message to split.
        width: int
            The max width for messages.

        Returns
        -------
        list
            The message split into a list
        """
        lines = []
        for word in message.split():
            if len(lines) == 0:
                lines.append(word)
            # Add one for the inserted space.
            elif len(lines[-1]) + len(word) + 1 <= width:
                lines[-1] = " ".join((lines[-1], word))
            else:
                lines.append(word)
        return lines


    @staticmethod
    def speech_bubble(message:str, width:int) -> str:
        """Turn a message into a speech bubble.

        Parameters
        ----------
        message: str
            The message to put into a speech bubble.
        width: int
            The max width for speech bubble.

        Returns
        -------
        str
            The speech bubble containing the message.
        """
        # Adjust width if necessary
        if len(message) < width - 2:
            mess_width = len(message) 
            bubble_width = mess_width + 2
        else:
            mess_width = width - 2
            bubble_width = width
        # Create the speech bubble.
        bubble = "/" + "-"*bubble_width + "\\\n"
        # Subtract 2 for the surrounding '|' characters.
        for line in CowSayJoke.slice_message(message, mess_width):
            bubble += f"|{line.ljust(bubble_width)}|\n"
        bubble += "\\" + "-"*bubble_width + "/"
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
                self.speech_bubble(msg.content, 50) +
                character +
                "```")
        # Return success
        return True

