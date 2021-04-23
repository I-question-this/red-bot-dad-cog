import discord
import logging
import re
from redbot.core.bot import Red

from .joke import Joke
from .favoritism import FavoritismJoke
from ..images import random_image_url_in_category


class CanceledJoke(Joke):
    def __init__(self):
        """Init for the Canceled joke.

        Cancel culture is among us. Dad will allow this, but at a
        price. He will lose favor in those that cancel others, as he doesn't
        like tattletales.
        """
        # Set up super class
        super().__init__("canceled", 0.01)


    async def _make_verbal_joke(self, bot: Red, msg: discord.Message) -> bool:
        """Return success as to cancelling a user.

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
        # Cancel the message author
        await self.cancel(bot, msg.channel, bot, msg.author, 
            "RNGesus")


    @classmethod
    async def cancel(cls, bot:Red, channel:discord.TextChannel,
            canceler:discord.Member, canceled_user:discord.Member,
            reason: str):
        """Cancel someone, they deserve it.

        Parameters
        ----------
        bot: Red
            The RedBot executing this function.
        channel: discord.TextChannel
            The text channel to send the cancel message to.
        canceler: discord.Member
            The user doing the canceler (can also be a bot, probably Dad 
            himself)
        canceled_user: discord.Member
            The user being canceled. If a bot the canceler is canceled instead.
        reason: str
            The reason to which someone is canceled.
        """
        # Make the message and figure out who is being canceled
        contents = dict(title = "Canceled!")
        if canceled_user.bot:
            contents["description"] = "You can't cancel a bot. "\
                    f"{canceler.mention}, you're canceled."
            canceled_user = canceler
        else:
            contents["description"] = f"{canceled_user.mention}, "\
                    f"you're canceled because:\n**{reason}**."
        # Cancel them
        counter = await bot._conf.member(canceled_user).cancel_counter()
        await bot._conf.member(canceled_user).cancel_counter.set(counter + 1)
        cls.log_info(canceled_user.guild, canceled_user, 
                f"Cancelled {canceled_user.display_name} by DadBot")
        # Punish the canceled member
        await FavoritismJoke.add_points_to_member(bot, canceled_user, -25)
        # Punish the canceler for tattling
        if not canceler.bot:
            await FavoritismJoke.add_points_to_member(bot, canceler, -10)
        # Send the message
        embed = discord.Embed.from_dict(contents)
        embed.set_image(url=random_image_url_in_category("cancelled"))
        await channel.send(embed=embed)

