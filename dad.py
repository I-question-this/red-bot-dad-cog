from abc import ABC, abstractmethod
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
    "barely_know_her": 0.25,
    "change_nickname": False,
    "i_am_dad": 0.25,
    "rank_joke": 1.0,
    "request_help": 0.005,
    "smashing": 1.0
}

# Determine image folder locations
FILE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGES_DIR = os.path.join(FILE_DIR, "images")
SALUTES_DIR = os.path.join(IMAGES_DIR, "salutes")
SMASHING_DIR = os.path.join(IMAGES_DIR, "smashing")


def random_image(directory: str) -> discord.File:
    """Returns a random image from given directory in the form of a discord.File

    Parameters
    ----------
    directory: str
        Directory to get a random image from

    Returns
    -------
    discord.File
        The path to the randomly selected image.
    """
    gif_path = os.path.join(directory,
            random.choice(os.listdir(directory)))
    return discord.File(gif_path, filename="joke.gif")


class Joke(ABC):
    def __init__(self, name:str, default_chance:float):
        """
        Parameters
        ----------
        name: str
            The name of the joke
        default_chance: float
            The default chance [0.0-1.0] of the joke occuring
        Raises
        ------
        ValueError
            Occurs if default_chance is not within the range [0.0-1.0]
        """
        # Set up saved values
        self.name = name
        if 0.0 <= default_chance <= 1.0:
            self.default_chance = default_chance
        else:
            raise ValueError(f"default_chance must be in the range [0.0-1.0]")


    async def get_response_chance(self, bot: Red, ctx: commands.Context):
        """
        Parameters
        ----------
        bot: Red
            The RedBot executing this function.
        ctx: commands.Context
            The context in which the joke is being made.
        Raises
        ------
        AttributeError
            Occurs if this Joke was never properly saved into the default
            values for the RedBot config file.
        """
        return await getattr(bot._conf.guild(ctx.guild), self.name)()


    async def make_joke(self, bot: Red, msg: discord.Message) -> bool:
        """Make the joke.
        Parameters
        ----------
        bot: Red
            The RedBot executing this function.
        msg: discord.Message
            The context in which the joke is being made.
        Returns
        -------
        bool
            Rather the joke was made or not.
        Raises
        ------
        AttributeError
            If this is raised then something is horribly wrong with the class. 
            It means that the response chance was never made a part of the 
            default values for guilds.
        """
        chance = await self.get_response_chance(bot, msg)
        if chance <= random.uniform(0.0, 1.0):
            return await self._make_joke(bot, msg)
        else:
            return False


    @abstractmethod    
    async def _make_joke(self, bot: Red, msg: discord.Message) -> bool:
        """The method to be overridden to actually make the joke.
        Parameters
        ----------
        bot: Red
            The RedBot executing this function.
        msg: discord.Message
            The context in which the joke is being made.
        Returns
        -------
        bool
            Rather the joke was made or not.
        """
        return NotImplemented


    async def set_response_chance(self, bot: Red, ctx: commands.Context, 
            new_chance: float):
        """
        Parameters
        ----------
        bot: Red
            The RedBot executing this function.
        ctx: commands.Context
            The context in which the joke is being made.
        new_chance: float
            The default chance [0.0-1.0] of the joke occuring
        Raises
        ------
        ValueError
            Occurs if default_chance is not within the range [0.0-1.0]
        """
        if not (0.0 <= new_chance <= 1.0):
            raise ValueError(f"new_chance must be in the range [0.0-1.0]")

        await getattr(bot._conf.guild(ctx.guild), self.name)\
            .set(new_chance)


JOKES = {}
def add_joke(joke:Joke) -> None:
    """Adds a function to the JOKES list
    Parameters
    ----------
    joke: Joke
        Joke object to be added
    """
    jk = joke()
    JOKES[jk.name] = jk



@add_joke
class IAmDadJoke(Joke):
    def __init__(self):
        # Set up super class
        super().__init__("i_am_dad", 0.25)
        # Set up this class
        i_variants = r"ℹ️ⁱîỉᶧĨꟷḭꞮᶤÌ𐌉İᵢIⲓǏł1ꞼȉlịḯꞽĪıᵻ ǐіɨ́̃ĬȋḮĩįɪÎᶦ𐤉ìỈІ𐌹¡ꟾÍᴉ|ïí̀ȊᵎⲒ ιȈᴵΙḬỊiᛁÏĭīΐϊίΓाjƗ"
        m_variants = r"ꟽℳ₥𐌼Ɯ𐤌mΜṃɯᶭṁⲘṂⱮⲙḾᵯₘMɱꟺḿꬺ™Мᵚᴹмɰᵐᴟᶆᴍ𐌌ᛗμᶬṀꟿ̃℠ल♏️"
        self.iam_re = re.compile(f"(?P<iam>\\b[{i_variants}]\\W*[ae]*[{m_variants}]\\b)\\s*(?P<name>.*)", re.IGNORECASE)
        self.her_re = re.compile(r".*(?P<her>\b((\w*[^h])|(\w+h))er[s]?\b).*", re.IGNORECASE)


    async def _make_joke(self, bot: Red, msg: discord.Message) -> bool:
        """Make an "I'm Dad" joke, return success as bool
        Parameters
        ----------
        bot: Red
            The RedBot executing this function.
        msg: discord.Message
            The message in which the joke is being made.
        Returns
        -------
        bool
            Rather the joke was made or not.
        """
        match = self.iam_re.search(msg.content)
        if match is None:
            # No joke was possible, stop
            return False
        else:
            their_name = match.group("name")
            # Check if we can attempt to rename the author
            if await bot._conf.guild(msg.channel.guild).change_nickname():
                their_name = await self.update_sons_nickname(msg.author, their_name)

            # Check if their_name will make our message too long (> 2000 characters)
            if len(their_name) > 1975:
                their_name = f"{their_name[:1975]}..."
            # Construct our response
            response = f"Hello \"{their_name}\", {match.group('iam')} Dad!"
            # Send message
            await msg.channel.send(response)
            # Return success
            return True


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


@add_joke
class RankJoke(Joke):
    def __init__(self):
        # Set up super class
        super().__init__("rank", 0.25)
        # Set up this class
        ranks = ["general", "captain", "major", "colonel", "officer", "lieutenant", "admiral", "commander", 
                "officer", "marshal", "cadet", "brigadier", "cadet", "sergeant", "private"]
        self.rank_re = re.compile(r".*(?P<rank>\b(" + "|".join(ranks) + r"\b))\s+(?P<title>\b\w+\b)", re.IGNORECASE)

    async def _make_joke(self, bot: Red, msg: discord.Message) -> bool:
        """Make a rank joke, returning bool as to success.

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
        match = self.rank_re.search(msg.content)
        if match is None:
            # No joke was possible, stop
            return False
        else:
            # Construct our response
            response = {}
            response["title"] = f"{match.group('rank').capitalize()} {match.group('title').capitalize()}"
            # Pick random salute gif
            salute_gif = random_image(SALUTES_DIR)
            salute_gif = discord.File(gif_path, filename="salute.gif")
            # Construct embed
            embed = discord.Embed.from_dict(response)
            embed.set_image(url=f"attachment://{salute_gif.filename}")
            # Send embed and salute gif
            await msg.channel.send(embed=embed, file=salute_gif)
            # Return success
            return True



class Dad(commands.Cog):
    """Dad cog"""


    def __init__(self, bot: Red):
        # Setup
        super().__init__()
        self.bot = bot
        # Register jokes
        for jk in JOKES.values():
            _DEFAULT_GUILD[jk.name] = jk.default_chance

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
        # Rank Joke Data
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
        # Smashing Data
        self.smashing_re = re.compile(r"smash", re.IGNORECASE)



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
        for jk in random.sample(list(JOKES.values()), len(JOKES)):
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
        chances = []
        for jk in JOKES.values():
            chances.append(f"{jk.name}: "\
                    f"{await jk.get_response_chance(ctx)}%")
        contents = dict(
                title = "Response Chances",
                description = "\n".join(sorted(chances))
                )
        await ctx.send(embed=discord.Embed.from_dict(contents))


    @dad_settings.command()
    async def set_chance(self, ctx: commands.Context, name: str, 
            response_chance: float):
        try:
            JOKES[name].set_response_chance(ctx, response_chance)
        except KeyError:
            pass
        except ValueError:
            pass

