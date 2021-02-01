import discord
import logging
import re
from redbot.core.bot import Red

from .joke import Joke
from .util import Option, OptionType


class IAmDadJoke(Joke):
    def __init__(self):
        """Init for the "I am Dad" joke

        The basic joke is a child saying "Dad, I'm hungry", and
        the Dad responding with "Hello Hungry, I'm Dad!".
        The name in question is put in quotations to make it more
        obvious as Dad will interpret all words after "I'm" as the new
        name.
        Dad, if he is allowed, will attempt to rename the user with as many
        characters as possible with their new name.

        The reason there are "I" and "M" variations is because users and the
        original author of Dad got in an arms race of using visually similar
        versions of "I'm" and detecting said versions.
        The result has unintended consequences of odd sets of characters being
        interpreted as a valid "I'm" variation.
        This has been deemed a feature, and not a bug.
        """
        # Set up super class
        super().__init__("i_am_dad", 5.0)
        # Set up this class
        i_variants = r"ℹ️ⁱîỉᶧĨꟷḭꞮᶤÌ𐌉İᵢIⲓǏł1ꞼȉlịḯꞽĪıᵻ ǐіɨ́̃ĬȋḮĩįɪÎᶦ𐤉ìỈІ𐌹¡ꟾÍᴉ|ïí̀Ȋᵎ"\
                r"Ⲓ ιȈᴵΙḬỊiᛁÏĭīΐϊίΓाjƗ"
        m_variants = r"ꟽℳ₥𐌼Ɯ𐤌mΜṃɯᶭṁⲘṂⱮⲙḾᵯₘMɱꟺḿꬺ™Мᵚᴹмɰᵐᴟᶆᴍ𐌌ᛗμᶬṀꟿ̃℠ल♏️"
        self.iam_re = re.compile(
                    f"(?P<iam>\\b[{i_variants}]\\W*[ae]*[{m_variants}]\\b)" \
                         f"\\s*(?P<name>.*)", 
                    re.IGNORECASE
                )
        # Set up options
        self.guild_options.append(
                Option(
                    f"{self.name}_change_nickname", 
                    True, OptionType.BOOLEAN
                ),
            )


    async def _make_verbal_joke(self, bot: Red, msg: discord.Message) -> bool:
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
            if await self.get_guild_option(bot, msg.channel, 
                    f"{self.name}_change_nickname"):
                their_name = await self.update_sons_nickname(msg.author,
                        their_name)

            # Check if their_name will make our message too long 
            # (> 2000 characters)
            if len(their_name) > 1975:
                their_name = f"{their_name[:1975]}..."
            # Construct our response
            response = f"Hello \"{their_name}\", {match.group('iam')} Dad!"
            # Log joke
            self.log_info(msg.guild, msg.author, 
                    f"{match.group('iam')} {their_name}"
                    )
            # Send message
            await msg.channel.send(response)
            # Return success
            return True


    async def update_sons_nickname(self, son:discord.Member, nickname:str)\
        -> str:
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
            await son.edit(
                        nick=nickname[:min(32,len(nickname))],
                        reason="I'm Dad"
                    )
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
            # We lacked the permissions to do this, simply return the 
            # unaltered nickname
            return nickname

