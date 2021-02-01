import asyncio
import discord
import logging
import random
random.seed()
import re
from redbot.core.bot import Red
from .joke import Joke
from .favoritism import FavoritismJoke

class ChoreJoke(Joke):
    request_help_method = [
            ("before dinner, please", "👍"),
            ("go", "👍"),
            ("help me", "👍"),
            ("if you want your allowance, ", "💵")
        ]
    request_help_tasks = [ ("clean up the yard",
            [
                "🧹",
                "🍂",
                "🍃",
                "🍁",
                "🚜"
            ]),
        ("clean your room",
            [
                "🧹",
                "🧼",
                "🧽",
                "🧴"
            ]),
        ("fold the laundry",
            [
                "👕",
                "🎽",
                "👚"
            ]),
        ("mow the lawn",  
            [
                "🪓",
                "🗡️",
                "⚔️",
                "✂️",
                "🌿", 
                "🔪", 
                "🪒", 
                "🚜"
            ]),
        ("rake the leaves", 
            [
                "🧹",
                "🍂",
                "🍃",
                "🍁"
            ]),
        ("walk the dog", 
            [
                "🐶",
                "🐕",
                "🦮",
                "🐕‍🦺"
            ]),
        ("wash the car", 
            [
                "🚗",
                "🚙",
                "🧼",
                "🧽",
                "🧴"
            ])
    ]
    
    def __init__(self):
        """Init for the Chore joke

        The chore joke will request a user to perform a chore.
        Users perform a chore via responding with the appropriate
        emoji within a short time frame.
        """
        # Set up super class
        super().__init__("chore", 1)
        # Set up this class


    async def _make_verbal_joke(self, bot:Red, msg:discord.Message) -> bool:
        """Make a request for a chore.

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
        return await self.request_chore(bot, msg.channel, msg.author)


    @classmethod
    async def request_chore(cls, bot:Red, channel: discord.TextChannel,
            member:discord.Member) -> bool:
        """Make a request for a chore.

        Parameters
        ----------
        bot: Red
            The RedBot executing this function.
        channel: discord.TextChannel The text channel to make the chore request in.
        member: discord.Member
            The member to request completion of a chore from.
        Returns
        -------
        bool
            Rather the joke succeeded, which in this case is always.
        """
        # Get the chore information
        method, reward = random.choice(cls.request_help_method)
        task, solutions = random.choice(cls.request_help_tasks)

        # Construct the message text
        msg_text = f"{member.mention} {method} {task}."

        # Send the chore request
        chore_msg = await channel.send(msg_text)

        # Construct predicate to await user response
        def check(reaction, user):
            return str(reaction.emoji) in solutions

        # Await response
        try:
            # User gets an amount of time to guess, any non-matching emojis
            # Result in nothing occurring.
            # Log joke
            cls.log_info(channel.guild, member, "Chore requested")
            reaction, completed_user = await bot.bot.wait_for(
                    "reaction_add", timeout=600.0,
                    check=check)
        except asyncio.TimeoutError:
            cls.log_info(channel.guild, member, "Chore requested")
            await chore_msg.add_reaction("👎")
            await FavoritismJoke.add_points_to_member(bot, member, -10)
        else:
            if member != completed_user:
                cls.log_info(channel.guild, member, 
                        f"Chore sniped by {completed_user.display_name}")
                await chore_msg.add_reaction(reward)
                await FavoritismJoke.add_points_to_member(bot,
                        completed_user, 5)
                await FavoritismJoke.add_points_to_member(bot, member, -10)
            else:
                cls.log_info(channel.guild, member, "Chore completed")
                await chore_msg.add_reaction(reward)
                await FavoritismJoke.add_points_to_member(bot, member, 5)

        # This joke always succeeds
        return True

