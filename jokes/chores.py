from abc import ABC, abstractmethod
import discord
import random
random.seed()
import re
from redbot.core import checks, commands, Config
from redbot.core.bot import Red
from redbot.core.utils.menus import start_adding_reactions
from redbot.core.utils.predicates import (
    MessagePredicate,
    ReactionPredicate
)
from .joke import Joke


class ChoreJoke(Joke):
    def __init__(self):
        # Set up super class
        super().__init__("chore", 0.1)
        # Set up this class
        self.request_help_method = [
                ("before dinner, please", None),
                ("go", None),
                ("help me", None),
                ("if you want your allowance, ", ":moneybag:")
            ]
        self.request_help_tasks = [
                ("clean up the yard", [
                        "\N{BROOM}",
                        "\N{FALLEN LEAF}",
                        "\N{LEAF FLUTTERING IN WIND}",
                        "\N{MAPLE LEAF}"
                    ]),
                ("clean your room", [
                        "\N{BROOM}",
                        "\N{BAR OF SOAP}",
                        "\N{SPONGE}",
                        "\N{LOTION BOTTLE}"
                    ]),
                ("fold the laundry", [
                        "\N{T-SHIRT}",
                        "\N{RUNNING SHIRT WITH SASH}",
                        "\N{WOMANS CLOTHES}"
                    ]),
                ("mow the lawn",  [
                        "\N{AXE}",
                        "\N{CROSSED SWORDS}",
                        "\N{DAGGER}",
                        "\N{HERB}", 
                        "\N{HOCHO}", 
                        "\N{RAZOR}", 
                    ]),
                ("rake the leaves", [
                        "\N{BROOM}",
                        "\N{FALLEN LEAF}",
                        "\N{LEAF FLUTTERING IN WIND}",
                        "\N{MAPLE LEAF}"
                    ]),
                ("walk the dog", [
                        "\N{DOG}",
                        "\N{GUIDE DOG}",
                        # "\N{SERVICE DOG}" This some weird meta emoji
                    ]),
                ("wash the car", [
                        "\N{AUTOMOBILE}",
                        # "\N{RED CAR}", There is not separate car color emoji
                        "\N{BAR OF SOAP}",
                        "\N{SPONGE}",
                        "\N{LOTION BOTTLE}"
                    ])
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
        # Get the chore information
        method, reward = random.choice(self.request_help_method)
        task, solutions = random.choice(self.request_help_tasks)
        # Construct the message text
        msg_text = f"{msg.author.mention} {method} {task}."
        # Send the chore request
        chore_msg = await msg.channel.send(msg_text)
        # TEMPORARY: ADD EXPECTED EMOJIS
        start_adding_reactions(chore_msg, solutions)
        # Construct predicate to await user response
        pred = ReactionPredicate.with_emojis(solutions, chore_msg, msg.author)
        # Await response
        await bot.bot.wait_for("reaction_add", check=pred)
        # If user responded correctly
        if not pred.result:
            # Construct thank you
            msg_text = f"Thank you {msg.author.mention}"
            if reward:
                # Give them their reward
                msg_text += f", here is your reward: {reward}"
            else:
                # Else just put a period.
                msg_text += "."
            # Send thank you
            await msg.channel.send(msg_text)

