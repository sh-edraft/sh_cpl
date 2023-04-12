from abc import ABC, abstractmethod
import discord


class OnPrivateChannelCreateABC(ABC):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    async def on_private_channel_create(self, channel: discord.abc.PrivateChannel):
        pass
