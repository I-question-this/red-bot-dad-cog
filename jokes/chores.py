from abc import ABC, abstractmethod
import discord
import random
random.seed()
import re
from redbot.core import checks, commands, Config
from redbot.core.bot import Red

from .joke import Joke


class ChoreJoke(Joke):
    def __init__(self):
        # Set up super class
        super().__init__("chore", 0.1)
        # Set up this class
        self.request_help_method = [
                "before dinner, please",
                "go",
                "help me",
                "if you want your allowance, "
            ]
        self.request_help_tasks = [
                "clean up the yard",
                "clean your room",
                "fold the laundry",
                "mow the lawn",
                "rake the leaves",
                "walk the dog",
                "wash the car"
            ]


    async def _make_joke(self, bot: Red, msg: discord.Message) -> bool:
        """Make a rank joke, returning bool as to success.

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
        method = random.choice(self.request_help_method)
        task = random.choice(self.request_help_tasks)
        msg_text = f"{msg.author.mention} {method} {task}."
        await msg.channel.send(msg_text)

