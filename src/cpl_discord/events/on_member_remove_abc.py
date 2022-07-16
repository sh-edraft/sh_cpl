from abc import ABC, abstractmethod
import discord


class OnMemberRemoveABC(ABC):

    @abstractmethod
    def __init__(self): pass

    @abstractmethod
    async def on_member_remove(self, member: discord.Member): pass
