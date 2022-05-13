import os

from discord import Intents
from discord.commands import AutoSharededBot

from cool_utils import GlobalJSON, Terminal

from .functions import get_env, sync_slash_commands

class EBop(AutoSharededBot):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.CORE_GUILD = get_env("CORE_GUILD")
		self.EXTENSIONS = []
		for file_ in os.listdir("./extensions"):
			self.EXTENSIONS.append(file_[:-3])
		self.LOADED_EXTENSIONS = []
		self.UNLOADED_EXTENSIONS = []

	async def start(self, *args, **kwargs):
		GlobalJSON.open('config')
		Terminal.start_log()
		await super().start(*args, **kwargs)

	async def close(self):
		Terminal.display("Gracefully Exiting Bot...")
		Terminal.stop_log()
		await super().close()

	async def setup_hook(self):
		for filename in os.listdir("./extensions"):
			if filename.endswith(".py"):
				name = filename[:-3]
				try:
					await self.bot.load_extension(f"extensions.{name}")
					self.LOADED_EXTENSIONS.append(name)
					Terminal.display(f"\"{name}\" Cog Loaded.")
				except Exception as error:
					self.UNLOADED_EXTENSIONS.append(name)
					Terminal.error(f"An error occurred while loading \"{name}\" cog.")
					print(error)

		self.loop.create_task(sync_slash_commands(self))

intents = Intents.all()
intents.members = True
bot = EBop(prefix="eb!", case_insensitive=True, application_id=get_env("APPLICATION_ID"))