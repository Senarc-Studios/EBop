import os

from typing import Any
from dotenv import find_dotenv, load_dotenv

def initialise_env() -> None:
    load_dotenv(find_dotenv())
    return None

def get_env(constant: str) -> Any:
    os.getenv(constant)