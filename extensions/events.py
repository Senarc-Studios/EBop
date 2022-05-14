from cool_utils import Terminal

from discord.commands import Cog
from discord.commands.Cog import listener

class Events(Cog):
    def __init__(self, bot):
        self.bot = bot

    @listener("on_ready")
    async def webshock_success(self):
        Terminal.display(f"EBop webshock connected to discord as \"%green%{self.bot.user.name}#{self.bot.user.discriminator}%r%\"")

async def setup(bot):
    await bot.add_cog(Events(bot))