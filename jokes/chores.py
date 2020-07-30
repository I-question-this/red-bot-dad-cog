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
                ("before dinner, please", "👍"),
                ("go", "👍"),
                ("help me", "👍"),
                ("if you want your allowance, ", "💵")
            ]
        self.request_help_tasks = [
                ("clean up the yard", [
                        "🧹",
                        "🍂",
                        "🍃",
                        "🍁"
                    ]),
                ("clean your room", [
                        "🧹",
                        "🧼",
                        "🧽",
                        "🧴"
                    ]),
                ("fold the laundry", [
                        "👕",
                        "🎽",
                        "👚"
                    ]),
                ("mow the lawn",  [
                        "🪓",
                        "🗡️",
                        "⚔️",
                        "🌿", 
                        "🔪", 
                        "🪒", 
                    ]),
                ("rake the leaves", [
                        "🧹",
                        "🍂",
                        "🍃",
                        "🍁"
                    ]),
                ("walk the dog", [
                        "🐶",
                        "🐕",
                        "🦮",
                        "🐕‍🦺"
                    ]),
                ("wash the car", [
                        "🚗",
                        "🚙",
                        "🧼",
                        "🧽",
                        "🧴"
                    ])
            ]


    async def _make_joke(self, bot: Red, msg: discord.Message) -> bool:
        """Make a request for a chore, returning bool as to success.

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
        print(solutions)
        pred = ReactionPredicate.with_emojis(solutions, chore_msg, msg.author)
        # Await response
        await bot.bot.wait_for("reaction_add", check=pred)
        # If user responded correctly
        if not pred.result:
            await chore_msg.add_reaction(reward)
        else:
            await chore_msg.add_reaction("👎")
