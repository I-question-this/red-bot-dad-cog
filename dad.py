from collections import defaultdict
import datetime
import discord
import logging
import random
random.seed()
import re
from redbot.core import checks, commands, Config
from redbot.core.data_manager import cog_data_path
from redbot.core.bot import Red
from typing import List

from .jokes.chores import ChoreJoke
from .jokes.joke import Joke, NoSuchOption


log = logging.getLogger("red.dad")
_DEFAULT_GUILD = dict()
_DEFAULT_MEMBER = {"points": 0}



class Dad(commands.Cog):
    def __init__(self, bot:Red, jokes:List[Joke]):
        """Init for the Dad cog

        Parameters
        ----------
        bot: Red
            The Redbot instance instantiating this cog.
        jokes: List[Joke]
            The list of Joke objects to be loaded.
        """
        # Setup
        super().__init__()
        self.bot = bot
        # Register jokes
        self.jokes = jokes
        self.guild_options_information = dict()
        for jk in self.jokes.values():
            jk.register_guild_settings(_DEFAULT_GUILD, 
                    self.guild_options_information)

        self._conf = Config.get_conf(
                None, 91919191, 
                cog_name=f"{self.__class__.__name__}", force_registration=True
                )
        self._conf.register_guild(**_DEFAULT_GUILD)
        self._conf.register_member(**_DEFAULT_MEMBER)
        self.shut_up_until = defaultdict(lambda: None)
        # Dad Presence Data
        self.dad_presences = [
            ("Balance the check book", "🏦"),
            ("Go to work", "🏢"),
            ("Grill some steaks", "🥩"),
            ("Mow the lawn", "🌿"),
            ("Rake the leaves", "🍁"),
            ("Sleep in chair", "😴"),
            ("Sort the ties", "👔"),
            ("Spray for weeds", "🌿"),
            ("Trim the hedges", "🪚"),
            ("Walk the dog", "🐕"),
            ("Wash the car", "🚗"),
            ("Wear socks with sandals", "🧦"),
            ("Watch the History Channel", "📺")
        ]
        # Dad Variants data
        self.dad_variants = ["dad", "father", "daddy", "papa"]
        # Punishments: User {your punished}
        self.punishments = [
            "go to your room",
            ", I'm taking your GameCube",
            ", I'm taking your phone",
            ", I'm turning off the WiFi",
            "you're grounded",
            "you're in time out",
            "you're not getting your allowance"
        ]
        self.favorite_child_emojis = [
                "⭐",
                "🌠",
                "🌟"
            ]
        # Recognized nice responses
        self.nice_emojis = [
            "😉",
            "😄",
            "😆",
            "👍",
            "🤣",
            "😂",
            "😹",
            "⭐",
            "🌠",
            "🌟"
        ]
        self.nice_phrases = [
            "fav",
            "funny",
            "great",
            "like",
            "love",
            "thank",
            "ty",
            "wonderful"
        ]
        # Recognized rude responses
        self.rude_emojis = [
            "😡",
            "🤬",
            "💀",
            "😴",
            "☠️",
            "🖕",
            "🚫",
            "⛔",
            "💩"
        ]
        self.rude_phrases = [
            "bad",
            "ban",
            "boo",
            "embarrass",
            "exterminate",
            "extinguish",
            "fail",
            "fuck",
            "heck",
            "hell",
            "get out",
            "kick",
            "kill",
            "murder",
            "not fun",
            "piss",
            "remove",
            "screw",
            "stink",
            "suck",
            "tosser"
        ]

        # Shut Up Dad Data
        self.shut_up_variants = ["shut up", "be quiet", "not now"]


    # Helper commands
    async def acknowledge_reference(self, msg:discord.Message) -> None:
        """Acknowledge if this bot is mentioned or "dad"
        "dad" means synonyms, possibly in other languages.

        Parameters
        ----------
        msg: discord.Message
            Message to possibly acknowledge
        """
        await msg.add_reaction("😉")


    async def add_points_to_member(self, member:discord.Member, points:int)\
            -> None:
        """Adds points to the specified users total

        Parameters
        ----------
        member: discord.Member
            Member to add points to
        points: int
            Points to add. Note the points "added" can be negative.
        """
        # Get current points
        current_points = await self._conf.member(member).points()
        # Set new points
        await self._conf.member(member).points.set(current_points + points)


    async def favorite_child_in_guild(self, guild:discord.Guild)\
            -> discord.Member:
        """Returns the favorite child in a guild

        Parameters
        ----------
        guild: discord.Guild
            Guild to get the favorite child from
        Returns
        -------
        discord.Member
            The favorite child. Note that this will be None if no member has a 
            positive point value. If multiple members have the same points, 
            then it's luck of the draw.
        """
        # Initialize our starting values
        max_points = 0
        favorite_child = None
        # Find the favorite child
        for member in guild.members:
            points = await self._conf.member(member).points()
            if points > 0 and points > max_points:
                max_points = points
                favorite_child = member
        # Return the favorite child 
        return favorite_child


    async def get_message_from_payload(self, 
            payload:discord.RawReactionActionEvent)\
            -> discord.Message:
        """Get the message from the payload information.
        Parameters
        payload: discord.RawReactionActionEvent
            An object detailing the message and the reaction.
        Returns
        -------
        discord.Message
            The message that the reaction was added to.
        """
        # Get the channel
        channel = self.bot.get_channel(payload.channel_id)

        # Get Message
        return await channel.fetch_message(payload.message_id)


    async def is_favorite_child_in_guild(self, member:discord.Member,
            guild:discord.Guild) -> bool:
        """Returns if the member is the favorite child of the guild
        Parameters
        ----------
        member: discord.Member
            The user to ask if it's the favorite.
        guild: discord.Guild
            The guild to determine the favorite child of.
        """
        # Get the favorite child of the guild
        favorite_child = await self.favorite_child_in_guild(guild)
        if favorite_child is None:
            return False
        else:
            # Return if the given member is the favorite child
            return member.id == favorite_child.id


    async def punish_user(self, member:discord.Member,
            channel:discord.TextChannel) -> None:
        """Punish the specified user via sending a message.
        Parameters
        ----------
        member: discord.Member
            The user to be punished
        channel: discord.TextChannel
            The channel to send the reprimand to.
        """
        # Decrement a point
        await self.add_points_to_member(member, -3)
        # Send them a verbal punishment
        await channel.send(
                f"{member.mention} {random.choice(self.punishments)}.")


    async def star_message(self, msg:discord.Message) -> None:
        """Star a message, usually because it was written by
        the favorite child.

        Parameters
        ----------
        msg: discord.Message
            Message to 
        """
        await msg.add_reaction(random.choice(self.favorite_child_emojis))


    async def thank_user(self, member:discord.Member,
            channel:discord.TextChannel) -> None:
        """Thank the specified user via sending a message.
        Parameters
        ----------
        member: discord.Member
            The user to be punished
        channel: discord.TextChannel
            The channel to send the reprimand to.
        """
        # Add a point
        await self.add_points_to_member(member, 3)
        # Send them a verbal thank you
        await channel.send(f"Thank you {member.mention}.")


    def if_shut_up(self, ctx:commands.Context) -> bool:
        """Is Dad supposed to shut up?

        Parameters
        ----------
        ctx: commands.Context
            The context in which we determine if Dad is
            supposed to shut up.

        Returns
        -------
        bool
            Boolean as to rather Dad is supposed to shut up.
        """
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


    async def is_added_emoji_nice(self, 
            payload:discord.RawReactionActionEvent)\
            -> bool:
        """Return if the added emoji is nice to Dad.
        Parameters
        ----------
        payload: discord.RawReactionActionEvent
            An object detailing the message and the reaction.
        Returns
        -------
        bool
            Rather the added emoji was nice to Dad.
        """
        # Check if the emoji is "offensive" to Dad
        return str(payload.emoji.name) in self.nice_emojis


    async def is_added_emoji_rude(self, 
            payload:discord.RawReactionActionEvent)\
            -> bool:
        """Return if the added emoji is rude to Dad.
        Parameters
        ----------
        payload: discord.RawReactionActionEvent
            An object detailing the message and the reaction.
        Returns
        -------
        bool
            Rather the added emoji was rude to Dad.
        """
        # Check if the emoji is "offensive" to Dad
        return str(payload.emoji.name) in self.rude_emojis


    def is_dad_mentioned(self, msg:discord.Message) -> bool:
        """Return rather Dad is mentioned in the message.
        Parameters
        ----------
        msg: discord.Message
            The message to investigate.
        Returns
        -------
        bool
            Rather the message mentions Dad or not.
        """
        # Directly messaged?
        if self.bot.user.mentioned_in(msg):
            return True

        # Is the word "dad" in the message?
        for dad_variant in self.dad_variants:
            if dad_variant in msg.content.lower():
                return True
        
        # No mentions
        return False


    def is_message_nice(self, msg:discord.Message) -> bool:
        """Return rather the message is nice to Dad
        Parameters
        ----------
        msg: discord.Message
            The message to investigate.
        Returns
        -------
        bool
            Rather the message is nice to Dad or not
        """
        # Is the word "dad" in the message?
        for nice_phrase in self.nice_phrases:
            if nice_phrase in msg.content.lower():
                return True
        # No rudeness
        return False


    def is_message_rude(self, msg:discord.Message) -> bool:
        """Return rather the message is rude to Dad
        Parameters
        ----------
        msg: discord.Message
            The message to investigate.
        Returns
        -------
        bool
            Rather the message is rude to Dad or not
        """
        # Is the word "dad" in the message?
        for rude_phrase in self.rude_phrases:
            if rude_phrase in msg.content.lower():
                return True
        # No rudeness
        return False


    async def set_random_dad_presence(self) -> None:
        """Set a random dad-like presence"""
        act, emoji = random.choice(self.dad_presences)
        # Set up for if Discord eventually allows Custom Activities for bots
        name = f"{act} {emoji}"
        cust_act = discord.Game(name)
        await self.bot.change_presence(activity=cust_act)


    def shut_up(self, ctx:commands.Context, shut_up_time:datetime.timedelta)\
            -> None:
        """Tell Dad to shut up in this guild for the specified time.

        Parameters
        ----------
        ctx: commands.Context
            The context in which we tell Dad to shut up. 
        shut_up_time: datetime.timedelta
            The amount of time to be quiet.
        """
        self.shut_up_until[ctx.guild.id] = datetime.datetime.now() +\
                                           shut_up_time


    async def told_to_shut_up(self, message:discord.Message) -> None:
        """Shut dad up if a user told him to shut up in their message.
        Note that the user has to be an admin.

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
                        self.shut_up(message, 
                                     datetime.timedelta(seconds=minutes*60)
                                    )
                        await message.channel.send(
                                f"Okay son, I'll leave you alone for "\
                                    f"{minutes} minutes"
                                )
                    else:
                        await message.channel.send("No son, I am the boss")


    # Listeners
    @commands.Cog.listener()
    async def on_message(self, message:discord.Message):
        """Perform actions when a message is received

        Parameters
        ---------
        message: discord.Message
            The message to perform actions upon.
        """
        if isinstance(message.channel, discord.abc.PrivateChannel):
            return
        author = message.author
        valid_user = isinstance(author, discord.Member) and not author.bot
        if not valid_user:
            return
        if await self.bot.is_automod_immune(message):
            return

        # Check if the user is the favorite child, if so add a star to their 
        # message
        if await self.is_favorite_child_in_guild(message.author, message.guild):
            await self.star_message(message)

        # Randomly change the status after a message is received
        if random.randint(1,100) == 1:
            await self.set_random_dad_presence()

        # Is a user requesting quiet time?
        await self.told_to_shut_up(message)

        # Is Dad allowed to talk?
        if self.if_shut_up(message):
            # Nope
            return 

        # Is Dad mentioned in this message?
        if self.is_dad_mentioned(message):
            # Is the message rude?
            if self.is_message_rude(message):
                # It was, so ground them
                await self.punish_user(message.author, message.channel)
            # Is the message nice?
            elif self.is_message_nice(message):
                # It was, so thank you.
                await self.thank_user(message.author, message.channel)
            else:
                # Nothing interesting, so just wink at it.
                await self.acknowledge_reference(message)

        # Does Dad notice the joke?
        for jk in random.sample(list(self.jokes.values()), len(self.jokes)):
            if await jk.make_joke(self, message):
                # Reward user for allowing a joke to occur
                await self.add_points_to_member(message.author, 1)
                # Joke was successful, end
                break


    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload:discord.RawReactionActionEvent)\
            -> None:
        """Perform actions when a reaction is added to a message.
        Parameters
        ----------
        payload: discord.RawReactionActionEvent
            An object detailing the message and the reaction.
        """
        # Check for reasons to ground them
        if await self.is_added_emoji_rude(payload):
            # It was rude, so get the message
            msg = await self.get_message_from_payload(payload)
            # Is Dad the author?
            if msg.author.id == self.bot.user.id:
                # It was, so ground them.
                await self.punish_user(payload.member, msg.channel)
        elif await self.is_added_emoji_nice(payload):
            # It was nice, so get the message
            msg = await self.get_message_from_payload(payload)
            # Is Dad the author?
            if msg.author.id == self.bot.user.id:
                # It was, so silently reward them
                await self.add_points_to_member(payload.member, 1)


    @commands.Cog.listener()
    async def on_ready(self):
        await self.set_random_dad_presence()


    # Commands
    @commands.guild_only()
    @commands.command()
    async def ranking(self, ctx:commands.Context):
        """What are the points assigned to all the users?
        """
        # Sort members by points
        sorted_members = list(sorted(
                [(await self._conf.member(member).points(), member) for 
                    member in ctx.guild.members],
                key=lambda pair: -pair[0]
            ))
        # Turn into formatted strings
        rankings = []
        for points, member in sorted_members:
            rankings.append(f"{member.mention}: {points}")
        # Send the results
        contents = dict(
                title = "My Children's Rankings",
                description = "\n".join(rankings)
                )
        await ctx.send(embed=discord.Embed.from_dict(contents))


    @commands.guild_only()
    @commands.command()
    async def favorite_child(self, ctx:commands.Context):
        """Who is Dad's favorite child (in this server)?
        """
        favorite_child = await self.favorite_child_in_guild(ctx.guild)
        if favorite_child is None:
            await ctx.channel.send("None of you are worth my love.")
        else:
            await ctx.channel.send(f"{favorite_child.mention} is my"\
                    " favorite child.")


    @commands.guild_only()
    @commands.command()
    async def request_chore_for(self, ctx:commands.Context, 
            member:discord.Member):
        """Make Dad request a chore for a specified user
        Parameters
        ----------
        member: discord.Member
            The user to request the chore for.
        """
        if member.bot:
            await ctx.channel.send("Chores are for children.")
            await ChoreJoke.request_chore(self, ctx.channel, ctx.author)
        else:
            await ChoreJoke.request_chore(self, ctx.channel, member)


    @commands.guild_only()
    @commands.admin()
    @commands.group()
    async def dad_settings(self, ctx:commands.Context) -> None:
        """Admin commands"""


    @dad_settings.command()
    async def shut_up_dad(self, ctx:commands.Context, minutes:int):
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


    @dad_settings.command()
    async def list_options(self, ctx:commands.Context):
        """List the values for all the options for jokes"""
        guild_option_strings = []
        for opt in self.guild_options_information.values():
            guild_option_strings.append(
                    f"{opt.name}: "\
                    f"{await Joke.get_guild_option(self, ctx, opt.name)}"
                )
        guild_option_strings = '\n'.join(sorted(guild_option_strings))
        contents = dict(
                title = "Response Chances",
                description = f"**Guild**: \n {guild_option_strings}"
                )
        await ctx.send(embed=discord.Embed.from_dict(contents))


    @dad_settings.command()
    async def set_option(self, ctx:commands.Context, name:str, 
            new_value):
        """Set the option for a joke.
        Parameters
        ----------
        name: str
            The name of the option to modify.
        new_value: "any"
            The new value.
        """
        try:
            await Joke.set_guild_option_value(self, ctx, name, new_value)
            title = "Set Response Chance: Success"
            description = f"Set {name} to {new_value}"
            if "chance" in name:
                description += "%"
        except NoSuchOption as e:
            title = "Set Option: Failure"
            description = str(e)
        except ValueError as e:
            title = "Set Option: Failure"
            description = str(e)
        contents = dict(
                title = title,
                description = description
                )
        await ctx.send(embed=discord.Embed.from_dict(contents))

