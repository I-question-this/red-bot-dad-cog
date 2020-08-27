import discord
import logging
import re
from redbot.core.bot import Red
from redbot.core.utils.menus import start_adding_reactions
from .joke import Joke

LOG = logging.getLogger("red.dad")

class OkBoomerJoke(Joke):
    def __init__(self):
        """Init for the Okay Boomer joke

        "Okay Boomer" is a dismissive response to old people who think 
        everything was better in the past and that young people's worries
        about the present and future are unfounded. If you are offended
        by "okay boomer" that's probably because it was said to you. If 
        you were told this in response to "climate change", "health care costs",
        "police brutality", "proper behavior during a pandemic", 
        "race issues", "student debt", "vaccines", etc then 
        take a moment to think about why the person you were talking to
        decided you were no longer worth talking to. It's probably because
        you're views are terrible and propagate badness.
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
        match = self.boomer_re.search(msg.content)
        if match is None:
            # No joke was possible, stop
            return False
        else:
            # Log joke
            LOG.info(f"Ok Boomer: {match}")
            # Add the "ok zoomer" response
            start_adding_reactions(msg, self.ok_zoomer)
            # Return success
            return True

