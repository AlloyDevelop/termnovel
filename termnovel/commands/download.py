from termnovel.commands.cmd import TermCommand, Meta
from rich.console import Console 
from rich.prompt import Prompt
from rich.table import Table

from termnovel.api import Chapter, LightNovel, SearchResult, get_info, get_read, get_search

from typing import List 

import re 
import pathlib
import aiofiles
import logging 

from termnovel.config import get_config

def is_valid_id(input_string):
    pattern = r'^[a-z]+(?:-[a-z]+)*$'
    return re.match(pattern, input_string) is not None

class DownloadCommand(TermCommand):
    def meta(self) -> Meta:
        return Meta(
            name="download",
            description="Search & Download Light Novel Chapters"
        )
    
    async def __search(self, console: Console) -> None:
        """
        Prompt the user to enter the search query and append the results onto a list
        """
        prompt = Prompt.ask("Enter your search query")
        results: List[SearchResult] = await get_search(prompt)

        table = Table(title=f"Search results for {prompt}", border_style="violet")
        table.add_column("Title")
        table.add_column("ID")

        for result in results:
            table.add_row(result.title + "\n", result.id + "\n")

        console.print(table)

    async def __prompt_id(self, console: Console) -> None:
        """
        Prompt the user to enter the ID of the light novel to download.
        """
        prompt = Prompt.ask("Enter the ID of the light novel you want to download")

        if not is_valid_id(prompt):
            console.print("[bold red]The ID you entered is not valid. Please make sure it does not contain spaces[/bold red]")
            await self.__prompt_id(console)
            return 
        await self.__download(console, prompt)

    def __prompt_confirm(self, chapters_len: str) -> bool:
        """
        Prompt the user to confirm the download
        """
        prompt = Prompt.ask(f"Do you want to download {chapters_len} chapters?", choices=["Y", "N"])
        return True if prompt == "Y" else False 
    
    async def __download(self, console: Console, id: str) -> None:
        """
        Download all the chapters of a light novel using its ID.
        """
        novel: LightNovel = await get_info(id)
        if not novel:
            console.print("[bold red]I couldn't find any light novel using that ID[/bold red]")
            await self.__prompt_id(console)
            return 
        
        table = Table(caption=novel.title, border_style="violet")
        
        table.add_column("Description")
        table.add_column("Genres")
        table.add_column("Views")
        table.add_column("Status")
        table.add_column("Author")
        table.add_column("Chapters")

        genres = ", ".join(x for x in novel.genres)
        chapters_len = str(len(novel.chapters))

        table.add_row(novel.description, genres, str(novel.views), novel.status, novel.author, chapters_len)

        console.print(table, justify="center")

        if not self.__prompt_confirm(chapters_len):
            return 

        console.print(f"[bold violet]Downloading {chapters_len} chapters, it may take a while...[/bold violet]")

        total_downloaded = 0

        for ch_i in range(len(novel.chapters)):
            try:
                ch = Chapter(**novel.chapters[ch_i])
                ch_content = await get_read(ch.id)

                if not ch_content:
                    console.print(f"[bold red]Failed to download {ch.title} ({ch.id})[/bold red]")
                    continue
                
                file_extension = await get_config("file_extension") or ".txt"
                text = ch_content.text
                path = pathlib.Path(f"./termshared/downloads/{novel.title}@{novel.id}" + f"/{ch_content.chapterTitle}f{file_extension}")
                path.parent.mkdir(parents=True, exist_ok=True)

                if not path.exists():
                    async with aiofiles.open(path.as_posix(), "w") as file:
                        await file.write(text)
                        console.print(f"[bold violet]{ch_content.chapterTitle} has been downloaded[/bold violet]")
                        total_downloaded += 1
                else:
                    console.print(f"[bold violet]{ch_content.chapterTitle} is already downloaded. Skipping...")

            except Exception as e:
                console.print(f"[bold red]Failed to download chapter {ch_i + 1}[/bold red]")
                logging.error(f"Failed to download chapter {ch_i + 1} because {e}")

        console.print(f"[bold red]{total_downloaded}/{chapters_len}[/bold red] [bold green]chapters have been downloaded![/bold green]")

    async def call(self, console: Console) -> None:
        await self.__search(console)
        await self.__prompt_id(console)
