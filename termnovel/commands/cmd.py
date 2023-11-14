from rich.console import Console

class NotImplemented(Exception):
    """
    Raise when the method body is not defined
    """

class Meta:
    def __init__(self, name, description) -> None:
        self.name = name 
        self.description = description

class TermCommand:
    """
    Base command class
    """
    def meta(self) -> Meta:
        raise NotImplemented("Meta data is not defined")
    
    async def call(self, console: Console) -> None:
        raise NotImplemented("Command body is not defined")