from abc import ABC, abstractmethod
import discord


class OnGuildRoleUpdateABC(ABC):

    @abstractmethod
    def __init__(self): pass

    @abstractmethod
    async def on_guild_role_update(self, before: discord.Role, after: discord.Role): pass
