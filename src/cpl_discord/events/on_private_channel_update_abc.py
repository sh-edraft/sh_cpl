from abc import ABC, abstractmethod
import discord


class OnPrivateChannelUpdateABC(ABC):

    @abstractmethod
    def __init__(self): pass

    @abstractmethod
    async def on_private_channel_update(self, before: discord.GroupChannel, after: discord.GroupChannel): pass
    