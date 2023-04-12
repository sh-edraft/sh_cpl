from abc import ABC, abstractmethod
import discord


class OnGuildAvailableABC(ABC):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    async def on_guild_available(self, guild: discord.Guild):
        pass
