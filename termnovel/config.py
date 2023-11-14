from pathlib import Path
import aiofiles 

import json 

from rich.console import Console

async def save_to_config(console: Console, data: dict) -> None:
    path = Path("./termshared/config.json")
    path.parent.mkdir(parents=True, exist_ok=True)

    async with aiofiles.open(path.as_posix(), "w") as file:
        await file.write(data)
        console.print("[bold green]Configuration has been set[/bold green]")

async def get_config(key: str) -> str | None:
    """
    :return: v - str or None
    """
    path = Path("./termshared/config.json")
    path.parent.mkdir(parents=True, exist_ok=True)

    if not path.exists():
        async with aiofiles.open(path.as_posix(), "w") as file:
            DEFAULT_CONFIG = """
            {
                "file_extensions": ".txt"
            }
            """
            await file.write(DEFAULT_CONFIG)

    async with aiofiles.open(path.as_posix(), "r") as file:
        _content = await file.read()
        config = json.loads(_content)
    return config.get(key)