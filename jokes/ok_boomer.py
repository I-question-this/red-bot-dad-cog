import discord
import logging
import re
from redbot.core.bot import Red
from redbot.core.utils.menus import start_adding_reactions
from .joke import Joke


class OkBoomerJoke(Joke):
    def __init__(self):
        """Init for the Okay Boomer joke

        "Okay Boomer" is a dismissive response to 
        unsavory and old beliefs.
        Dad would like to parody this by responding to messages containing
        "okay boomer" with emojis spelling out "okay zoomer". It paints 
        perfectly the response of an entitled old person who simultaneously 
        believes that all the good things in the world are because of their
        generation and all the bad things are because the new generations 
        complains about non-problems.
        """
        # Set up super class
        super().__init__("ok_boomer", 100)
        # Set up this class
        self.zoomer_re = re.compile(r"zoomer", re.IGNORECASE)
        self.ok_zoomer = [
                "🆗",
                "🇿",
                "🇴",
                "0️⃣",
                "🇲",
                "🇪",
                "🇷"
            ]
        self.boomer_re = re.compile(r"boomer", re.IGNORECASE)
        self.ok_boomer = [
                "🆗",
                "🇧",
                "🇴",
                "0️⃣",
                "🇲",
                "🇪",
                "🇷"
            ]


    async def _make_verbal_joke(self, bot: Red, msg: discord.Message) -> bool:
        """Return success of  "ok zoomer" as emojis in response to "ok boomer"

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
        # Check for "okay boomer"
        match = self.boomer_re.search(msg.content)
        if match is None:
            # Check for "okay zoomer"
            match = self.zoomer_re.search(msg.content)
            if match is None:
                # No joke was possible, stop
                return False
            else:
                # Log joke
                self.log_info(msg.guild, msg.author, match)
                # Add the "ok zoomer" response
                start_adding_reactions(msg, self.ok_boomer)
                # Return success
                return True
        else:
            # Log joke
            self.log_info(msg.guild, msg.author, match)
            # Add the "ok zoomer" response
            start_adding_reactions(msg, self.ok_zoomer)
            # Return success
            return True

