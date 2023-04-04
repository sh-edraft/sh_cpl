from abc import ABC, abstractmethod
import discord


class OnGuildRoleCreateABC(ABC):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    async def on_guild_role_create(self, role: discord.Role):
        pass
