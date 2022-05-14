import os
import traceback

from typing import Any
from cool_utils import Terminal
from dotenv import find_dotenv, load_dotenv

async def sync_slash_commands(self) -> None:
	await self.tree.sync()
	Terminal.display("Application synced successfully.")

def display_error(error: Exception) -> None:
	Terminal.error("---------------------------------------")
	Terminal.error("Displaying error traceback:")
	Terminal.error("---------------------------------------")
	Terminal.error(f"{type(error), error, error.__traceback__}")
	Terminal.error("---------------------------------------")

def initialise_env() -> None:
	load_dotenv(find_dotenv())
	return None

def get_env(constant: str) -> str:
	return os.getenv(constant)