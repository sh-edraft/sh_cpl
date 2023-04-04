from abc import ABC, abstractmethod
import discord


class OnMemberUpdateABC(ABC):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    async def on_member_update(self, before: discord.Member, after: discord.Member):
        pass
