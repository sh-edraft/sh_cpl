from abc import ABC, abstractmethod
import discord


class OnMemberBanABC(ABC):

    @abstractmethod
    def __init__(self): pass

    @abstractmethod
    async def on_member_ban(self, guild: discord.Guild, user: discord.User): pass
