from abc import ABC, abstractmethod

from discord.ext.commands import Context, CommandError


class OnCommandCompletionABC(ABC):

    @abstractmethod
    def __init__(self): pass

    @abstractmethod
    async def on_command_completion(self, ctx: Context): pass
