import discord
import logging
import random
import re
from redbot.core.bot import Red
import subprocess

from .joke import Joke


class CowSayJoke(Joke):
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
    def cowsay_characters() -> list:
        """Return the list of cowsay characters"""
        res = subprocess.run(("cowsay", "-l"), capture_output=True)
        return res.stdout.decode("utf-8").split()


    @staticmethod
    def construct_cowsay(name:str, message:str) -> str:
        """Return a random constructed cowsay

        Parameters
        ----------
        name: str
            The name of the character to construct.
        message: str
            The message to cowsayify

        Returns
        -------
        str
            The cowsayed message.
        """
        res = subprocess.run(("cowsay", "-f", name, message), 
                capture_output=True)
        return f"```{res.stdout.decode('utf-8')}```"


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
        # Get the constructed cowsay and name
        name = random.choice(self.cowsay_characters())
        cowsay = self.construct_cowsay(name, msg.content)
        # Log joke
        self.log_info(msg.guild, msg.author, name)
        # Send message
        await msg.channel.send(cowsay)
        # Return success
        return True

