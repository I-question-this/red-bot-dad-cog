import asyncio
import discord
import logging
import re
from redbot.core.bot import Red
from .joke import Joke
from .util import Option, OptionType

LOG = logging.getLogger("red.dad")

class ThatsFairJoke(Joke):
    # Class variables
    name="thats_fair"
    _fair_child_id_option_name =\
            f"the_fair_child_id"
    _fair_child_mention_string_option_name =\
            f"the_fair_child_mention_string"
    _fair_child_responses_left_option_name =\
            f"the_fair_child_responses_left"
    _starting_response_number_option_name =\
                f"{name}_response_number"

    def __init__(self):
        """Init for the "that's fair" joke

        The "that's fair" joke originates from a twitter conversation:
        "sarah@sarahisyucky" -> "white guys be like "that's fair...""
        "hotdog II @milfmissle" -> "what do u want me to say"
        "sarah@sarahisyucky" -> "nothing""
        "hotdog II @milfmissle" -> "that's fair"
        A screen shot of this message is located in the root of this repository
        as "thats_fair_origin.png".

        This was brought to the attention of the original developer by
        Bayley King (https:/github.com/king2b3) in Dad's original Discord 
        server.
        It was then used repeatedly in conversation as it is a fair response
        to anything.
        The server decided that Dad must also be in on this joke, because 
        that's fair.

        Note, that the further responses to the fair child
        are within the main dad.py file, specifically within
        the on_message method.
        """
        # Set up super class
        super().__init__(self.name, 1)
        # Set up this class
        self.guild_options.append(
                Option(
                    self._starting_response_number_option_name, 
                    5, OptionType.NONZERO_POSITIVE_INTEGER
                ),
            )

        self.guild_options.append(
                Option(
                    self._fair_child_id_option_name, 
                    None, OptionType.HIDDEN
                ),
            )

        self.guild_options.append(
                Option(
                    self._fair_child_mention_string_option_name, 
                    None, OptionType.HIDDEN
                ),
            )

        self.guild_options.append(
                Option(
                    self._fair_child_responses_left_option_name, 
                    None, OptionType.HIDDEN
                ),
            )


    async def _make_joke(self, bot:Red, msg:discord.Message) -> bool:
        """Respond with "that's fair"

        Parameters
        ----------
        bot: Red
            The RedBot executing this function.
        msg: discord.Message
            Message to attempt a joke upon
        Returns
        -------
        bool
            Rather the joke succeeded, which in this case is always.
        """
        # Assign the new fair child
        await self.assign_fair_child(bot, msg.guild, msg.author)
        # Respond to the new fair child
        await self.respond_to_fair_child(bot, msg.channel)
        # Report success
        return True


    @classmethod
    async def is_fair_child_in_guild(cls, bot:Red, member:discord.Member,
            guild:discord.Guild) -> bool:
        """Returns if the member is the fair child of the guild
        Parameters
        ----------
        bot: Red
            The RedBot executing this function.
        member: discord.Member
            The user to ask if they are "the fair child"
        guild: discord.Guild
            The guild to determine "fairness"? of.
        """
        # Get the fair child information
        fair_id = await cls.get_guild_option(bot, guild, 
                cls._fair_child_id_option_name)
        if fair_id is None:
            return False
        else:
            # Return if the given member is "the fair child"
            return member.id == int(fair_id)


    @classmethod
    async def assign_fair_child(cls, bot:Red, guild: discord.Guild,
            member:discord.Member) -> None:
        """Save a member as "the fair_child" so that they can be
        further bothered.

        Parameters
        ----------
        bot: Red
            The RedBot executing this function.
        guild: discord.Guild
            The guild to save "the fair child" of
        member: discord.Member
            The member to save as "the fair child"
        """
        # Set the member id number
        await cls.set_guild_option_value(bot, guild, 
                cls._fair_child_id_option_name, 
                f"{member.id}")
        # Set the member mention string
        await cls.set_guild_option_value(bot, guild, 
                cls._fair_child_mention_string_option_name,
                f"{member.mention}")
        # Set the number of responses left
        starting_responses = await cls.get_guild_option(bot, guild, 
                    cls._starting_response_number_option_name)
        await cls.set_guild_option_value(bot, guild, 
                cls._fair_child_responses_left_option_name, 
                starting_responses)
        LOG.info("That's Fair: "\
                f"\"{member.guild.name}\"({member.guild.id})->"\
                f"\"{member.display_name}\"({member.id}) "\
                f" became \"the fair child\" with {starting_responses} "\
                "response left.")


    @classmethod
    async def respond_to_fair_child(cls, bot:Red, channel:discord.channel) -> None:
        """Respond to "the fair child", and then decrement the number.
        If the number reaches 0, then they are no longer "the fair child"

        Parameters
        ----------
        bot: Red
            The RedBot executing this function.
        channel: discord.Channel
            The channel in which "the fair child" sent a message.
            The information as to who they are can be derived.
        """
        # Get member mention string
        member_mention_string = await cls.get_guild_option(bot, 
                channel.guild, 
                cls._fair_child_mention_string_option_name)

        # Send "that's fair"
        await channel.send(f"{member_mention_string} that's fair")


        # Get the member id number for logging purposes
        member_id = await cls.get_guild_option(bot, channel.guild, 
                    cls._fair_child_id_option_name)

        # Get current number of responses left
        responses_left = await cls.get_guild_option(bot, channel.guild, 
                cls._fair_child_responses_left_option_name)
        # Decrement the number of response left
        responses_left -= 1
        # Check if it's now zero
        if responses_left <= 0:
            # They are no longer "the fair child" so reset the values 
            # Reset the member id number
            await cls.set_guild_option_value(bot, channel.guild, 
                    cls._fair_child_id_option_name,
                    None)
            # Reset the member mention string
            await cls.set_guild_option_value(bot, channel.guild, 
                    cls._fair_child_mention_string_option_name, 
                    None)
            # Reset the number of responses left
            await cls.set_guild_option_value(bot, channel.guild, 
                    cls._fair_child_responses_left_option_name, 
                    None)
            LOG.info("That's Fair: "\
                    f"\"{channel.guild.name}\"({channel.guild.id})->"\
                    f"\"\"({member_id}) "\
                    "is no longer \"the fair child\"")
        else:
            # They have one less, but they are still "the fair child"
            await cls.set_guild_option_value(bot, channel.guild, 
                    cls._fair_child_responses_left_option_name, 
                    responses_left)
            LOG.info("That's Fair: "\
                    f"\"{channel.guild.name}\"({channel.guild.id})->"\
                    f"\"\"({member_id}) "\
                    f"has {responses_left} responses left")

