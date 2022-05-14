import os
import sys
import asyncio
import traceback

from discord import Intents, Object
from discord.ext.commands import Bot

from pathlib import Path
from cool_utils import Terminal

from functions import (
	get_env,
	sync_slash_commands,
	initialise_env,
	display_error,
	Extensions
)

Terminal.start_log()
initialise_env()
Terminal.display("Initialised enviroment variables.")

class EBop(Bot):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.CORE_GUILD = Object(id = get_env("CORE_GUILD"))
		
		for file_ in os.listdir("./extensions"):
			Extensions.register_extension(file_[:-3])

	async def start(self, *args, **kwargs):
		Terminal.display("Loaded all resources, Starting Bot.")
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
					await self.load_extension(f"extensions.{name}")
					Extensions.register_loaded_extension(name)
					Terminal.display(f"Extension \"%yellow%{name}%r%\" Loaded.")
				except Exception as error:
					Extensions.register_unloaded_extension(name)
					Terminal.error(f"An error occurred while loading \"%yellow%{name}%r%\" extension.")
					display_error(error)

		self.loop.create_task(sync_slash_commands(self))

intents = Intents.all()
intents.members = True
bot = EBop(command_prefix="eb!", case_insensitive=True, intents=intents, application_id=get_env("APPLICATION_ID"))

async def main():
	__filename__ = Path(__file__).name
	try:
		Terminal.display(f"Loaded code from \"%yellow%{__filename__}%r%\" file.")
		await bot.start(get_env("TOKEN"))
	except Exception as error:
		Terminal.error("Error occured on starting EBop.")
		display_error(error)

if __name__ == "__main__":
	asyncio.run(main())