from abc import ABC, abstractmethod
import discord


class OnPrivateChannelDeleteABC(ABC):

    @abstractmethod
    def __init__(self): pass

    @abstractmethod
    async def on_private_channel_delete(self, channel: discord.abc.PrivateChannel): pass
    
