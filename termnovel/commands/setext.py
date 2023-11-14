from rich.console import Console
from rich.prompt import Prompt
from termnovel.commands.cmd import TermCommand, Meta

import json 
from termnovel.config import save_to_config

class SetExtCommand(TermCommand):
    def meta(self) -> Meta:
        return Meta(
            name="set-extension",
            description="Set the file extension which will be applied when a new chapter is downloaded"
        )
    
    def __is_valid_ext(self, ext: str) -> bool:
        return ext.startswith(".")
    
    def __prompt_ext(self, console: Console) -> str:
        prompt = Prompt.ask("Enter the file extension")

        if not self.__is_valid_ext(prompt):
            console.print("[bold red]This is not a valid file extension, an extension should start with a period, e.g, .txt[/bold red]")
            self.__prompt_ext(console)
            return 
        return prompt
    

    async def call(self, console: Console) -> None:
        ext = self.__prompt_ext(console)
        config = json.dumps({
            "file_extension": ext
        })
        await save_to_config(console, config)
