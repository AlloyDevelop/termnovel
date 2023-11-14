import sys
from rich.console import Console
from rich.panel import Panel
from rich.table import Table 

from termnovel.commands.download import DownloadCommand
from termnovel.commands.setext import SetExtCommand

import asyncio 
import logging 

commands = [
    DownloadCommand(),
    SetExtCommand()
]

def init():
    """
    Factory method
    """
    console = Console()
    args = sys.argv
    logging.basicConfig(filename="termnovel.logs", encoding="utf-8", level=logging.DEBUG, format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

    logging.info("Application startup complete")

    if len(args) == 1:
        console.clear()
        console.print("[bold violet]Hey! Welcome to TermNovel, a way to download light novels from your terminal. You can use the commands below to get started.\n[/bold violet]", justify="center")
        

        console.print("[bold violet]Author: @AlloyDevelop[/bold violet]", justify="right")

        table = Table(title="Available commands")
        table.add_column("Command", style="bold")
        table.add_column("Description")

        for cmd in commands:
            meta = cmd.meta()
            table.add_row(meta.name, meta.description)
        
        panel = Panel.fit(table, title="TermNovel: LN from terminal", border_style="violet")
        console.print(panel, justify="center")
    elif len(args) > 1:
        for command in commands:
            meta = command.meta()
            
            if args[1] == meta.name:
                try:
                    asyncio.run(command.call(console))
                    logging.info(f"Running command: {meta.name} | Executed by the user")
                except Exception as e:
                    logging.error(f"Error while running command {meta.name}: {e}")
            
if __name__ == '__main__':
    try:
        init()
    except KeyboardInterrupt:
        print('\n')
        sys.exit(0)