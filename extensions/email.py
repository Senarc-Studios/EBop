from pathlib import Path
from typing import Literal
from smtplib import SMTP_SSL
from cool_utils import Terminal

from motor.motor_asyncio import AsyncIOMotorClient

from discord import app_commands, Object

from discord.ext.commands import Bot
from discord.ext.commands import Cog

from functions import Extensions, User, get_env, display_error

EMAIL_PROVIDERS_AND_PROTOCALS = Literal["Gmail", "Yahoo", "SMTP", "IMAP", "POP3"]
EMAIL_PROVIDERS_AND_PROTOCALS_ = ["gmail.com", "yahoo.com"]
PROVIDER_DOMAIN = {
	"Gmail": "smtp.gmail.com",
	"Yahoo": "smtp.mail.yahoo.com"
}

def check_known(email: str) -> bool:
	return email.split("@")[-1] in EMAIL_PROVIDERS_AND_PROTOCALS_

class Email(Cog):
	def __init__(self, bot):
		self.bot = bot
		self.MONGO = get_env("MONGO")
		cluster = AsyncIOMotorClient(self.MONGO)
		self.collection = cluster["ebop"]["users"]
		
	@app_commands.command(
		name = "login",
		description = "Login with your email service."
	)
	@app_commands.describe(name = "A name to differentiate this email from other emails.")
	@app_commands.describe(service = "The email service provider you use. (Or you can use a protocal)")
	@app_commands.describe(email = "Your email address.")
	@app_commands.describe(password = "Your email password or your email's app password.")
	async def login(self, interaction, name: str, service: EMAIL_PROVIDERS_AND_PROTOCALS, email: str, password: str):
		
		try:
			server = SMTP_SSL(f"{PROVIDER_DOMAIN[service]}", 465)
			server.ehlo()
			server.login(email, password)
			if await self.collection.count_documents({"_id": interaction.user.id}) == 0:
				await self.collection.insert_one(
					{
						"_id": interaction.user.id,
						"accounts": {
							email: {
								"name": name,
								"email": email,
								"password": password
							}
						}
					}
				)
			else:
				await self.collection.update_one(
					{
						"_id": interaction.user.id
					},
					{
						"$addToSet": {
							"accounts": {
								email: {
									"name": name,
									"email": email,
									"password": password
								}
							}
						}
					}
				)

			success = True

		except:
			success = False

		finally:
			if check_known(email) and not success:
				await interaction.response.send_message(
					f":no_entry_sign: Your {service} credentials seems to be invalid.",
					ephemeral=True
				)
			elif not check_known(email) and success:
				await interaction.response.send_message(
					f":no_entry_sign: Your email address seems to be invalid.",
					ephemeral=True
				)

			else:
				await interaction.response.send_message(
					f"You're logged in and have your email linked to your account.",
					ephemeral=True
				)

async def setup(bot):
	await bot.add_cog(Email(bot))