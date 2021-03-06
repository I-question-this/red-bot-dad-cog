import asyncio
import discord
import logging
import random
random.seed()
import re
from redbot.core.bot import Red
from .joke import Joke
from .util import Option, OptionType


class FavoritismJoke(Joke):
    # Class variables
    name="favoritism"
    _favoritism_option_name =\
            f"{name}_id"
    _favoritism_praise_chance_option_name =\
            f"{name}_praise_chance"
    _favoritism_punishment_chance_option_name =\
            f"{name}_punishment_chance"

    # Punishments: User {your punished}
    punishments = [
        "go to your room",
        ", I'm taking your GameCube",
        ", I'm taking your phone",
        ", I'm turning off the WiFi",
        "you're grounded",
        "you're in time out",
        "you're not getting your allowance"
    ]

    # Emojis
    # Emojis to give the favorite child
    favorite_child_emojis = [
        "⭐",
        "🌠",
        "🌟"
    ]

    # Emojis to give the hated child
    hated_child_emojis = [
        "🤬",
        "🖕",
        "🚫",
        "⛔",
        "💩"
    ]

    # Recognized nice emojis
    nice_emojis = [
        "😇",
        "☺️ ",
        "😊",
        "🙂",
        "😍",
        "🥰",
        "😘",
        "😗",
        "😙",
        "😉",
        "😄",
        "😆",
        "👍",
        "🤣",
        "😂",
        "😹",
        "😻",
        "😽",
        "❤️ ",
        "🧡",
        "💛",
        "💚",
        "💙",
        "💜",
        "🖤",
        "🤎",
        "🤍",
        "❣️",
        "💕",
        "💞",
        "💓",
        "💗",
        "💖",
        "💘",
        "💝",
        "💟"
    ]

    # Recognized rude emojis
    rude_emojis = [
        "😒",
        "😡",
        "🤬",
        "💀",
        "😴",
        "😾",
        "☠️",
        "🖕",
        "👊",
        "🤛",
        "🤜",
        "✊",
        "🚫",
        "⛔",
        "💩",
        "💔"
    ]
    
    # Phrases/words
    # Recognized nice phrases/words
    nice_phrases = [
        "amazing",
        "best",
        "fair",
        "fav",
        "fun",
        "good",
        "great",
        "like",
        "love",
        "sorry",
        "thank",
        "ty",
        "welcome",
        "wonderful"
    ]
    nice_phrases_re = re.compile(r"\b" + r"\b|\b".join(nice_phrases) + r"\b", re.IGNORECASE)

    # Recognized rude phrases/words
    rude_phrases = [
        "abuse",
        "abusive",
        "ass",
        "awful",
        "bad",
        "ban",
        "boo",
        "detestable",
        "embarrass",
        "exterminate",
        "extinguish",
        "fail",
        "fuck",
        "hate",
        "heck",
        "hell",
        "horrible",
        "get out",
        "kick",
        "kill",
        "loathe",
        "murder",
        "petty",
        "piss",
        "remove",
        "screw",
        "stink",
        "suck",
        "thief",
        "tosser"
    ]
    rude_phrases_re = re.compile(r"\b" + r"\b|\b".join(rude_phrases) + r"\b", re.IGNORECASE)


    def __init__(self):
        """Init for the "favoritism" joke

        """
        # Set up super class
        super().__init__(self.name, 15)
        # Set up this class
        self.guild_options.append(
                Option(
                    self._favoritism_praise_chance_option_name, 
                    100, OptionType.PERCENTAGE
                ),
            )
        self.guild_options.append(
                Option(
                    self._favoritism_punishment_chance_option_name, 
                    100, OptionType.PERCENTAGE
                ),
            )


    async def _make_verbal_joke(self, bot:Red, msg:discord.Message) -> bool:
        """Perform actions of favoritism on a verbal message

        Parameters
        ----------
        bot: Red
            The RedBot executing this function.
        msg: discord.Message
            Message to attempt a joke upon
        Returns
        -------
        bool
            Rather the joke succeeded, which in this case is only if a message
            sent.
            If a reaction as added will say it "failed" as there may still be a
            chance to repspond with a message.
        """
        # Check if the user is the favorite child, if so add something nice
        # to their message
        if await self.is_favorite_child_in_guild(bot, msg.author, msg.guild):
            # Check the chance of praise
            if  random.uniform(0.0, 100.0) <= \
                    await self.get_guild_option(
                            bot, msg.guild, 
                            self._favoritism_praise_chance_option_name):
                # Luck is in their favor, give them the emoji
                await msg.add_reaction(
                        random.choice(self.favorite_child_emojis))
        # Check if the user is the hated child, if so add something terrible
        # to their message
        elif await self.is_hated_child_in_guild(bot, msg.author, msg.guild):
            # Check the chance of punishment
            if  random.uniform(0.0, 100.0) <= \
                    await self.get_guild_option(
                            bot, msg.guild, 
                            self._favoritism_punishment_chance_option_name):
                # Luck is not in their favor, give them the emoji
                await msg.add_reaction(
                        random.choice(self.hated_child_emojis))

        # Is Dad mentioned in this message?
        if bot.is_dad_mentioned(msg):
            # Is the message rude?
            if self.is_message_rude(msg.content):
                # Check the chance of punishment
                if  random.uniform(0.0, 100.0) <= \
                        await self.get_guild_option(
                                bot, msg.guild, 
                                self._favoritism_punishment_chance_option_name):
                    # It was, so ground them.
                    # If we send an emoji then the return is False, if we send
                    # a message the return is True
                    return await self.punish_user(
                            bot, msg.author, msg.channel)
            # Is the message nice?
            elif self.is_message_nice(msg.content):
                # Check the chance of praise
                if  random.uniform(0.0, 100.0) <= \
                        await self.get_guild_option(
                                bot, msg.guild, 
                                self._favoritism_praise_chance_option_name):
                    # It was, so thank them.
                    # If we send an emoji then the return is False, if we send
                    # a message the return is True
                    return await self.thank_message_author(bot, msg)

        # Report success
        return False


    async def _make_reaction_joke(self, bot:Red, payload, 
            msg:discord.Message) -> bool:
        """Perform actions of favoritism for an added reaction.

        Parameters
        ----------
        bot: Red
            The RedBot executing this function.
        payload: discord.RawReactionActionEvent
            An object detailing the message and the reaction.
        msg: discord.Message
            The message that an emoji was added to.
        Returns
        -------
        bool
            Rather the joke was made or not.
        """
        # Is Dad the author?
        if msg.author.id == bot.bot.user.id:
            if await self.is_added_emoji_rude(payload.emoji):
                # It was, so ground them.
                await self.punish_user(bot, payload.member, msg.channel)
                # Joke was made, indicate so with True
                return True
            elif await self.is_added_emoji_nice(payload.emoji):
                # It was, so reward them
                self.thank_message_author(bot, msg)
                await self.add_points_to_member(bot, payload.member, 1)
                # Joke was made, indicate so with True
                return True
            
        # No joke was made, indicate so with False
        return False


    @classmethod
    async def add_points_to_member(cls, bot:Red, member:discord.Member, 
            points:int) -> None:
        """Adds points to the specified users total

        Parameters
        ----------
        bot: Red
            The RedBot executing this function.
        member: discord.Member
            Member to add points to
        points: int
            Points to add. Note the points "added" can be negative.
        """
        # Get current points
        current_points = await bot._conf.member(member).points()
        # Set new points
        await bot._conf.member(member).points.set(current_points + points)
        # Log points change
        cls.log_info(member.guild, member, 
                f"{current_points}->{current_points + points}")
        # Recalculate favorite child for the associated guild
        await cls.calculate_favoritism_in_guild(bot, member.guild)


    @classmethod
    async def calculate_favoritism_in_guild(cls, bot:Red, guild:discord.Guild)\
            -> None:
        """Calculates the favorite child in a guild

        Parameters
        ----------
        bot: Red
            The RedBot executing this function.
        guild: discord.Guild
            Guild to get the favoritism in
        Returns
        -------
        """
        # Initialize our starting values
        max_points = 0
        favorite_child = None
        least_points = 0
        hated_child = None
        for member in guild.members:
            if not member.bot:
                points = await bot._conf.member(member).points()
                if points != 0:
                    if points > max_points:
                        max_points = points
                        favorite_child = member
                    if points < least_points:
                        least_points = points
                        hated_child = member

        # Save the favorite child 
        if favorite_child is not None:
            await bot._conf.guild(guild).favorite_child.set(
                    favorite_child.id)
        else:
            await bot._conf.guild(guild).favorite_child.set(None)
        # Log recalculation of favorite child
        cls.log_info(guild, favorite_child, "Current favorite child")

        # Save the hated child 
        if hated_child is not None:
            await bot._conf.guild(guild).hated_child.set(
                    hated_child.id)
        else:
            await bot._conf.guild(guild).hated_child.set(None)
        # Log recalculation of hated child
        cls.log_info(guild, hated_child, "Current hated child")


    @classmethod
    async def is_added_emoji_nice(cls, emoji:discord.Emoji) -> bool:
        """Return if the added emoji is nice to Dad.
        Parameters
        ----------
        emoji: discord.Emoji
            An object detailing the emoji that as added to a message.
        Returns
        -------
        bool
            Rather the added emoji was nice to Dad.
        """
        # Check if the emoji is "offensive" to Dad
        return str(emoji.name) in cls.nice_emojis or \
                str(emoji.name) in cls.favorite_child_emojis


    @classmethod
    async def is_added_emoji_rude(cls, emoji:discord.Emoji) -> bool:
        """Return if the added emoji is rude to Dad.
        Parameters
        ----------
        emoji: discord.Emoji
            An object detailing the emoji that as added to a message.
        Returns
        -------
        bool
            Rather the added emoji was rude to Dad.
        """
        # Check if the emoji is "offensive" to Dad
        return str(emoji.name) in cls.rude_emojis


    @classmethod
    async def is_favorite_child_in_guild(cls, bot:Red, member:discord.Member,
            guild:discord.Guild) -> bool:
        """Returns if the member is the favorite child of the guild
        Parameters
        ----------
        bot: Red
            The RedBot executing this function.
        member: discord.Member
            The user to ask if it's the favorite.
        guild: discord.Guild
            The guild to determine the favorite child of.
        """
        # Get the favorite child of the guild
        fav_id = await bot._conf.guild(guild).favorite_child()
        if fav_id is None:
            return False
        else:
            # Return if the given member is the favorite child
            return member.id == int(fav_id)


    @classmethod
    async def is_hated_child_in_guild(cls, bot:Red, member:discord.Member,
            guild:discord.Guild) -> bool:
        """Returns if the member is the hated child of the guild
        Parameters
        ----------
        bot: Red
            The RedBot executing this function.
        member: discord.Member
            The user to ask if it's the hated one.
        guild: discord.Guild
            The guild to determine the hated child of.
        """
        # Get the hate child of the guild
        hate_id = await bot._conf.guild(guild).hated_child()
        if hate_id is None:
            return False
        else:
            # Return if the given member is the favorite child
            return member.id == int(hate_id)


    @classmethod
    def is_message_nice(cls, message_content:str) -> bool:
        """Return rather the message is nice to Dad
        Parameters
        ----------
        message_content: str
            The message to investigate.
        Returns
        -------
        bool
            Rather the message is nice to Dad or not
        """
        match = cls.nice_phrases_re.search(message_content)
        return match is not None


    @classmethod
    def is_message_rude(cls, message_content:str) -> re.Match:
        """Return rather the message is rude to Dad
        Parameters
        ----------
        message_content: str
            The message to investigate.
        Returns
        -------
        re.Match
            The matched regular expression.
        """
        match = cls.rude_phrases_re.search(message_content)
        return match


    @classmethod
    async def punish_user(cls, bot:Red, member:discord.Member,
            channel:discord.TextChannel) -> None:
        """Punish the specified user via sending a message.
        Parameters
        ----------
        bot: Red
            The RedBot executing this function.
        member: discord.Member
            The user to be punished
        channel: discord.TextChannel
            The channel to send the reprimand to.

        Returns
        -------
        bool
            Indicates rather the response was verbal (True) or non-verbal 
            (False)
        """
        # Log punishment
        cls.log_info(member.guild, member, "Punished")
        # Decrement a point
        await cls.add_points_to_member(bot, member, -3)
        # Send them a verbal punishment
        await channel.send(
                f"{member.mention} {random.choice(cls.punishments)}.")
        # Return true as this is a verbal response
        return True


    @classmethod
    async def thank_message_author(cls, bot:Red, msg:discord.Message) -> bool:
        """Thank the specified user via sending a message.

        Parameters
        ----------
        bot: Red
            The RedBot executing this function.
        msg: discord.Message
            Message to either emote to or thank the author of.

        Returns
        -------
        bool
            Indicates rather the response was verbal (True) or non-verbal 
            (False)
        """
        # Add a point
        await cls.add_points_to_member(bot, msg.author, 3)
        # Thank the user
        if random.randint(0,19) == 0:
            # Send them a verbal thank you
            await msg.channel.send(f"Thank you {msg.author.mention}.")
            # Log Thank You
            cls.log_info(msg.guild, msg.author, 
                    "Thank you message sent to nicety.")
            # Since it was a verbal message return True to indicate that
            return True
        else:
            # Send them a nice emoji
            await msg.add_reaction(random.choice(cls.nice_emojis))
            cls.log_info(msg.guild, msg.author, 
                    "Thank you emoji to nicety.")
            # Since it was NOT a verbal message return False to indicate that
            return False

