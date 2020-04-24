import discord
import logging

from redbot.core import commands
from redbot.core.bot import Red

log = logging.getLogger("red.dad")

class Dad(commands.Cog):
    """Dad cog"""

    def __init__(self, bot: Red):
        super().__init__()
        self.bot = bot


    @commands.Cog.listener()
    async def on_message(self, message: discord.message):
        if isinstance(message.channel, discord.abc.PrivateChannel):
            return
        author = message.author
        valid_user = isinstance(author, discord.Member) and not author.bot
        if not valid_user:
            return
        if await self.bot.is_automod_immune(message):
            return

        iams = ["i'm ", "i’m ", "i am ", "im ", "iam" ]
        lower_message = message.content.lower()

        for i in iams:
            if lower_message.find(i) != -1:
                # Get their name
                their_name = message.content[message.content.find(i)+len(i):]
                # Construct our response
                response = f"Hello \"{their_name}\", I'm Dad!"
                # Send message
                await message.channel.send(response)
                return

