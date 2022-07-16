from abc import ABC, abstractmethod
import discord


class OnGuildRemoveABC(ABC):

    @abstractmethod
    def __init__(self): pass
    @abstractmethod
    async def on_guild_remove(self, guild: discord.Guild): pass
