from abc import ABC, abstractmethod
import discord


class OnGuildUpdateABC(ABC):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    async def on_guild_update(self, before: discord.Guild, after: discord.Guild):
        pass
