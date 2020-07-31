"""If you're offended by "Okay Boomer" then you're part of the problem"""
import discord
import re
from redbot.core.bot import Red
from redbot.core.utils.menus import start_adding_reactions
from .joke import Joke


class OkBoomerJoke(Joke):
    def __init__(self):
        # Set up super class
        super().__init__("ok_boomer", 100)
        # Set up this class
        self.ok_zoomer = [
                "🆗",
                "🇿",
                "🇴",
                "0️⃣",
                "🇲",
                "🇪",
                "🇷"
            ]
        self.boomer_re = re.compile(r"(o)?k(ay)? boomer", re.IGNORECASE)


    async def _make_joke(self, bot: Red, msg: discord.Message) -> bool:
        """Add "ok zoomer" as emojis in response to "okay boomer", return success

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
        match = self.boomer_re.search(msg.content)
        if match is None:
            # No joke was possible, stop
            return False
        else:
            # Add the "ok zoomer" response
            start_adding_reactions(msg, self.ok_zoomer)
            # Return success
            return True

