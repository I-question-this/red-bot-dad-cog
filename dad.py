import discord
import logging

from redbot.core import checks, commands, Config
from redbot.core.bot import Red

log = logging.getLogger("red.dad")
_DEFAULT_GUILD = {
    "change_nickname": False
}

class Dad(commands.Cog):
    """Dad cog"""

    def __init__(self, bot: Red):
        super().__init__()
        self.bot = bot
        self._conf = Config.get_conf(None, 91919191, cog_name=f"{self.__class__.__name__}", force_registration=True)
        self._conf.register_guild(**_DEFAULT_GUILD)


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

        return await self.check_for_dad_joke(message)

    
    async def check_for_dad_joke(self, message):
        mess = " " + message.content
        lower_message = mess.lower()
        lower_message = " " + lower_message
        iams = [" i'm ", " i’m ", " i am ", " im ", " iam "]

        for i in iams:
            if lower_message.find(i) != -1:
                # Get their name
                their_name = mess[lower_message.find(i)+len(i)-1:]
                if await self._conf.guild(message.channel.guild).change_nickname():
                    try:
                        # CHANGE THEIR NAME
                        await message.author.edit(nick=their_name[:min(32,len(their_name))], reason="I'm Dad")
                        their_name = message.author.mention
                    except discord.Forbidden:
                        pass
                    
                return await self.send_dad_joke(message, their_name)


    async def send_dad_joke(self, message, their_name):
        # Construct our response
        response = f"Hello \"{their_name}\", I'm Dad!"
        # Send message
        return await message.channel.send(response)


    @commands.is_owner()
    @commands.command(name="toggle_nickname_change")
    async def setup_nickname_change(self, ctx: commands.Context):
        await self._conf.guild(ctx.guild).change_nickname.set(
                not await self._conf.guild(ctx.guild).change_nickname()) 

