from abc import ABC, abstractmethod
import discord


class OnMemberJoinABC(ABC):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    async def on_member_join(self, member: discord.Member):
        pass
