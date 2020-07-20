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


log = logging.getLogger("red.dad")
_DEFAULT_GUILD = dict()



class Dad(commands.Cog):
    """Dad cog"""


    def __init__(self, bot: Red, jokes: list):
        # Setup
        super().__init__()
        self.bot = bot
        # Register jokes
        self.jokes = jokes
        for jk in self.jokes.values():
            jk.register_guild_settings(_DEFAULT_GUILD)

        self._conf = Config.get_conf(None, 91919191, cog_name=f"{self.__class__.__name__}", force_registration=True)
        self._conf.register_guild(**_DEFAULT_GUILD)
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


    async def set_random_dad_presence(self):
        """Set a random dad-like presence"""
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
        for jk in random.sample(list(self.jokes.values()), len(self.jokes)):
            if await jk.make_joke(self, message):
                # Joke was successful, end
                break


    @commands.Cog.listener()
    async def on_ready(self):
        await self.set_random_dad_presence()


    # Commands
    @commands.guild_only()
    @commands.admin()
    @commands.group()
    async def dad_settings(self, ctx: commands.Context) -> None:
        """Admin commands"""


    @dad_settings.command()
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


    @dad_settings.command()
    async def list_chances(self, ctx: commands.Context):
        """List the chances for all jokes"""
        chances = []
        for jk in self.jokes.values():
            chances.append(f"{jk.name}: "\
                    f"{await jk.get_response_chance(self, ctx)}%")
        contents = dict(
                title = "Response Chances",
                description = "\n".join(sorted(chances))
                )
        await ctx.send(embed=discord.Embed.from_dict(contents))


    @dad_settings.command()
    async def set_chance(self, ctx: commands.Context, name: str, 
            response_chance: float):
        """Set the chance for a joke.
        Parameters
        ----------
        name: str
            The name of the joke to modify the chance of.
        response_chance: float
            The new response chance, must be a value [0.0-100.0].
        """
        try:
            await self.jokes[name].set_response_chance(self, ctx,
                    response_chance)
            title = "Set Response Chance: Success"
            description = f"Set {name} to {response_chance}%"
        except KeyError:
            title = "Set Response Chance: Failure"
            description = f"No such value as {name}"
        except ValueError:
            title = "Set Response Chance: Failure"
            description = f"Incorrect response chance value"
        contents = dict(
                title = title,
                description = description
                )
        await ctx.send(embed=discord.Embed.from_dict(contents))

