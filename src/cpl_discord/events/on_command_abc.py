from abc import ABC, abstractmethod

from discord.ext.commands import Context


class OnCommandABC(ABC):

    @abstractmethod
    def __init__(self): pass

    @abstractmethod
    async def on_command(self, ctx: Context): pass
