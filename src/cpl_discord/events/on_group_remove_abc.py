from abc import ABC, abstractmethod
import discord


class OnGroupRemoveABC(ABC):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    async def on_group_remove(self, chhanel: discord.GroupChannel, user: discord.User):
        pass
