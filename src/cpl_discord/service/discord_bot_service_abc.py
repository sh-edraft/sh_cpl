from abc import abstractmethod

from discord.ext import commands

from cpl_discord.container.guild import Guild
from cpl_query.extension.list import List


class DiscordBotServiceABC(commands.Bot):

    def __init__(self, *args, **kwargs):
        commands.Bot.__init__(self, *args, **kwargs)

    @abstractmethod
    async def start_async(self): pass

    @abstractmethod
    async def stop_async(self): pass

    @abstractmethod
    async def on_ready(self): pass

    @property
    @abstractmethod
    def guilds(self) -> List[Guild]: pass
