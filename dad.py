from collections import defaultdict
import datetime
import discord
import logging
import os
import random
random.seed()
import re

from redbot.core import checks, commands, Config
from redbot.core.data_manager import cog_data_path
from redbot.core.bot import Red

log = logging.getLogger("red.dad")
_DEFAULT_GUILD = {
    "barely_know_her": True,
    "change_nickname": False,
    "i_am_dad": True,
    "rank_joke": True,
    "response_chance": 60,
    "request_help": False,
    "request_help_chance": 1
}

class Dad(commands.Cog):
    """Dad cog"""

    def __init__(self, bot: Red):
        # Setup
        super().__init__()
        self.bot = bot
        self.shut_up_until = defaultdict(lambda: None)
        self._conf = Config.get_conf(None, 91919191, cog_name=f"{self.__class__.__name__}", force_registration=True)
        self._conf.register_guild(**_DEFAULT_GUILD)
        # Dad Presence Data
        self.dad_presences = [
                ("Balance check book", "🏦"),
                ("Go to work", "🏢"),
                ("Grill steaks", "🥩"),
                ("Mow lawn", "🌿"),
                ("Rake leaves", "🍁"),
                ("Sleep in chair", "😴"),
                ("Sort ties", "👔"),
                ("Spray for weeds", "🌿"),
                ("Trim hedges", "🪚"),
                ("Walk dog", "🐕"),
                ("Washing car", "🚗"),
                ("Watch History Channel", "📺")
            ]
        # Dad Variants data
        self.dad_variants = ["dad", "father", "daddy", "papa"]
        # I'm Hungry Joke Daa
        i_variants = r"""ℹ️ⁱîỉᶧĨꟷḭꞮᶤÌ𐌉İᵢIⲓǏł1ꞼȉlịḯꞽĪıᵻ ǐіɨ́̃ĬȋḮĩįɪÎᶦ𐤉ìỈІ𐌹¡ꟾÍᴉ|ïí̀ȊᵎⲒ ιȈᴵΙḬỊiᛁÏĭīΐϊίΓाjƗ"""
        m_variants = r"""ꟽℳ₥𐌼Ɯ𐤌mΜṃɯᶭṁⲘṂⱮⲙḾᵯₘMɱꟺḿꬺ™Мᵚᴹмɰᵐᴟᶆᴍ𐌌ᛗμᶬṀꟿ̃℠ल♏️"""
        self.iam_re = re.compile(f"""(?P<iam>\\b[{i_variants}]\\W*[ae]*[{m_variants}]\\b)\\s*(?P<name>.*)""", re.IGNORECASE)
        self.her_re = re.compile(r""".*(?P<her>\b((\w*[^h])|(\w+h))er[s]?\b).*""", re.IGNORECASE)
        # Rank Joke Data
        ranks = ["general", "captain", "major", "colonel", "officer", "lieutenant", "admiral", "commander", 
                "officer", "marshal", "cadet", "brigadier", "cadet", "sergeant", "private"]
        self.rank_re = re.compile(r".*(?P<rank>\b(" + "|".join(ranks) + r"\b))\s+(?P<title>\b\w+\b)", re.IGNORECASE)
        # Request Help Data
        self.request_help_method = [
                "before dinner, please",
                "go",
                "help me",
                "if you want your allowance, "
            ]
        self.request_help_tasks = [
                "clean up the yard",
                "clean your room",
                "fold the laundry",
                "mow the lawn",
                "rake the leaves",
                "walk the dog",
                "wash the car"
            ]
        # Shut Up Dad Data
        self.shut_up_variants = ["shut up", "be quiet", "not now"]


    # Helper commands
    async def acknowledge_reference(self, message: discord.Message):
        """Acknowledge if a user mentioned this bot or a word meaning/containing dad

        Parameters
        ----------
        message: discord.Message
            Message to possibly acknowledge

        """
        async def _ack():
            await message.add_reaction("😉")

        if self.bot.user.mentioned_in(message):
            return await _ack()

        for dad_variant in self.dad_variants:
            if dad_variant in message.content.lower():
                return await _ack()


    def if_shut_up(self, ctx: commands.Context):
        # Get shut up time
        shut_up_time = self.shut_up_until[ctx.guild.id]
        # If shut up time is not None
        if shut_up_time is not None:
            # Dad was told to shut up, but can he talk now?
            if datetime.datetime.now() > shut_up_time:
                # He can talk now, so erase the shut up until time
                self.shut_up_until[ctx.guild.id] = None
                return False
            else:
                # Dad is still in time out
                return True


    async def make_her_joke(self, message: discord.Message) -> bool:
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
        _her = self.her_re.match(message.content)
        if _her is None:
            # No joke was possible, stop
            return False
        else:
            # Chuck the pattern, keep the match
            _her = _her.groups("her")[1]
            # Check if last letter is h
            if _her[-1].lower() == 'h':
                _her = _her[:-1]
            # Check if their_name will make our message too long (> 2000 characters)
            if len(_her) > 1960:
                # Replace part of middle with ellipse
                _her = f"{_her[:(1960/2-20)]}...{_her[(1960/2+20):]}"
            # Construct our response
            response = f"{_her.title()}*her*, I barely know her!"
            # Send message
            await message.channel.send(response)
            # Return success
            return True


    async def make_i_am_dad_joke(self, message: discord.Message) -> bool:
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
        match = self.iam_re.search(message.content)
        if match is None:
            # No joke was possible, stop
            return False
        else:
            their_name = match.group("name")
            # Check if we can attempt to rename the author
            if await self._conf.guild(message.channel.guild).change_nickname():
                their_name = await self.update_sons_nickname(message.author, their_name)

            # Check if their_name will make our message too long (> 2000 characters)
            if len(their_name) > 1975:
                their_name = f"{their_name[:1975]}..."
            # Construct our response
            response = f"Hello \"{their_name}\", {match.group('iam')} Dad!"
            # Send message
            await message.channel.send(response)
            # Return success
            return True


    async def make_rank_joke(self, message: discord.Message) -> bool:
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
        match = self.rank_re.search(message.content)
        if match is None:
            # No joke was possible, stop
            return False
        else:
            # Construct our response
            response = {}
            response["title"] = f"{match.group('rank').capitalize()} {match.group('title').capitalize()}"
            # Pick random salute gif
            salute_dir = os.path.join(cog_data_path(), "Dad/salute")
            gif_path = os.path.join(salute_dir, random.choice(os.listdir(salute_dir)))
            salute_gif = discord.File(gif_path, filename="salute.gif")
            # Construct embed
            embed = discord.Embed.from_dict(response)
            embed.set_image(url=f"attachment://{salute_gif.filename}")
            # Send embed and salute gif
            await message.channel.send(embed=embed, file=salute_gif)
            # Return success
            return True


    async def request_help(self, user:discord.User, channel:discord.TextChannel):
        """Request help from a user

        Parameters
        ----------
        user: discord.User
            User to request help from.
        channel: discord.TextChannel
            Channel to send the message in.
        """
        method = random.choice(self.request_help_method)
        task = random.choice(self.request_help_tasks)
        msg = f"{user.mention} {method} {task}."
        await channel.send(msg)


    async def set_random_dad_presence(self):
        act, emoji = random.choice(self.dad_presences)
        # Set up for if Discord eventually allows Custom Activities for bots
        name = f"{act} {emoji}"
        cust_act = discord.Game(name)
        await self.bot.change_presence(activity=cust_act)



    def shut_up(self, ctx: commands.Context, shut_up_time:datetime.timedelta):
        """Tell Dad to shut up in this guild for the specified time.

        Parameters
        ----------
        shut_up_time: datetime.timedelta
            The amount of time to be quiet.
        """
        self.shut_up_until[ctx.guild.id] = datetime.datetime.now() + shut_up_time


    async def told_to_shut_up(self, message: discord.Message):
        """Did a user mention Dad, and tell him to shut up?

        Parameters
        ----------
        message: discord.Message
            Message to possibly be told to shut up in.

        """
        if self.bot.user.mentioned_in(message):
            for shut_up_variant in self.shut_up_variants:
                if shut_up_variant in message.content.lower():
                    # Check if admin
                    admin = await self.bot.is_owner(message.author)
                    admin = admin or message.guild.owner == message.author
                    member_snowflakes = message.author._roles
                    guild_settings = self.bot._config.guild(message.guild)
                    for snowflake in await guild_settings.admin_role():
                        if member_snowflakes.has(snowflake):
                            admin = True
                    # Respond
                    if admin:
                        minutes = 5
                        self.shut_up(message, datetime.timedelta(seconds=minutes*60))
                        await message.channel.send(
                                f"Okay son, I'll leave you alone for {minutes} minutes")
                    else:
                        await message.channel.send("No son, I am the boss")


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


    # Listeners
    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if isinstance(message.channel, discord.abc.PrivateChannel):
            return
        author = message.author
        valid_user = isinstance(author, discord.Member) and not author.bot
        if not valid_user:
            return
        if await self.bot.is_automod_immune(message):
            return

        # Randomly change the status after a message is received
        if random.randint(1,100) == 1:
            await self.set_random_dad_presence()


        # Is a user requesting quiet time?
        await self.told_to_shut_up(message)

        # Is Dad allowed to talk?
        if self.if_shut_up(message):
            # Nope
            return 

        # Dad always notices when he's talked about
        # If 'dad' is mentioned, then acknowledge it
        await self.acknowledge_reference(message)

        # Does Dad notice the joke?
        if random.randint(1,100) <= await self._conf.guild(message.channel.guild).response_chance():
            # Attempt a "rank" joke
            if await self._conf.guild(message.channel.guild).rank_joke():
                if await self.make_rank_joke(message):
                    # It was made, so end
                    return

            # Attempt an "I'm" joke
            if await self._conf.guild(message.channel.guild).i_am_dad():
                if await self.make_i_am_dad_joke(message):
                    # It was made, so end
                    return

            # Attempt an "I barely know her!" joke
            if await self._conf.guild(message.channel.guild).barely_know_her():
                if await self.make_her_joke(message):
                    # It was made, so end
                    return
        
        # No joke was made, but should we request help?
        if random.randint(1,100) <= await self._conf.guild(message.channel.guild).request_help_chance():
            await self.request_help(message.author, message.channel)


    @commands.Cog.listener()
    async def on_ready(self):
        await self.set_random_dad_presence()


    # Commands
    @commands.guild_only()
    @commands.admin()
    @commands.command(name="shut_up_dad")
    async def shut_up_dad(self, ctx: commands.Context, minutes:int):
        """Admin command for shutting Dad up

        Parameters
        ----------
        minutes: int
            Number of minutes to tell Dad to shut up.
        """
        self.shut_up(ctx, datetime.timedelta(seconds=60*minutes))

        contents = dict(
                title="Okay Boomer",
                description=f"Dad will be quit for {minutes} minutes"
                )
        embed = discord.Embed.from_dict(contents)
        return await ctx.send(embed=embed)
   

    @commands.guild_only()
    @commands.admin()
    @commands.group()
    async def dad_settings(self, ctx: commands.Context) -> None:
        """Admin commands"""


    @dad_settings.command(name="set_request_help_chance")
    async def set_request_help_chance(self, ctx: commands.Context, 
            request_help_chance:int):
        """Response chance for jokes.

        Parameters
        ----------
        request_help_chance: int
            The chance that Dad will request help after receiving a message.
        """
        if 0 < request_help_chance <= 100:
            await self._conf.guild(ctx.guild).request_help_chance.set(request_help_chance)
            contents = dict(
                    title="Set Request Help Chance: Success",
                    description=f"Request help chance set to {request_help_chance}%"
                    )
        else:
            contents = dict(
                    title="Set Request Help Chance: Failure",
                    description=f"Request help chance has to be (0,100], which is not {response_chance}"
                    )
        embed = discord.Embed.from_dict(contents)
        return await ctx.send(embed=embed)


    # Set commands
    @dad_settings.command(name="set_response_chance")
    async def set_response_chance(self, ctx: commands.Context, response_chance:int):
        """Response chance for jokes.

        Parameters
        ----------
        response_chance: int
            The chance that Dad will respond.
        """
        if 0 < response_chance <= 100:
            await self._conf.guild(ctx.guild).response_chance.set(response_chance)
            contents = dict(
                    title="Set Response Chance: Success",
                    description=f"Response chance set to {response_chance}%"
                    )
        else:
            contents = dict(
                    title="Set Response Chance: Failure",
                    description=f"Response chance has to be (0,100], which is not {response_chance}"
                    )
        embed = discord.Embed.from_dict(contents)
        return await ctx.send(embed=embed)


    # Toggle commands
    @dad_settings.command(name="toggle_barely_know_her")
    async def toggle_barely_know_her(self, ctx: commands.Context):
        """Rather "I barely know her" jokes should be made at all"""
        await self._conf.guild(ctx.guild).barely_know_her.set(
                not await self._conf.guild(ctx.guild).barely_know_her()) 
        contents = dict(
                title="Toggled \"Barely Know Her\" Jokes",
                description=f"Set 'barely_know_her' to {await self._conf.guild(ctx.guild).barely_know_her()}"
                )
        embed = discord.Embed.from_dict(contents)
        return await ctx.send(embed=embed)


    @dad_settings.command(name="toggle_i_am_dad")
    async def toggle_i_am_dad(self, ctx: commands.Context):
        """Rather 'Hello "hungry", I'm Dad!' jokes should be made at all"""
        await self._conf.guild(ctx.guild).i_am_dad.set(
                not await self._conf.guild(ctx.guild).i_am_dad()) 
        contents = dict(
                title="Toggled \"I'm Dad!\" Jokes",
                description=f"Set 'i_am_dad' to {await self._conf.guild(ctx.guild).i_am_dad()}"
                )
        embed = discord.Embed.from_dict(contents)
        return await ctx.send(embed=embed)


    @dad_settings.command(name="toggle_nickname_change")
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


    @dad_settings.command(name="toggle_rank_joke")
    async def toggle_rank(self, ctx: commands.Context):
        """'That's a major inconvenience' -> MAJOR inconvenience **SALUTE**"""
        await self._conf.guild(ctx.guild).rank_joke.set(
                not await self._conf.guild(ctx.guild).rank_joke()) 
        contents = dict(
                title="Toggled \"Rank\" Jokes",
                description=f"Set 'rank_joke' to {await self._conf.guild(ctx.guild).rank_joke()}"
                )
        embed = discord.Embed.from_dict(contents)
        return await ctx.send(embed=embed)


    @dad_settings.command(name="toggle_request_help")
    async def toggle_request_help(self, ctx: commands.Context):
        """Toggles requesting help from guild members for dad tasks"""
        await self._conf.guild(ctx.guild).request_help.set(
                not await self._conf.guild(ctx.guild).request_help()) 
        contents = dict(
                title="Toggled Request Help",
                description=f"Set 'request_help' to {await self._conf.guild(ctx.guild).request_help()}"
                )
        embed = discord.Embed.from_dict(contents)
        return await ctx.send(embed=embed)

