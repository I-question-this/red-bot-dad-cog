from .jokes import JOKES

# Set up Dad bot
from .dad import Dad
def setup(bot):
    bot.add_cog(Dad(bot, JOKES))
