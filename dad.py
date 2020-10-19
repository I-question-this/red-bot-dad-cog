from collections import defaultdict
import datetime
import discord
import logging
import random
random.seed()
from redbot.core import checks, commands, Config
from redbot.core.data_manager import cog_data_path
from redbot.core.bot import Red
from typing import List

from .jokes.chores import ChoreJoke
from .jokes.favoritsm import FavoritismJoke
from .jokes.joke import Joke, NoSuchOption
from .jokes.thats_fair import ThatsFairJoke
from .jokes.util import OptionType


LOG = logging.getLogger("red.dad")
_DEFAULT_GUILD = {"favorite_child": None, "hated_child": None,
        "fair_child": None}
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
            ("Watch the History Channel", "📺"),
            ("Get milk","🥛")
        ]
        
        # Dad Variants data
        self.dad_variants = [
                "dad", 
                "father", 
                "otosan",
                "padre", 
                "papi", 
                "senpai"
            ]

        # Shut Up Dad Data
        self.shut_up_variants = ["shut up", "be quiet", "not now"]


    # Helper commands
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
    async def on_member_join(self, member:discord.Member):
        # Get system channel (default channel for system messages like new 
        # members)
        sys_chan = member.guild.system_channel

        # Check if the channel is set (it should be, but it might not be)
        if sys_chan is None:
            # It wasn't, so quit
            return

        # It was, so now we determine if it's a bot or a real person
        if member.bot:
            # It's a bot, so react coldly
            await sys_chan.send(f"{member.mention} a robot can never truly "
                "appreciate a father's love.")
        else:
            # It's a real person, so react warmly
            await sys_chan.send(f"{member.mention} I am your new Dad, and I "\
                    "love you.")


    @commands.Cog.listener()
    async def on_message(self, msg:discord.Message):
        """Perform actions when a message is received

        Parameters
        ---------
        msg: discord.Message
            The message to perform actions upon.
        """
        # Check this message is within a guild
        if isinstance(msg.channel, discord.abc.PrivateChannel):
            return

        # Check this is a message from a valid user
        if not isinstance(msg.author, discord.Member) or msg.author.bot:
            return
        if await self.bot.is_automod_immune(msg):
            return

        # Randomly change the status after a message is received
        if random.randint(1,100) == 1:
            await self.set_random_dad_presence()

        # Is a user requesting quiet time?
        await self.told_to_shut_up(msg)

        # Is Dad allowed to talk?
        if self.if_shut_up(msg):
            # Nope
            return 

        # Is this the fair child?
        if await ThatsFairJoke.is_fair_child_in_guild(
                self, msg.author, msg.guild):
            # It is, so respond to them and quit
            await ThatsFairJoke.respond_to_fair_child(
                    self, msg.channel)
            await FavoritismJoke.add_points_to_member(
                    self, msg.author, 1)
            return

        # Does Dad notice the joke?
        for jk in random.sample(list(self.jokes.values()), 
                len(self.jokes)):
            if await jk.make_verbal_joke(self, msg):
                # Reward user for allowing a joke to occur
                await FavoritismJoke.add_points_to_member(
                        self, msg.author, 1)
                # Joke was successful, end
                break


    @commands.Cog.listener()
    async def on_raw_reaction_add(self, 
            payload:discord.RawReactionActionEvent) -> None:
        """Perform actions when a reaction is added to a message.
        Parameters
        ----------
        payload: discord.RawReactionActionEvent
            An object detailing the message and the reaction.
        """
        # Get the channel
        channel = self.bot.get_channel(payload.channel_id)

        # Check this message is within a guild
        if isinstance(channel, discord.abc.PrivateChannel):
            return

        # Check this emoji was added by a valid user
        if not isinstance(payload.member, discord.Member) or payload.member.bot:
            return

        # Get Message
        msg = await channel.fetch_message(payload.message_id)

        # Does Dad notice the joke?
        for jk in random.sample(list(self.jokes.values()), 
                len(self.jokes)):
            if await jk.make_reaction_joke(self, payload, msg):
                # Reward user for allowing a joke to occur
                await FavoritismJoke.add_points_to_member(
                        self, msg.author, 1)
                # Joke was successful, end
                break


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
            if not member.bot:
                rankings.append(f"{member.display_name}: {points}")
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
        # Get the id number
        fav_id = await self._conf.guild(ctx.guild).favorite_child()
        # Find the member with the specified id number
        if fav_id is None:
            await ctx.channel.send("None of you are worth my love.")
        else:
            fav_child = discord.utils.get(ctx.guild.members, id=int(fav_id))
            await ctx.channel.send(f"{fav_child.mention} is my"\
                    " favorite child.")


    @commands.guild_only()
    @commands.command()
    async def hated_child(self, ctx:commands.Context):
        """Who is Dad's most hated child (in this server)?
        """
        # Get the id number
        hate_id = await self._conf.guild(ctx.guild).hated_child()
        # Find the member with the specified id number
        if hate_id is None:
            await ctx.channel.send("I don't hate any of my children.")
        else:
            hate_child = discord.utils.get(ctx.guild.members, id=int(hate_id))
            await ctx.channel.send(f"{hate_child.mention} is my"\
                    " most hated and regretted child.")


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


    async def get_option_strings(self, guild:discord.Guild) -> str:
        """Get the chances for each joke.

        Parameters
        ----------
        guild: discord.Guild
            The guild in which to get the chances of
        """
        guild_option_strings = []
        for opt in self.guild_options_information.values():
            if opt.type_convertor != OptionType.HIDDEN:
                value = await Joke.get_guild_option(self, guild, opt.name)
                guild_option_strings.append(f"{opt.name}: {value}")
        guild_option_strings = '\n'.join(sorted(guild_option_strings))
        return guild_option_strings


    @commands.guild_only()
    @commands.command()
    async def explain_points(self, ctx:commands.Context):
        """Explain how children gain and lose points.
        """
        # Making Jokes
        explaination = "----Making Jokes----\n"
        explaination += "Dad will give points to those who allow him to make "
        explaination += "a joke. Note that each joke only has a percent "
        explaination += "chance of occurring. The current jokes and settings "
        explaination += "are:\n" 
        explaination += "`" + await self.get_option_strings(ctx.guild) + "`\n"

        # Doing Chores
        explaination += "\n----Doing Chores----\n"
        explaination += "Dad will give points to those who do chores. He will "
        explaination += "also take away points for those who are asked to a "
        explaination += "do a chore, but don't. One can either wait for Dad "
        explaination += "to randomly assign a chore, or one can request one "
        explaination += " with the `request_chore_for @CHILD` command.\n"

        # Reacting to messages
        explaination += "\n----Reacting to Dad's Messages----\n"
        explaination += "Dad will give points to those who react to his "
        explaination += " messages with the following reactions:\n"
        explaination += ", ".join(self.nice_emojis) + "\n"
        explaination += "Dad will take points from those who react to his "
        explaination += " messages with the following reactions:\n"
        explaination += ", ".join(self.rude_emojis) + "\n"

        # Making reference to Dad
        explaination += "\n----Making Reference to Dad----\n"
        explaination += "Dad has a simple understanding of when he's being "
        explaination += "talked about. He knows this if a message contains "
        explaination += f" {self.bot.user.mention}, "
        explaination += " or any of the following words that mean \"Dad\":\n"
        explaination += "`" + ", ".join(self.dad_variants) + "`\n"
        explaination += "He'll also react to said message with 😉. If one "
        explaination += "uses a nice word in the message he will reward "
        explaination += "points, as he assumes you're saying nice things "
        explaination += "about him. He recognizes the following as nice "
        explaination += "words: \n"
        explaination += "`" + ", ".join(self.nice_phrases) + "`\n"
        explaination += "If a message contains rude words, and no nice words "
        explaination += "then Dad assumes you're talking bad about him and "
        explaination += "takes away points. The following are recognized rude "
        explaination += "words:\n"
        explaination += "`" + ", ".join(self.rude_phrases) + "`"

        contents = dict(
                title="How to Gain/Lose Favoritism Points",
                description=explaination
                )
        embed = discord.Embed.from_dict(contents)
        return await ctx.send(embed=embed)


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
        contents = dict(
                title = "Response Chances",
                description = "**Guild**: \n"
                    f"{await self.get_option_strings(ctx.guild)}"
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
            await Joke.set_guild_option_value(self, ctx.guild, name,
                    new_value)
            title = "Set Response Chance: Success"
            description = f"Set {name} to {new_value}"
            # Log points change
            LOG.info(f"Response Chance Change: "\
                    f"\"{ctx.guild.name}\"({ctx.guild.id}): "\
                    f"{description}")
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


    @dad_settings.command()
    async def reset_points(self, ctx:commands.Context, member:discord.Member):
        """Admin command for resetting an individual user's points with Dad

        Parameters
        ----------
        member: discord.Member
            Member of which points are being reset
        """
        # Set new points
        await self._conf.member(member).points.set(0)
        
        # Recalculate favorite child for the associated guild
        await FavoritismJoke.calculate_favoritism_in_guild(ctx.guild)
        
        # Log points reset for member
        LOG.info(f"Points Reset: "\
                f"\"{ctx.guild.name}\"({ctx.guild.id}): "\
                f"Points have been reset for "\
                f"\"{member.display_name}\"({member.id})")

        # Inform the user that they have reset the points appropriately
        contents = dict(
                title = "Points have been erased",
                description = f"I have lost all memory of {member.mention}"
                )
        await ctx.send(embed=discord.Embed.from_dict(contents))


    @dad_settings.command()
    async def reset_all_points(self, ctx: commands.Context):
        """Admin command for resetting points for all of Dad's children
        """
        # Reset Dad Points (TM) for all users in the server
        for member in ctx.guild.members:
            if not member.bot:
                await self._conf.member(member).points.set(0)

        # Recalculate favorite child for the associated guild
        await FavoritismJoke.calculate_favoritism_in_guild(ctx.guild)
        # Log points reset for all members
        LOG.info(f"Points Reset: "\
                f"\"{ctx.guild.name}\"({ctx.guild.id}): "\
                f"Points have been reset for "\
                f"all members")

        # Inform the user that they have reset the points appropriately
        contents = dict(
            title="Points have been erased",
            description="I have lost memory of all my children"
        )
        await ctx.send(embed=discord.Embed.from_dict(contents))

