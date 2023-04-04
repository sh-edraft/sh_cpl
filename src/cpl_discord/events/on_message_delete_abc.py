from abc import ABC, abstractmethod
import discord


class OnMessageDeleteABC(ABC):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    async def on_message_delete(self, message: discord.Message):
        pass
