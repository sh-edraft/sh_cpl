from abc import ABC, abstractmethod
import discord


class OnMemberUnbanABC(ABC):

    @abstractmethod
    def __init__(self): pass

    @abstractmethod
    async def on_member_unban(self, guild: discord.Guild, user: discord.User): pass
