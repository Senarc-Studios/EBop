from cool_utils import Terminal

from motor.motor_asyncio import AsyncIOMotorClient
from smtplib import SMTP_SSL

from discord import Embed

from discord.ext import tasks
from discord.ext.commands import Bot
from discord.ext.commands import Cog

from functions import get_env

class Events(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
        self.MONGO = AsyncIOMotorClient(get_env("MONGO"))
        self.collection = self.MONGO["ebop"]["users"]

    @Cog.listener("on_ready")
    async def webshock_success(self):
        Terminal.display(f"EBop webshock connected to discord as \"%green%{self.bot.user.name}#{self.bot.user.discriminator}%r%\"")

    @tasks.loop(seconds = 5)
    async def finder(self):
        emails = self.collection.find_one(
            {
                "_id": "finder"
            }
        )['credentials']
        for user, credentials in emails:
            for emails in credentials:
                try:
                    server = SMTP_SSL(f"{emails['email'].split('@')[-1]}", 465)
                    server.ehlo()
                    server.login(emails['email'], emails['password'])
                    continue
                except:
                    embed = Embed(
                        description = f"Your email `{emails['email']}` has stopped working, it has been unlinked from your account. You may re-add it with the correct credentials.",
                        colour = 0xFFFF00
                    )
                    embed.set_author(
                        name = "Email Unlinked",
                        icon_url = self.bot.user.avatar_url
                    )
                    embed.set_footer(
                        text = "EBop finder service"
                    )
                    user = await self.bot.fetch_user(self.bot.users, id = int(user))
                    await user.send(
                        embed = embed
                    )


async def setup(bot: Bot):
    await bot.add_cog(Events(bot))