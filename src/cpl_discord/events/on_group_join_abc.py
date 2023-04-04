from abc import ABC, abstractmethod
import discord


class OnGroupJoinABC(ABC):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    async def on_group_join(self, channel: discord.GroupChannel, user: discord.User):
        pass
