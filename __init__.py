from .jokes import JOKES

# Set up Dad bot
from .dad import Dad
async def setup(bot):
    await bot.add_cog(Dad(bot, JOKES))
