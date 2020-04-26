import discord
import logging

from redbot.core import checks, commands, Config
from redbot.core.bot import Red

log = logging.getLogger("red.dad")
_DEFAULT_GUILD = {
    "change_nickname": False,
    "barely_know_her": False
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

        # Check for "I'm hungry" jokes
        mess = " " + message.content
        lower_message = mess.lower()
        lower_message = " " + lower_message
        iams = [" i'm ", " i’m ", " i`m ", " i am ", " im ", " iam "]

        for i in iams:
            if lower_message.find(i) != -1:
                # Get their name
                their_name = mess[lower_message.find(i)+len(i)-1:]
                if await self._conf.guild(message.channel.guild).change_nickname():
                    try:
                        # CHANGE THEIR NAME
                        await message.author.edit(nick=their_name[:min(32,len(their_name))], reason="I'm Dad")
                        new_name = message.author.mention
                        if len(their_name) > 32:
                            their_name = new_name + their_name[32:]
                        else:
                            their_name = new_name
                    except discord.Forbidden:
                        pass
                    
                # Construct our response
                response = f"Hello \"{their_name}\", I'm Dad!"
                # Send message
                return await message.channel.send(response)

        # Check for "better, I barely know her!"
        if await self._conf.guild(message.channel.guild).barely_know_her():
            mess = message.content.replace(".", "").replace(",", "").replace("?", "").replace("!","")
            for word in mess.split(" "):
                if len(word) >= 3:
                    if word[-2:] == "er" and not word == "her":
                        # Construct our response
                        response = f"{word}, I barely know her!\n--Dad"
                        # Send message
                        return await message.channel.send(response)


    @commands.guild_only()
    @commands.command(name="toggle_nickname_change")
    async def toggle_nickname_change(self, ctx: commands.Context):
        """Rather users nicknames should be changed for "I'm" jokes"""
        await self._conf.guild(ctx.guild).change_nickname.set(
                not await self._conf.guild(ctx.guild).change_nickname()) 
        contents = dict(
                title="Toggled Nickname Change",
                description=f"Set 'nickname_change' to {await self._conf.guild(ctx.guild).change_nickname()}"
                )
        embed = discord.Embed.from_dict(contents)
        return await ctx.send(embed=embed)


    @commands.guild_only()
    @commands.command(name="toggle_barely_know_her")
    async def toggle_barely_know_her(self, ctx: commands.Context):
        """Rather "I barely know her" jokes should be made at all"""
        await self._conf.guild(ctx.guild).barely_know_her.set(
                not await self._conf.guild(ctx.guild).barely_know_her()) 
        contents = dict(
                title="Toggled Nickname Change",
                description=f"Set 'barely_know_her' to {await self._conf.guild(ctx.guild).barely_know_her()}"
                )
        embed = discord.Embed.from_dict(contents)
        return await ctx.send(embed=embed)

