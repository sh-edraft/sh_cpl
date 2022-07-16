from abc import ABC, abstractmethod
import discord


class OnUserUpdateABC(ABC):

    @abstractmethod
    def __init__(self): pass

    @abstractmethod
    async def on_user_update(self, before: discord.User, after: discord.User): pass
