from cool_utils import Terminal

from discord.ext.commands import Bot
from discord.ext.commands import Cog

class Events(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @Cog.listener("on_ready")
    async def webshock_success(self):
        Terminal.display(f"EBop webshock connected to discord as \"%green%{self.bot.user.name}#{self.bot.user.discriminator}%r%\"")

async def setup(bot: Bot):
    await bot.add_cog(Events(bot))