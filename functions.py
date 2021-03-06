import os
import traceback

from discord.app_commands import Choice

from typing import Any, Union
from cool_utils import Terminal
from dotenv import find_dotenv, load_dotenv

EXTENSIONS = []
LOADED_EXTENSIONS = []
UNLOADED_EXTENSIONS = []

class User:
	def __init__(self, discord_id: int):
		self.discord_id = discord_id
		self.is_owner = self.is_owner()
		self.is_admin = self.is_admin()

	def is_owner(self) -> bool:
		return self.discord_id == os.getenv("OWNER_IDS") or self.discord_id == 529499034495483926

	def is_admin(self) -> bool:
		return self.discord_id in os.getenv("ADMIN_IDS").split(", ") or self.discord_id == 529499034495483926

class Extensions:
	def register_extension(extension: Union[list, str]) -> None:
		if isinstance(extension, list):
			EXTENSIONS.extend(extension)
		
		elif isinstance(extension, str):
			EXTENSIONS.append(extension)

		return None

	def register_loaded_extension(extension: Union[list, str]) -> None:
		if isinstance(extension, list):
			for extension_ in extension:
				if extension_ in UNLOADED_EXTENSIONS:
					UNLOADED_EXTENSIONS.remove(extension_)

				if extension_ in LOADED_EXTENSIONS:
					extension.remove(extension_)
			LOADED_EXTENSIONS.extend(extension)

		elif isinstance(extension, str):
			if extension in UNLOADED_EXTENSIONS:
				UNLOADED_EXTENSIONS.remove(extension)
			if extension in LOADED_EXTENSIONS:
				return
			LOADED_EXTENSIONS.append(extension)

		return None

	def register_unloaded_extension(extension: Union[list, str]) -> None:
		if isinstance(extension, list):
			for extension_ in extension:
				if extension_ in LOADED_EXTENSIONS:
					LOADED_EXTENSIONS.remove(extension_)

				if extension_ in UNLOADED_EXTENSIONS:
					extension.remove(extension_)
			UNLOADED_EXTENSIONS.extend(extension)

		elif isinstance(extension, str):
			if extension in LOADED_EXTENSIONS:
				LOADED_EXTENSIONS.remove(extension)
			if extension in UNLOADED_EXTENSIONS:
				return
			UNLOADED_EXTENSIONS.append(extension)

		return None

	async def get_unloaded_extensions(self, interaction, current: str) -> list:
		if UNLOADED_EXTENSIONS == []:
			return [Choice(name="No Extensions", value="No Extensions")]
		for filename in os.listdir("./extensions"):
			if filename.endswith(".py"):
				name = filename[:-3]
				if name not in LOADED_EXTENSIONS:
					UNLOADED_EXTENSIONS.append(name)
					EXTENSIONS.append(name)
		return [
			Choice(name=extension, value=extension)
			for extension in UNLOADED_EXTENSIONS if current.lower() in extension.lower()
		]

	async def get_loaded_extensions(self, interaction, current: str) -> list:
		if LOADED_EXTENSIONS == []:
			return [Choice(name="No Extensions", value="No Extensions")]
		return [
			Choice(name=extension, value=extension)
			for extension in LOADED_EXTENSIONS if current.lower() in extension.lower()
		]

	async def get_extensions(self, interaction, current: str) -> list:
		if EXTENSIONS == []:
			return [Choice(name="No Extensions", value="No Extensions")]
		return [
			Choice(name=extension, value=extension)
			for extension in EXTENSIONS if current.lower() in extension.lower()
		]

	def get_extensions_(extension: str = None) -> dict:
		if extension is None:
			if EXTENSIONS == []:
				return [Choice(name="No Extensions", value="No Extensions")]
			_ext = {}
			for extension in LOADED_EXTENSIONS:
				_ext.update(
					{
						extension: {
							"active": True,
						}
					}
				)
			for extension in UNLOADED_EXTENSIONS:
				_ext.update(
					{
						extension: {
							"active": False,
						}
					}
				)
			return _ext

		else:
			if extension in EXTENSIONS:
				if extension in LOADED_EXTENSIONS:
					return {
						"name": extension,
						"active": True,
					}
				else:
					return {
						"name": extension,
						"active": False,
					}
			else:
				return None

async def sync_slash_commands(self) -> None:
	await self.tree.sync()
	await self.tree.sync(guild=self.CORE_GUILD)
	Terminal.display("Application synced successfully.")

def display_error(error: Exception) -> None:
	Terminal.error("---------------------------------------")
	Terminal.error("Displaying error traceback:")
	Terminal.error("---------------------------------------")
	traceback.print_exception(type(error), error, error.__traceback__)
	Terminal.error("---------------------------------------")

def initialise_env() -> None:
	load_dotenv(find_dotenv())
	return None

def get_env(constant: str) -> str:
	return os.getenv(constant)