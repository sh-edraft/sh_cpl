from abc import ABC, abstractmethod

from discord.ext.commands import Context, CommandError


class OnCommandErrorABC(ABC):

    @abstractmethod
    def __init__(self): pass

    @abstractmethod
    async def on_command_error(self, ctx: Context, error: CommandError): pass
