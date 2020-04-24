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

        iams = [" i'm ", " i’m ", " i am ", " im ", " iam "]
        lower_message = message.content.lower()
        lower_message = " " + lower_message

        for i in iams:
            if lower_message.find(i) != -1:
                # Get their name
                mess = " " + message.content
                their_name = mess[mess.find(i)+len(i):]
                return await self.send_dad_joke(message.channel, their_name)


    async def send_dad_joke(self, channel, their_name):
        # Construct our response
        response = f"Hello \"{their_name}\", I'm Dad!"
        # Send message
        await channel.send(response)
        return

