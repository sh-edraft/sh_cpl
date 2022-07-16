from abc import ABC, abstractmethod
import discord


class OnGuildIntegrationsUpdateABC(ABC):

    @abstractmethod
    def __init__(self): pass

    @abstractmethod
    async def on_guild_integrations_update(self, guild: discord.Guild): pass
    