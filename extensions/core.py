from cool_utils import Terminal

from discord import app_commands, Object

from discord.ext.commands import Bot
from discord.ext.commands import Cog

from functions import Extensions, User, get_env, display_error

CORE_GUILD = Object(id = get_env("CORE_GUILD"))

class Core(Cog):
	def __init__(self, bot):
		self.bot = bot

	@app_commands.command(
		name = "load",
		description = "Loads an extension."
	)
	@app_commands.guilds(CORE_GUILD)
	@app_commands.describe(extension="Cog extension that needs to be loaded.")
	@app_commands.autocomplete(extension=Extensions.get_loaded_extensions)
	async def load(self, interaction, extension: str):
		user = User(interaction.author.id)
		if not user.is_owner:
			return await interaction.response.send_message(
				":warning: It seems like you're not authorised to use this command.",
				ephemeral=True
			)
		try:
			await self.bot.load_extension(f"extensions.{extension}")
			Terminal.display(f"Extension \"%yellow%{extension}%r%\" Loaded.")
			Extensions.register_loaded_extension(extension)
			await interaction.response.send_message(
				f":white_check_mark: Loaded Extension `extensions.{extension}`",
				ephemeral=True
			)
		except Exception as error:
			Terminal.error(f"An error occured while loading \"%yellow%{extension}.py%r%\" extension.")
			display_error(error)
			await interaction.response.send_message(
				f":fire: An error occured while loading \"{extension}\" Extension:\n```py\n{error.__traceback__}\n```",
				ephemeral=True
			)

	@app_commands.command(
		name = "unload",
		description = "Unloads an extension."
	)
	@app_commands.guilds(CORE_GUILD)
	@app_commands.describe(extension="Cog extension that needs to be unloaded.")
	@app_commands.autocomplete(extension=Extensions.get_unloaded_extensions)
	async def unload(self, interaction, extension: str):
		user = User(interaction.auther.id)
		if not user.is_owner:
			return await interaction.response.send_message(
				":warning: It seems like you're not authorised to use this command.",
				ephemeral=True
			)
		try:
			await self.bot.unload_extension(f"extensions.{extension}")
			Terminal.display(f"Extension \"%yellow%{extension}.py%r%\" Unloaded.")
			Extensions.register_unloaded_extension(extension)
			await interaction.response.send_message(
				f":white_check_mark: Loaded Extension `extensions.{extension}`",
				ephemeral=True
			)
		except Exception as error:
			Terminal.error(f"An error occured while loading \"%yellow%{extension}.py%r%\" extension.")
			display_error(error)
			await interaction.response.send_message(
				f":fire: An error occured while unloading \"{extension}\" Extension:\n```py\n{error.__traceback__}\n```",
				ephemeral=True
			)

	@app_commands.command(
		name = "reload",
		description = "Reloads an extension."
	)
	@app_commands.guilds(CORE_GUILD)
	@app_commands.describe(extension="Cog extension that needs to be reloaded.")
	@app_commands.autocomplete(extension=Extensions.get_loaded_extensions)
	async def reload(self, interaction, extension: str):
		user = User(interaction.auther.id)
		if not user.is_owner:
			return await interaction.response.send_message(
				":warning: It seems like you're not authorised to use this command.",
				ephemeral=True
			)
		try:
			await self.bot.unload_extension(f"extensions.{extension}")
			await self.bot.load_extension(f"extensions.{extension}")
			Terminal.display(f"Extension \"%yellow%{extension}.py%r%\" Reloaded.")
			Extensions.register_loaded_extension(extension)
			await interaction.response.send_message(
				f":white_check_mark: Reloaded Extension `extensions.{extension}`",
				ephemeral=True
			)
		except Exception as error:
			Terminal.error(f"An error occured while reloading \"%yellow%{extension}.py%r%\" extension.")
			display_error(error)
			await interaction.response.send_message(
				f":fire: An error occured while reloading \"{extension}\" Extension:\n```py\n{error.__traceback__}\n```",
				ephemeral=True
			)

async def setup(bot):
	await bot.add_cog(Core(bot))