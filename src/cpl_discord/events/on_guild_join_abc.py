from abc import ABC, abstractmethod
import discord


class OnGuildJoinABC(ABC):

    @abstractmethod
    def __init__(self): pass

    @abstractmethod
    async def on_guild_join(self, guild: discord.Guild): pass
