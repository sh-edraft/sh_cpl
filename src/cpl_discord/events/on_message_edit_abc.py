from abc import ABC, abstractmethod
import discord


class OnMessageEditABC(ABC):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    async def on_message_edit(self, before: discord.Message, after: discord.Message):
        pass
