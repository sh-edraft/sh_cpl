from abc import ABC, abstractmethod
import discord


class OnMessageABC(ABC):

    @abstractmethod
    def __init__(self): pass
    
    @abstractmethod
    async def on_message(self, message: discord.Message): pass
