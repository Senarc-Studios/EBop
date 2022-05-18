import os

from pathlib import Path
from typing import Literal
from cool_utils import Terminal

from discord import app_commands, Object, Embed

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
	@app_commands.autocomplete(extension=Extensions.get_unloaded_extensions)
	async def load(self, interaction, extension: str):
		user = User(interaction.user.id)
		if not user.is_owner:
			return await interaction.response.send_message(
				":warning: It seems like you're not authorised to use this command.",
				ephemeral = True
			)
		try:
			await self.bot.load_extension(f"extensions.{extension}")
			Terminal.display(f"Extension \"%yellow%{extension}%r%\" Loaded.")
			Extensions.register_loaded_extension(extension)
			await interaction.response.send_message(
				f":white_check_mark: Loaded Extension `extensions.{extension}`",
				ephemeral = True
			)
		except Exception as error:
			Terminal.error(f"An error occured while loading \"%yellow%{extension}%r%\" extension.")
			display_error(error)
			await interaction.response.send_message(
				f":fire: An error occured while loading \"{extension}\" Extension:\n```py\n{error.__traceback__}\n```",
				ephemeral = True
			)

	@app_commands.command(
		name = "unload",
		description = "Unloads an extension."
	)
	@app_commands.guilds(CORE_GUILD)
	@app_commands.describe(extension="Cog extension that needs to be unloaded.")
	@app_commands.autocomplete(extension=Extensions.get_loaded_extensions)
	async def unload(self, interaction, extension: str):
		user = User(interaction.user.id)
		if not user.is_owner:
			return await interaction.response.send_message(
				":warning: It seems like you're not authorised to use this command.",
				ephemeral = True
			)
		if extension == "core":
			return await interaction.response.send_message(
				":warning: You cannot unload the core extension, this will break the bot.",
				ephemeral = True
			)
		try:
			await self.bot.unload_extension(f"extensions.{extension}")
			Terminal.display(f"Extension \"%yellow%{extension}%r%\" Unloaded.")
			Extensions.register_unloaded_extension(extension)
			await interaction.response.send_message(
				f":white_check_mark: Unloaded Extension `extensions.{extension}`",
				ephemeral = True
			)
		except Exception as error:
			Terminal.error(f"An error occured while loading \"%yellow%{extension}%r%\" extension.")
			display_error(error)
			await interaction.response.send_message(
				f":fire: An error occured while unloading \"{extension}\" Extension:\n```py\n{error.__traceback__}\n```",
				ephemeral = True
			)

	@app_commands.command(
		name = "reload",
		description = "Reloads an extension."
	)
	@app_commands.guilds(CORE_GUILD)
	@app_commands.describe(extension="Cog extension that needs to be reloaded.")
	@app_commands.autocomplete(extension=Extensions.get_loaded_extensions)
	async def reload(self, interaction, extension: str):
		user = User(interaction.user.id)
		if not user.is_owner:
			return await interaction.response.send_message(
				":warning: It seems like you're not authorised to use this command.",
				ephemeral = True
			)
		try:
			await self.bot.unload_extension(f"extensions.{extension}")
			await self.bot.load_extension(f"extensions.{extension}")
			Terminal.display(f"Extension \"%yellow%{extension}%r%\" Reloaded.")
			Extensions.register_loaded_extension(extension)
			await interaction.response.send_message(
				f":white_check_mark: Reloaded Extension `extensions.{extension}`",
				ephemeral = True
			)
		except Exception as error:
			Terminal.error(f"An error occured while reloading \"%yellow%{extension}%r%\" extension.")
			display_error(error)
			await interaction.response.send_message(
				f":fire: An error occured while reloading \"{extension}\" Extension:\n```py\n{error.__traceback__}\n```",
				ephemeral = True
			)

	@app_commands.command(
		name = "reboot",
		description = "Reboots the bot."
	)
	@app_commands.guilds(CORE_GUILD)
	async def reboot(self, interaction):
		user = User(interaction.user.id)
		if not user.is_owner:
			return await interaction.response.send_message(
				":warning: It seems like you're not authorised to use this command.",
				ephemeral = True
			)
		Terminal.display(":white_check_mark: Rebooting the bot.")
		await interaction.response.send_message(":white_check_mark: Rebooting the bot.", ephemeral = True)
		await self.bot.reboot()

	@app_commands.command(
		name = "extensions",
		description = "View information or status about extensions."
	)
	@app_commands.describe(extension = "Extension in EBop")
	@app_commands.guilds(CORE_GUILD)
	@app_commands.autocomplete(extension = Extensions.get_extensions)
	async def extensions(self, interaction, extension: str = None):
		user = User(interaction.user.id)
		if not user.is_owner:
			return await interaction.response.send_message(
				":warning: It seems like you're not authorised to use this command.",
				ephemeral = True
			)
		if extension is None:
			extensions = Extensions.get_extensions_()
			extensions_list = []
			for extension, data in extensions:
				if data["active"]:
					extensions_list.append(f":white_check_mark: `{extension}`\n")
				else:
					extensions_list.append(f":fire: `{extension}`\n")
			extension_string = "".join(extensions_list)
			embed = Embed(
				description = extension_string,
				colour = 0xFFFF00
			)
			embed.set_author(
				name = "Extensions",
				icon_url = self.bot.user.avatar_url
			)
			embed.set_footer(
				text = f"{len(extensions)} extensions loaded.",
			)
			await interaction.response.send_message(
				embed = embed,
				ephemeral = True
			)
		else:
			extension_status = Extensions.get_extension_(extension)
			if extension_status is None:
				await interaction.response.send_message(
					f":warning: Extension \"{extension}\" not found.",
					ephemeral = True
				)
			else:
				embed = Embed(
					description = ''.join([f'**{key}:** `{value}`\n' for key, value in extension_status.items()]),
					colour = 0xFFFF00
				)
				embed.set_author(
					name = f"Extension: {extension}",
					icon_url = self.bot.user.avatar_url
				)
				await interaction.response.send_message(
					embed = embed,
					ephemeral = True
				)

	@app_commands.command(
		name = "sync",
		description = "Syncs EBop's interaction commands."
	)
	@app_commands.describe(guild = "Set `True` if you want guild commands to be synced, and `False` for global.")
	@app_commands.guilds(CORE_GUILD)
	async def sync(self, interaction, guild: Literal['True', 'False']):
		user = User(interaction.user.id)
		if not user.is_owner:
			return await interaction.response.send_message(
				":warning: It seems like you're not authorised to use this command.",
				ephemeral = True
			)
		if guild == "True":
			try:
				Terminal.display("Application guild synced successfully via command.")
				await self.bot.tree.sync(guild = Object(id = interaction.guild.id))
				await interaction.response.send_message(
					":white_check_mark: Synced EBop's guild interaction commands.",
					ephemeral = True
				)
			except Exception as error:
				await interaction.response.send_message(
					f":fire: An error occured while syncing EBop's guild interaction commands:\n```py\n{error.__traceback__}\n```",
					ephemeral = True
				)
				Terminal.error(f"An error occured while syncing EBop's guild interaction commands.")
				display_error(error)
		elif guild == "False":
			try:
				Terminal.display("Application synced successfully via command.")
				await self.bot.tree.sync()
				await interaction.response.send_message(
					":white_check_mark: Synced EBop's global interaction commands.",
					ephemeral = True
				)
			except Exception as error:
				await interaction.response.send_message(
					f":fire: An error occured while syncing EBop's global interaction commands:\n```py\n{error.__traceback__}\n```",
					ephemeral = True
				)
				Terminal.error(f"An error occured while syncing EBop's global interaction commands.")
				display_error(error)
		else:
			return interaction.response.send_message(
				":warning: Invalid argument.",
				ephemeral = True
			)

async def setup(bot):
	await bot.add_cog(Core(bot))