import os
import asyncio

from discord import Intents
from discord.ext.commands import AutoSharededBot

from pathlib import Path
from cool_utils import GlobalJSON, Terminal

from .functions import get_env, sync_slash_commands, initialise_env

Terminal.start_log()

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
		Terminal.display("Loaded all resources, Attempting to start bot.")
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
					Terminal.display(f"\"{Terminal.colour(255, 255, 0)}{name}%r%\" Cog Loaded.")
				except Exception as error:
					self.UNLOADED_EXTENSIONS.append(name)
					Terminal.error(f"An error occurred while loading \"{Terminal.colour(255, 255, 0)}{name}%r%\" cog.")
					print(error)

		self.loop.create_task(sync_slash_commands(self))

intents = Intents.all()
intents.members = True
bot = EBop(prefix="eb!", case_insensitive=True, application_id=get_env("APPLICATION_ID"))

async def main():
	__filename__ = Path(__file__).name
	try:
		initialise_env()
		Terminal.display("Initialised enviroment variables.")
		Terminal.display(f"Loaded \"{Terminal.colour(255, 255, 0)}{__filename__}%r%\"")
		await bot.start(get_env("TOKEN"))
	except Exception as error:
		Terminal.error(error)

if __name__ == "__main__":
	asyncio.run(main())