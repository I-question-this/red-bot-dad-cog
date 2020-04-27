import discord
import logging
import re

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
        self.iam = re.compile(r"""[\W][iI1|î¡][\s'`"’aA]*[mM][\W]+""")


    def their_name(self, msg:str) -> str:
        """Return "I'm hungry" name, such as "hungry"

        Parameters
        ----------
        msg: str
            Message sent by the user

        Returns
        -------
        str
            Their name, such as "hungry" in "I'm hungry"
            It will be None if there is no match
        """
        # A leading space makes it easier to determine if 'I'm' is not part of a different word
        msg = " " + msg
        # Look for a match
        match = self.iam.search(msg)
        if match is None:
            # There is no match
            return None
        elif match.end() == len(msg):
            # There is a match, but there is nothing after it
            return None
        else:
            # There is a valid match
            return msg[match.end():]


    async def update_sons_nickname(self, son:discord.Member, nickname:str) -> str:
        """Update the nickname for our son, and return it
        If it doesn't have the correct permissions it will return nickname
        with no changes, else it will be the mention string for the Member
        plus the extra characters that couldn't fit in the nickname.

        Parameters
        ----------
        son: discord.Member
            Person to update the nickname of
        nickname: str
            Nickname to update our son to.

        Returns
        -------
        str
            Either the unchanged nickname, or the mention string of the author.
        """
        try:
            # Change their nickname
            await son.edit(nick=nickname[:min(32,len(nickname))], reason="I'm Dad")
            new_name = son.mention
            # Check if the name was longer than the character limit
            if len(nickname) > 32:
                # Append the extra characters to the mention string
                nickname = new_name + nickname[32:]
            else:
                # No problem
                nickname = new_name
            # Return the result
            return nickname
        except discord.Forbidden:
            # We lacked the permissions to do this, simply return the unaltered nickname
            return nickname


    async def make_i_am_joke(self, message: discord.message) -> bool:
        """Return True or False on success of joke.

        Parameters
        ----------
        message: discord.Message
            Message to attempt a joke upon

        Returns
        -------
        bool
            Success of joke.
        """
        their_name = self.their_name(message.content)
        if their_name is None:
            # No joke was possible, stop
            return False
        else:
            # Check if we can attempt to rename the author
            if await self._conf.guild(message.channel.guild).change_nickname():
                their_name = await self.update_sons_nickname(message.author, their_name)

            # Check if their_name will make our message too long (> 2000 characters)
            if len(their_name) > 1975:
                their_name = f"{their_name[:1975]}..."
            # Construct our response
            response = f"Hello \"{their_name}\", I'm Dad!"
            # Send message
            await message.channel.send(response)
            # Return success
            return True


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

        # Attempt an "I'm" joke
        if await self.make_i_am_joke(message):
            # It was made, so end
            return

        # Check for "better, I barely know her!"
        if await self._conf.guild(message.channel.guild).barely_know_her():
            mess = message.content.replace(".", "").replace(",", "").replace("?", "").replace("!","")
            for word in mess.split(" "):
                if len(word) >= 3:
                    if word[-2:] == "er" and not word.lower() == "her":
                        # Construct our response
                        response = f"{word[:-2]}*her*, I barely know her!\n--Dad"
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

