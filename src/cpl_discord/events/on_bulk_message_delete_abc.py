from abc import ABC, abstractmethod
import discord


class OnBulkMessageDeleteABC(ABC):

    @abstractmethod
    def __init__(self): pass

    @abstractmethod
    async def on_bulk_message_delete(self, messages: list[discord.Message]): pass
