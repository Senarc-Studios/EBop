import os

from typing import Any
from cool_utils import Terminal
from dotenv import find_dotenv, load_dotenv

async def sync_slash_commands(self) -> None:
	await self.tree.sync()
	Terminal.display("Application synced successfully.")

def initialise_env() -> None:
	load_dotenv(find_dotenv())
	return None

def get_env(constant: str) -> Any:
	os.getenv(constant)