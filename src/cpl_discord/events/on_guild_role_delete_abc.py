from abc import ABC, abstractmethod
import discord


class OnGuildRoleDeleteABC(ABC):

    @abstractmethod
    def __init__(self): pass

    @abstractmethod
    async def on_guild_role_delete(self, role: discord.Role): pass
